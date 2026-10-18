import { Hono } from 'hono';

export const app = new Hono().get('/', (c) => c.text('gym-tracker api'));

export default app;
