package main

import (
	"fmt"
	"os"
	"strings"
	"text/tabwriter"

	"github.com/google/uuid"
	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "prompt-manager",
	Short: "A tool for managing and using prompts with tmux.",
	RunE: func(cmd *cobra.Command, args []string) error {
		target, _ := cmd.Flags().GetString("target")
		// This is where we will launch the TUI
		return RunTUI(target)
	},
}

var createCmd = &cobra.Command{
	Use:   "create",
	Short: "Create a new prompt",
	RunE: func(cmd *cobra.Command, args []string) error {
		name, _ := cmd.Flags().GetString("name")
		text, _ := cmd.Flags().GetString("text")
		tags, _ := cmd.Flags().GetStringSlice("tags")

		if name == "" || text == "" {
			return fmt.Errorf("name and text are required")
		}

		store, err := NewStore()
		if err != nil {
			return err
		}

		newPrompt := Prompt{
			ID:   uuid.New(),
			Name: name,
			Text: text,
			Tags: tags,
		}

		if err := store.Add(newPrompt); err != nil {
			return err
		}

		fmt.Printf("Prompt '%s' created with ID %s\n", newPrompt.Name, newPrompt.ID)
		return nil
	},
}

var listCmd = &cobra.Command{
	Use:   "list",
	Short: "List all prompts",
	RunE: func(cmd *cobra.Command, args []string) error {
		store, err := NewStore()
		if err != nil {
			return err
		}

		prompts := store.GetAll()
		if len(prompts) == 0 {
			fmt.Println("No prompts found.")
			return nil
		}

		w := tabwriter.NewWriter(os.Stdout, 0, 0, 2, ' ', 0)
		fmt.Fprintln(w, "ID\tNAME\tTAGS")
		for _, p := range prompts {
			fmt.Fprintf(w, "%s\t%s\t%s\n", p.ID, p.Name, strings.Join(p.Tags, ", "))
		}
		return w.Flush()
	},
}

var updateCmd = &cobra.Command{
	Use:   "update [ID]",
	Short: "Update an existing prompt",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		id, err := uuid.Parse(args[0])
		if err != nil {
			return fmt.Errorf("invalid ID: %w", err)
		}

		store, err := NewStore()
		if err != nil {
			return err
		}

		prompt, ok := store.Get(id)
		if !ok {
			return fmt.Errorf("prompt with ID %s not found", id)
		}

		if cmd.Flags().Changed("name") {
			prompt.Name, _ = cmd.Flags().GetString("name")
		}
		if cmd.Flags().Changed("text") {
			prompt.Text, _ = cmd.Flags().GetString("text")
		}
		if cmd.Flags().Changed("tags") {
			prompt.Tags, _ = cmd.Flags().GetStringSlice("tags")
		}

		if err := store.Update(prompt); err != nil {
			return err
		}

		fmt.Printf("Prompt '%s' updated.\n", prompt.Name)
		return nil
	},
}

var removeCmd = &cobra.Command{
	Use:   "remove [ID]",
	Short: "Remove a prompt",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		id, err := uuid.Parse(args[0])
		if err != nil {
			return fmt.Errorf("invalid ID: %w", err)
		}

		store, err := NewStore()
		if err != nil {
			return err
		}

		if err := store.Remove(id); err != nil {
			return err
		}

		fmt.Printf("Prompt with ID %s removed.\n", id)
		return nil
	},
}

var searchCmd = &cobra.Command{
	Use:   "search [keyword]",
	Short: "Search for prompts by name or tag",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		keyword := strings.ToLower(args[0])
		store, err := NewStore()
		if err != nil {
			return err
		}

		prompts := store.GetAll()
		var filtered []Prompt

		for _, p := range prompts {
			if strings.Contains(strings.ToLower(p.Name), keyword) {
				filtered = append(filtered, p)
				continue
			}
			for _, tag := range p.Tags {
				if strings.Contains(strings.ToLower(tag), keyword) {
					filtered = append(filtered, p)
					break
				}
			}
		}

		if len(filtered) == 0 {
			fmt.Println("No matching prompts found.")
			return nil
		}

		w := tabwriter.NewWriter(os.Stdout, 0, 0, 2, ' ', 0)
		fmt.Fprintln(w, "ID\tNAME\tTAGS")
		for _, p := range filtered {
			fmt.Fprintf(w, "%s\t%s\t%s\n", p.ID, p.Name, strings.Join(p.Tags, ", "))
		}
		return w.Flush()
	},
}

func init() {
	rootCmd.PersistentFlags().StringP("target", "t", "", "tmux target pane (e.g., session:window.pane)")

	createCmd.Flags().String("name", "", "Name of the prompt")
	createCmd.Flags().String("text", "", "Content of the prompt")
	createCmd.Flags().StringSlice("tags", []string{}, "Comma-separated tags for the prompt")
	createCmd.MarkFlagRequired("name")
	createCmd.MarkFlagRequired("text")

	updateCmd.Flags().String("name", "", "New name for the prompt")
	updateCmd.Flags().String("text", "", "New text for the prompt")
	updateCmd.Flags().StringSlice("tags", []string{}, "New set of tags (will replace old tags)")

	rootCmd.AddCommand(createCmd, listCmd, updateCmd, removeCmd, searchCmd)
}

// Execute runs the root command.
func Execute() error {
	return rootCmd.Execute()
}
