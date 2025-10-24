package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/modelcontextprotocol/go-sdk/mcp"
	"kairos/client/shared"
)

type Server struct {
	session *mcp.ClientSession
}

func NewServer(mcpURL string) (*Server, error) {
	ctx := context.Background()
	client := mcp.NewClient(&mcp.Implementation{Name: "kairos-proxy", Version: "1.0.0"}, nil)
	transport := mcp.StreamableClientTransport{Endpoint: mcpURL}
	session, err := client.Connect(ctx, &transport, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to MCP server: %w", err)
	}
	return &Server{session: session}, nil
}

func (s *Server) callTool(name string, args map[string]any) (string, error) {
	ctx := context.Background()
	params := &mcp.CallToolParams{
		Name:      name,
		Arguments: args,
	}
	res, err := s.session.CallTool(ctx, params)
	if err != nil {
		return "", fmt.Errorf("CallTool failed: %w", err)
	}
	if res.IsError {
		return "", fmt.Errorf("tool failed")
	}
	var output string
	for _, c := range res.Content {
		if text, ok := c.(*mcp.TextContent); ok {
			output += text.Text + "\n"
		}
	}
	return output, nil
}

func (s *Server) handleTool(toolName string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}
		var req map[string]any
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Invalid JSON", http.StatusBadRequest)
			return
		}
		output, err := s.callTool(toolName, req)
		resp := shared.ToolCallResponse{Success: err == nil, Output: output}
		if err != nil {
			resp.Error = err.Error()
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(resp)
	}
}

func (s *Server) setupRoutes() {
	http.HandleFunc("/start", s.handleTool("start_timer"))
	http.HandleFunc("/stop", s.handleTool("stop_timer"))
	http.HandleFunc("/modify", s.handleTool("modify_entry"))
	http.HandleFunc("/remove", s.handleTool("remove_entry"))
	http.HandleFunc("/summary", s.handleTool("summary"))
	http.HandleFunc("/export", s.handleTool("export"))
	http.HandleFunc("/inspect", s.handleTool("inspect_tracker"))
}
