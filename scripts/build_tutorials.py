# -*- coding: utf-8 -*-
"""
Build the /tutorials/ informational cluster for faviconpal.com.

Why this exists (2026-09-12 GSC diagnosis):
  faviconpal has 6 pages, all "X to ICO" converter pages, all stuck at SERP
  position 55-69 with 0 clicks. The converter SERPs are owned by
  cloudconvert / convertio / freeconvert (DR 80+).
  Meanwhile the INFORMATIONAL favicon cluster ("favicon size", "favicon
  dimensions", "what size should a favicon be") has a soft SERP made of
  blogs, Wikipedia and Reddit — and favicon.io, a comparable independent
  site, ranks #1 for all of them with a single page (/tutorials/favicon-sizes/).
  faviconpal had zero informational pages. This script builds that cluster.

Guarantees:
  - visible FAQ block and FAQPage JSON-LD are generated from the SAME list
    (no schema/visible drift)
  - Article + FAQPage + BreadcrumbList per page
  - design tokens/nav/footer identical to the existing tool pages
"""
import os, json

SITE = r"D:\workbuddy-出海web\faviconpal"
BASE = "https://www.faviconpal.com"
DATE = "2026-09-12"
DATE_LONG = "September 12, 2026"

NAV = [
    ("/", "WebP to ICO"),
    ("/jpg-to-ico/", "JPG to ICO"),
    ("/svg-to-ico/", "SVG to ICO"),
    ("/avif-to-ico/", "AVIF to ICO"),
    ("/favicon-generator.html", "Favicon Generator"),
    ("/tutorials/", "Guides"),
]

CSS = """<style>
  :root {
    --bg: #f6f7f9; --card: #ffffff; --border: #e4e7ec;
    --text: #101828; --text-2: #475467; --text-3: #98a2b3;
    --primary: #2563eb; --primary-600: #1d4ed8; --primary-50: #eff6ff;
    --green: #067647; --green-50: #ecfdf3;
    --amber: #b54708; --amber-50: #fffaeb;
    --red: #b42318; --red-50: #fef3f2;
    --radius: 14px;
    --shadow: 0 1px 3px rgba(16,24,40,.08), 0 8px 24px -8px rgba(16,24,40,.1);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.6; -webkit-font-smoothing: antialiased; }
  .container { max-width: 1080px; margin: 0 auto; padding: 0 20px; }

  header { background: var(--card); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 50; }
  .header-inner { display: flex; align-items: center; justify-content: space-between; height: 60px; }
  .logo { display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 17px; color: var(--text); text-decoration: none; }
  .logo-mark { width: 30px; height: 30px; border-radius: 8px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    display: flex; align-items: center; justify-content: center; color: #fff; font-size: 15px; font-weight: 800; }
  nav { display: flex; align-items: center; gap: 4px; }
  nav a { color: var(--text-2); text-decoration: none; font-size: 14px; font-weight: 500; padding: 8px 12px; border-radius: 8px; }
  nav a:hover { background: var(--primary-50); color: var(--primary-600); }
  nav a.active { color: var(--primary-600); background: var(--primary-50); }
  @media (max-width: 720px) { nav { display: none; } }

  .hero { text-align: center; padding: 44px 0 4px; }
  .hero h1 { font-size: 36px; font-weight: 800; letter-spacing: -0.02em; line-height: 1.18; max-width: 820px; margin: 0 auto; }
  .hero p { color: var(--text-2); font-size: 17px; max-width: 680px; margin: 14px auto 0; }
  .hero-badges { display: flex; justify-content: center; gap: 10px; margin-top: 20px; flex-wrap: wrap; }
  .badge { display: inline-flex; align-items: center; gap: 6px; background: var(--card); border: 1px solid var(--border);
    border-radius: 999px; padding: 6px 14px; font-size: 13px; font-weight: 600; color: var(--text-2); }
  .badge.green { color: var(--green); background: var(--green-50); border-color: #abefc6; }
  .badge.blue { color: var(--primary-600); background: var(--primary-50); border-color: #bfdbfe; }
  .updated { font-size: 13px; color: var(--text-3); margin-top: 12px; }

  .answer-box { background: var(--primary-50); border: 1px solid #bfdbfe; border-radius: 12px; padding: 18px 22px; margin: 26px 0; }
  .answer-box b { display: block; font-size: 12px; text-transform: uppercase; letter-spacing: .07em; color: var(--primary-600); margin-bottom: 7px; }
  .answer-box p { color: var(--text); font-size: 15px; margin: 0; }

  .toc { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 18px 22px; margin: 24px 0; }
  .toc b { display: block; font-size: 12px; text-transform: uppercase; letter-spacing: .07em; color: var(--text-3); margin-bottom: 8px; }
  .toc ol { margin: 0; padding-left: 20px; color: var(--text-2); }
  .toc li { margin-bottom: 4px; }
  .toc a { color: var(--primary-600); text-decoration: none; }
  .toc a:hover { text-decoration: underline; }

  .content { margin: 48px 0; }
  .content h2 { font-size: 25px; font-weight: 800; letter-spacing: -0.01em; margin: 40px 0 14px; }
  .content h2:first-child { margin-top: 0; }
  .content h3 { font-size: 18px; font-weight: 700; margin: 26px 0 10px; }
  .content p { color: var(--text-2); margin-bottom: 14px; }
  .content ul, .content ol { color: var(--text-2); padding-left: 22px; margin-bottom: 14px; }
  .content li { margin-bottom: 6px; }
  .content strong { color: var(--text); }
  .content a { color: var(--primary-600); }

  .note { background: var(--amber-50); border: 1px solid #fedf89; border-radius: 12px; padding: 14px 18px; margin: 18px 0; font-size: 14px; color: #7a2e0e; }
  .note b { color: #7a2e0e; }

  .code-block { background: #0f172a; color: #e2e8f0; border-radius: 10px; padding: 16px 18px;
    font-family: 'SFMono-Regular', Consolas, monospace; font-size: 12.5px; line-height: 1.75;
    overflow-x: auto; margin: 14px 0 20px; white-space: pre; }

  table { width: 100%; border-collapse: collapse; margin: 18px 0 26px; background: var(--card); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
  th, td { text-align: left; padding: 12px 16px; font-size: 14px; border-bottom: 1px solid var(--border); }
  th { background: #f9fafb; font-weight: 600; color: var(--text-2); }
  tr:last-child td { border-bottom: none; }
  td:first-child { font-weight: 600; }

  .faq { margin-top: 20px; }
  details { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; margin-bottom: 10px; }
  details summary { cursor: pointer; font-weight: 600; font-size: 15px; }
  details p { color: var(--text-2); font-size: 14px; margin-top: 10px; margin-bottom: 0; }
  details p + p { margin-top: 8px; }

  .cta-inline { text-align: center; margin: 32px 0 8px; }
  .btn { display: inline-flex; align-items: center; gap: 6px; padding: 12px 24px; border-radius: 10px;
    font-size: 15px; font-weight: 600; cursor: pointer; border: 1px solid var(--border);
    background: var(--card); color: var(--text); text-decoration: none; }
  .btn:hover { border-color: var(--primary); color: var(--primary-600); }
  .btn.primary { background: var(--primary); border-color: var(--primary); color: #fff; }
  .btn.primary:hover { background: var(--primary-600); color: #fff; }

  .guide-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; margin-top: 20px; }
  .guide-card { display: block; text-decoration: none; color: inherit; background: var(--card);
    border: 1px solid var(--border); border-radius: 12px; padding: 18px 20px; }
  .guide-card:hover { border-color: var(--primary); box-shadow: var(--shadow); }
  .guide-card .gc-icon { font-size: 24px; }
  .guide-card b { display: block; font-size: 16px; margin-top: 8px; color: var(--primary-600); }
  .guide-card p { font-size: 13px; color: var(--text-2); margin-top: 4px; margin-bottom: 0; }

  .link-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; margin-top: 16px; }
  .link-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 14px 16px;
    text-decoration: none; color: var(--text); display: block; position: relative; }
  .link-card:hover { border-color: var(--primary); box-shadow: var(--shadow); }
  .link-card b { font-size: 14px; color: var(--primary-600); }
  .link-card p { font-size: 12px; color: var(--text-2); margin-top: 2px; }
  .lk-status { position: absolute; top: 12px; right: 14px; font-size: 10px; font-weight: 700; letter-spacing: .06em; padding: 2px 8px; border-radius: 999px; }
  .lk-status.live { color: var(--green); background: var(--green-50); border: 1px solid #abefc6; }

  footer { border-top: 1px solid var(--border); background: var(--card); padding: 28px 0; margin-top: 40px; }
  .footer-inner { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
  .footer-inner p { font-size: 13px; color: var(--text-3); }

  @media (max-width: 720px) {
    .hero h1 { font-size: 27px; }
    .content h2 { font-size: 21px; }
    th, td { padding: 10px 12px; font-size: 13px; }
  }
</style>"""

