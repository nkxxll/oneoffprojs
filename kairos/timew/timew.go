package timew

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os/exec"
	"strings"
	"time"
)

// TimeEntry represents a single time tracking entry
type TimeEntry struct {
	ID         string        `json:"id"`
	Start      string        `json:"start"`
	End        string        `json:"end"`
	Tags       []string      `json:"tags"`
	Annotation string        `json:"annotation"`
	Duration   time.Duration `json:"-"` // Calculated field, not in JSON
}

// TimeRange represents a time interval
type TimeRange struct {
	Start *time.Time
	End   *time.Time
}

// CommandResult encapsulates CLI command execution results
type CommandResult struct {
	Success bool
	Output  string
	Error   string
}

// TimeEntryList is a slice of TimeEntry with methods
type TimeEntryList []TimeEntry

// OperationStatus enumeration
type OperationStatus int

const (
	StatusActive OperationStatus = iota
	StatusCompleted
	StatusError
)

// ExecuteCommand executes a timew command and returns the result
func ExecuteCommand(args []string) (CommandResult, error) {
	cmd := exec.Command("timew", args...)
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err := cmd.Run()
	success := err == nil
	output := strings.TrimSpace(stdout.String())
	errorMsg := strings.TrimSpace(stderr.String())

	return CommandResult{
		Success: success,
		Output:  output,
		Error:   errorMsg,
	}, err
}

// StartTimer starts a new timer with optional start time and hint
func StartTimer(name string, startTime *time.Time) error {
	args := []string{"start", name}
	if startTime != nil {
		args = append(args, startTime.Format("2006-01-02T15:04:05"))
	}

	result, err := ExecuteCommand(args)
	if err != nil {
		return fmt.Errorf("failed to start timer: %s", result.Error)
	}
	return nil
}

// StopTimer stops the current timer with optional end time
func StopTimer(stopTime *time.Time) error {
	args := []string{"stop"}
	if stopTime != nil {
		args = append(args, stopTime.Format("2006-01-02T15:04:05"))
	}

	result, err := ExecuteCommand(args)
	if err != nil {
		return fmt.Errorf("failed to stop timer: %s", result.Error)
	}
	return nil
}

// ModifyEntry modifies an existing entry's start and/or end time
func ModifyEntry(id string, startTime, endTime *time.Time) error {
	if startTime != nil {
		args := []string{"modify", id, "start", startTime.Format("2006-01-02T15:04:05")}
		result, err := ExecuteCommand(args)
		if err != nil {
			return fmt.Errorf("failed to modify start time: %s", result.Error)
		}
	}
	if endTime != nil {
		args := []string{"modify", id, "end", endTime.Format("2006-01-02T15:04:05")}
		result, err := ExecuteCommand(args)
		if err != nil {
			return fmt.Errorf("failed to modify end time: %s", result.Error)
		}
	}
	return nil
}

// RemoveEntry deletes an entry by ID
func RemoveEntry(id string) error {
	args := []string{"delete", id}
	result, err := ExecuteCommand(args)
	if err != nil {
		return fmt.Errorf("failed to remove entry: %s", result.Error)
	}
	return nil
}

// ListEntries retrieves time entries, optionally filtered by time range
func ListEntries(filter TimeRange) (TimeEntryList, error) {
	args := []string{"export", "--json"}
	if filter.Start != nil && filter.End != nil {
		args = append(args, filter.Start.Format("2006-01-02T15:04:05"), filter.End.Format("2006-01-02T15:04:05"))
	} else if filter.Start != nil {
		args = append(args, "from", filter.Start.Format("2006-01-02T15:04:05"))
	} else if filter.End != nil {
		args = append(args, "to", filter.End.Format("2006-01-02T15:04:05"))
	}

	result, err := ExecuteCommand(args)
	if err != nil {
		return nil, fmt.Errorf("failed to list entries: %s", result.Error)
	}

	var entries []TimeEntry
	err = json.Unmarshal([]byte(result.Output), &entries)
	if err != nil {
		return nil, fmt.Errorf("failed to parse entries: %v", err)
	}

	// Calculate durations
	for i := range entries {
		if entries[i].Start != "" && entries[i].End != "" {
			start, err1 := time.Parse("2006-01-02T15:04:05", entries[i].Start)
			end, err2 := time.Parse("2006-01-02T15:04:05", entries[i].End)
			if err1 == nil && err2 == nil {
				entries[i].Duration = end.Sub(start)
			}
		}
	}

	return TimeEntryList(entries), nil
}

// Summary retrieves a summary for a given period
func Summary(period string) (string, error) {
	args := []string{"summary", ":" + period}
	result, err := ExecuteCommand(args)
	if err != nil {
		return "", fmt.Errorf("failed to get summary: %s", result.Error)
	}
	return result.Output, nil
}

// Export retrieves exported entries for a period or time range
func Export(period string, from, to *time.Time) (string, error) {
	args := []string{"export", "--json"}
	if period != "" {
		args = []string{"export", ":" + period, "--json"}
	} else {
		if from != nil {
			args = append(args, "from", from.Format("2006-01-02T15:04:05"))
		}
		if to != nil {
			args = append(args, "to", to.Format("2006-01-02T15:04:05"))
		}
	}

	result, err := ExecuteCommand(args)
	if err != nil {
		return "", fmt.Errorf("failed to export: %s", result.Error)
	}
	return result.Output, nil
}
