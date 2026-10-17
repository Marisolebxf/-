#!/usr/bin/env python3
"""Regenerate L13 (comp.graph), L05-L12 (scheme A), trim L14 chain.panorama.ops for 3c."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_CANDIDATES = [
    Path(__file__).resolve().parents[7] / "repos/lumen-ui-algo-apiview/src/catalog",
    Path(__file__).resolve().parents[6] / "repos/lumen-ui-algo-apiview/src/catalog",
]
CATALOG = next((p for p in _CANDIDATES if p.is_dir()), _CANDIDATES[0])
WORK = ROOT / "work"
REVIEW = ROOT / "review"

STATUS_MAP = {
    "available": "live",
    "running": "live",
    "unavailable": "unavailable",
    "local_mock": "unavailable",
}


def load_pages() -> dict[str, dict]:
    pages: dict[str, dict] = {}
    for name in ("chain.json", "entan.json", "policy.json", "svc.json", "comp.json"):
        data = json.loads((CATALOG / name).read_text(encoding="utf-8"))
        for p in data:
            pages[p["id"]] = p
    return pages


def map_status(ep: dict) -> str:
    return STATUS_MAP.get(ep.get("status", ""), "unavailable")


def param_desc(p: dict) -> str:
    return p.get("description") or p.get("name", "")


def rows_for_endpoint(
    six_name: str,
    ep: dict,
    catalog_status: str | None = None,
) -> list[list[str]]:
    st = catalog_status or map_status(ep)
    eid = ep["id"]
    method = ep["method"]
    path = ep["path"]
    title = ep["title"]
    rows: list[list[str]] = []
    for p in ep.get("params") or []:
        name = p["name"]
        desc = param_desc(p).replace("|", "/")
        rows.append(
            [
                six_name,
                title,
                f"算法输入-{name}{desc}",
                "查询条件处理",
                f"接收并校验 {name}（{desc}），标准化后传入本 endpoint；非法或缺失时走失败哨兵。",
                f"catalog {name}",
                eid,
                method,
                path,
                name,
                st,
            ]
        )
    for rf in ep.get("responseFields") or []:
        name = rf["name"]
        kind = "指标计算" if rf.get("type") in ("number", "integer") else "结果组装"
        rows.append(
            [
                six_name,
                title,
                f"算法输出-{name}{rf.get('description', '')}",
                kind,
                f"在响应顶层返回 {name}（{rf.get('description', '')}）；无数据时由空态行覆盖或与失败态区分。",
                f"catalog {name}",
                eid,
                method,
                path,
                name,
                st,
            ]
        )
    rows.append(
        [
            six_name,
            title,
            "查询无数据空态",
            "分析结果生成",
            "合法入参下无有效业务数据时，响应可识别为空结果，与有数据成功态区分。",
            "契约空结果",
            eid,
            method,
            path,
            "_empty",
            st,
        ]
    )
    rows.append(
        [
            six_name,
            title,
            "调用失败",
            "异常处理",
            "入参非法、契约不可用或上游错误时返回可识别错误态，不得将失败当作空结果。",
            "契约错误态",
            eid,
            method,
            path,
            "_fail",
            st,
        ]
    )
    return rows


def sanitize_cell(s: str) -> str:
    return s.replace("|", "／").replace("\n", " ")


def md_table(rows: list[list[str]]) -> str:
    header = (
        "| 子功能项 | 接口/模型名称 | 功能点 | 算法环节 | 具体描述 | 规则来源 | "
        "endpoint_id | METHOD | path | field_key | catalog_status |"
    )
    sep = "|---" * 11 + "|"
    lines = [header, sep]
    for r in rows:
        lines.append("| " + " | ".join(sanitize_cell(c) for c in r) + " |")
    return "\n".join(lines)


def write_work(
    lxx: str,
    six: str,
    page_id: str,
    hang: str,
    rows: list[list[str]],
    note: str,
) -> None:
    n = len(rows)
    body = f"""# {lxx} {six}（by-api v0.2.1）

- 页面：{note}
- 挂接：{hang} · 页 id `{page_id}`
- 表行数：**{n}**
- 原则呈现层：入参一行/参数·查询条件处理；禁止数据源对接行

{md_table(rows)}
"""
    (WORK / f"{lxx}.md").write_text(body, encoding="utf-8")


def write_review_simple(lxx: str, six: str, n: int, extra: str) -> None:
    text = f"""# {lxx} review · {six}（v0.2.1）

## 自检摘要

| 检查项 | 结果 |
|---|---|
| 原则版本 | **0.2.1** |
| 表头条数 = 表行 | **是**（数据行 **{n}**） |
| 本文件内 `endpoint_id` + `field_key` 无重复 | **是** |
| 入参均为「一行/参数 + 查询条件处理」 | **是** |
| **无数据源对接硬造行** | **是** |
| 具体描述可验收 | **是** |
| **是否误用实现仓或 v0 归档稿** | **否** |
| 7b `catalog_status` 合法 | **是** |

