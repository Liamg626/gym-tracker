import { Hono } from 'hono';
import { BUILD_SHA } from './build-info';

export const app = new Hono()
  .get('/api/health', (c) => c.json({ ok: true, sha: BUILD_SHA }))
  .notFound((c) => c.json({ error: 'not found' }, 404));

export default app;
