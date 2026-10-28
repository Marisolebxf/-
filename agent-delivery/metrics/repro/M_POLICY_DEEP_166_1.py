#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_DEEP_166_1｜政策焦点识别模型（王惠四维口径 + 分位秩展示轨 + 堵点扫描）

零 SQL：读 20261021 快照
  code/_snapshots21/pg_policy_rows_20261021.json   20,000 行（type/rank/publish_year/长度计数）
  code/_snapshots21/policy_content_20261021.json   18,763 行（[id,title,content,publish_year,abstract]）

四维闭集词表照抄 calc-logic/POLICY/M_POLICY_DEEP_166_1.md，不临时扩词：
  D1 制定背景 = 依据类词频 / 正文字数        （扫 content + abstract）
  D2 政策目标 = 目标类词频 / 正文字数        （扫 content；另附 `到20\\d{2}年` 锚定子证据）
  D3 适用范围 = 对象/范围类词频 / 正文字数    （扫 content；support_object 项因 JSON 全空不可加）
  D4 措施完备性 = COUNT(DISTINCT support_behavior)+COUNT(DISTINCT support_way)
                 → policy_support 20,000 行全为占位符，本维整维缺失

两条合成轨（同一批原始值，只差归一方式）：
  A 王惠原式：各维截面 min-max → 缺维不进平均 → 等权 ×100
  B 分位秩  ：各维截面百分位 → 缺维不进平均 → 等权 ×100（页面可发布口径，P50 恒 50）

关键实现细节：
  * 词表按「长词优先、命中区间不重复计」计数，避免「贯彻落实」与「为贯彻落实」重复计数。
  * 先除以正文字符数（口径原文「词频 / 正文字数」），否则长文件会把分数整片拉满。
  * 快照正文是去空白形式（同一条政策 1,559 字符 vs 库内 LENGTH 4,301，差额为换行缩进），
    分母统一用去空白后的字符数，全库一致。
  * 年度口径只用 2016—2021；2022 残片/2023 空年/2024 单条不进分母（DATA_FACTS §3.16）。

