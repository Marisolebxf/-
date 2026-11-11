# -*- coding: utf-8 -*-
"""校验生产前端 bundle 的 ECO 页面版本（R1 基线 / R2 人才四图+高企列+灌数标注）。只读外网。

入口 chunk 里 eco 页是懒加载动态 import，文件名带 hash，故列出入口引用的全部 js 全量扫描（**不早停**）。

判定分两层（踩坑记录，2026-11-11）：
- ``R1_BASELINE``：R1 版本就有的页面串，只用来**定位 ECO 页 chunk**，不能用来判版本；
- ``R2_ONLY``：R2 才引入的串，用来**判版本**。

为什么必须分层：早前用「高新技术企业 / 演示种子」当 R2 特征会误判——「高新技术企业」在 R1 的数据源台账
文案里已存在（"创新载体 / 人才 / 高新技术企业 / 专利"），而「演示种子」在 knowledge-graph、policy 等
其它页面同样出现（"lumen 演示种子（demo 冻结）"），两者都不能证明 ECO 页已升级。
"""
import io, re, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
UA = {"User-Agent": "Mozilla/5.0"}
BASE = "https://edu.itic-sci.com"

# R1 基线：用于定位 ECO 页 chunk
R1_BASELINE = [
    "数据梳理分析", "接口开发设计", "前端演示目录", "暂无视频资料", "暂无资讯", "载体名录检索",
]
# R2 独有：用于判版本（人才四图懒加载 / 灌数标注 / 高企接口参数 / 指标编码）
R2_ONLY = [
    "talent-panorama",       # 561 人才态势端点（api 层）
    "M_SCIUI_SVC_001",       # 人才旭日卡指标编码
    "演示灌数",               # 专利趋势灌数标注
    "人才结构四指标",          # 人才页签说明文案
    "is_high_tech",          # 区级下钻高企列参数
]


def get(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=60
    ).read().decode("utf-8", "ignore")


html = get(BASE + "/tid/service/innovation-ecology-service")
entry = re.search(r'src="(/tid/assets/[^"]+\.js)"', html).group(1)
print("entry:", entry)
js = get(BASE + entry)

refs = sorted(set(re.findall(r'"\./([\w.-]+\.js)"', js) + re.findall(r'"(assets/[\w.-]+\.js)"', js)))
print("chunk refs in entry:", len(refs))

bodies = {}
for name in refs:
    url = f"{BASE}/tid/assets/{name}" if not name.startswith("assets/") else f"{BASE}/tid/{name}"
    try:
        bodies[name] = get(url)
    except Exception:  # noqa: BLE001
        continue
print("scanned:", len(bodies))

# ECO 页 chunk = R1 基线命中最多者
eco_name, eco_body, eco_base_hits = None, "", []
for name, body in bodies.items():
    hits = [m for m in R1_BASELINE if m in body]
    if len(hits) > len(eco_base_hits):
        eco_name, eco_body, eco_base_hits = name, body, hits

if not eco_name:
    print("RESULT: 未定位到 ECO 页 chunk（入口引用块未含基线串，可能构建结构变化，需人工核对）")
    sys.exit(2)

print(f"ECO chunk: {eco_name} size={len(eco_body)//1024}KB 基线命中 {len(eco_base_hits)}/{len(R1_BASELINE)}")

r2_hits = [m for m in R2_ONLY if m in eco_body]
missing = [m for m in R2_ONLY if m not in eco_body]
print(f"R2 独有串命中 {len(r2_hits)}/{len(R2_ONLY)}: {r2_hits}")
if missing:
    print("  缺:", missing)

if not missing:
    print("RESULT: 生产已发布 R2 版 ECO 页面")
    sys.exit(0)
if not r2_hits:
    print("RESULT: 生产 ECO 页面仍是 R1 版（基线全中、R2 独有串全缺）→ 前端未发布 R2")
    sys.exit(1)
print(f"RESULT: 生产 ECO 页面部分更新（R2 命中 {len(r2_hits)}/{len(R2_ONLY)}，缺 {missing}）")
sys.exit(1)
