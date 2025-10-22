package main

import (
	"context"
	"fmt"
	"log/slog"
	"os"
	"path/filepath"
	"strings"

	"github.com/BurntSushi/toml"
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

type Input struct {
	Name string `json:"name" jsonschema:"the name of the person to greet"`
}

type Output struct {
	Greeting string `json:"greeting" jsonschema:"the greeting to tell to the user"`
}

type ServerState struct {
	Client  *mcp.Client
	Session *mcp.ClientSession
	Name    string
	Ctx     context.Context
}

// todo this function is not generic it is very adjusted to the example code
// can you make it generic for any input and output
func WrapFuncWithClient(cc context.Context, cs *mcp.ClientSession, serverName string, logger *slog.Logger) mcp.ToolHandlerFor[Input, Output] {
	handler := func(ctx context.Context, req *mcp.CallToolRequest, input Input) (
		*mcp.CallToolResult,
		Output,
		error,
	) {
		toolName := strings.TrimPrefix(req.Params.Name, serverName+"-")
		result, err := cs.CallTool(cc, &mcp.CallToolParams{
			Name:      toolName,
			Arguments: req.Params.Arguments,
		})
		if err != nil {
			return nil, Output{""}, err
		}
		if textContent, ok := result.Content[0].(*mcp.TextContent); ok {
			return nil, Output{Greeting: textContent.Text}, nil
		}
		return nil, Output{""}, fmt.Errorf("Content type does not fit")
	}
	return handler
}

func main() {
	logger := slog.New(slog.NewTextHandler(os.Stderr, nil))
	config := NewConfig(logger)
	logger.Info(fmt.Sprintln("Config", config))
	server := mcp.NewServer(&mcp.Implementation{Name: "proxyserver", Version: "v1.0.0"}, nil)
	var states []ServerState
	for _, srv := range config.Servers {
		ctx := context.Background()
		c := mcp.NewClient(&mcp.Implementation{Name: "mcp-client", Version: "v1.0.0"}, nil)
		session, err := c.Connect(ctx, &mcp.StreamableClientTransport{Endpoint: srv.URL}, nil)
		if err != nil {
			logger.Error("could not connect to server", "server", srv.Name, "error", err)
			continue
		}
		states = append(states, ServerState{Client: c, Session: session, Name: srv.Name, Ctx: ctx})

		tools, err := session.ListTools(ctx, &mcp.ListToolsParams{})
		if err != nil {
			logger.Error("could not list tools", "server", srv.Name, "error", err)
			continue
		}

		toolNames := make([]string, len(tools.Tools))
		for i, tool := range tools.Tools {
			toolNames[i] = tool.Name
		}
		logger.Info("tools available", "server", srv.Name, "count", len(tools.Tools), "tools", toolNames)

		for _, tool := range tools.Tools {
			if tool.Name == "greet" {
				prefixedTool := &mcp.Tool{
					Name:        srv.Name + "-" + tool.Name,
					Description: tool.Description,
					InputSchema: tool.InputSchema,
				}
				mcp.AddTool(server, prefixedTool, WrapFuncWithClient(ctx, session, srv.Name, logger))
			}
		}
	}
	if len(states) == 0 {
		logger.Error("no servers connected")
		panic("no servers connected")
	}
	if err := server.Run(context.Background(), &mcp.StdioTransport{}); err != nil {
		logger.Error(fmt.Sprintf("%+v\n", err))
		panic("error in mcp server exiting...")
	}
}
