"""严格校验 faviconpal 每页 FAQPage JSON-LD 与可见 <summary>/<p> 卡的 Q/A 逐字一致。

技能 SOP 强调：必须用 json.loads 整块解析，不能用宽松字符串切片正则。
"""
import re, json, os, glob, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

EXCLUDE = ('/test/', '/scripts/', '/contact/', '/privacy/')


def list_targets():
    return sorted(
        f.replace('\\', '/')
        for f in glob.glob('**/*.html', recursive=True)
        if not any(x in ('/' + f.replace('\\','/')) for x in EXCLUDE)
    )


def find_faqpage(content):
    for b in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', content):
        try:
            d = json.loads(b)
        except json.JSONDecodeError:
            continue
        if isinstance(d, dict) and d.get('@type') == 'FAQPage':
            return d
    return None


def get_visible_faq(content):
    """直接读 <summary>Q</summary><p>A</p> 的 Q/A 内容（含 inline code 等原文）。"""
    items = []
    block_m = re.search(
        r'<h2[^>]*>Frequently asked questions</h2>\s*<div class="faq">(.*?)</div>',
        content, flags=re.S,
    )
    if not block_m:
        return items
    for d in re.finditer(
        r'<details>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>',
        block_m.group(1), flags=re.S,
    ):
        q = re.sub(r'\s+', ' ', d.group(1)).strip()
        a = re.sub(r'\s+', ' ', d.group(2)).strip()
        if q and a:
            items.append((q, a))
    return items


def normalize_html_entities(s):
    """把 HTML 实体标准化（去除 &xxx; 转义影响），因为 JSON-LD 的 text 不会含 HTML 实体而 <summary>/<p> 里可能。"""
    # 但 inline <code> 标签保留其符号（不要清掉 tag）— 我们关心原始内容差异
    return s


def main():
    pages = list_targets()
    print(f'# targets: {len(pages)}')
    total_miss = 0
    for fn in pages:
        c = open(fn, encoding='utf-8').read()
        faq = find_faqpage(c)
        if not faq:
            print(f'  {fn}: NO FAQPage JSON-LD')
            continue
        vis = get_visible_faq(c)
        ld = [(ent['name'].strip(), ent['acceptedAnswer']['text'].strip())
              for ent in faq['mainEntity']]
        miss = 0
        if len(vis) != len(ld):
            print(f'  {fn}: COUNT MISMATCH visible={len(vis)} ld={len(ld)}')
            miss += abs(len(vis) - len(ld))
        for i, ((vq, va), (lq, la)) in enumerate(zip(vis, ld)):
            if vq != lq:
                print(f'  {fn} Q{i} DIFF:')
                print(f'    visible: {vq!r}')
                print(f'    ld:      {lq!r}')
                miss += 1
            if va != la:
                print(f'  {fn} A{i} DIFF (Q={vq[:40]!r}):')
                print(f'    visible: {va!r}')
                print(f'    ld:      {la!r}')
                miss += 1
        status = 'PASS' if miss == 0 else f'FAIL ({miss})'
        print(f'  {fn}: visible={len(vis)} ld={len(ld)} {status}')
        total_miss += miss
    print(f'# total misses: {total_miss}')
    sys.exit(0 if total_miss == 0 else 1)


if __name__ == '__main__':
    main()
