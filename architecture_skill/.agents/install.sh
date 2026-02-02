#!/bin/bash

# Installs the documenting-architecture skill to the global Amp skills folder
# Usage: ./install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_NAME="documenting-architecture"
GLOBAL_SKILLS_DIR="$HOME/.config/agents/skills"
DEST_DIR="$GLOBAL_SKILLS_DIR/$SKILL_NAME"

echo "Installing $SKILL_NAME skill..."

# Create global skills directory if it doesn't exist
mkdir -p "$GLOBAL_SKILLS_DIR"

# Remove existing installation
if [ -d "$DEST_DIR" ]; then
    echo "Removing existing installation at $DEST_DIR"
    rm -rf "$DEST_DIR"
fi

# Copy skill files (exclude install.sh itself)
mkdir -p "$DEST_DIR"
cp "$SCRIPT_DIR/SKILL.md" "$DEST_DIR/"
cp -r "$SCRIPT_DIR/scripts" "$DEST_DIR/"
cp -r "$SCRIPT_DIR/reference" "$DEST_DIR/"

echo "Installed to $DEST_DIR"
echo "Done!"
