import os, re

AD_SCRIPT = """<script>(function(s){s.dataset.zone='11641687',s.src='https://al5sm.com/tag.min.js'})([document.documentElement, document.body].filter(Boolean).pop().appendChild(document.createElement('script')))</script>"""

BASE = "."
changed = 0
skipped = 0
files = []

for dp, _, fns in os.walk(BASE):
    for fn in fns:
        if not fn.endswith(".html"):
            continue
        p = os.path.join(dp, fn)
        with open(p, "r", encoding="utf-8") as f:
            txt = f.read()
        if "al5sm.com/tag.min.js" in txt:
            skipped += 1
            files.append((os.path.relpath(p, BASE), "skipped"))
            continue
        if "</head>" not in txt:
            files.append((os.path.relpath(p, BASE), "no_head_tag"))
            continue
        # insert right before closing </head>
        txt = txt.replace("</head>", AD_SCRIPT + "\n</head>", 1)
        with open(p, "w", encoding="utf-8") as f:
            f.write(txt)
        changed += 1
        files.append((os.path.relpath(p, BASE), "changed"))

print("Changed:", changed)
print("Skipped (already present):", skipped)
for rel, status in files:
    print(f"  {status:12} {rel}")
