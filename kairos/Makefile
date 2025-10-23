# Project settings
BINARY_SERVER := server
BINARY_CLIENT := client
BUILD_DIR := build

# Targets
.PHONY: all clean linux mac local

all: linux mac

# --- Linux (Raspberry Pi, ARM64) ---
linux: $(BUILD_DIR)/linux-arm64/$(BINARY_SERVER) $(BUILD_DIR)/linux-arm64/$(BINARY_CLIENT)

$(BUILD_DIR)/linux-arm64/$(BINARY_SERVER): server/server.go
	@echo "Building server for Linux ARM64..."
	GOOS=linux GOARCH=arm64 go build -o $@ ./server

$(BUILD_DIR)/linux-arm64/$(BINARY_CLIENT): client/client.go
	@echo "Building client for Linux ARM64..."
	GOOS=linux GOARCH=arm64 go build -o $@ ./client

# --- macOS (both Intel and ARM) ---
mac: mac-amd mac-arm

mac-amd: $(BUILD_DIR)/darwin-amd64/$(BINARY_SERVER) $(BUILD_DIR)/darwin-amd64/$(BINARY_CLIENT)

mac-arm: $(BUILD_DIR)/darwin-arm64/$(BINARY_SERVER) $(BUILD_DIR)/darwin-arm64/$(BINARY_CLIENT)

$(BUILD_DIR)/darwin-amd64/$(BINARY_SERVER): server/server.go
	@echo "Building server for macOS AMD64..."
	GOOS=darwin GOARCH=amd64 go build -o $@ ./server

$(BUILD_DIR)/darwin-amd64/$(BINARY_CLIENT): client/client.go
	@echo "Building client for macOS AMD64..."
	GOOS=darwin GOARCH=amd64 go build -o $@ ./client

$(BUILD_DIR)/darwin-arm64/$(BINARY_SERVER): server/server.go
	@echo "Building server for macOS ARM64..."
	GOOS=darwin GOARCH=arm64 go build -o $@ ./server

$(BUILD_DIR)/darwin-arm64/$(BINARY_CLIENT): client/client.go
	@echo "Building client for macOS ARM64..."
	GOOS=darwin GOARCH=arm64 go build -o $@ ./client

# --- Local build for current platform ---
local: $(BUILD_DIR)/$(BINARY_SERVER) $(BUILD_DIR)/$(BINARY_CLIENT)

$(BUILD_DIR)/$(BINARY_SERVER): server/server.go
	@echo "Building server for local platform..."
	go build -o $@ ./server

$(BUILD_DIR)/$(BINARY_CLIENT): client/client.go
	@echo "Building client for local platform..."
	go build -o $@ ./client

# --- Cleanup ---
clean:
	@echo "Cleaning build directory..."
	rm -rf $(BUILD_DIR)
