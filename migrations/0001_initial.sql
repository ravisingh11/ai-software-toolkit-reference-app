-- Additive initial schema. Sessions and their synthetic boards expire together.
CREATE TABLE sessions (
  token_hash TEXT PRIMARY KEY NOT NULL,
  workspace_id TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL CHECK (role IN ('editor', 'viewer')),
  expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL
) STRICT;
CREATE INDEX sessions_expiration ON sessions(expires_at);
CREATE TABLE issues (
  id TEXT PRIMARY KEY NOT NULL,
  workspace_id TEXT NOT NULL REFERENCES sessions(workspace_id) ON DELETE CASCADE,
  title TEXT NOT NULL CHECK (length(trim(title)) BETWEEN 1 AND 120),
  description TEXT NOT NULL CHECK (length(description) <= 2000),
  priority TEXT NOT NULL CHECK (priority IN ('low', 'medium', 'high')),
  status TEXT NOT NULL CHECK (status IN ('triage', 'in_progress', 'done')),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
) STRICT;
CREATE INDEX issues_workspace ON issues(workspace_id, created_at);
CREATE TABLE comments (
  id TEXT PRIMARY KEY NOT NULL,
  issue_id TEXT NOT NULL REFERENCES issues(id) ON DELETE CASCADE,
  body TEXT NOT NULL CHECK (length(trim(body)) BETWEEN 1 AND 1000),
  created_at TEXT NOT NULL
) STRICT;
CREATE INDEX comments_issue ON comments(issue_id, created_at);
CREATE TABLE rate_buckets (
  key TEXT PRIMARY KEY NOT NULL,
  count INTEGER NOT NULL CHECK (count BETWEEN 1 AND 10),
  expires_at TEXT NOT NULL
) STRICT;
CREATE INDEX rate_buckets_expiration ON rate_buckets(expires_at);
