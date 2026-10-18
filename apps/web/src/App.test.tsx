import { expect, it } from 'vitest';
import { App } from './App';

it('renders a blank page', () => {
  expect(App()).toBeNull();
});
