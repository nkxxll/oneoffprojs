package tmcp

import (
	"context"
	"fmt"
	"time"

	"github.com/modelcontextprotocol/go-sdk/mcp"
	"kairos/timew"
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

	return server
}

// RunServer runs the MCP server over stdio
func RunServer() error {
	server := CreateServer()
	return server.Run(context.Background(), &mcp.StdioTransport{})
}
