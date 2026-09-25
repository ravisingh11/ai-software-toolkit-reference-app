export const priorities = ['low', 'medium', 'high'] as const;
export const statuses = ['triage', 'in_progress', 'done'] as const;
export type Priority = typeof priorities[number];
export type Status = typeof statuses[number];
export type Role = 'editor' | 'viewer';

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

export function record(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new ApiError(400, 'A JSON object is required.');
  }
  return value as Record<string, unknown>;
}

export function textField(value: unknown, name: string, min: number, max: number): string {
  if (typeof value !== 'string') throw new ApiError(400, `${name} must be text.`);
  const text = value.trim();
  if (text.length < min || text.length > max) {
    throw new ApiError(400, `${name} must contain ${min} to ${max} characters.`);
  }
  return text;
}

export function parseRole(value: unknown): Role {
  const role = record(value).role;
  if (role !== 'editor' && role !== 'viewer') throw new ApiError(400, 'Choose editor or viewer.');
  return role;
}

export function parseIssue(value: unknown): { title: string; description: string; priority: Priority } {
  const body = record(value);
  if (!priorities.includes(body.priority as Priority)) throw new ApiError(400, 'Choose low, medium, or high priority.');
  return {
    title: textField(body.title, 'Title', 1, 120),
    description: textField(body.description, 'Description', 0, 2000),
    priority: body.priority as Priority,
  };
}

export function parseStatus(value: unknown): Status {
  const status = record(value).status;
  if (!statuses.includes(status as Status)) throw new ApiError(400, 'Choose a valid issue status.');
  return status as Status;
}

export function parseComment(value: unknown): string {
  return textField(record(value).body, 'Comment', 1, 1000);
}

export function canTransition(from: Status, to: Status): boolean {
  if (from === to) return true;
  return from === 'in_progress' || to === 'in_progress';
}

export function requireEditor(role: Role): void {
  if (role !== 'editor') throw new ApiError(403, 'Viewer sessions cannot change this board.');
}

export function sessionToken(cookie: string | null): string | null {
  const matches = (cookie ?? '').split(';').map((part) => part.trim()).filter((part) => part.startsWith('fieldnotes_session='));
  if (matches.length !== 1) return null;
  const value = matches[0].slice('fieldnotes_session='.length);
  return /^[a-f0-9]{64}$/.test(value) ? value : null;
}

export function checkWriteHeaders(request: Request): void {
  if (request.headers.get('origin') !== new URL(request.url).origin) {
    throw new ApiError(403, 'Requests must originate from this application.');
  }
  if (request.headers.get('content-type')?.split(';')[0].trim().toLowerCase() !== 'application/json') {
    throw new ApiError(415, 'Use application/json.');
  }
}

export async function readJson(request: Request): Promise<unknown> {
  const limit = 8192;
  const declaredSize = Number(request.headers.get('content-length'));
  if (declaredSize > limit) throw new ApiError(413, 'Request body exceeds 8 KiB.');
  const reader = request.body?.getReader();
  if (!reader) throw new ApiError(400, 'A JSON body is required.');
  const chunks: Uint8Array[] = [];
  let size = 0;
  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > limit) {
        await reader.cancel();
        throw new ApiError(413, 'Request body exceeds 8 KiB.');
      }
      chunks.push(value);
    }
  } finally {
    reader.releaseLock();
  }
  const bytes = new Uint8Array(size);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.byteLength;
  }
  try {
    return JSON.parse(new TextDecoder('utf-8', { fatal: true, ignoreBOM: false }).decode(bytes));
  } catch {
    throw new ApiError(400, 'Malformed JSON body.');
  }
}
