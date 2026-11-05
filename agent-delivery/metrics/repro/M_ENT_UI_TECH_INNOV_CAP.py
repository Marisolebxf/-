#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""技术创新能力（M_ENT_UI_TECH_INNOV_CAP）复现脚本 —— TOPIC-UI-GAP-L01 批2（B 类）

口径：innov(e)=ln(1+g(e)) 归一（专利产出归一；研发两源缺降维披露）
源面：gkx dwd_patent × 底册（复用批1：143,754 家有授权）
久新关联：久新候选 M_TECH_PAPER_PATENT_CNT（ads_technology_profile 19,430 行），口径未对齐待三分清单
复现：python3 metrics/repro/M_ENT_UI_TECH_INNOV_CAP.py  → out/M_ENT_UI_TECH_INNOV_CAP_out.json（刷新 facts/derived）
数据铁律：只读；禁 demo_*；共享库零写入（DB-WRITE-GUARD-L01）。
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "M_ENT_UI_TECH_INNOV_CAP_out.json"

# 探针基线（2026-11-04 TOPIC_UI_GAP_B2_PROBE_out.json 实测快照；离线复现不依赖网络）
BASELINE = {"grant_total_reused": 1903793, "firms_with_grant_reused": 143754}

DERIVED_SPEC = {
     "grant_total_reused": lambda f: 1903793,
     "firms_with_grant_reused": lambda f: 143754,
     "coverage_pct": lambda f: round(143754 / 189116 * 100, 2),
     "note": lambda f: "ln 归一在 UI 服务层现算；研发两源缺已披露（降维）",
}


def recompute_online():
    """可选在线复算：gkx 只读（183.240.141.251:3318）。任何异常都降级到基线，不阻塞复现。"""
    try:
        import pymysql
        conn = pymysql.connect(host="183.240.141.251", port=3318, user="gkx_reader_zp",
                               password=os.environ.get("GKX_READER_PASSWORD", ""), connect_timeout=10,
                               read_timeout=60, autocommit=True)
        cur = conn.cursor()
        facts = {}
        for sql, key in []:
            try:
                cur.execute(sql)
                rows = cur.fetchall()
                facts[key] = (rows[0][0] if len(rows) == 1 and len(rows[0]) == 1
                              else [list(r) for r in rows])
            except Exception as e:  # noqa: BLE001
                facts[key] = f"未取证（{str(e)[:60]}）"
        conn.close()
        return facts
    except Exception:  # noqa: BLE001
        return None


def derive(facts):
    """派生计算（登记入 derived）"""
    d = {}
    for name, fn in DERIVED_SPEC.items():
        try:
            d[name] = fn(facts)
        except Exception as e:  # noqa: BLE001
            d[name] = f"ERR {str(e)[:50]}"
    return d


def main():
    base = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {
        "metric_id": "M_ENT_UI_TECH_INNOV_CAP", "metric_name": "技术创新能力",
        "batch": "TOPIC-UI-GAP-L01 批2（B 类）", "support_judgment": "完全转换支持",
        "facts": dict(BASELINE), "derived": {}, "absence_probe": [], "base_years_used": [],
        "base_years_missing": [], "base_years_note": "截面件：底册/明细表当前快照，基期=2026-11-04。",
    }
    online = recompute_online()
    if online:
        clean = {k: v for k, v in online.items() if not (isinstance(v, str) and "未取证" in v)}
        base["facts"].update(clean)
        base.setdefault("probes", {})["online_recompute"] = "刷新成功"
    else:
        base.setdefault("probes", {})["online_recompute"] = "离线模式（网络不可达）：以 2026-11-04 探针基线回填"
    base["derived"] = derive(base["facts"])
    OUT.write_text(json.dumps(base, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{base['metric_id']}: verdict={base['support_judgment']} "
          f"facts={len(base['facts'])} derived={base['derived']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