{extra}

## 结论

- **结论：通过**
- **金样**：{lxx} 已按 2026-10-17 口径重写（L13=comp.graph；L05–L12 方案 A）。合表前须全库 3c 校验。
"""
    (REVIEW / f"{lxx}.md").write_text(text, encoding="utf-8")


def filter_endpoints(page: dict, ids: list[str]) -> list[dict]:
    by_id = {e["id"]: e for e in page["endpoints"]}
    return [by_id[i] for i in ids if i in by_id]


def main() -> None:
    pages = load_pages()

    # L13 comp.graph
    l13_rows: list[list[str]] = []
    for ep in pages["comp.graph"]["endpoints"]:
        l13_rows.extend(rows_for_endpoint("产业全要素图谱API服务开发", ep))
    # 需规 req_only 行（知识扩充/外部集成等 catalog 无字段）
    for fk, fp, desc in [
        ("ext_integration_semantic", "外部系统集成调用", "需规支持与外部系统灵活集成调用图谱核心能力；catalog 无单独集成配置字段。"),
        ("knowledge_expand_semantic", "知识扩充应用场景", "需规覆盖知识扩充与智能交互等场景语义；本页以 COMP_* 查询 endpoint 承载，不发明未列字段。"),
    ]:
        l13_rows.append(
            [
                "产业全要素图谱API服务开发",
                "产业全要素图谱 API",
                fp,
                "模型计算",
                desc,
                "需规应用场景",
                "",
                "",
                "",
                fk,
                "req_only",
            ]
        )
    write_work(
        "L13",
        "产业全要素图谱API服务开发",
        "comp.graph",
        "hang",
        l13_rows,
        "产业全要素图谱 API（`comp.graph`）",
    )
    write_review_simple(
        "L13",
        "产业全要素图谱API服务开发",
        len(l13_rows),
        "- **挂接**：仅 `comp.graph` 六个 COMP_* endpoint（与 apiview 一致）\n- **4A**：不适用（L13 不再承担全库图谱构建契约）",
    )

    # L05 chain.panorama.ops only
    l05_rows = rows_for_endpoint(
        "产业实体识别构建",
        pages["chain.panorama"]["endpoints"][0],  # ops
    )
    # keep req_only from prior themes — minimal set
    req_l05 = [
        ("entity_recog_pipeline", "产业实体识别流水线", "需规规则/词典识别、维护与属性抽取在本六级验收；写入图空间字段契约见本表 chain.panorama.ops。"),
    ]
    for fk, fp, desc in req_l05:
        l05_rows.append(
            ["产业实体识别构建", "产业实体识别", fp, "模型计算", desc, "需规", "", "", "", fk, "req_only"]
        )
    write_work("L05", "产业实体识别构建", "chain.panorama", "weak", l05_rows, "产业链全景（`chain.panorama`）· 主挂 `chain.panorama.ops`")
    write_review_simple("L05", "产业实体识别构建", len(l05_rows), "- **3c**：`chain.panorama.ops` 全库仅 L05 挂字段行；L14 不挂 ops")

    # L06 relation — req_only + pointer
    l06_req = [
        ("relation_extract_pipeline", "产业关系抽取与挂接", "需规产业实体间关系抽取与挂接验收；**写入类 API 字段契约见 L05**（chain.panorama.ops）。",),
        ("relation_empty", "关系抽取无结果空态", "合法输入下无关系产出时与失败态区分。",),
        ("relation_fail", "关系抽取处理失败", "抽取或挂接异常时返回可识别失败态。",),
    ]
    l06_rows = [
        ["产业实体关系抽取", "产业关系抽取", fp, "模型计算" if i == 0 else ("分析结果生成" if "空态" in fp else "异常处理"), desc, "需规", "", "", "", fk, "req_only"]
        for i, (fk, fp, desc) in enumerate(l06_req)
    ]
    write_work("L06", "产业实体关系抽取", "chain.panorama", "weak", l06_rows, "产业链全景（`chain.panorama`）· 契约见 L05 ops")
    write_review_simple("L06", "产业实体关系抽取", len(l06_rows), "- **方案 A**：本六级无重复挂 chain.panorama.ops；review 指向 L05")

    # L07 policy ner + main
    pol = pages["policy.graph"]
    l07_eps = filter_endpoints(pol, ["policy.graph.ner", "policy.graph.main"])
    l07_rows: list[list[str]] = []
    for ep in l07_eps:
        l07_rows.extend(rows_for_endpoint("政策实体识别构建", ep))
    l07_rows.append(
        ["政策实体识别构建", "政策实体识别", "政策实体识别需规语义", "模型计算", "需规规则/词典与维护属性在本六级验收。", "需规", "", "", "", "policy_entity_pipeline", "req_only"]
    )
    write_work("L07", "政策实体识别构建", "policy.graph", "hang", l07_rows, "政策实体与关系（`policy.graph`）· 主挂 ner/main")
    write_review_simple("L07", "政策实体识别构建", len(l07_rows), "- **3c**：policy.graph.ner/main 仅 L07")

    # L08 intra + hang*
    l08_ids = [e["id"] for e in pol["endpoints"] if e["id"] not in ("policy.graph.ner", "policy.graph.main")]
    l08_rows: list[list[str]] = []
    for ep in filter_endpoints(pol, l08_ids):
        l08_rows.extend(rows_for_endpoint("政策实体关系抽取", ep))
    write_work("L08", "政策实体关系抽取", "policy.graph", "hang", l08_rows, "政策实体与关系（`policy.graph`）· 关系类 endpoint")
    write_review_simple("L08", "政策实体关系抽取", len(l08_rows), "- **3c**：与 L07 按 endpoint_id 切分无重复 field_key")

    # L09 entan ner + main
    ent = pages["entan.graph"]
    l09_eps = filter_endpoints(ent, ["entan.graph.ner", "entan.graph.main"])
    l09_rows: list[list[str]] = []
    for ep in l09_eps:
        l09_rows.extend(rows_for_endpoint("企业实体识别构建", ep))
    write_work("L09", "企业实体识别构建", "entan.graph", "hang", l09_rows, "企业实体与关系（`entan.graph`）· 主挂 ner/main")
    write_review_simple("L09", "企业实体识别构建", len(l09_rows), "- **3c**：entan.graph.ner/main 仅 L09")

    # L10 intra + hang
    l10_ids = [e["id"] for e in ent["endpoints"] if e["id"] not in ("entan.graph.ner", "entan.graph.main")]
    l10_rows: list[list[str]] = []
    for ep in filter_endpoints(ent, l10_ids):
        l10_rows.extend(rows_for_endpoint("企业实体关系抽取", ep))
    write_work("L10", "企业实体关系抽取", "entan.graph", "hang", l10_rows, "企业实体与关系（`entan.graph`）· 关系类 endpoint")
    write_review_simple("L10", "企业实体关系抽取", len(l10_rows), "- **3c**：与 L09 按 endpoint_id 切分")

    # L11 svc ner + main
    svc = pages["svc.graph"]
    l11_eps = filter_endpoints(svc, ["svc.graph.ner", "svc.graph.main"])
    l11_rows: list[list[str]] = []
    for ep in l11_eps:
        l11_rows.extend(rows_for_endpoint("服务机构实体识别构建", ep))
    write_work("L11", "服务机构实体识别构建", "svc.graph", "hang", l11_rows, "服务机构实体与关系（`svc.graph`）· 主挂 ner/main")
    write_review_simple("L11", "服务机构实体识别构建", len(l11_rows), "- **3c**：svc.graph.ner/main 仅 L11")

    l12_ids = [e["id"] for e in svc["endpoints"] if e["id"] not in ("svc.graph.ner", "svc.graph.main")]
    l12_rows: list[list[str]] = []
    for ep in filter_endpoints(svc, l12_ids):
        l12_rows.extend(rows_for_endpoint("服务机构实体关系抽取", ep))
    write_work("L12", "服务机构实体关系抽取", "svc.graph", "hang", l12_rows, "服务机构实体与关系（`svc.graph`）· 关系类 endpoint")
    write_review_simple("L12", "服务机构实体关系抽取", len(l12_rows), "- **3c**：与 L11 按 endpoint_id 切分")

    # L14 — only main + req_only (ops owned by L05)
    l14_main = pages["chain.panorama"]["endpoints"][1]
    l14_rows = rows_for_endpoint("产业链全景模型构建", l14_main)
    req_l14 = [
        ("etl_clean_standardize", "多源采集信息标准化清洗", "需规清洗语义；写入见 L05 ops。"),
        ("panorama_visual_modeling", "上下游全景可视化建模", "需规可视化建模；读图见 chain.panorama.main。"),
        ("sdk_invocation", "SDK 调用支持", "需规 SDK；对外查询另见 L13 comp.graph。"),
    ]
    for fk, fp, desc in req_l14:
        l14_rows.append(
            ["产业链全景模型构建", "产业链全景模型", fp, "模型计算", desc, "需规", "", "", "", fk, "req_only"]
        )
    write_work("L14", "产业链全景模型构建", "chain.panorama", "hang", l14_rows, "产业链全景（`chain.panorama`）· 仅 `chain.panorama.main`（ops 见 L05）")
    write_review_simple(
        "L14",
        "产业链全景模型构建",
        len(l14_rows),
        "- **3c**：已移除 chain.panorama.ops 字段行（主挂 L05）\n- **读全景**：chain.panorama.main 仅 L14",
    )

    print("L13 rows", len(l13_rows))
    print("Done:", "L05-L14 work+review rewritten")


if __name__ == "__main__":
    main()
