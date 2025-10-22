# Plan to Fix Hot Reload Issues in stdioproxy

## Problem Overview

The current hot reload implementation in `ReloadConfig` has two main issues identified by TODO comments:

1. **URL Change Detection**: When reloading config, the system does not check if an existing server's URL has changed. If a URL changes, the connection should be updated.

2. **Client Notification**: After adding or removing tools due to config changes, the MCP client connected to the proxy is not notified about the updated tool list. This means the client may not see new tools until it reconnects.

## Proposed Solution

### 1. Implement URL Change Detection and Reconnection

**Location**: `ServerManager.ReloadConfig` method

**Steps**:
- For existing servers, compare the current URL with the new URL from config
- If URL has changed:
  - Disconnect the existing server
  - Connect to the new URL
- This ensures that URL changes are handled properly without leaving stale connections

### 2. Implement Client Notification for Tool Updates

**Location**: `ServerManager.ReloadConfig` method, after connecting/disconnecting servers

**Steps**:
- After all connections are updated, trigger a notification to the MCP client
- In MCP protocol, tools are discovered via `ListTools` request from client
- Since the proxy server dynamically adds/removes tools, we need to ensure the client can refresh its tool cache
- Potential approaches:
  - Send a notification message to the client (if MCP supports tool update notifications)
  - Or ensure the server properly handles `ListTools` to reflect current tools
  - Or implement a custom notification mechanism

## Implementation Considerations

- Ensure thread safety: All changes happen within the existing mutex lock
- Error handling: Log errors but continue with other servers if one fails
- Debouncing: The existing debouncing in `watchConfig` should prevent excessive reloads
- Testing: Need to test both URL changes and new server additions/removals

## Next Steps

1. Modify `ReloadConfig` to compare URLs and reconnect when necessary
2. Research MCP protocol for tool update notifications or implement appropriate notification mechanism
3. Update server to properly reflect tool changes to clients
4. Test the hot reload functionality with config file changes
