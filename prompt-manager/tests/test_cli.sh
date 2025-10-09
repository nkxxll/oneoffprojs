#!/bin/bash

# A script to test the CLI functionality of the prompt-manager.

# Ensure the binary exists
if [ ! -f ./prompt-manager ]; then
    echo "Building the application..."
    go build
fi

# Cleanup previous test data
rm -f ~/.config/prompt-manager/prompts.toml

echo "--- Testing CLI ---"

# Test: Create a prompt
echo "1. Testing 'create' command..."
./prompt-manager create --name "Test Prompt 1" --text "This is the first test prompt." --tags "test,cli"
ID=$(./prompt-manager list | grep "Test Prompt 1" | awk '{print $1}')
if [ -z "$ID" ]; then
    echo "FAIL: Create command failed."
    exit 1
fi
echo "CREATE successful. Prompt ID: $ID"
echo

# Test: Create another prompt
./prompt-manager create --name "Another Go Prompt" --text "This is about Go." --tags "go,test"

# Test: List prompts
echo "2. Testing 'list' command..."
./prompt-manager list
echo

# Test: Search for a prompt by name
echo "3. Testing 'search' command (by name)..."
./prompt-manager search "Another"
echo

# Test: Search for a prompt by tag
echo "4. Testing 'search' command (by tag)..."
./prompt-manager search "cli"
echo

# Test: Update a prompt
echo "5. Testing 'update' command..."
./prompt-manager update $ID --name "Updated Test Prompt 1" --tags "test,cli,updated"
./prompt-manager list | grep "Updated Test Prompt 1"
if [ $? -ne 0 ]; then
    echo "FAIL: Update command failed."
    exit 1
fi
echo "UPDATE successful."
echo

# Test: Remove a prompt
echo "6. Testing 'remove' command..."
./prompt-manager remove $ID
./prompt-manager list | grep $ID
if [ $? -eq 0 ]; then
    echo "FAIL: Remove command failed."
    exit 1
fi
echo "REMOVE successful."
echo

echo "--- CLI Tests Passed ---"
