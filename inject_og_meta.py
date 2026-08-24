#!/usr/bin/env python3
"""Inject og:image, og:url, og:site_name and twitter card tags into all faviconpal pages."""
import os, re, html

SITE = "https://www.faviconpal.com"
IMAGE = f"{SITE}/assets/og-image.png"

def process(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    if 'property="og:image"' in text:
        print("SKIP (already has og:image):", path)
        return

    # find canonical href for og:url
    m = re.search(r'<link rel="canonical" href="([^"]+)">', text)
    page_url = m.group(1) if m else SITE + "/"

    # find og:title and og:description for twitter reuse
    title_m = re.search(r'<meta property="og:title" content="([^"]+)">', text)
    desc_m = re.search(r'<meta property="og:description" content="([^"]+)">', text)
    title = title_m.group(1) if title_m else ""
    desc = desc_m.group(1) if desc_m else ""

    # block to inject after og:type
    inject = (
        f'<meta property="og:url" content="{page_url}">\n'
        f'<meta property="og:site_name" content="FaviconPal">\n'
        f'<meta property="og:image" content="{IMAGE}">\n'
        '<meta property="og:image:width" content="1200">\n'
        '<meta property="og:image:height" content="630">\n'
        '<meta property="og:image:alt" content="FaviconPal — free online favicon ICO converter">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
    )
    if title:
        inject += f'<meta name="twitter:title" content="{title}">\n'
    if desc:
        inject += f'<meta name="twitter:description" content="{desc}">\n'
    inject += f'<meta name="twitter:image" content="{IMAGE}">\n'

    new_text, n = re.subn(
        r'(<meta property="og:type" content="website">)',
        r'\1\n' + inject.rstrip(),
        text,
        count=1,
    )

    if n == 0:
        # fallback: insert after og:description if no og:type
        new_text, n = re.subn(
            r'(<meta property="og:description" content="[^"]*">)',
            r'\1\n' + inject.rstrip(),
            text,
            count=1,
        )

    if n == 0:
        print("WARN: could not insert in", path)
        return

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("UPDATED:", path)

files = [
    "index.html",
    "avif-to-ico/index.html",
    "jpg-to-ico/index.html",
    "svg-to-ico/index.html",
    "contact/index.html",
    "privacy/index.html",
]

for f in files:
    process(f)
