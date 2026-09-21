import { cpSync, mkdirSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
const out = `${root}dist`;
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
cpSync(`${root}app`, out, { recursive: true });
const library = JSON.parse(readFileSync(`${root}data/library.json`, 'utf8'));
library.completedTasks = [];
for (const resource of library.resources) {
  resource.notes = '';
  resource.status = 'saved';
}
writeFileSync(`${out}/library.json`, JSON.stringify(library));
const html = readFileSync(`${out}/index.html`, 'utf8').replace('<script src="app.js">', '<script>window.ATLAS_STATIC=true;</script><script src="app.js">');
writeFileSync(`${out}/index.html`, html);
console.log(`Built ${library.resources.length} resources for static hosting.`);
