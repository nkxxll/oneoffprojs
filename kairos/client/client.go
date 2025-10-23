package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/spf13/cobra"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

var url string

func connectToServer() (*mcp.ClientSession, error) {
	ctx := context.Background()
	client := mcp.NewClient(&mcp.Implementation{Name: "kairos-client", Version: "1.0.0"}, nil)
	transport := mcp.StreamableClientTransport{Endpoint: url}
	session, err := client.Connect(ctx, &transport, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to connect: %w", err)
	}
	return session, nil
}

func callTool(session *mcp.ClientSession, name string, args map[string]any) (string, error) {
	ctx := context.Background()
	params := &mcp.CallToolParams{
		Name:      name,
		Arguments: args,
	}
	res, err := session.CallTool(ctx, params)
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

var rootCmd = &cobra.Command{
	Use:   "kairos",
	Short: "CLI client for Kairos time tracking MCP server",
	PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
		return nil
	},
}

var startCmd = &cobra.Command{
	Use:   "start <name>",
	Short: "Start a timer with the given name",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		name := args[0]
		startTimeStr, _ := cmd.Flags().GetString("start-time")
		argsMap := map[string]any{"name": name}
		if startTimeStr != "" {
			startTime, err := time.Parse(time.RFC3339, startTimeStr)
			if err != nil {
				log.Fatal("Invalid start-time format, use RFC3339")
			}
			argsMap["start_time"] = startTime
		}
		session, err := connectToServer()
		if err != nil {
			log.Fatal(err)
		}
		defer session.Close()
		output, err := callTool(session, "start_timer", argsMap)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Print(output)
	},
}

var stopCmd = &cobra.Command{
	Use:   "stop",
	Short: "Stop the currently running timer",
	Run: func(cmd *cobra.Command, args []string) {
		stopTimeStr, _ := cmd.Flags().GetString("stop-time")
		argsMap := map[string]any{}
		if stopTimeStr != "" {
			stopTime, err := time.Parse(time.RFC3339, stopTimeStr)
			if err != nil {
				log.Fatal("Invalid stop-time format, use RFC3339")
			}
			argsMap["stop_time"] = stopTime
		}
		session, err := connectToServer()
		if err != nil {
			log.Fatal(err)
		}
		defer session.Close()
		output, err := callTool(session, "stop_timer", argsMap)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Print(output)
	},
}

var modifyCmd = &cobra.Command{
	Use:   "modify <id>",
	Short: "Modify an entry by ID",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		id := args[0]
		startTimeStr, _ := cmd.Flags().GetString("start-time")
		endTimeStr, _ := cmd.Flags().GetString("end-time")
		argsMap := map[string]any{"id": id}
		if startTimeStr != "" {
			startTime, err := time.Parse(time.RFC3339, startTimeStr)
			if err != nil {
				log.Fatal("Invalid start-time format, use RFC3339")
			}
			argsMap["start_time"] = startTime
		}
		if endTimeStr != "" {
			endTime, err := time.Parse(time.RFC3339, endTimeStr)
			if err != nil {
				log.Fatal("Invalid end-time format, use RFC3339")
			}
			argsMap["end_time"] = endTime
		}
		session, err := connectToServer()
		if err != nil {
			log.Fatal(err)
		}
		defer session.Close()
		output, err := callTool(session, "modify_entry", argsMap)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Print(output)
	},
}

var removeCmd = &cobra.Command{
	Use:   "remove <id>",
	Short: "Remove an entry by ID",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		id := args[0]
		argsMap := map[string]any{"id": id}
		session, err := connectToServer()
		if err != nil {
			log.Fatal(err)
		}
		defer session.Close()
		output, err := callTool(session, "remove_entry", argsMap)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Print(output)
	},
}

var summaryCmd = &cobra.Command{
	Use:   "summary <period>",
	Short: "Get summary for period (week, day, month)",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		period := args[0]
		argsMap := map[string]any{"period": period}
		session, err := connectToServer()
		if err != nil {
			log.Fatal(err)
		}
		defer session.Close()
		output, err := callTool(session, "summary", argsMap)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Print(output)
	},
}

var exportCmd = &cobra.Command{
	Use:   "export",
	Short: "Export time tracking data",
	Run: func(cmd *cobra.Command, args []string) {
		period, _ := cmd.Flags().GetString("period")
		fromStr, _ := cmd.Flags().GetString("from")
		toStr, _ := cmd.Flags().GetString("to")
		argsMap := map[string]any{}
		if period != "" {
			argsMap["period"] = period
		}
		if fromStr != "" {
			from, err := time.Parse(time.RFC3339, fromStr)
			if err != nil {
				log.Fatal("Invalid from format, use RFC3339")
			}
			argsMap["from"] = from
		}
		if toStr != "" {
			to, err := time.Parse(time.RFC3339, toStr)
			if err != nil {
				log.Fatal("Invalid to format, use RFC3339")
			}
			argsMap["to"] = to
		}
		session, err := connectToServer()
		if err != nil {
			log.Fatal(err)
		}
		defer session.Close()
		output, err := callTool(session, "export", argsMap)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Print(output)
	},
}

func init() {
	rootCmd.PersistentFlags().StringVar(&url, "url", "localhost:3000", "URL to the MCP server")
	startCmd.Flags().String("start-time", "", "Start time in RFC3339 format")
	stopCmd.Flags().String("stop-time", "", "Stop time in RFC3339 format")
	modifyCmd.Flags().String("start-time", "", "New start time in RFC3339 format")
	modifyCmd.Flags().String("end-time", "", "New end time in RFC3339 format")
	exportCmd.Flags().String("period", "", "Period for export (week, day, month)")
	exportCmd.Flags().String("from", "", "Start datetime for export in RFC3339 format")
	exportCmd.Flags().String("to", "", "End datetime for export in RFC3339 format")

	rootCmd.AddCommand(startCmd)
	rootCmd.AddCommand(stopCmd)
	rootCmd.AddCommand(modifyCmd)
	rootCmd.AddCommand(removeCmd)
	rootCmd.AddCommand(summaryCmd)
	rootCmd.AddCommand(exportCmd)
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		log.Fatal(err)
	}
}
