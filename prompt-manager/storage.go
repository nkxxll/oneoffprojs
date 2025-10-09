package main

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/google/uuid"
	"github.com/pelletier/go-toml/v2"
)

// Prompt represents a single prompt configuration.
type Prompt struct {
	ID   uuid.UUID `toml:"id"`
	Name string    `toml:"name"`
	Text string    `toml:"text"`
	Tags []string  `toml:"tags,omitempty"`
}

type PromptList struct {
	Prompts []Prompt `toml:"promts"`
}

// Store manages the collection of prompts and their persistence.
type Store struct {
	filePath string
	prompts  PromptList
}

// getStorageFilePath resolves the storage file path.
func getStorageFilePath() (string, error) {
	home, err := os.UserHomeDir()
	if err != nil {
		return "", fmt.Errorf("could not get user home directory: %w", err)
	}
	configDir := filepath.Join(home, ".config", "prompt-manager")
	if err := os.MkdirAll(configDir, 0755); err != nil {
		return "", fmt.Errorf("could not create config directory: %w", err)
	}
	return filepath.Join(configDir, "prompts.toml"), nil
}

// NewStore creates a new store and loads initial data.
func NewStore() (*Store, error) {
	filePath, err := getStorageFilePath()
	if err != nil {
		return nil, err
	}
	s := &Store{
		filePath: filePath,
	}
	if err := s.Load(); err != nil {
		return nil, fmt.Errorf("could not load prompts: %w", err)
	}
	return s, nil
}

// Load reads the TOML file from disk.
func (s *Store) Load() error {
	data, err := os.ReadFile(s.filePath)
	if os.IsNotExist(err) {
		return nil // File doesn't exist yet, which is fine.
	}
	if err != nil {
		return fmt.Errorf("could not read prompts file: %w", err)
	}
	if err := toml.Unmarshal(data, &s.prompts); err != nil {
		return fmt.Errorf("could not unmarshal prompts file: %w", err)
	}
	return nil
}

// Save writes the current prompts to the TOML file.
func (s *Store) Save() error {
	data, err := toml.Marshal(s.prompts)
	if err != nil {
		return fmt.Errorf("could not marshal prompts: %w", err)
	}
	if err := os.WriteFile(s.filePath, data, 0644); err != nil {
		return fmt.Errorf("could not write prompts file: %w", err)
	}
	return nil
}

// GetAll returns all prompts.
func (s *Store) GetAll() []Prompt {
	return s.prompts.Prompts
}

// Add adds a new prompt.
func (s *Store) Add(p Prompt) error {
	s.prompts.Prompts = append(s.prompts.Prompts, p)
	return s.Save()
}

// Get returns a single prompt by ID.
func (s *Store) Get(id uuid.UUID) (Prompt, bool) {
	for _, p := range s.prompts.Prompts {
		if p.ID == id {
			return p, true
		}
	}
	return Prompt{}, false
}

// Update modifies an existing prompt.
func (s *Store) Update(p Prompt) error {
	for i, prompt := range s.prompts.Prompts {
		if prompt.ID == p.ID {
			s.prompts.Prompts[i] = p
			return s.Save()
		}
	}
	return fmt.Errorf("prompt with ID %s not found", p.ID)
}

// Remove deletes a prompt by ID.
func (s *Store) Remove(id uuid.UUID) error {
	for i, p := range s.prompts.Prompts {
		if p.ID == id {
			s.prompts.Prompts = append(s.prompts.Prompts[:i], s.prompts.Prompts[i+1:]...)
			return s.Save()
		}
	}
	return fmt.Errorf("prompt with ID %s not found", id)
}
