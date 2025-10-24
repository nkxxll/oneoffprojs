# Project settings
BINARY_SERVER := server
BINARY_PROXY := proxy
BINARY_CLI := cli
BUILD_DIR := build

# Targets
.PHONY: all clean linux mac local

all: linux mac

# --- Linux (Raspberry Pi, ARM64) ---
linux: $(BUILD_DIR)/linux-arm64/$(BINARY_SERVER) $(BUILD_DIR)/linux-arm64/$(BINARY_PROXY) $(BUILD_DIR)/linux-arm64/$(BINARY_CLI)

$(BUILD_DIR)/linux-arm64/$(BINARY_SERVER): server/server.go
	@echo "Building server for Linux ARM64..."
	GOOS=linux GOARCH=arm64 go build -o $@ ./server

$(BUILD_DIR)/linux-arm64/$(BINARY_PROXY): client/proxy/main.go client/proxy/server.go
	@echo "Building proxy for Linux ARM64..."
	GOOS=linux GOARCH=arm64 go build -o $@ ./client/proxy

$(BUILD_DIR)/linux-arm64/$(BINARY_CLI): client/cli/main.go client/cli/commands.go
	@echo "Building cli for Linux ARM64..."
	GOOS=linux GOARCH=arm64 go build -o $@ ./client/cli

# --- macOS (both Intel and ARM) ---
mac: mac-amd mac-arm

mac-amd: $(BUILD_DIR)/darwin-amd64/$(BINARY_SERVER) $(BUILD_DIR)/darwin-amd64/$(BINARY_PROXY) $(BUILD_DIR)/darwin-amd64/$(BINARY_CLI)

mac-arm: $(BUILD_DIR)/darwin-arm64/$(BINARY_SERVER) $(BUILD_DIR)/darwin-arm64/$(BINARY_PROXY) $(BUILD_DIR)/darwin-arm64/$(BINARY_CLI)

$(BUILD_DIR)/darwin-amd64/$(BINARY_SERVER): server/server.go
	@echo "Building server for macOS AMD64..."
	GOOS=darwin GOARCH=amd64 go build -o $@ ./server

$(BUILD_DIR)/darwin-amd64/$(BINARY_PROXY): client/proxy/main.go client/proxy/server.go
	@echo "Building proxy for macOS AMD64..."
	GOOS=darwin GOARCH=amd64 go build -o $@ ./client/proxy

$(BUILD_DIR)/darwin-amd64/$(BINARY_CLI): client/cli/main.go client/cli/commands.go
	@echo "Building cli for macOS AMD64..."
	GOOS=darwin GOARCH=amd64 go build -o $@ ./client/cli

$(BUILD_DIR)/darwin-arm64/$(BINARY_SERVER): server/server.go
	@echo "Building server for macOS ARM64..."
	GOOS=darwin GOARCH=arm64 go build -o $@ ./server

$(BUILD_DIR)/darwin-arm64/$(BINARY_PROXY): client/proxy/main.go client/proxy/server.go
	@echo "Building proxy for macOS ARM64..."
	GOOS=darwin GOARCH=arm64 go build -o $@ ./client/proxy

$(BUILD_DIR)/darwin-arm64/$(BINARY_CLI): client/cli/main.go client/cli/commands.go
	@echo "Building cli for macOS ARM64..."
	GOOS=darwin GOARCH=arm64 go build -o $@ ./client/cli

# --- Local build for current platform ---
local: $(BUILD_DIR)/$(BINARY_SERVER) $(BUILD_DIR)/$(BINARY_PROXY) $(BUILD_DIR)/$(BINARY_CLI)

$(BUILD_DIR)/$(BINARY_SERVER): server/server.go
	@echo "Building server for local platform..."
	go build -o $@ ./server

$(BUILD_DIR)/$(BINARY_PROXY): client/proxy/main.go client/proxy/server.go
	@echo "Building proxy for local platform..."
	go build -o $@ ./client/proxy

$(BUILD_DIR)/$(BINARY_CLI): client/cli/main.go client/cli/commands.go
	@echo "Building cli for local platform..."
	go build -o $@ ./client/cli

# --- Cleanup ---
clean:
	@echo "Cleaning build directory..."
	rm -rf $(BUILD_DIR)
