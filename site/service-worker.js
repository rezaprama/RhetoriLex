// RhetoriLex moved to /Lugas/. Remove only the old app's cache.
// Cache Storage is shared across every GitHub Pages project on this origin;
// deleting every cache here would also evict Lugas' own offline cache.
const LEGACY_CACHE_PREFIX = "rhetorilex-pwa-";
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key.startsWith(LEGACY_CACHE_PREFIX)).map((key) => caches.delete(key))))
      .then(() => self.registration.unregister())
      .then(() => self.clients.matchAll({ type: "window" }))
      .then((clients) => clients.forEach((client) => client.navigate(client.url)))
  );
});
