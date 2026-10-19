// Resets the shared preview D1 database: drops every table (including d1_migrations), applies
// the migrations, then (FND-017) loads the demo data. Only ever targets gym-tracker-preview.
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';

const PREVIEW_DATABASE = 'gym-tracker-preview';
const PREVIEW_CONFIG = 'wrangler.preview-migrations.jsonc';

const database = process.argv[2] ?? PREVIEW_DATABASE;
if (database !== PREVIEW_DATABASE) {
  console.error(`Refusing to reseed "${database}": only "${PREVIEW_DATABASE}" can be reseeded.`);
  process.exit(1);
}

const require = createRequire(import.meta.url);
const wranglerBin = require.resolve('wrangler/bin/wrangler.js');
const wrangler = (args) =>
  execFileSync(process.execPath, [wranglerBin, ...args], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'inherit'],
  });

// List every table so they can be dropped, including the migration bookkeeping table.
const listed = JSON.parse(
  wrangler([
    'd1',
    'execute',
    PREVIEW_DATABASE,
    '--remote',
    '--config',
    PREVIEW_CONFIG,
    '--json',
    '--command',
    "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_cf_%'",
  ]),
);
const tables = (listed[0]?.results ?? []).map((row) => row.name);

if (tables.length > 0) {
  const drops = tables
    .map((name) => `DROP TABLE IF EXISTS "${name.replaceAll('"', '""')}";`)
    .join(' ');
  wrangler([
    'd1',
    'execute',
    PREVIEW_DATABASE,
    '--remote',
    '--config',
    PREVIEW_CONFIG,
    '--command',
    drops,
  ]);
  console.log(`dropped ${tables.length} table(s) from ${PREVIEW_DATABASE}`);
}

wrangler(['d1', 'migrations', 'apply', PREVIEW_DATABASE, '--remote', '--config', PREVIEW_CONFIG]);
console.log(`migrations applied to ${PREVIEW_DATABASE}; demo data loader arrives with FND-017`);
