import os

# 2026-08-25 策略修正：早期低流量工具站不用 OneClick（强干扰、负收益）。
# 已按社群实战结论移除 zone 11641687 的 OneClick 代码（见 remove_monetag_and_rebuild.py）。
# 工具站变现终点是 AdSense（千次访问 ~$6）；UV 破千 + GSC 攒 7 天数据后再申 AdSense，批下即上。
# 本脚本暂不注入任何广告（AD_SCRIPT 留空），并检测是否误残留 OneClick，避免重新注入。
AD_SCRIPT = ""  # OneClick 已移除；未来如需静默型(Popunder/Push)在此替换

BASE = "."
for dp, _, fns in os.walk(BASE):
    for fn in fns:
        if not fn.endswith(".html"):
            continue
        p = os.path.join(dp, fn)
        with open(p, "r", encoding="utf-8") as f:
            txt = f.read()
        if "al5sm.com/tag.min.js" in txt:
            print("WARNING 仍残留 Monetag OneClick:", os.path.relpath(p, BASE))
        if AD_SCRIPT and "</head>" in txt and AD_SCRIPT not in txt:
            txt = txt.replace("</head>", AD_SCRIPT + "\n</head>", 1)
            with open(p, "w", encoding="utf-8") as f:
                f.write(txt)
            print("Injected:", os.path.relpath(p, BASE))
print("Done. No ad script configured (OneClick removed).")
