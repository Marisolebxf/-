#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_SZ_STATUS —— 深圳人才地位对标（SRS 88/89）。

口径：主档面板 20,420 人（dwd_scholar × 中文论文 × 合著度）。
  深圳组 = is_sz_org（机构名含「深圳」或 loc2=深圳市，236 人）——面板的 city 字段是旧 loc()
  前缀匹配的产物，会把「哈尔滨工业大学(深圳)」判回哈尔滨（实测 23 人），必须用 is_sz_org 修正；
  对照组 = 其余有属地者（不含未归属，避免把「判不出」当外地）；
  另给「窄口径」city==深圳市（213 人）只作敏感性对照。
质量维：h-index、总被引、论文数、h≥50、被引≥1 万、ORCID 覆盖率；结构维：机构/集群。
零 SQL；产物 code/M_TALENT_SZ_STATUS_out.json。
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent10_common as C  # noqa: E402

METRIC = "M_TALENT_SZ_STATUS"


def stat(vals):
    v = sorted(x for x in vals if x is not None)
    if not v:
        return {}
    return {"n": len(v), "mean": round(sum(v) / len(v), 2), "median": C.pctl(v, 0.5),
            "p25": C.pctl(v, 0.25), "p75": C.pctl(v, 0.75), "p90": C.pctl(v, 0.90),
            "max": max(v)}


