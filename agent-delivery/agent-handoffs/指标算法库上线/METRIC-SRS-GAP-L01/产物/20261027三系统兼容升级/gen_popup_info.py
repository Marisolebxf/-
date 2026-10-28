#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_popup_info.py —— 指标弹窗数据编译器（20261028_1021版指标入库查实 · Track B）

把 573 份指标调研 md（20261027 批，含 8 件 _ZT/_ZS 拆分变体）编译成三大 UI
（demo-ui-system-test / demo-ui-topic / demo-ui-science）指标弹窗用的结构化数据
METRIC_POPUP_INFO：req_overview / calc_logic / references / support / applicable_systems。

输入（全部只读）：
  1. <本目录>/第三方库指标计算过程/*.md（20261027 批正本，已实物化入仓）
  2. gkx-orchestration/agent-delivery/metrics/registry/cfg_metric-*-seed.yaml（兜底 definition/formula）
  3. gkx-orchestration/agent-delivery/metrics/registry/metric-readiness-matrix-*.yaml（仅校验覆盖）
  4. 参照实现 repos/lumen-ui-algo-apiview/scripts/gen_metric_docs.py（参照，运行不依赖）（章节解析 / 句净化 / DEAD_URLS
     —— 思路与正则借用，独立实现，不 import）

产物（全部 GENERATED 文件头 + 生成时间）：
  - repos/demo-ui-system-test/src/views/shared/metricPopupInfo.generated.ts
      key=原 ID（565 基线件：20261027 批去 _ZT/_ZS 后全量，含 GAP 件）
  - repos/demo-ui-topic/src/app/mock/enterprise/metricPopupInfo.generated.ts
      同结构，但 6 个拆分族优先 _ZT 版内容覆盖原 key
  - repos/demo-ui-science/src/metricPopupInfo.generated.js
      ESM export，6 族优先 _ZS 版
  - _work/gen_popup_stats.json（统计）

拆分族（依据 20261027/过程文件/02_D2兼容判定与拆分_总结.md；实际文件中 M_CHAIN_REGION_INDEX
与 M_ENT_REVENUE_LATEST 亦有 _ZT/_ZS 变体，共 6 族 12 件）：
  M_CHAIN_STAGE_SCORE / M_CHAIN_REGION_INDEX / M_ENT_REVENUE_LATEST /
  M_ENT_COMPETITIVENESS_SCORE / M_ORG_TECH_SCORE / M_TALENT_FLOW_TRACK
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import yaml

# 入仓锚点：本文件位于 agent-delivery/agent-handoffs/指标算法库上线/METRIC-SRS-GAP-L01/产物/20261027三系统兼容升级/
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]                      # .../gkx-orchestration/agent-delivery 前的仓根
MD_DIR = HERE / "第三方库指标计算过程"          # 正本已实物化入仓（20261027 批 573 份）
REGISTRY = REPO / "agent-delivery" / "metrics" / "registry"
STATS_PATH = Path(__file__).resolve().parent / "gen_popup_stats.json"

OUT_SYSTEM_TEST = REPO / "repos" / "demo-ui-system-test" / "src" / "views" / "shared" / "metricPopupInfo.generated.ts"
OUT_TOPIC = REPO / "repos" / "demo-ui-topic" / "src" / "app" / "mock" / "enterprise" / "metricPopupInfo.generated.ts"
OUT_SCIENCE = REPO / "repos" / "demo-ui-science" / "src" / "metricPopupInfo.generated.js"

GEN_AT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

SPLIT_FAMILIES = [
    "M_CHAIN_STAGE_SCORE",
    "M_CHAIN_REGION_INDEX",
    "M_ENT_REVENUE_LATEST",
    "M_ENT_COMPETITIVENESS_SCORE",
    "M_ORG_TECH_SCORE",
    "M_TALENT_FLOW_TRACK",
]

# ---------------------------------------------------------------------------
# 死链清单（整表复制自 repos/lumen-ui-algo-apiview/scripts/gen_metric_docs.py，
# 导出自 /tmp/agent_docs/url_final.json 的 dead 数组，20261025 全页 URL 体检）
# ---------------------------------------------------------------------------
DEAD_URLS: frozenset = frozenset({
    "http://www.gov.cn/zhengce/2020-10/11/content_5550505.htm",
    "http://www.moe.gov.cn/s78/A16/A16_tjdc/202512/t20251211_1423144.html",
    "http://www.scio.gov.cn/live/2024/35043/wjzc/202410/t20241022_870437.html",
    "http://www.stats.gov.cn/tjsj/tjbz/201801/t20180103_1569357.html",
    "http://www.stats.gov.cn/tjsj/tjbz/201812/t20181229_1642354.html",
    "http://www.sz.gov.cn/cn/xxgk/zfxxgj/zcfg/szsfg/content/post_9932813.html",
    "http://www.sz.gov.cn/zfgb/2022/gb1234/content/post_9778888.html",
    "https://doi.org/10.1016/0377-2217(87)901067",
    "https://doi.org/10.1016/S0169-7218(05)01001-2",
    "https://doi.org/10.1016/j.jpolmod.2011.01.002",
    "https://doi.org/10.1023/A:1007922003277",
    "https://doi.org/10.1023/A:1007973900665",
    "https://doi.org/10.1057/9781137436350_2",
    "https://doi.org/10.1093/oso/9780198289777.001.0001",
    "https://doi.org/10.1111/j.1435-5597.1960.tb01797.x",
    "https://doi.org/10.1787/3a2f3b1e-en",
    "https://doi.org/10.1787/9789264022432-en",
    "https://doi.org/10.2307/2232389",
    "https://doi.org/10.2307/270654",
    "https://ec.europa.eu/eurostat/web/nace-rev2",
    "https://ec.europa.eu/eurostat/web/research-methodology",
    "https://gxj.sz.gov.cn/xxgk/xxgkml/zcfg/",
    "https://hbr.org/1972/07/evolution-and-revolution-as-organizations-grow",
    "https://incites.help.clarivate.com/",
    "https://jcr.clarivate.com/",
    "https://kns.cnki.net/kcms2/article/abstract?v=ggjTjMZ9K8Y",
    "https://kns.cnki.net/kcms2/article/abstract?v=ltp_platform",
    "https://kns.cnki.net/kcms2/article/abstract?v=policy_measure",
    "https://kns.cnki.net/kcms2/article/abstract?v=policy_process",
    "https://neo4j.com/docs/getting-started/appendix/graph-modeling/",
    "https://nlp.stanford.edu/IR-book/",
    "https://tjj.huizhou.gov.cn/",
    "https://trends.google.com/",
    "https://www.brookings.edu/articles/the-rise-of-innovation-districts/",
    "https://www.cac.gov.cn/2017-05/02/c_1120885601.htm",
    "https://www.casted.org.cn/",
    "https://www.cces.org.cn/",
    "https://www.ccidgroup.com/",
    "https://www.ccidthinktank.com/",
    "https://www.cec-ceda.org.cn/",
    "https://www.chinatorch.gov.cn/",
    "https://www.chinatorch.org.cn/",
    "https://www.customs.gov.cn/",
    "https://www.etsi.org/intellectual-property/",
    "https://www.etsi.org/intellectual-property/ipr-standards",
    "https://www.gd.gov.cn/gkmlpt/content/2/2422/post_2422368.html",
    "https://www.gd.gov.cn/zwgk/wjk/qbwj/yf/content/post_3011123.html",
    "https://www.gdass.gov.cn/",
    "https://www.gei.com.cn/",
    "https://www.ggzy.gov.cn/",
    "https://www.gjsy.gov.cn/",
    "https://www.gov.cn/gongbao/content/2012/content_2165562.htm",
    "https://www.gov.cn/gongbao/content/2016/content_5077053.htm",
    "https://www.gov.cn/xinwen/2019-02/21/content_5367465.htm",
    "https://www.gov.cn/yaowen/liebiao/202303/content_6945847.htm",
    "https://www.gov.cn/zhengce/2015-04/30/content_2855352.htm",
    "https://www.gov.cn/zhengce/2016-07/31/content_5096406.htm",
    "https://www.gov.cn/zhengce/2021-08/02/content_5629039.htm",
    "https://www.gov.cn/zhengce/content/2014-12/03/content_9278.htm",
    "https://www.gov.cn/zhengce/content/2017-06/19/content_5203677.htm",
    "https://www.gov.cn/zhengce/content/2018-01/31/content_5262566.htm",
    "https://www.gov.cn/zhengce/content/2019-03/15/content_5373898.htm",
    "https://www.gov.cn/zhengce/content/2019-05/08/content_5389667.htm",
    "https://www.gov.cn/zhengce/content/2022-03/01/content_5677170.htm",
    "https://www.gov.cn/zhengce/content/202308/content_6899945.htm",
    "https://www.gov.cn/zhengce/content/202401/content_6924378.htm",
    "https://www.gov.cn/zhengce/content/202401/content_6926257.htm",
    "https://www.gov.cn/zhengce/zhengceku/2020-03/02/content_5487878.htm",
    "https://www.gov.cn/zhengce/zhengceku/2021-07/02/content_5622154.htm",
    "https://www.gov.cn/zhengce/zhengceku/2022-06/02/content_5693142.htm",
    "https://www.gov.cn/zhengce/zhengceku/2022-09/06/content_5708004.htm",
    "https://www.gov.cn/zhengce/zhengceku/202401/content_6929024.htm",
    "https://www.gov.cn/zwgk/2011-07/04/content_1898747.htm",
    "https://www.gstianzhu.gov.cn/art/2024/9/26/art_5585_1368776.html",
    "https://www.gsxt.gov.cn/",
    "https://www.hustp.com/",
    "https://www.innocom.gov.cn/",
    "https://www.justice.gov/atr/horizontal-merger-guidelines-08192010",
    "https://www.keenage.com/",
    "https://www.oecd.org/",
    "https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf",
    "https://www.oecd.org/en/publications/oecd-regions-and-cities-at-a-glance-2024_f42db3bf-en/full-report/methodologies_b841d611.html",
    "https://www.oecd.org/migration/",
    "https://www.oecd.org/regional/",
    "https://www.oecd.org/sdd/42495745.pdf",
    "https://www.oecd.org/sti/",
    "https://www.oecd.org/sti/frascati-manual-2015-9789264239012-en.htm",
    "https://www.oecd.org/sti/frascati-manual-2015.htm",
    "https://www.oecd.org/sti/frascati-manual.htm",
    "https://www.oecd.org/sti/ind/measuring-trade-in-value-added.htm",
    "https://www.oecd.org/sti/inno/",
    "https://www.oecd.org/sti/inno/frascati-manual.htm",
    "https://www.oecd.org/sti/inno/oecdpatentstatisticsmanual.htm",
    "https://www.oecd.org/sti/inno/patent-statistics.htm",
    "https://www.oecd.org/sti/inno/policy-mix.htm",
    "https://www.oecd.org/sti/intellectual-property-statistics-and-analysis.htm",
    "https://www.oecd.org/sti/outlook/",
    "https://www.oecd.org/sti/scoreboard.htm",
    "https://www.samr.gov.cn/zw/tjxx/",
    "https://www.sasac.gov.cn/",
    "https://www.scip.org/page/CI-MI-Basics-Topic-Hub",
    "https://www.scopus.com/",
    "https://www.scopus.com/sources",
    "https://www.simonandschuster.com/",
    "https://www.stats.gov.cn/sj/ndsj/trcc/",
    "https://www.stats.gov.cn/sj/tjbz/201801/t20180102_1569431.html",
    "https://www.stats.gov.cn/sj/tjbz/201801/t20180103_1569357.html",
    "https://www.stats.gov.cn/sj/tjbz/gjtjbz/201710/t20171017_1758922.html",
    "https://www.stats.gov.cn/sj/tjbz/gjtjbz/202008/P020200817372060806480.pdf",
    "https://www.stats.gov.cn/sj/tjbz/gjtjbz/202302/P020230213403045604944.pdf",
    "https://www.stats.gov.cn/sj/tjbz/gjtjbz/202302/t20230213_1902774.html",
    "https://www.stats.gov.cn/sj/tjbz/gjtjbz/202302/t20230213_1902798.html",
    "https://www.stats.gov.cn/sj/tjcbw/",
    "https://www.stats.gov.cn/sj/tjcbw/202302/t20230213_1902772.html",
    "https://www.stats.gov.cn/sj/tjfg/",
    "https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjpcgb/201911/t20191127_1712490.html",
    "https://www.stats.gov.cn/sj/zxfb/202310/t20231026_1943443.html",
    "https://www.stats.gov.cn/sj/zxfb/202509/t20250929_1961392.html",
    "https://www.sz.gov.cn/zfgb/2022/gb1234/content/post_9876543.html",
    "https://www.unesco.org/reports/science/",
    "https://www.worldcat.org/",
    "https://www.worldcat.org/title/11547934",
    "https://www.zgc.gov.cn/",
    "https://xzqh.mca.gov.cn/",
    "https://zjinfo.gov.cn/",
})
DEAD_URLS_NORM: frozenset = frozenset(u.strip().rstrip("/") for u in DEAD_URLS)

# ---------------------------------------------------------------------------
# 内部工程语言 / 开发日志句式（借自 gen_metric_docs.py，独立内联）
# ---------------------------------------------------------------------------
DIRTY_SENT_RE = re.compile(
    r"旧稿|旧版|本批|此前版本|之前版本|历史版本|上一版|复盘修正|返工|欠账"
    r"|POV-|B 轨|B轨|禁止改挂|会签|正本|登记依赖|待甲方|pending|已核|真源|底稿"
    r"|王惠|calc-logic|DATA_FACTS"
    r"|属\s*[AB]\s*类|[AB]\s*类指标|判\s*完全不支持|判\s*部分支持|判\s*完全支持"
    r"|判定为\s*完全不支持|判定为\s*部分支持|数据支持度"
    r"|项目内|钉版|池表|卡面投影|事实面|登记依赖"
    r"|20261021|20261027|20261020|抬头治理|拆分件|兼容升级|单系统件|三系统兼容"
    r"|复跑|复现脚本|落盘快照|_snapshots21|_work_gkx21|METRIC-SRS-GAP|抬头|拍板",
    re.I,
)
DIRTY_REFS_RE = re.compile(
    r"项目内部|项目内|内部文档|本轮事实底稿|work_gkx21|DATA_FACTS|_snapshots21"
    r"|王惠|内部数据纪律|calc-logic|真源|旧稿|旧版|本批"
    r"|local-workspace|原始产品需求文档|gkx-orchestration"  # 净化词表：命中即剔除该句（防本地路径外泄），非路径引用
)

# ---------------------------------------------------------------------------
# 参考文献分组：国内官方机构白名单正则（借 ApiInfoPanel.vue L183 refOrder 思路）
# ---------------------------------------------------------------------------
GOV_INSTITUTION_RE = re.compile(
    r"国家统计局|工信部|工业和信息化部|科技部|科学技术部|知识产权局|专利局|国务院|发改委"
    r"|发展和改革委员会|教育部|自然科学基金|科学院|中国科学院|工程院|工程院"
    r"|深圳市政府|深圳市人民政府|深圳市统计局|深圳市地方金融|统计局|知识产权"
    r"|OECD|WIPO|世界知识产权|世界银行|世界贸易组织| UNESCO|联合国|欧盟委员会"
    r"|Eurostat|欧洲统计局|海关总署|海关|市场监管|商务部|财政部|国家卫生健康委"
    r"|国资委|科技信息展示系统需求|深圳市|广东省人民政府|广东省",
)
FOREIGN_INSTITUTION_RE = re.compile(
    r"University|Universit[yé]|Press|Journal|Journals|WIPO|World Bank|World"
    r"|Hirsch|Glänzel|Rasmussen|Barabási|Newman|Borgatti|Granovetter"
    r"|Institute|Springer|Elsevier|Nature|Science.*\d{4}|Scopus|Clarivate"
    r"|NBER|Brookings|McGraw|Routledge|Cambridge|Oxford|MIT|IEEE|ACM"
    r"|Association|American|National Bureau|RAND|Deloitte|PwC|OECD Library"
    r"|\.gov/|\.org/|\.com/|\.edu/|doi\.org",
    re.I,
)

# ---------------------------------------------------------------------------
# 统计
# ---------------------------------------------------------------------------
STATS = Counter()
FATALS: list[str] = []


def add_stat(k: str, n: int = 1) -> None:
    STATS[k] += n


# ---------------------------------------------------------------------------
# md 基础解析（借 gen_metric_docs.py 的 split_sections/find_section/strip_md 思路）
# ---------------------------------------------------------------------------
def split_sections(text: str) -> dict:
    parts = re.split(r"\n(?=## )", text)
    out = {}
    for p in parts:
        if p.startswith("## "):
            out[p.split("\n", 1)[0][3:].strip()] = p
    return out


def find_section(secs: dict, prefixes) -> str | None:
    for pre in prefixes:
        for k in sorted(secs):
            if k.startswith(pre):
                return secs[k]
    return None


def split_subsections(section_body: str) -> dict:
    """### N.M 标题 → 子章节正文（含标题行）。"""
    parts = re.split(r"\n(?=### )", section_body)
    out = {}
    for p in parts:
        m = re.match(r"### (\d+\.\d+)\s*(.*)", p)
        if m:
            out[m.group(1)] = p
    return out


def strip_md(s: str) -> str:
    s = re.sub(r"```[\s\S]*?```", "（代码见完整文档）", s)
    s = re.sub(r"\$\$[^$]*\$\$", "（公式见完整文档）", s, flags=re.S)
    s = re.sub(r"\$([^$]+)\$", r"\1", s)
    s = re.sub(r"\|", " ", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"[*#>`_]{2,}", " ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"(?<=[\u4e00-\u9fff（）、，。：；「」『』])\s+(?=[\u4e00-\u9fff（）、，。：；「」『』])", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    # 行首列表编号残留（"2. 内容" / "3）内容"）剥除
    s = re.sub(r"^\s*\d+[.、）)]\s*", "", s)
    return s


def prose_paragraphs(section_body: str, skip_head: bool = True) -> list[str]:
    """取章节正文里的散文段（跳过标题行/表格行/引用行/列表标记内容行/代码块）。"""
    lines = section_body.split("\n")
    paras: list[str] = []
    buf: list[str] = []
    in_code = False
    for i, ln in enumerate(lines):
        if skip_head and i == 0 and ln.startswith("## "):
            continue
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        st = ln.strip()
        if not st or st == "---":
            if buf:
                paras.append("".join(buf))
                buf = []
            continue
        if st.startswith(("|", ">", "#")):
            if buf:
                paras.append("".join(buf))
                buf = []
            continue
        # 列表项也并入散文流（结尾有句号即视为散文句）
        buf.append(st.lstrip("-*·• ").strip())
    if buf:
        paras.append("".join(buf))
    return [p for p in (strip_md(x) for x in paras) if p]


def purify_sentences(text: str, dirty: re.Pattern) -> list[str]:
    kept = []
    for s in re.split(r"(?<=[。！？])", text):
        t = s.strip()
        if not t:
            continue
        # 句首列表编号残留剥除
        t = re.sub(r"^\d+[.、）)]\s*", "", t)
        if dirty.search(t):
            add_stat("sentences_dropped_dirty")
            continue
        if len(t) < 6:
            continue
        kept.append(t)
    return kept


def take_n_sentences(text: str, n: int, dirty: re.Pattern = DIRTY_SENT_RE) -> str:
    sents = purify_sentences(text, dirty)
    return "".join(sents[:n])


# ---------------------------------------------------------------------------
# 头部 `>` 引用块字段解析（文件头 12 行内的 **字段名**：值）
# ---------------------------------------------------------------------------
HEAD_FIELD_RE = re.compile(r"\*\*(?:数据支持度|四判定摘要|适用系统)\*\*[：:]\s*(.+)")


def parse_head_fields(text: str) -> dict:
    head = text.split("\n## ", 1)[0]
    out = {"数据支持度": "", "四判定摘要": "", "适用系统": ""}
    for ln in head.split("\n"):
        if not ln.startswith(">"):
            continue
        m = re.search(r"\*\*数据支持度\*\*[：:]\s*(.+)", ln)
        if m:
            out["数据支持度"] = m.group(1).strip()
            continue
        m = re.search(r"\*\*四判定摘要\*\*[：:]\s*(.+)", ln)
        if m:
            out["四判定摘要"] = m.group(1).strip()
            continue
        m = re.search(r"\*\*适用系统\*\*[：:]\s*(.+)", ln)
        if m:
            out["适用系统"] = m.group(1).strip()
    return out


SUPPORT_LEVELS = ("完全直接支持", "完全转换支持", "部分支持", "完全不支持")


def extract_support_level(raw_field: str) -> str:
    """从『数据支持度』行原文提取四档之一。"""
    if not raw_field:
        return ""
    for lv in SUPPORT_LEVELS:
        if lv in raw_field:
            return lv
    return ""


def extract_verdict_summary(text: str, head: dict) -> str:
    """『四判定摘要』行原文；头部没有则不伪造（空串）。"""
    return head.get("四判定摘要", "")


# ---------------------------------------------------------------------------
# H1 标题解析指标中文名
# ---------------------------------------------------------------------------
def extract_name_zh(text: str, h1: str, seed: dict | None) -> str:
    m = re.match(r"#\s*(.+?)（[A-Za-z0-9\-_]+）\s*$", h1)
    if m:
        return m.group(1).strip()
    m = re.match(r"#\s*[A-Za-z0-9\-_]+\s*[—·—-]+\s*(.+)$", h1)
    if m:
        return m.group(1).strip()
    # H1 没有标准格式时用 seed 名
    if seed and seed.get("metric_name_zh"):
        return seed["metric_name_zh"]
    # 兜底：首个非空散文句前 20 字
    return h1.lstrip("# ").strip()[:30]


# ---------------------------------------------------------------------------
# req_overview：『## 摘要』前 2-3 句 + 『一、需求定义概述』1.2/1.6 小节概括
# ---------------------------------------------------------------------------
def build_req_overview(secs: dict, seed: dict | None) -> str:
    parts: list[str] = []
    abstract = find_section(secs, ("摘要",))
    if abstract:
        paras = prose_paragraphs(abstract)
        if paras:
            first = paras[0]
            sents = purify_sentences(first, DIRTY_SENT_RE)
            parts.append("".join(sents[:3]))
            if len(sents) < 2 and len(paras) > 1:
                more = take_n_sentences(paras[1], 3 - len(sents))
                if more:
                    parts.append(more)
    req_sec = find_section(secs, ("一、",))
    biz_parts: list[str] = []
    if req_sec:
        subs = split_subsections(req_sec)
        for num in ("1.2", "1.6"):
            sub = subs.get(num)
            if not sub:
                continue
            body_paras = prose_paragraphs(sub)
            if not body_paras:
                continue
            picked = take_n_sentences(body_paras[0], 2)
            if picked:
                biz_parts.append(picked)
    if biz_parts:
        parts.append("".join(biz_parts))
    out = "".join(parts).strip()
    if len(out) >= 30:
        return out
    # 兜底 seed definition
    if seed and seed.get("definition"):
        add_stat("req_overview_seed_fallback")
        return strip_md(seed["definition"])[:400]
    add_stat("req_overview_empty")
    return out


# ---------------------------------------------------------------------------
# calc_logic：『二、计算过程』2.1 + 2.4 各 1-2 句；无此章用『二、依赖性质裁定』
# 或『五、(方法对照)』替代；再兜底 seed formula
# ---------------------------------------------------------------------------
def build_calc_logic(secs: dict, seed: dict | None) -> str:
    parts: list[str] = []
    calc = find_section(secs, ("二、计算过程",))
    if calc:
        subs = split_subsections(calc)
        for num in ("2.1", "2.4"):
            sub = subs.get(num)
            if not sub:
                continue
            body_paras = prose_paragraphs(sub)
            if not body_paras:
                continue
            picked = take_n_sentences(body_paras[0], 2)
            if picked:
                parts.append(picked)
        # 无 2.1/2.4 子头时，取章首散文段
        if not parts:
            body_paras = prose_paragraphs(calc)
            if body_paras:
                picked = take_n_sentences(body_paras[0], 3)
                if picked:
                    parts.append(picked)
        if parts:
            add_stat("calc_from_二计算过程")
            return "".join(parts)
    dep = find_section(secs, ("二、依赖性质裁定",))
    if dep:
        subs = split_subsections(dep)
        for num in ("2.1", "2.5"):
            sub = subs.get(num)
            if not sub:
                continue
            body_paras = prose_paragraphs(sub)
            if not body_paras:
                continue
            picked = take_n_sentences(body_paras[0], 2)
            if picked:
                parts.append(picked)
        if not parts:
            body_paras = prose_paragraphs(dep)
            if body_paras:
                picked = take_n_sentences(body_paras[0], 3)
                if picked:
                    parts.append(picked)
        if parts:
            add_stat("calc_from_二依赖性质裁定")
            return "".join(parts)
    # 『五、…方法对照与选用建议』/『五、结论与发布建议』替代
    for k in sorted(secs):
        if k.startswith("五、") and ("方法对照" in k or "选用建议" in k or "结论" in k):
            sec = secs[k]
            subs = split_subsections(sec)
            # 优先「方法概述/选用建议/后续」小节，再退「可用结论」
            for num in ("5.2", "5.4", "5.1"):
                sub = subs.get(num)
                if not sub:
                    continue
                body_paras = prose_paragraphs(sub)
                if not body_paras:
                    continue
                picked = take_n_sentences(body_paras[0], 2)
                if picked and len(picked) >= 30:
                    parts.append(picked)
                    break
            if not parts:
                body_paras = prose_paragraphs(sec)
                if body_paras:
                    picked = take_n_sentences(body_paras[0], 3)
                    if picked:
                        parts.append(picked)
            if parts:
                add_stat("calc_from_五方法对照")
                return "".join(parts)
    # 『二、产物与复现』（拆分契约件）替代
    prod = find_section(secs, ("二、产物与复现",))
    if prod:
        body_paras = prose_paragraphs(prod)
        if body_paras:
            picked = take_n_sentences(body_paras[0], 3)
            if picked:
                add_stat("calc_from_二产物与复现")
                return picked
    # 兜底 seed formula（净化内部工程语言）
    if seed and seed.get("formula"):
        add_stat("calc_seed_fallback")
        sents = purify_sentences(strip_md(seed["formula"]), DIRTY_SENT_RE)
        if sents:
            return "".join(sents[:4])
        return strip_md(seed["formula"])[:200]
    add_stat("calc_empty")
    return ""


# ---------------------------------------------------------------------------
# references：『## 参考文献』逐条 {text, url, group}
# ---------------------------------------------------------------------------
REF_INLINE = re.compile(
    r"^(?:\d+[.、\s]+)?(.+?)[\s\u3000]*[：:。；;，,\s\u3000]+(https?://\S+?)(?:[\s\u3000]+[（(].*)?\s*$"
)


def _scrub_ref_text(text: str) -> str:
    # 剥除残留行首编号与行尾验证性/工程性括注
    text = re.sub(r"^\s*\d+[.、\s]+", "", text)
    if not DIRTY_REFS_RE.search(text) and not DIRTY_SENT_RE.search(text):
        return text
    cleaned = re.sub(r"[（(][^（）()]*[）)]", "", text)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip(" ；;，,")
    return cleaned if cleaned else text


def _norm_url(u: str) -> str:
    return (u or "").strip().rstrip("/")


def classify_ref(text: str) -> str:
    """gov → cn → foreign。先官方白名单（且不含英文机构词），再英文机构词，其余国内。"""
    if GOV_INSTITUTION_RE.search(text):
        if not re.search(r"Journal|Press|University|Hirsch|Glänzel|Rasmussen|Barabási|Newman|Borgatti|Granovetter", text):
            return "gov"
    if FOREIGN_INSTITUTION_RE.search(text):
        return "foreign"
    if re.search(r"[A-Za-z]{4,}", text) and not GOV_INSTITUTION_RE.search(text):
        # 长英文串且未命中官方白名单 → foreign
        return "foreign"
    return "cn"


def parse_refs(ref_section: str | None) -> list[dict]:
    if not ref_section:
        return []
    out = []
    for line in ref_section.split("\n"):
        line = line.strip().lstrip("-*").strip()
        if not line or line.startswith(("#", ">")) or line == "---":
            continue
        m = REF_INLINE.match(line)
        if m:
            text, url = strip_md(m.group(1)).rstrip("：: "), m.group(2)
            if text:
                out.append({"text": _scrub_ref_text(text), "url": url})
            continue
        text = strip_md(line)
        if text and len(text) > 3:
            out.append({"text": _scrub_ref_text(text)})
    seen, dedup = set(), []
    for r in out:
        key = r["text"][:60]
        if key in seen:
            add_stat("refs_dedup")
            continue
        seen.add(key)
        dedup.append(r)
    return dedup


def filter_and_group_refs(refs: list[dict]) -> list[dict]:
    kept = []
    for r in refs:
        blob = r.get("text") or ""
        if DIRTY_REFS_RE.search(blob):
            add_stat("refs_dropped_internal")
            continue
        # 『不适用』占位（整节仅占位说明，无外部文献）
        if re.fullmatch(r"[（(]?不适用[。）)]?[。.]?", blob) or blob.startswith("不适用"):
            add_stat("refs_dropped_placeholder")
            continue
        url = r.get("url")
        if url and _norm_url(url) in DEAD_URLS_NORM:
            add_stat("refs_dropped_dead")
            continue
        r2 = {"text": r["text"]}
        if url:
            r2["url"] = url
        r2["group"] = classify_ref(r["text"])
        kept.append(r2)
    # 排序 gov → cn → foreign（组内保持原序）
    order = {"gov": 0, "cn": 1, "foreign": 2}
    kept.sort(key=lambda r: order[r["group"]])
    return kept


# ---------------------------------------------------------------------------
# 单件编译
# ---------------------------------------------------------------------------
def compile_one(stem: str, text: str, seeds: dict) -> dict:
    secs = split_sections(text)
    head = parse_head_fields(text)
    h1 = text.split("\n", 1)[0]
    seed = seeds.get(stem)

    name = extract_name_zh(text, h1, seed)
    add_stat("compiled_ok")

    ref_section = find_section(secs, ("参考文献",))
    refs = parse_refs(ref_section)
    grouped = filter_and_group_refs(refs)
    add_stat("refs_total", len(grouped))
    for r in grouped:
        add_stat(f"refs_group_{r['group']}")

    sup_raw = head["数据支持度"]
    level = extract_support_level(sup_raw)
    if level:
        add_stat("support_level_ok")
    else:
        add_stat("support_level_missing")

    return {
        "metric_id": stem,
        "metric_name_zh": name,
        "req_overview": build_req_overview(secs, seed),
        "calc_logic": build_calc_logic(secs, seed),
        "references": grouped,
        "support": {
            "level": level,
            "verdict_summary": extract_verdict_summary(text, head),
        },
        "applicable_systems": head["适用系统"],
    }


# ---------------------------------------------------------------------------
# 产物落盘（json.dumps 内嵌，防裸反引号/转义问题）
# ---------------------------------------------------------------------------
TS_HEADER = """// GENERATED FILE — 由 gen_popup_info.py 生成，勿手改。
// 源：20261027 批指标调研 md（第三方库指标计算过程，{n} 件）+ cfg_metric-*-seed.yaml
// 拆分族覆盖策略：{policy}
// 生成时间：{ts}

/** 指标弹窗信息（三库共构）：需规概述 / 计算逻辑 / 参考文献 / 支持度 / 适用系统 */
export interface MetricPopupInfo {{
  metric_id: string;
  metric_name_zh: string;
  req_overview: string;
  calc_logic: string;
  references: {{ text: string; url?: string; group: 'gov' | 'cn' | 'foreign' }}[];
  support: {{ level: string; verdict_summary: string }};
  applicable_systems: string;
}}