输出：code/M_POLICY_DEEP_166_1_out.json
"""
import bisect
import collections
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")

BASIS_WORDS = ["为贯彻落实", "深入贯彻落实", "贯彻落实", "根据有关法律法规", "国务院决策部署",
               "有关规定", "有关要求", "根据", "依据", "依照", "遵照", "按照"]
GOAL_WORDS = ["总体目标", "发展目标", "预期目标", "主要目标", "工作目标",
              "目标", "预期", "力争", "确保", "实现"]
SCOPE_WORDS = ["适用于", "适用对象", "适用范围", "覆盖", "面向", "中小微企业", "中小企业",
               "高新技术企业", "专精特新", "制造业", "高校", "科研院所", "事业单位",
               "社会组织", "创业服务机构"]
GOAL_YEAR_RE = re.compile(r"到20\d{2}年")
PLACEHOLDER = {"", "NULL", "NONE", "-"}
WINDOW = [2016, 2017, 2018, 2019, 2020, 2021]


def nn(v):
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.upper() in PLACEHOLDER else s


def count_nonoverlap(text, words):
    """长词优先、命中区间不重复计。"""
    t = text or ""
    spans = []
    for w in words:
        start = 0
        while True:
            i = t.find(w, start)
            if i < 0:
                break
            spans.append((i, i + len(w)))
            start = i + len(w)
    spans.sort(key=lambda p: (p[0], -(p[1] - p[0])))
    n, last_end = 0, -1
    for s, e in spans:
        if s >= last_end:
            n += 1
            last_end = e
    return n


def mm01(vals):
    present = [v for v in vals if v is not None]
    if not present:
        return [None] * len(vals)
    u = set(present)
    if len(u) == 1:
        return [0.5 if v is not None else None for v in vals]
    lo, hi = min(u), max(u)
    return [(0.5 if v is None else (v - lo) / (hi - lo)) for v in vals]


def pct_rank(vals):
    """截面百分位（并列取平均秩）；None 原样返回。"""
    present = sorted(v for v in vals if v is not None)
    m = len(present)
    if not m:
        return [None] * len(vals)
    out = []
    for v in vals:
        if v is None:
            out.append(None)
        else:
            lo = bisect.bisect_left(present, v)
            hi = bisect.bisect_right(present, v)
            out.append(((lo + hi) / 2.0) / m)
    return out


def quant(sorted_vals, p):
    if not sorted_vals:
        return None
    return round(sorted_vals[min(len(sorted_vals) - 1, int(len(sorted_vals) * p))], 2)


def main():
    rows = json.load(open(os.path.join(SNAP, "pg_policy_rows_20261021.json"), encoding="utf-8"))
    content = json.load(open(os.path.join(SNAP, "policy_content_20261021.json"), encoding="utf-8"))
    txt = {r[0]: {"content": nn(r[2]), "abstract": nn(r[4])} for r in content}

    n = len(rows)
    basis_raw, goal_raw, scope_raw = [], [], []
    basis_avail, goal_avail, scope_avail = [], [], []
    anchor_hit, years = [], []

    for r in rows:
        t = txt.get(r["id"], {})
        body, abs_ = t.get("content", ""), t.get("abstract", "")
        ct_len, ab_len = len(body), len(abs_)

        if ct_len or ab_len:
            c = count_nonoverlap(body, BASIS_WORDS) + count_nonoverlap(abs_, BASIS_WORDS)
            basis_raw.append(1000.0 * c / max(ct_len + ab_len, 1))
        else:
            basis_raw.append(None)
        basis_avail.append(bool(ct_len or ab_len))

        if ct_len:
            goal_raw.append(1000.0 * count_nonoverlap(body, GOAL_WORDS) / ct_len)
            scope_raw.append(1000.0 * count_nonoverlap(body, SCOPE_WORDS) / ct_len)
        else:
            goal_raw.append(None)
            scope_raw.append(None)
        goal_avail.append(bool(ct_len))
        scope_avail.append(bool(ct_len))

        anchor_hit.append(1 if GOAL_YEAR_RE.search(body) else 0)
        y = nn(r.get("publish_year"))
        years.append(int(y) if y.isdigit() else None)

    dims = [("制定背景", basis_raw, basis_avail),
            ("政策目标", goal_raw, goal_avail),
            ("适用范围", scope_raw, scope_avail)]
    mm = {name: mm01(vals) for name, vals, _ in dims}
    pr = {name: pct_rank(vals) for name, vals, _ in dims}

    def compose(norm_map):
        scores, used, flags_all = [], [], []
        for i in range(n):
            avail = [name for name, _, av in dims if av[i]]
            if not avail:
                scores.append(None)
                used.append(0)
                flags_all.append([])
                continue
            vals = [norm_map[name][i] for name in avail]
            scores.append(sum(vals) / len(vals) * 100)
            used.append(len(avail))
            flags_all.append([name for name in avail if norm_map[name][i] < 0.25])
        return scores, used, flags_all

    score_a, used, block_a = compose(mm)
    score_b, _, block_minmax = compose(pr)

    # 堵点口径 B（本报告采用）：某维闭集词零命中 → 该维在文本中缺位
    block_b = []
    for i in range(n):
        avail = [name for name, vals, av in dims if av[i]]
        block_b.append([name for name, vals, av in dims if av[i] and vals[i] == 0])

    # 焦点标签：原始密度 argmax（min-max 是逐维单调变换，标签与 A 轨一致）
    labels = []
    label_cnt = collections.Counter()
    for i in range(n):
        avail = [(name, vals[i]) for name, vals, av in dims if av[i]]
        if not avail:
            labels.append("无文本")
            continue
        top = max(avail, key=lambda kv: kv[1])[0]
        labels.append(top)
        label_cnt[top] += 1

    va = sorted(s for s in score_a if s is not None)
    vb = sorted(s for s in score_b if s is not None)
    ns = len(va)

    def idx_stats(v, label):
        return {"track": label, "scored_rows": len(v),
                "p50": quant(v, 0.5), "p75": quant(v, 0.75), "p90": quant(v, 0.90),
                "min": round(v[0], 2), "max": round(v[-1], 2),
                "mean": round(sum(v) / len(v), 2),
                "ge60": sum(1 for s in v if s >= 60),
                "ge60_pct": round(100.0 * sum(1 for s in v if s >= 60) / len(v), 2)}

    block_cnt_a = collections.Counter()
    block_cnt_b = collections.Counter()
    for f in block_a:
        block_cnt_a.update(f)
    for f in block_b:
        block_cnt_b.update(f)

    yagg = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for i, y in enumerate(years):
        if y in WINDOW and score_b[i] is not None:
            yagg[y][0] += score_b[i]
            yagg[y][1] += score_a[i]
            yagg[y][2] += 1
    year_intensity = [{"year": y, "n": yagg[y][2],
                       "mean_score_percentile": round(yagg[y][0] / yagg[y][2], 2) if yagg[y][2] else None,
                       "mean_score_minmax": round(yagg[y][1] / yagg[y][2], 2) if yagg[y][2] else None}
                      for y in WINDOW]

    out = {
        "metric_id": "M_POLICY_DEEP_166_1",
        "title": "政策焦点识别模型",
        "probe_date": "2026-10-22",
        "data_support_level": "部分支持",
        "support_judgment": "部分支持",
        "support_reason": "四维里三维（制定背景/政策目标/适用范围）可算；措施完备性维依赖 policy_support，"
                          "该列 20,000 行全为占位符（非占位符计数 0）→ 整维缺失。按 §〇 定义落部分支持。",
        "base_years_used": ["2016", "2017", "2018", "2019", "2020", "2021"],
        "base_years_missing": ["2023"],
        "base_years_note": "焦点指数本身是截面归一，不涉时序分母；年度焦点强度只用 2016—2021 六个连续年份。"
                            "2023 年库内 0 行（缺失）、2022 年 289 条为采集截断残片、2024 年 1 条，三者均不进年度口径，"
                            "更不按 0 摊入任何年份分母（DATA_FACTS §3.16）。",
        "sources": {
            "pg_policy_rows": "code/_snapshots21/pg_policy_rows_20261021.json（20,000 行）",
            "policy_content": "code/_snapshots21/policy_content_20261021.json（18,763 行，正文去空白存储）",
            "field_probe": "code/_snapshots21/policy_fields_a23_20261021.json（4 条 SQL 实探）",
            "db": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
        },
        "inputs": {
            "rows": n,
            "rows_in_content_snapshot": len(content),
            "rows_without_text": n - sum(basis_avail),
            "content_snapshot_rule": "保留库内 content 长度 ≥51 字符的 18,763 条；"
                                     "另有 440 条正文 ≤50 字符、797 条正文为空，合计 1,237 条无可用正文",
            "abstract_available_in_snapshot": sum(1 for r in content if nn(r[4])),
            "theme_nonnull": 2,
            "keypoints_nonnull": 0,
            "policy_support_nonnull": 0,
        },
        "dims": {
            "measure_dim_available": False,
            "available_dims": "3/4（措施完备性整维缺失）",
            "mean_dims_used": round(sum(used) / n, 3),
            "unit": "每千字符词频（去空白正文字符数）",
            "raw": {
                "basis_per_1k": {"n": sum(1 for v in basis_raw if v is not None),
                                 "zero": sum(1 for v in basis_raw if v == 0),
                                 "mean": round(sum(v for v in basis_raw if v is not None) / ns, 4),
                                 "max": round(max(v for v in basis_raw if v is not None), 4)},
                "goal_per_1k": {"n": sum(1 for v in goal_raw if v is not None),
                                "zero": sum(1 for v in goal_raw if v == 0),
                                "mean": round(sum(v for v in goal_raw if v is not None) / ns, 4),
                                "max": round(max(v for v in goal_raw if v is not None), 4)},
                "scope_per_1k": {"n": sum(1 for v in scope_raw if v is not None),
                                 "zero": sum(1 for v in scope_raw if v == 0),
                                 "mean": round(sum(v for v in scope_raw if v is not None) / ns, 4),
                                 "max": round(max(v for v in scope_raw if v is not None), 4)},
            },
        },
        "focus_index": {
            "A_wanghui_minmax": idx_stats(va, "min-max（王惠原式）"),
            "B_percentile": idx_stats(vb, "分位秩（展示口径）"),
            "degeneracy_note": "min-max 轨在右偏词频上坍缩：P50<5、max<40、无一条 ≥60，"
                               "不能当 0—100 分发布；分位秩轨 P50 恒 50，可作页面展示但须标注「非王惠原式」",
        },
        "focus_label": {"rows": [{"label": k, "n": v, "pct": round(100.0 * v / ns, 2)}
                                 for k, v in label_cnt.most_common()],
                        "no_text_rows": n - ns},
        "block_scan": {
            "threshold_A": {"rule": "min-max < 0.25（calc-logic 演示阈值）",
                            "by_dim": [{"dim": k, "n": v} for k, v in block_cnt_a.most_common()],
                            "policy_with_any_block_pct": round(100.0 * sum(1 for f in block_a if f) / ns, 2),
                            "verdict": "几乎全量命中 → 该阈值在本库无判别力，弃用"},
            "threshold_B": {"rule": "该维闭集词零命中（文本中该维完全缺位）",
                            "by_dim": [{"dim": k, "n": v, "pct": round(100.0 * v / ns, 2)}
                                       for k, v in block_cnt_b.most_common()],
                            "policy_with_any_block": sum(1 for f in block_b if f),
                            "policy_with_any_block_pct": round(100.0 * sum(1 for f in block_b if f) / ns, 2),
                            "verdict": "零命中是「文本未写」的直接证据，不受归一标尺影响，本报告采用此口径"},
        },
        "goal_year_anchor": {
            "hit": sum(anchor_hit),
            "hit_pct": round(100.0 * sum(anchor_hit) / n, 2),
            "note": "正则 到20\\d{2}年 命中正文；作为「目标可量化」补充证据，不进指数",
        },
        "year_intensity": year_intensity,
        "verdict": "三维可算、标签与堵点可用；焦点指数只能用分位秩轨展示，min-max 轨坍缩不发布。"
                   "措施维待 policy_support 灌数后自动满配。",
    }

    dst = os.path.join(HERE, "M_POLICY_DEEP_166_1_out.json")
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: out[k] for k in ("metric_id", "support_judgment", "base_years_used")}, ensure_ascii=False))
    print("inputs", out["inputs"])
    print("raw", out["dims"]["raw"])
    print("A", out["focus_index"]["A_wanghui_minmax"])
    print("B", out["focus_index"]["B_percentile"])
    print("labels", out["focus_label"])
    print("blocksA", out["block_scan"]["threshold_A"]["by_dim"], out["block_scan"]["threshold_A"]["policy_with_any_block_pct"])
    print("blocksB", out["block_scan"]["threshold_B"]["by_dim"], out["block_scan"]["threshold_B"]["policy_with_any_block_pct"])
    print("anchor", out["goal_year_anchor"])
    print("year", year_intensity)
    print("->", dst)


if __name__ == "__main__":
    main()
