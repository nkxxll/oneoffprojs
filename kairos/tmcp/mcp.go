package tmcp

import (
	"context"
	"fmt"
	"kairos/timew"
	"log"
	"net/http"
	"time"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

// Input and output structs for tools

type StartTimerInput struct {
	Name      string     `json:"name" jsonschema:"the name of the timer to start"`
	StartTime *time.Time `json:"start_time,omitempty" jsonschema:"optional start time for the timer"`
}

type StartTimerOutput struct {
	Message string `json:"message" jsonschema:"the result message"`
}

type StopTimerInput struct {
	StopTime *time.Time `json:"stop_time,omitempty" jsonschema:"optional stop time for the timer"`
}

type StopTimerOutput struct {
	Message string `json:"message" jsonschema:"the result message"`
}

type ModifyEntryInput struct {
	ID        string     `json:"id" jsonschema:"the ID of the entry to modify"`
	StartTime *time.Time `json:"start_time,omitempty" jsonschema:"new start time for the entry"`
	EndTime   *time.Time `json:"end_time,omitempty" jsonschema:"new end time for the entry"`
}

type ModifyEntryOutput struct {
	Message string `json:"message" jsonschema:"the result message"`
}

type RemoveEntryInput struct {
	ID string `json:"id" jsonschema:"the ID of the entry to remove"`
}

type RemoveEntryOutput struct {
	Message string `json:"message" jsonschema:"the result message"`
}

type SummaryInput struct {
	Period string `json:"period" jsonschema:"the period for summary: week, day, month"`
}

type SummaryOutput struct {
	Summary string `json:"summary" jsonschema:"the summary data"`
}

type ExportInput struct {
	Period string     `json:"period,omitempty" jsonschema:"the period for export: week, day, month"`
	From   *time.Time `json:"from,omitempty" jsonschema:"start datetime for export range"`
	To     *time.Time `json:"to,omitempty" jsonschema:"end datetime for export range"`
}

type ExportOutput struct {
	Export string `json:"export" jsonschema:"the exported data"`
}

type InspectTrackerInput struct {
}

type InspectTrackerOutput struct {
	Status string `json:"status" jsonschema:"the current status of the time tracker"`
}

// Handlers

func HandleStartTimer(ctx context.Context, req *mcp.CallToolRequest, input StartTimerInput) (*mcp.CallToolResult, StartTimerOutput, error) {
	err := timew.StartTimer(input.Name, input.StartTime)
	if err != nil {
		return nil, StartTimerOutput{}, err
	}
	return nil, StartTimerOutput{Message: fmt.Sprintf("Timer '%s' started successfully", input.Name)}, nil
}

func HandleStopTimer(ctx context.Context, req *mcp.CallToolRequest, input StopTimerInput) (*mcp.CallToolResult, StopTimerOutput, error) {
	err := timew.StopTimer(input.StopTime)
	if err != nil {
		return nil, StopTimerOutput{}, err
	}
	return nil, StopTimerOutput{Message: "Timer stopped successfully"}, nil
}

func HandleModifyEntry(ctx context.Context, req *mcp.CallToolRequest, input ModifyEntryInput) (*mcp.CallToolResult, ModifyEntryOutput, error) {
	err := timew.ModifyEntry(input.ID, input.StartTime, input.EndTime)
	if err != nil {
		return nil, ModifyEntryOutput{}, err
	}
	return nil, ModifyEntryOutput{Message: fmt.Sprintf("Entry '%s' modified successfully", input.ID)}, nil
}

func HandleRemoveEntry(ctx context.Context, req *mcp.CallToolRequest, input RemoveEntryInput) (*mcp.CallToolResult, RemoveEntryOutput, error) {
	err := timew.RemoveEntry(input.ID)
	if err != nil {
		return nil, RemoveEntryOutput{}, err
	}
	return nil, RemoveEntryOutput{Message: fmt.Sprintf("Entry '%s' removed successfully", input.ID)}, nil
}

func HandleSummary(ctx context.Context, req *mcp.CallToolRequest, input SummaryInput) (*mcp.CallToolResult, SummaryOutput, error) {
	summary, err := timew.Summary(input.Period)
	if err != nil {
		return nil, SummaryOutput{}, err
	}
	return nil, SummaryOutput{Summary: summary}, nil
}

func HandleExport(ctx context.Context, req *mcp.CallToolRequest, input ExportInput) (*mcp.CallToolResult, ExportOutput, error) {
	export, err := timew.Export(input.Period, input.From, input.To)
	if err != nil {
		return nil, ExportOutput{}, err
	}
	return nil, ExportOutput{Export: export}, nil
}

func HandleInspectTracker(ctx context.Context, req *mcp.CallToolRequest, input InspectTrackerInput) (*mcp.CallToolResult, InspectTrackerOutput, error) {
	status, err := timew.InspectTracker()
	if err != nil {
		return nil, InspectTrackerOutput{}, err
	}
	return nil, InspectTrackerOutput{Status: status}, nil
}

// CreateServer creates and returns the MCP server with all tools
func CreateServer() *mcp.Server {
	server := mcp.NewServer(&mcp.Implementation{Name: "kairos-timew", Version: "1.0.0"}, nil)

	// Add tools
	mcp.AddTool(server, &mcp.Tool{Name: "start_timer", Description: "Start a new timer with a given name, optionally at a specific start time"}, HandleStartTimer)
	mcp.AddTool(server, &mcp.Tool{Name: "stop_timer", Description: "Stop the currently running timer, optionally at a specific stop time"}, HandleStopTimer)
	mcp.AddTool(server, &mcp.Tool{Name: "modify_entry", Description: "Modify the start or end time of an existing entry by ID"}, HandleModifyEntry)
	mcp.AddTool(server, &mcp.Tool{Name: "remove_entry", Description: "Remove an entry by ID"}, HandleRemoveEntry)
	mcp.AddTool(server, &mcp.Tool{Name: "summary", Description: "Get a summary of time tracking data for a period (week, day, month)"}, HandleSummary)
	mcp.AddTool(server, &mcp.Tool{Name: "export", Description: "Export time tracking entries for a period or date range"}, HandleExport)
	mcp.AddTool(server, &mcp.Tool{Name: "inspect_tracker", Description: "Inspect the currently running time tracker"}, HandleInspectTracker)

	return server
}

// responseWriter wraps http.ResponseWriter to capture the status code.
type responseWriter struct {
	http.ResponseWriter
	statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
	rw.statusCode = code
	rw.ResponseWriter.WriteHeader(code)
}

func loggingHandler(handler http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		// Create a response writer wrapper to capture status code.
		wrapped := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}

		// Log request details.
		log.Printf("[REQUEST] %s | %s | %s %s",
			start.Format(time.RFC3339),
			r.RemoteAddr,
			r.Method,
			r.URL.Path)

		// Call the actual handler.
		handler.ServeHTTP(wrapped, r)

		// Log response details.
		duration := time.Since(start)
		log.Printf("[RESPONSE] %s | %s | %s %s | Status: %d | Duration: %v",
			time.Now().Format(time.RFC3339),
			r.RemoteAddr,
			r.Method,
			r.URL.Path,
			wrapped.statusCode,
			duration)
	})
}

// RunServer runs the MCP server over stdio
func RunServer(url string) error {
	server := CreateServer()
	// Create the streamable HTTP handler.
	handler := mcp.NewStreamableHTTPHandler(func(req *http.Request) *mcp.Server {
		return server
	}, nil)

	handlerWithLogging := loggingHandler(handler)
	// Start the HTTP server with logging handler.
	return http.ListenAndServe(url, handlerWithLogging)
}
