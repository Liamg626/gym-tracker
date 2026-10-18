import { expect, it } from 'vitest';
import { app } from './index';

it('answers the root route', async () => {
  const res = await app.request('/');
  expect(res.status).toBe(200);
  expect(await res.text()).toBe('gym-tracker api');
});
