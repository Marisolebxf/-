#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TALENT 首批（5 件）公共计算库 —— 只读本地快照，零 DB。

数据面（全部来自 `code/_snapshots21/`）：
  probe_a26_20261022.json        scholar_dump：21,316 名学者主档（A-26 批窄列落盘）
  probe_talent21_20261022.json   本批探针：履历 57,117 / 学历 43,766 / 研究方向 20,030 /
                                 高校名录 3,501 / 院士 112 / 深圳在任活跃年 29
  base_20261021.json             企业底册 189,116 行（name → 省/市，机构属地兜底）
  patent_inventor_counts_gkx.json 发明人姓名 → 件数（403,743 名；件数合计 2,939,851
                                 ≈ gkx.dwd_patent 行数 2,939,895，差 44 为发明人字段空值）
  star_applicant_agg_gkx.json    申请人聚合 169,226 名（[件数, 授权数]）

铁律：
  1. 不连库、不发 SQL；专利侧一条 SQL 都不发（本模块只读 cache）。
  2. 发明人计数是**姓名精确匹配**，先按「同名多人」判缺测，再给上界值；不做任何「补 0」。
  3. 归一统一 log1p → 池内 min-max；缺维按剩余权重归一并输出 dims_available。
"""
from __future__ import annotations

import json
import math
import re
import statistics
from pathlib import Path

HERE = Path(__file__).parent
SNAP = HERE / "_snapshots21"

_C: dict[str, object] = {}


def _load(name: str):
    if name not in _C:
        _C[name] = json.loads((SNAP / name).read_text(encoding="utf-8"))
    return _C[name]


# ------------------------------------------------------------------ 统计工具


def pctl(vals, q: float):
    if not vals:
        return None
    s = sorted(vals)
    k = (len(s) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    if lo == hi:
        return round(s[int(k)], 4)
    return round(s[lo] + (s[hi] - s[lo]) * (k - lo), 4)


def st(vals) -> dict:
    if not vals:
        return {}
    return {"n": len(vals), "min": round(min(vals), 4), "max": round(max(vals), 4),
            "mean": round(statistics.mean(vals), 4), "median": round(statistics.median(vals), 4),
            "p10": pctl(vals, 0.10), "p90": pctl(vals, 0.90), "p99": pctl(vals, 0.99)}


def _ranks(v: list[float]) -> list[float]:
    order = sorted(range(len(v)), key=lambda i: v[i])
    out = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[order[k]] = avg
        i = j + 1
    return out


def spearman(a, b):
    if len(a) < 3:
        return None
    ra, rb = _ranks(a), _ranks(b)
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return round(num / den, 4) if den else None


def log_minmax(vals: list[float]) -> list[float]:
    """log1p 后在池内 min-max 到 0—1；全同值时返回 0.5（不制造区分度）。"""
    if not vals:
        return []
    lg = [math.log1p(max(0.0, v)) for v in vals]
    lo, hi = min(lg), max(lg)
    if hi - lo < 1e-12:
        return [0.5] * len(vals)
    return [(x - lo) / (hi - lo) for x in lg]


def pct_rank(vals: list[float]) -> list[float]:
    r = _ranks(vals)
    n = len(vals)
    if n <= 1:
        return [50.0] * n
    return [round(100 * (x - 1) / (n - 1), 2) for x in r]


def write_out(metric: str, payload: dict) -> Path:
    out = HERE / f"{metric}_out.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("wrote", out.name, f"({out.stat().st_size} bytes)")
    return out


def base_year_block(used: list[int], missing: list[int], note: str) -> dict:
    """§3.16 强制字段：分母只允许用库内真实存在的年份。"""
    return {"base_years_used": used, "base_years_missing": missing, "note": note}


# ------------------------------------------------------------------ 学者主档


def scholars() -> list[dict]:
    """21,316 名学者。三列 100% 非空（本批复核：h/citation/paper 均 21,316 有值）。"""
    if "sch" not in _C:
        rows = _load("probe_a26_20261022.json")["scholar_dump"]["rows"]
        _C["sch"] = [{
            "sid": r[0], "name": (r[1] or "").strip(), "org": (r[2] or "").strip(),
            "paper": int(float(r[3] or 0)), "cite": int(float(r[4] or 0)),
            "h": int(float(r[5] or 0)), "status": r[6],
        } for r in rows]
    return _C["sch"]  # type: ignore[return-value]


def talent() -> dict:
    if "tal" not in _C:
        _C["tal"] = _load("probe_talent21_20261022.json")
    return _C["tal"]  # type: ignore[return-value]


_YR = re.compile(r"(\d{4})")


def year_of(s: str | None):
    m = _YR.search(s or "")
    return int(m.group(1)) if m else None


def work() -> list[dict]:
    """57,117 段履历，覆盖 20,028 名学者（93.96%）。org 为空 11,656 行（20.4%）。"""
    if "wx" not in _C:
        rows = talent()["work_exp"]["rows"]
        _C["wx"] = [{
            "sid": r[0], "org": (r[1] or "").strip(),
            "y0": year_of(r[2]), "y1": year_of(r[3]),
            "cur": str(r[4] or "").strip() == "1", "pos": (r[5] or "").strip(),
        } for r in rows]
    return _C["wx"]  # type: ignore[return-value]


def edu() -> list[dict]:
    """43,766 段学历，覆盖 20,025 名学者。degree_zh 空 9,825 行，degree_en 空 2,223 行。"""
    if "ed" not in _C:
        rows = talent()["edu"]["rows"]
        _C["ed"] = [{
            "sid": r[0], "org": (r[1] or "").strip(),
            "deg_zh": (r[2] or "").strip(), "deg_en": (r[3] or "").strip(),
            "y0": year_of(r[4]), "y1": year_of(r[5]), "major": (r[6] or "").strip(),
        } for r in rows]
    return _C["ed"]  # type: ignore[return-value]


def research() -> dict[str, list[str]]:
    """scholar_id → 研究方向标签列表（20,030 行、19,514 行有值；展开后 97,249 个去重标签）。"""
    if "rd" not in _C:
        d: dict[str, list[str]] = {}
        for sid, fields in talent()["research"]["rows"]:
            toks = [t.strip() for t in re.split(r"[;；]+", fields or "") if t.strip()]
            if toks:
                d[sid] = toks
        _C["rd"] = d
    return _C["rd"]  # type: ignore[return-value]


def academicians() -> set[str]:
    if "acad" not in _C:
        _C["acad"] = {r[0] for r in talent()["academician"]["rows"]}
    return _C["acad"]  # type: ignore[return-value]


# ------------------------------------------------------------------ 机构属地


CITY_PROV = {
    "北京": "北京市", "上海": "上海市", "天津": "天津市", "重庆": "重庆市",
    "广州": "广东省", "深圳": "广东省", "东莞": "广东省", "惠州": "广东省", "佛山": "广东省",
    "珠海": "广东省", "中山": "广东省", "江门": "广东省", "肇庆": "广东省",
    "杭州": "浙江省", "宁波": "浙江省", "温州": "浙江省",
    "南京": "江苏省", "苏州": "江苏省", "无锡": "江苏省", "徐州": "江苏省", "常州": "江苏省",
    "武汉": "湖北省", "长沙": "湖南省", "成都": "四川省", "西安": "陕西省",
    "合肥": "安徽省", "济南": "山东省", "青岛": "山东省", "厦门": "福建省", "福州": "福建省",
    "大连": "辽宁省", "沈阳": "辽宁省", "哈尔滨": "黑龙江省", "长春": "吉林省",
    "郑州": "河南省", "南昌": "江西省", "昆明": "云南省", "贵阳": "贵州省",
    "兰州": "甘肃省", "太原": "山西省", "石家庄": "河北省", "南宁": "广西",
    "海口": "海南省", "银川": "宁夏", "西宁": "青海省", "乌鲁木齐": "新疆",
    "呼和浩特": "内蒙古", "拉萨": "西藏",
}

FOREIGN_CN = [
    "美国", "英国", "日本", "德国", "法国", "加拿大", "澳大利亚", "新加坡", "韩国", "荷兰",
    "瑞典", "瑞士", "意大利", "西班牙", "比利时", "丹麦", "挪威", "芬兰", "奥地利", "以色列",
    "印度", "巴西", "俄罗斯", "马来西亚", "泰国", "越南", "新西兰", "爱尔兰", "波兰", "葡萄牙",
    "捷克", "土耳其", "南非", "墨西哥", "阿根廷", "智利", "沙特", "阿联酋", "伊朗", "埃及",
    "巴基斯坦", "孟加拉", "乌克兰", "希腊", "匈牙利", "罗马尼亚", "印度尼西亚", "菲律宾",
    "香港", "澳门", "台湾",
]
FOREIGN_EN = [
    "USA", "United States", "U.S.A", "America", "UK", "U.K.", "United Kingdom", "England",
    "Scotland", "Japan", "Germany", "France", "Canada", "Australia", "Singapore", "Korea",
    "Netherlands", "Sweden", "Switzerland", "Italy", "Spain", "Belgium", "Denmark", "Norway",
    "Finland", "Austria", "Israel", "India", "Brazil", "Russia", "Malaysia", "Thailand",
    "Vietnam", "New Zealand", "Ireland", "Poland", "Portugal", "Czech", "Turkey", "South Africa",
    "Mexico", "Argentina", "Chile", "Saudi", "UAE", "Iran", "Egypt", "Pakistan", "Bangladesh",
    "Ukraine", "Greece", "Hungary", "Romania", "Indonesia", "Philippines", "Hong Kong", "Taiwan",
]


def is_foreign(s: str) -> bool:
    if not s:
        return False
    for t in FOREIGN_CN:
        if t in s:
            return True
    low = s.lower()
    return any(t.lower() in low for t in FOREIGN_EN)


def _loc_maps():
    if "loc" not in _C:
        base = _load("base_20261021.json")          # [org_id, credit, name, province, city, year]
        bmap = {r[2]: (r[3] or "", r[4] or "") for r in base if r[2]}
        hmap = {r[0]: (r[1] or "", r[2] or "") for r in talent()["heis"]["rows"] if r[0]}
        _C["loc"] = (bmap, hmap)
    return _C["loc"]  # type: ignore[tuple]


def loc(org: str) -> tuple[str, str, str]:
    """机构名 → (省, 市, 归属方式)。顺序：高校名录精确 → 底册精确 → 高校名录前缀 →
    底册前缀 → 城市关键词 → 海外 → 未归属。高校名录（3,501 所）覆盖 75.2% 学者，
    是企业底册（深圳占 99.8%）在学术场景下的必要前置。"""
    if not org:
        return ("未填", "未填", "empty")
    bmap, hmap = _loc_maps()
    if org in hmap:
        return (hmap[org][0], hmap[org][1], "heis_exact")
    if org in bmap:
        return (bmap[org][0], bmap[org][1], "base_exact")
    for L in range(min(len(org), 30), 3, -1):
        if org[:L] in hmap:
            return (hmap[org[:L]][0], hmap[org[:L]][1], "heis_prefix")
    for L in range(min(len(org), 30), 3, -1):
        if org[:L] in bmap:
            return (bmap[org[:L]][0], bmap[org[:L]][1], "base_prefix")
    for c, p in CITY_PROV.items():
        if c in org:
            return (p, c + "市", "city_kw")
    if is_foreign(org):
        return ("海外", "海外", "foreign")
    return ("未归属", "未归属", "unmatched")


def is_sz(org: str) -> bool:
    return "深圳" in (org or "")


# ------------------------------------------------------------------ 专利（姓名匹配）


def inventor_counts() -> dict[str, int]:
    if "inv" not in _C:
        _C["inv"] = _load("patent_inventor_counts_gkx.json")["counts"]
    return _C["inv"]  # type: ignore[return-value]


def applicant_agg() -> dict[str, list[int]]:
    if "agg" not in _C:
        _C["agg"] = _load("star_applicant_agg_gkx.json")["agg"]
    return _C["agg"]  # type: ignore[return-value]


def name_dup() -> dict[str, int]:
    """学者池内同名人数（1,006 个姓名出现 ≥2 次，涉及 3,558 条记录）。"""
    if "dup" not in _C:
        d: dict[str, int] = {}
        for s in scholars():
            if s["name"]:
                d[s["name"]] = d.get(s["name"], 0) + 1
        _C["dup"] = d
    return _C["dup"]  # type: ignore[return-value]


def patent_of(s: dict) -> tuple[int | None, str]:
    """发明人件数：姓名唯一**且**姓名不少于 3 字才给值，否则判缺测（不补 0）。

    两条硬约束都来自实测：① 池内同名 1,006 个姓名、3,558 条记录，无法判定件数归属；
    ② 两字姓名（王雷 630 件、陈军 498 件）在 40 万发明人姓名里重名概率过高，纯姓名匹配
    必然把他人专利算到本人头上，故一律按缺测处理，不参与归一。

    返回 (件数或 None, 口径标签)。发明人字段每行仅一个姓名（件数合计 2,939,851 ≈ 表行数
    2,939,895），故该口径等价「第一发明人」；不是个人全部专利。
    """
    nm = s["name"]
    if not nm:
        return (None, "no_name")
    if name_dup().get(nm, 0) > 1:
        return (None, "homonym_in_pool")
    if len(nm) < 3:
        return (None, "short_name_homonym_risk")
    inv = inventor_counts()
    v = inv.get(nm)
    if v is None:
        return (None, "no_inventor_hit")
    return (int(v), "name_exact")


# ------------------------------------------------------------------ 研究方向 → 产业


# 深圳「20+8」产业集群关键词字典（英/中双语，人工维护 v2）
# v2 相对 v1 的两处修正：① 删掉 design / 裸 cell / 裸 gene 这类会被 "excellent" "general"
# 误命中的泛词；② 英文词改「左边界正则」匹配（允许复数），中文词仍走子串。
CLUSTERS: dict[str, list[str]] = {
    "网络与通信": ["communication", "telecommunication", "networking", "5g", "6g", "wireless",
                   "optical fiber", "光通信", "通信"],
    "半导体与集成电路": ["semiconductor", "integrated circuit", "chip", "vlsi", "cmos", "集成电路", "芯片"],
    "超高清视频显示": ["display", "oled", "lcd", "video coding", "显示", "超高清"],
    "智能终端": ["smart terminal", "wearable", "mobile device", "智能终端", "可穿戴"],
    "智能传感器": ["sensor", "mems", "sensing", "传感器"],
    "软件与信息服务": ["software", "cloud computing", "云计算", "软件"],
    "数字创意": ["digital media", "game", "animation", "virtual reality", "数字创意", "动漫", "游戏"],
    "现代时尚": ["fashion", "textile", "时尚", "纺织"],
    "工业母机": ["machine tool", "cnc", "机床", "工业母机"],
    "智能机器人": ["robot", "robotics", "manipulator", "机器人"],
    "激光与增材制造": ["laser", "additive manufacturing", "3d printing", "laser cladding", "激光", "增材制造"],
    "精密仪器设备": ["precision instrument", "measuring instrument", "仪器", "精密仪器", "光谱仪"],
    "新能源": ["new energy", "solar", "photovoltaic", "wind power", "battery", "储能", "光伏", "新能源"],
    "安全节能环保": ["energy saving", "environmental", "carbon", "节能", "环保", "碳中和"],
    "智能网联汽车": ["autonomous driving", "intelligent vehicle", "connected vehicle", "智能网联", "自动驾驶"],
    "新材料": ["new material", "polymer", "alloy", "composite", "新材料", "材料"],
    "高端医疗器械": ["medical device", "医疗器械", "医学影像"],
    "生物医药": ["biomedicine", "drug", "pharmaceutical", "pharmacology", "生物医药", "药物"],
    "大健康": ["health", "clinical", "nursing", "健康", "临床"],
    "海洋产业": ["marine", "ocean", "海洋"],
    "合成生物": ["synthetic biology", "metabolic engineering", "合成生物"],
    "区块链": ["blockchain", "distributed ledger", "区块链"],
    "细胞与基因": ["stem cell", "single-cell", "cell therapy", "gene therapy", "gene editing",
                   "genomics", "genetic", "crispr", "细胞", "基因"],
    "空天技术": ["aerospace", "satellite", "空天", "卫星"],
    "脑科学与类脑智能": ["neuroscience", "brain", "neuromorphic", "脑科学", "类脑"],
    "深地深海": ["deep sea", "deep earth", "深海", "深地"],
    "可见光通信与光计算": ["visible light communication", "optical computing", "光计算", "可见光通信"],
    "量子信息": ["quantum", "量子"],
}

CLUSTER_KEYS = [(k, [w.lower() for w in ws]) for k, ws in CLUSTERS.items()]
_CJK = re.compile(r"[\u4e00-\u9fff]")


def _kw_hit(text_low: str, kw: str) -> bool:
    """中文关键词走子串；英文关键词走**左右双边界**（允许 s/es 复数），
    避免 network 命中 neural network、instrument 命中 instrumental 这类跨义误命中。"""
    if _CJK.search(kw):
        return kw in text_low
    return re.search(r"(?<![a-z])" + re.escape(kw) + r"(?:e?s)?(?![a-z])", text_low) is not None


def clusters_of(tags: list[str]) -> list[str]:
    """研究方向标签 → 命中的 20+8 集群（去重、保序）。"""
    hits: list[str] = []
    low = [t.lower() for t in tags]
    for name, kws in CLUSTER_KEYS:
        if name in hits:
            continue
        for t in low:
            if any(_kw_hit(t, k) for k in kws):
                hits.append(name)
                break
    return hits


# ------------------------------------------------------------------ 中文论文作者面
# 为什么需要这一层：`dwd_scholar_work_experience` / `education_background` / `research_direction`
# 三张子表的 scholar_id 与 `dwd_scholar.scholar_id` **只有 9.3% 交集**（实测 work 1,856/20,028、
# edu 1,853/20,025、research 1,853/19,514；改用 dwd_scholar.id 连只有 1,509 行），三表无姓名列，
# 无法桥接。中文论文面 `a25_paper_panel`（100,900 篇、20,048 条关键词、作者信息 JSON）带
# 「姓名 + 机构 + 年份」，可做**姓名+机构前缀双锚定**的活动度桥接，覆盖率 68.33%，是本批
# 成长性/产业相关/产学研触点三维的唯一可用桥。

_ORG_SEP = re.compile(r"[（(，,、/|;；]")


def _org_head(s: str, k: int = 6) -> str:
    """机构名的稳定前缀：先按括号/标点切掉后缀，再取前 k 字。"""
    s = _ORG_SEP.split(s or "")[0].strip()
    return s[:k]


def paper_index() -> dict[str, list[dict]]:
    """姓名 → [{y, inst, pid, kw, ti}]；作者记录 215,816 条（100,900 篇全量解析，零 DB）。"""
    if "pix" not in _C:
        panel = _load("a25_paper_panel.json")
        kw = {r["id"]: (r.get("keywords") or "") for r in panel["cls"]}
        idx: dict[str, list[dict]] = {}
        for p in panel["paper"]:
            try:
                y = int(str(p.get("y") or "")[:4])
            except Exception:
                continue
            pid = p.get("id")
            k = kw.get(pid, "")
            ti = (p.get("zh_name") or "") + " " + (p.get("en_name") or "")
            try:
                authors = json.loads(p.get("author_info_list") or "[]")
            except Exception:
                continue
            for a in authors:
                nm = (a.get("zh_name") or "").strip()
                if not nm:
                    continue
                idx.setdefault(nm, []).append(
                    {"y": y, "inst": (a.get("institution") or ""), "pid": pid, "kw": k, "ti": ti})
        _C["pix"] = idx
    return _C["pix"]  # type: ignore[return-value]


def name_papers(s: dict) -> list[dict]:
    """仅姓名匹配（不锚机构）：用于「曾在深圳署名」这类**履历性**信号，
    因为人不一定还在原机构；代价是同名误配，故只做 0/1 信号、不做计数。"""
    return paper_index().get(s["name"], []) if s["name"] else []


def anchored_papers(s: dict) -> list[dict]:
    """姓名 + 机构前缀双锚定的论文记录（结果按 scholar_id 记忆化）。"""
    key = ("anc", s["sid"])
    if key in _C:
        return _C[key]  # type: ignore[return-value]
    o = s["org"]
    out: list[dict] = []
    if o and s["name"]:
        head = _org_head(o)
        for r in paper_index().get(s["name"], []):
            inst = r["inst"]
            if not inst:
                continue
            if head and (head in inst or _org_head(inst) in o):
                out.append(r)
    _C[key] = out
    return out


ENT_KW = ("公司", "集团", "有限", "股份", "厂", "研究院（企业）")


def is_enterprise(org: str) -> bool:
    s = org or ""
    return any(k in s for k in ENT_KW)


def paper_insts() -> dict[str, list[str]]:
    """paper_id → 全部作者机构名列表；用于「是否有深圳机构合作者」的判定（按论文粒度）。"""
    if "pinst" not in _C:
        panel = _load("a25_paper_panel.json")
        d: dict[str, list[str]] = {}
        for p in panel["paper"]:
            try:
                authors = json.loads(p.get("author_info_list") or "[]")
            except Exception:
                continue
            d[p.get("id")] = [(a.get("institution") or "") for a in authors]
        _C["pinst"] = d
    return _C["pinst"]  # type: ignore[return-value]


_PCL: dict[str, list[str]] = {}


def paper_clusters(pid: str, kw: str, ti: str) -> list[str]:
    """论文 → 命中的 20+8 集群（按 paper_id 记忆化；关键词与标题都用，标题用于补关键词缺失的 80%）。"""
    if pid in _PCL:
        return _PCL[pid]
    tags: list[str] = []
    if kw:
        tags.extend(x.strip() for x in kw.split(",") if x.strip())
    if ti:
        tags.append(ti)
    v = clusters_of(tags) if tags else []
    _PCL[pid] = v
    return v
