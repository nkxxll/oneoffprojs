package shared

import (
	"time"
)

// ToolCallRequest represents a request to call an MCP tool
type ToolCallRequest struct {
	ToolName  string         `json:"tool_name"`
	Arguments map[string]any `json:"arguments"`
}

// ToolCallResponse represents the response from a tool call
type ToolCallResponse struct {
	Success bool   `json:"success"`
	Output  string `json:"output"`
	Error   string `json:"error,omitempty"`
}

// TimeEntry represents a time tracking entry
type TimeEntry struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	StartTime time.Time `json:"start_time"`
	EndTime   *time.Time `json:"end_time,omitempty"`
}

// SummaryPeriod represents a summary request
type SummaryPeriod struct {
	Period string `json:"period"` // "day", "week", "month"
}

// ExportRequest represents an export request
type ExportRequest struct {
	Period string     `json:"period,omitempty"`
	From   *time.Time `json:"from,omitempty"`
	To     *time.Time `json:"to,omitempty"`
}

// Config represents the CLI configuration
type Config struct {
	ProxyURL string `json:"proxy_url"`
}
