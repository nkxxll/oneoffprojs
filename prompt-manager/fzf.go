package main

import (
	"bufio"
	"errors"
	"fmt"
	"io"
	"os/exec"
	"strings"

	"github.com/google/uuid"
)

var ErrFzfCancelled = errors.New("fzf selection cancelled")

// IsFzfAvailable checks if fzf is in the PATH.
func IsFzfAvailable() bool {
	_, err := exec.LookPath("fzf")
	return err == nil
}

// Select uses fzf to select a prompt from a list.
func Select(prompts []Prompt) (uuid.UUID, error) {
	if !IsFzfAvailable() {
		return uuid.Nil, errors.New("fzf command not found")
	}

	cmd := exec.Command("fzf")
	stdin, err := cmd.StdinPipe()
	if err != nil {
		return uuid.Nil, err
	}
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return uuid.Nil, err
	}

	if err := cmd.Start(); err != nil {
		return uuid.Nil, err
	}

	go func() {
		defer stdin.Close()
		for _, p := range prompts {
			// Format: [ID] Name - Tags
			tagStr := strings.Join(p.Tags, ", ")
			io.WriteString(stdin, fmt.Sprintf("[%s] %s - %s\n", p.ID, p.Name, tagStr))
		}
	}()

	scanner := bufio.NewScanner(stdout)
	var selectedID uuid.UUID
	if scanner.Scan() {
		line := scanner.Text()
		// Extract ID from "[ID] ..."
		idStr := strings.Trim(line[1:strings.Index(line, "]")], " ")
		parsedID, err := uuid.Parse(idStr)
		if err != nil {
			return uuid.Nil, fmt.Errorf("failed to parse ID from fzf output: %w", err)
		}
		selectedID = parsedID
	}

	if err := cmd.Wait(); err != nil {
		if _, ok := err.(*exec.ExitError); ok {
			return uuid.Nil, ErrFzfCancelled
		}
		return uuid.Nil, err
	}

	if selectedID == uuid.Nil {
		return uuid.Nil, ErrFzfCancelled
	}

	return selectedID, nil
}