export const METRIC_POPUP_INFO: Record<string, MetricPopupInfo> = {payload};
"""

JS_HEADER = """// GENERATED FILE — 由 gen_popup_info.py 生成，勿手改。
// 源：20261027 批指标调研 md（第三方库指标计算过程，{n} 件）+ cfg_metric-*-seed.yaml
// 拆分族覆盖策略：{policy}
// 生成时间：{ts}

export const METRIC_POPUP_INFO = {payload};
"""


def write_output(path: Path, data: dict, kind: str, policy: str) -> None:
    payload = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
    n = len(data)
    if kind == "ts":
        content = TS_HEADER.format(n=n, policy=policy, ts=GEN_AT, payload=payload)
    else:
        content = JS_HEADER.format(n=n, policy=policy, ts=GEN_AT, payload=payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    add_stat(f"wrote_{path.name}")


def merge_variant_over_base(base: dict, variant: dict, fam: str) -> dict:
    """拆分族合并：变体（_ZT/_ZS 契约件）字段优先覆盖；空白字段回落原件。

    变体是结构/契约件，四区块常只有适用系统非空；原件（算法库继承件）承载
    完整需规/计算/参考文献。合并原则：
      - metric_name_zh / applicable_systems：变体优先（系统归属是拆分的核心语义）
      - req_overview / calc_logic / references / support：非空者取变体，空则回落原件
      - metric_id 归一为原 ID
    """
    out = dict(base)
    out["metric_id"] = fam
    for field in ("metric_name_zh", "applicable_systems"):
        if variant.get(field):
            out[field] = variant[field]
    for field in ("req_overview", "calc_logic"):
        if variant.get(field):
            out[field] = variant[field]
    if variant.get("references"):
        out["references"] = variant["references"]
    sup_v = variant.get("support") or {}
    sup_b = base.get("support") or {}
    out["support"] = {
        "level": sup_v.get("level") or sup_b.get("level") or "",
        "verdict_summary": sup_v.get("verdict_summary") or sup_b.get("verdict_summary") or "",
    }
    return out


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def load_seeds() -> dict:
    seeds = {}
    for yf in sorted(REGISTRY.glob("cfg_metric-*-seed.yaml")):
        y = yaml.safe_load(yf.read_text(encoding="utf-8"))
        for m in y.get("metrics") or []:
            seeds[m["metric_id"]] = m
    return seeds


def load_matrix_ids() -> set:
    ids = set()
    for yf in sorted(REGISTRY.glob("metric-readiness-matrix-*.yaml")):
        y = yaml.safe_load(yf.read_text(encoding="utf-8"))
        for m in y.get("metrics") or []:
            ids.add(m["metric_id"])
    return ids


def main() -> int:
    files = sorted(MD_DIR.glob("*.md"))
    if len(files) != 573:
        FATALS.append(f"期望 573 份 md，实际 {len(files)}")

    seeds = load_seeds()
    matrix_ids = load_matrix_ids()

    compiled: dict[str, dict] = {}
    for f in files:
        stem = f.stem
        text = f.read_text(encoding="utf-8")
        try:
            compiled[stem] = compile_one(stem, text, seeds)
        except Exception as e:  # noqa: BLE001
            FATALS.append(f"{stem}: {type(e).__name__}: {e}")
            add_stat("compile_error")

    # 基线 key 集（原 ID）：565 = 573 - 8 变体
    baseline_ids = [s for s in compiled if not (s.endswith("_ZT") or s.endswith("_ZS"))]
    add_stat("baseline_ids", len(baseline_ids))

    # 三份产物
    # 1) system-test：key=原 ID，内容=原件
    out_st = {k: compiled[k] for k in baseline_ids}
    write_output(
        OUT_SYSTEM_TEST, out_st, "ts",
        "key=原 ID（20261027 批 565 基线件 + GAP 件；不含 _ZT/_ZS 变体）",
    )

    # 2) topic：同结构，6 族优先 _ZT 版内容（仍以原 ID 为 key；空白回落原件）
    out_topic = dict(out_st)
    zt_overrides = []
    for fam in SPLIT_FAMILIES:
        zt_id = f"{fam}_ZT"
        if zt_id in compiled and fam in out_topic:
            out_topic[fam] = merge_variant_over_base(out_topic[fam], compiled[zt_id], fam)
            zt_overrides.append(f"{zt_id}→{fam}")
    write_output(
        OUT_TOPIC, out_topic, "ts",
        "key=原 ID；6 拆分族优先 _ZT 版（" + "、".join(zt_overrides) + "；空白字段回落原件）",
    )

    # 3) science：ESM js，6 族优先 _ZS 版（空白回落原件）
    out_sci = dict(out_st)
    zs_overrides = []
    for fam in SPLIT_FAMILIES:
        zs_id = f"{fam}_ZS"
        if zs_id in compiled and fam in out_sci:
            out_sci[fam] = merge_variant_over_base(out_sci[fam], compiled[zs_id], fam)
            zs_overrides.append(f"{zs_id}→{fam}")
    write_output(
        OUT_SCIENCE, out_sci, "js",
        "key=原 ID；6 拆分族优先 _ZS 版（" + "、".join(zs_overrides) + "；空白字段回落原件）",
    )

    # 区块非空率
    n_base = len(baseline_ids)
    for field in ("req_overview", "calc_logic", "applicable_systems"):
        add_stat(f"nonempty_{field}", sum(1 for k in baseline_ids if compiled[k].get(field)))
    add_stat("nonempty_refs", sum(1 for k in baseline_ids if compiled[k].get("references")))
    add_stat("nonempty_support_level", sum(1 for k in baseline_ids if compiled[k]["support"]["level"]))
    add_stat("nonempty_verdict", sum(1 for k in baseline_ids if compiled[k]["support"]["verdict_summary"]))
    add_stat("n_baseline", n_base)

    # 矩阵覆盖校验（软）
    uncovered = [k for k in baseline_ids if k not in matrix_ids]
    add_stat("matrix_uncovered", len(uncovered))

    stats = {
        "generated_at": GEN_AT,
        "total_md": len(files),
        "compiled_ok": STATS["compiled_ok"],
        "fatal_errors": FATALS,
        "baseline_ids": n_base,
        "block_nonempty": {
            "req_overview": STATS["nonempty_req_overview"],
            "calc_logic": STATS["nonempty_calc_logic"],
            "references": STATS["nonempty_refs"],
            "support_level": STATS["nonempty_support_level"],
            "verdict_summary": STATS["nonempty_verdict"],
            "applicable_systems": STATS["nonempty_applicable_systems"],
        },
        "block_nonempty_rate": {
            k: round(v / n_base, 4) for k, v in {
                "req_overview": STATS["nonempty_req_overview"],
                "calc_logic": STATS["nonempty_calc_logic"],
                "references": STATS["nonempty_refs"],
                "support_level": STATS["nonempty_support_level"],
                "verdict_summary": STATS["nonempty_verdict"],
                "applicable_systems": STATS["nonempty_applicable_systems"],
            }.items()
        },
        "refs": {
            "total": STATS["refs_total"],
            "group_gov": STATS["refs_group_gov"],
            "group_cn": STATS["refs_group_cn"],
            "group_foreign": STATS["refs_group_foreign"],
            "dropped_dead": STATS["refs_dropped_dead"],
            "dropped_internal": STATS["refs_dropped_internal"],
            "dropped_placeholder": STATS["refs_dropped_placeholder"],
            "dedup": STATS["refs_dedup"],
        },
        "calc_source": {
            "二计算过程": STATS["calc_from_二计算过程"],
            "二依赖性质裁定": STATS["calc_from_二依赖性质裁定"],
            "五方法对照": STATS["calc_from_五方法对照"],
            "二产物与复现": STATS["calc_from_二产物与复现"],
            "seed_fallback": STATS["calc_seed_fallback"],
            "empty": STATS["calc_empty"],
        },
        "req_seed_fallback": STATS["req_overview_seed_fallback"],
        "req_empty": STATS["req_overview_empty"],
        "sentences_dropped_dirty": STATS["sentences_dropped_dirty"],
        "outputs": {
            "system_test": str(OUT_SYSTEM_TEST),
            "topic": str(OUT_TOPIC),
            "science": str(OUT_SCIENCE),
        },
        "matrix_uncovered": STATS["matrix_uncovered"],
    }
    STATS_PATH.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({k: v for k, v in stats.items() if k != "fatal_errors"}, ensure_ascii=False, indent=2))
    if FATALS:
        print("FATALS:", FATALS[:10], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
