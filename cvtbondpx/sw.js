// sw.js — service worker for the convertible-bond pricer PWA.
// Strategy: network-first with cache fallback — always fresh while online
// (no stale-build surprises during development), fully functional offline.
// Bump CACHE on breaking layout changes to drop stale entries.

const CACHE = 'cvtbond-v2';
const SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './wasm/icon-192.png',
  './wasm/icon-512.png',
  './wasm/cvtbond.js',
  './wasm/cvtbond.wasm',
  './wasm/cvtbond.json',
  './wasm/worker.js',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE)
                                    .map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request)
      .then(resp => {
        if (resp.ok && new URL(e.request.url).origin === location.origin) {
          const copy = resp.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy));
        }
        return resp;
      })
      // ignoreSearch: ?autorun=... etc. still resolve to the cached page
      .catch(() => caches.match(e.request, { ignoreSearch: true }))
  );
});
