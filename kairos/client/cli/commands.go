package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"
	"time"

	"github.com/spf13/cobra"
	"kairos/client/shared"
	"kairos/timew"
)

var proxyURL string

func callHTTP(endpoint string, args map[string]any) (string, error) {
	url := fmt.Sprintf("http://%s%s", proxyURL, endpoint)
	jsonData, err := json.Marshal(args)
	if err != nil {
		return "", fmt.Errorf("failed to marshal request: %w", err)
	}
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return "", fmt.Errorf("HTTP request failed: %w", err)
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to read response: %w", err)
	}
	var toolResp shared.ToolCallResponse
	if err := json.Unmarshal(body, &toolResp); err != nil {
		return "", fmt.Errorf("failed to unmarshal response: %w", err)
	}
	if !toolResp.Success {
		return "", fmt.Errorf("tool error: %s", toolResp.Error)
	}
	return toolResp.Output, nil
}

var rootCmd = &cobra.Command{
	Use:   "kairos-cli",
	Short: "CLI client for Kairos time tracking via proxy",
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
		output, err := callHTTP("/start", argsMap)
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
		output, err := callHTTP("/stop", argsMap)
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
		output, err := callHTTP("/modify", argsMap)
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
		output, err := callHTTP("/remove", argsMap)
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
		output, err := callHTTP("/summary", argsMap)
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
		output, err := callHTTP("/export", argsMap)
		if err != nil {
			log.Fatal(err)
		}
		var entries []timew.TimeEntry
		if json.Unmarshal([]byte(output), &entries) == nil {
			if len(entries) == 0 {
				fmt.Println("No entries found.")
				return
			}
			fmt.Println("Exported Time Entries:")
			fmt.Printf("%-5s %-20s %-20s %-20s %s\n", "ID", "Start", "End", "Tags", "Annotation")
			fmt.Println(strings.Repeat("-", 80))
			for _, e := range entries {
				tags := strings.Join(e.Tags, ", ")
				fmt.Printf("%-5s %-20s %-20s %-20s %s\n", e.ID, e.Start, e.End, tags, e.Annotation)
			}
		} else {
			fmt.Print(output)
		}
	},
}

var inspectCmd = &cobra.Command{
	Use:   "inspect",
	Short: "Inspect the currently running time tracker",
	Run: func(cmd *cobra.Command, args []string) {
		output, err := callHTTP("/inspect", map[string]any{})
		if err != nil {
			log.Fatal(err)
		}
		fmt.Print(output)
	},
}

func init() {
	rootCmd.PersistentFlags().StringVar(&proxyURL, "proxy-url", "localhost:8080", "URL to the proxy server")
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
	rootCmd.AddCommand(inspectCmd)
}
