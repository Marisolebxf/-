# ALGO-LIB-T0X-L01 · 会前清单（F−L 77 未分拣 + L−F 未分拣）
# 禁止预填四桶。会后才写处置桶。
from __future__ import annotations

from pathlib import Path

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[3]
REQ = ROOT / "metrics" / "request"
ALGO = ROOT / "metrics" / "algo-results"
OUT = REQ / "T0X"

BUCKET = "未分拣"
ALSO_IN_SKIP = "also_in: E7-POLICY"


def load(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_main_missing(item: dict, system: str) -> bool:
    if item.get("差集判定") != "missing":
        return False
    if system == "display":
        note = item.get("缺口说明") or ""
        if ALSO_IN_SKIP in note:
            return False
    return True


def flatten_fl(items: list, system: str, system_zh: str) -> list[dict]:
    rows = []
    for it in items:
        if not is_main_missing(it, system):
            continue
        rows.append(
            {
                "合同集合": "F−L",
                "系统": system_zh,
                "模块": it.get("模块"),
                "page_id": it.get("page_id"),
                "row_id": it.get("row_id"),
                "主项": it.get("主项"),
                "子项": it.get("子项"),
                "metric_id": it.get("metric_id"),
                "A1需规ID": it.get("A1需规ID"),
                "缺口说明": (it.get("缺口说明") or "").strip(),
                "处置桶": BUCKET,
                "会中备注": "",
            }
        )
    return rows


def used_req_ids(items: list, verdict: str) -> set[str]:
    out = set()
    for it in items:
        if it.get("差集判定") != verdict:
            continue
        rid = it.get("A1需规ID")
        if rid:
            out.add(str(rid))
    return out


def main() -> None:
    topic = load(REQ / "专题系统" / "TOPIC-ALGO-GAP-L02.yaml")
    display = load(REQ / "展示系统" / "DS-ALGO-GAP-L02.yaml")
    a1 = load(ALGO / "ALGO-LIB-METRIC-DEPS-L01-requirements.yaml")

    fl = flatten_fl(topic["items"], "topic", "专题") + flatten_fl(
        display["items"], "display", "展示"
    )
    n_topic = sum(1 for r in fl if r["系统"] == "专题")
    n_ds = sum(1 for r in fl if r["系统"] == "展示")
    if n_topic != 7 or n_ds != 70 or len(fl) != 77:
        raise SystemExit(f"F−L 计数不对：专题 {n_topic} 展示 {n_ds} 合计 {len(fl)}（期望 7+70=77）")

    mapped_ids = used_req_ids(topic["items"], "mapped") | used_req_ids(display["items"], "mapped")
    tp_ids = used_req_ids(topic["items"], "third_party") | used_req_ids(
        display["items"], "third_party"
    )

    lf = []
    for req in a1["requirements"]:
        rid = req["requirement_id"]
        in_mapped = rid in mapped_ids
        in_tp = rid in tp_ids
        if in_mapped:
            continue
        lf.append(
            {
                "合同集合": "L−F",
                "requirement_id": rid,
                "seq": req.get("seq"),
                "dimension": req.get("dimension"),
                "layer": req.get("layer"),
                "requirement_title": req.get("requirement_title"),
                "仅third_party消费": "是" if in_tp else "否",
                "处置桶": BUCKET,
                "会中备注": "",
            }
        )

    n_a1 = len(a1["requirements"])
    if n_a1 != 97:
        raise SystemExit(f"A1 表1 叶数 {n_a1} ≠ 97")

    n_mapped_topic = sum(1 for it in topic["items"] if it.get("差集判定") == "mapped")
    n_mapped_ds = sum(1 for it in display["items"] if it.get("差集判定") == "mapped")

    payload = {
        "version": 1,
        "task": "ALGO-LIB-T0X-L01",
        "updated": "2026-08-24",
        "bucket_rule": "会前全部未分拣；禁止预填 ①STAT ②已有模型 ③新MODEL ④DEMO",
        "counts": {
            "F交L_mapped_专题": n_mapped_topic,
            "F交L_mapped_展示": n_mapped_ds,
            "F减L_missing_专题": n_topic,
            "F减L_missing_展示": n_ds,
            "F减L_合计": len(fl),
            "A1叶": n_a1,
            "A1被mapped消费叶": len(mapped_ids),
            "L减F_未mapped消费": len(lf),
            "L减F_其中仅third_party": sum(1 for r in lf if r["仅third_party消费"] == "是"),
        },
        "f_minus_l": fl,
        "l_minus_f": lf,
        "jiuxin_note": "JIUXIN 51 条待确认不进本表；禁止会中把 third_party 派成桶③新 MODEL",
    }

    OUT.mkdir(parents=True, exist_ok=True)
    yaml_path = OUT / "ALGO-LIB-T0X-L01-pre-meeting.yaml"
    with yaml_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(payload, f, allow_unicode=True, sort_keys=False)

    md = []
    md.append("# ALGO-LIB-T0X-L01 · 会前清单")
    md.append("")
    md.append("> 任务：`ALGO-LIB-T0X-L01` · 日期：2026-08-24")
    md.append("> **处置桶全部 = 未分拣**。禁止会前预填四桶。")
    md.append("")
    md.append("## 计数")
    md.append("")
    md.append("| 口径 | 条数 |")
    md.append("|------|------|")
    md.append(f"| F∩L · 专题 mapped | **{n_mapped_topic}** |")
    md.append(f"| F∩L · 展示 mapped | **{n_mapped_ds}** |")
    md.append(f"| F−L · 专题 missing | **{n_topic}** |")
    md.append(f"| F−L · 展示 missing | **{n_ds}** |")
    md.append(f"| F−L 合计（本会主清单） | **{len(fl)}** |")
    md.append(f"| A1 库叶 | {n_a1} |")
    md.append(f"| 其中已被 mapped 消费 | {len(mapped_ids)} |")
    md.append(f"| L−F（库叶未被 mapped 消费） | **{len(lf)}** |")
    md.append(
        f"| 上表中仅 third_party 消费 | {sum(1 for r in lf if r['仅third_party消费'] == '是')} |"
    )
    md.append("")
    md.append("九新 51 条待确认 **不进** 本表。禁止把 third_party 派成桶③。")
    md.append("")
    md.append("## F−L（77，未分拣）")
    md.append("")
    md.append("| # | 系统 | 模块 | page_id | row_id | 主项 | metric_id | 处置桶 |")
    md.append("|---|------|------|---------|--------|------|-----------|--------|")
    for i, r in enumerate(fl, 1):
        mid = r["metric_id"] or "（无正式 ID）"
        md.append(
            f"| {i} | {r['系统']} | {r['模块']} | `{r['page_id']}` | `{r['row_id']}` | {r['主项']} | `{mid}` | {BUCKET} |"
        )
    md.append("")
    md.append("## L−F（未被 mapped 消费的库叶，未分拣）")
    md.append("")
    md.append("| # | requirement_id | seq | 维 | 层 | 库叶 | 仅third_party | 处置桶 |")
    md.append("|---|----------------|-----|----|----|------|---------------|--------|")
    for i, r in enumerate(lf, 1):
        md.append(
            f"| {i} | `{r['requirement_id']}` | {r['seq']} | {r['dimension']} | {r['layer']} | {r['requirement_title']} | {r['仅third_party消费']} | {BUCKET} |"
        )
    md.append("")
    (OUT / "ALGO-LIB-T0X-L01-pre-meeting.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    wb = Workbook()
    ws = wb.active
    ws.title = "F减L-missing"
    headers = [
        "合同集合",
        "系统",
        "模块",
        "page_id",
        "row_id",
        "主项",
        "子项",
        "metric_id",
        "A1需规ID",
        "缺口说明",
        "处置桶",
        "会中备注",
    ]
    ws.append(headers)
    for r in fl:
        ws.append([r[h] for h in headers])
    ws2 = wb.create_sheet("L减F-库叶")
    h2 = [
        "合同集合",
        "requirement_id",
        "seq",
        "dimension",
        "layer",
        "requirement_title",
        "仅third_party消费",
        "处置桶",
        "会中备注",
    ]
    ws2.append(h2)
    for r in lf:
        ws2.append([r[h] for h in h2])
    ws3 = wb.create_sheet("计数")
    ws3.append(["口径", "条数"])
    for k, v in payload["counts"].items():
        ws3.append([k, v])
    ws3.append(["处置桶", BUCKET])
    ws3.append(["九新", "51 待确认不进本表"])
    header_fill = PatternFill("solid", fgColor="165DFF")
    header_font = Font(color="FFFFFF", bold=True)
    for sheet in (ws, ws2, ws3):
        for cell in sheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(wrap_text=True)
        for col in sheet.columns:
            letter = get_column_letter(col[0].column)
            sheet.column_dimensions[letter].width = 18
    xlsx_path = OUT / "ALGO-LIB-T0X-L01-pre-meeting.xlsx"
    wb.save(xlsx_path)
    print(f"F-L={len(fl)} L-F={len(lf)} -> {OUT}")


if __name__ == "__main__":
    main()
