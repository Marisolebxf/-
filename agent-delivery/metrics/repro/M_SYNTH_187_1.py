#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_187_1 区域创新要素类型综合评价模型 —— gkx 重建版（20261022）。

王惠口径：七维（创新人才 / 企业 / 政策 / 服务机构 / 科研机构 / 资金 / 空间），
维内叶子极值归一等权，七维等权合成 0—100。

与旧版（20261020 `code/M_SYNTH_187_1.py`）的差别不在公式，在**叶子能不能算**：
旧版走 `_synthb_engine.probe_all()`，该引擎连的是一个已被隔离的演示库实例（ods / ads 两个 schema，
主机与库名见 `_quarantine` 内的原件，本文不复制），因此「服务机构」维直接读演示 ADS 的 `svc_org_card`、
「资金」维读 `SUM(funding_amount)`（自由文本列）。本版逐叶在 gkx 上重取，
不可算的叶子记 None 并写明原因，**不拿演示面的数补位**。

本脚本只读本目录 `code/_snapshots21/`（见 `_synth18x_common.SOURCES`），零数据库连接。
输出：`code/M_SYNTH_187_1_out.json`
"""
from __future__ import annotations

import collections
import os
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
import _synth18x_common as S  # noqa: E402

METRIC = "M_SYNTH_187_1"

# 七结构 → 叶子。键名同时是 188 的消费契约（`M_SYNTH_188_1.py` 的 STRUCT_LEAVES
# 必须与本字典逐字一致，否则 188 会因 KeyError 直接断——这是 §3.20 那类「上游不在场」
# 事故的另一种形态，故两边都在文件头写明）。
STRUCT_LEAVES = collections.OrderedDict([
    ("人才结构", ["D1_学者密度", "D1_高学历人才占比"]),
    ("企业结构", ["D2_新注册企业数2024", "D2_科技型企业占比", "D2_大型企业占比"]),
    ("政策结构", ["D3_政策文件数", "D3_政策类型数"]),
    ("服务机构结构", ["D4_科技服务业企业数", "D4_科技服务业企业占比"]),
    ("科研机构结构", ["D5_科研机构数", "D5_科研机构类型数", "D5_RI对齐2024授权"]),
    ("资金结构", ["D6_上市研发2024", "D6_融资笔数2024"]),
    ("空间结构", ["D7_园区代理数"]),
])

LEAF_META = {
    "D1_学者密度": {"unit": "人/万家企业", "src": "probe_a26_20261022.json + star_base_rows_gkx.json"},
    "D1_高学历人才占比": {"unit": "%", "src": "probe_talent21_20261022.json(edu) / 同学者数"},
    "D2_新注册企业数2024": {"unit": "家", "src": "dwd_org_base_info.incorporation_year=2024"},
    "D2_科技型企业占比": {"unit": "%", "src": "cityfam_hightech_20261021.json / 企业底册"},
    "D2_大型企业占比": {"unit": "%", "src": "dwd_org_base_info.org_size='大型'"},
    "D3_政策文件数": {"unit": "条", "src": "dwd_policy_base（市级存量，采集止点 2022-06）"},
    "D3_政策类型数": {"unit": "类", "src": "dwd_policy_base.type 文件体裁去重（非主题）"},
    "D4_科技服务业企业数": {"unit": "家", "src": "企业底册 industry_l1='科学研究和技术服务业'"},
    "D4_科技服务业企业占比": {"unit": "%", "src": "同上 / 企业底册"},
    "D5_科研机构数": {"unit": "家", "src": "dwd_research_institute_base_info（2,074 行）"},
    "D5_科研机构类型数": {"unit": "类", "src": "同上 org_type 去重"},
    "D5_RI对齐2024授权": {"unit": "件", "src": "patent_2024_by_name ∩ 机构名册（精确匹配）"},
    "D6_上市研发2024": {"unit": "亿元", "src": "gba_rd_20261021.json（仅上市主体）"},
    "D6_融资笔数2024": {"unit": "笔", "src": "_fin_year_20261022.json（completion_date 年）"},
    "D7_园区代理数": {"unit": "家", "src": "企业名称含 园区/高新区/众创/孵化/产业基地"},
}

LEAVES_UNAVAILABLE = {    "D1_研发人员占比": "dwd_org_annual_financial_info.development_employee 全表 90,926 行"
                    "非空 0 行（SUM(col IS NOT NULL)=0，DATA_FACTS §3.10），分母不存在",
    "D4_服务机构类型数": "六类服务机构分类（FINANCE/IP/HR/MKT/CONSULT/INNOV）只存在于演示 ADS 的 "
                    "svc_org_card，gkx 无此表；改行业小类后四市均只有 3 类，无区分度",
    "D6_融资总额": "dwd_org_financing_info.funding_amount 是自由文本（『8320.0万人民币』"
               "『4.70049747亿人民币』『1.1亿美元』混排），SUM() 会把不同量纲直接相加",
    "D7_创新空间面积": "库内无园区面积/建筑面积字段",
    "D7_创新空间密度": "同上",
}

# 能算出、但不进维度分的叶子：不是缺数，是「这点差异撑不起 0—100 的跨度」。
# 高学历占比只有深穗两城有学位记录（39/39=100.00% 对 75/77=97.40%），
# 两比例差异用 Fisher 精确检验 p=0.5498，统计上不可区分；
# 2.60 个百分点的差在批内 min-max 下会被放大成整整 100 分的极差，
# 反而让「广州学者密度是深圳 7.2 倍」这个真实结构被抹平。
# 原始值照常写进 leaves，供复核；维度分不用它，理由写进 MD §四。
LEAF_DEGENERATE = {
    "D1_高学历人才占比": "仅深穗两城有学位记录（39/39 = 100.00% vs 75/77 = 97.40%），"
                   "Fisher 精确检验 p=0.5498，差异不显著；批内 min-max 会把 2.60pp "
                   "放大成 0—100 的伪区分度，故只披露原始值、不进维度分",
}


def main():
    ot = S.org_totals()
    tot = ot["count"]
    sb = S.scholar_by_city()
    ht = S.hightech_by_city()
    ind = S.org_industry()
    ri = S.research_institutes()
    ri_gr = S.ri_aligned_grants()
    pol = S.policy_stats()
    rd = S.rd_by_city()
    fin = S.financing()

    # ---- 企业底册四城聚合（本批探针一次全表扫描，见 probe org_city_agg） ----
    agg = {r[0]: {"n": int(r[1]), "large": int(r[2]), "size_ok": int(r[3]),
                  "new2024": int(r[4]), "new2025": int(r[5]), "new2124": int(r[6]),
                  "park_proxy": int(r[7]), "sci_serv": int(r[8]),
                  "kinds_l2": int(r[9]), "status_ok": int(r[10])}
           for r in S.q("org_city_agg")}

    leaves = collections.OrderedDict()

    # D1 人才结构
    leaves["D1_学者密度"] = {c: (round(sb["n"].get(c, 0) / (tot[c] / 10000.0), 4)
                                if tot.get(c) else None) for c in S.CITIES}
    leaves["D1_高学历人才占比"] = {c: (round(sb["grad_ratio"][c] * 100.0, 4)
                                     if sb["grad_ratio"].get(c) is not None else None)
                                  for c in S.CITIES}

    # D2 企业结构
    leaves["D2_新注册企业数2024"] = {c: agg[c]["new2024"] for c in S.CITIES}
    leaves["D2_科技型企业占比"] = {c: S.ratio(ht.get(c, 0), tot[c]) for c in S.CITIES}
    leaves["D2_大型企业占比"] = {c: S.ratio(agg[c]["large"], tot[c]) for c in S.CITIES}

    # D3 政策结构
    leaves["D3_政策文件数"] = {c: pol["n"].get(c, 0) for c in S.CITIES}
    leaves["D3_政策类型数"] = {c: pol["kinds"].get(c, 0) for c in S.CITIES}

    # D4 服务机构结构（演示 ADS 不可用 → 用科技服务业企业口径替代）
    leaves["D4_科技服务业企业数"] = {c: ind["sci"].get(c, 0) for c in S.CITIES}
    leaves["D4_科技服务业企业占比"] = {c: S.ratio(ind["sci"].get(c, 0), tot[c])
                                    for c in S.CITIES}

    # D5 科研机构结构
    leaves["D5_科研机构数"] = {c: ri["n"].get(c, 0) for c in S.CITIES}
    leaves["D5_科研机构类型数"] = {c: ri["kinds"].get(c, 0) for c in S.CITIES}
    leaves["D5_RI对齐2024授权"] = {c: ri_gr.get(c, 0) for c in S.CITIES}

    # D6 资金结构
    leaves["D6_上市研发2024"] = {c: rd["y2024"].get(c) for c in S.CITIES}
    leaves["D6_融资笔数2024"] = {c: fin["y2024"].get(c, 0) for c in S.CITIES}

    # D7 空间结构
    leaves["D7_园区代理数"] = {c: ind["park"].get(c, 0) for c in S.CITIES}

    # ---- 极值归一 + 维内等权 + 七维等权 ----
    leaf_norm = {k: S.mm(v) for k, v in leaves.items()}
    dim_scores, dim_detail = collections.OrderedDict(), collections.OrderedDict()
    for st, keys in STRUCT_LEAVES.items():
        use = [k for k in keys if k not in LEAF_DEGENERATE]
        dim_scores[st] = {c: S.wmean([leaf_norm[k].get(c) for k in use]) for c in S.CITIES}
        dim_detail[st] = {c: [leaf_norm[k].get(c) for k in keys] for c in S.CITIES}

    index = {c: S.wmean([dim_scores[st][c] for st in STRUCT_LEAVES]) for c in S.CITIES}
    rank = sorted([c for c in S.CITIES if index[c] is not None], key=lambda x: -index[x])

    # ---- 敏感性：四条替代口径（全现算）----
    dim_all = collections.OrderedDict()
    for st, keys in STRUCT_LEAVES.items():
        dim_all[st] = {c: S.wmean([leaf_norm[k].get(c) for k in keys]) for c in S.CITIES}
    sensitivity = {
        "含退化叶子": {c: S.wmean([dim_all[st][c] for st in STRUCT_LEAVES]) for c in S.CITIES},
        "剔除人才结构维": {c: S.wmean([dim_scores[st][c] for st in STRUCT_LEAVES
                                if st != "人才结构"]) for c in S.CITIES},
        "剔除人才+服务机构维": {c: S.wmean([dim_scores[st][c] for st in STRUCT_LEAVES
                                  if st not in ("人才结构", "服务机构结构")])
                        for c in S.CITIES},
        "15叶全等权": {c: S.wmean([leaf_norm[k].get(c) for k in leaves
                               if k not in LEAF_DEGENERATE]) for c in S.CITIES},
    }
    aux = {
        "高企数2024": {c: ht.get(c, 0) for c in S.CITIES},
        "底册企业数": {c: tot[c] for c in S.CITIES},
        "大型企业数": {c: agg[c]["large"] for c in S.CITIES},
        "新注册2024": {c: agg[c]["new2024"] for c in S.CITIES},
        "科研机构数": {c: ri["n"].get(c, 0) for c in S.CITIES},
    }

    out = {
        "metric_id": METRIC,
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "source": "gkx @ 183.240.141.251:3318（gkx_reader_zp 只读），经 _snapshots21/ 落盘快照读取；"
                  "零数据库连接（本脚本不连库）",
        "evaluation_set": S.CITIES,
        "stat_year": S.T_YEAR,
        "leaves": leaves,
        "leaves_meta": LEAF_META,
        "leaves_unavailable": LEAVES_UNAVAILABLE,
        "leaves_degenerate_excluded": LEAF_DEGENERATE,
        "leaf_norm": leaf_norm,
        "dim_scores": dim_scores,
        "dim_detail_norm": dim_detail,
        "aux": aux,
        "sensitivity": sensitivity,
        "index_0_100": {c: (round(index[c], 1) if index[c] is not None else None)
                        for c in S.CITIES},
        "rank": rank,
        "n_leaves": {st: len(keys) for st, keys in STRUCT_LEAVES.items()},
        "coverage": {
            "org_rows": ot["n_rows"],
            "org_rows_4city": sum(tot[c] for c in S.CITIES),
            "org_4city_share": round(sum(tot[c] for c in S.CITIES) / ot["n_rows"] * 100, 2),
            "dup_names": ot["n_dup_names"],
            "scholars_total": len(S.scholars()),
            "scholars_4city": sb["total_n"],
            "scholars_4city_share": round(sb["total_n"] / len(S.scholars()) * 100, 2),
            "policy_rows": pol["total_rows"],
            "policy_4city": sum(pol["n"].values()),
            "ri_rows": ri["total"],
            "rd_orgs": rd["orgs"],
        },
        "params": {
            "normalization": "批内 min-max（跨四城，单叶全同或单点 → None，不补 0）",
            "degenerate_leaf": "D1_高学历人才占比 只披露不移入维度分（2 城、2.60pp、Fisher p=0.5498）",
            "dim_weight": "维内叶子等权（缺叶不进分母）",
            "structure_weight": "七结构等权",
            "policy_window": "存量（四市 publish_date 止于 2022，未按年截断，见 DATA_FACTS §3.7）",
            "park_proxy": "企业名称关键词：园区/高新区/众创/孵化/产业基地（名称代理，非园区名录）",
            "rnd_window": "2024 年全年累计（occur_period 末两位=12），仅上市主体",
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "七结构中五结构（企业/政策/科研机构/资金/空间）有 gkx 真实非零读数并逐叶可复现；"
            "但人才结构维的『研发人员占比』分母整列为空（development_employee 0/90,926 非空）、"
            "高学历占比只有深穗两城有学历样本（116 条学位记录）；服务机构维的六类分类只存在于"
            "演示 ADS 的 svc_org_card，gkx 无此表，只能退化为行业口径；空间维仅有名称关键词代理、"
            "无面积与密度。存在至少四个维度被迫降级，不满足『完全转换支持』要求的"
            "『结构 + 数据量都够』，判部分支持"),
        "note": "旧版（20261020）读数由演示库 _synthb_engine 产出，与本文不可直接比较；"
                "逐项差异见 MD §〇.2。",
    }
    out.update(S.base_block(
        [S.T_YEAR],
        [y for y in S.PATENT_YEARS if y != S.T_YEAR],
        "本指标为 2024 年截面，单叶都是当年计数或当年比率，不做多年均值、不做 CAGR，"
        "因此没有『前 N 年基准』这一层分母。专利只取 2024（库内 2021—2026 真实存在，"
        "2017—2020 零行，§3.16）；政策取全表存量、不按年截断（§3.7）。"
        "2025/2026 在 missing 里是因为它们不是本批的统计年，不是因为缺失被摊成 0。"))

    S.write_out(METRIC, out)
    print("index", out["index_0_100"], "rank", rank)


if __name__ == "__main__":
    main()
