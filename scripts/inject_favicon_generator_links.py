"""faviconpal 内链注入：4 converter 页 + index.html 的 nav 加 Favicon Generator；
   More conversion tools 网格加 Favicon Generator card。幂等。"""
import re, os, glob, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')


NAV_INSERT = '\n      <a href="/favicon-generator.html">Favicon Generator</a>'
GRID_CARD = (
    '        <a class="link-card" href="/favicon-generator.html"><b>Favicon Generator</b>'
    '<span class="lk-status live">LIVE</span>'
    '<p>Free in-browser favicon generator – pick any format, get the full set.</p></a>\n'
)

# 只需要 nav 注入的页面（contact/privacy 也加，更一致）
NAV_PAGES = sorted(
    f.replace('\\', '/')
    for f in glob.glob('**/index.html', recursive=True)
    if not any(x in ('/' + f.replace('\\','/')) for x in ('/test/', '/scripts/'))
)
# 同时加 grid card 的页面（只有内容页有 <div class="link-grid">）
GRID_PAGES = sorted(
    f.replace('\\', '/')
    for f in glob.glob('**/index.html', recursive=True)
    if not any(x in ('/' + f.replace('\\','/')) for x in
               ('/test/', '/scripts/', '/contact/', '/privacy/'))
)


def inject_nav(c):
    if 'href="/favicon-generator.html"' in c and '<a href="/favicon-generator.html">' in c:
        return c, False
    new_c = re.sub(
        r'(      <a href="/avif-to-ico/"[^>]*>[^<]+</a>)\s*\n    ',
        r'\1' + NAV_INSERT + '\n    ',
        c, count=1,
    )
    return new_c, new_c != c


def inject_grid_card(c):
    if 'class="link-card" href="/favicon-generator.html"' in c:
        return c, False
    m = re.search(r'(<div class="link-grid">\n)', c)
    if not m:
        return c, False
    insert_pos = m.end()
    return c[:insert_pos] + GRID_CARD + c[insert_pos:], True


def main():
    dry = '--dry' in sys.argv
    print(f'# nav targets: {len(NAV_PAGES)} | grid targets: {len(GRID_PAGES)}'
          f' | mode: {"DRY" if dry else "WRITE"}')
    n_nav = n_grid = 0
    # Pass 1: nav injection across all pages
    for fn in NAV_PAGES:
        c = open(fn, encoding='utf-8').read()
        c2, changed = inject_nav(c)
        print(f'  [nav]   {fn}: added={changed}')
        if not dry and changed:
            open(fn, 'w', encoding='utf-8').write(c2)
            n_nav += 1
    # Pass 2: grid card injection on content pages
    for fn in GRID_PAGES:
        c = open(fn, encoding='utf-8').read()
        c2, changed = inject_grid_card(c)
        print(f'  [grid]  {fn}: added={changed}')
        if not dry and changed:
            open(fn, 'w', encoding='utf-8').write(c2)
            n_grid += 1
    print(f'# summary: nav_injected={n_nav} grid_injected={n_grid}')


if __name__ == '__main__':
    main()
