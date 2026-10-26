#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_ORG_DEEP_153_1 科研合作关系链条模型
需求来源：同目录 深度分析.md 序号 153

构图：dwd_scholar_coauthor（1,187,606 条真实共著关系）→ 机构级无向加权图。
  节点 = 机构名（学者所属机构 × 合著者所属机构）
  边权 = Σ co_paper_count（合作强度），边数 = 共著记录数（合作频率）
指标：合作链总量、合作密度（深圳节点子图）、核心节点（加权度）、跨区域合作占比。
数据限制：科研项目表无合作机构字段；专利共同申请人表仅 0.68% 采样且深圳机构仅命中 11 条。
"""
import os, sys, json, re, datetime, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

MID = "M_ORG_DEEP_153_1"
OUT = os.path.join(HERE, f"{MID}_out.json")
SNAP = os.path.join(HERE, "_snapshots", "org_pop_20261021.json")

# ---------------------------------------------------------------- 机构名清洗
# 共著表机构名未标准化：带「中国/中国广东省」前缀、带「教授/研究员」头衔、
# 全半角括号混用、同一机构多种写法。以下规则只做确定性归一，不做模糊匹配。
TITLE = r"(特聘教授|助理教授|副教授|教授|副研究员|助理研究员|研究员|院士|博士|讲师|工程师|主任医师|副主任医师)$"
ALIAS = {
    "哈尔滨工业大学深圳": "哈尔滨工业大学（深圳）",
    "哈尔滨工业大学(深圳)": "哈尔滨工业大学（深圳）",
    "哈尔滨工业大学深圳校区": "哈尔滨工业大学（深圳）",
    "哈尔滨工业大学深圳研究生院": "哈尔滨工业大学（深圳）",
    "深圳先进技术研究院": "中国科学院深圳先进技术研究院",
    "中国深圳先进技术大学": "深圳先进技术大学",
    "清华大学深圳研究生院": "清华大学深圳国际研究生院",
}


def canon(s):
    s = (s or "").strip()
    s = s.replace("\u3000", " ")
    s = re.sub(r"\s+", "", s)
    s = s.replace("(", "（").replace(")", "）")
    # 只去「中国/广东」+「深圳」的地理前缀，避免误伤「中国科学院」「中国农业科学院」
    s = re.sub(r"^(中国广东省|中国深圳|中国广东|广东省|广东)(?=深圳)", "", s)
    s = re.sub(r"^中国(?=深圳)", "", s)
    s = re.sub(r"^深圳市", "深圳", s)
    s = re.sub(r"^(特聘教授|助理教授|副教授|教授)，", "", s)
    for _ in range(2):
        s = re.sub(TITLE, "", s)
    s = ALIAS.get(s, s)
    return s


def split_orgs(s):
    """一个字段里并列多个机构（「深圳大学，武汉大学」）时拆开，权重按组合数均分。"""
    parts = [canon(x) for x in re.split(r"[，,；;]", s or "")]
    parts = [p for p in parts if p]
    return parts or [""]


def load_snap():
    with open(SNAP, encoding="utf-8") as f:
        return json.load(f)


def main():
    snap = load_snap()
    edges_raw = snap["coauthor_sz_edges"]
    graph = {}
    self_loop = 0
    dropped_empty = 0
    for a, b, n, w in edges_raw:
        As, Bs = split_orgs(a), split_orgs(b)
        if not As[0] or not Bs[0]:
            dropped_empty += 1
            continue
        parts = len(As) * len(Bs)
        for A in As:
            for B in Bs:
                if A == B:
                    self_loop += 1
                    continue
                key = tuple(sorted((A, B)))
                d = graph.setdefault(key, {"n": 0, "w": 0})
                if parts == 1:
                    d["n"] += n
                    d["w"] += w
                else:  # 多机构串：权重按组合数均分，保证总强度守恒
                    d["n"] += n / parts
                    d["w"] += w / parts

    nodes = set()
    for (a, b) in graph:
        nodes.add(a)
        nodes.add(b)
    sz_nodes = {n for n in nodes if "深圳" in n}

    def is_sz(n):
        return "深圳" in n

    wdeg = {n: 0 for n in nodes}
    deg = {n: 0 for n in nodes}
    freq = {n: 0 for n in nodes}
    for (a, b), d in graph.items():
        deg[a] += 1
        deg[b] += 1
        wdeg[a] += d["w"]
        wdeg[b] += d["w"]
        freq[a] += d["n"]
        freq[b] += d["n"]

    sz_core = sorted(sz_nodes, key=lambda n: -wdeg[n])
    intra_sz = [(a, b) for (a, b) in graph if is_sz(a) and is_sz(b)]
    cross = [(a, b) for (a, b) in graph if is_sz(a) != is_sz(b)]
    foreign = [(a, b) for (a, b) in graph if is_sz(a) or is_sz(b)]
    n_possible = len(sz_nodes) * (len(sz_nodes) - 1) / 2
    density = len(intra_sz) / n_possible if n_possible else 0

    def top_partners(org, k=8):
        out = []
        for (a, b), d in graph.items():
            if a == org or b == org:
                other = b if a == org else a
                out.append({"partner": other, "records": round(d["n"]), "strength": round(d["w"])})
        out.sort(key=lambda x: -x["strength"])
        return out[:k]

    chains = []
    for org in sz_core[:10]:
        chains.append({"org": org, "degree": deg[org], "strength": round(wdeg[org]),
                       "records": round(freq[org]), "top_partners": top_partners(org, 5)})

    res = {
        "metric_id": MID,
        "name": "科研合作关系链条模型",
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "source": "gkx 真源快照 _snapshots/org_pop_20261021.json（2026-10-21 11:25 实测；"
                  "开发库 111.198.38.90:34306 当日 TCP 不可达，未参与本次复算）",
        "probes": {
            "dwd_scholar_coauthor": int(snap["coauthor_stats"]["n"]),
            "共著学者": int(snap["coauthor_stats"]["s"]),
            "共著表机构名去重": int(snap["coauthor_stats"]["orgs"]),
            "深圳相关边（原始分组）": len(edges_raw),
            "深圳相关边（清洗去自环后）": len(graph),
            "dwd_zh_project（无合作机构字段）": int(snap["project_stats"]["n"]),
            "dwd_patent_applicants（采样）": int(snap["applicant_sample"]["patents"]),
            "采样中深圳机构申请人行": 11,
        },
        "compute": {
            "n_nodes": len(nodes),
            "n_edges": len(graph),
            "n_sz_nodes": len(sz_nodes),
            "total_strength": round(sum(d["w"] for d in graph.values())),
            "intra_sz_edges": len(intra_sz),
            "cross_edges": len(cross),
            "density_sz": round(density, 6),
            "density_note": f"{len(intra_sz)} / C({len(sz_nodes)},2) = {n_possible:.0f}",
            "self_loop_edges": self_loop,
            "dropped_empty_org": dropped_empty,
            "degree_dist": {"min": min(deg.values()), "max": max(deg.values()),
                            "mean": round(statistics.mean(deg.values()), 2),
                            "median": statistics.median(deg.values())},
            "strength_dist": {"min": round(min(wdeg.values()), 2), "max": round(max(wdeg.values()), 2),
                              "mean": round(statistics.mean(wdeg.values()), 2),
                              "median": statistics.median(wdeg.values())},
            "sz_core_nodes": [{"org": n, "degree": deg[n], "strength": round(wdeg[n]), "records": round(freq[n])}
                              for n in sz_core[:20]],
            "chains": chains,
            "top_nodes_overall": sorted(
                [{"org": n, "degree": deg[n], "strength": round(wdeg[n]), "is_sz": is_sz(n)} for n in nodes],
                key=lambda x: -x["strength"])[:20],
        },
        "disclosure": [
            "合作边只来自论文共著（dwd_scholar_coauthor，1,187,606 条），不含科研项目合作与专利共同申请："
            "dwd_zh_project 的 participating_institution 为单一机构字段（多机构行 0 条），"
            "dwd_patent_applicants 仅 20,000 件专利采样（占专利主表 0.68%），深圳机构仅命中 11 行。",
            "共著表机构名未标准化（深圳侧出现 254 种写法，含「XX大学 教授」等头衔串），已按别名表归并，"
            f"归并后深圳节点 {len(sz_nodes)} 个；相比 1,014 家登记底册仍有覆盖缺口与残余误并。",
            "共著表中 166,427 条记录合著者机构为空，无法落边；深圳相关边原始分组 1,687 组，"
            f"去掉自环（{self_loop}）、空机构（{dropped_empty}）并双向归并后为 {len(graph)} 条，规模有限。",
            "需求要求的「跨领域合作特征」需要 IPC/学科标签，共著表无学科字段，本轮未实现。",
            "dwd_scholar 仅 21,316 人（深圳 194 人），相对真实科研合作体量是稀疏采样，网络结论只作结构验证。",
        ],
        "support_judgment": "部分支持",
        "support_reason": f"可用真实共著关系构建机构级加权合作网络（清洗后 {len(graph)} 条深圳相关边、{len(sz_nodes)} 个深圳节点，"
                          "核心节点与伙伴可解释），但项目合作无字段、专利共同申请仅 0.68% 采样、跨领域特征无标签 → 部分支持。",
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: res[k] for k in ("compute", "support_judgment")}, ensure_ascii=False, indent=1, default=str)[:6000])


if __name__ == "__main__":
    main()
