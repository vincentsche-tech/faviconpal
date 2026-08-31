import sys

P = "index.html"
s = open(P, encoding="utf-8").read()
DRY = "--dry" in sys.argv

# ---- 1. CSS: 在 .convert-btn:disabled 之后插入 .hero-cta 样式 ----
css_anchor = "  .convert-btn:disabled { opacity: .5; cursor: not-allowed; transform: none; box-shadow: none; }\n"
css_block = css_anchor + """
  .hero-cta {
    display: inline-block; margin-top: 18px; background: #fff; color: #2563eb;
    font-size: 15px; font-weight: 700; padding: 12px 28px; border: 2px solid #2563eb; border-radius: 12px;
    cursor: pointer; transition: transform .1s, box-shadow .15s;
  }
  .hero-cta:hover { transform: translateY(-1px); box-shadow: 0 6px 16px -4px rgba(37,99,235,.4); }
"""
assert css_anchor in s, "CSS anchor not found"

# ---- 2. HTML: hero-badges 关闭后插入按钮 ----
html_anchor = """      <div class="hero-badges">
        <span class="badge green">🔒 100% local · files never leave your device</span>
        <span class="badge blue">⚡ Instant, in-browser</span>
        <span class="badge blue">🆓 Free forever</span>
      </div>
    </section>"""
html_block = html_anchor.replace(
    "      </div>\n    </section>",
    "      </div>\n      <button class=\"hero-cta\" id=\"trySample\" type=\"button\">\u2728 Try it with a sample image \u2192</button>\n    </section>",
    1,
)
assert html_anchor in s, "HTML anchor not found"

# ---- 3. JS: convertBtn handler 之后插入 trySample handler ----
js_anchor = "  function scaleSourceToCanvas(srcCanvas, size, qualityMode) {"
svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">'
    '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#2563eb"/><stop offset="1" stop-color="#7c3aed"/>'
    '</linearGradient></defs>'
    '<rect width="256" height="256" rx="56" fill="url(#g)"/>'
    '<circle cx="128" cy="100" r="42" fill="#ffffff" opacity="0.95"/>'
    '<rect x="90" y="150" width="76" height="15" rx="7.5" fill="#ffffff" opacity="0.9"/>'
    '<text x="128" y="232" font-family="Arial, sans-serif" font-size="22" font-weight="bold" '
    'fill="#ffffff" text-anchor="middle" opacity="0.92">FaviconPal</text></svg>'
)
js_block = (
    "  /* ---- one-click sample ---- */\n"
    "  const trySample = $('trySample');\n"
    "  if (trySample) {\n"
    "    trySample.addEventListener('click', async () => {\n"
    "      const blob = new Blob([`" + svg + "`], { type: 'image/svg+xml' });\n"
    "      const file = new File([blob], 'sample-logo.svg', { type: 'image/svg+xml' });\n"
    "      await addFiles([file]);\n"
    "      document.getElementById('tool').scrollIntoView({ behavior: 'smooth', block: 'start' });\n"
    "      convertBtn.click();\n"
    "    });\n"
    "  }\n\n"
) + js_anchor
assert js_anchor in s, "JS anchor not found"

if DRY:
    print("=== CSS preview (after anchor) ===")
    print(css_block)
    print("=== HTML preview (button line) ===")
    print("      <button class=\"hero-cta\" id=\"trySample\" type=\"button\">\u2728 Try it with a sample image \u2192</button>")
    print("=== JS preview ===")
    print(js_block)
    print("All 3 anchors present — DRY OK.")
else:
    s = s.replace(css_anchor, css_block, 1)
    s = s.replace(html_anchor, html_block, 1)
    s = s.replace(js_anchor, js_block, 1)
    open(P, "w", encoding="utf-8").write(s)
    print("OK: trySample button + handler added to index.html")