ANALYTICS = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QMF2LHLL2B"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-QMF2LHLL2B');
</script>

<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "yatffguzb3");
</script>"""

TOOL_LINKS = """      <h2 id="tools">Convert your image now</h2>
      <p>Everything on FaviconPal runs inside your browser — your files are never uploaded to a server. Pick the converter that matches your source file:</p>
      <div class="link-grid">
        <a class="link-card" href="/"><b>WebP to ICO</b><span class="lk-status live">LIVE</span><p>The flagship converter — WebP images to favicon.</p></a>
        <a class="link-card" href="/jpg-to-ico/"><b>JPG to ICO</b><span class="lk-status live">LIVE</span><p>Photos to icons (no alpha channel).</p></a>
        <a class="link-card" href="/svg-to-ico/"><b>SVG to ICO</b><span class="lk-status live">LIVE</span><p>Vector to icon — any size, lossless.</p></a>
        <a class="link-card" href="/avif-to-ico/"><b>AVIF to ICO</b><span class="lk-status live">LIVE</span><p>The new format, converted to Windows icons.</p></a>
        <a class="link-card" href="/favicon-generator.html"><b>Favicon Generator</b><span class="lk-status live">LIVE</span><p>Full favicon set with the HTML snippet.</p></a>
      </div>"""


def faq_html(pairs):
    out = ['<div class="faq">']
    for q, a in pairs:
        out.append("    <details>")
        out.append("      <summary>%s</summary>" % q)
        out.append("      <p>%s</p>" % a)
        out.append("    </details>")
    out.append("  </div>")
    return "\n  ".join(out)


def faq_schema(pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a.replace("<strong>", "").replace("</strong>", "")}}
            for q, a in pairs
        ],
    }


def breadcrumb_schema(crumbs):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
            for i, (n, u) in enumerate(crumbs)
        ],
    }


def article_schema(url, h1, desc):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": h1,
        "description": desc,
        "url": url,
        "datePublished": DATE,
        "dateModified": DATE,
        "author": {"@type": "Organization", "name": "FaviconPal", "url": BASE + "/"},
        "publisher": {"@type": "Organization", "name": "FaviconPal",
                      "logo": {"@type": "ImageObject", "url": BASE + "/assets/og-image.png"}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "image": BASE + "/assets/og-image.png",
    }


def render(*, slug, title, desc, h1, hero_p, answer, toc, body, faq, crumbs, badges=None):
    url = BASE + slug
    parts = []
    parts.append("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n" + ANALYTICS)
    parts.append('<meta charset="UTF-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    parts.append("<title>%s</title>" % title)
    parts.append('<meta name="description" content="%s">' % desc)
    parts.append('<meta name="robots" content="index, follow">')
    parts.append('<link rel="canonical" href="%s">' % url)
    parts.append('<link rel="icon" href="/favicon.ico" sizes="any">')
    parts.append('<link rel="icon" href="/favicon-32x32.png" sizes="32x32" type="image/png">')
    parts.append('<link rel="icon" href="/favicon-16x16.png" sizes="16x16" type="image/png">')
    parts.append('<link rel="apple-touch-icon" href="/apple-touch-icon.png">')
    parts.append('<link rel="manifest" href="/site.webmanifest">')
    parts.append('<meta property="og:title" content="%s">' % title)
    parts.append('<meta property="og:description" content="%s">' % desc)
    parts.append('<meta property="og:type" content="article">')
    parts.append('<meta property="og:url" content="%s">' % url)
    parts.append('<meta property="og:site_name" content="FaviconPal">')
    parts.append('<meta property="og:image" content="%s/assets/og-image.png">' % BASE)
    parts.append('<meta property="og:image:width" content="1200">')
    parts.append('<meta property="og:image:height" content="630">')
    parts.append('<meta property="og:image:alt" content="FaviconPal — free in-browser favicon tools">')
    parts.append('<meta name="twitter:card" content="summary_large_image">')
    parts.append('<meta name="twitter:title" content="%s">' % title)
    parts.append('<meta name="twitter:description" content="%s">' % desc)
    parts.append('<meta name="twitter:image" content="%s/assets/og-image.png">' % BASE)
    parts.append('<link rel="preconnect" href="https://fonts.googleapis.com">')
    parts.append('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    parts.append('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">')
    parts.append(CSS)
    parts.append('<script type="application/ld+json">\n%s\n</script>' % json.dumps(article_schema(url, h1, desc), ensure_ascii=False, indent=2))
    parts.append('<script type="application/ld+json">\n%s\n</script>' % json.dumps(faq_schema(faq), ensure_ascii=False, indent=2))
    parts.append("</head>\n<body>\n")
    parts.append("<header>")
    parts.append('  <div class="container header-inner">')
    parts.append('    <a class="logo" href="/"><span class="logo-mark">F</span> FaviconPal</a>')
    parts.append("    <nav>")
    for href, label in NAV:
        cls = ' class="active"' if href == "/tutorials/" else ""
        parts.append('      <a href="%s"%s>%s</a>' % (href, cls, label))
    parts.append("    </nav>")
    parts.append("  </div>")
    parts.append("</header>\n")
    parts.append("<main>\n  <div class=\"container\">")
    parts.append('    <section class="hero">')
    parts.append("      <h1>%s</h1>" % h1)
    parts.append("      <p>%s</p>" % hero_p)
    if badges:
        parts.append('      <div class="hero-badges">')
        for b, kind in badges:
            parts.append('        <span class="badge %s">%s</span>' % (kind, b))
        parts.append("      </div>")
    parts.append('      <p class="updated">Last updated: %s</p>' % DATE_LONG)
    parts.append("    </section>")
    if answer:
        parts.append('    <div class="answer-box"><b>Short answer</b><p>%s</p></div>' % answer)
    if toc:
        parts.append('    <div class="toc"><b>On this page</b><ol>')
        for anchor, label in toc:
            parts.append('      <li><a href="#%s">%s</a></li>' % (anchor, label))
        parts.append("    </ol></div>")
    parts.append('    <section class="content">')
    parts.append(body)
    parts.append("    </section>\n  </div>\n</main>\n")
    parts.append("<footer>")
    parts.append('  <div class="container footer-inner">')
    parts.append("    <p>© 2026 FaviconPal · Free in-browser image tools</p>")
    parts.append('    <p>Made for developers &amp; designers · <a href="/privacy/" style="color:var(--text-3)">Privacy</a> · <a href="/contact/" style="color:var(--text-3)">Contact</a></p>')
    parts.append("  </div>")
    parts.append("</footer>\n")
    parts.append('<script type="application/ld+json">\n%s\n</script>' % json.dumps(breadcrumb_schema(crumbs), ensure_ascii=False, indent=2))
    parts.append("</body>\n</html>\n")
    return "\n".join(parts)


def write(slug, html_text):
    d = os.path.join(SITE, slug.strip("/").replace("/", os.sep))
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "index.html")
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(html_text)
    return p


# ===========================================================================
# Guide 1 — favicon sizes  (the champion: favicon.io owns this cluster with 1 page)
# ===========================================================================
SIZES_FAQ = [
    ("What size should a favicon be?",
     "A favicon should be <strong>16×16 px at minimum</strong>, with a <strong>32×32 px</strong> version for high-DPI screens. In practice you ship both inside a single <code>favicon.ico</code>, then add PNGs at <strong>180×180</strong> (Apple Touch Icon), <strong>192×192</strong> and <strong>512×512</strong> (Android and PWA) so the icon stays sharp everywhere."),
    ("What is the standard favicon size in pixels?",
     "The long-standing standard is <strong>16×16 pixels</strong> — it has been the browser-tab and bookmark size since Internet Explorer 5. Modern browsers display a slightly larger icon, so 32×32 is now the practical default for the tab itself."),
    ("Is 16×16 or 32×32 better for a favicon?",
     "Ship both. A 32×32 icon looks crisp on high-DPI (Retina) displays where the tab is rendered at 2× scale, while 16×16 is still needed for bookmarks, history lists and older browsers. An ICO file can hold multiple resolutions, so there is no reason to choose."),
    ("Do I need a 512×512 favicon?",
     "Only if you want an <strong>installable web app (PWA)</strong> or you want Google to display your icon next to your site in mobile search results. Android uses 192×192 for the home-screen shortcut and 512×512 for the splash screen, and both come from your web app manifest."),
    ("Can a favicon be a PNG instead of an ICO file?",
     "Yes. Every modern browser (Chrome, Edge, Firefox, Safari) accepts PNG favicons declared with the <code>icon</code> link tag. You still want an ICO, because it packs several resolutions into one file and covers older Windows shortcuts and legacy browsers."),
    ("What size is the Apple Touch Icon?",
     "<strong>180×180 px</strong> for current iPhones and iPads. Apple recommends a square PNG with no transparency, because iOS composites it onto a solid background — an icon with a transparent background can end up on black."),
    ("Why does my favicon look blurry?",
     "Three usual causes: the source image is smaller than the size you are asking for (so it gets upscaled), the source is not square (so it gets squashed or padded), or you only supplied a 16×16 icon and the browser stretched it for a high-DPI tab. Always generate from a square source of at least 512×512."),
    ("How many sizes should one ICO file contain?",
     "Three is the sweet spot: <strong>16×16, 32×32 and 48×48</strong>. Add 64×64 and 128×128 if you also use the file for desktop shortcuts. The whole point of ICO is that the operating system picks the closest match, so extra sizes cost bytes but never cost quality."),
]

SIZES_BODY = """      <h2 id="what-size">What size should a favicon be?</h2>
      <p>The honest answer is that a favicon is not one size — it is <strong>a small set of sizes</strong>, and which sizes you need depends on where the icon is displayed. A browser tab, an iPhone home screen and an Android splash screen all draw from different files at different resolutions.</p>
      <p>If you only remember one number, remember <strong>16×16 pixels</strong>. That is the size a favicon has been since 1999 and it is still what most bookmarks and history lists use. If you want the icon to look sharp everywhere without thinking about it, generate the four sizes below and wire them up once.</p>

      <h2 id="chart">The complete favicon size chart</h2>
      <p>These are the sizes that actually matter in 2026. Anything larger than 512×512 is a source asset, not a favicon.</p>
      <table>
        <tr><th>Size</th><th>Format</th><th>Where it is used</th></tr>
        <tr><td>16×16</td><td>ICO / PNG</td><td>Browser tab, bookmarks, history, the classic default</td></tr>
        <tr><td>32×32</td><td>ICO / PNG</td><td>High-DPI browser tabs, Windows taskbar shortcuts</td></tr>
        <tr><td>48×48</td><td>ICO / PNG</td><td>Windows site icons and desktop shortcuts</td></tr>
        <tr><td>96×96</td><td>PNG</td><td>Legacy Android home-screen icon (still referenced by older templates)</td></tr>
        <tr><td>150×150</td><td>PNG</td><td>Windows tile image (<code>mstile</code>)</td></tr>
        <tr><td>180×180</td><td>PNG</td><td>Apple Touch Icon — iPhone and iPad home screen</td></tr>
        <tr><td>192×192</td><td>PNG</td><td>Android home screen, PWA manifest icon</td></tr>
        <tr><td>512×512</td><td>PNG</td><td>Android splash screen, PWA install, Google mobile results</td></tr>
      </table>

      <h2 id="minimum">The minimum favicon set for 2026</h2>
      <p>If you want to stop reading and just ship something correct, produce these four files and drop them in your site root:</p>
      <div class="code-block">/favicon.ico               16×16 + 32×32 (+ 48×48) packed into one ICO
