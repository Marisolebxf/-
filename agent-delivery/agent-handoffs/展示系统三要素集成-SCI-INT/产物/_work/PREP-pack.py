# SCI-INT 预备材料包：给后续 A / B 叶子出精简输入，减少子智能体重复通读大文件。
# 指标数据来自 MCP metric-srs-export 产物 registry/export/指标需求来源.xlsx（导出件，非 seed/矩阵）。
# 运行：python 产物/_work/PREP-pack.py（任意 cwd）；重跑前先调一次 MCP metric-srs-export 刷新导出件。
import re
import subprocess
import sys
from pathlib import Path

import openpyxl
import yaml

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
PREP = OUT / "_prep"
AD = HERE.parents[3]
GKX = AD.parents[1]
SRS = AD / "bid-reference/srs/02-科技信息展示系统"
XLSX = AD / "metrics/registry/export/指标需求来源.xlsx"
FE = GKX / "repos/lumen-ui-science-pc/src"

sys.path.insert(0, str(HERE))
from importlib import import_module  # noqa: E402

p00 = import_module("P00-check")
BLOCK, field, A_LEAVES = p00.BLOCK, p00.field, p00.A_LEAVES

A_NUM = {f"A{i:02d}": (i - 1) * 100 for i in range(1, 16)}
B_NUM = {f"B{i:02d}": (i - 1) * 100 for i in range(1, 10)}


def dump(path, data):
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    yaml.safe_load(path.read_text(encoding="utf-8"))


def load_xlsx():
    wb = openpyxl.load_workbook(XLSX, read_only=True)

    def rows(name):
        it = wb[name].iter_rows(values_only=True)
        head = next(it)
        return [dict(zip(head, r)) for r in it]

    cat = {r["指标ID"]: r for r in rows("指标目录")}
    detail = [r for r in rows("需求来源明细") if r["分册"] == "02" and r["序号"] is not None]
    return cat, detail


def metric_brief(cat, mid):
    r = cat.get(mid) or {}
    return {"metric_id": mid, "name": r.get("指标名"), "domain": r.get("域"), "algorithm_type": r.get("算法类型") or "UNKNOWN",
            "d1": r.get("D1定义"), "d4": r.get("D4接入"), "decision_ids": r.get("决策清单中的编号"), "definition": r.get("口径摘要")}


def load_products():
    prods = {}
    for f in sorted(OUT.glob("SCI-INT-*.yaml")):
        prods[f.stem.replace("SCI-INT-", "")] = yaml.safe_load(f.read_text(encoding="utf-8"))
    return prods


def card_brief(c):
    ds = c.get("data_source") or {}
    return {k: v for k, v in {
        "int_id": c.get("int_id"), "layer": c.get("layer"), "dimension": c.get("dimension"), "metric_ids": c.get("metric_ids"),
        "algorithm_type": c.get("algorithm_type"), "integration_pattern": c.get("integration_pattern"), "counterpart": c.get("counterpart"),
        "delivery_form": c.get("delivery_form"), "jiuxin_row_id": c.get("jiuxin_row_id"),
        "table": ds.get("table") if isinstance(ds, dict) else None, "srs_row": (c.get("srs") or {}).get("excel_row") if isinstance(c.get("srs"), dict) else None,
        "page_ref": c.get("page_ref"), "java": (c.get("call_chain") or {}).get("java"), "python": (c.get("call_chain") or {}).get("python"),
    }.items() if v not in (None, [], "")}


def global_findings(prods):
    out = []
    for leaf, d in prods.items():
        for key in ("decision_needed", "open_items", "risks", "conflicts"):
            items = d.get(key) or []
            if isinstance(items, dict):
                items = [{"id": k, "item": v} for k, v in items.items()]
            for it in items:
                if isinstance(it, dict):
                    text = it.get("item") or it.get("question") or it.get("desc") or it.get("risk") or it.get("summary") or it.get("title")
                    out.append({"leaf": leaf, "kind": key, "id": it.get("id"), "owner": it.get("owner"), "text": str(text or it)[:300]})
                else:
                    out.append({"leaf": leaf, "kind": key, "text": str(it)[:300]})
    return out


def fe_hits(keyword):
    try:
        res = subprocess.run(["rg", "-l", "--fixed-strings", keyword, str(FE)], capture_output=True, text=True, encoding="utf-8", timeout=60)
        return sorted(str(Path(p).relative_to(GKX)) for p in res.stdout.split())[:40]
    except (OSError, subprocess.SubprocessError):
        return []


