#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TECH 139/140/104/105/STRUCT 共用离线口径层（20261022 批）。

铁律：
  1. 本模块零 SQL、零 demo 依赖，只读 code/_snapshots21 与 code/_snapshots_gkx21 的授权缓存。
  2. 专利口径固定为「申请年 2021—2024、按 pn 去重、IPC 主分类前 4 位」；
     深圳 = 申请人名称经企业底册归到深圳市；全国 = 面板全量（含深圳）。
  3. 2017—2020 在 dwd_patent 为零行（DATA_FACTS §3.16），任何基期只允许 2021。

主要输入：
  _snapshots21/patent_panel_innov_20261021.json  全国 IPC4×年、申请人×年
  _snapshots21/patent_scan_20261021.pkl          六城×年×IPC4 的 pn 集合
  _snapshots21/patent_ipc4_by_name_20261021.json IPC4×申请人 件数
  _snapshots21/star_applicant_agg_gkx.json       申请人 [件数, 授权数]
  _snapshots21/star_base_rows_gkx.json           企业底册（含行业二级）
  _snapshots_gkx21/sz_patent_city_name_gkx.json  申请人→城市 + 件数/发明/价值
  _snapshots21/policy_base_20261021.json         政策存量 20,000 条
  _snapshots21/tech_tags_20261021.json           机构技术标签（org_id → tags）
