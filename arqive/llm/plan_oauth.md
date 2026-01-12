# OAuth Setup Plan for React Application

## Overview
Implement server-side OAuth with PKCE flow using Octokit for GitHub authentication. Store access tokens in SQLite database using Bun SQLite3. Create middleware for token validation and login redirection.

## Dependencies
- `@octokit/oauth-app` - For handling OAuth flow
- `bun:sqlite3` - For SQLite database operations

## Database Schema
Create SQLite table to store access tokens:
```sql
CREATE TABLE user_tokens (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  github_id INTEGER UNIQUE NOT NULL,
  access_token TEXT NOT NULL,
  refresh_token TEXT,
  expires_at DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Implementation Steps

### 1. Database Setup
- Create SQLite database connection in server
- Initialize database schema on server start
- Create helper functions for token CRUD operations

### 2. OAuth PKCE Flow Implementation
- Generate code verifier and challenge on login request
- Redirect user to GitHub OAuth authorization URL
- Handle callback at `/auth/callback`
- Exchange authorization code for access token using Octokit
- Store token in database with user info

### 3. Authentication Middleware
- Create middleware function that checks for valid access token
- Extract token from session/cookie or database lookup
- Validate token expiry and refresh if needed
- Redirect to `/auth/login` if no valid token found
- Apply middleware to protected routes

### 4. Server Routes
- `/auth/login` - Initiate OAuth flow, generate PKCE, redirect to GitHub
- `/auth/callback` - Handle OAuth callback, exchange code, store token
- `/auth/logout` - Clear session/token, redirect to login
- Apply auth middleware to existing API routes that need protection

### 5. Client Integration
- React components for login/logout UI
- Handle redirects after authentication
- Store session state (authenticated/not authenticated)

### 6. Security Considerations
- Use secure HTTP-only cookies for session management
- Implement CSRF protection
- Validate state parameter in OAuth flow
- Handle token refresh automatically

## File Structure Changes
```
src/
├── server/
│   ├── auth.ts          # OAuth logic and middleware
│   ├── db.ts            # Database operations
│   └── index.ts         # Main server file
├── client/
│   ├── components/
│   │   ├── Login.tsx    # Login component
│   │   └── AuthGuard.tsx # Client-side auth guard
│   └── index.tsx        # Client entry point
```

## Testing
- Test OAuth flow end-to-end
- Test token validation and refresh
- Test middleware redirection
- Test database operations
