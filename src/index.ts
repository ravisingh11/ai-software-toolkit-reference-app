import { ApiError, canTransition, checkWriteHeaders, parseComment, parseIssue, parseRole, parseStatus, readJson, requireEditor, sessionToken } from './domain.ts';
import type { Role, Status } from './domain.ts';

type Session = { workspaceId: string; role: Role; expiresAt: string };
type Issue = { id: string; title: string; description: string; priority: string; status: Status; createdAt: string; updatedAt: string };
const issueColumns = 'id, title, description, priority, status, created_at AS createdAt, updated_at AS updatedAt';

function json(value: unknown, status = 200, headers: Record<string, string> = {}): Response {
  return Response.json(value, { status, headers: { 'cache-control': 'no-store', 'x-content-type-options': 'nosniff', ...headers } });
}

async function hash(value: string): Promise<string> {
  return [...new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value)))].map((n) => n.toString(16).padStart(2, '0')).join('');
}

async function authenticate(request: Request, env: Env): Promise<Session> {
  const token = sessionToken(request.headers.get('cookie'));
  if (!token) throw new ApiError(401, 'Start a demo session to open your board.');
  const session = await env.DB.prepare('SELECT workspace_id AS workspaceId, role, expires_at AS expiresAt FROM sessions WHERE token_hash = ? AND expires_at > ?')
    .bind(await hash(token), new Date().toISOString()).first<Session>();
  if (!session) throw new ApiError(401, 'Your demo session expired. Start a fresh board.');
  return session;
}

async function createSession(request: Request, env: Env): Promise<Response> {
  const role = parseRole(await readJson(request));
  const url = new URL(request.url);
  const ip = request.headers.get('cf-connecting-ip') ?? (['localhost', '127.0.0.1', '[::1]'].includes(url.hostname) ? 'local-development' : null);
  if (!ip) throw new ApiError(503, 'Demo sessions are temporarily unavailable.');
  const now = new Date();
  const hour = Math.floor(now.getTime() / 3_600_000);
  const rate = await env.DB.prepare('INSERT INTO rate_buckets (key, count, expires_at) VALUES (?, 1, ?) ON CONFLICT(key) DO UPDATE SET count = count + 1 WHERE count < 10 RETURNING count')
    .bind(await hash(`${ip}:${hour}`), new Date((hour + 1) * 3_600_000).toISOString()).all();
  if (!rate.results.length) throw new ApiError(429, 'Demo session limit reached. Try again next hour.');
  const token = [...crypto.getRandomValues(new Uint8Array(32))].map((n) => n.toString(16).padStart(2, '0')).join('');
  const workspaceId = crypto.randomUUID();
  const expiresAt = new Date(now.getTime() + 86_400_000).toISOString();
  const createdAt = now.toISOString();
  const seeds = [
    ['Make empty states useful', 'Help a new teammate understand what to do next when a board has no matching issues.', 'medium', 'triage'],
    ['Check keyboard navigation', 'Walk through the issue details and creation dialog using only the keyboard.', 'high', 'in_progress'],
    ['Publish release evidence', 'Link the deployed revision and verification results so anyone can inspect this reference app.', 'low', 'done'],
  ];
  await env.DB.batch([
    env.DB.prepare('INSERT INTO sessions (token_hash, workspace_id, role, expires_at, created_at) VALUES (?, ?, ?, ?, ?)').bind(await hash(token), workspaceId, role, expiresAt, createdAt),
    ...seeds.map(([title, description, priority, status]) => env.DB.prepare('INSERT INTO issues (id, workspace_id, title, description, priority, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)').bind(crypto.randomUUID(), workspaceId, title, description, priority, status, createdAt, createdAt)),
  ]);
  return json({ role, expiresAt }, 201, { 'set-cookie': `fieldnotes_session=${token}; Path=/; HttpOnly; SameSite=Strict; Max-Age=86400${url.protocol === 'https:' ? '; Secure' : ''}` });
}

async function findIssue(env: Env, workspaceId: string, id: string): Promise<Issue> {
  const issue = await env.DB.prepare(`SELECT ${issueColumns} FROM issues WHERE id = ? AND workspace_id = ?`).bind(id, workspaceId).first<Issue>();
  if (!issue) throw new ApiError(404, 'Issue not found.');
  return issue;
}