/favicon-32x32.png         32×32 PNG
/favicon-16x16.png         16×16 PNG
/apple-touch-icon.png      180×180 PNG, no transparency

Optional but recommended for installable web apps:
/icon-192.png              192×192 PNG
/icon-512.png              512×512 PNG
/site.webmanifest          declares the two icons above</div>
      <p>That set covers browser tabs, bookmarks, Windows shortcuts, iPhone home screens, Android home screens and PWA splash screens. It is what our own <a href="/favicon-generator.html">favicon generator</a> outputs.</p>

      <h2 id="why-multiple">Why one size is never enough</h2>
      <p>A single 512×512 PNG scaled down to 16×16 looks muddy. Browsers downscale by averaging neighbouring pixels, so fine detail — thin strokes, small text, a complicated monogram — turns into grey mush. The fix is not a better algorithm, it is <strong>supplying a purpose-drawn icon for each size</strong>.</p>
      <p>That is exactly what the ICO format is for. An ICO file is a container: it holds one bitmap per resolution, and the operating system or browser picks whichever is closest to what it needs. Ship a 16×16 that has been simplified (thicker strokes, no fine detail) alongside a 32×32 and a 48×48, and every context gets a version that was designed for it.</p>
      <div class="note"><b>Rule of thumb:</b> the smaller the icon, the simpler it must be. If your logo has a wordmark, drop it below 48×48 and use the glyph or the initial letter only.</div>

      <h2 id="platforms">Platform-by-platform requirements</h2>
      <p>Each platform looks for a specific file. This is the checklist to work through when a favicon works on one device but not another.</p>
      <table>
        <tr><th>Platform / surface</th><th>File it looks for</th><th>Size</th></tr>
        <tr><td>Browser tab (Chrome, Edge, Firefox, Safari)</td><td><code>favicon.ico</code></td><td>16×16 &amp; 32×32</td></tr>
        <tr><td>Bookmarks &amp; history</td><td><code>favicon.ico</code></td><td>16×16</td></tr>
        <tr><td>iOS / iPadOS home screen</td><td><code>apple-touch-icon.png</code></td><td>180×180</td></tr>
        <tr><td>Android home screen (PWA)</td><td>manifest <code>icon-192.png</code></td><td>192×192</td></tr>
        <tr><td>Android splash screen (PWA)</td><td>manifest <code>icon-512.png</code></td><td>512×512</td></tr>
        <tr><td>Windows taskbar / desktop shortcut</td><td><code>favicon.ico</code></td><td>32×32 or 48×48</td></tr>
        <tr><td>Safari pinned tab</td><td><code>mask-icon.svg</code></td><td>Any (monochrome SVG)</td></tr>
        <tr><td>Google mobile search result</td><td>Any declared icon</td><td>≥ 48×48, square</td></tr>
      </table>
      <p>For the exact markup that declares each of these, see <a href="/tutorials/how-to-add-a-favicon-to-a-website/">how to add a favicon to a website</a>.</p>

      <h2 id="mistakes">Common favicon size mistakes</h2>
      <ul>
        <li><strong>Starting from a small source.</strong> If your master file is 64×64 you can never produce a clean 512×512. Keep a square master of at least 512×512, ideally 1024×1024.</li>
        <li><strong>Using a non-square image.</strong> Favicons are square. A 500×300 logo gets squashed, or padded with bars, and looks broken at 16×16.</li>
        <li><strong>Assuming one file is enough.</strong> A lone 16×16 stretched onto a Retina display is the most common cause of "my favicon is blurry".</li>
        <li><strong>Fine detail at small sizes.</strong> Text and hairlines disappear below 32×32. Simplify the small variant.</li>
        <li><strong>Transparent apple-touch-icon.</strong> iOS renders transparency as black. Fill the background.</li>
        <li><strong>Forgetting the manifest.</strong> Android and PWA installs read <code>site.webmanifest</code>, not <code>favicon.ico</code> — without it, your icon shows as a grey placeholder.</li>
      </ul>

      <h2 id="generate">How to generate every size at once</h2>
      <p>You do not need Photoshop or a command line. Drop a square source image into FaviconPal and it produces the ICO plus every PNG size listed above, along with the <code>&lt;head&gt;</code> snippet and the manifest file. Everything runs locally in your browser — nothing is uploaded.</p>
      <div class="cta-inline">
        <a class="btn primary" href="/favicon-generator.html">Generate the full favicon set →</a>
      </div>

      <h2 id="faq">Frequently asked questions</h2>
