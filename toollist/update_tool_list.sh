#!/usr/bin/env bash
set -euo pipefail

trap 'echo "❌ Error on line $LINENO" >&2; exit 1' ERR

## This is only for me just to update my tool list to my local stow dotfile dir

os=$(uname)
file_name="${os}-tool-list.txt"
stow_dir="${HOME}/stow_dotfiles"

echo "📋 Generating tool list for $os..."

if ! list=$(uv run main.py 2>&1); then
  echo "❌ Failed to generate tool list" >&2
  exit 1
fi

if [[ -z "$list" ]]; then
  echo "❌ Tool list is empty" >&2
  exit 1
fi

echo "✏️  Writing to $file_name..."
if ! printf "++ FULL TOOL LIST %s ++\n\n%s\n" "$os" "$list" > "$file_name"; then
  echo "❌ Failed to write file" >&2
  exit 1
fi

if [[ ! -d "$stow_dir" ]]; then
  echo "❌ Directory not found: $stow_dir" >&2
  exit 1
fi

echo "📦 Copying to $stow_dir..."
if ! cp "$file_name" "$stow_dir/$file_name"; then
  echo "❌ Failed to copy file" >&2
  exit 1
fi

echo "🗑️ Cleanup!"

rm -f "$file_name"

echo "✅ Done!"

