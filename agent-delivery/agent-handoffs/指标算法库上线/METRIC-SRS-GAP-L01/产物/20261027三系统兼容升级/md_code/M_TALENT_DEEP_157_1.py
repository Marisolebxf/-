#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_DEEP_157_1 —— 人才流动追踪模型（TALENT 深度分析第 157 号）

需求语义：基于人才关系链与资讯数据，按时间线展示区域/行业人才流入、流出与留存，
支撑趋势可视化与热点识别。需求未给「流动事件」的判定口径，也未给统计窗口。

本文口径（零 SQL，全部读 A-26 批落盘快照）：
  1. 流动主体 = `dwd_scholar_work_experience` 的 57,117 段履历（20,028 名学者）。
     该表自带 `is_current` 标记，**现机构取自表内标记，不 JOIN 学者主档**——因为两表
     scholar_id 只有 9.27% 交集（见 out.json 的 id_gap），JOIN 会把 90% 的人读成「无现机构」，
     从而把「历史在深圳」全部误计为流出（20261020 旧版即踩此坑）。
  2. 机构维度：一段履历 = 一个机构；机构名 → 城市用 _talent21_common.loc() 五级归属
     （高校名录 → 企业底册 → 前缀 → 城市关键词 → 海外）。
  3. 流动事件：按 start_time 升序把机构串成序列，相邻两段城市不同即记一条城际流动边。
     流入深圳 = 现机构城市为深圳、且历史出现过非深圳城市；流出深圳 = 现机构不在深圳、
     历史出现过深圳机构；留存 = 现机构与全部历史都在深圳。
  4. 时间线：取该人**首段深圳履历的 start_time 年份**作近似流入年；缺失年份不补。

产物：code/M_TALENT_DEEP_157_1_out.json。
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _talent21_common import base_year_block, loc, pctl, scholars, st, work, write_out  # noqa: E402

METRIC = "M_TALENT_DEEP_157_1"
SZ = "深圳市"

# 共享库的海外词表只覆盖国名，不覆盖「牛津大学/斯坦福大学」这类校名，
# 会把 3.4 万段履历误判为「未归属」。这里补一层校名/地名词表，只影响
# 「海外 vs 未归属」的归类，不改变任何城市级结果（两者都不进城市序列）。
FOREIGN_EXTRA = (
    "牛津", "剑桥", "伦敦", "帝国理工", "曼彻斯特", "爱丁堡", "格拉斯哥", "伯明翰", "利兹",
    "斯坦福", "哈佛", "麻省理工", "加州", "伯克利", "耶鲁", "普林斯顿", "康奈尔", "哥伦比亚大学",
    "芝加哥大学", "华盛顿大学", "密歇根", "威斯康星", "伊利诺伊", "宾夕法尼亚", "约翰霍普金斯",
    "东京", "京都", "大阪", "东北大学（日本）", "名古屋", "北海道", "首尔", "延世", "高丽",
    "南洋理工", "新加坡国立", "墨尔本", "悉尼", "新南威尔士", "昆士兰", "莫纳什", "阿德莱德",
    "多伦多", "麦吉尔", "滑铁卢", "阿尔伯塔", "英属哥伦比亚", "哥本哈根", "奥胡斯", "乌普萨拉",
    "苏黎世", "洛桑", "代尔夫特", "埃因霍温", "鲁汶", "根特", "慕尼黑", "柏林", "海德堡",
    "亚琛", "科英布拉", "阿威罗", "波尔图", "巴塞罗那", "马德里", "米兰", "罗马", "巴黎",
    "里昂", "马赛", "维也纳", "布拉格", "华沙", "莫斯科", "圣彼得堡", "开罗", "特拉维夫",
    "圣保罗", "赫尔辛基", "里斯本", "亚利桑那", "纽卡斯尔", "明尼苏达", "米尼奥", "霍普金斯",
    "普渡", "隆德", "南安普顿", "布里斯托", "卡内基梅隆", "贝尔格莱德", "佐治亚", "佛罗里达",
    "俄亥俄", "诺丁汉", "谢菲尔德", "北卡罗来纳", "那不勒斯", "奥尔堡", "埃默里", "帕多瓦",
    "橡树岭", "萨格勒布", "瓦伦西亚", "奥克兰", "约克大学", "杜克", "莱斯大学", "范德堡",
)
DOMESTIC_SPECIAL = {
    "中国科学院": "北京市", "中国社会科学院": "北京市", "中国农业科学院": "北京市",
    "中国医学科学院": "北京市", "中国工程院": "北京市", "中国科协": "北京市",
}


def city_of(org: str) -> str:
    if org in DOMESTIC_SPECIAL:
        return DOMESTIC_SPECIAL[org]
    c = loc(org)[1]
    if c in ("未填", "未归属") and any(t in (org or "") for t in FOREIGN_EXTRA):
        return "海外"
    return c


