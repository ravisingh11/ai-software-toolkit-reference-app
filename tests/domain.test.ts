import { test } from 'node:test';
import assert from 'node:assert/strict';
import { ApiError, canTransition, checkWriteHeaders, parseComment, parseIssue, parseRole, parseStatus, readJson, record, requireEditor, sessionToken, statuses, textField } from '../src/domain.ts';

function rejectsStatus(fn: () => unknown, status: number) {
  assert.throws(fn, (error: unknown) => error instanceof ApiError && error.status === status);
}

const issue = { title: 'Useful title', description: '', priority: 'medium' };

test('validates issue fields and normalizes surrounding whitespace', () => {
  assert.deepEqual(parseIssue({ ...issue, title: '  Useful title  ', description: '  Context  ' }), { ...issue, description: 'Context' });
  assert.deepEqual(parseIssue(issue), issue);
  for (const priority of ['low', 'medium', 'high']) assert.equal(parseIssue({ ...issue, priority }).priority, priority);
  for (const title of ['', '  ', 'x'.repeat(121), null, 12]) rejectsStatus(() => parseIssue({ ...issue, title }), 400);
  rejectsStatus(() => parseIssue({ ...issue, description: 'x'.repeat(2001) }), 400);
  rejectsStatus(() => parseIssue({ ...issue, priority: 'urgent' }), 400);
  assert.equal(parseIssue({ ...issue, title: 'x'.repeat(120), description: 'x'.repeat(2000) }).title.length, 120);
});

test('rejects non-object JSON and validates role, status and comments', () => {
  for (const input of [null, false, 1, 'str', []]) rejectsStatus(() => record(input), 400);
  assert.deepEqual(record({}), {});
  for (const role of ['editor', 'viewer']) assert.equal(parseRole({ role }), role);
  rejectsStatus(() => parseRole({ role: 'admin' }), 400);
  for (const status of statuses) assert.equal(parseStatus({ status }), status);
  rejectsStatus(() => parseStatus({ status: 'closed' }), 400);
  assert.equal(parseComment({ body: '  Note  ' }), 'Note');
  assert.equal(parseComment({ body: 'x'.repeat(1000) }).length, 1000);
  for (const body of ['', 'x'.repeat(1001), undefined]) rejectsStatus(() => parseComment({ body }), 400);
  assert.equal(textField('', 'Optional', 0, 10), '');
});

test('enforces the complete transition matrix and server role', () => {
  for (const from of statuses) {
    for (const to of statuses) {
      assert.equal(canTransition(from, to), from === to || from === 'in_progress' || to === 'in_progress', `${from} -> ${to}`);
    }
  }
  // Deliberate negative control: this assertion must fail before gate verification.
  assert.equal(canTransition('triage', 'done'), true);
  requireEditor('editor');
  rejectsStatus(() => requireEditor('viewer'), 403);
});

test('accepts exactly one valid session cookie and rejects ambiguity', () => {
  const token = 'a1'.repeat(32);
  assert.equal(sessionToken(`other=hello; fieldnotes_session=${token}; preference=dark`), token);
  for (const cookie of [null, '', 'other=a', 'fieldnotes_session=short', `fieldnotes_session=${'G'.repeat(64)}`, `fieldnotes_session=${token}; fieldnotes_session=${token}`, `fieldnotes_session=${token}%00`]) {
    assert.equal(sessionToken(cookie), null);
  }
});

test('requires same origin and JSON on writes', () => {
  const write = (headers: Record<string, string>) => new Request('https://example.com/api/issues', { method: 'POST', headers });
  checkWriteHeaders(write({ origin: 'https://example.com', 'content-type': 'application/json; charset=utf-8' }));
  checkWriteHeaders(write({ origin: 'https://example.com', 'content-type': 'APPLICATION/JSON' }));
  rejectsStatus(() => checkWriteHeaders(write({ origin: 'https://evil.example', 'content-type': 'application/json' })), 403);
  rejectsStatus(() => checkWriteHeaders(write({ 'content-type': 'application/json' })), 403);
  rejectsStatus(() => checkWriteHeaders(write({ origin: 'https://example.com' })), 415);
  rejectsStatus(() => checkWriteHeaders(write({ origin: 'https://example.com', 'content-type': 'text/plain' })), 415);
});

test('reads bounded valid JSON including chunked streams', async () => {
  const stream = new ReadableStream({ start(controller) {
    controller.enqueue(new TextEncoder().encode('{"title":'));
    controller.enqueue(new TextEncoder().encode('"hello"}'));
    controller.close();
  } });
  const request = new Request('https://example.com', { method: 'POST', body: stream, duplex: 'half' } as RequestInit);
  assert.deepEqual(await readJson(request), { title: 'hello' });
  assert.equal(await readJson(new Request('https://example.com', { method: 'POST', body: '"' + 'x'.repeat(8190) + '"' })), 'x'.repeat(8190));
});

test('rejects missing, malformed, invalid UTF-8 and oversized bodies', async () => {
  const bad = async (request: Request, status: number) => assert.rejects(readJson(request), (error: unknown) => error instanceof ApiError && error.status === status);
  await bad(new Request('https://example.com'), 400);
  await bad(new Request('https://example.com', { method: 'POST', body: '{' }), 400);
  await bad(new Request('https://example.com', { method: 'POST', body: new Uint8Array([0xff]) }), 400);
  await bad(new Request('https://example.com', { method: 'POST', body: '{}', headers: { 'content-length': '8193' } }), 413);
  await bad(new Request('https://example.com', { method: 'POST', body: 'x'.repeat(8193) }), 413);
});
