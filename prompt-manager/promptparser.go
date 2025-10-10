package main

import (
	"regexp"
	"strings"
)

// ParseTemplate finds all template fields in a string.
// Template fields are in the format {{field_name}}.
func ParseTemplate(text string) []string {
	re := regexp.MustCompile(`\{\{([^{}]+)\}\}`)
	matches := re.FindAllStringSubmatch(text, -1)
	if matches == nil {
		return []string{}
	}

	// Use a map to store unique field names to avoid duplicates
	uniqueFields := make(map[string]bool)
	for _, match := range matches {
		uniqueFields[match[1]] = true
	}

	// Convert map keys to a slice
	fields := make([]string, 0, len(uniqueFields))
	for field := range uniqueFields {
		fields = append(fields, field)
	}
	return fields
}

// RenderTemplate replaces template fields with their values.
func RenderTemplate(text string, values map[string]string) string {
	for key, value := range values {
		placeholder := "{{" + key + "}}"
		text = strings.ReplaceAll(text, placeholder, value)
	}
	return text
}