"""

SIZES_HTML = render(
    slug="/tutorials/favicon-sizes/",
    title="Favicon Sizes Explained – What Size Should a Favicon Be?",
    desc="The standard favicon size is 16×16 px. See every size you actually need — 16, 32, 48, 180, 192, 512 — plus how ICO and manifest set them up.",
    h1="Favicon Sizes Explained: What Size Should a Favicon Be?",
    hero_p="Every favicon size that matters, what each one is for, and the four files that cover every browser, phone and installable web app.",
    answer="A favicon should be <strong>16×16 px at minimum</strong>. Ship 16×16 and 32×32 inside a single <code>favicon.ico</code> for tabs and bookmarks, then add PNGs at <strong>180×180</strong> (Apple Touch Icon), <strong>192×192</strong> and <strong>512×512</strong> (Android and PWA) so the icon stays sharp on every device.",
    toc=[("what-size", "What size should a favicon be?"),
         ("chart", "The complete favicon size chart"),
         ("minimum", "The minimum favicon set for 2026"),
         ("why-multiple", "Why one size is never enough"),
         ("platforms", "Platform-by-platform requirements"),
         ("mistakes", "Common favicon size mistakes"),
         ("generate", "How to generate every size at once"),
         ("faq", "Frequently asked questions")],
    body=SIZES_BODY + "\n  " + faq_html(SIZES_FAQ) + "\n\n" + TOOL_LINKS,
    faq=SIZES_FAQ,
    crumbs=[("Home", BASE + "/"), ("Guides", BASE + "/tutorials/"), ("Favicon Sizes", BASE + "/tutorials/favicon-sizes/")],
    badges=[("📐 Every size in one place", "blue"), ("⚡ Generated in your browser", "green"), ("🆓 Free forever", "blue")],
)

# ===========================================================================
# Guide 2 — what is a favicon
# ===========================================================================
WHAT_FAQ = [
    ("What is a favicon in one sentence?",
     "A favicon is the <strong>small square icon that identifies a website</strong> — it appears in browser tabs, bookmarks, history lists, mobile home screens and often next to your site in search results."),
    ("What does the word favicon mean?",
     "It is a contraction of <strong>\"favorites icon\"</strong>, coined when Internet Explorer 5 introduced the feature in 1999. The file was literally the icon for your Favorites menu, and the name stuck even though that menu is now called Bookmarks."),
    ("Where do favicons show up?",
     "Browser tabs, the address bar, bookmarks, browsing history, mobile home screens when a site is saved or installed, Android and iOS app switchers, and increasingly in mobile search results and browser tab search."),
    ("What file format should a favicon use?",
     "<strong>ICO</strong> for the legacy multi-resolution file, <strong>PNG</strong> for modern browsers and mobile icons, and <strong>SVG</strong> for a crisp scalable monochrome Safari pinned tab. JPG is a poor choice because it has no transparency."),
    ("Do favicons affect SEO?",
     "Not directly — a favicon is not a ranking factor. It does affect <strong>click-through rate</strong>: a recognisable icon in a search result or tab makes a site look legitimate and helps returning visitors spot it instantly, and browsers and search engines may display it beside your result."),
    ("Can I use a favicon that is not a square?",
     "Technically yes, but do not. Browsers and operating systems crop or pad non-square icons, so an off-ratio image ends up stretched or letterboxed. Always start from a square source."),
]

WHAT_BODY = """      <h2 id="definition">What is a favicon?</h2>
      <p>A favicon is a small, square icon that identifies a website or web page. The browser fetches it once and then reuses it everywhere the site is referenced — the tab strip, the address bar, the bookmarks menu, the history list, and the home screen if the site is saved or installed on a phone.</p>
      <p>It is one of the oldest pieces of web branding still in daily use, and it is the only piece of your visual identity that sits permanently inside the browser chrome rather than inside the page.</p>

      <h2 id="etymology">Where does the word \"favicon\" come from?</h2>
      <p>Favicon is a contraction of <strong>favorites icon</strong>. Microsoft introduced the feature with Internet Explorer 5 in 1999: the browser looked for a file called <code>favicon.ico</code> in the root of your site and used it as the icon next to the page in the Favorites menu.</p>
      <p>The Favorites menu was later renamed Bookmarks, and browsers stopped requiring the exact filename, but the name and the convention survived. To this day the safest place to put your icon is still <code>/favicon.ico</code> in the site root.</p>

      <h2 id="where">Where favicons appear</h2>
      <ul>
        <li><strong>Browser tabs</strong> — the primary use. The icon is how users recognise your tab among twenty others.</li>
        <li><strong>Address bar and search bar</strong> — shown as a trust cue next to the URL.</li>
        <li><strong>Bookmarks and favourites</strong> — a bookmark without an icon looks broken.</li>
        <li><strong>Browsing history</strong> — helps users find a page they visited earlier.</li>
        <li><strong>Mobile home screen</strong> — via <code>apple-touch-icon</code> on iOS and the web app manifest on Android.</li>
        <li><strong>Installable web apps (PWA)</strong> — the icon is part of the install prompt and the splash screen.</li>
        <li><strong>Search results</strong> — Google and other engines may show your icon beside your result on mobile.</li>
      </ul>
      <p>Because it appears in so many places, a favicon is usually the most-seen image on a website in terms of raw impressions per visitor.</p>

      <h2 id="formats">Favicon file formats compared</h2>
      <table>
        <tr><th>Format</th><th>Transparency</th><th>Best for</th><th>Browser support</th></tr>
        <tr><td>ICO</td><td>Yes (1-bit or 32-bit)</td><td>Multi-resolution tab icon, Windows shortcuts</td><td>Universal, including legacy</td></tr>
        <tr><td>PNG</td><td>Yes (8-bit alpha)</td><td>Modern tabs, Apple Touch Icon, PWA icons</td><td>All current browsers</td></tr>
        <tr><td>SVG</td><td>Yes</td><td>Safari pinned tab, crisp at any scale</td><td>Safari (pinned tabs), modern Chrome/Firefox</td></tr>
        <tr><td>WebP</td><td>Yes</td><td>Small file size on modern browsers</td><td>Chrome, Edge, Firefox — not Safari everywhere</td></tr>
        <tr><td>AVIF</td><td>Yes</td><td>Smallest file size, newest format</td><td>Chrome, Firefox, Safari 16+</td></tr>
        <tr><td>JPG</td><td>No</td><td>Not recommended for icons</td><td>Renders, but edges show white boxes</td></tr>
        <tr><td>GIF</td><td>Yes (1-bit)</td><td>Animated favicons (rarely a good idea)</td><td>All browsers, but animation is distracting</td></tr>
      </table>
      <div class="note"><b>Practical advice:</b> use ICO as the baseline, PNG for the mobile and manifest icons, and SVG only as an optional Safari pinned-tab extra. That combination covers everything without juggling exotic formats.</div>

      <h2 id="matters">Why favicons matter</h2>
      <h3>Instant brand recognition</h3>
      <p>Users keep dozens of tabs open. A distinctive icon lets them find yours without reading a single tab title, which is worth more than most people assume — it is the difference between a tab staying open and being closed.</p>
      <h3>Perceived legitimacy</h3>
      <p>A site with no favicon shows a generic globe icon. That reads as unfinished, and on a checkout or signup page it reads as suspicious. The icon is a small trust signal, but it is one users notice when it is missing.</p>
      <h3>Better click-through in search</h3>
      <p>Search engines may display your icon beside your listing on mobile. A recognisable icon makes a result easier to spot among competitors, particularly for branded queries.</p>
      <h3>Required for installable web apps</h3>
      <p>If you want your site to be installable on a phone, a proper icon set is mandatory — Android and iOS will not offer the install prompt without one.</p>

      <h2 id="how">How do you add a favicon?</h2>
      <p>Three steps: generate the icon files, upload them to the root of your site, and declare them in the <code>&lt;head&gt;</code> of every page. The full walkthrough, including the exact HTML and how to clear your cache when the old icon refuses to go away, is in <a href="/tutorials/how-to-add-a-favicon-to-a-website/">how to add a favicon to a website</a>.</p>
      <p>If you are still deciding what resolution you need, start with <a href="/tutorials/favicon-sizes/">favicon sizes explained</a>.</p>

      <h2 id="faq">Frequently asked questions</h2>
