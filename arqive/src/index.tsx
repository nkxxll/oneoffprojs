import { serve } from "bun";
import index from "./index.html";
import docs from "./docs.html";
import { initDb } from "./server/db";
import {
  handleLogin,
  handleCallback,
  handleLogout,
  authMiddleware,
  authStatus,
} from "./server/auth";
import { handleQuerySearch, handleSaveQuery } from "./server/github";

// Initialize the database on server startup
initDb();

console.log("Database initialized successfully.");

const server = serve({
  routes: {
    "/api/query": (request) => authMiddleware(request, handleQuerySearch),
    "/api/save-query": (request) => authMiddleware(request, handleSaveQuery),
    "/api/auth/login": handleLogin,
    "/api/auth/callback": handleCallback,
    "/api/auth/logout": handleLogout,
    "/api/auth/status": authStatus,
    "/docs": docs,
    "/*": index,
  },

  development: process.env.NODE_ENV !== "production" && {
    hmr: true,
    console: true,
  },
});

console.log(`🚀 Server running at ${server.url}`);
