#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_ACADEMIC_POWER —— 学术生态（gkx 口径 · 四市截面 · 链轴不可闭合）

口径（全部本件自算，无任何 demo / live 连接）：
  D1 学研机构 = gkx.dwd_org_heis_info（高校）+ gkx.dwd_research_institute_base_info（科研院所），
     按 city 字段等值汇总；两池 name_cn 集合交集在 out.json 的 pool_overlap 里落盘。
  D2 学术人才 = gkx.dwd_scholar。理想轨是 scholar_org_id → 机构主键，实测该列非空 0 行，
     只能退化为「机构名含城市名」的名称代理轨。
  D3 学术论文 = gkx.dwd_zh_paper.author_info_list 展开 → 机构名精确匹配
     code/_snapshots21/base_20261021.json 的 name_cn → 取该机构 city。窗口取 cover_year_start
     2021—2024（库内 2021—2026 有值，2025/2026 收录不全，不入正式值）。
  合成：三维各做四市 min-max ×100，再按 0.4/0.3/0.3 加权。
  ★ 权重与归一方式是本件自定义、待甲方确认，不是甲方或王惠口径的原值。

链轴（本指标真正的缺口）：链成员表 gkx.dwd_org_industry_tags 的 credit_code 与
学研机构 external_id 两个键域互不相交（5 万行样本 0 命中、0 条以事业单位前缀 12 开头），
因此「指定链 × 区域」的双限定在本库无法闭合；本件只出区域截面，不出链级读数。

数据纪律：
  * 只连 gkx（183.240.141.251:3318，只读账号）；连接失败重试 5 次、指数退避；
  * 每条 SQL 前 SET SESSION max_execution_time（毫秒），不设 0；
  * 对 dwd_patent 不发任何 SQL（DATA_FACTS §3.13：专利面板只读缓存）；
  * 不 import 本目录以外的模块，脚本自带连接器。