async function api(request: Request, env: Env): Promise<Response> {
  const { pathname } = new URL(request.url);
  const method = request.method;
  if (!['GET', 'POST', 'PATCH'].includes(method)) throw new ApiError(405, 'Method not allowed.');
  if (method !== 'GET') checkWriteHeaders(request);
  if (pathname === '/api/health' && method === 'GET') {
    await env.DB.prepare('SELECT count(*) AS ready FROM sessions WHERE 0').first();
    return json({ status: 'ok', revision: env.APP_REVISION, toolkitRevision: env.TOOLKIT_REVISION, version: env.CF_VERSION_METADATA.id });
  }
  if (pathname === '/api/session' && method === 'POST') return createSession(request, env);
  const session = await authenticate(request, env);
  if (pathname === '/api/session' && method === 'GET') return json({ role: session.role, expiresAt: session.expiresAt });
  if (pathname === '/api/issues' && method === 'GET') {
    const rows = await env.DB.prepare(`SELECT ${issueColumns} FROM issues WHERE workspace_id = ? ORDER BY created_at DESC, id`).bind(session.workspaceId).all<Issue>();
    return json({ issues: rows.results });
  }
  if (pathname === '/api/issues' && method === 'POST') {
    requireEditor(session.role);
    const { title, description, priority } = parseIssue(await readJson(request));
    const id = crypto.randomUUID();
    const now = new Date().toISOString();
    const created = await env.DB.prepare(`INSERT INTO issues (id, workspace_id, title, description, priority, status, created_at, updated_at)
      SELECT ?, ?, ?, ?, ?, 'triage', ?, ? WHERE (SELECT count(*) FROM issues WHERE workspace_id = ?) < 100 RETURNING ${issueColumns}`)
      .bind(id, session.workspaceId, title, description, priority, now, now, session.workspaceId).first<Issue>();
    if (!created) throw new ApiError(429, 'This demo board has reached its 100 issue limit.');
    return json({ issue: created }, 201);
  }
  const match = /^\/api\/issues\/([a-f0-9-]{36})(\/comments)?$/.exec(pathname);
  if (match) {
    const [, id, commentsPath] = match;
    if (method !== 'GET') requireEditor(session.role);
    const issue = await findIssue(env, session.workspaceId, id);
    if (!commentsPath && method === 'PATCH') {
      const status = parseStatus(await readJson(request));
      if (!canTransition(issue.status, status)) throw new ApiError(409, 'This status transition is not allowed.');
      if (issue.status === status) return json({ issue });
      // Include observed status to reject races instead of bypassing transition rules.
      const updated = await env.DB.prepare(`UPDATE issues SET status = ?, updated_at = ? WHERE id = ? AND workspace_id = ? AND status = ? RETURNING ${issueColumns}`)
        .bind(status, new Date().toISOString(), id, session.workspaceId, issue.status).first<Issue>();
      if (!updated) throw new ApiError(409, 'The issue changed. Refresh and try again.');
      return json({ issue: updated });
    }
    if (commentsPath && method === 'GET') {
      const rows = await env.DB.prepare('SELECT c.id, c.body, c.created_at AS createdAt FROM comments c JOIN issues i ON i.id = c.issue_id WHERE c.issue_id = ? AND i.workspace_id = ? ORDER BY c.created_at, c.id').bind(id, session.workspaceId).all();
      return json({ comments: rows.results });
    }
    if (commentsPath && method === 'POST') {
      const body = parseComment(await readJson(request));
      const comment = await env.DB.prepare(`INSERT INTO comments (id, issue_id, body, created_at)
        SELECT ?, i.id, ?, ? FROM issues i WHERE i.id = ? AND i.workspace_id = ? AND (SELECT count(*) FROM comments WHERE issue_id = i.id) < 50
        RETURNING id, body, created_at AS createdAt`).bind(crypto.randomUUID(), body, new Date().toISOString(), id, session.workspaceId).first();
      if (!comment) throw new ApiError(429, 'This issue has reached its 50 comment limit.');
      return json({ comment }, 201);
    }
  }
  throw new ApiError(404, 'Endpoint not found.');
}

export default {
  async fetch(request, env): Promise<Response> {
    if (!new URL(request.url).pathname.startsWith('/api/')) return env.ASSETS.fetch(request);
    try {
      return await api(request, env);
    } catch (error) {
      if (error instanceof ApiError) return json({ error: error.message }, error.status);
      // Do not log request bodies, cookies, database values, or errors that might include them.
      console.error('API request failed unexpectedly.');
      return json({ error: 'The service is temporarily unavailable. Please retry.' }, 503);
    }
  },
  async scheduled(_controller, env): Promise<void> {
    const now = new Date().toISOString();
    await env.DB.batch([
      env.DB.prepare('DELETE FROM sessions WHERE expires_at <= ?').bind(now),
      env.DB.prepare('DELETE FROM rate_buckets WHERE expires_at <= ?').bind(now),
    ]);
  },
} satisfies ExportedHandler<Env>;
