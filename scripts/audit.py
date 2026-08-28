"""Faviconpal 步骤 0 审计：title/desc 长度 + FAQPage 覆盖 + 词数"""
import re, html, os, glob, json

os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

EXCLUDE_DIR = ('test/', '/test', 'scripts/', '/scripts')

files = sorted(
    f.replace('\\', '/')
    for f in glob.glob('**/*.html', recursive=True)
    if not any(x in ('/' + f.replace('\\','/')) for x in EXCLUDE_DIR)
)
print(f'# files found: {len(files)}', flush=True)

print(f"{'file':38} {'title':>6} {'desc':>5} {'faq':>4} {'wc':>5}   title")
print('-' * 120)

for fn in files:
    c = open(fn, encoding='utf-8').read()
    mt = re.search(r'<title>(.*?)</title>', c)
    md = re.search(r'<meta name="description" content="(.*?)"', c)
    t = html.unescape(mt.group(1)).strip() if mt else ''
    d = md.group(1).strip() if md else ''
    has_faq = '"@type": "FAQPage"' in c

    # 词数：去 style/script/head/HTML 标签后分词
    body = re.sub(r'<style.*?</style>', '', c, flags=re.S)
    body = re.sub(r'<script.*?</script>', '', body, flags=re.S)
    body = re.sub(r'<head.*?</head>', '', body, flags=re.S)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = re.sub(r'&[a-z]+;', ' ', body)
    body = re.sub(r'\s+', ' ', body).strip()
    wc = len(body.split())

    print(f"{fn:38} {len(t):>6} {len(d):>5} {str(has_faq):>5} {wc:>5}   {t}")

# 同时打印 desc+og+twitter 三同步
print()
print('=' * 80)
print('三标签一致性（title/og:title/twitter:title）')
print('=' * 80)
for fn in files:
    c = open(fn, encoding='utf-8').read()
    t_tag = (re.search(r'<title>(.*?)</title>', c) or [None,''])[1] if re.search(r'<title>(.*?)</title>', c) else ''
    t_tag = html.unescape(t_tag).strip()
    og = re.search(r'<meta property="og:title" content="(.*?)"', c)
    tw = re.search(r'<meta name="twitter:title" content="(.*?)"', c)
    og_t = html.unescape(og.group(1)).strip() if og else 'MISSING'
    tw_t = html.unescape(tw.group(1)).strip() if tw else 'MISSING'
    sync = 'OK' if (t_tag == og_t == tw_t) else 'MISMATCH'
    print(f'{fn:38} [{sync}]  title={len(t_tag)} og={len(og_t)} tw={len(tw_t)}')
    if sync != 'OK':
        print(f'    title:  {t_tag}')
        print(f'    og:     {og_t}')
        print(f'    twitter:{tw_t}')
