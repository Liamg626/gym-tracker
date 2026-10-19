import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { parse } from 'jsonc-parser';
import { expect, it } from 'vitest';

const configPath = (name: string) => fileURLToPath(new URL(`../${name}`, import.meta.url));
const readConfig = (name: string) =>
  parse(readFileSync(configPath(name), 'utf8')) as Record<string, unknown>;

type D1Binding = { binding?: string; database_name?: string; database_id?: string };

const productionDatabaseId = (config: Record<string, unknown>) =>
  (config.d1_databases as D1Binding[] | undefined)?.[0]?.database_id;

it('never binds a preview to the production D1 database', () => {
  const config = readConfig('wrangler.jsonc');
  const production = productionDatabaseId(config);
  expect(production).toBeTruthy();

  const previewBindings =
    (config.previews as { d1_databases?: D1Binding[] } | undefined)?.d1_databases ?? [];
  expect(previewBindings.length).toBeGreaterThan(0);
  for (const binding of previewBindings) {
    expect(binding.database_id).toBeTruthy();
    expect(binding.database_id).not.toBe(production);
    expect(binding.database_name).toBe('gym-tracker-preview');
  }
});

it('keeps the preview migrations config pointed at the preview database only', () => {
  const production = productionDatabaseId(readConfig('wrangler.jsonc'));
  const migrations = readConfig('wrangler.preview-migrations.jsonc');
  const bindings = (migrations.d1_databases as D1Binding[] | undefined) ?? [];
  expect(bindings).toHaveLength(1);
  expect(bindings[0]?.database_name).toBe('gym-tracker-preview');
  expect(bindings[0]?.database_id).not.toBe(production);
});
