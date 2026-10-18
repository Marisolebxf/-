# SCI-INT-P00：生成 P00-baseline.yaml 并自检（计数 + 唯一归属）。
# 指标清单来自 MCP metric-registry metric-query（2026-10-18 快照），不读 registry 文件。
# 运行：python 产物/_work/P00-check.py（任意 cwd）
import re
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
AD = HERE.parents[3]  # agent-delivery
SRS = AD / "bid-reference/srs/02-科技信息展示系统"
JIUXIN = AD / "metrics/request/九新-技术机构人才/JIUXIN-TECH-ORG-TALENT-L01.yaml"

A_LEAVES = [  # (leaf, 目录/文件, excel_row 起, 止, DS 页面映射)
    ("A01", "科技发展态势/科技全域态势.md", 4, 19, "DS-01-MAP/LAYERS/FACTORS/EVENTS"),
    ("A02", "科技发展态势/科学技术全景.md", 20, 36, "DS-02-TECHGRAPH/ENTITY/PATH"),
    ("A03", "科技发展态势/科学技术全景.md", 37, 50, "DS-02-MAINTAIN-GRAPH/MAINTAIN-ENTITY"),
    ("A04", "科技发展态势/技术发展跟踪.md", 51, 58, "DS-03-RESULT/WORKFLOW"),
    ("A05", "科技发展态势/全球创新监测.md", 59, 75, "DS-04-ACHIEVE-OVERVIEW/ACHIEVE-DETAIL/REALTIME"),
    ("A06", "科技发展态势/全球创新监测.md", 76, 91, "DS-04-CARRIER-RANK/MONITOR/CITY"),
    ("A07", "科技发展态势/湾区创新监测.md", 92, 114, "DS-05-GBA-*"),
    ("A08", "科技发展态势/深圳创新监测.md", 115, 138, "DS-06-CARRIER/INDICATOR/DOMAIN/CITY"),
    ("A09", "科技发展态势/科技创新评估.md", 139, 161, "DS-07-*"),
    ("A10", "科技发展态势/科技指数.md", 162, 180, "DS-08-INDICATOR/VIZ/RANK"),
    ("A11", "科技发展态势/科技发展规划.md", 181, 199, "DS-09-*"),
    ("A12", "科技人才态势/全球领域人才态势.md", 246, 268, "DS-13-TALENT-GLOBAL"),
    ("A13", "科技人才态势/关注地区人才态势.md", 269, 279, "DS-14-TALENT-REGION"),
    ("A14", "科技人才态势/重点科技人才画像.md", 280, 307, "DS-15-TALENT-PROFILE"),
    ("A15", "科技人才态势/人才引进推荐评估.md", 308, 332, "DS-16-TALENT-RECRUIT"),
]

S, M = "STAT", "MODEL"
B_LEAVES = {  # leaf -> [(metric_id, algorithm_type)]；未列类型 = third_party
    "B02": [f"M_TALENT_DEEP_{n}_1" for n in range(156, 166)],
    "B03": ["M_TALENT_BASE_98_1", "M_TALENT_GRAPH_110_1", "M_TALENT_GRAPH_111_1"]
    + ["M_TALENT_" + s for s in "ACADEMIC_SCORE ATTRACT_SCORE CULTIVATE_SCORE INDUSTRY_SCORE FLOW_TRACK ORG_DIST REGIONAL_DIST RELATION_NET SUPPLY_STRUCT SZ_STATUS SZ_SUPPLY_DEMAND UNIV_NEW".split()],
    "B04": [f"M_TALENT_DS_16_TALENT_RECRUIT_{n}" for n in "005 006 007 010 013 025".split()] + [("M_TALENT_STRUCT_QUERY", S)],
    "B05": [f"M_TECH_DEEP_{n}_1" for n in range(130, 141)],
    "B06": ["M_TECH_BASE_96_1", "M_TECH_GRAPH_104_1", "M_TECH_GRAPH_105_1"]
    + ["M_TECH_" + s for s in "EDGE_STRENGTH ENTITY_INFLUENCE ENTITY_REL ENTITY_TOP5 GRAPH_STRUCT PATH_CENTRALITY PATH_KEYNODE PATH_PRIORITY REL_STRENGTH".split()],
    "B07": [(f"M_TECH_DS_07_TECH_INNOV_{n}", M) for n in "002 004 006".split()]
    + [("M_TECH_" + s, S) for s in "HEAT_QUERY INVEST_AMOUNT OUTPUT_SCALE PAPER_PATENT_CNT".split()]
    + ["M_TECH_" + s for s in "COMPOSITE_SCORE CONVERT_BOTTLENECK HEAT_INDEX LIFE_STAGE MATURITY_LEVEL POTENTIAL_SCORE STAGE_JUDGE SZ_ASSESS TOPIC_HEAT".split()],
    "B08": [f"M_ORG_DEEP_{n}_1" for n in range(149, 156)],
    "B09": ["M_ORG_BASE_99_1", "M_ORG_GRAPH_114_1", "M_ORG_GRAPH_115_1"]
    + ["M_ORG_" + s for s in "ATTENTION_TREND ATTRACT_SCORE COLLAB_CHAIN CULTIVATE_SCORE INDUSTRY_COVER NEW_TREND SZ_ADVANTAGE SZ_PAINPOINT SZ_STATUS TECH_LAYOUT TECH_SCORE".split()]
    + [("M_ORG_PERF_QUERY", S)],
}