def main() -> None:
    rows = C.rows()
    orcid = {r[0] for r in C.load("scholar_fill_20261022.json")["rows"] if r[1]}
    sz = [r for r in rows if C.is_sz_org(r["org"] or "")]
    narrow = [r for r in rows if r["city"] == "深圳市"]
    other = [r for r in rows if not C.is_sz_org(r["org"] or "")
             and r["city"] not in ("未归属", "未填")]

    def block(g):
        return {"n": len(g),
                "h": stat([r["h"] for r in g]),
                "cite": stat([r["cite"] for r in g]),
                "paper": stat([r["paper"] for r in g]),
                "h_ge50": sum(1 for r in g if (r["h"] or 0) >= 50),
                "h_ge50_share": C.share(sum(1 for r in g if (r["h"] or 0) >= 50), len(g)),
                "h_ge30_share": C.share(sum(1 for r in g if (r["h"] or 0) >= 30), len(g)),
                "cite_ge10000": sum(1 for r in g if (r["cite"] or 0) >= 10000),
                "cite_ge10000_share": C.share(sum(1 for r in g if (r["cite"] or 0) >= 10000), len(g)),
                "paper_ge100_share": C.share(sum(1 for r in g if (r["paper"] or 0) >= 100), len(g)),
                "orcid_share": C.share(sum(1 for r in g if r["sid"] in orcid), len(g))}

    A, B = block(sz), block(other)
    W = block(narrow)
    cities = {}
    for c in ("北京市", "上海市", "广州市", "杭州市", "南京市", "武汉市", "苏州市"):
        g = [r for r in rows if r["city"] == c]
        if g:
            cities[c] = {"n": len(g), "h_median": C.pctl([r["h"] for r in g], 0.5),
                         "cite_mean": round(sum(r["cite"] or 0 for r in g) / len(g), 2),
                         "h_ge50_share": C.share(sum(1 for r in g if (r["h"] or 0) >= 50), len(g))}
    orgs = Counter(r["org"] for r in sz if r["org"])
    cl = Counter(c for r in sz for c in r["cl"])
    cl_all = Counter(c for r in rows for c in r["cl"])
    acad = [r for r in sz if r.get("acad")]

    payload = {
        "support_judgment": "完全转换支持",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面地位对标；h-index/被引为库内累计值，不带年份，不能算「近五年增速」",
        "scope": {"universe": "talent22 面板 20,420（主档∩中文论文）",
                  "unit": "scholar_id", "sz_definition": "is_sz_org（机构名含深圳 或 loc2=深圳市）",
                  "control": "有属地且非深圳（不含未归属/未填）", "denominator": len(rows)},
        "groups": {"shenzhen": A, "other": B, "shenzhen_narrow": W},
        "ratio": {"h_median": round(A["h"]["median"] / B["h"]["median"], 4)
                  if B["h"].get("median") else None,
                  "cite_mean": round(A["cite"]["mean"] / B["cite"]["mean"], 4)
                  if B["cite"].get("mean") else None,
                  "h_ge50_share_pp": round(A["h_ge50_share"] - B["h_ge50_share"], 2),
                  "note": "比值 >1 表示深圳组更高；未做年龄/学科标准化，不能直接读成「人才更强」"},
        "cities": cities,
        "shenzhen_orgs": [{"org": k, "n": v} for k, v in orgs.most_common(12)],
        "shenzhen_clusters": [{"cluster": k, "n": v, "share": C.share(v, len(sz))}
                              for k, v in cl.most_common(12)],
        "cluster_lift": [{"cluster": k, "sz_share": C.share(v, len(sz)),
                          "all_share": C.share(cl_all.get(k, 0), len(rows)),
                          "lift": round((v / len(sz)) / (cl_all.get(k, 1) / len(rows)), 4)}
                         for k, v in cl.most_common(10) if cl_all.get(k)],
        "academicians": {"n": len(acad), "note": "面板 acad 标记来自 talent_flag 与主档交集，"
                                                 "深圳仅个位数，不能当城市院士总量"},
        "data_quality": {
            "denominator": "对照组剔除了 3,038 个未归属/未填者；若把他们并入对照组，深圳的领先幅度会变大，"
                           "本件不这么做",
            "no_normalization": "未按学科/年龄/机构类型标准化；深圳高校少、院所集中，"
                                "h-index 高可能反映「留下来的人本身更资深」",
            "cumulative": "h/cite/paper 是库内累计，老机构天然占优；深圳高校建校晚，"
                          "累计值对被试不利，结论偏保守",
            "wide_gap": f"严口径 {A['n']} 人 vs 窄口径 {W['n']} 人，差 {A['n']-W['n']} 人；"
                        "差额全是面板 city 把「哈尔滨工业大学(深圳)」等分支校区判回本部的错分"
                        "（10+5+4+1+1 人）与「北京大学深圳医院」2 人",
            "acad": "院士标记 112 个 id 中深圳可对齐者极少，城市院士总量应查外部名册，不应用本库",
        },
        "diff_vs_old_draft": {
            "old": "旧稿深圳 237 人、h 中位 23、被引均值 8,289、h≥50 占 15.19%",
            "now": f"深圳 {A['n']} 人、h 中位 {A['h'].get('median')}、被引均值 "
                   f"{A['cite'].get('mean'):,}、h≥50 占 {A['h_ge50_share']}%",
            "why": "本件与旧稿口径一致（机构名含深圳），人数差 1 人来自面板重建；"
                   "窄口径 213 人列在 shenzhen_narrow 供对照",
        },
        "findings": [
            f"深圳 {A['n']} 人：h 中位 {A['h'].get('median')}（对照组 {B['h'].get('median')}），"
            f"被引均值 {A['cite'].get('mean'):,}（对照组 {B['cite'].get('mean'):,}）",
            f"h≥50 占 {A['h_ge50_share']}%（对照组 {B['h_ge50_share']}%），"
            f"被引≥1 万占 {A['cite_ge10000_share']}%（对照组 {B['cite_ge10000_share']}%）",
            f"深圳集群首位 {cl.most_common(1)[0][0] if cl else '无'}"
            f"（{cl.most_common(1)[0][1] if cl else 0} 人），"
            f"机构首位 {orgs.most_common(1)[0][0] if orgs else '无'}"
            f"（{orgs.most_common(1)[0][1] if orgs else 0} 人）",
        ],
    }
    C.write(METRIC, payload)
    print("sz", A["n"], A["h"], A["cite"]["mean"], A["h_ge50_share"], "wide", W["n"])
    print("other", B["n"], B["h"], B["cite"]["mean"], B["h_ge50_share"])
    print("ratio", payload["ratio"])
    print("cities", cities)
    print("orgs", orgs.most_common(5), "cl", cl.most_common(5))
    print("acad", len(acad))


if __name__ == "__main__":
    main()
