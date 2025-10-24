package main

import (
	"flag"
	"kairos/tmcp"
	"log"
)

func main() {
	url := flag.String("url", "localhost:3000", "url for the server")
	flag.Parse()
	log.Printf("Starting MCP server... at %s", *url)
	if err := tmcp.RunServer(*url); err != nil {
		log.Fatal(err)
	}
}
