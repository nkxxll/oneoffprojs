package main

import (
	"flag"
	"kairos/tmcp"
	"log"
)

func main() {
	url := flag.String("u", "localhost:3000", "url for the server")
	log.Println("Starting MCP server...")
	if err := tmcp.RunServer(*url); err != nil {
		log.Fatal(err)
	}
}
