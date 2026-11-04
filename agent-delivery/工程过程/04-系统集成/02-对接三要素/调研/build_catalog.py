# -*- coding: utf-8 -*-
"""Build field catalog and metric-support table from _raw_schema.json.

Read-only. No connection string and no password. Support labels describe
whether a same-theme result table exists in the Jiuxin Doris library.
They do not change metric口径 and they do not mean the metric is aligned.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "_raw_schema.json"

GROUPS = (
    ("ads_talent_", "人才"),
    ("ads_technology_", "技术"),
    ("ads_institution_", "科研机构"),
    ("ads_research_problem_", "研究问题"),
    ("ads_research_outcome_", "研究问题"),
    ("ads_discipline_", "学科"),
    ("ads_emerging_", "新兴主题"),
    ("ads_topic_", "新兴主题"),
    ("ads_geo_", "地理"),
    ("ads_location", "地理"),
    ("ads_paper_", "文献"),
    ("ads_patent_", "文献"),
    ("ads_project_", "文献"),
    ("ads_media_", "媒体"),
    ("ads_recommendation_", "推荐"),
    ("ads_resource_", "资源"),
    ("ads_city_subfield_resource_", "资源"),
    ("ads_research_resource_", "资源"),
    ("ads_shenzhen_institution_", "科研机构"),
    ("ads_sz_gkx_", "产业"),
    ("ads_industry", "产业"),
    ("ads_scientific_update_signal", "研究问题"),
)


def group_of(name):
    for prefix, label in GROUPS:
        if name.startswith(prefix):
            return label
    return "其他"


# (metric_id, 中文名, 域, algorithm_type, 候选表, 字段名片段, 期望档)
# 期望档：结果表在 / 原料在 / 还没有
# 候选表行数全 0，或字段片段一个都对不上且期望是结果表在 → 降一档
METRICS = [
    ("M_TECH_BASE_96_1", "技术基础指标模型构建", "技术", "third_party", ["ads_technology_profile", "ads_technology_yearly_metrics"], ["paper_count", "patent_count"], "结果表在"),
    ("M_TECH_COMPOSITE_SCORE", "评估综合得分", "技术", "third_party", ["ads_technology_region_assessment", "ads_technology_stage_assessment"], ["composite", "overall_score", "total_score"], "结果表在"),
    ("M_TECH_CONVERT_BOTTLENECK", "技术转化瓶颈识别", "技术", "third_party", ["ads_technology_bottleneck_assessment"], ["bottleneck"], "结果表在"),
    ("M_TECH_DEEP_130_1", "全景技术链模型", "技术", "third_party", ["ads_technology_graph_node", "ads_technology_graph_edge", "ads_technology_profile"], ["chain_role", "is_chain_connected"], "结果表在"),
    ("M_TECH_DEEP_131_1", "深圳技术链模型", "技术", "third_party", ["ads_technology_region_assessment", "ads_technology_region_yearly_metrics"], [], "原料在"),
    ("M_TECH_DEEP_132_1", "技术发展历程模型", "技术", "third_party", ["ads_technology_evolution_yearly", "ads_technology_evolution_edge", "ads_technology_evolution_path_step"], [], "结果表在"),
    ("M_TECH_DEEP_133_1", "深圳细分领域分布模型", "技术", "third_party", ["ads_technology_region_yearly_metrics", "ads_technology_community"], [], "原料在"),
    ("M_TECH_DEEP_134_1", "技术前沿热点领域识别模型", "技术", "third_party", ["ads_technology_hotspot_snapshot", "ads_technology_hotspot_signal"], ["hotspot"], "结果表在"),
    ("M_TECH_DEEP_135_1", "技术产业化潜力识别模型", "技术", "third_party", ["ads_technology_potential_assessment", "ads_technology_potential_dimension"], ["potential"], "结果表在"),
    ("M_TECH_DEEP_136_1", "技术转化瓶颈堵点原因识别模型", "技术", "third_party", ["ads_technology_bottleneck_assessment", "ads_technology_bottleneck_evidence"], ["bottleneck"], "结果表在"),
    ("M_TECH_DEEP_137_1", "技术阶段分析模型", "技术", "third_party", ["ads_technology_stage_assessment"], ["stage_code"], "结果表在"),
    ("M_TECH_DEEP_138_1", "深圳技术发展问题识别模型", "技术", "third_party", ["ads_technology_region_assessment"], ["problem", "risk", "pain"], "原料在"),
    ("M_TECH_DEEP_139_1", "深圳技术发展机遇识别模型", "技术", "third_party", ["ads_technology_region_assessment"], ["opportunity", "chance"], "原料在"),
    ("M_TECH_DEEP_140_1", "深圳技术发展重点布局领域推荐模型", "技术", "third_party", ["ads_technology_region_assessment", "ads_technology_community"], ["recommend", "layout", "priority"], "原料在"),
    ("M_TECH_DS_07_TECH_INNOV_002", "专利质量评估", "技术", "MODEL", ["ads_technology_patent", "ads_patent_profile"], ["quality"], "原料在"),
    ("M_TECH_DS_07_TECH_INNOV_004", "技术创新力综合评估", "技术", "MODEL", ["ads_technology_profile", "ads_technology_yearly_metrics"], ["innovation", "composite"], "原料在"),
    ("M_TECH_DS_07_TECH_INNOV_006", "技术创新趋势预测", "技术", "MODEL", ["ads_technology_yearly_metrics", "ads_technology_evolution_yearly"], ["forecast", "predict", "trend"], "原料在"),
    ("M_TECH_EDGE_STRENGTH", "技术–技术关联强度", "技术", "third_party", ["ads_technology_graph_edge"], ["strength", "weight"], "结果表在"),
    ("M_TECH_ENTITY_INFLUENCE", "技术点影响力 / 实体优先级", "技术", "third_party", ["ads_technology_graph_node"], ["influence", "priority", "importance"], "结果表在"),
    ("M_TECH_ENTITY_REL", "实体关联关系网", "技术", "third_party", ["ads_technology_graph_edge", "ads_technology_graph_node"], [], "结果表在"),
    ("M_TECH_ENTITY_TOP5", "根节点 Top5 关键实体与关联强度", "技术", "third_party", ["ads_technology_graph_node", "ads_technology_graph_edge"], ["top5", "rank"], "原料在"),
    ("M_TECH_GRAPH_104_1", "技术实体识别构建", "技术", "third_party", ["ads_technology_graph_node", "ads_technology_profile"], [], "结果表在"),
    ("M_TECH_GRAPH_105_1", "技术实体关系抽取", "技术", "third_party", ["ads_technology_graph_edge"], [], "结果表在"),
    ("M_TECH_GRAPH_STRUCT", "技术点网图结构", "技术", "third_party", ["ads_technology_graph_node", "ads_technology_graph_edge"], [], "结果表在"),
    ("M_TECH_HEAT_INDEX", "技术热点热度指数", "技术", "third_party", ["ads_technology_hotspot_snapshot", "ads_technology_hotspot_signal"], ["heat", "hot"], "结果表在"),
    ("M_TECH_HEAT_QUERY", "查询结果·技术热度", "技术", "STAT", ["ads_technology_hotspot_snapshot", "ads_technology_yearly_metrics"], ["heat", "hot"], "结果表在"),
    ("M_TECH_INVEST_AMOUNT", "技术投资额", "技术", "STAT", ["ads_technology_profile"], ["investment_estimate"], "结果表在"),
    ("M_TECH_LIFE_STAGE", "技术发展阶段", "技术", "third_party", ["ads_technology_stage_assessment"], ["stage_code"], "结果表在"),
    ("M_TECH_MATURITY_LEVEL", "技术成熟度", "技术", "third_party", ["ads_technology_stage_assessment"], ["maturity"], "原料在"),
    ("M_TECH_OUTPUT_SCALE", "技术规模", "技术", "STAT", ["ads_technology_yearly_metrics", "ads_technology_profile"], ["paper_count", "patent_count"], "结果表在"),
    ("M_TECH_PAPER_PATENT_CNT", "技术点论文量 / 专利量", "技术", "STAT", ["ads_technology_profile", "ads_technology_paper", "ads_technology_patent"], ["paper_count", "patent_count"], "结果表在"),
    ("M_TECH_PATH_CENTRALITY", "中心度", "技术", "third_party", ["ads_technology_graph_node", "ads_technology_evolution_path_step"], ["centrality"], "结果表在"),
    ("M_TECH_PATH_KEYNODE", "关键节点重要性", "技术", "third_party", ["ads_technology_graph_node"], ["importance", "key_node", "priority"], "结果表在"),
    ("M_TECH_PATH_PRIORITY", "节点优先级 / 重要度", "技术", "third_party", ["ads_technology_graph_node"], ["priority", "importance"], "结果表在"),
    ("M_TECH_POTENTIAL_SCORE", "技术产业化潜力评分", "技术", "third_party", ["ads_technology_potential_assessment"], ["potential", "score"], "结果表在"),
    ("M_TECH_REL_STRENGTH", "技术关联强度", "技术", "third_party", ["ads_technology_graph_edge"], ["strength", "weight"], "结果表在"),
    ("M_TECH_STAGE_JUDGE", "技术阶段判定", "技术", "third_party", ["ads_technology_stage_assessment"], ["stage_code", "stage_confidence"], "结果表在"),
    ("M_TECH_SZ_ASSESS", "深圳技术潜力与阶段综合评估", "技术", "third_party", ["ads_technology_region_assessment", "ads_technology_stage_assessment"], [], "原料在"),
    ("M_TECH_TOPIC_HEAT", "技术话题热度", "技术", "third_party", ["ads_technology_hotspot_snapshot", "ads_emerging_topic_yearly_metrics"], ["heat", "hot"], "结果表在"),
    ("M_TALENT_ACADEMIC_SCORE", "人才学术力指数", "人才", "third_party", ["ads_talent_profile", "ads_talent_yearly_metrics"], ["academic_capability"], "结果表在"),
    ("M_TALENT_ATTRACT_SCORE", "引入人才推荐指数", "人才", "third_party", ["ads_talent_potential_result"], ["attract", "recommend"], "原料在"),
    ("M_TALENT_BASE_98_1", "人才基础指标模型构建", "人才", "third_party", ["ads_talent_profile", "ads_talent_yearly_metrics"], ["paper_count", "h_index"], "结果表在"),
    ("M_TALENT_CULTIVATE_SCORE", "培育人才推荐指数", "人才", "third_party", ["ads_talent_potential_result"], ["cultivate", "recommend"], "原料在"),
    ("M_TALENT_DEEP_156_1", "重点人才识别模型", "人才", "third_party", ["ads_talent_profile", "ads_emerging_topic_key_talent"], ["is_academician", "key_talent"], "结果表在"),
    ("M_TALENT_DEEP_157_1", "人才流动追踪模型", "人才", "third_party", ["ads_talent_mobility_event", "ads_talent_mobility_yearly_flow", "ads_talent_mobility_flow_detail"], [], "结果表在"),
    ("M_TALENT_DEEP_158_1", "高校学院新培育人才模型", "人才", "third_party", ["ads_talent_potential_result", "ads_talent_experience"], ["univ", "college", "new_talent"], "原料在"),
    ("M_TALENT_DEEP_159_1", "深圳重点人才优势和短板分析模型", "人才", "third_party", ["ads_talent_yearly_location", "ads_talent_profile"], ["advantage", "shortcoming", "gap"], "原料在"),
    ("M_TALENT_DEEP_160_1", "人才关系链模型", "人才", "third_party", ["ads_talent_collaborator", "ads_talent_similarity", "ads_talent_taxonomy_relation"], [], "结果表在"),
    ("M_TALENT_DEEP_161_1", "人才供需分析评价模型", "人才", "third_party", ["ads_talent_yearly_metrics", "ads_talent_profile"], ["supply", "demand"], "原料在"),
    ("M_TALENT_DEEP_162_1", "人才学术力评估模型", "人才", "third_party", ["ads_talent_profile", "ads_talent_research_achievement"], ["academic_capability"], "结果表在"),
    ("M_TALENT_DEEP_163_1", "人才产业力评估模型", "人才", "third_party", ["ads_talent_industry_activity", "ads_talent_industry_capability_simulation", "ads_talent_yearly_metrics"], ["industrial_capability"], "结果表在"),
    ("M_TALENT_DEEP_164_1", "招入人才推荐模型", "人才", "third_party", ["ads_talent_potential_result"], ["attract", "recommend", "recruit"], "原料在"),
    ("M_TALENT_DEEP_165_1", "培育人才布局模型", "人才", "third_party", ["ads_talent_potential_result", "ads_talent_taxonomy"], ["cultivate", "layout"], "原料在"),
    ("M_TALENT_DS_16_TALENT_RECRUIT_005", "沟通障碍智能检测", "人才", "third_party", [], ["barrier", "communication"], "还没有"),
    ("M_TALENT_DS_16_TALENT_RECRUIT_006", "文化融合风险评估", "人才", "third_party", [], ["culture"], "还没有"),
    ("M_TALENT_DS_16_TALENT_RECRUIT_007", "国际流动壁垒分析", "人才", "third_party", ["ads_talent_mobility_event"], ["barrier", "visa", "restriction"], "原料在"),
    ("M_TALENT_DS_16_TALENT_RECRUIT_010", "引进阻力量化评分", "人才", "third_party", [], ["resistance", "barrier_score"], "还没有"),
    ("M_TALENT_DS_16_TALENT_RECRUIT_013", "高精度成本模型构建", "人才", "third_party", [], ["cost"], "还没有"),
    ("M_TALENT_DS_16_TALENT_RECRUIT_025", "团队组合与协同分析", "人才", "third_party", ["ads_talent_collaborator", "ads_talent_similarity"], ["team"], "原料在"),
    ("M_TALENT_FLOW_TRACK", "人才流动追踪", "人才", "third_party", ["ads_talent_mobility_event", "ads_talent_mobility_yearly_flow"], [], "结果表在"),
    ("M_TALENT_GRAPH_110_1", "人才实体识别构建", "人才", "third_party", ["ads_talent_profile"], [], "结果表在"),
    ("M_TALENT_GRAPH_111_1", "人才实体关系抽取", "人才", "third_party", ["ads_talent_collaborator", "ads_talent_taxonomy_relation"], [], "结果表在"),
    ("M_TALENT_INDUSTRY_SCORE", "人才产业力指数", "人才", "third_party", ["ads_talent_yearly_metrics", "ads_talent_industry_capability_simulation"], ["industrial_capability"], "结果表在"),
    ("M_TALENT_ORG_DIST", "重点人才机构分布", "人才", "third_party", ["ads_talent_profile", "ads_talent_experience"], ["current_institution"], "结果表在"),
    ("M_TALENT_REGIONAL_DIST", "重点人才区域分布", "人才", "third_party", ["ads_talent_yearly_location", "ads_talent_profile"], ["country", "province", "city"], "结果表在"),
    ("M_TALENT_RELATION_NET", "重点人才关系链结构", "人才", "third_party", ["ads_talent_collaborator", "ads_talent_similarity"], [], "结果表在"),
    ("M_TALENT_STRUCT_QUERY", "查询结果·人才结构", "人才", "STAT", ["ads_talent_yearly_discipline", "ads_talent_taxonomy"], [], "结果表在"),
    ("M_TALENT_SUPPLY_STRUCT", "人才供给情况", "人才", "third_party", ["ads_talent_yearly_metrics"], ["supply"], "原料在"),
    ("M_TALENT_SZ_STATUS", "深圳人才现状与优劣势", "人才", "third_party", ["ads_talent_yearly_location"], ["advantage", "shenzhen"], "原料在"),
    ("M_TALENT_SZ_SUPPLY_DEMAND", "深圳人才供需评价", "人才", "third_party", ["ads_talent_yearly_metrics", "ads_talent_yearly_location"], ["supply", "demand"], "原料在"),
    ("M_TALENT_UNIV_NEW", "高校新培育人才", "人才", "third_party", ["ads_talent_potential_result", "ads_talent_experience"], ["univ", "new_talent"], "原料在"),
    ("M_ORG_ATTENTION_TREND", "科研关注度", "机构", "third_party", ["ads_institution_yearly_metrics"], ["attention", "cited_by_count"], "原料在"),
    ("M_ORG_ATTRACT_SCORE", "科研机构招引推荐指数", "机构", "third_party", ["ads_institution_profile"], ["attract", "recommend"], "原料在"),
    ("M_ORG_BASE_99_1", "科研机构基础指标模型构建", "机构", "third_party", ["ads_institution_profile", "ads_institution_yearly_metrics"], ["paper_count", "talent_count"], "结果表在"),
    ("M_ORG_COLLAB_CHAIN", "科研合作关系链条", "机构", "third_party", ["ads_institution_collaboration_yearly"], [], "结果表在"),
    ("M_ORG_CULTIVATE_SCORE", "科研机构扶持推荐指数", "机构", "third_party", ["ads_institution_profile"], ["cultivate", "support_score"], "原料在"),
    ("M_ORG_DEEP_149_1", "科研机构重点技术领域布局模型", "机构", "third_party", ["ads_institution_discipline_profile", "ads_institution_technology_power", "ads_institution_topic_entry"], [], "结果表在"),
    ("M_ORG_DEEP_150_1", "科研机构发展历程模型", "机构", "third_party", ["ads_institution_yearly_metrics"], [], "原料在"),
    ("M_ORG_DEEP_151_1", "深圳科研机构优势分析模型", "机构", "third_party", ["ads_institution_profile", "ads_institution_yearly_metrics"], ["advantage"], "原料在"),
    ("M_ORG_DEEP_152_1", "深圳科研机构痛难点识别模型", "机构", "third_party", ["ads_institution_profile"], ["pain", "bottleneck"], "原料在"),
    ("M_ORG_DEEP_153_1", "科研合作关系链条模型", "机构", "third_party", ["ads_institution_collaboration_yearly"], [], "结果表在"),
    ("M_ORG_DEEP_154_1", "科研机构引入推荐模型", "机构", "third_party", ["ads_institution_profile"], ["attract", "recommend"], "原料在"),
    ("M_ORG_DEEP_155_1", "科研机构扶持推荐模型", "机构", "third_party", ["ads_institution_profile"], ["cultivate", "support"], "原料在"),
    ("M_ORG_GRAPH_114_1", "科研机构实体识别构建", "机构", "third_party", ["ads_institution_profile"], [], "结果表在"),
    ("M_ORG_GRAPH_115_1", "科研机构实体关系抽取", "机构", "third_party", ["ads_institution_collaboration_yearly"], [], "结果表在"),
    ("M_ORG_INDUSTRY_COVER", "科研机构产业领域覆盖", "机构", "third_party", ["ads_institution_industry"], [], "结果表在"),
    ("M_ORG_NEW_TREND", "新增科研机构趋势", "机构", "third_party", ["ads_institution_yearly_metrics", "ads_institution_profile"], ["new_institution", "established_year"], "原料在"),
    ("M_ORG_PERF_QUERY", "查询结果·科研机构绩效", "机构", "STAT", ["ads_institution_yearly_metrics"], ["paper_count", "fwci"], "结果表在"),
    ("M_ORG_SZ_ADVANTAGE", "深圳科研机构优势", "机构", "third_party", ["ads_institution_profile", "ads_geo_yearly_metrics"], ["advantage"], "原料在"),
    ("M_ORG_SZ_PAINPOINT", "深圳科研机构痛难点", "机构", "third_party", ["ads_institution_profile"], ["pain", "bottleneck"], "还没有"),
    ("M_ORG_SZ_STATUS", "深圳科研机构现状解读", "机构", "third_party", ["ads_institution_profile", "ads_geo_yearly_institution_type_metrics"], [], "原料在"),
    ("M_ORG_TECH_LAYOUT", "科研机构技术领域布局", "机构", "third_party", ["ads_institution_discipline_profile", "ads_institution_technology_power"], [], "结果表在"),
    ("M_ORG_TECH_SCORE", "科研机构技术力评价与对比", "机构", "third_party", ["ads_institution_technology_power"], ["power", "score"], "结果表在"),
]


def main():
    data = json.loads(RAW.read_text(encoding="utf-8"))
    tables = {t["table"]: t for t in data["tables"]}
    cols = {}
    for c in data["columns"]:
        cols.setdefault(c["table"], []).append(c)

    with (HERE / "表清单.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["表", "分组", "行数", "字段数"])
        for t in data["tables"]:
            w.writerow([t["table"], group_of(t["table"]), t["table_rows"], t["column_count"]])

    with (HERE / "字段清单.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["表", "序号", "字段", "类型", "可空", "键", "注释"])
        for c in data["columns"]:
            w.writerow([
                c["table"], c.get("pos"), c["column"], c.get("type"),
                c.get("nullable"), c.get("key"), c.get("comment") or "",
            ])

    rows_out = []
    for mid, name, domain, algo, cands, needles, expect in METRICS:
        present = [t for t in cands if t in tables]
        filled = [t for t in present if (tables[t]["table_rows"] or 0) > 0]
        empty = [t for t in present if (tables[t]["table_rows"] or 0) == 0]
        hits = []
        if needles:
            for t in filled:
                for c in cols.get(t, []):
                    cl = c["column"].lower()
                    if any(n in cl for n in needles):
                        hits.append(c["column"])
                        break
        if expect == "还没有" and not filled:
            level = "还没有"
        elif not filled:
            level = "还没有"
        elif expect == "结果表在" and needles and not hits:
            level = "原料在"
        else:
            level = expect
        note = []
        if filled:
            note.append("有行：" + "、".join(filled))
        if empty:
            note.append("空表：" + "、".join(empty))
        if needles and filled and not hits:
            note.append("候选表里没有字段名片段 " + "/".join(needles))
        if level == "还没有" and not present:
            note.append("没有同主题结果表")
        note.append("口径是否等于指标库：还没有。不标已对齐。")
        rows_out.append((mid, name, domain, algo, "draft", "mock", level, "、".join(filled), "；".join(note)))

    with (HERE / "指标支持.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric_id", "中文名", "域", "algorithm_type", "D1", "D4", "库内支持", "有行的候选表", "说明"])
        w.writerows(rows_out)

    from collections import Counter
    c = Counter(r[6] for r in rows_out)
    by_dom = {}
    for r in rows_out:
        by_dom.setdefault(r[2], Counter())[r[6]] += 1
    print("metrics", len(rows_out), dict(c))
    for d, cc in by_dom.items():
        print(d, dict(cc))
    print("还没有:")
    for r in rows_out:
        if r[6] == "还没有":
            print(r[0], r[1])


if __name__ == "__main__":
    main()
