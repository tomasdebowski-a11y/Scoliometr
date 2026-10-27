import pathlib, re, hashlib
src = pathlib.Path('app.html').read_text()
head = '''<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#1f4fa3">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Skoliometr">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-192.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);box-sizing:border-box;height:100%}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
'''
# split leading head-ish part (title/meta/link/style) from body
m = re.search(r'</style>\s*', src)
top, rest = src[:m.end()], src[m.end():]
out = head + top + '\n</head>\n<body>\n' + rest + '\n</body>\n</html>\n'
d = pathlib.Path('dist'); d.mkdir(exist_ok=True)
(d/'index.html').write_text(out)
ver = hashlib.sha1(out.encode()).hexdigest()[:8]
(d/'manifest.webmanifest').write_text('''{
  "name": "Skoliometr",
  "short_name": "Skoliometr",
  "description": "Digitální skoliometr: úhel rotace trupu (ATR) v Adamsově předklonu",
  "lang": "cs",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#0d1017",
  "theme_color": "#1f4fa3",
  "icons": [
    {"src": "icon.svg", "sizes": "any", "type": "image/svg+xml"},
    {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
  ]
}
''')
(d/'sw.js').write_text(f'''const C = 'skoliometr-{ver}';
const FILES = ['./', 'index.html', 'manifest.webmanifest', 'icon.svg', 'icon-192.png', 'icon-512.png'];
self.addEventListener('install', e => {{ e.waitUntil(caches.open(C).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); }});
self.addEventListener('activate', e => {{ e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k)))).then(() => self.clients.claim())); }});
self.addEventListener('fetch', e => {{
  if (e.request.method !== 'GET') return;
  // the app page itself: network first, so an update shows on the next start; offline falls back to the cache
  if (e.request.mode === 'navigate') {{ e.respondWith(fetch(e.request).then(res => {{ const cp = res.clone(); caches.open(C).then(c => c.put('index.html', cp)); return res; }}).catch(() => caches.match('index.html'))); return; }}
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => {{
    if (res.ok && (e.request.url.startsWith(self.location.origin) || e.request.url.includes('fonts.g'))) {{ const cp = res.clone(); caches.open(C).then(c => c.put(e.request, cp)); }}
    return res;
  }}).catch(() => caches.match('index.html'))));
}});
''')
import shutil; shutil.copy('icon.svg', d/'icon.svg')
print('ok', ver, len(out))
