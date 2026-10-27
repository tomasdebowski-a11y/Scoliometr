const C = 'skoliometr-184046be';
const FILES = ['./', 'index.html', 'manifest.webmanifest', 'icon.svg', 'icon-192.png', 'icon-512.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(C).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  // the app page itself: network first, so an update shows on the next start; offline falls back to the cache
  if (e.request.mode === 'navigate') { e.respondWith(fetch(e.request).then(res => { const cp = res.clone(); caches.open(C).then(c => c.put('index.html', cp)); return res; }).catch(() => caches.match('index.html'))); return; }
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => {
    if (res.ok && (e.request.url.startsWith(self.location.origin) || e.request.url.includes('fonts.g'))) { const cp = res.clone(); caches.open(C).then(c => c.put(e.request, cp)); }
    return res;
  }).catch(() => caches.match('index.html'))));
});
