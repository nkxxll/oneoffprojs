import { Database } from "bun:sqlite";

export const db = new Database("tokens.sqlite");

export type Session = {
  id: string;
  github_id: number;
  expires_at: string;
};

export function initDb() {
  db.run(`
    CREATE TABLE IF NOT EXISTS user_tokens (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      github_id INTEGER UNIQUE NOT NULL,
      access_token TEXT NOT NULL,
      refresh_token TEXT,
      expires_at DATETIME,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
  `);
  db.run(`
    CREATE TABLE IF NOT EXISTS sessions (
      id TEXT PRIMARY KEY,
      github_id INTEGER NOT NULL,
      expires_at DATETIME,
      FOREIGN KEY(github_id) REFERENCES user_tokens(github_id)
    );
  `);
}

export function saveToken(
  githubId: number,
  tokenData: {
    access_token: string;
    refresh_token?: string;
    expires_at?: string;
  },
) {
  const insert = db.prepare(
    "INSERT OR REPLACE INTO user_tokens (github_id, access_token, refresh_token, expires_at) VALUES (?, ?, ?, ?)",
  );
  insert.run(
    githubId,
    tokenData.access_token,
    tokenData.refresh_token || null,
    tokenData.expires_at || null,
  );
}

export function getTokenByGithubId(githubId: number) {
  const query = db.prepare("SELECT * FROM user_tokens WHERE github_id = ?");
  return query.get(githubId) as {
    id: number;
    github_id: number;
    access_token: string;
    refresh_token?: string;
    expires_at?: string;
    created_at: string;
  } | null;
}

export function saveSession(sessionId: string, githubId: number) {
  const expiresAt = new Date(Date.now() + 86400 * 1000).toISOString(); // 1 day
  const insert = db.prepare(
    "INSERT OR REPLACE INTO sessions (id, github_id, expires_at) VALUES (?, ?, ?)",
  );
  insert.run(sessionId, githubId, expiresAt);
}

export function getSession(sessionId: string): Session | null {
  const query = db.prepare(
    'SELECT * FROM sessions WHERE id = ? AND expires_at > datetime("now")',
  );
  return query.get(sessionId) as {
    id: string;
    github_id: number;
    expires_at: string;
  } | null;
}

export function deleteSession(sessionId: string) {
  const del = db.prepare("DELETE FROM sessions WHERE id = ?");
  del.run(sessionId);
}
