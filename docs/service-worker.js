const CACHE_NAME = "rhetorilex-pwa-v1";
const CORE_ASSETS = [
  "./",
  "./en/",
  "./id/",
  "./en/paraphrase-workbench/",
  "./id/alat-parafrasa/",
  "./styles.css",
  "./app.js",
  "./site.webmanifest",
  "./assets/icon.svg",
  "./data/phrases.json"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))))
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  const requestUrl = new URL(event.request.url);
  if (requestUrl.origin !== self.location.origin) return;
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        return response;
      })
      .catch(() => caches.match(event.request).then((cached) => cached || caches.match("./en/paraphrase-workbench/")))
  );
});
