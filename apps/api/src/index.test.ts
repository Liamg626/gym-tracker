import { expect, it } from 'vitest';
import { app } from './index';

it('GET /api/health returns ok and the build commit SHA', async () => {
  const res = await app.request('/api/health');
  expect(res.status).toBe(200);
  expect(res.headers.get('content-type')).toMatch(/application\/json/);
  const body = (await res.json()) as { ok: boolean; sha: string };
  expect(body.ok).toBe(true);
  expect(typeof body.sha).toBe('string');
  expect(body.sha.length).toBeGreaterThan(0);
});

it('unknown API routes are JSON 404s', async () => {
  const res = await app.request('/api/nope');
  expect(res.status).toBe(404);
  expect(res.headers.get('content-type')).toMatch(/application\/json/);
  expect(await res.json()).toEqual({ error: 'not found' });
});
