// Release-only smoke. Uses synthetic data in one short-lived isolated board.
const base = process.env.APP_URL;
if (!base || !/^https:\/\//.test(base)) throw new Error('APP_URL must be the HTTPS release URL');
const revision = process.env.APP_REVISION;
const health = await fetch(`${base}/api/health`).then(response => response.json());
if (health.status !== 'ok' || (revision && health.revision !== revision)) throw new Error('Health/revision mismatch');
let cookie;
async function request(path, method = 'GET', data) {
  const response = await fetch(`${base}${path}`, {
    method, headers: { Origin: base, ...(cookie ? { Cookie: cookie } : {}), ...(data ? { 'Content-Type': 'application/json' } : {}) },
    body: data ? JSON.stringify(data) : undefined,
  });
  if (response.headers.get('set-cookie')) cookie = response.headers.get('set-cookie').split(';')[0];
  const result = await response.json();
  if (!response.ok) throw new Error(`${method} ${path}: ${response.status} ${JSON.stringify(result)}`);
  return result;
}
await request('/api/session', 'POST', { role: 'editor' });
const { issue } = await request('/api/issues', 'POST', { title: 'Release smoke', description: 'Synthetic release verification; expires with demo session.', priority: 'low' });
await request(`/api/issues/${issue.id}`, 'PATCH', { status: 'in_progress' });
await request(`/api/issues/${issue.id}/comments`, 'POST', { body: 'Live API verified.' });
const { comments } = await request(`/api/issues/${issue.id}/comments`);
if (comments.length !== 1) throw new Error('Comment persistence failed');
console.log(JSON.stringify({ status: 'passed', revision: health.revision, toolkitRevision: health.toolkitRevision, workerVersion: health.version, checks: ['database health', 'isolated session', 'create issue', 'transition', 'persist comment'] }, null, 2));
