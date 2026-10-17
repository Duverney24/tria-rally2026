// Service worker de TRIA: el prototipo abre sin internet y el mapa ya recorrido sigue visible.
// - Página: red primero (para ver siempre la última versión) y copia guardada si no hay red.
// - Librerías, fuentes, íconos y manifiesto locales: copia guardada primero.
// - Teselas de OpenStreetMap y Esri: se guardan al verlas (no se descargan en bloque, por las políticas de uso).
// - La API (/version, /estado, …) nunca se guarda.
const VER = "tria-v10"; // subir este número obliga a los navegadores a traer la versión nueva
const APP = VER + "-app";
const TESELAS = "tria-teselas";
const MAX_TESELAS = 1500;
const BASE = [
  "./", "index.html", "vendor/leaflet/leaflet.js", "manifest.webmanifest",
  "icons/icon.svg", "icons/icon-192.png", "icons/icon-512.png", "icons/maskable-512.png", "icons/apple-touch-icon.png",
  ...["sans-latin-400", "sans-latin-500", "sans-latin-600",
      "sans-condensed-latin-500", "sans-condensed-latin-600", "sans-condensed-latin-700",
      "mono-latin-400", "mono-latin-500", "mono-latin-600"].map(f => `vendor/fonts/ibm-plex-${f}-normal.woff2`),
];
const HOSTS_TESELAS = ["tile.openstreetmap.org", "server.arcgisonline.com", "tile.opentopomap.org"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(APP).then(c => c.addAll(BASE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== APP && k !== TESELAS).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

let guardadas = 0;
async function recortar() {
  const c = await caches.open(TESELAS);
  const ks = await c.keys();
  for (const k of ks.slice(0, Math.max(0, ks.length - MAX_TESELAS))) await c.delete(k);
}

async function tesela(req) {
  const c = await caches.open(TESELAS);
  const hit = await c.match(req.url);
  if (hit) return hit;
  // Se pide con CORS para poder guardarla (las respuestas opacas ocupan mucha cuota).
  // Si el servidor no lo permite, se usa la petición original y esa tesela no se guarda.
  let res;
  try {
    res = await fetch(new Request(req.url, { mode: "cors", credentials: "omit" }));
  } catch (err) {
    return fetch(req);
  }
  if (res.ok) {
    await c.put(req.url, res.clone());
    if (++guardadas % 50 === 0) recortar();
  }
  return res;
}

async function pagina(req) {
  const c = await caches.open(APP);
  try {
    const res = await fetch(req);
    if (res.ok) c.put(req, res.clone());
    return res;
  } catch (err) {
    return (await c.match(req)) || (await c.match("index.html"));
  }
}

async function recurso(req) {
  const hit = await caches.match(req);
  return hit || fetch(req);
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (HOSTS_TESELAS.some(h => url.hostname === h || url.hostname.endsWith("." + h))) {
    e.respondWith(tesela(req));
  } else if (url.origin === self.location.origin) {
    if (req.mode === "navigate") e.respondWith(pagina(req));
    else if (/\/(vendor|icons)\/|\.webmanifest$/.test(url.pathname)) e.respondWith(recurso(req));
    // Todo lo demás del mismo origen (la API) va directo a la red
  }
});