"""

WHAT_HTML = render(
    slug="/tutorials/what-is-a-favicon/",
    title="What Is a Favicon? Definition, Purpose & Examples",
    desc="A favicon is the small icon shown in browser tabs, bookmarks and search results. Learn what it is, where it appears, which formats work and why it matters.",
    h1="What Is a Favicon? Definition, Purpose &amp; Formats",
    hero_p="The small icon that represents your site in a browser tab, a bookmark and a mobile home screen — what it is, where it appears, and which file format to use.",
    answer="A favicon is the <strong>small square icon that identifies a website</strong>. Browsers show it in the tab strip, address bar, bookmarks and history, and phones show it on the home screen when a site is saved or installed. The name is short for <strong>\"favorites icon\"</strong>.",
    toc=[("definition", "What is a favicon?"),
         ("etymology", "Where the word comes from"),
         ("where", "Where favicons appear"),
         ("formats", "Favicon file formats compared"),
         ("matters", "Why favicons matter"),
         ("how", "How do you add one?"),
         ("faq", "Frequently asked questions")],
    body=WHAT_BODY + "\n  " + faq_html(WHAT_FAQ) + "\n\n" + TOOL_LINKS,
    faq=WHAT_FAQ,
    crumbs=[("Home", BASE + "/"), ("Guides", BASE + "/tutorials/"), ("What Is a Favicon", BASE + "/tutorials/what-is-a-favicon/")],
    badges=[("💡 Plain-English definition", "blue"), ("🧩 Format comparison table", "blue"), ("🆓 No signup", "green")],
)

# ===========================================================================
# Guide 3 — how to add a favicon to a website
# ===========================================================================
ADD_FAQ = [
    ("How do I add a favicon to my website?",
     "Put <code>favicon.ico</code> in the root folder of your site, then add <code>&lt;link rel=\"icon\" href=\"/favicon.ico\" sizes=\"any\"&gt;</code> inside the <code>&lt;head&gt;</code> of every page. Add the PNG and Apple Touch Icon links alongside it. Finally, hard-refresh your browser, because favicons are cached aggressively."),
    ("Where exactly do favicon files go?",
     "In the <strong>root directory</strong> of the site — the same folder that holds <code>index.html</code> — so they resolve at <code>https://example.com/favicon.ico</code>. Browsers request <code>/favicon.ico</code> automatically even if you never declare it, which is why the root location is the safest default."),
    ("Why is my favicon not showing up?",
     "Almost always caching, or a wrong path. Check in this order: hard-refresh (Ctrl/Cmd+Shift+R), open <code>yourdomain.com/favicon.ico</code> directly to confirm it loads, verify the file is in the site root and not inside an images subfolder, confirm your <code>&lt;link&gt;</code> tags are in the <code>&lt;head&gt;</code> rather than the body, and remember browsers may take hours to refresh a favicon they already cached."),
    ("Does the favicon need to be on every page?",
     "Yes. The <code>&lt;link&gt;</code> tags belong in the <code>&lt;head&gt;</code> of every page you want the icon on. On a static site that usually means a shared template or partial; in a CMS it is normally a single site-wide setting."),
    ("How do I add a favicon in WordPress?",
     "Appearance → Customize → <strong>Site Identity</strong> → <strong>Site Icon</strong>, then upload a square image of at least 512×512. WordPress generates the resized versions and writes the markup for you. Older themes may instead expose the setting under Appearance → Customize → Header."),
    ("How do I add a favicon to Shopify, Wix or Squarespace?",
     "Shopify: Online Store → Themes → Customize → Theme settings → Favicon. Wix: Settings → Business Info → Favicon. Squarespace: Design → Browser Icon. All three accept a square PNG, and all three generate the file themselves."),
    ("Do I need the site.webmanifest file?",
     "Only if you want an <strong>installable web app</strong> or a correct Android home-screen icon. The manifest declares the 192×192 and 512×512 icons Android uses. Desktop browsers ignore it, so omitting it does not break your tab icon — it just leaves Android without a proper icon."),
]

ADD_BODY = """      <h2 id="step1">Step 1 — Generate your favicon files</h2>
      <p>Start from a <strong>square</strong> image, at least 512×512 pixels. Non-square sources get stretched or padded, and small sources can never be upscaled cleanly.</p>
      <p>FaviconPal converts your image and produces the whole set locally in your browser — the ICO, the PNG sizes, the HTML snippet and the manifest. Nothing is uploaded to a server.</p>
      <div class="cta-inline">
        <a class="btn primary" href="/favicon-generator.html">Open the favicon generator →</a>
      </div>
      <p>Prefer to convert a specific source format? Use <a href="/">WebP to ICO</a>, <a href="/jpg-to-ico/">JPG to ICO</a>, <a href="/svg-to-ico/">SVG to ICO</a> or <a href="/avif-to-ico/">AVIF to ICO</a>.</p>

      <h2 id="step2">Step 2 — Upload the files to your site root</h2>
      <p>Place the files in the same directory as your <code>index.html</code>, not in a subfolder. Browsers look for <code>favicon.ico</code> at the root of the domain by default, so this location works even before you write any markup.</p>
      <div class="code-block">your-website/
