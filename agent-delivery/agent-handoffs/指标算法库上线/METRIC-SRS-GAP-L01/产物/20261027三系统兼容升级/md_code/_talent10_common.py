#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TALENT 十件（FLOW / GRAPH_110 / ORG / REGION / RELATION / STRUCT_QUERY /
SUPPLY / SZ_STATUS / SZ_SUPPLY_DEMAND / UNIV_NEW）公共计算层 —— 零 DB、只读快照。

本模块只做四件事，不做指标口径：
  1. 读 `_snapshots21/` 下已落盘的 gkx 快照（含 source 字段），并暴露统一的 `panel()`；
  2. 机构名 → 属地的**分支校区修正**（`loc2`）：`哈尔滨工业大学（深圳）` 必须落深圳，
     而不是被「哈尔滨工业大学」前缀带回哈尔滨；`中山大学` 例外回广州；
  3. 机构类型、学位、职称、学科域的归一函数（规则式，正文逐条披露）；
  4. 集中度/分位/落盘封装（`hhi` / `cr` / `gini` / `write`），并强制
     `support_judgment` + `base_years_*` 三个基期键，缺一即报错。

铁律：
  - 缺失写 None 或空列表，不写 0；本模块不提供任何「补零」入口。
  - 不连库、不发 SQL；专利数字只读 `star_applicant_agg_gkx.json` /
    `patent_inventor_counts_gkx.json`。
