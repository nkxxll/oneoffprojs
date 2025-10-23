package main

import (
	"log"

	"kairos/tmcp"
)

func main() {
	log.Println("Starting MCP server...")
	if err := tmcp.RunServer(); err != nil {
		log.Fatal(err)
	}
}