├── index.html          ← the page you are editing
├── favicon.ico         ← 16×16 + 32×32 (+ 48×48) in one file
├── favicon-32x32.png
├── favicon-16x16.png
├── apple-touch-icon.png    ← 180×180, opaque background
├── icon-192.png            ← optional, for Android / PWA
├── icon-512.png            ← optional, for Android / PWA
└── site.webmanifest        ← optional, declares the two icons above</div>
      <div class="note"><b>Common mistake:</b> uploading the icon to <code>/images/favicon.ico</code>. It will still work if you declare the full path, but browsers will also keep requesting <code>/favicon.ico</code> and getting a 404. Put it at the root.</div>

      <h2 id="step3">Step 3 — Add the HTML to your &lt;head&gt;</h2>
      <p>Paste this into the <code>&lt;head&gt;</code> section of every page — after the <code>&lt;title&gt;</code> and meta tags. Order matters: the ICO goes first so older browsers, which stop at the first supported entry, pick it up.</p>
      <div class="code-block">&lt;link rel="icon" href="/favicon.ico" sizes="any"&gt;
&lt;link rel="icon" href="/favicon-32x32.png" sizes="32x32" type="image/png"&gt;
&lt;link rel="icon" href="/favicon-16x16.png" sizes="16x16" type="image/png"&gt;
&lt;link rel="apple-touch-icon" href="/apple-touch-icon.png"&gt;
&lt;link rel="manifest" href="/site.webmanifest"&gt;</div>
      <p>A shortcut for the same thing in PHP-based themes and includes:</p>
      <div class="code-block">&lt;?php include $_SERVER['DOCUMENT_ROOT'] . '/favicon-head.html'; ?&gt;</div>

      <h2 id="step4">Step 4 — Add the web app manifest</h2>
      <p>The manifest is what Android and installable web apps read. Create <code>site.webmanifest</code> in your site root:</p>
      <div class="code-block">{
  "name": "Your Site Name",
  "short_name": "YourSite",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#ffffff",
  "background_color": "#ffffff",
  "display": "standalone"
}</div>
      <p>The <code>theme_color</code> is what Android tints the status bar with once the site is installed, so set it to your brand colour for a coherent look.</p>

      <h2 id="step5">Step 5 — Clear the cache and verify</h2>
      <p>This is the step almost everyone skips, and it is the reason people think their new favicon \"did not work\". Browsers cache favicons far longer than ordinary page assets.</p>
      <ol>
        <li><strong>Hard refresh:</strong> <code>Ctrl+Shift+R</code> on Windows or <code>Cmd+Shift+R</code> on macOS.</li>
        <li><strong>Check the file directly:</strong> open <code>https://yourdomain.com/favicon.ico</code> in a new tab. If it downloads or displays, the file is in the right place.</li>
        <li><strong>Try a private window</strong> — it ignores the cached favicon.</li>
        <li><strong>Purge your CDN cache</strong> if you use Cloudflare, Vercel or similar; the icon may be served from the edge.</li>
        <li><strong>Wait.</strong> Even after a purge, some browsers keep a favicon for hours or until the tab is closed.</li>
      </ol>

      <h2 id="cms">CMS quick reference</h2>
      <table>
        <tr><th>Platform</th><th>Where to set it</th><th>Acceptable input</th></tr>
        <tr><td>WordPress</td><td>Appearance → Customize → Site Identity → Site Icon</td><td>Square image, min 512×512</td></tr>
        <tr><td>Shopify</td><td>Online Store → Themes → Customize → Theme settings → Favicon</td><td>PNG or ICO, 32×32 recommended</td></tr>
        <tr><td>Wix</td><td>Settings → Business Info → Favicon</td><td>PNG, JPG or ICO</td></tr>
        <tr><td>Squarespace</td><td>Design → Browser Icon</td><td>PNG or ICO, min 100×100</td></tr>
        <tr><td>Webflow</td><td>Project Settings → General → Favicon</td><td>PNG or ICO, 32×32</td></tr>
        <tr><td>Static HTML / Next.js / Astro</td><td>Files in the public or root folder + <code>&lt;link&gt;</code> tags</td><td>Full manual control</td></tr>
      </table>

      <h2 id="troubleshoot">Why your favicon is still not showing</h2>
      <table>
        <tr><th>Symptom</th><th>Likely cause</th><th>Fix</th></tr>
        <tr><td>Generic globe icon</td><td>File missing from the site root</td><td>Move <code>favicon.ico</code> next to <code>index.html</code></td></tr>
        <tr><td>Old icon persists</td><td>Browser or CDN cache</td><td>Hard refresh and purge the CDN</td></tr>
        <tr><td>Sharp on desktop, blurry on phone</td><td>No 180×180 Apple Touch Icon</td><td>Add <code>apple-touch-icon.png</code> and declare it</td></tr>
        <tr><td>Works on desktop, blank on Android</td><td>No web app manifest</td><td>Add <code>site.webmanifest</code> with 192 and 512 icons</td></tr>
        <tr><td>Icon appears on some pages only</td><td><code>&lt;link&gt;</code> tags missing from a template</td><td>Add them to the shared layout</td></tr>
        <tr><td>White box around the icon</td><td>Source was a JPG with no transparency</td><td>Regenerate from a PNG or SVG source</td></tr>
        <tr><td>Icon squashed or letterboxed</td><td>Non-square source image</td><td>Crop to a square master and regenerate</td></tr>
      </table>

      <h2 id="faq">Frequently asked questions</h2>
