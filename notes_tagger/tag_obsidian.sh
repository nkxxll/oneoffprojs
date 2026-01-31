#!/usr/bin/env bash
# Tag and link Obsidian vault using notes-tagger

VAULT_PATH="$HOME/git/obsidian-notes"

# Check if vault exists
if [ ! -d "$VAULT_PATH" ]; then
    echo "Error: Vault not found at $VAULT_PATH"
    exit 1
fi

cd "$(dirname "$0")" || exit 1

# Parse arguments
RUN_TAGS=false
RUN_ANALYZE=false
RUN_LINK=false
EXTRA_ARGS=()

for arg in "$@"; do
    case $arg in
        --tags)
            RUN_TAGS=true
            ;;
        --analyze)
            RUN_ANALYZE=true
            ;;
        --link)
            RUN_LINK=true
            ;;
        *)
            EXTRA_ARGS+=("$arg")
            ;;
    esac
done

# If no stages specified, run all
if ! $RUN_TAGS && ! $RUN_ANALYZE && ! $RUN_LINK; then
    RUN_TAGS=true
    RUN_ANALYZE=true
    RUN_LINK=true
fi

if $RUN_TAGS; then
    echo "Tagging notes in $VAULT_PATH..."
    uv run notes-tagger tag "$VAULT_PATH" --recursive --verbose "${EXTRA_ARGS[@]}"
fi

if $RUN_ANALYZE; then
    echo "Analyzing notes in $VAULT_PATH..."
    uv run notes-tagger analyze "$VAULT_PATH" --recursive --verbose
fi

if $RUN_LINK; then
    echo "Linking notes in $VAULT_PATH..."
    uv run notes-tagger link-db "$VAULT_PATH" --verbose "${EXTRA_ARGS[@]}"
fi
