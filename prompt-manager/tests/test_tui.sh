#!/bin/bash

# A script to test the TUI functionality of the prompt-manager.

# Ensure the binary exists
if [ ! -f ./prompt-manager ]; then
    echo "Building the application..."
    go build
fi

echo "--- Testing TUI ---"
echo "This script will launch the TUI."
echo "Please manually inspect the TUI for the following:"
echo "1. The list of prompts should be displayed."
echo "2. You should be able to navigate the list with arrow keys."
echo "3. Pressing 'c' should open the create form."
echo "4. Pressing 'e' should open the edit form."
echo "5. Pressing 'd' should delete the selected prompt."
echo "6. Pressing 'q' or 'ctrl+c' should exit the TUI."
echo
echo "The TUI will be launched in 3 seconds..."
sleep 3

# Launch the TUI.
# We can't easily script interactions, so this is a manual check.
./prompt-manager

echo
echo "--- TUI Test Finished ---"
