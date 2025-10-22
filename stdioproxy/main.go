package main

import (
	"context"
	"fmt"
	"log/slog"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"github.com/BurntSushi/toml"
	"github.com/fsnotify/fsnotify"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

// config toml is a list of mcp server with their name and their ip address/url
type McpServer struct {
	Name string `toml:"name"`
	URL  string `toml:"url"`
}

type McpServers []McpServer

type Config struct {
	Servers McpServers `toml:"servers"`
}

func loadConfig(logger *slog.Logger) Config {
	home, err := os.UserHomeDir()
	if err != nil {
		logger.Error("could not get home dir", "error", err)
		return Config{}
	}
	configPath := filepath.Join(home, ".config", "stdioproxy", "config.toml")
	var config Config
	if _, err := toml.DecodeFile(configPath, &config); err != nil {
		logger.Error("failed to load config", "error", err)
		return Config{}
	}
	return config
}

func NewConfig(logger *slog.Logger) Config {
	return loadConfig(logger)
}

type ServerState struct {
	Client  *mcp.Client
	Session *mcp.ClientSession
	Name    string
	Ctx     context.Context
	Tools   []*mcp.Tool
}

type ServerManager struct {
	mu       sync.RWMutex
	servers  map[string]*ServerState
	server   *mcp.Server
	logger   *slog.Logger
	config   Config
}

func WrapFuncWithClient(cc context.Context, cs *mcp.ClientSession, serverName string, logger *slog.Logger) mcp.ToolHandlerFor[any, any] {
	handler := func(ctx context.Context, req *mcp.CallToolRequest, input any) (
		*mcp.CallToolResult,
		any,
		error,
	) {
		toolName := strings.TrimPrefix(req.Params.Name, serverName+"-")
		result, err := cs.CallTool(cc, &mcp.CallToolParams{
			Name:      toolName,
			Arguments: req.Params.Arguments,
		})
		if err != nil {
			return nil, nil, err
		}
		if len(result.Content) == 0 {
			return nil, nil, fmt.Errorf("no content in result")
		}
		// Forward the content from the remote result
		return nil, result.Content, nil
	}
	return handler
}

func NewServerManager(server *mcp.Server, logger *slog.Logger, config Config) *ServerManager {
	return &ServerManager{
		servers: make(map[string]*ServerState),
		server:  server,
		logger:  logger,
		config:  config,
	}
}

func (sm *ServerManager) ConnectServer(serverConfig McpServer) error {
	sm.mu.Lock()
	defer sm.mu.Unlock()

	if _, exists := sm.servers[serverConfig.Name]; exists {
		sm.logger.Info("server already connected", "server", serverConfig.Name)
		return nil
	}

	sm.logger.Info("connecting to server", "server", serverConfig.Name, "url", serverConfig.URL)

	ctx := context.Background()
	c := mcp.NewClient(&mcp.Implementation{Name: "mcp-client", Version: "v1.0.0"}, nil)
	session, err := c.Connect(ctx, &mcp.StreamableClientTransport{Endpoint: serverConfig.URL}, nil)
	if err != nil {
		sm.logger.Error("could not connect to server", "server", serverConfig.Name, "error", err)
		return err
	}

	tools, err := session.ListTools(ctx, &mcp.ListToolsParams{})
	if err != nil {
		sm.logger.Error("could not list tools", "server", serverConfig.Name, "error", err)
		session.Close()
		return err
	}

	var prefixedTools []*mcp.Tool
	toolNames := make([]string, len(tools.Tools))
	for i, tool := range tools.Tools {
		toolNames[i] = tool.Name
		prefixedTool := &mcp.Tool{
			Name:        serverConfig.Name + "-" + tool.Name,
			Description: tool.Description,
			InputSchema: tool.InputSchema,
		}
		prefixedTools = append(prefixedTools, prefixedTool)
		mcp.AddTool(sm.server, prefixedTool, WrapFuncWithClient(ctx, session, serverConfig.Name, sm.logger))
	}

	sm.servers[serverConfig.Name] = &ServerState{
		Client:  c,
		Session: session,
		Name:    serverConfig.Name,
		Ctx:     ctx,
		Tools:   prefixedTools,
	}

	sm.logger.Info("server connected successfully", "server", serverConfig.Name, "tools", toolNames)
	return nil
}

func (sm *ServerManager) DisconnectServer(serverName string) error {
	sm.mu.Lock()
	defer sm.mu.Unlock()

	state, exists := sm.servers[serverName]
	if !exists {
		sm.logger.Info("server not connected", "server", serverName)
		return nil
	}

	sm.logger.Info("disconnecting server", "server", serverName)

	// Remove tools from server
	for _, tool := range state.Tools {
		sm.server.RemoveTools(tool.Name)
	}

	// Close session
	state.Session.Close()

	delete(sm.servers, serverName)
	sm.logger.Info("server disconnected", "server", serverName)
	return nil
}

func (sm *ServerManager) ReloadConfig(newConfig Config) {
	sm.mu.Lock()
	defer sm.mu.Unlock()

	sm.logger.Info("reloading config")

	// Create maps for current and new servers
	currentServers := make(map[string]bool)
	for name := range sm.servers {
		currentServers[name] = true
	}

	newServers := make(map[string]McpServer)
	for _, srv := range newConfig.Servers {
		newServers[srv.Name] = srv
	}

	// Disconnect servers that are no longer in config
	for name := range currentServers {
		if _, exists := newServers[name]; !exists {
			sm.DisconnectServer(name)
		}
	}

	// Connect new servers or update existing ones
	for name, srv := range newServers {
		if _, exists := currentServers[name]; !exists {
			// New server
			if err := sm.ConnectServer(srv); err != nil {
				sm.logger.Error("failed to connect new server", "server", name, "error", err)
			}
		} else {
			// TODO: Check if URL changed and reconnect if necessary
			sm.logger.Info("server already connected, skipping", "server", name)
		}
	}
	// TODO: we have to notfify the client from the proxy here that there is a
	// new list of tools else we only have the new server in the local
	// capabilities and the client of the proxy still does not know that there
	// are new tools

	sm.config = newConfig
	sm.logger.Info("config reloaded")
}

func watchConfig(configPath string, manager *ServerManager, logger *slog.Logger) {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		logger.Error("failed to create watcher", "error", err)
		return
	}
	defer watcher.Close()

	err = watcher.Add(configPath)
	if err != nil {
		logger.Error("failed to watch config file", "error", err)
		return
	}

	logger.Info("watching config file", "path", configPath)

	var debounceTimer *time.Timer
	debounceDuration := 1000 * time.Millisecond

	for {
		select {
		case event, ok := <-watcher.Events:
			if !ok {
				return
			}
			if event.Has(fsnotify.Write) {
				// Debounce rapid writes
				if debounceTimer != nil {
					debounceTimer.Stop()
				}
				debounceTimer = time.AfterFunc(debounceDuration, func() {
					newConfig := loadConfig(logger)
					if newConfig.Servers == nil {
						logger.Error("invalid config loaded")
						return
					}
					manager.ReloadConfig(newConfig)
				})
			}
		case err, ok := <-watcher.Errors:
			if !ok {
				return
			}
			logger.Error("watcher error", "error", err)
		}
	}
}

func main() {
	logger := slog.New(slog.NewTextHandler(os.Stderr, nil))
	config := NewConfig(logger)
	logger.Info(fmt.Sprintln("Config", config))

	server := mcp.NewServer(&mcp.Implementation{Name: "proxyserver", Version: "v1.0.0"}, nil)
	manager := NewServerManager(server, logger, config)

	// Connect initial servers
	for _, srv := range config.Servers {
		if err := manager.ConnectServer(srv); err != nil {
			logger.Error("failed to connect initial server", "server", srv.Name, "error", err)
		}
	}

	serverCount := len(manager.servers)

	if serverCount == 0 {
		logger.Error("no servers connected")
		panic("no servers connected")
	}

	// Start config watcher
	home, err := os.UserHomeDir()
	if err != nil {
		logger.Error("could not get home dir", "error", err)
		panic("could not get home dir")
	}
	configPath := filepath.Join(home, ".config", "stdioproxy", "config.toml")

	go watchConfig(configPath, manager, logger)

	if err := server.Run(context.Background(), &mcp.StdioTransport{}); err != nil {
		logger.Error(fmt.Sprintf("%+v\n", err))
		panic("error in mcp server exiting...")
	}
}
