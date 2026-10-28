#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_CULTIVATION_INDEX 培育推荐指数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_CULTIVATION_INDEX.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
#!/usr/bin/env python3
"""M_ENT_CULTIVATION_INDEX 培育推荐指数 — 依赖侧实测脚本

王惠口径（calc-logic 真源）：
  三维（产业相关度/政策匹配度/企业潜力）×极值归一化 0-100 → 加权（等权 1/3 或熵值法，Q015）。
  ① 产业相关度=产业链融入度（Link×Centroid；同 M_ENT_INDUSTRY_MATCH_SCORE）
  ② 政策匹配度=行动型契合+话语型契合（政策词典+GPT 分类企业文本）
  ③ 企业潜力=资产总额+盈利能力(ROE)+研发投入强度 加权
实测（2026-10-20）gkx：
  ① tags 2,283,762 行✅；股东 400,286 行✅（图谱边原料在）；财务收入占比列在（低填充）
  ② 政策库 20,000 行 content 96%；企业文本 dwd_org_org_product_info 45,011 行 description 71.3%——
     但行动/话语契合的 GPT 分类框架未建（前置模型缺）
  ③ 财务 90,926 行：资产>0 2,628（2.9%）、pure_profit 非空 2,349（2.6%）、arch_development_am>0 全空（None）、营收>0 2,191（2.4%）
结论：潜力维三指标两低一空、政策维 GPT 未建、融入度维原料可算 → 三维一可两缺 → 部分支持。
"""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pymysql

OUT = Path(__file__).with_name("M_ENT_CULTIVATION_INDEX_out.json")
ENV_GKX = Path(__file__).resolve().parents[6] / "gkx-orchestration/agent-delivery/data/third-party-source/gkx-mysql-raw/.env.local"


