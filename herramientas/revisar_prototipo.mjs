// Revisión rápida del prototipo para la CI: sintaxis de cada <script> en línea de index.html y de sw.js,
// manifiesto válido y que existan los archivos locales que se referencian (vendor, íconos).
// Uso: node herramientas/revisar_prototipo.mjs
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const DIR = "prototipo";
let errores = 0;
const fallo = msg => { console.error("✗", msg); errores++; };
const ok = msg => console.log("✓", msg);

const html = readFileSync(join(DIR, "index.html"), "utf8");
const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (!scripts.length) fallo("index.html no tiene scripts en línea");
scripts.forEach((codigo, i) => {
  try { new Function(codigo); ok(`index.html: script ${i + 1} (${codigo.length} caracteres)`); }
  catch (e) { fallo(`index.html: script ${i + 1}: ${e.message}`); }
});

try { new Function(readFileSync(join(DIR, "sw.js"), "utf8")); ok("sw.js"); }
catch (e) { fallo(`sw.js: ${e.message}`); }

try {
  const m = JSON.parse(readFileSync(join(DIR, "manifest.webmanifest"), "utf8"));
  for (const ic of m.icons || []) if (!existsSync(join(DIR, ic.src))) fallo(`manifiesto: falta ${ic.src}`);
  ok(`manifest.webmanifest (${(m.icons || []).length} íconos)`);
} catch (e) { fallo(`manifest.webmanifest: ${e.message}`); }

// Archivos locales referenciados desde index.html y sw.js
const refs = new Set([...html.matchAll(/(?:src|href)="((?:vendor|icons)\/[^"]+)"/g)].map(m => m[1]));
for (const m of html.matchAll(/url\((vendor\/[^)]+)\)/g)) refs.add(m[1]);
for (const m of readFileSync(join(DIR, "sw.js"), "utf8").matchAll(/"((?:vendor|icons)\/[^"$]+)"/g)) refs.add(m[1]);
for (const r of refs) if (!existsSync(join(DIR, r))) fallo(`falta el archivo ${r}`);
ok(`${refs.size} archivos locales referenciados`);

if (errores) { console.error(`\n${errores} problema(s)`); process.exit(1); }
console.log("\nPrototipo en orden");