BLOCK = re.compile(r"^### (.+?) · 序号 \d+\s*$(.*?)(?=^### |\Z)", re.M | re.S)


def field(body, key):
    m = re.search(rf"^- {key}: (.+)$", body, re.M)
    return m.group(1).strip() if m else None


def srs_rows():
    rows, seen_files = [], {}
    for leaf, rel, lo, hi, ds in A_LEAVES:
        text = seen_files.setdefault(rel, (SRS / rel).read_text(encoding="utf-8"))
        for name, body in BLOCK.findall(text):
            r = int(field(body, "excel_row"))
            if lo <= r <= hi:
                rows.append({"excel_row": r, "seq": int(field(body, "seq")), "name": name.strip(),
                             "path": field(body, "path"), "leaf": leaf, "file": rel, "page_ref": ds})
    # 每个文件的全部块都必须落进某叶（防止范围表漏行）
    for rel, text in seen_files.items():
        all_rows = {int(field(b, "excel_row")) for _, b in BLOCK.findall(text)}
        covered = {x["excel_row"] for x in rows if x["file"] == rel}
        assert all_rows == covered, f"{rel} 未归属行: {sorted(all_rows - covered)}"
    return sorted(rows, key=lambda x: x["excel_row"])


def metric_rows():
    out = []
    for leaf, items in B_LEAVES.items():
        for it in items:
            mid, t = it if isinstance(it, tuple) else (it, "third_party")
            out.append({"metric_id": mid, "domain": mid.split("_")[1], "algorithm_type": t, "leaf": leaf})
    return out


def jiuxin_rows():
    items = yaml.safe_load(JIUXIN.read_text(encoding="utf-8"))["items"]
    return [{"row_id": i["row_id"], "系统": i.get("系统"), "维度": i.get("维度"), "page_id": i.get("page_id"),
             "名称": i.get("主项/库叶名"), "algorithm_type": i.get("algorithm.type"),
             "交付形态": i.get("交付形态"), "确认": i.get("九新确认"), "row_kind": i.get("row_kind")} for i in items]


def main():
    srs, mets, jx = srs_rows(), metric_rows(), jiuxin_rows()

    rows = [x["excel_row"] for x in srs]
    assert len(rows) == len(set(rows)), "SRS excel_row 重复归属"
    assert sum(r <= 199 for r in rows) == 196 and sum(r >= 246 for r in rows) == 87, "SRS 计数应为 196 + 87"
    for leaf, _, lo, hi, _ in A_LEAVES:
        assert sum(x["leaf"] == leaf for x in srs) == hi - lo + 1, f"{leaf} 行数不符"

    ids = [m["metric_id"] for m in mets]
    assert len(ids) == len(set(ids)), "metric_id 重复归属"
    cnt = {d: sum(m["domain"] == d for m in mets) for d in ("TALENT", "TECH", "ORG")}
    assert cnt == {"TALENT": 32, "TECH": 39, "ORG": 22}, cnt
    types = {(m["domain"], m["algorithm_type"]) for m in mets}
    assert sum(m["algorithm_type"] == "STAT" for m in mets) == 6 and sum(m["algorithm_type"] == "MODEL" for m in mets) == 3, types

    jids = [j["row_id"] for j in jx]
    assert len(jids) == 51 == len(set(jids)), f"久新行 {len(jids)} / 唯一 {len(set(jids))}"
    forms = {f: sum(j["交付形态"] == f for j in jx) for f in ("SQL", "Python", "API")}
    assert forms == {"SQL": 3, "Python": 6, "API": 42}, forms

    baseline = {
        "task_id": "SCI-INT-P00",
        "generated_by": "产物/_work/P00-check.py",
        "note": "对端正名「久新」；久新清单路径保留旧目录名「九新-技术机构人才」。指标类型来自 MCP metric-query 2026-10-18。",
        "counts": {"srs": {"科技发展态势": 196, "科技人才态势": 87, "total": len(srs)},
                   "metrics": {**cnt, "total": len(mets)}, "jiuxin_rows": {**forms, "total": len(jx)}},
        "srs_leaves": srs,
        "metrics": mets,
        "jiuxin_rows": jx,
    }
    (OUT / "P00-baseline.yaml").write_text(yaml.safe_dump(baseline, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    print(f"OK srs={len(srs)} metrics={len(mets)} jiuxin={len(jx)}")


if __name__ == "__main__":
    main()
