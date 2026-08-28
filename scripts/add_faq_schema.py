"""Faviconpal FAQPage JSON-LD 注入。

从每页可见的 <h2>Frequently asked questions</h2> + <details> 提 Q/A → 生成匹配 JSON-LD → 插入 </head> 前。

幂等：已存在 FAQPage JSON-LD 块时跳过；WebApplication 块保留并存。
"""
import re, json, os, glob, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

EXCLUDE = ('/test/', '/scripts/', '/contact/', '/privacy/')

FAQ_HEAD_RE = re.compile(
    r'<h2[^>]*>Frequently asked questions</h2>\s*<div class="faq">(.*?)</div>',
    flags=re.S,
)
DETAIL_RE = re.compile(
    r'<details>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>',
    flags=re.S,
)
JSONLD_BLOCK_RE = re.compile(
    r'<script type="application/ld\+json">\s*\{[\s\S]*?"@type":\s*"FAQPage"[\s\S]*?</script>',
)


def extract_faq(content):
    """Return list of (question, answer) tuples from visible FAQ cards."""
    m = FAQ_HEAD_RE.search(content)
    if not m:
        return []
    block = m.group(1)
    out = []
    for d in DETAIL_RE.finditer(block):
        q = re.sub(r'\s+', ' ', d.group(1).strip())
        a = re.sub(r'\s+', ' ', d.group(2).strip())
        if q and a:
            out.append((q, a))
    return out


def make_faq_jsonld(items):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def has_existing_faq_jsonld(content):
    return bool(JSONLD_BLOCK_RE.search(content))


def inject(content, jsonld):
    """Insert JSON-LD before </head>. Idempotent: skip if already present."""
    if has_existing_faq_jsonld(content):
        return content, False
    new_c = content.replace('</head>',
                            f'<script type="application/ld+json">\n{jsonld}\n</script>\n</head>',
                            1)
    return new_c, new_c != content


def list_target_pages():
    return sorted(
        f.replace('\\', '/')
        for f in glob.glob('**/*.html', recursive=True)
        if not any(x in ('/' + f.replace('\\','/')) for x in EXCLUDE)
    )


def main():
    dry = '--dry' in sys.argv
    pages = list_target_pages()
    print(f'# target pages: {len(pages)} | mode: {"DRY" if dry else "WRITE"}')
    print('-' * 70)

    n_extract = n_write = n_skip_nofaq = n_skip_exist = 0
    for fn in pages:
        c = open(fn, encoding='utf-8').read()
        if has_existing_faq_jsonld(c):
            print(f'  SKIP  {fn} (already has FAQPage JSON-LD)')
            n_skip_exist += 1
            continue
        items = extract_faq(c)
        if not items:
            print(f'  SKIP  {fn} (no visible FAQ cards)')
            n_skip_nofaq += 1
            continue
        n_extract += len(items)
        jsonld = make_faq_jsonld(items)
        if dry:
            print(f'  PREVIEW {fn}: {len(items)} items, jsonld {len(jsonld)} chars')
            print(f'    first Q: {items[0][0][:60]}')
            continue
        new_c, changed = inject(c, jsonld)
        if changed:
            open(fn, 'w', encoding='utf-8').write(new_c)
            print(f'  WRITE  {fn}: {len(items)} items')
            n_write += 1
        else:
            print(f'  UNCHANGED  {fn}')

    print('-' * 70)
    print(f'# summary: extracted {n_extract} Q/A pairs | wrote {n_write} pages'
          f' | skipped (no FAQ) {n_skip_nofaq} | skipped (already exists) {n_skip_exist}')


if __name__ == '__main__':
    main()
