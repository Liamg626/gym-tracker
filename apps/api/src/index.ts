import { Hono } from 'hono';
import { BUILD_SHA } from './build-info';

export const app = new Hono().get('/api/health', (c) => c.json({ ok: true, sha: BUILD_SHA }));

export default app;
