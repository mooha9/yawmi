#!/usr/bin/env python3
"""يبني نسخة مستقلة من قصاصة الـArtifact في src/app.html، مع الملخص والأيقونات والـmanifest."""
import pathlib, re, json, shutil, zlib, struct, math

ROOT = pathlib.Path(__file__).parent
PUB = ROOT / "public"; PUB.mkdir(exist_ok=True)
frag = (ROOT / "src/app.html").read_text(encoding="utf-8")

title = re.search(r"<title>(.*?)</title>", frag).group(1)
fonts = re.findall(r'<link rel="(?:preconnect|stylesheet)"[^>]*>', frag)
style = re.search(r"<style>.*?</style>", frag, re.S).group(0)
body  = frag[frag.index('<header class="top">'):]
DESC = "جدولك اليومي حول أوقات الصلاة: الورد ×٣٠، العادات، ملخص الأسواق والذكاء الاصطناعي، وتمارين الإلقاء."

html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#F3F5F1" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0E1512" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="{title}">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="mobile-web-app-capable" content="yes">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{DESC}">
<meta property="og:locale" content="ar_SA">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}[hidden]{{display:none!important}}img{{max-width:100%}}</style>
{chr(10).join(fonts)}
{style}
</head>
<body>
{body}
</body>
</html>
"""
(PUB / "index.html").write_text(html, encoding="utf-8")
shutil.copy(ROOT / "src/news.json", PUB / "news.json")

# الأيقونة: حلقة الورد الذهبية على أخضر المسجد، والقوس المكتمل ٣٠/٣٠
GREEN, GOLD, SOFT = (0x1F,0x6B,0x52), (0xE0,0xB0,0x4E), (0x2E,0x80,0x65)
def write_png(path, w, h, rgba):
    raw = b"".join(b"\x00" + rgba[y*w*4:(y+1)*w*4] for y in range(h))
    ch = lambda t,d: struct.pack(">I",len(d)) + t + d + struct.pack(">I", zlib.crc32(t+d) & 0xffffffff)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)) + ch(b"IDAT", zlib.compress(raw, 9)) + ch(b"IEND", b""))
def icon(n):
    out = bytearray(n*n*4); c = n/2; R = n*0.30; T = n*0.065
    for y in range(n):
        for x in range(n):
            acc=[0,0,0]
            for sy in (.25,.75):
                for sx in (.25,.75):
                    px,py=x+sx-c,y+sy-c; d=math.hypot(px,py); col=GREEN
                    if abs(d-R)<=T:
                        ang=(math.degrees(math.atan2(px,-py))+360)%360
                        col = GOLD if ang>=100 else SOFT
                    if d<=n*0.07: col=GOLD
                    for i in range(3): acc[i]+=col[i]
            o=(y*n+x)*4; out[o:o+4]=bytes([round(acc[0]/4),round(acc[1]/4),round(acc[2]/4),255])
    return bytes(out)
for name,size in (("apple-touch-icon.png",180),("icon-192.png",192),("icon-512.png",512)):
    if not (PUB/name).exists(): write_png(PUB/name,size,size,icon(size))
(PUB/"icon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="112" fill="#1F6B52"/><circle cx="256" cy="256" r="154" fill="none" stroke="#2E8065" stroke-width="66"/><path d="M406.6 223.9A154 154 0 1 1 256 102" fill="none" stroke="#E0B04E" stroke-width="66" transform="rotate(100 256 256) rotate(-100 256 256)"/><circle cx="256" cy="256" r="36" fill="#E0B04E"/></svg>')
(PUB/"manifest.webmanifest").write_text(json.dumps({"name":title,"short_name":title,"description":DESC,"lang":"ar","dir":"rtl","start_url":"/","display":"standalone","background_color":"#F3F5F1","theme_color":"#1F6B52","icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]},ensure_ascii=False))
(PUB/"_headers").write_text("""/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

/news.json
  Cache-Control: no-cache

/index.html
  Cache-Control: no-cache

/manifest.webmanifest
  Content-Type: application/manifest+json; charset=utf-8
""")
print("built", len(html), "bytes")