def main() -> None:
    rows = work()
    main_ids = {s["sid"] for s in scholars() if s["name"]}

    seg: dict[str, list[dict]] = defaultdict(list)
    org_empty = 0
    no_year = 0
    for w in rows:
        if not w["org"]:
            org_empty += 1
            continue
        if w["y0"] is None:
            no_year += 1
        seg[w["sid"]].append(w)

    scholars_with_org = len(seg)
    seg_total = sum(len(v) for v in seg.values())

    # ---- 现机构：is_current 优先，多条取 start 最大；无标记取最近一段 ----
    cur_org: dict[str, str] = {}
    cur_city: dict[str, str] = {}
    cur_idx: dict[str, int] = {}
    for sid, ss in seg.items():
        cur = [(i, x) for i, x in enumerate(ss) if x["cur"]]
        if cur:
            i, pick = max(cur, key=lambda p: (p[1]["y0"] or 0))
        else:
            i, pick = max(enumerate(ss), key=lambda p: (p[1]["y0"] or 0))
        cur_org[sid] = pick["org"]
        cur_city[sid] = city_of(pick["org"])
        cur_idx[sid] = i

    orgs_n = Counter(len({x["org"] for x in ss}) for ss in seg.values())
    cities_n = Counter(len({city_of(x["org"]) for x in ss}) for ss in seg.values())

    mobile_org = {sid for sid, ss in seg.items() if len({x["org"] for x in ss}) >= 2}
    mobile_city = {sid for sid, ss in seg.items() if len({city_of(x["org"]) for x in ss}) >= 2}

    # ---- 深圳三态 ----
    inflow, outflow, stay, local_single = [], [], [], []
    entry_year: Counter = Counter()
    for sid, ss in seg.items():
        # 历史 = 除现机构那一段以外的所有机构；把现机构算进历史会让「流入」恒为 0
        hist_cities = {city_of(x["org"]) for i, x in enumerate(ss) if i != cur_idx[sid]}
        hist_non_sz = hist_cities - {SZ}
        sz_hist = SZ in hist_cities
        sz_now = cur_city[sid] == SZ
        is_inflow = False
        if sz_now and hist_non_sz:
            inflow.append(sid)
            is_inflow = True
        elif sz_now and sz_hist:
            stay.append(sid)
        elif sz_now:
            local_single.append(sid)          # 只有一段履历且就在深圳：无历史可比，不算流入也不算留存
        elif sz_hist:
            outflow.append(sid)
        if is_inflow:
            ys = [x["y0"] for x in ss if city_of(x["org"]) == SZ and x["y0"]]
            if ys:
                entry_year[min(ys)] += 1

    # ---- 城际流动边：按 start 年排序后相邻城市变化 ----
    edge: Counter = Counter()
    unknown_edge = 0
    for sid, ss in seg.items():
        seq = []
        for x in sorted(ss, key=lambda z: (z["y0"] or 0)):
            c = city_of(x["org"])
            if c in ("未填", "未归属"):
                unknown_edge += 1
                continue
            if c in ("海外",):
                continue
            if not seq or seq[-1] != c:
                seq.append(c)
        for a, b in zip(seq, seq[1:]):
            if a != b:
                edge[(a, b)] += 1

    sz_in_edges = sum(n for (a, b), n in edge.items() if b == SZ)
    sz_out_edges = sum(n for (a, b), n in edge.items() if a == SZ)

    # ---- 具名样例：只有 9.27% 可挂主档，因此主键给机构、姓名仅在可挂时给 ----
    name_of = {s["sid"]: s["name"] for s in scholars()}

    def sample(sid: str) -> dict:
        ss = sorted(seg[sid], key=lambda z: (z["y0"] or 0))
        return {"name": name_of.get(sid, ""), "name_available": sid in main_ids,
                "now_org": cur_org[sid], "now_city": cur_city[sid],
                "n_orgs": len({x["org"] for x in ss}),
                "first_sz_year": min([x["y0"] for x in ss
                                      if city_of(x["org"]) == SZ and x["y0"]] or [None]) or None}

    inflow_sorted = sorted(inflow, key=lambda sid: (sample(sid)["first_sz_year"] or 9999))
    inflow_examples = [sample(x) for x in inflow_sorted[:12]]

    # ---- 城市存量与净流动 ----
    city_now = Counter(cur_city[sid] for sid in seg)
    top_cities = [{"city": c, "scholars": v} for c, v in city_now.most_common(12)]

    years = sorted(entry_year)
    missing_years = [y for y in range(years[0], years[-1] + 1) if y not in entry_year] if years else []
    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": (
            "履历表 57,117 段覆盖 20,028 名学者，机构序列/城际边/深圳三态可全量现转，"
            "流动骨架成立；但需求点名的社交网络、招聘网站、简历数据库三类源在库内无表"
            "（dwd_job 仅 10 行），流失与流入只能用「现机构 vs 历史机构」代理，"
            "且履历表与身份主档只有 9.27% 可挂（姓名/职称仅在这部分可用），"
            "深圳流入年样本集中在少数年份 → 部分支持。"),
        "method": {
            "flow_unit": "一段履历 = 一个机构；同一机构多段合并",
            "current_org_rule": "is_current=1 优先，多条取 start_time 最大；无标记取最近一段",
            "city_attribution": "高校名录精确 → 企业底册精确 → 前缀 → 城市关键词 → 海外 → 未归属",
            "inflow": "现机构城市=深圳市，且历史城市集合不含深圳市",
            "outflow": "现机构城市≠深圳市，且历史城市集合含深圳市",
            "stay": "现机构城市=深圳市，且历史城市集合含深圳市",
            "edge": "按 start_time 升序的相邻两个不同城市记一条有向边",
            "entry_year": "该人首段深圳履历的 start_time 年份",
        },
        "id_gap": {
            "work_distinct_ids": len(seg),
            "main_named_ids": len(main_ids),
            "linked": len(set(seg) & main_ids),
            "linked_pct": round(100 * len(set(seg) & main_ids) / max(1, len(seg)), 2),
            "note": "履历表用另一套 scholar_id 码域且无姓名列，姓名/职称只在约一成的人上可得；"
                    "本文的流动判定全部在履历表内部完成，不依赖该 JOIN。",
        },
        "coverage": {
            "work_rows": len(rows),
            "rows_with_org": seg_total,
            "rows_org_empty": org_empty,
            "rows_org_empty_pct": round(100 * org_empty / max(1, len(rows)), 2),
            "rows_no_start_year": no_year,
            "scholars_with_org": scholars_with_org,
            "scholars_with_current_flag": sum(1 for ss in seg.values() if any(x["cur"] for x in ss)),
            "current_rows": sum(1 for x in rows if x["cur"]),
        },
        "org_structure": {
            "orgs_per_scholar": {str(k): v for k, v in sorted(orgs_n.items())[:12]},
            "cities_per_scholar": {str(k): v for k, v in sorted(cities_n.items())[:12]},
            "mobile_org_scholars": len(mobile_org),
            "mobile_org_pct": round(100 * len(mobile_org) / max(1, scholars_with_org), 2),
            "mobile_city_scholars": len(mobile_city),
            "mobile_city_pct": round(100 * len(mobile_city) / max(1, scholars_with_org), 2),
        },
        "sz_flow": {
            "inflow": len(inflow),
            "outflow": len(outflow),
            "stay": len(stay),
            "local_single": len(local_single),
            "net_proxy": len(inflow) - len(outflow),
            "inflow_plus_stay_plus_local": len(inflow) + len(stay) + len(local_single),
            "inflow_pct_of_all": round(100 * len(inflow) / max(1, scholars_with_org), 2),
            "outflow_pct_of_all": round(100 * len(outflow) / max(1, scholars_with_org), 2),
            "sz_now_total": sum(1 for sid in seg if cur_city[sid] == SZ),
            "sz_hist_total": sum(1 for ss in seg.values() if SZ in {city_of(x["org"]) for x in ss}),
        },
        "city_flow": {
            "edges_total": sum(edge.values()),
            "distinct_pairs": len(edge),
            "top20": [{"from": a, "to": b, "n": n} for (a, b), n in edge.most_common(20)],
            "to_sz": sz_in_edges,
            "from_sz": sz_out_edges,
            "unknown_city_segments_skipped": unknown_edge,
        },
        "entry_year_dist": {str(y): entry_year[y] for y in years},
        "entry_year_stats": {
            "years_covered": len(years),
            "min": years[0] if years else None,
            "max": years[-1] if years else None,
            "n_events": sum(entry_year.values()),
            "with_year": sum(entry_year.values()),
        },
        "top_cities_now": top_cities,
        "inflow_examples": inflow_examples,
        "base_years_used": years,
        "base_years_missing": missing_years,
        "base_years_note": (
            "流入年分布只用履历 start_time 中**真实出现**的年份（%s—%s，共 %d 个有事件的年）；"
            "区间内没有事件的年份列入 base_years_missing，不补 0、也不作分母。"
            "本指标不做跨年基准或增速，因此不存在「前 N 年均值」这类分母。"
            % (years[0] if years else "—", years[-1] if years else "—", len(years))),
        "probes": {
            "sql_count": 0,
            "source": "gkx.dwd_scholar_work_experience 快照 _snapshots21/probe_talent21_20261022.json",
            "org_geo": "_snapshots21/base_20261021.json + talent.heis（3,501 所高校）",
        },
        "reused_from": [],
    }
    write_out(METRIC, payload)


if __name__ == "__main__":
    main()
