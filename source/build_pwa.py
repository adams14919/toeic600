# -*- coding: utf-8 -*-
# 由 toeic600.html 產生離線獨立版（PWA）：index.html、manifest、service worker、圖示
import hashlib, json, os, re, subprocess, sys, time

SRC, OUT, EDGE = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(os.path.join(OUT, 'icons'), exist_ok=True)
src = open(SRC, encoding='utf-8').read()

title = re.search(r'<title>(.*?)</title>', src).group(1)
head_part, body_part = src.split('\n<div class="app">', 1)
head_part = head_part.replace(f'<title>{title}</title>', '').strip()
body_part = '<div class="app">' + body_part

index = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="以多益 600 分為目標的英文學習 App：單字間隔複習、Part 1–7 題庫、文法重點、模擬測驗與錯題本，可離線使用。">
<meta name="theme-color" content="#2448b8">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="多益600">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px/1.5 system-ui,sans-serif;background:#f3f5f9}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
{head_part}
</head>
<body>
{body_part}
<script>
if ('serviceWorker' in navigator) {{
  addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {{}}));
}}
</script>
</body>
</html>
"""
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(index)

manifest = {
  "name": "TOEIC 600 衝刺本",
  "short_name": "多益600",
  "description": "以多益 600 分為目標的英文學習 App，可離線使用。",
  "lang": "zh-Hant",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#f3f5f9",
  "theme_color": "#2448b8",
  "icons": [
    {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
    {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
    {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
  ]
}
open(os.path.join(OUT, 'manifest.webmanifest'), 'w', encoding='utf-8').write(json.dumps(manifest, ensure_ascii=False, indent=2))

version = hashlib.sha1(index.encode('utf-8')).hexdigest()[:10]
sw = f"""// TOEIC 600 衝刺本 service worker：頁面優先抓新版，斷線時用快取；字型與圖示快取優先
const CACHE = 'toeic600-{version}';
const CORE = ['./', 'index.html', 'manifest.webmanifest', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/apple-touch-icon.png'];

self.addEventListener('install', e => {{
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
}});

self.addEventListener('activate', e => {{
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k.startsWith('toeic600-') && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
}});

self.addEventListener('fetch', e => {{
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (req.mode === 'navigate') {{
    e.respondWith(fetch(req).then(res => {{
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put('index.html', copy));
      return res;
    }}).catch(() => caches.match('index.html')));
    return;
  }}
  const cacheable = url.origin === location.origin || url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com';
  if (!cacheable) return;
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => {{
    if (res.ok || res.type === 'opaque') {{ const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }}
    return res;
  }})));
}});
"""
open(os.path.join(OUT, 'sw.js'), 'w', encoding='utf-8').write(sw)

# ---------- 圖示：答案卡圈圈 + 600 ----------
def icon_svg(size, pad, rounded=True):
    inner = size - pad * 2
    r = inner * 0.22 if (pad == 0 and rounded) else 0
    cx = size / 2
    bub = inner * 0.085
    gap = bub * 2.7
    y = pad + inner * 0.32
    circles = ''.join(
        f'<circle cx="{cx + (i - 1) * gap}" cy="{y}" r="{bub}" fill="{"#ffffff" if i != 1 else "none"}" stroke="#ffffff" stroke-width="{bub * 0.32}"/>'
        for i in range(3))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
<rect x="0" y="0" width="{size}" height="{size}" rx="{r}" fill="#2448b8"/>
{circles}
<text x="{cx}" y="{pad + inner * 0.78}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-weight="800" font-size="{inner * 0.36}" fill="#ffffff" letter-spacing="{inner * -0.01}">600</text>
</svg>"""

def render(name, size, pad, rounded=True):
    html = os.path.join(OUT, f'_{name}.html')
    open(html, 'w', encoding='utf-8').write(f'<!doctype html><html><body style="margin:0;background:transparent">{icon_svg(size, pad, rounded)}</body></html>')
    png = os.path.join(OUT, 'icons', name)
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--default-background-color=00000000',
                    f'--window-size={size},{size}', f'--screenshot={png}', 'file:///' + html.replace('\\', '/')],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
    os.remove(html)
    return os.path.exists(png)

ok = [render('icon-512.png', 512, 0), render('icon-192.png', 192, 0),
      render('icon-maskable-512.png', 512, 52), render('apple-touch-icon.png', 180, 0, rounded=False)]
print('index', len(index) // 1024, 'KB; version', version, '; icons', ok)
