# -*- coding: utf-8 -*-
"""校验生产前端 bundle 是否含 ECO 页面最新版本（五页签 + 多媒体空态 + R2 演示种子/高企列）。只读外网。

入口 chunk 里 eco 页是懒加载动态 import，文件名是 hash；故列出入口引用的全部 js，
逐个抓取按页面特征串命中判定（命中即停）。
"""
import io, re, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
UA = {"User-Agent": "Mozilla/5.0"}
BASE = "https://edu.itic-sci.com"


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf-8", "ignore")


html = get(BASE + "/tid/service/innovation-ecology-service")
entry = re.search(r'src="(/tid/assets/[^"]+\.js)"', html).group(1)
print("entry:", entry)
js = get(BASE + entry)

refs = sorted(set(re.findall(r'"\./([\w.-]+\.js)"', js) + re.findall(r'"(assets/[\w.-]+\.js)"', js)))
print("chunk refs in entry:", len(refs))

MARKERS = [
    "数据梳理分析", "接口开发设计", "前端演示目录", "暂无视频资料", "暂无资讯",
    "载体名录检索",
    # R2 特征串：558 已闭环后旧串「区级时序待供数」不再存在，替换为人才种子/高企列/专利灌数
    "演示种子", "高新技术企业", "演示灌数",
]
found = None
for name in refs:
    url = f"{BASE}/tid/assets/{name}" if not name.startswith("assets/") else f"{BASE}/tid/{name}"
    try:
        body = get(url)
    except Exception:  # noqa: BLE001
        continue
    hits = [m for m in MARKERS if m in body]
    if len(hits) >= 3:
        print(f"HIT {name} size={len(body)//1024}KB hits={len(hits)}/{len(MARKERS)} {hits}")
        found = hits
        break

if found:
    missing = [m for m in MARKERS if m not in found]
    print("RESULT: 生产已发布新版 ECO 页面（缺:", missing or "无", "）")
else:
    print("RESULT: 未在入口引用块中命中 ECO 特征串（可能 chunk 未列入入口 preload，需人工核对）")