"""

ADD_HTML = render(
    slug="/tutorials/how-to-add-a-favicon-to-a-website/",
    title="How to Add a Favicon to a Website – HTML Code & WordPress",
    desc="Step-by-step: generate the files, upload them to your site root, paste the HTML link tags, and clear the cache so the new favicon actually shows up.",
    h1="How to Add a Favicon to a Website",
    hero_p="The complete walkthrough — files, folder placement, the exact HTML, the manifest, plus the cache-clearing step that makes the new icon actually appear.",
    answer="Put <code>favicon.ico</code> in your site's <strong>root folder</strong>, then paste <code>&lt;link rel=\"icon\" href=\"/favicon.ico\" sizes=\"any\"&gt;</code> into the <code>&lt;head&gt;</code> of every page, alongside the 32×32, 16×16 and Apple Touch Icon links. Then <strong>hard-refresh</strong> — favicons are cached far longer than normal assets.",
    toc=[("step1", "1. Generate the files"),
         ("step2", "2. Upload to your site root"),
         ("step3", "3. Add the HTML to <head>"),
         ("step4", "4. Add the web app manifest"),
         ("step5", "5. Clear the cache and verify"),
         ("cms", "CMS quick reference"),
         ("troubleshoot", "Why it is still not showing"),
         ("faq", "Frequently asked questions")],
    body=ADD_BODY + "\n  " + faq_html(ADD_FAQ) + "\n\n" + TOOL_LINKS,
    faq=ADD_FAQ,
    crumbs=[("Home", BASE + "/"), ("Guides", BASE + "/tutorials/"), ("How to Add a Favicon", BASE + "/tutorials/how-to-add-a-favicon-to-a-website/")],
    badges=[("🧱 Works with any stack", "blue"), ("📋 Copy-paste HTML", "blue"), ("🆓 No signup", "green")],
)

# ===========================================================================
# Hub — /tutorials/
# ===========================================================================
HUB_FAQ = [
    ("What is a favicon used for?",
     "Identification. It is the small square icon browsers show for your site in the tab strip, bookmarks, history and — on phones — the home screen, so both new and returning visitors can recognise your site at a glance."),
    ("What size should a favicon be?",
     "16×16 px is the classic minimum and 32×32 px is the practical default for modern high-DPI tabs. A complete set also includes 180×180 for iOS, and 192×192 plus 512×512 for Android and installable web apps."),
    ("How do I add a favicon to my website?",
     "Generate the icon files, upload <code>favicon.ico</code> to your site root, then declare it in the <code>&lt;head&gt;</code> with <code>&lt;link rel=\"icon\" href=\"/favicon.ico\" sizes=\"any\"&gt;</code>. Hard-refresh afterwards, because browsers cache favicons aggressively."),
    ("Is an ICO file still necessary in 2026?",
     "For modern browsers, no — a declared PNG works. But ICO still earns its place: one file holds several resolutions, so the operating system picks the right one for tabs, bookmarks and Windows shortcuts instead of stretching a single image."),
]

HUB_BODY = """      <h2 id="guides">All favicon guides</h2>
      <p>Three guides that answer the questions people actually search for — before they ever look for a converter. Each one links straight to the tool you need.</p>
      <div class="guide-grid">
        <a class="guide-card" href="/tutorials/favicon-sizes/">
          <span class="gc-icon">📐</span>
          <b>Favicon Sizes Explained</b>
          <p>Every size that matters — 16, 32, 48, 180, 192, 512 — what each one is for, the platform-by-platform checklist, and the common mistakes that make icons look blurry.</p>
        </a>
        <a class="guide-card" href="/tutorials/what-is-a-favicon/">
          <span class="gc-icon">💡</span>
          <b>What Is a Favicon?</b>
          <p>The plain-English definition, where the word comes from, every place the icon appears, and a format comparison covering ICO, PNG, SVG, WebP and AVIF.</p>
        </a>
        <a class="guide-card" href="/tutorials/how-to-add-a-favicon-to-a-website/">
          <span class="gc-icon">🧱</span>
          <b>How to Add a Favicon</b>
          <p>Five steps from a square source image to a working icon: folder placement, the exact HTML, the web manifest, CMS instructions and cache troubleshooting.</p>
        </a>
      </div>

      <h2 id="start">Where should you start?</h2>
      <ul>
        <li><strong>Building a site right now?</strong> Go straight to <a href="/tutorials/how-to-add-a-favicon-to-a-website/">how to add a favicon</a> — it includes the generator and the code.</li>
        <li><strong>Icon looks blurry or wrong size?</strong> Start with <a href="/tutorials/favicon-sizes/">favicon sizes</a>, specifically the section on why one size is never enough.</li>
        <li><strong>Not sure what a favicon even is?</strong> Read <a href="/tutorials/what-is-a-favicon/">what is a favicon</a> — it is three minutes.</li>
        <li><strong>Just need the file converted?</strong> Use a converter directly: <a href="/">WebP</a>, <a href="/jpg-to-ico/">JPG</a>, <a href="/svg-to-ico/">SVG</a> or <a href="/avif-to-ico/">AVIF</a> to ICO.</li>
      </ul>

      <h2 id="faq">Frequently asked questions</h2>