"""
from __future__ import annotations

import json
import math
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent21_common as T  # noqa: E402

SNAP = HERE / "_snapshots21"
SOURCES = {
    "db": "gkx（三方库，只读）",
    "host": "183.240.141.251:3318",
    "snapshots": [
        "code/_snapshots21/probe_a26_20261022.json（学者主档 21,316）",
        "code/_snapshots21/talent22_panel_20261022.json（学者面板 20,420）",
        "code/_snapshots21/probe_talent21_20261022.json（履历 57,117 / 学历 43,766 / 方向 20,030）",
        "code/_snapshots21/heis21_20261022.json（高校名录 3,501）",
        "code/_snapshots21/scholar_fill_20261022.json（ORCID 明细 21,316）",
        "code/_snapshots21/coauthor160_20261022.json（合著度 20,011 / 深圳子图 9,066）",
        "code/_snapshots21/recruit161_20261022.json（招聘样本 82,201）",
        "code/_snapshots21/a25_paper_panel.json（中文论文 100,900）",
        "code/_snapshots21/base_20261021.json（企业底册 189,116）",
    ],
    "sql_count": 4,
    "note": "4 条 SQL 仅用于补快照：高校名录增强 1 条、dwd_scholar 填充率与 ORCID 明细 2 条、"
            "其余指标全部离线读快照；专利侧 0 条 SQL。",
}

_C: dict[str, object] = {}


def load(name: str):
    key = name
    if key not in _C:
        _C[key] = json.loads((SNAP / name).read_text(encoding="utf-8"))
    return _C[key]


def panel() -> dict:
    return load("talent22_panel_20261022.json")


def rows() -> list[dict]:
    return panel()["scholars"]


def scholars_all() -> list[list]:
    """21,316 行 [sid, name, org, paper, cite, h, status, ...]（A-26 scholar_dump）。"""
    return load("probe_a26_20261022.json")["scholar_dump"]["rows"]


def work() -> list[dict]:
    return T.work()


def edu() -> list[dict]:
    return T.edu()


def research() -> dict[str, list[str]]:
    return T.research()


def heis_rows() -> list[list]:
    return load("heis21_20261022.json")["rows"]


# ------------------------------------------------------------------ 属地

_CITY_TOKENS = sorted(set(T.CITY_PROV) | {c + "市" for c in T.CITY_PROV},
                      key=len, reverse=True)
_LOC: dict[str, tuple[str, str, str]] = {}


def loc2(org: str) -> tuple[str, str, str]:
    """机构 → (省, 市, 归属方式)，带两条覆盖规则。

    规则一（分支校区）：取机构名里**最靠右**的城市名。实测 `loc()` 的前缀匹配会把
    `哈尔滨工业大学（深圳）` 判回哈尔滨（12 人）、把 `北京大学深圳医院` 判回北京（2 人），
    这类错误会影响深圳口径的 24 人，必须修正。
    规则二（中山大学）：`中山大学` 在广州市，不能按城市字面判到中山市。
    """
    o = (org or "").strip()
    if o in _LOC:
        return _LOC[o]
    out: tuple[str, str, str]
    if not o:
        out = ("未填", "未填", "empty")
    elif "中山大学" in o and "中山市" not in o:
        out = ("广东省", "广州市", "uni_override")
    else:
        best = None
        for c in _CITY_TOKENS:
            i = o.rfind(c)
            if i < 0:
                continue
            if best is None or i > best[0] or (i == best[0] and len(c) > len(best[1])):
                best = (i, c)
        if best is not None and T.CITY_PROV.get(best[1].rstrip("市")):
            short = best[1].rstrip("市")
            out = (T.CITY_PROV[short], short + "市", "city_rightmost")
        elif o.startswith("中国科学院") or o.startswith("中国社会科学院"):
            out = ("北京市", "北京市", "academy_hq")
        else:
            out = T.loc(o)
    _LOC[o] = out
    return out


def is_sz_org(org: str) -> bool:
    p, c, _ = loc2(org)
    return c == "深圳市" or "深圳" in (org or "")


# ------------------------------------------------------------------ 机构类型

_HEIS_NAMES: set[str] | None = None


def heis_names() -> set[str]:
    global _HEIS_NAMES
    if _HEIS_NAMES is None:
        _HEIS_NAMES = {h[0] for h in heis_rows() if h[0]}
    return _HEIS_NAMES


def org_type(org: str) -> str:
    """五类：高校 / 医疗机构 / 科研院所 / 企业 / 其他。顺序不可颠倒。

    `XX大学附属医院` 必须落「医疗机构」而不是「高校」——否则医疗维会被并进高校，
    实测会多算 1,100 余人。高校名册（3,501 行）优先，其次名称规则。
    """
    o = (org or "").strip()
    if not o:
        return "未填"
    if o in heis_names():
        return "高校"
    if any(k in o for k in ("医院", "医学中心", "疾病预防", "卫生院", "保健院")):
        return "医疗机构"
    if any(k in o for k in ("大学", "学院", "学校")):
        return "高校"
    if any(k in o for k in ("研究院", "研究所", "科学院", "研究中心", "实验室", "工程中心")):
        return "科研院所"
    if any(k in o for k in ("公司", "集团", "有限", "股份", "厂", "企业", "事务所")):
        return "企业"
    return "其他"


# ------------------------------------------------------------------ 学位 / 职称

_DEG_RANK = {"博士后": 5, "博士": 4, "硕士": 3, "学士": 2, "专科": 1, "未填": 0}


def degnorm(zh: str, en: str = "") -> str:
    t = f"{zh or ''} {en or ''}".strip()
    low = t.lower()
    if "博士后" in t or "postdoc" in low:
        return "博士后"
    if "博士" in t or re.search(r"\bph\.?\s?d\b|doctor", low):
        return "博士"
    if "硕士" in t or re.search(r"master|msc|m\.s", low):
        return "硕士"
    if "学士" in t or "本科" in t or re.search(r"bachelor|bsc|b\.s", low):
        return "学士"
    if "专科" in t or "大专" in t:
        return "专科"
    return "未填"


def highest_degree() -> dict[str, str]:
    """sid → 最高学位（同一人多段学历取最高；不跨宇宙补值）。"""
    if "deg" not in _C:
        d: dict[str, str] = {}
        for e in edu():
            v = degnorm(e["deg_zh"], e["deg_en"])
            if _DEG_RANK[v] > _DEG_RANK.get(d.get(e["sid"], "未填"), 0):
                d[e["sid"]] = v
        _C["deg"] = d
    return _C["deg"]  # type: ignore[return-value]


_POS_RANK = {"正高": 4, "副高": 3, "中级": 2, "其他/未填": 1}


def posnorm(p: str) -> str:
    s = p or ""
    if re.search(r"副教授|副研究员|副高|副主任医师|副主任|高级工程师", s):
        return "副高"
    if re.search(r"教授|研究员|正高|主任医师|首席", s):
        return "正高"
    if re.search(r"讲师|助理研究员|主治|工程师|博士后|助理教授", s):
        return "中级"
    return "其他/未填"


def highest_position() -> dict[str, str]:
    if "pos" not in _C:
        d: dict[str, str] = {}
        for w in work():
            v = posnorm(w["pos"])
            if _POS_RANK[v] > _POS_RANK.get(d.get(w["sid"], "其他/未填"), 1):
                d[w["sid"]] = v
        _C["pos"] = d
    return _C["pos"]  # type: ignore[return-value]


# ------------------------------------------------------------------ 学科域

DOMAINS = ["生物医药/健康", "能源/材料/化工", "AI/软件与信息", "电子/芯片与通信",
           "装备/机器人与制造", "基础科学", "经管/人文社科", "农业/食品/生态",
           "建筑/土木/交通", "其他/未归类"]

_DOM_KW = {
    "生物医药/健康": ("医药", "医学", "临床", "生物", "药", "健康", "护理", "公共卫生",
                    "medical", "biolog", "pharma", "clinical", "health", "生命"),
    "能源/材料/化工": ("材料", "化工", "能源", "电池", "光伏", "储能", "环境", "冶金", "燃料",
                    "material", "energy", "chemical", "battery", "environment"),
    "AI/软件与信息": ("算法", "软件", "计算机", "数据", "人工智能", "机器学习", "智能", "信息",
                    "通信", "网络", "computer", "software", "algorithm", "learning",
                    "information", "network", "communication"),
    "电子/芯片与通信": ("电子", "芯片", "半导体", "硬件", "射频", "电路", "光电", "微电子",
                    "semiconductor", "circuit", "electronic", "optical"),
    "装备/机器人与制造": ("机械", "结构", "自动化", "电气", "设备", "工艺", "制造", "机器人",
                      "控制", "车辆", "航空", "航天", "robot", "mechanic", "manufactur", "control"),
    "基础科学": ("数学", "物理", "化学", "天文", "地理", "地质", "力学", "统计",
              "mathematic", "physic", "chemistry", "astronom"),
    "经管/人文社科": ("经济", "管理", "金融", "会计", "法律", "法学", "教育", "历史", "哲学",
                   "文学", "新闻", "社会", "心理", "艺术", "design",
                   "econom", "management", "finance", "law", "education"),
    "农业/食品/生态": ("农业", "农学", "食品", "林学", "畜牧", "水产", "生态", "作物",
                    "agricultur", "food", "ecolog"),
    "建筑/土木/交通": ("建筑", "土木", "交通", "规划", "水利", "测绘", "桥梁",
                    "architect", "civil", "transport"),
}


def domain_of(text: str) -> str:
    """学科/岗位文本 → 十域之一（先中文关键词，再英文）。顺序即优先级。"""
    s = (text or "").lower()
    if not s:
        return "其他/未归类"
    for d in DOMAINS[:-1]:
        if any(k.lower() in s for k in _DOM_KW[d]):
            return d
    return "其他/未归类"


# 20+8 集群 → 十域（仅 SZ_SUPPLY_DEMAND 的供给侧使用，正文披露为人工映射）
CL2D = {
    "生物医药": "生物医药/健康", "高端医疗器械": "生物医药/健康", "大健康": "生物医药/健康",
    "细胞与基因": "生物医药/健康", "合成生物": "生物医药/健康", "脑科学与类脑智能": "生物医药/健康",
    "新能源": "能源/材料/化工", "新材料": "能源/材料/化工", "安全节能环保": "能源/材料/化工",
    "网络与通信": "电子/芯片与通信", "半导体与集成电路": "电子/芯片与通信",
    "超高清视频显示": "电子/芯片与通信", "智能终端": "电子/芯片与通信",
    "智能传感器": "电子/芯片与通信", "可见光通信与光计算": "电子/芯片与通信",
    "工业母机": "装备/机器人与制造", "智能机器人": "装备/机器人与制造",
    "激光与增材制造": "装备/机器人与制造", "精密仪器设备": "装备/机器人与制造",
    "智能网联汽车": "装备/机器人与制造",
    "软件与信息服务": "AI/软件与信息", "区块链": "AI/软件与信息", "数字创意": "AI/软件与信息",
    "现代时尚": "经管/人文社科", "海洋产业": "其他/未归类", "空天技术": "其他/未归类",
    "深地深海": "其他/未归类", "量子信息": "基础科学",
}

# 招聘岗位 → 十域（标题文本，权重由标题词决定；正文披露为规则映射）
JOB2D = {
    "AI/软件与信息": ("算法", "软件", "开发", "java", "python", "前端", "后端", "数据", "人工智能",
                  "机器学习", "测试", "运维", "嵌入式", "产品经理", "ui", "架构", "程序"),
    "电子/芯片与通信": ("电子", "芯片", "半导体", "硬件", "射频", "通信", "电路", "pcb", "fpga", "光学"),
    "装备/机器人与制造": ("机械", "结构", "自动化", "电气", "设备", "工艺", "制造", "机器人", "模具",
                    "品质", "质量", "生产", "装配", "焊"),
    "能源/材料与化工": ("材料", "化工", "能源", "电池", "光伏", "储能", "环境", "安全"),
    "生物医药/健康": ("医药", "医学", "临床", "生物", "药", "护士", "医生", "健康", "器械"),
    "经管/人文社科": ("销售", "市场", "商务", "财务", "会计", "人力", "行政", "采购", "运营",
                  "法务", "经理", "总监", "助理", "文员", "外贸", "客服", "设计", "策划", "教师"),
}


def job_domain(title: str) -> str:
    s = (title or "").lower()
    for d in ("AI/软件与信息", "电子/芯片与通信", "装备/机器人与制造",
              "能源/材料与化工", "生物医药/健康", "经管/人文社科"):
        if any(w in s for w in JOB2D[d]):
            return d
    return "其他/未归类"


# ------------------------------------------------------------------ 统计工具


def pctl(vals, q: float):
    return T.pctl(vals, q)


def st(vals) -> dict:
    return T.st(vals)


def cr(counts: list[int], k: int, total: int | None = None) -> float:
    tot = total if total is not None else sum(counts)
    return round(100 * sum(sorted(counts, reverse=True)[:k]) / tot, 2) if tot else 0.0


def hhi(counts: list[int]) -> float:
    tot = sum(counts)
    return round(sum((c / tot) ** 2 for c in counts) * 10000, 1) if tot else 0.0


def gini(vals: list[int]) -> float:
    v = sorted(vals)
    n = len(v)
    s = sum(v)
    if not n or not s:
        return 0.0
    return round(sum((2 * i - n - 1) * x for i, x in enumerate(v, 1)) / (n * s), 4)


def share(n: int, d: int) -> float:
    return round(100 * n / d, 2) if d else 0.0


# ------------------------------------------------------------------ 落盘


def write(metric: str, payload: dict) -> Path:
    for f in ("support_judgment", "base_years_used", "base_years_missing", "base_years_note"):
        if f not in payload:
            raise SystemExit(f"{metric}: 缺少顶层 {f}（见 DISPATCH_BRIEF v6 第二节 / DATA_FACTS §3.16）")
    if payload["support_judgment"] not in ("完全直接支持", "完全转换支持", "部分支持", "完全不支持"):
        raise SystemExit(f"{metric}: support_judgment 不在四档内")
    payload.setdefault("metric", metric)
    payload.setdefault("sources", SOURCES)
    out = HERE / f"{metric}_out.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str),
                   encoding="utf-8")
    print("wrote", out.name, f"({out.stat().st_size} bytes)")
    return out
