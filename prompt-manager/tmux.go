package main

import (
	"os/exec"
)

// IsTmuxAvailable checks if the tmux executable is in the system's PATH.
func IsTmuxAvailable() bool {
	_, err := exec.LookPath("tmux")
	return err == nil
}

// Send sends text to a tmux pane.
func Send(targetPane string, text string, execute bool) error {
	args := []string{"send-keys"}
	if targetPane != "" {
		args = append(args, "-t", targetPane)
	}
	args = append(args, text)
	if execute {
		args = append(args, "C-m")
	}

	cmd := exec.Command("tmux", args...)
	return cmd.Run()
}