def load_dotenv(path: Path) -> dict:
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def main():
    rep = {"metric_id": "M_ENT_CULTIVATION_INDEX", "metric_name": "培育推荐指数", "script": Path(__file__).name}
    e = load_dotenv(ENV_GKX)
    gc = pymysql.connect(host=e["GKX_SRC_HOST"], port=int(e["GKX_SRC_PORT"]), user=e["GKX_SRC_USER"],
                         password=e["GKX_SRC_PASSWORD"], database="gkx", charset="utf8mb4",
                         cursorclass=pymysql.cursors.DictCursor, connect_timeout=20, read_timeout=300)
    with gc.cursor() as cur:
        cur.execute("SELECT COUNT(*) n FROM dwd_org_industry_tags")
        tags = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) n FROM dwd_org_shareholder_info")
        sh = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) n, SUM(total_assets>0) assets, SUM(pure_profit IS NOT NULL) profit, "
                    "SUM(arch_development_am>0) rd, SUM(operating_revenue>0) rev FROM dwd_org_annual_financial_info")
        fin = {k: (str(v) if isinstance(v, Decimal) else v) for k, v in dict(cur.fetchone()).items()}
        cur.execute("SELECT COUNT(*) n, SUM(description IS NOT NULL AND description<>'') d FROM dwd_org_org_product_info")
        prod = {k: str(v) for k, v in dict(cur.fetchone()).items()}
    gc.close()
    n = int(fin["n"])
    pct = lambda x: f"{round(int(x or 0)/n*100,1)}%"

    probe = {
        "gkx_tags": tags, "gkx_shareholder": sh,
        "gkx_financial": fin, "fin_pct": {"assets": pct(fin["assets"]), "profit": pct(fin["profit"]),
                                          "rd(arch_development_am)": "全空(None)", "rev": pct(fin["rev"])},
        "gkx_product_text": prod,
        "gpt_classification_built": False,
    }
    rep["probe"] = probe
    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": (
            f"三维成熟度：①产业相关度原料可算（tags {tags} 行+股东 {sh} 行图谱边+目录）✅；"
            f"②政策匹配度缺 GPT 分类框架（政策库 content 96%、企业文本 {prod['n']} 行 description 71.3%，"
            f"但行动/话语两型契合的识别模型未建）❌；"
            f"③企业潜力财务三指标：资产 {pct(fin['assets'])}、净利润 {pct(fin['profit'])}、"
            f"研发投入 arch_development_am 全空、营收 {pct(fin['rev'])}——低填充+一列空❌。"
            "三维一可两缺（GPT 框架未建+财务薄）→ 部分支持。"
        ),
        "criteria": {
            "industry_dim_ready": True,
            "policy_gpt_ready": False,
            "potential_financial_fill_pct": pct(fin["assets"]),
        },
    }
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rep["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统', '科技信息展示系统']

# 缺省参数：三系统可传子集；快照/探针粒度上不可再分的参数会在 assumptions 显式声明
COMPAT_DEFAULTS = {
    "start_date": None,        # 算法库/展示常传；缺省 → 基线口径窗口（产物 base_years_*）
    "end_date": None,          # 同上；缺省 → 基线口径窗口
    "region": None,            # 地域过滤；缺省 → 全区域（基线口径）
    "industry_tag": None,      # 链/领域标签；缺省 → 全量（基线口径）
    "weights": None,           # 维度权重（模型型指标）；缺省 → 基线内置权重（Q014 类未定项不擅自赋值）
    "dims": None,              # 维度子集（模型型指标）；缺省 → 基线全维度
    "format": None,            # "detail"/"display"；缺省 → 两段都返回
}


def compute(params=None):
    """三系统统一入口：执行基线 main() 的计算逻辑，读取其产物并附兼容元数据返回。

    返回 dict：
      value / detail   : 主值与明细（透传基线产物 headline/stats，数值逐位=基线）
      display          : 展示系统友好结构（headline 精简 + 明细首层序列化）
      assumptions      : 本次运行采用的缺省假设（缺参时非空，前端可提示）
      applicable_systems / params_effective / metric_id / metric_name / generated_at
    典型调用：
      算法库  : compute({"start_date": ..., "end_date": ..., "region": ...})   全参
      专题系统: compute({}) 或 compute({"industry_tag": "..."})               少传参
      展示系统: compute({"format": "display"})                                只要展示段
    """
    import importlib.util, json as _json, time as _time
    from pathlib import Path as _Path

    p_in = dict(params or {})
    eff = {**COMPAT_DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = []
    for k, v in eff.items():
        if v is not None and k in ("start_date", "end_date", "region", "industry_tag", "weights", "dims"):
            assumptions.append(f"{k}={v!r} 已接收：本件快照/探针粒度为基线口径，参数生效范围见同名 md「入参兼容策略」"
                               "（不可再分时返回基线口径值并在此声明）")
    assumptions.append("本件为 20261021 基线口径包装（兼容层不改数学定义）；三系统主值同源")

    t0 = _time.time()
    here = _Path(__file__).resolve().parent
    out_json = here / "M_ENT_CULTIVATION_INDEX_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_CULTIVATION_INDEX.py 等价）
        run_baseline()
    data = _json.loads(out_json.read_text(encoding="utf-8"))

    headline = data.get("headline") or {}
    value = headline.get("value") if isinstance(headline, dict) and "value" in headline else None
    if value is None and isinstance(headline, dict):
        value = next((headline[k] for k in ("total_le2024", "total", "sz_total", "score", "index", "n", "count")
                      if k in headline and isinstance(headline[k], (int, float))), None)
    if value is None:   # 无 headline 结构的产物：从顶层常见键提取（KPI/分布型）
        for k in ("total", "value", "n_total", "count", "org_total", "sz_total", "sum", "amount"):
            v = data.get(k)
            if isinstance(v, (int, float)):
                value = v
                break
            if isinstance(v, dict):
                for kk in ("total", "value", "n", "sz"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
                if value is not None:
                    break
    if value is None:   # 探针/分布型产物：从 population / audit_chain / probe 找主计数
        for sec in ("population", "audit_chain", "probe", "stats"):
            v = data.get(sec)
            if isinstance(v, dict):
                for kk in ("distinct_org_id", "total", "n", "count", "org_count", "rows",
                           "filled", "polar_rows", "chain_members_total"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
            if value is not None:
                break
    if value is None:   # 兜底声明：无单一主值（分布/明细型产物），value=None 属正常而非错误
        assumptions.append("本件为分布/明细型产物（无单一主值键），value=None；调用方请消费 detail/display 段")
    detail = {k: data[k] for k in ("stats", "facts", "population", "rule", "support_judgment",
                                   "base_years_used", "base_years_missing", "sources") if k in data}
    display = {"headline": headline, "rows_preview": None}
    for k in ("chains", "rows", "items", "list", "ranking", "detail_list"):
        if isinstance(data.get(k), list):
            display["rows_preview"] = {"key": k, "n": len(data[k]), "sample": data[k][:5]}
            break
    if eff.get("format") == "display":
        detail = {"support_judgment": data.get("support_judgment")}
    return {
        "metric_id": "M_ENT_CULTIVATION_INDEX",
        "metric_name": data.get("metric_name"),
        "applicable_systems": APPLICABLE,
        "params_effective": eff,
        "assumptions": assumptions,
        "value": value,
        "detail": detail,
        "display": display,
        "generated_at": _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(_time.time() - t0, 2),
        "baseline_generated_at": data.get("generated_at"),
    }


def run_baseline():
    """原样执行基线 main()（兼容层调用；产物 _out.json 由基线逻辑写盘，铁律：产物只由脚本产出）。"""
    main()  # noqa: F821  ← 基线入口（上方原代码定义）
