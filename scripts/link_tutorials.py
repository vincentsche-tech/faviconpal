# -*- coding: utf-8 -*-
"""
Wire the new /tutorials/ cluster into faviconpal.com:
  1. add a "Guides" item to the site nav on every existing page
  2. add a "Favicon guides" internal-link block to the 5 tool pages
  3. register the 4 new URLs in sitemap.xml and bump lastmod on touched pages
Idempotent: re-running makes no further changes.
"""
import os, re

SITE = r"D:\workbuddy-出海web\faviconpal"
TODAY = "2026-09-12"

ALL_PAGES = ["index.html", "favicon-generator.html", "avif-to-ico/index.html",
             "jpg-to-ico/index.html", "svg-to-ico/index.html",
             "contact/index.html", "privacy/index.html"]
LINK_BLOCK_PAGES = ["index.html", "avif-to-ico/index.html", "jpg-to-ico/index.html",
                    "svg-to-ico/index.html", "favicon-generator.html"]

NAV_ANCHOR = '<a href="/favicon-generator.html"'
NAV_INSERT = '\n      <a href="/tutorials/">Guides</a>'

GUIDES_LINK_GRID = """      <h2>Favicon guides</h2>
      <p>New to favicons? Start with the size chart and the setup walkthrough — both link straight back to the converter you need.</p>
      <div class="link-grid">
        <a class="link-card" href="/tutorials/favicon-sizes/"><b>Favicon Sizes Explained</b><p>Every size you need — 16 to 512 — and why one file is never enough.</p></a>
        <a class="link-card" href="/tutorials/what-is-a-favicon/"><b>What Is a Favicon?</b><p>Definition, formats and everywhere the icon appears.</p></a>
        <a class="link-card" href="/tutorials/how-to-add-a-favicon-to-a-website/"><b>How to Add a Favicon</b><p>Folder placement, HTML code, CMS setup and cache fixes.</p></a>
      </div>

"""

GUIDES_TOOL_GRID = """      <h2>Favicon guides</h2>
      <p>New to favicons? Start with the size chart and the setup walkthrough — both link straight back to the converter you need.</p>
      <div class="tool-grid">
        <a class="tool-card-item" href="/tutorials/favicon-sizes/"><span class="tg-ext">Guide</span><b>Favicon Sizes Explained</b><p>Every size you need — 16 to 512 — and why one file is never enough.</p></a>
        <a class="tool-card-item" href="/tutorials/what-is-a-favicon/"><span class="tg-ext">Guide</span><b>What Is a Favicon?</b><p>Definition, formats and everywhere the icon appears.</p></a>
        <a class="tool-card-item" href="/tutorials/how-to-add-a-favicon-to-a-website/"><span class="tg-ext">Guide</span><b>How to Add a Favicon</b><p>Folder placement, HTML code, CMS setup and cache fixes.</p></a>
      </div>

"""

print("=" * 68)
print("1) NAV")
print("=" * 68)
for rel in ALL_PAGES:
    p = os.path.join(SITE, rel.replace("/", os.sep))
    t = open(p, encoding="utf-8").read()
    if '/tutorials/">Guides</a>' in t:
        print("  SKIP  (already has Guides)  %s" % rel)
        continue
    i = t.find(NAV_ANCHOR)
    if i == -1:
        print("  !!    no nav anchor          %s" % rel)
        continue
    j = t.find("</a>", i) + 4
    t = t[:j] + NAV_INSERT + t[j:]
    open(p, "w", encoding="utf-8", newline="").write(t)
    print("  OK    nav updated           %s" % rel)

print()
print("=" * 68)
print("2) GUIDES LINK BLOCK")
print("=" * 68)
for rel in LINK_BLOCK_PAGES:
    p = os.path.join(SITE, rel.replace("/", os.sep))
    t = open(p, encoding="utf-8").read()
    if "<h2>Favicon guides</h2>" in t:
        print("  SKIP  (already has block)   %s" % rel)
        continue
    i = t.find("More conversion tools")
    if i == -1:
        print("  !!    no 'More conversion tools' anchor  %s" % rel)
        continue
    # the grid that follows closes with a line containing only "      </div>"
    m = re.search(r"\n(      </div>)\n", t[i:])
    if not m:
        print("  !!    no grid close found   %s" % rel)
        continue
    at = i + m.end()
    block = GUIDES_TOOL_GRID if "favicon-generator" in rel else GUIDES_LINK_GRID
    t = t[:at] + block + t[at:]
    open(p, "w", encoding="utf-8", newline="").write(t)
    print("  OK    guides block added    %s" % rel)

print()
print("=" * 68)
print("3) SITEMAP")
print("=" * 68)
sm = os.path.join(SITE, "sitemap.xml")
t = open(sm, encoding="utf-8").read()

NEW = [("https://www.faviconpal.com/tutorials/", "0.8", "weekly"),
       ("https://www.faviconpal.com/tutorials/favicon-sizes/", "0.9", "monthly"),
       ("https://www.faviconpal.com/tutorials/what-is-a-favicon/", "0.8", "monthly"),
       ("https://www.faviconpal.com/tutorials/how-to-add-a-favicon-to-a-website/", "0.8", "monthly")]

insert = ""
for url, prio, freq in NEW:
    if url in t:
        print("  SKIP  already listed        %s" % url)
        continue
    insert += ("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
               "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>\n" % (url, TODAY, freq, prio))
    print("  OK    added                 %s" % url)

if insert:
    t = t.replace("</urlset>", insert + "</urlset>")

# bump lastmod for every page we touched (nav/links changed)
TOUCHED = [u for u in [
    "https://www.faviconpal.com/",
    "https://www.faviconpal.com/favicon-generator.html",
    "https://www.faviconpal.com/avif-to-ico/",
    "https://www.faviconpal.com/jpg-to-ico/",
    "https://www.faviconpal.com/svg-to-ico/",
]]
for u in TOUCHED:
    t, n = re.subn(r"(<loc>" + re.escape(u) + r"</loc>\s*<lastmod>)[^<]*(</lastmod>)",
                   r"\g<1>" + TODAY + r"\g<2>", t)
    if n:
        print("  OK    lastmod -> %s  %s" % (TODAY, u))

open(sm, "w", encoding="utf-8", newline="").write(t)
print("  <loc> count now: %d  (was 7)" % t.count("<loc>"))