"""
from __future__ import annotations

import collections
import json
import math
import statistics
from pathlib import Path

CODE = Path(__file__).resolve().parent
SNAP = CODE / "_snapshots21"
SNAPG = CODE / "_snapshots_gkx21"

COMPLETE_YEARS = [2021, 2022, 2023, 2024]
MISSING_BASE_YEARS = [2017, 2018, 2019, 2020]

# 深圳「20+8」产业集群 → IPC4 前缀（深府〔2022〕1 号 + 20261016 批 IPC 锚点）。
# 同一 IPC4 出现在多个产业时，按本字典的书写顺序取第一个（确定性归属），
# 因此产业口径是「归属次」而不是「并集件数」；未覆盖的 IPC4 单列，不摊进产业。
SZ208_MAP = {
    "网络与通信": ["H04L", "H04W", "H04B", "H04N", "H04R", "H04Q", "H04J"],
    "半导体与集成电路": ["H01L", "H05K", "G05F", "H03K", "H01G"],
    "超高清视频显示": ["H01J", "G09F", "H05B", "G02B", "G09G"],
    "智能终端": ["G06F", "H04M", "G06C", "H01R", "G06V"],
    "智能传感器": ["G01D", "G01S", "G01R", "G01J"],
    "软件与信息服务": ["G06Q", "G06N", "G06T", "G06K", "G11B", "G11C"],
    "智能机器人": ["B25J", "G05B", "B65G"],
    "新能源": ["H01M", "H02J", "F03D", "C10L", "H02S"],
    "智能网联汽车": ["B60W", "B60R", "B60L", "B60G", "B60T", "B60J"],
    "新材料": ["C01B", "C08L", "C22C", "C09C", "B32B"],
    "高端医疗器械": ["A61B", "A61M", "G16H", "A61N"],
    "生物医药": ["A61K", "C07K", "C12N", "C12Q"],
    "大健康": ["A23L", "A61H"],
    "海洋产业": ["B63B", "E02B", "B63C"],
    "精密仪器设备": ["G01N", "G12B", "G02C", "G03B"],
    "数字创意": ["G06T", "H04N", "G09F"],
    "安全节能环保": ["F24F", "B09B", "F23G", "B01D", "F21S"],
    "工业母机": ["B23Q", "B23B", "B23C", "B24B", "B26D", "F16M"],
    "激光与增材制造": ["B23K", "B22F", "B29C", "B29B"],
    "现代时尚": ["A41D", "A47G", "G04B", "A47B"],
    "合成生物": ["C12N", "C12P", "C07H"],
    "区块链": ["G06Q", "H04L", "G06F"],
    "细胞与基因": ["C12N", "C07K", "C12Q"],
    "空天技术": ["B64C", "B64G", "B64U", "B64D"],
    "脑科学与类脑智能": ["G06N", "A61B", "A61F"],
    "深地深海": ["E21B", "B63C"],
    "可见光通信与光计算": ["G02F", "B82Y", "G02B"],
    "量子信息": ["G01J", "G02F", "B82Y", "G06N"],
}

# 产业 → 政策检索词（推测口径，用于在深圳市政策全文中做关键词命中；非甲方词典）
IND_KW = {
    "网络与通信": ["通信", "5G", "光通信", "网络", "宽带"],
    "半导体与集成电路": ["半导体", "集成电路", "芯片", "晶圆"],
    "超高清视频显示": ["超高清", "显示", "面板", "视频"],
    "智能终端": ["智能终端", "手机", "终端", "消费电子"],
    "智能传感器": ["传感器", "智能传感", "感知"],
    "软件与信息服务": ["软件", "信息服务", "人工智能", "大数据", "云计算"],
    "智能机器人": ["机器人", "智能装备", "工业机器"],
    "新能源": ["新能源", "电池", "储能", "光伏", "风电"],
    "智能网联汽车": ["智能网联", "新能源汽车", "自动驾驶", "汽车"],
    "新材料": ["新材料", "材料", "合金", "高分子"],
    "高端医疗器械": ["医疗器械", "医疗设备", "诊断", "影像"],
    "生物医药": ["生物医药", "医药", "生物药", "创新药"],
    "大健康": ["大健康", "健康", "食品", "养老"],
    "海洋产业": ["海洋", "海工", "港口", "航运"],
    "精密仪器设备": ["精密仪器", "仪器", "检测设备", "测量"],
    "数字创意": ["数字创意", "文化创意", "数字内容", "电竞"],
    "安全节能环保": ["节能", "环保", "安全", "绿色", "低碳"],
    "工业母机": ["工业母机", "机床", "数控", "基础零部件"],
    "激光与增材制造": ["激光", "增材制造", "3D打印", "打印"],
    "现代时尚": ["时尚", "服装", "家具", "钟表", "黄金珠宝"],
    "合成生物": ["合成生物", "生物制造", "生物合成"],
    "区块链": ["区块链", "分布式账本", "web3"],
    "细胞与基因": ["细胞", "基因", "干细胞", "基因治疗"],
    "空天技术": ["空天", "航空航天", "卫星", "无人机"],
    "脑科学与类脑智能": ["脑科学", "类脑", "脑机", "智能"],
    "深地深海": ["深地", "深海", "油气", "勘探"],
    "可见光通信与光计算": ["光通信", "光计算", "光电"],
    "量子信息": ["量子", "量子计算", "量子通信"],
}

# IPC 部 → 中文名（仅用于正文可读性）
IPC_SECTION = {
    "A": "人类生活必需", "B": "作业运输", "C": "化学冶金",
    "D": "纺织造纸", "E": "固定建筑", "F": "机械工程",
    "G": "物理", "H": "电学",
}


def _load(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_nat_ipc():
    """全国 IPC4×年 → ({(ipc4, year): 件数}, {year: 总件数})，窗口 2021—2024。"""
    panel = _load(SNAP / "patent_panel_innov_20261021.json")
    cell, by_year = {}, collections.Counter()
    for k, n in panel["ipc_year"].items():
        y_s, ipc = k.split("|", 1)
        y = int(y_s)
        if y in COMPLETE_YEARS:
            cell[(ipc, y)] = int(n)
            by_year[y] += int(n)
    return cell, dict(by_year)


def load_sz_ipc():
    """深圳 IPC4×年 → ({(ipc4, year): 件数}, {year: 总件数})，窗口 2021—2024。"""
    import pickle

    with open(SNAP / "patent_scan_20261021.pkl", "rb") as f:
        raw = pickle.load(f)
    cell, by_year = {}, collections.Counter()
    for (city, y, ipc), pns in raw["ipc_pn"].items():
        if city != "深圳" or int(y) not in COMPLETE_YEARS:
            continue
        n = len(pns)
        cell[(ipc, int(y))] = n
        by_year[int(y)] += n
    return cell, dict(by_year)


def load_sz_groups():
    """深圳申请人清单：名称、全期件数、发明件数、价值填充。"""
    groups = _load(SNAPG / "sz_patent_city_name_gkx.json")["groups"]
    return [g for g in groups if g.get("city") == "深圳市" and g.get("nm")]


def load_base_rows():
    """底册 189,116 行：org_id/name/province/city/area/industry_l1/industry_l2/org_type。"""
    rows = _load(SNAP / "star_base_rows_gkx.json")
    by_name = {}
    for org_id, name, prov, city, area, ind1, ind2, otype in rows:
        by_name.setdefault(name, {
            "org_id": org_id, "name": name, "province": prov, "city": city,
            "area": area, "industry_l1": ind1, "industry_l2": ind2, "org_type": otype,
        })
    return by_name


def load_star_agg():
    d = _load(SNAP / "star_applicant_agg_gkx.json")
    return d["agg"], {"table_rows": d.get("table_rows"), "names": d.get("names")}


def load_ipc_name():
    return _load(SNAP / "patent_ipc4_by_name_20261021.json")


def load_panel_app_year():
    panel = _load(SNAP / "patent_panel_innov_20261021.json")
    out = {}
    for k, n in panel["app_year"].items():
        y_s, nm = k.split("|", 1)
        out[(int(y_s), nm)] = int(n)
    return out


def load_policies():
    return _load(SNAP / "policy_base_20261021.json")


def load_policy_text():
    """id → (title, content)；content 缺行时回退标题。"""
    out = {}
    for row in _load(SNAP / "policy_content_20261021.json"):
        if len(row) >= 3:
            out[str(row[0])] = (row[1] or "", row[2] or "")
    return out


def load_tech_tags():
    return _load(SNAP / "tech_tags_20261021.json")


def ipc_industry(ipc4: str):
    """IPC4 → 产业（第一个命中）；未覆盖返回 None。"""
    for ind, prefixes in SZ208_MAP.items():
        if ipc4 in prefixes:
            return ind
    return None


def industry_prefixes(ind: str):
    return list(SZ208_MAP.get(ind, []))


def industry_policy_counts():
    """深圳市政策全文中，各产业关键词命中条数（存量全表，不按年截断）。"""
    policies = [p for p in load_policies() if p.get("city") == "深圳市"]
    texts = load_policy_text()
    out = collections.Counter()
    for p in policies:
        title, content = texts.get(str(p.get("id")), (p.get("title") or "", ""))
        blob = (title + " " + content).lower()
        for ind, kws in IND_KW.items():
            if any(kw.lower() in blob for kw in kws):
                out[ind] += 1
    return dict(out), len(policies)


def is_enterprise_name(name: str) -> bool:
    """按名称粗分企业主体（用于高潜力企业榜，机构/高校单列）。"""
    if any(x in name for x in ("大学", "学院", "研究院", "研究所", "研究中心", "实验室", "医院")):
        return False
    return any(x in name for x in ("公司", "集团", "厂", "企业", "合伙"))


def zscores(values):
    mu = statistics.mean(values)
    sd = statistics.pstdev(values) or 1.0
    return [(v - mu) / sd for v in values], mu, sd


def minmax(values):
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.5 for _ in values]
    return [(v - lo) / (hi - lo) for v in values]


def base_year_block(used, missing, note):
    return {"base_years_used": used, "base_years_missing": missing, "base_years_note": note}


def write_out(metric_id, payload):
    out = CODE / f"{metric_id}_out.json"
    payload.setdefault("metric_id", metric_id)
    payload.setdefault("generated_at", "2026-10-22")
    payload.setdefault("main_db", "gkx @ 183.240.141.251:3318 (gkx_reader_zp, read-only)")
    payload.setdefault("sql_count", 0)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print("done ->", out)
    return out