def main():
    PREP.mkdir(exist_ok=True)
    base = yaml.safe_load((OUT / "P00-baseline.yaml").read_text(encoding="utf-8"))
    cat, detail = load_xlsx()
    prods = load_products()
    b01 = {m["metric_id"]: m for m in prods["B01"]["initial_mapping"]}
    jx = {j["row_id"]: j for j in base["jiuxin_rows"]}
    p00_metrics = {m["metric_id"]: m for m in base["metrics"]}

    c_cards = [card_brief(c) for k, d in prods.items() if k.startswith("C") for c in d.get("cards") or []]
    a_cards = [card_brief(c) for k, d in prods.items() if k.startswith("A") for c in d.get("cards") or []]
    dump(PREP / "C-index.yaml", {"note": "C01–C04 数据源 / 图谱卡索引（精简）；引用 int_id，不重复造卡。全文见 产物/SCI-INT-C0x.yaml", "cards": c_cards})
    dump(PREP / "global-findings.yaml", {"note": "已完成叶子的待决 / 开放 / 风险 / 冲突汇总；已有的直接引用 id，不重复登记", "items": global_findings(prods)})

    texts = {}
    for leaf, rel, lo, hi, ds in A_LEAVES:
        if (OUT / f"SCI-INT-{leaf}.yaml").exists():
            continue
        text = texts.setdefault(rel, (SRS / rel).read_text(encoding="utf-8"))
        blocks = {int(field(b, "excel_row")): (n.strip(), b.strip()) for n, b in BLOCK.findall(text)}
        srs = []
        for r in base["srs_leaves"]:
            if r["leaf"] != leaf:
                continue
            ms = sorted({d["指标ID"] for d in detail if int(d["序号"]) == r["seq"]})
            srs.append({**r, "srs_text": blocks[r["excel_row"]][1], "metrics": [metric_brief(cat, m) for m in ms]})
        mids = {m["metric_id"] for s in srs for m in s["metrics"]}
        prefix = ds.split("-")[0] + "-" + ds.split("-")[1]
        page_only = sorted(m for m, r in cat.items() if m not in mids and (
            str(r.get("模块") or "").startswith(prefix) or prefix.replace("-", "_") + "_" in m))
        jrows = [j for j in base["jiuxin_rows"] if str(j.get("page_id") or "").startswith(prefix)]
        pack = {
            "leaf": leaf, "file": rel, "excel_rows": [lo, hi], "page_ref": ds,
            "int_id_range": f"INT-A-{{TAL|TECH|ORG|X}}-{A_NUM[leaf]:03d}~{A_NUM[leaf] + 99:03d}",
            "note": "srs_text = SRS 原文块；metrics = 指标需求来源导出件按 分册02+序号 匹配（algorithm_type / D1 / D4 已是 MCP 口径，可直接用，存疑再 metric-get）。",
            "srs": srs,
            "page_metrics_unlinked": [metric_brief(cat, m) for m in page_only],
            "page_metrics_unlinked_note": "模块=页面编号 或 id 含页面编号、但未回填 SRS 序号的候选指标；需自行判断挂到哪个叶",
            "b01_mapping": [b01[m] for m in sorted(mids | set(page_only)) if m in b01],
            "jiuxin_rows_page": jrows,
            "jiuxin_rows_generic_note": "page_id=SRS-TECH/SRS-TALENT/SRS-ORG 的久新通用行见 P00-baseline.yaml jiuxin_rows",
            "fe_files_hit": fe_hits(Path(rel).stem),
        }
        dump(PREP / f"{leaf}-pack.yaml", pack)
        print(f"{leaf}: srs={len(srs)} metrics={len(mids)} unlinked={len(page_only)} jiuxin_page={len(jrows)} fe_hits={len(pack['fe_files_hit'])}")

    for leaf in B_NUM:
        if leaf == "B01" or (OUT / f"SCI-INT-{leaf}.yaml").exists():
            continue
        mids = [m for m, v in p00_metrics.items() if v["leaf"] == leaf]
        ms = set(mids)
        refs = {m: sorted({(d["序号"], d["需规名称"], d["页面"]) for d in detail if d["指标ID"] == m}, key=str) for m in mids}
        pack = {
            "leaf": leaf, "int_id_range": f"INT-B-{{TAL|TECH|ORG|X}}-{B_NUM[leaf]:03d}~{B_NUM[leaf] + 99:03d}",
            "metrics": [{**metric_brief(cat, m), "p00_algorithm_type": p00_metrics[m]["algorithm_type"], "b01": b01.get(m),
                         "jiuxin_row": jx.get((b01.get(m) or {}).get("jiuxin_row_id")),
                         "srs_refs_02": [{"seq": s, "name": n, "page": p} for s, n, p in refs[m]]} for m in mids],
            "c_cards": [c for c in c_cards if ms & set(c.get("metric_ids") or [])],
            "a_cards": [c for c in a_cards if ms & set(c.get("metric_ids") or [])],
            "b01_patterns": "见 产物/SCI-INT-B01.yaml patterns（IP-01…IP-13 全文）",
        }
        dump(PREP / f"{leaf}-pack.yaml", pack)
        print(f"{leaf}: metrics={len(mids)} c_cards={len(pack['c_cards'])} a_cards={len(pack['a_cards'])}")

    # 自检：A06（已完成）序号 → 指标匹配必须命中其卡上的 INNOV 指标，证明 分册02+序号 对得上
    a06 = [r for r in base["srs_leaves"] if r["excel_row"] == 76][0]
    hit = {d["指标ID"] for d in detail if int(d["序号"]) == a06["seq"]}
    assert "M_INNOV_DS_04_CARRIER_RANK_001" in hit, f"序号匹配失效：seq={a06['seq']} hit={hit}"
    print(f"OK c_index={len(c_cards)} findings={len(global_findings(prods))}")


if __name__ == "__main__":
    main()
