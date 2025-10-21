package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/joho/godotenv"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type Config struct {
	remote string
}

func NewConfig() Config {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	mcpRemote := os.Getenv("MCP_REMOTE")
	if mcpRemote == "" {
		panic("The remote has to be set!")
	}
	return Config{remote: mcpRemote}
}

type Input struct {
	Name string `json:"name" jsonschema:"the name of the person to greet"`
}

type Output struct {
	Greeting string `json:"greeting" jsonschema:"the greeting to tell to the user"`
}

func WrapFuncWithClient(cc context.Context, cs *mcp.ClientSession) mcp.ToolHandlerFor[Input, Output] {
	handler := func(ctx context.Context, req *mcp.CallToolRequest, input Input) (
		*mcp.CallToolResult,
		Output,
		error,
	) {

		result, err := cs.CallTool(cc, &mcp.CallToolParams{
			Name:      req.Params.Name,
			Arguments: Input{Name: input.Name},
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
	config := NewConfig()
	ctx := context.Background()
	fmt.Println("Config", config)
	c := mcp.NewClient(&mcp.Implementation{Name: "mcp-client", Version: "v1.0.0"}, nil)
	session, err := c.Connect(ctx, &mcp.StreamableClientTransport{Endpoint: config.remote}, nil)
	if err != nil {
		panic("could not connect to server")
	}
	server := mcp.NewServer(&mcp.Implementation{Name: "proxyserver", Version: "v1.0.0"}, nil)
	mcp.AddTool(server, &mcp.Tool{Name: "greet", Description: "say hi"}, WrapFuncWithClient(ctx, session))
	// Run the server over stdin/stdout, until the client disconnects.
	if err := server.Run(context.Background(), &mcp.StdioTransport{}); err != nil {
		log.Fatal(err)
	}
}