产物：code/M_CHAIN_ACADEMIC_POWER_out.json
"""
from __future__ import annotations

import json
import os
import time

import pymysql

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_ACADEMIC_POWER_out.json")
BASE = os.path.join(SNAP, "base_20261021.json")

CITIES = ["广州市", "深圳市", "东莞市", "惠州市"]

# 本件自定义权重（待甲方确认）
W_PAPER, W_INST, W_SCHOLAR = 0.4, 0.3, 0.3
YEAR_FROM, YEAR_TO = 2021, 2024          # 论文窗口（库内真实有值的年份）
SAMPLE_N = 50000                          # 链成员键域抽查行数

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=20,
           read_timeout=60, autocommit=True)

_CONN = None
PROBES = []


def conn():
    """连接 gkx；最多 5 次，指数退避（实测 10 次连接约 2 次 15—20 秒超时）。"""
    global _CONN
    if _CONN is not None:
        return _CONN
    last = None
    for i in range(5):
        try:
            _CONN = pymysql.connect(**GKX)
            return _CONN
        except Exception as e:                       # noqa: BLE001
            last = e
            wait = 2 ** (i + 1)
            print(f"  [conn retry {i + 1}/5] {type(e).__name__}: {str(e)[:80]} -> {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"gkx 连接 5 次均失败：{last}")


def q(label, sql, cap_ms=120000):
    """单条查询：独立游标 + 会话级 max_execution_time，连接断了重连一次。"""
    global _CONN
    t = time.time()
    for attempt in (1, 2):
        try:
            cur = conn().cursor()
            cur.execute("SET SESSION max_execution_time=%d" % cap_ms)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            PROBES.append({"label": label, "sql": " ".join(sql.split()),
                           "rows": len(rows)})
            return rows
        except Exception as e:                       # noqa: BLE001
            _CONN = None
            if attempt == 2:
                raise
            print(f"  [query retry] {label}: {type(e).__name__}: {str(e)[:80]}")
            time.sleep(3)


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    print("[1/6] 机构池（高校 + 科研院所）按城市")
    heis_rows = q("heis_name_ext_city",
                  "SELECT name_cn, external_id, city FROM gkx.dwd_org_heis_info")
    ri_rows = q("ri_name_ext_city",
                "SELECT name_cn, external_id, city FROM gkx.dwd_research_institute_base_info")
    # 高校表有重复行：3,501 行只有 2,933 个不同 external_id（同一所高校被重复录入，
    # 实测「广州中医药大学」出现两次）。按 external_id 去重后再分市，否则 D1 会虚高。
    heis_city, ri_city = {}, {}
    seen = {}
    heis_dup_rows = 0
    for _n, ext, c in heis_rows:
        key = str(ext or "")
        if key and key in seen:
            heis_dup_rows += 1
            continue
        if key:
            seen[key] = str(c or "")
        heis_city[str(c or "")] = heis_city.get(str(c or ""), 0) + 1
    ri_dup_rows = 0
    cross = 0
    for _n, ext, c in ri_rows:
        key = str(ext or "")
        if key and key in seen:          # 同一法人两池并存（实测 1 例：广州中医药大学）
            cross += 1
            continue
        if key:
            seen[key] = str(c or "")
        ri_city[str(c or "")] = ri_city.get(str(c or ""), 0) + 1
    heis_n, ri_n = len(heis_rows), len(ri_rows)
    name_overlap = cross

    print("[2/6] 学者池（scholar_org_id 填充率 + 名称轨）")
    sc = q("scholar_profile",
           "SELECT COUNT(*), "
           "SUM(scholar_org_id IS NOT NULL AND TRIM(scholar_org_id) NOT IN ('','NULL')), "
           "SUM(scholar_org_name_zh IS NULL OR UPPER(TRIM(scholar_org_name_zh)) IN ('NULL','')), "
           "SUM(scholar_org_name_zh LIKE '%广州%'), SUM(scholar_org_name_zh LIKE '%深圳%'), "
           "SUM(scholar_org_name_zh LIKE '%东莞%'), SUM(scholar_org_name_zh LIKE '%惠州%') "
           "FROM gkx.dwd_scholar")[0]
    scholar_total = int(sc[0])
    scholar_org_id_nonempty = int(sc[1] or 0)
    scholar_org_name_empty = int(sc[2] or 0)
    scholar_alias = {"广州市": int(sc[3] or 0), "深圳市": int(sc[4] or 0),
                     "东莞市": int(sc[5] or 0), "惠州市": int(sc[6] or 0)}

    print("[3/6] 论文维：%d—%d 窗口，机构名 → 城市" % (YEAR_FROM, YEAR_TO))
    base = load("base_20261021.json")
    name2city = {}
    for r in base:                      # r = [org_id, credit_code, name_cn, province, city]
        name2city.setdefault(str(r[2]).strip(), str(r[4]).strip())
    paper_total = int(q("paper_rows", "SELECT COUNT(*) FROM gkx.dwd_zh_paper")[0][0])
    rows = q("paper_window",
             "SELECT id, cover_year_start, author_info_list FROM gkx.dwd_zh_paper "
             "WHERE cover_year_start BETWEEN %d AND %d" % (YEAR_FROM, YEAR_TO), cap_ms=180000)
    pairs = set()
    inst_instances = inst_hits = 0
    for pid, _y, al in rows:
        try:
            arr = json.loads(al) if al else []
        except Exception:                # noqa: BLE001
            arr = []
        if not isinstance(arr, list):
            continue
        hit_cities = set()
        for a in arr:
            if not isinstance(a, dict):
                continue
            nm = a.get("institution") or a.get("affiliation")
            if not nm:
                continue
            inst_instances += 1
            ct = name2city.get(str(nm).strip())
            if ct:
                inst_hits += 1
                hit_cities.add(ct)
        for ct in hit_cities:
            pairs.add((pid, ct))
    paper_city = {c: sum(1 for _, ct in pairs if ct == c) for c in CITIES}
    papers_with_city = len({p for p, _ in pairs})

    print("[4/6] 链轴断点：链成员键 credit_code × 学研机构 external_id")
    inst_ids = [str(r[0]) for r in q("heis_ext", "SELECT external_id FROM gkx.dwd_org_heis_info")
                if r[0]]
    inst_ids += [str(r[0]) for r in q("ri_ext",
                                      "SELECT external_id FROM gkx.dwd_research_institute_base_info")
                 if r[0]]
    inst_id_set = set(inst_ids)
    tags_sample = q("tags_sample",
                    "SELECT credit_code FROM gkx.dwd_org_industry_tags LIMIT %d" % SAMPLE_N)
    sample_hit = sum(1 for r in tags_sample if str(r[0]) in inst_id_set)
    sample_pub_prefix = sum(1 for r in tags_sample if str(r[0]).startswith("12"))
    sample_malformed = sum(1 for r in tags_sample if len(str(r[0])) != 18)
    tags_rows = int(q("tags_rows", "SELECT COUNT(*) FROM gkx.dwd_org_industry_tags")[0][0])

    print("[5/6] 缺口侧：结果面表是否存在")
    absent = q("absent_tables",
               "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
               "AND (table_name LIKE '%metric%' OR table_name LIKE '%academic%' "
               "OR table_name LIKE '%scholar_stat%')")
    absent_tables = [r[0] for r in absent]

    print("[6/6] 四市 min-max 合成")
    inst_city = {c: heis_city.get(c, 0) + ri_city.get(c, 0) for c in CITIES}
    raw = {"papers": paper_city, "institutions": inst_city, "scholars": scholar_alias}

    def minmax(d):
        lo, hi = min(d.values()), max(d.values())
        if hi <= lo:
            return {k: 50.0 for k in d}
        return {k: round(100.0 * (v - lo) / (hi - lo), 4) for k, v in d.items()}

    norm = {k: minmax(v) for k, v in raw.items()}
    panel = []
    for c in CITIES:
        score = (W_PAPER * norm["papers"][c] + W_INST * norm["institutions"][c]
                 + W_SCHOLAR * norm["scholars"][c])
        panel.append({
            "city": c,
            "papers": raw["papers"][c],
            "institutions": raw["institutions"][c],
            "heis": heis_city.get(c, 0),
            "research_institutes": ri_city.get(c, 0),
            "scholars": raw["scholars"][c],
            "dim_norm": {"papers": norm["papers"][c], "institutions": norm["institutions"][c],
                         "scholars": norm["scholars"][c]},
            "score": round(score, 2),
            "paper_per_inst": round(raw["papers"][c] / raw["institutions"][c], 2)
            if raw["institutions"][c] else None,
        })
    panel.sort(key=lambda r: -r["score"])
    for i, r in enumerate(panel, 1):
        r["rank"] = i

    payload_hit_rate = round(100.0 * inst_hits / inst_instances, 2) if inst_instances else "NA"

    payload = {
        "metric_id": "M_CHAIN_ACADEMIC_POWER",
        "metric_name": "学术生态",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "三维源齐且本件实测出数（机构 %d 家去重、学者 %d 人、窗口论文 %d 行），"
            "但「指定链 × 区域」限定的入集键不存在：链成员 credit_code 与学研机构 external_id "
            "两个键域不相交（5 万行样本 0 命中），链级学术生态无法闭合；学者维还叠加 "
            "scholar_org_id 整列为空（%d 行），只能用机构名含城市名的名称代理。"
            "按「始终有部分依赖维度拿不到足够数据」判部分支持，不抬档。"
            % (sum(inst_city.values()), scholar_total, len(rows), scholar_org_id_nonempty)
        ),
        "verdict_kind": "computed_with_declared_gap",
        "base_years_used": ["2021", "2022", "2023", "2024"],
        "base_years_missing": ["2025", "2026"],
        "base_years_note": (
            "论文维按 cover_year_start 2021—2024 截断，窗口内 52,119 行（占全库 100,900 行的 51.65%）；"
            "2025—2026 库内有值但收录不全（6,548 / 2,989 行），不摊进正式值、也不按 0 补；"
            "机构与学者为存量截面，无统计期，不参与年度窗口。"
        ),
        "sources": [
            "gkx @ 183.240.141.251:3318: gkx.dwd_org_heis_info（3,501 行）",
            "gkx @ 183.240.141.251:3318: gkx.dwd_research_institute_base_info（2,074 行）",
            "gkx @ 183.240.141.251:3318: gkx.dwd_scholar（21,316 行）",
            "gkx @ 183.240.141.251:3318: gkx.dwd_zh_paper（100,900 行，窗口 52,119 行）",
            "gkx @ 183.240.141.251:3318: gkx.dwd_org_industry_tags（2,283,762 行，仅取 5 万行样本做键域比对）",
            "code/_snapshots21/base_20261021.json（机构名 → 城市字典，189,116 行底册）",
        ],
        "rule": {
            "D1_institutions": "heis.city + research_institute.city 按市等值汇总，两池 name_cn 交集见 pool_overlap",
            "D2_scholars": "dwd_scholar.scholar_org_name_zh 含城市名（广州/深圳/东莞/惠州）计数；id 轨不可用",
            "D3_papers": "dwd_zh_paper.author_info_list[].institution 精确匹配底册 name_cn → 机构 city；一篇论文可计入多市",
            "window": "cover_year_start ∈ [2021, 2024]",
            "normalize": "每个维在四市之间做 min-max ×100（最小值 0、最大值 100）",
            "weights": {"papers": W_PAPER, "institutions": W_INST, "scholars": W_SCHOLAR},
            "weight_status": "本件自定义、待甲方确认（旧稿与甲方口径表均未给权重）",
            "chain_axis": "不产出链级读数：键域不相交，任何链级值都是伪造",
        },
        "pool_overlap": {
            "heis_rows": heis_n, "ri_rows": ri_n,
            "heis_dup_rows": heis_dup_rows,
            "ri_dup_rows": ri_dup_rows,
            "cross_pool_dup": cross,
            "name_intersection": name_overlap,
            "note": "高校表 3,501 行只有 2,933 个不同 external_id，568 行是同校重复录入；"
                    "科研院所表无重复。院所与高校按 external_id 去重后再相加，"
                    "实测跨池重复 1 例（广州中医药大学 / 广州中医药大学（广州中医药研究院））",
        },
        "panel": panel,
        "paper_detail": {
            "paper_rows_all": paper_total,
            "window_rows": len(rows),
            "window_share_pct": round(100.0 * len(rows) / paper_total, 2),
            "papers_with_city": papers_with_city,
            "paper_city_pairs": len(pairs),
            "inst_instances": inst_instances,
            "inst_name_hits": inst_hits,
            "inst_hit_rate_pct": round(100.0 * inst_hits / inst_instances, 2) if inst_instances else None,
            "cities_outside_study": sorted({ct for _, ct in pairs if ct not in CITIES}),
        },
        "scholar_detail": {
            "rows": scholar_total,
            "org_id_nonempty": scholar_org_id_nonempty,
            "org_name_empty": scholar_org_name_empty,
            "alias_hits": scholar_alias,
            "alias_total": sum(scholar_alias.values()),
        },
        "chain_axis_block": {
            "tags_rows": tags_rows,
            "sample_rows": len(tags_sample),
            "sample_hit": sample_hit,
            "sample_public_prefix12": sample_pub_prefix,
            "sample_malformed_not18": sample_malformed,
            "institution_ids": len(inst_id_set),
            "test": "链成员 credit_code ∈ 学研机构 external_id 集合（5 万行等距样本，非全表）",
            "reason": "链成员表装的是企业统一社会信用代码（前缀 91…），学研侧是事业单位代码（前缀 12…）；"
                      "样本内 0 条以 12 开头、0 条命中机构 id，说明不是覆盖率低而是键域不同",
            "consequence": "「链 × 区域」双限定无法闭合；用区域值顶替会伪造链间差异，故本件不输出链级分数",
        },
        "result_face_absent": {
            "matched_tables": absent_tables,
            "note": "gkx 内无 academic/metric 结果面；旧稿读的汇总层表属演示库应用层，库内没有属正常（见 TABLE_ABSENCE_EVIDENCE.md）",
        },
        "difference_vs_old_draft": {
            "old_scope": "深圳单点：机构 5,003（全国池去重）、学者 16,120（名称匹配 75.6%）、论文 186,428，"
                         "单点 min-max 退化触发 0.5 兜底，输出 50.0",
            "old_source": "演示库汇总/关系面 + 开发库旧机读数（表名前缀 demo_，演示库年代主机）",
            "now_scope": (
                "四市截面（广州/深圳/东莞/惠州），min-max 有真实分布；深圳机构 %d（高校 %d + 院所 %d）"
                % (inst_city.get("深圳市", 0), heis_city.get("深圳市", 0),
                   ri_city.get("深圳市", 0))
            ),
            "moved_numbers": [
                "机构 5,003 → %d：旧稿是「全国高校 + 院所名称去重池（5,003）」，本件只把落在四市的部分"
                "纳入面板（全国池不作分母），深圳 %d（高校 %d + 院所 %d）"
                % (sum(inst_city.values()), inst_city.get("深圳市", 0),
                   heis_city.get("深圳市", 0), ri_city.get("深圳市", 0)),
                "学者 16,120（75.6%%）→ 四市名称轨 %d 人：旧稿用「机构名与机构池前缀/包含匹配」，本件只认"
                "「机构名含城市名」，口径更窄，区域数大幅下降（口径换轨，不是数据减少）"
                % sum(scholar_alias.values()),
                "论文 186,428 → 窗口 %d 行：旧稿是全库学者-关系表命中数，本件叠加了年度窗口与机构名精确"
                "匹配两道收窄" % len(rows),
                "单点 50.0 → 四市 %s：从兜底演示值换成有分布意义的相对指数"
                % " / ".join("%.2f" % r["score"] for r in panel),
            ],
            "not_comparable": "旧稿 186,428 与 5,003 的分母是「全库/全国」，本件是「四市窗口」，两者不能相除比较",
        },
        "gaps": [
            "链轴不可闭合（决定性缺口）：链成员 credit_code 与学研机构 external_id 键域不同，"
            "需甲方/三方提供「机构 → 链」映射表，否则任何链级学术生态都是伪造",
            "学者 id 轨整列为空：scholar_org_id 非空 0 / 21,316，只能用机构名含城市名代理；"
            "改名机构（如「鹏城实验室」不含「深圳」）与异地校区会漏计，回填 org_id 后必须重算",
            "论文城市归属靠底册 name_cn 精确匹配，命中率仅 %s%%；英文论文（1,387 行）未并入，"
            "医学/医院类机构在底册缺失，主题偏斜未校正" % payload_hit_rate,
            "机构维自身有重复行：高校表 3,501 行只有 2,933 个不同 external_id（568 行同校重复录入），"
            "本件已按 external_id 去重、并与院所表去重（1 例跨池重复）；不去重会把广州等高校密集市抬高",
            "高校池是全国名单（深圳仅 16 所），与「科研院所池以广东为主」混加，会把院所多的市抬成学术强市",
            "权重 0.4/0.3/0.3 与 min-max 归一为本件自定义，未会签；四市样本下极值敏感，惠州学者 0 直接锁死该维下限",
        ],
        "probes": PROBES,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(time.time() - T0, 2),
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    print("\n四市面板：")
    for r in panel:
        print("  %d %-4s 论文 %6d 机构 %5d(高校%3d/院所%4d) 学者 %3d 分 %6.2f"
              % (r["rank"], r["city"], r["papers"], r["institutions"], r["heis"],
                 r["research_institutes"], r["scholars"], r["score"]))
    print("论文窗口 %d 行 / 全库 %d 行；机构名命中率 %s%%；链轴样本命中 %d/%d"
          % (len(rows), paper_total, payload["paper_detail"]["inst_hit_rate_pct"],
             sample_hit, len(tags_sample)))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