"""

HUB_HTML = render(
    slug="/tutorials/",
    title="Favicon Guides & Tutorials – Sizes, Formats & Setup",
    desc="Practical favicon guides: which sizes you actually need, what a favicon is, and the exact HTML to add one to your site. No signup, no fluff.",
    h1="Favicon Guides &amp; Tutorials",
    hero_p="Short, practical answers to the favicon questions people actually search for — sizes, formats, HTML setup and troubleshooting.",
    answer=None,
    toc=None,
    body=HUB_BODY + "\n  " + faq_html(HUB_FAQ) + "\n\n" + TOOL_LINKS,
    faq=HUB_FAQ,
    crumbs=[("Home", BASE + "/"), ("Guides", BASE + "/tutorials/")],
    badges=[("📚 3 practical guides", "blue"), ("🔧 Links straight to the tools", "blue"), ("🆓 Free, no signup", "green")],
)


if __name__ == "__main__":
    pages = [
        ("/tutorials/", HUB_HTML),
        ("/tutorials/favicon-sizes/", SIZES_HTML),
        ("/tutorials/what-is-a-favicon/", WHAT_HTML),
        ("/tutorials/how-to-add-a-favicon-to-a-website/", ADD_HTML),
    ]
    for slug, html_text in pages:
        p = write(slug, html_text)
        print("wrote %-52s %6d bytes" % (slug, os.path.getsize(p)))
