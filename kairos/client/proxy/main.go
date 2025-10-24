package main

import (
	"flag"
	"log"
	"net/http"
)

func main() {
	mcpURL := flag.String("mcp-url", "localhost:3000", "URL to the MCP server")
	port := flag.String("port", "8080", "Port for proxy server")
	flag.Parse()

	server, err := NewServer(*mcpURL)
	if err != nil {
		log.Fatal(err)
	}
	defer server.session.Close()

	server.setupRoutes()

	log.Printf("Starting proxy server on :%s, connecting to MCP at %s", *port, *mcpURL)
	log.Fatal(http.ListenAndServe(":"+*port, nil))
}
