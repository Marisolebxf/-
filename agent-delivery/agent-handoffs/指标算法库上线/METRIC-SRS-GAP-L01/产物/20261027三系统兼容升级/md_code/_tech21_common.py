#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TECH 家族 133/134/136/137/138 共用离线取数层（20261021 批）。

铁律：本模块零 SQL、零 demo 依赖，只读 _snapshots21 / _snapshots_gkx21 下的授权缓存。
专利口径：
  - 全国 IPC4×年：patent_ipc4_year_20261021.json -> [ipc4, year, 件数, 机构数]
  - 全国 IPC4×申请人：patent_ipc4_by_name_20261021.json -> [ipc4, 申请人, 件数]
  - 四城×年×IPC4：patent_scan_20261021.pkl 的 ipc_pn -> (city, year, ipc4) -> pn 集合
  - 深圳申请人：sz_patent_city_name_gkx.json（groups）+ innovative_base 名称→区
  - 申请人件数/授权数：star_applicant_agg_gkx.json 的 agg[nm] = [件数, 授权数]
"""
from __future__ import annotations

import collections
import json
import math
import pickle
import statistics
from pathlib import Path

CODE = Path(__file__).resolve().parent
SNAP = CODE / "_snapshots21"
SNAPG = CODE / "_snapshots_gkx21"

# 深圳 20+8 产业 → IPC4 前缀（深府〔2022〕1 号 + 20261016 批 IPC 锚点，与 20261020 批一致）
SZ208_MAP = {
    "网络与通信": ["H04L", "H04W", "H04B", "H04N"],
    "半导体与集成电路": ["H01L", "G05F", "H05K"],
    "超高清视频显示": ["H01J", "G09F", "H05B"],
    "智能终端": ["G06F", "H04M", "G06C"],
    "智能传感器": ["G01D", "G01S", "H01L"],
    "软件与信息服务": ["G06F", "G06Q", "G06N"],
    "智能机器人": ["B25J", "G05B"],
    "新能源": ["H01M", "H02J", "F03D", "C10L"],
    "智能网联汽车": ["B60W", "B60R", "B60L"],
    "新材料": ["C01B", "C08L", "C22C", "C09C"],
    "高端医疗器械": ["A61B", "A61M", "G16H"],
    "生物医药": ["A61K", "C07K", "C12N"],
    "大健康": ["A61K", "A23L"],
    "海洋产业": ["B63B", "E02B"],
    "精密仪器设备": ["G01N", "G01R", "G12B"],
    "数字创意": ["G06T", "H04N"],
    "安全节能环保": ["F24F", "B09B", "F23G"],
    "工业母机": ["B23Q", "B23B"],
    "激光与增材制造": ["B23K", "B22F", "B29C"],
    "现代时尚": ["A41D", "A47G", "G04B"],
    "合成生物": ["C12N", "C12P"],
    "区块链": ["G06Q", "H04L"],
    "细胞与基因": ["C12N", "C07K"],
    "空天技术": ["B64C", "B64G"],
    "脑科学与类脑智能": ["G06N", "A61B"],
    "深地深海": ["E21B", "B63C"],
    "可见光通信与光计算": ["H04B", "G02F"],
    "量子信息": ["G01J", "G02F", "B82Y"],
}

# 常用 IPC4 语义标签（仅用于正文可读性，不参与计算）
IPC_LABEL = {
    "G06F": "电数字数据处理", "H04W": "无线通信", "H04L": "数字信息传输",
    "H05K": "印刷电路/电设备结构", "H01M": "电池/燃料电池", "H04N": "图像通信",
    "G01N": "物理/化学分析", "G06Q": "行政与商业数据处理", "A24F": "吸烟用品",
    "H01R": "电连接器", "G01R": "电性能测量", "H02J": "供电/配电",
    "H01L": "半导体器件", "G06T": "图像数据处理", "G06V": "图像识别",
    "C12N": "微生物/酶/基因工程", "A61B": "诊断/外科器械", "B29C": "塑料成型",
    "H04B": "传输系统", "G16H": "医疗信息学", "G01S": "无线电定位",
    "H10H": "半导体发光器件（新版 IPC）", "H10D": "半导体器件（新版 IPC）",
    "G06K": "数据识别", "F21S": "非便携照明", "B60S": "车辆维护设备",
    "G01J": "红外/光谱测量", "G07F": "投币/自助装置", "B64C": "飞行器",
    "G09F": "显示/广告装置", "A47L": "家居清洁", "A47B": "家具", "B32B": "层状产品",
    "G02F": "光学控制器件", "H04M": "电话通信", "B60S": "车辆维护", "B31B": "纸品成型",
    "E01F": "道路附属设施", "B25H": "车间工具/工作台", "B22D": "金属铸造",
    "B60G": "车辆悬架", "B60T": "车辆制动", "G02C": "眼镜/光学配件", "H01J": "电子管/放电灯",
    "H10K": "有机半导体器件", "H10F": "光敏半导体器件", "H10W": "半导体封装",
    "H10P": "半导体工艺", "B64U": "无人机", "F21K": "光源", "B64D": "飞行器设备",
    "A41D": "服装", "B65F": "垃圾贮运", "B28C": "黏土/水泥制备", "C14B": "皮革加工",
    "F03B": "水力机械", "A47F": "商店陈列", "B65C": "贴标签", "B65B": "包装",
    "B41F": "印刷机械", "G08G": "交通控制", "B29B": "塑料预处理", "G04B": "钟表",
    "B60L": "电动车辆", "H02S": "光伏系统", "G11C": "存储器", "G11B": "信息存储",
    "G09G": "显示控制", "H04Q": "选择开关", "H04J": "复用通信", "G21C": "核反应堆",
    "A61L": "消毒/材料处理", "H01Q": "天线", "G03B": "摄影设备", "B01F": "混合",
    "A01G": "园艺", "H02B": "电力配电盘", "F16M": "机架/支承", "H04R": "扬声器",
}

# 2021—2026 是 dwd_patent 的全部年份；2017—2020 为零行（DATA_FACTS §3.16）
PATENT_YEARS_ALL = [2021, 2022, 2023, 2024, 2025, 2026]
COMPLETE_YEARS = [2021, 2022, 2023, 2024]
MISSING_BASE_YEARS = [2017, 2018, 2019, 2020]


def _load(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_ipc_year():
    """返回 ({(ipc4, year): (件数, 机构数)}, {year: 总件数}, 域集合)。"""
    data = _load(SNAP / "patent_ipc4_year_20261021.json")
    cell, by_year, domains = {}, collections.Counter(), set()
    for ipc4, year, n, n_org in data:
        cell[(ipc4, int(year))] = (int(n), int(n_org))
        by_year[int(year)] += int(n)
        domains.add(ipc4)
    return cell, dict(by_year), domains


def load_city_ipc():
    """四城×年×IPC4 件数。返回 ({(city, year): Counter(ipc4 -> 件数)}, 元数据)。"""
    with open(SNAP / "patent_scan_20261021.pkl", "rb") as f:
        raw = pickle.load(f)
    out = collections.defaultdict(collections.Counter)
    for (city, year, ipc4), pns in raw["ipc_pn"].items():
        out[(city, int(year))][ipc4] += len(pns)
    meta = {
        "source": "code/_snapshots21/patent_scan_20261021.pkl（83913 扫描，2021—2024 四城）",
        "row_total": raw.get("row_total"),
        "groups": len(raw["ipc_pn"]),
        "years": sorted({y for (_, y) in out}),
    }
    return out, meta


def load_sz_ipc_year():
    """深圳 IPC4×年件数。返回 ({(ipc4, year): 件数}, {year: 总件数})。"""
    city_ipc, _ = load_city_ipc()
    cell, year_total = {}, collections.Counter()
    for (city, year), cnt in city_ipc.items():
        if city != "深圳":
            continue
        for ipc4, n in cnt.items():
            cell[(ipc4, year)] = cell.get((ipc4, year), 0) + n
            year_total[year] += n
    return cell, dict(year_total)


def load_sz_name_dom():
    """深圳申请人×IPC4 件数（全期）。返回 {ipc4: Counter(申请人 -> 件数)}。

    桥：以 sz_patent_city_name 的深圳申请人名集合过滤全国 name×domain 聚合。
    与 133 区级矩阵同一桥，覆盖深圳有 IPC 专利的 99.996%。
    """
    names = set(load_sz_names()[0])
    out = collections.defaultdict(collections.Counter)
    for ipc4, nm, n in load_ipc_name():
        if nm in names:
            out[ipc4][nm] += int(n)
    return out


def load_star_agg():
    """申请人全期 [申请件数, 授权件数]。"""
    return _load(SNAP / "star_applicant_agg_gkx.json")["agg"]


def load_ipc_name():
    """[(ipc4, 申请人, 件数)]，全表 2,420,915 件有 IPC 的聚合。"""
    return _load(SNAP / "patent_ipc4_by_name_20261021.json")


def load_sz_names():
    """深圳申请人名集合 + 每名件数（来自 sz_patent_city_name_gkx groups）。"""
    groups = _load(SNAPG / "sz_patent_city_name_gkx.json")["groups"]
    names, counts, invention, ipc_empty = {}, {}, {}, {}
    for r in groups:
        if r.get("city") != "深圳市":
            continue
        nm = r["nm"]
        names[nm] = int(r.get("n", 0))
        counts[nm] = int(r.get("n", 0))
        invention[nm] = int(r.get("invention", 0))
        ipc_empty[nm] = int(r.get("ipc_empty", 0))
    return names, counts, invention, ipc_empty


def load_sz_area():
    """深圳 189,116 底册中的名称→区；同名多区返回 None（本批实测 0 例）。"""
    rows = _load(SNAP / "innov_base_20261021.json")
    area_of = {}
    conflicts = collections.defaultdict(set)
    for r in rows:
        if r.get("city") != "深圳市":
            continue
        a = (r.get("area") or "").strip()
        if not a or a.upper() == "NULL":
            continue
        conflicts[r["name_cn"]].add(a)
    for nm, areas in conflicts.items():
        if len(areas) == 1:
            area_of[nm] = next(iter(areas))
    return area_of, {"sz_orgs_named": len(conflicts), "ambiguous_names": sum(1 for a in conflicts.values() if len(a) > 1)}


def load_star_agg():
    d = _load(SNAP / "star_applicant_agg_gkx.json")
    return d["agg"], {"table_rows": d.get("table_rows"), "names": d.get("names")}


def load_bridge_and_tree():
    bridge = _load(SNAP / "bridge_20261021.json")
    tree = _load(SNAP / "chain_tree_20261021.json")
    code2name = {r["industry_code"]: r["industry_name"] for r in tree}
    return bridge, code2name, {"bridge_rows": len(bridge), "tree_nodes": len(tree)}


def load_tagmap():
    return _load(SNAPG / "sz_patent_tagmap_gkx.json")


def hhi(counter) -> float:
    vals = list(counter.values()) if isinstance(counter, dict) else list(counter)
    total = sum(vals)
    if not total:
        return 0.0
    return round(sum((v / total) ** 2 for v in vals) * 10000, 2)


def share(counter, k) -> float:
    total = sum(counter.values()) if isinstance(counter, dict) else sum(counter)
    return round(counter.get(k, 0) / total, 4) if total else 0.0


def zscores(values):
    mu = statistics.mean(values)
    sd = statistics.pstdev(values) or 1.0
    return [(v - mu) / sd for v in values], mu, sd


def pct(x):
    return round(x * 100, 2)


def label(code):
    return IPC_LABEL.get(code, "")


def write_out(metric_id, payload):
    out = CODE / f"{metric_id}_out.json"
    payload.setdefault("metric_id", metric_id)
    payload.setdefault("generated_at", "2026-10-22")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print("done ->", out)
    return out
