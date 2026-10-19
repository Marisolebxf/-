# -*- coding: utf-8 -*-
"""SCI-INT-C05 生成：把 C05-collect 的原始 structure_escalation 提法归并成规范标准层结构卡。
运行：python 产物/_work/C05-build.py  -> 写 产物/SCI-INT-C05.yaml
映射（原始提法 → 规范卡）在 MAP 中手工维护；元数据（页面/源卡/指标/久新行/消费方）从源产物现算。"""
import importlib.util
import pathlib
import re
import sys

import yaml

sys.stdout.reconfigure(encoding="utf-8")
WORK = pathlib.Path(__file__).resolve().parent
BASE = WORK.parent

spec = importlib.util.spec_from_file_location("collect", WORK / "C05-collect.py")
collect_mod = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[0]]
spec.loader.exec_module(collect_mod)
RAW = collect_mod.collect()
RAW_BY_ID = {r["raw_id"]: r for r in RAW}

JX = "待确认"
LW = "human:李伟"

# ---------------------------------------------------------------- 原始提法 → 规范卡（primary + also）
MAP = {
    "SCI-INT-B01:": ("INT-C-X-480", ["INT-C-X-481", "INT-C-X-482"]),
    "SCI-INT-B01:patterns[7]": ("INT-C-X-481", []),
    "SCI-INT-B01:patterns[10]": ("INT-C-X-480", ["INT-C-X-482"]),
    "SCI-INT-C01:INT-C-TAL-041": ("INT-C-TAL-401", ["INT-C-TAL-400", "INT-C-X-480"]),
    "SCI-INT-C01:INT-C-TAL-042": ("INT-C-TAL-404", ["INT-C-X-490"]),
    "SCI-INT-C01:INT-C-TAL-060": ("INT-C-X-490", ["INT-C-TAL-400"]),
    "SCI-INT-C01:INT-C-TAL-061": ("INT-C-X-490", ["INT-C-TAL-404", "INT-C-TAL-402"]),
    "SCI-INT-C01:INT-C-TAL-070": ("INT-C-TAL-400", []),
    "SCI-INT-C01:INT-C-TAL-071": ("INT-C-TAL-402", ["INT-C-TAL-406"]),
    "SCI-INT-C01:INT-C-TAL-072": ("INT-C-TAL-401", []),
    "SCI-INT-C02:INT-C-TECH-151": ("INT-C-TECH-420", ["INT-C-TECH-426", "INT-C-X-480"]),
    "SCI-INT-C02:INT-C-TECH-152": ("INT-C-TECH-424", ["INT-C-TECH-426"]),
    "SCI-INT-C02:INT-C-TECH-170": ("INT-C-X-490", ["INT-C-TECH-420"]),
    "SCI-INT-C02:INT-C-TECH-171": ("INT-C-X-490", ["INT-C-TECH-424"]),
    "SCI-INT-C02:INT-C-TECH-180": ("INT-C-TECH-420", []),
    "SCI-INT-C02:INT-C-TECH-181": ("INT-C-TECH-421", ["INT-C-TECH-422"]),
    "SCI-INT-C02:INT-C-TECH-182": ("INT-C-TECH-423", []),
    "SCI-INT-C03:INT-C-ORG-240": ("INT-C-ORG-440", []),
    "SCI-INT-C03:INT-C-ORG-241": ("INT-C-ORG-441", []),
    "SCI-INT-C03:INT-C-ORG-242": ("INT-C-ORG-442", []),
    "SCI-INT-C04:INT-C-TECH-300": ("INT-C-X-490", ["INT-C-TECH-420"]),
    "SCI-INT-C04:INT-C-TAL-310": ("INT-C-X-490", ["INT-C-TAL-400"]),
    "SCI-INT-C04:INT-C-ORG-320": ("INT-C-X-490", ["INT-C-ORG-440"]),
    "SCI-INT-C04:INT-C-TECH-340": ("INT-C-X-490", ["INT-C-TECH-424"]),
    "SCI-INT-C04:INT-C-TECH-341": ("INT-C-X-490", ["INT-C-TECH-424"]),
    "SCI-INT-C04:INT-C-TAL-350": ("INT-C-X-490", ["INT-C-TAL-404"]),
    "SCI-INT-C04:INT-C-TAL-351": ("INT-C-X-490", ["INT-C-TAL-402"]),
    "SCI-INT-C04:INT-C-TAL-352": ("INT-C-X-490", ["INT-C-TAL-404"]),
    "SCI-INT-C04:INT-C-ORG-360": ("INT-C-X-490", ["INT-C-X-460"]),
    "SCI-INT-C04:space_plan": ("INT-C-X-490", []),
    "SCI-INT-C04:write_back_conflicts.items[0]": ("INT-C-TECH-426", []),
    "SCI-INT-C04:write_back_conflicts.items[1]": ("INT-C-TECH-428", ["INT-C-TECH-427"]),
    "SCI-INT-C04:write_back_conflicts.items[2]": ("INT-C-TECH-420", []),
    "SCI-INT-C04:write_back_conflicts.items[3]": ("INT-C-TAL-403", []),
    "SCI-INT-A01:INT-A-X-004": ("INT-C-X-463", []),
    "SCI-INT-A01:INT-A-X-005": ("INT-C-X-466", []),
    "SCI-INT-A01:INT-A-X-007": ("INT-C-X-469", []),
    "SCI-INT-A01:INT-A-X-008": ("INT-C-X-468", []),
    "SCI-INT-A01:INT-A-X-009": ("INT-C-X-467", ["INT-C-X-466"]),
    "SCI-INT-A01:INT-A-X-014": ("INT-C-X-470", []),
    "SCI-INT-A01:INT-A-TECH-015": ("INT-C-TECH-431", []),
    "SCI-INT-A01:INT-A-TAL-016": ("INT-C-TAL-405", []),
    "SCI-INT-A01:INT-A-ORG-017": ("INT-C-ORG-443", []),
    "SCI-INT-A01:INT-A-X-020": ("INT-C-X-460", ["INT-C-X-490"]),
    "SCI-INT-A01:INT-A-TAL-021": ("INT-C-X-480", []),
    "SCI-INT-A02:INT-A-TECH-105": ("INT-C-TECH-420", ["INT-C-TECH-421", "INT-C-TECH-423", "INT-C-TECH-428"]),
    "SCI-INT-A02:INT-A-TECH-107": ("INT-C-X-463", ["INT-C-TECH-420"]),
    "SCI-INT-A02:INT-A-TECH-115": ("INT-C-TECH-429", []),
    "SCI-INT-A02:INT-A-TECH-117": ("INT-C-TECH-430", []),
    "SCI-INT-A02:INT-A-TECH-118": ("INT-C-TECH-429", []),
    "SCI-INT-A02:INT-A-TECH-119": ("INT-C-TECH-430", []),
    "SCI-INT-A03:INT-A-TECH-200": ("INT-C-TECH-425", ["INT-C-TECH-420"]),
    "SCI-INT-A03:INT-A-TECH-201": ("INT-C-TECH-421", ["INT-C-TECH-420"]),
    "SCI-INT-A03:INT-A-TECH-202": ("INT-C-TECH-420", ["INT-C-X-490"]),
    "SCI-INT-A03:INT-A-TECH-203": ("INT-C-TECH-426", []),
    "SCI-INT-A03:INT-A-TECH-204": ("INT-C-TECH-424", []),
    "SCI-INT-A03:INT-A-TECH-205": ("INT-C-TECH-424", ["INT-C-TECH-426"]),
    "SCI-INT-A03:INT-A-TECH-206": ("INT-C-TECH-426", ["INT-C-TECH-420"]),
    "SCI-INT-A03:INT-A-TECH-208": ("INT-C-TECH-427", []),
    "SCI-INT-A03:INT-A-TECH-209": ("INT-C-TECH-428", []),
    "SCI-INT-A03:INT-A-TECH-210": ("INT-C-X-460", ["INT-C-X-490"]),
    "SCI-INT-A03:INT-A-TECH-211": ("INT-C-TECH-426", ["INT-C-TECH-425"]),
    "SCI-INT-A03:INT-A-TECH-212": ("INT-C-TECH-425", []),
    "SCI-INT-A03:INT-A-X-215": ("INT-C-X-461", []),
    "SCI-INT-A03:INT-A-X-217": ("INT-C-X-461", []),
    "SCI-INT-A03:INT-A-X-218": ("INT-C-TECH-424", ["INT-C-TECH-426"]),
    "SCI-INT-A03:INT-A-X-219": ("INT-C-X-462", []),
    "SCI-INT-A03:INT-A-X-220": ("INT-C-X-462", ["INT-C-TECH-426"]),
    "SCI-INT-A03:INT-A-X-221": ("INT-C-TECH-425", []),
    "SCI-INT-A04:INT-A-X-305": ("INT-C-TECH-432", ["INT-C-X-474"]),
    "SCI-INT-A04:INT-A-TECH-320": ("INT-C-TECH-433", ["INT-C-X-480"]),
    "SCI-INT-A04:INT-A-TECH-323": ("INT-C-TECH-434", []),
    "SCI-INT-A05:INT-A-X-401": ("INT-C-X-464", ["INT-C-X-465"]),
    "SCI-INT-A05:INT-A-X-405": ("INT-C-X-480", []),
    "SCI-INT-A05:INT-A-ORG-411": ("INT-C-ORG-442", []),
    "SCI-INT-A05:INT-A-X-413": ("INT-C-X-471", []),
    "SCI-INT-A05:INT-A-X-415": ("INT-C-X-472", []),
    "SCI-INT-A05:INT-A-TECH-418": ("INT-C-X-490", ["INT-C-X-466"]),
    "SCI-INT-A05:INT-A-X-421": ("INT-C-TECH-429", []),
    "SCI-INT-A05:INT-A-X-423": ("INT-C-X-480", []),
}

PY = "lumen-algo-py"
ETL = "lumen-etl-es-py"
JAVA = "lumen-svc-platform（gkxlumen-* Java 门面，只读）"


def C(int_id, kind, name, physical, existence, fields, pk, refresh, writer, *, dim, pattern,
      ours, counterpart="none", form="table", read_by=JAVA, java=None, python=None, gaps=(),
      conflicts=(), dn=(), risks=(), tests=(), conf="medium", escalate=None, extra_src=(),
      extra_consumers=(), predicted_for=(), freshness="T+1", note=None):
    return dict(
        int_id=int_id, kind=kind, name=name, physical=physical, existence=existence,
        fields=list(fields), pk=pk, refresh=refresh, writer=writer, dim=dim, pattern=pattern,
        ours=ours, counterpart=counterpart, form=form, read_by=read_by, java=java, python=python,
        gaps=list(gaps), conflicts=list(conflicts), dn=list(dn), risks=list(risks), tests=list(tests),
        conf=conf, escalate=(existence != "existing") if escalate is None else escalate,
        extra_src=list(extra_src), extra_consumers=list(extra_consumers),
        predicted_for=list(predicted_for), freshness=freshness, note=note)


SPECS = [
    # ============================ TAL
    C("INT-C-TAL-400", "dwd_master", "人才主档 talent_master", "gkxlumenx_dim.talent_master（物理名待定；ADS 只读投影 gkxlumenx_ads.sci_talent_profile）",
      "missing",
      ["scholar_id", "name_zh", "name_en", "orc_id", "gender", "nationality_code(code_country)", "is_chinese_ethnic(待确认口径)",
       "current_org_uid", "region_code(code_region)", "domain_code[](tech_domain)", "degree_level", "title_level", "is_key", "source", "version", "updated_at"],
      "scholar_id（沿用三方 dwd_scholar.scholar_id，稳定性待确认）", "T+1 随入站 ETL；人工修订经 TAL-403 合并视图",
      f"{PY} 主数据 Job（单写者）", dim=["TAL"], pattern=["IP-01", "IP-07"], ours=["etl", "python_internal"],
      counterpart="gkx_mysql_raw", extra_src=["INT-C-TAL-020"],
      dn=["DN-C05-01 人才主数据持有方：三方 scholar_id 直用 / 我方代理键 / 久新 110 产出（同 C01 决策）→ " + LW],
      gaps=["nationality / 华人标识口径（DS-13 seq 248）无源字段，unknown"],
      tests=["主键唯一：scholar_id 去重后行数 = dwd_scholar 行数", "Nebula talent VID = talent:{scholar_id} 一一对应"],
      extra_consumers=["DS-13-TALENT-GLOBAL", "DS-14-TALENT-REGION", "DS-15-TALENT-PROFILE", "DS-16-TALENT-RECRUIT"]),
    C("INT-C-TAL-401", "map_bridge", "人员 ID 映射 person_id_map", "gkxlumenx_dim.person_id_map", "missing",
      ["src_system", "src_person_key", "scholar_id", "method(rule|jx110|manual)", "confidence", "version", "updated_at"],
      "(src_system, src_person_key, version)", "T+1；久新 110 消歧产出按 run 合入（待确认）",
      f"{PY} 消歧 Job（久新 Python-110 并入后）", dim=["TAL"], pattern=["IP-07"], ours=["python_internal"],
      counterpart="jiuxin", form="Python",
      dn=["DN-C05-02 久新 110 消歧产出是否作为本表正式来源（同 C01 OI）→ 久新/" + LW]),
    C("INT-C-TAL-402", "ads", "人才任职/流动边 talent_flow", "gkxlumenx_ads.sci_talent_flow", "missing",
      ["scholar_id", "from_org_uid", "to_org_uid", "from_region_code", "to_region_code", "move_year", "title", "method(work_exp_diff|jx157)", "version"],
      "(scholar_id, move_year, from_org_uid, to_org_uid)", "T+1（派生自 dwd_scholar_work_experience）",
      f"{PY} 流动派生 Job", dim=["TAL", "ORG"], pattern=["IP-02", "IP-07"], ours=["python_internal"],
      counterpart="gkx_mysql_raw", extra_consumers=["DS-13-TALENT-GLOBAL", "DS-14-TALENT-REGION"],
      gaps=["流动 = 关系边 + 时间属性，非 GPS 轨迹（DS-13/14 裁定）"]),
    C("INT-C-TAL-403", "override", "人才修订层 talent_override", "gkxlumenx_ads.sci_talent_override", "missing",
      ["scholar_id", "field_name", "old_value", "new_value", "audit_status(pending|approved|rejected)", "operator", "trace_id", "version", "created_at"],
      "(scholar_id, field_name, version)", "事件驱动（审核通过即合入合并视图）",
      f"{PY} 写（Java 经 /internal/* 提交，不直写）", dim=["TAL"], pattern=["IP-11"], ours=["java_facade", "python_internal"],
      dn=["DN-C05-03 人才修订层写入口：Java 提交→Python 落表 是否被 Java 只读 ADS 铁律接受（写口归 Python）→ " + LW],
      extra_consumers=["DS-15-TALENT-PROFILE"]),
    C("INT-C-TAL-404", "ads", "人才关系边 talent_relation（合作/教育/项目共参）", "gkxlumenx_ads.sci_talent_relation", "missing",
      ["src_scholar_id", "dst_type(talent|inst|ent|project)", "dst_id", "rel_type(coauthor|project|mentor|educated_at)", "coop_count", "first_year", "last_year",
       "strength", "evidence_ids", "source(rule|jx111|manual)", "version"],
      "(src_scholar_id, dst_type, dst_id, rel_type, version)", "weekly 增量（待确认）",
      f"{PY} 关系抽取/派生 Job → 再投影 Nebula（X-490）", dim=["TAL", "ORG"], pattern=["IP-05", "IP-07"], ours=["python_internal", "graph_load"],
      counterpart="jiuxin", form="Python", extra_consumers=["DS-13-TALENT-GLOBAL", "DS-15-TALENT-PROFILE"]),
    C("INT-C-TAL-405", "ads", "人才基础指标 sci_talent_base（地区×领域×年度聚合）", "gkxlumenx_ads.sci_talent_base", "missing",
      ["region_code", "geo_level(country|admin1|city|district|street)", "domain_code", "org_type", "degree_level", "stat_year", "talent_cnt", "org_cnt", "yoy_rate",
       "metric_id", "as_of", "batch_id"],
      "(metric_id, region_code, domain_code, org_type, degree_level, stat_year, as_of)", "T+1 / 月（久新 SQL-98 由我方 GDF/ETL 执行，待确认）",
      "GDF/ETL（执行久新 SQL-98）", dim=["TAL"], pattern=["IP-06"], ours=["etl"], counterpart="jiuxin", form="SQL",
      extra_consumers=["DS-13-TALENT-GLOBAL", "DS-14-TALENT-REGION"],
      gaps=["DS-13/14 粒度（全球→国家→省州→城市；深圳 市→区→园区）为预判（confidence low）"], conf="low"),
    C("INT-C-TAL-406", "ads", "人才流动 OD 聚合 sci_talent_flow_od（预判）", "gkxlumenx_ads.sci_talent_flow_od", "missing",
      ["from_region_code", "to_region_code", "geo_level", "domain_code", "stat_year", "inflow_cnt", "outflow_cnt", "retain_cnt", "metric_id", "as_of", "version"],
      "(metric_id, from_region_code, to_region_code, domain_code, stat_year, as_of)", "月（待确认）",
      f"{PY}（157 人才流动追踪；久新 Python 并入，待确认）", dim=["TAL"], pattern=["IP-07", "IP-11"], ours=["python_internal"],
      counterpart="jiuxin", form="Python", conf="low", predicted_for=["DS-13 seq 246/252/256", "DS-14 seq 267"],
      extra_consumers=["DS-13-TALENT-GLOBAL", "DS-14-TALENT-REGION"]),
    C("INT-C-TAL-407", "ads", "人才扩展档案 sci_talent_ext（荣誉/出访/动态 feed，预判）", "gkxlumenx_ads.sci_talent_ext", "missing",
      ["scholar_id", "ext_type(honor|visit|news|lecture)", "title", "org_or_place", "country_code", "event_date", "source_url", "source", "as_of"],
      "(scholar_id, ext_type, title, event_date)", "unknown",
      "GDF/ETL（源表 unknown）", dim=["TAL"], pattern=["IP-01", "IP-10"], ours=["etl"], counterpart="gkx_mysql_raw",
      conf="low", predicted_for=["DS-13 seq 262/264/265", "DS-15 成果/动态"],
      gaps=["荣誉/出访/动态无已知三方源表（unknown），无源则 IP-10 空态"], extra_consumers=["DS-13-TALENT-GLOBAL", "DS-15-TALENT-PROFILE"]),
    # ============================ TECH
    C("INT-C-TECH-420", "dwd_master", "技术点主数据 technology_master", "gkxlumenx_dim.technology_master（ADS 只读投影 gkxlumenx_ads.sci_technology）", "missing",
      ["technology_id", "name_cn", "name_en", "aliases[]", "domain_code", "parent_technology_id", "importance_level", "status(active|deleted)", "source(jx104|manual)",
       "version", "updated_at"],
      "technology_id（我方 ADS 主表发号，C04 WB-C04-03）", "随 104 auto 层 run + 人工 change_set 发布",
      f"{PY} 主数据 Job（人工发布经 TECH-425）", dim=["TECH"], pattern=["IP-07", "IP-11"], ours=["python_internal"],
      counterpart="jiuxin", form="Python",
      dn=["DN-C05-04 技术点主数据持有方 + technology_id 发号规则（= C02 OI-C02-01 / A03 DN-A03-01）→ " + LW],
      risks=["主数据未定前 104/105 写入的顶点后续需迁移 VID（全图重灌风险）"]),
    C("INT-C-TECH-421", "dim", "技术领域分类维 tech_domain", "gkxlumenx_dim.tech_domain", "missing",
      ["domain_code", "domain_name", "parent_code", "level", "is_focus(重点技术领域)", "taxonomy_source", "version"],
      "domain_code", "版本化，低频（人工发布）", f"{PY} 维表发布脚本 / data-agent 正式化",
      dim=["TECH", "TAL", "ORG"], pattern=["IP-01"], ours=["etl"],
      conflicts=["CF-C05-05"],
      dn=["DN-C05-05 分类体系选型（IPC/学科/自建；= C02 OI-C02-02，供应方 TECH-P0-2 未回）→ 甲方/" + LW]),
    C("INT-C-TECH-422", "map_bridge", "领域锚点映射 map_tech_domain_anchor", "gkxlumenx_dim.map_tech_domain_anchor", "missing",
      ["anchor_system(ipc|cpc|gb13745|project_discipline|wos_category|paper_scope)", "anchor_code", "domain_code", "weight", "version"],
      "(anchor_system, anchor_code, domain_code, version)", "随 tech_domain 版本", "data-agent 正式化 + ETL 导入",
      dim=["TECH", "TAL", "ORG"], pattern=["IP-01"], ours=["etl"],
      note="由 C02 INT-C-TECH-181 的 ipc_anchor[] / discipline_anchor[] 数组字段拆出为桥表"),
    C("INT-C-TECH-423", "map_bridge", "技术点桥接 technology_doc_rel", "gkxlumenx_ads.sci_technology_doc_rel", "missing",
      ["technology_id", "doc_type(patent|zh_paper|en_paper|scholar_paper|project|report)", "doc_id", "weight", "method(ipc|keyword|ner)", "version"],
      "(technology_id, doc_type, doc_id, version)", "T+1 / 随 104 run", f"{PY} 文献挂接 Job",
      dim=["TECH", "TAL", "ORG"], pattern=["IP-02", "IP-07"], ours=["python_internal"]),
    C("INT-C-TECH-424", "ads", "技术关系真源 sci_tech_relation（技术–技术 / 实体–技术）", "gkxlumenx_ads.sci_tech_relation", "missing",
      ["src_type(tech|ent|inst|talent)", "src_id", "dst_technology_id", "rel_type(evolve|depend|contain|substitute|rd|apply|industrialize|master)", "strength",
       "evidence_ids", "source(manual|jx105|rule)", "locked", "version", "is_deleted"],
      "(src_type, src_id, dst_technology_id, rel_type, version)", "weekly 增量（待确认）+ A03 发布事件",
      f"{PY} 关系 Job + 人工发布 → 投影 Nebula tech_relation/produces", dim=["TECH", "ORG", "TAL"], pattern=["IP-05", "IP-07"],
      ours=["python_internal", "graph_load"], counterpart="jiuxin", form="Python"),
    C("INT-C-TECH-425", "ads", "图变更集 graph_change_set（含批量 ops / 状态机）", "gkxlumenx_ads.sci_graph_change_set", "missing",
      ["change_set_id", "graph_scope(tech|panorama)", "ops_json", "status(draft|submitted|approved|published|rejected)", "operator", "reviewer", "trace_id", "created_at", "published_at"],
      "change_set_id", "事件驱动", f"{PY}（Java 经 /internal/* 提交；发布执行 nGQL 只在 Python）",
      dim=["TECH", "X"] if False else ["TECH"], pattern=["IP-11"], ours=["java_facade", "python_internal"],
      risks=["若 Java 直接 INSERT VERTEX / 直写主表 → 违反 Java 不写 nGQL / 只读 ADS（A03 risk）"]),
    C("INT-C-TECH-426", "override", "图人工层 graph_manual_layer（manual 关系/属性覆盖 + tombstone）", "gkxlumenx_ads.sci_graph_manual", "missing",
      ["object_type(node|edge)", "object_key", "field_name", "manual_value", "tombstone", "priority(manual>jx>rule)", "change_set_id", "version"],
      "(object_type, object_key, field_name, version)", "事件驱动（change_set 发布）", f"{PY}",
      dim=["TECH", "TAL", "ORG"], pattern=["IP-11"], ours=["python_internal"],
      note="auto 层 = 久新 104/105 按 run_id 产出；published = auto ⊕ manual（manual 优先）"),
    C("INT-C-TECH-427", "ads", "图变更日志 graph_change_log", "gkxlumenx_ads.sci_graph_change_log", "missing",
      ["log_id", "change_set_id", "object_type", "object_key", "before_json", "after_json", "operator", "trace_id", "created_at"],
      "log_id", "事件驱动（追加写）", f"{PY}", dim=["TECH"], pattern=["IP-11"], ours=["python_internal"]),
    C("INT-C-TECH-428", "snapshot", "图版本与快照 graph_version", "gkxlumenx_ads.sci_graph_version（+ sci_graph_version_snapshot）", "missing",
      ["version_id", "graph_scope", "base_version_id", "change_set_ids[]", "snapshot_uri_or_rows", "node_cnt", "edge_cnt", "operator", "published_at", "status(published|retired)"],
      "version_id", "每次发布一版", f"{PY}", dim=["TECH"], pattern=["IP-11"], ours=["python_internal"],
      conflicts=["CF-C05-11"], note="Nebula 只存当前版；回滚 = 由 ADS 版本重投影（C04 WB-C04-02）"),
    C("INT-C-TECH-429", "snapshot", "图节点指标快照 sci_graph_metric_snapshot（中心性/影响力/影响分）", "gkxlumenx_ads.sci_graph_metric_snapshot", "missing",
      ["graph_version_id", "node_vid", "entity_type", "entity_id", "metric_id", "value", "rank", "is_key_node", "run_id", "model_version", "as_of"],
      "(metric_id, graph_version_id, node_vid, as_of)", "weekly / 随图版本（待确认）", f"{PY} 图算法 Job",
      dim=["TECH", "ORG"], pattern=["IP-05", "IP-11"], ours=["python_internal"],
      conflicts=["CF-C05-06"], risks=["不得复用 innov demo ads_node_influence（A02）"]),
    C("INT-C-TECH-430", "snapshot", "图路径快照 sci_graph_path_snapshot（关键路径 + 路径详情）", "gkxlumenx_ads.sci_graph_path_snapshot", "missing",
      ["path_id", "graph_version_id", "path_type(key_path)", "node_seq[]", "edge_seq[]", "score", "narrative(技术含义/历程/突破)", "run_id", "as_of"],
      "(path_id, graph_version_id)", "随图版本", f"{PY} 图算法 Job",
      dim=["TECH"], pattern=["IP-05", "IP-11", "IP-10"], ours=["python_internal"],
      gaps=["路径技术含义/发展历程/关键突破无来源（A02 TECH-119），narrative 可空"],
      risks=["禁止复用 lumen-algo-py /internal/v1/chain 产业链 Job（写 demo_* 快照，D12）"]),
    C("INT-C-TECH-431", "ads", "技术基础指标 sci_tech_base", "gkxlumenx_ads.sci_tech_base", "missing",
      ["domain_code", "technology_id", "region_code", "stat_year", "doc_type", "doc_cnt", "growth_rate", "metric_id", "as_of", "batch_id"],
      "(metric_id, domain_code, technology_id, region_code, stat_year, as_of)", "T+1 / 月（久新 SQL-96，待确认）",
      "GDF/ETL（执行久新 SQL-96）", dim=["TECH"], pattern=["IP-06"], ours=["etl"], counterpart="jiuxin", form="SQL"),
    C("INT-C-TECH-432", "ads", "区域技术评估 sci_region_tech_eval", "gkxlumenx_ads.sci_region_tech_eval", "missing",
      ["region_code", "geo_level", "domain_code", "technology_id", "dev_level_score", "application_score", "doc_cnt", "org_cnt", "metric_id", "as_of", "version"],
      "(metric_id, region_code, domain_code, technology_id, as_of)", "月（待确认）", f"GDF/ETL 聚合 或 {PY}",
      dim=["TECH", "ORG"], pattern=["IP-02", "IP-11"], ours=["etl", "python_internal"],
      gaps=["区域「技术发展水平」「应用情况」无注册 metric_id（A04）"]),
    C("INT-C-TECH-433", "cfg", "评估运行记录（复用 lumen_analysis_task 三表）", "gkxlumenx_cfg.lumen_analysis_task / _task_node / _task_retry（存量）", "existing_alter",
      ["task_id", "task_type(sci_tech_eval)", "user_id", "params_hash", "status", "result_ref(X-480 snapshot_version)", "created_at"],
      "task_id", "按用户触发", f"{PY} 异步 Job（存量任务框架）",
      dim=["TECH"], pattern=["IP-04", "IP-11"], ours=["python_internal"],
      dn=["DN-C05-06「开始评估」语义 a/b/c 三选一（= A04 决策）→ 甲方+产品"],
      note="复用已有任务表，仅新增 task_type 枚举；结果入 X-480 统一快照"),
    C("INT-C-TECH-434", "user_own", "用户参数模板 sci_eval_param_template", "gkxlumenx_cfg.sci_eval_param_template", "missing",
      ["template_id", "user_id", "scope(system|user)", "name", "params_json", "created_at", "updated_at"],
      "template_id", "用户写", "Java 自有配置写（非 ADS，业务配置表）", dim=["TECH"], pattern=["IP-13"],
      ours=["java_facade"], read_by="lumen-svc-platform（读写自有配置表）",
      conflicts=["CF-C05-16"]),
    # ============================ ORG
    C("INT-C-ORG-440", "dwd_master", "科研机构主数据 research_org", "gkxlumenx_dim.research_org（ADS 只读投影 gkxlumenx_ads.sci_research_org）", "missing",
      ["org_uid", "src_refs[{system,table,org_id}]", "credit_code", "school_code", "name_cn", "name_en", "aliases", "org_category", "adcode(code_region)",
       "country_code", "city_code", "lng", "lat", "parent_org_uid", "status", "version"],
      "org_uid", "T+1 随入站 ETL", f"{PY} 机构归一 Job", dim=["ORG"], pattern=["IP-01", "IP-07"],
      ours=["etl", "python_internal"], counterpart="gkx_mysql_raw", extra_src=["INT-C-ORG-230"],
      conflicts=["CF-C05-01", "CF-C05-17"], dn=["DN-C05-07 机构主数据持有方（同 C03）→ " + LW]),
    C("INT-C-ORG-441", "map_bridge", "机构名称归一 map_org_alias", "gkxlumenx_dim.map_org_alias", "missing",
      ["raw_name", "lang", "source_table", "org_uid", "match_method(xydm|school_code|exact|fuzzy|ner|manual)", "score", "confirmed_by"],
      "(raw_name, source_table)", "T+1", f"{PY} 归一 Job", dim=["ORG"], pattern=["IP-07"], ours=["python_internal"]),
    C("INT-C-ORG-442", "map_bridge", "文献/成果–机构桥接 rel_doc_org（含成果–载体）", "gkxlumenx_ads.sci_rel_doc_org", "missing",
      ["doc_type(paper|patent|project|report|scholar|achievement)", "doc_id", "org_uid", "carrier_id(可空)", "role(作者单位|申请人|承担|参与|转让)", "source", "version"],
      "(doc_type, doc_id, org_uid, role)", "T+1", f"{PY} 归一 Job", dim=["ORG", "TECH"], pattern=["IP-02"], ours=["python_internal"],
      conflicts=["CF-C05-17"]),
    C("INT-C-ORG-443", "ads", "机构基础指标 sci_org_base", "gkxlumenx_ads.sci_org_base", "missing",
      ["org_uid", "region_code", "org_category", "domain_code", "stat_year", "paper_cnt", "patent_cnt", "project_cnt", "talent_cnt", "metric_id", "as_of", "batch_id"],
      "(metric_id, org_uid, domain_code, stat_year, as_of)", "T+1 / 月（久新 SQL-99，待确认）",
      "GDF/ETL（执行久新 SQL-99）", dim=["ORG"], pattern=["IP-06"], ours=["etl"], counterpart="jiuxin", form="SQL",
      extra_consumers=["DS-13-TALENT-GLOBAL"], note="DS-13 seq 250 顶尖机构人才排名可读本表 talent_cnt（预判 low）"),
    # ============================ X
    C("INT-C-X-460", "ads", "三要素图 ADS 投影 sci_graph_node / sci_graph_edge（供 Java 只读）", "gkxlumenx_ads.sci_graph_node / sci_graph_edge", "missing",
      ["graph_version_id", "vid", "entity_type", "entity_id", "label", "props_json", "src_vid", "dst_vid", "edge_type", "rank", "weight"],
      "节点 (graph_version_id, vid)；边 (graph_version_id, src_vid, edge_type, dst_vid, rank)", "随图版本 / weekly",
      f"{PY} 投影 Job（与 Nebula 投影同批，先 ADS 再图）", dim=["TECH", "TAL", "ORG"], pattern=["IP-05"], ours=["python_internal"],
      risks=["innov GraphController 直读 dwm_graph_*（B01 R4），三要素门面不得沿用"]),
    C("INT-C-X-461", "map_bridge", "全景图实体挂接 sci_graph_entity_membership", "gkxlumenx_ads.sci_graph_entity_membership", "missing",
      ["graph_scope", "entity_type(talent|inst|ent|paper|patent)", "entity_id", "status(active|removed)", "change_set_id", "version"],
      "(graph_scope, entity_type, entity_id, version)", "事件驱动", f"{PY}", dim=["TECH", "TAL", "ORG"], pattern=["IP-11"],
      ours=["python_internal"], risks=["移除挂接只删作用域内实体–技术边，禁止 DELETE VERTEX 主数据投影（A03 X-217）"]),
    C("INT-C-X-462", "override", "全景图实体覆盖层 sci_graph_entity_override", "gkxlumenx_ads.sci_graph_entity_override", "missing",
      ["graph_scope", "entity_type", "entity_id", "field_name", "override_value", "change_set_id", "version"],
      "(graph_scope, entity_type, entity_id, field_name, version)", "事件驱动", f"{PY}", dim=["TAL", "ORG", "TECH"], pattern=["IP-11"],
      ours=["python_internal"], conflicts=["CF-C05-10"], dn=["DN-C05-08 全景页实体属性编辑生效范围（= A03 DN-A03-04）→ 产品/" + LW]),
    C("INT-C-X-463", "es", "三要素检索索引 sci_factor（人才/机构/技术点/服务机构）", "ES alias sci_factor → 物理 sci_factor_v1", "missing",
      ["factor_type", "factor_id(scholar_id|org_uid|technology_id|org_id)", "name", "aliases", "region_code", "domain_code[]", "lat", "lng", "org_category", "updated_at"],
      "_id = {factor_type}:{factor_id}", "T+1 增量（水位表 gkxlumenx_cfg.es_sync_watermark 复用）",
      f"{ETL}（新增 sci_factor 模块，读 gkxlumenx_dim/ads，不读三方库直连）", dim=["TAL", "ORG", "TECH"], pattern=["IP-01"],
      ours=["etl"], read_by="lumen-svc-platform（ES 只读检索）",
      gaps=["lumen-etl-es-py 现仅 gkx_enterprise / gkx_enterprise_global 企业索引"],
      risks=["主数据 ID 未定前索引 _id 不稳定 → 收藏/飞点断链"]),
    C("INT-C-X-464", "ads", "成果统一表 sci_achievement", "gkxlumenx_ads.sci_achievement", "missing",
      ["achievement_id", "achievement_type(paper|patent|project|award|report)", "src_table", "src_id", "title", "pub_date", "region_code", "domain_code", "technology_ids[]",
       "org_uids[]", "scholar_ids[]", "value_score_ref", "as_of"],
      "achievement_id（= {type}:{src_id}）", "T+1", "GDF/ETL", dim=["TECH", "ORG", "TAL"], pattern=["IP-01"], ours=["etl"],
      counterpart="gkx_mysql_raw", conflicts=["CF-C05-14"]),
    C("INT-C-X-465", "es", "成果检索索引 sci_achievement", "ES alias sci_achievement → 物理 sci_achievement_v1", "missing",
      ["achievement_id", "achievement_type", "title", "abstract", "pub_date", "region_code", "domain_code", "org_uids", "scholar_ids"],
      "_id = achievement_id", "T+1 增量", f"{ETL}（读 X-464）", dim=["TECH", "ORG", "TAL"], pattern=["IP-01"], ours=["etl"],
      read_by="lumen-svc-platform（ES 只读检索）"),
    C("INT-C-X-466", "ads", "要素落点 sci_factor_geo（含创新点落点）", "gkxlumenx_ads.sci_factor_geo", "missing",
      ["factor_type(paper|patent|talent|org|meeting|project|innovation_point|user_fill)", "factor_id", "region_code", "geo_level", "lat", "lng", "cnt", "layer_id", "as_of"],
      "(factor_type, factor_id, layer_id, as_of) / 聚合行 (factor_type, region_code, geo_level, as_of)", "T+1",
      f"GDF/ETL + {PY}（创新点落点）", dim=["TECH", "TAL", "ORG"], pattern=["IP-01", "IP-05"], ours=["etl", "python_internal"],
      extra_consumers=["DS-13-TALENT-GLOBAL", "DS-14-TALENT-REGION"],
      note="innov demo 已有 ads_innovation_point_map（demo_gkxlumenx_ads），lumen 不得读 demo 表，改读本表"),
    C("INT-C-X-467", "ods", "用户图层填报 ods_user_layer_fill", "gkxlumenx_ods.user_layer_fill", "missing",
      ["fill_id", "user_id", "layer_id", "name", "lat", "lng", "region_code", "attrs_json", "audit_status", "created_at"],
      "fill_id", "用户写 → T+1 ETL 并入 X-466", "Java 自有写（ODS 入口）→ ETL", dim=["NONE_3E"], pattern=["IP-13"],
      ours=["java_facade", "etl"], read_by="lumen-svc-platform（写 ODS 自有入口）", conflicts=["CF-C05-16"]),
    C("INT-C-X-468", "cfg", "图层数据源登记 cfg_layer_datasource", "gkxlumenx_cfg.layer_datasource", "missing",
      ["datasource_id", "layer_id", "kind(ads_table|es_index|external_api_ref)", "ref_name", "secret_ref(仅 Python 侧 K8s Secret 名)", "freshness", "owner", "status"],
      "datasource_id", "人工配置", "Java 登记（只存引用，不存凭据）+ ETL/Python 执行", dim=["NONE_3E"], pattern=["IP-13"],
      ours=["java_facade", "etl"], read_by="lumen-svc-platform（读写自有配置）",
      risks=["任意 API 配置存在 SSRF/凭据泄露：凭据只在 Python 侧，Java 只登记引用（A01）"]),
    C("INT-C-X-469", "user_own", "用户图层分组 sys_user_layer_group", "gkxlumenx_cfg.sys_user_layer_group（或 PigX upms 库，待定）", "missing",
      ["group_id", "user_id", "name", "layer_ids[]", "sort", "created_at"], "group_id", "用户写",
      "Java 自有表", dim=["NONE_3E"], pattern=["IP-13"], ours=["java_facade"], read_by="lumen-svc-platform（读写自有表）",
      conflicts=["CF-C05-16"]),
    C("INT-C-X-470", "user_own", "用户收藏/标签 sys_user_favorite / sys_user_factor_tag", "gkxlumenx_cfg.sys_user_favorite / sys_user_factor_tag", "missing",
      ["user_id", "entity_type", "entity_id", "tag", "created_at"], "(user_id, entity_type, entity_id[, tag])", "用户写",
      "Java 自有表", dim=["TAL", "ORG", "TECH"], pattern=["IP-13"], ours=["java_facade"], read_by="lumen-svc-platform（读写自有表）",
      conflicts=["CF-C05-16"], risks=["entity_id 依赖主数据 ID 稳定；主数据重建产生孤儿收藏（A01）"]),
    C("INT-C-X-471", "user_own", "订阅规则 + 推送记录 sys_user_subscription / sys_push_record", "gkxlumenx_cfg.sys_user_subscription / sys_push_record", "missing",
      ["sub_id", "user_id", "rule_json", "channel", "status", "push_id", "sent_at", "result"], "sub_id / push_id", "用户写 + 推送任务写",
      "Java 自有表 + 推送任务", dim=["NONE_3E"], pattern=["IP-13"], ours=["java_facade"], read_by="lumen-svc-platform（读写自有表）",
      conflicts=["CF-C05-16"]),
    C("INT-C-X-472", "ads", "实时 KPI 聚合 sci_kpi_agg", "gkxlumenx_ads.sci_kpi_agg", "missing",
      ["metric_id", "region_code", "domain_code", "period(day|month)", "value", "as_of"],
      "(metric_id, region_code, domain_code, period, as_of)", "T+1（默认，展示「数据截至」；A05 realtime_verdict）",
      "GDF/ETL", dim=["TECH", "ORG"], pattern=["IP-01", "IP-06"], ours=["etl"],
      conflicts=["CF-C05-15"], gaps=["前端自造 M_INNOV_*_RT 不在 registry（A05）"]),
    C("INT-C-X-474", "dim", "行政区划维扩展 code_region（+街道 / 港澳台 / 大鹏新区）", "gkxlumenx_dim.code_region（存量 ALTER/补数）", "existing_alter",
      ["code", "parent_code", "name", "level(1省|2市|3区县|4街道 新增)", "lng", "lat", "code_std(GB/T 2260|统计用区划12位)", "valid_from", "valid_to"],
      "code", "年度（随国标/统计用区划发布）", "data-agent 正式化（DDL 在 agent-delivery/data/ddl/）",
      dim=["NONE_3E"], pattern=["IP-01"], ours=["etl"], conflicts=["CF-C05-13"],
      extra_src=["INT-C-ORG-222", "INT-C-TAL-026"],
      extra_consumers=["DS-13-TALENT-GLOBAL", "DS-14-TALENT-REGION"]),
    C("INT-C-X-475", "dim", "区域范围维扩展 region_scope / region_scope_member", "gkxlumenx_dim.region_scope / region_scope_member（存量 ALTER/补数）", "existing_alter",
      ["scope_code(global|national|jjj|yrd|gba|hot_city|shenzhen|focus_park)", "member_code", "member_level", "member_type(country|admin1|city|district|street|park)", "sort", "version"],
      "(scope_code, member_code)", "人工发布", "data-agent 正式化",
      dim=["NONE_3E"], pattern=["IP-01"], ours=["etl"], conflicts=["CF-C05-13"],
      extra_consumers=["DS-13-TALENT-GLOBAL", "DS-14-TALENT-REGION"]),
    C("INT-C-X-476", "dim", "国家维 code_country（复用，不改）", "gkxlumenx_dim.code_country", "existing",
      ["alpha3", "alpha2", "name_cn", "name_en", "is_g20"], "alpha3", "低频", "存量", dim=["NONE_3E"], pattern=["IP-01"], ours=["etl"],
      escalate=False, gaps=["全球「省/州」admin1 级（DS-13 seq 244）无维表：ISO 3166-2 是否引入待定（OI-C05-04）"]),
    C("INT-C-X-477", "map_bridge", "地名/区划归一映射 map_region_alias", "gkxlumenx_dim.map_region_alias", "missing",
      ["src_system", "src_value(cur_code|地名文本|城市英文名)", "lang", "region_code", "country_code", "match_method", "confidence", "version"],
      "(src_system, src_value)", "T+1 随入站 ETL", f"{PY} / ETL 地理归一（复用 lumen-etl-es-py etl/geo_code.py、region_code.py 逻辑）",
      dim=["NONE_3E"], pattern=["IP-02"], ours=["etl"], extra_src=["INT-C-ORG-222", "INT-C-TAL-026"]),
    C("INT-C-X-478", "dim", "产业集群维 dim_industry_cluster（复用，不并入技术领域）", "gkxlumenx_dim.industry_cluster（存量）", "existing",
      ["cluster_code", "name", "parent_code", "level"], "cluster_code", "低频", "存量", dim=["NONE_3E"], pattern=["IP-01"], ours=["etl"],
      escalate=False),
    C("INT-C-X-480", "snapshot", "模型结果统一快照 sci_result_snapshot（久新 Python/API 回流 + 我方模型）", "gkxlumenx_ads.sci_result_snapshot", "missing",
      ["metric_id", "entity_type(talent|tech|org|region|none)", "entity_id", "region_code", "domain_code", "dims_json", "value", "value_json", "ci_low", "ci_high",
       "source(jx_py|jx_api|own)", "run_id", "model_version", "snapshot_version", "as_of", "created_at"],
      "(metric_id, entity_type, entity_id, dims_hash, snapshot_version)", "按模型 freshness（offline / weekly / T+1）",
      f"{PY}（久新 Python 并入后的 Job / 适配层落库）", dim=["TAL", "TECH", "ORG"], pattern=["IP-07", "IP-08", "IP-11"],
      ours=["python_internal"], counterpart="jiuxin", form="Python",
      conflicts=["CF-C05-12", "CF-C05-15"], dn=["DN-C05-09 久新 API 结果是否允许落库（= B01 DN-09）→ 甲方"]),
    C("INT-C-X-481", "cache", "久新 API 适配缓存 jx_api_cache", "Redis（键 jx:{接口}:{参数hash}）；可选 gkxlumenx_cfg.jx_api_cache", "missing",
      ["cache_key(接口, 规范化参数)", "response_json(已映射我方字段)", "fetched_at", "ttl", "jx_api_version", "status_code"],
      "cache_key", "TTL = freshness", f"{PY} 适配层（凭据只在 Python K8s Secret）", dim=["TAL", "TECH", "ORG"], pattern=["IP-08"],
      ours=["python_internal"], counterpart="jiuxin", form="API", read_by="仅 lumen-algo-py（Java 不读）",
      dn=["DN-C05-09 同上（缓存/落库合规）→ 甲方"]),
    C("INT-C-X-482", "cfg", "快照版本登记 sci_snapshot_version", "gkxlumenx_cfg.sci_snapshot_version", "missing",
      ["snapshot_version", "scope(metric_id|graph_scope|task_type)", "source(jx_sql|jx_py|jx_api|own)", "as_of", "row_cnt", "status(staging|published|retired)",
       "published_at", "retire_at", "checksum"],
      "snapshot_version", "每批一条", f"{PY} / GDF/ETL 写批次", dim=["TAL", "TECH", "ORG"], pattern=["IP-11"],
      ours=["python_internal", "etl"], read_by=JAVA + "（读当前 published 版本号）"),
    C("INT-C-X-490", "nebula_schema", "三要素 Nebula 增量 schema（引用 C04 9 卡 + innovation_point 待定）", "NebulaGraph TRSGraph space demo_gkx_chain（正式 gkx_chain 待定）",
      "missing",
      ["TAG technology / talent / institution(ALTER)", "EDGE tech_relation / produces / talent_coop / work_at / educated_at / research_coop", "innovation_point（A05 提，C04 未收，待定）"],
      "VID: tech:{technology_id} / talent:{scholar_id} / inst:{org_uid} / ent:{org_id}", "先 ADS 再投影；weekly 增量（待确认）",
      f"{PY} 三要素投影 Job（单写者）", dim=["TECH", "TAL", "ORG"], pattern=["IP-05"], ours=["graph_load"], counterpart="trsgraph",
      form="none", read_by="lumen-algo-py /internal/*（Java 不直连 nGQL）",
      conflicts=["CF-C05-01", "CF-C05-02", "CF-C05-08", "CF-C05-18"],
      dn=["DN-C05-10 三要素图 space：demo_gkx_chain 追加 vs 正式 gkx_chain（= C04 DN-C04-01）→ " + LW]),
]
KIND_CN = {"ads": "ADS", "es": "ES", "dim": "维表", "snapshot": "快照", "dwd_master": "主数据", "map_bridge": "映射/桥表",
           "override": "人工层", "cfg": "配置", "user_own": "用户自有", "ods": "ODS", "cache": "缓存", "nebula_schema": "Nebula"}

# ---------------------------------------------------------------- 源产物元数据
SRC_DOCS = {t: yaml.safe_load((BASE / f"{t}.yaml").read_text(encoding="utf-8")) for t in collect_mod.SRC}
CARD_IDX = {}
for t, d in SRC_DOCS.items():
    for c in d.get("cards", []) or []:
        CARD_IDX[c["int_id"]] = (t, c)


def raw_meta(raw_id):
    task, key = raw_id.split(":", 1)
    if key in CARD_IDX and CARD_IDX[key][0] == task:
        c = CARD_IDX[key][1]
        jx = c.get("jiuxin_row_id")
        jx_rows = ([jx] if isinstance(jx, str) else list(jx or [])) + list((c.get("data_source") or {}).get("jiuxin_rows", []) or [])
        pr = c.get("page_ref")
        pages = [pr] if isinstance(pr, str) else list(pr or [])
        cons = list(((c.get("consumers") or {}).get("page_cards")) or [])
        return dict(card=key, pages=pages, metrics=list(c.get("metric_ids") or []), jx=[x for x in jx_rows if x], consumers=cons)
    return dict(card=None, pages=[], metrics=[], jx=[], consumers=[])


SPEC_IDS = [s["int_id"] for s in SPECS]
assert len(SPEC_IDS) == len(set(SPEC_IDS))
prim, also = {i: [] for i in SPEC_IDS}, {i: [] for i in SPEC_IDS}
for rid, (p, a) in MAP.items():
    prim[p].append(rid)
    for x in a:
        also[x].append(rid)


def uniq(xs):
    out = []
    for x in xs:
        if x not in out:
            out.append(x)
    return out


cards = []
for s in SPECS:
    rids = prim[s["int_id"]] + also[s["int_id"]]
    metas = [raw_meta(r) for r in rids]
    src_cards = uniq([m["card"] for m in metas if m["card"] and m["card"].startswith("INT-C-")] + s["extra_src"])
    page_cards = [m["card"] for m in metas if m["card"] and m["card"].startswith("INT-A-")]
    consumers = uniq(page_cards + [x for m in metas for x in m["consumers"]] + s["extra_consumers"])
    pages = uniq([p for m in metas for p in m["pages"]])
    metrics = uniq([x for m in metas for x in m["metrics"]])
    jx = uniq([x for m in metas for x in m["jx"]])
    gaps = list(s["gaps"])
    if jx or s["counterpart"] == "jiuxin":
        gaps.append(f"久新交付形态/字段/频率：{JX}（{', '.join(jx) if jx else '久新行未逐行挂接'}）")
    if not rids:
        gaps.append("无原始 structure_escalation 提法；C05 按 geo/domain/人才态势预判补卡")
    card = {
        "int_id": s["int_id"],
        "layer": "data",
        "srs": {"ref": "见 merged_from 原卡 srs" if rids else ("预判：" + "；".join(s["predicted_for"]) if s["predicted_for"] else "C05 维表规划")},
        "page_ref": pages,
        "dimension": s["dim"],
        "dep_kind": ["data"] + (["graph"] if s["kind"] in ("nebula_schema",) or "IP-05" in s["pattern"] else []) +
                    (["write_back"] if s["kind"] == "override" else []),
        "metric_ids": metrics,
        "metric_domain_other": [],
        "algorithm_type": "n/a（结构卡；指标算法类型见原卡 / MCP）",
        "integration_pattern": "/".join(s["pattern"]),
        "ours": s["ours"],
        "counterpart": s["counterpart"],
        "delivery_form": s["form"],
        "jiuxin_row_id": jx[0] if len(jx) == 1 else (jx or None),
        "call_chain": {
            "fe_route": None,
            "java": s["java"] or f"{s['read_by']}",
            "python": s["python"] or ("lumen-algo-py /internal/*（写者）" if PY in s["writer"] else None),
            "downstream": s["physical"],
        },
        "contract_draft": {
            "request": [],
            "response_key_fields": s["fields"][:6],
            "granularity": {"pk": s["pk"]},
            "freshness": s["freshness"] if "T+1" in s["refresh"] else ("offline" if "offline" in s["refresh"] else s["freshness"]),
        },
        "status": {"demo": "无（三要素标准层未建）" if s["existence"] != "existing" else "存量",
                   "lumen": {"missing": "未建", "existing_alter": "存量需扩展", "existing": "存量可复用", "planned_not_built": "已规划未建"}[s["existence"]],
                   "d1_d4": "n/a（结构卡）"},
        "gaps": gaps,
        "conflicts": s["conflicts"],
        "decision_needed": s["dn"],
        "structure_escalation": s["escalate"],
        "risks": s["risks"],
        "test_points": s["tests"] or [f"DDL 评审：{s['physical']} 主键 = {s['pk']}", "写者唯一：只有 " + s["writer"].split("（")[0] + " 写入"],
        "confidence": s["conf"],
        # —— C05 扩展块 ——
        "canonical": {
            "kind": s["kind"], "kind_cn": KIND_CN[s["kind"]], "name": s["name"], "physical": s["physical"],
            "existence": s["existence"], "fields_draft": s["fields"], "primary_key": s["pk"],
            "refresh": s["refresh"], "writer": s["writer"], "read_by": s["read_by"],
            "escalate_to": LW if s["escalate"] else None,
        },
        "source_cards": src_cards,
        "consumer_cards": consumers,
        "merged_from": prim[s["int_id"]],
        "merged_also": also[s["int_id"]],
    }
    if s["note"]:
        card["canonical"]["note"] = s["note"]
    if s["predicted_for"]:
        card["canonical"]["predicted_for"] = s["predicted_for"]
    cards.append(card)

dedup_map = [{"raw_id": rid, "kind": RAW_BY_ID[rid]["kind"], "to": p, "also": a} for rid, (p, a) in MAP.items()]

# ---------------------------------------------------------------- 冲突 / 规划块
conflicts = [
    {"id": "CF-C05-01", "topic": "机构 VID 前缀", "sides": ["C03 草案 org:{org_uid}", "C04 inst:{org_uid}（CF-C04-01）", "SVC as-built institution:"],
     "suggestion": "归一 inst:{org_uid}（与 C04 九卡 / tech:/talent:/ent: 短前缀一致）；C03 草案改文、SVC as-built 迁移批次另排", "decide_by": LW, "cards": ["INT-C-ORG-440", "INT-C-X-490"]},
    {"id": "CF-C05-02", "topic": "三要素图 space：demo_gkx_chain vs gkx_chain（D12）", "sides": ["C04 space_plan：在 demo_gkx_chain 追加", "A03 卡写 gkx_chain", "storage README 决策#7 一张 G"],
     "suggestion": "demo 环境写 demo_gkx_chain；lumen 环境须写正式 gkx_chain（demo_ 进入 lumen 链路违反 D12）；正式 space 建否由李伟拍板，未拍板前 lumen 图写入阻塞",
     "decide_by": LW, "cards": ["INT-C-X-490"], "d12": True},
    {"id": "CF-C05-03", "topic": "gkxlumen-innov 读 demo_gkxlumenx_*（D12）", "sides": ["A05 R-A05-1：InnovSql 把 ads_*/dwd_* 解析到 demo_gkxlumenx_*", "helm values-lumen.yaml INNOV_MYSQL_DB=demo_gkxlumenx_ads / INNOV_DIM_SCHEMA=demo_gkxlumenx_dim"],
     "suggestion": "三要素新表一律建在 gkxlumenx_*；innov 存量切库另立 bugfix 单（不在 C05 改）", "decide_by": LW, "cards": ["INT-C-X-464", "INT-C-X-466", "INT-C-TECH-429"], "d12": True},
    {"id": "CF-C05-04", "topic": "lumen-algo-py K8s 写 demo_* 库（D12）", "sides": ["lumen_common/db.py 默认 gkxlumenx_ads", "k8s/api.yaml、worker.yaml 覆盖 LUMEN_ALGO_MYSQL_ADS_DB=demo_gkxlumenx_ads、DWD_DB=demo_gkxlumenx_dwd"],
     "suggestion": "三要素写者全部在 lumen-algo-py；上线前 K8s env 须切 gkxlumenx_*，否则本清单所有 Python 写表都落 demo 库", "decide_by": LW,
     "cards": ["INT-C-X-480", "INT-C-TECH-420", "INT-C-TAL-400"], "d12": True},
    {"id": "CF-C05-05", "topic": "dim_tech_domain 同名异构", "sides": ["C02/A03：技术领域维表不存在", "lumen-algo-py vendor/innov-py schema_mysql.sql 已有 dim_tech_domain(domain_id,name,parent_id,level,domain_source,source_code)，mock 种子，demo 库"],
     "suggestion": "规范名 gkxlumenx_dim.tech_domain（主键 domain_code）；innov 存量表视为 demo 原型，由 innov 迁移时改读规范表；不另起第三套", "decide_by": LW, "cards": ["INT-C-TECH-421"]},
    {"id": "CF-C05-06", "topic": "节点中心性/影响力/影响分 三处提法", "sides": ["A02 TECH-115/118（不得复用 innov ads_node_influence）", "A05 X-421 节点影响分快照", "C04 ads_sci_graph_metric_snapshot 候选"],
     "suggestion": "统一长表 sci_graph_metric_snapshot，以 metric_id 区分；innov ads_node_influence 存量不动", "decide_by": LW, "cards": ["INT-C-TECH-429"]},
    {"id": "CF-C05-07", "topic": "ADS 物理命名前缀", "sides": ["各叶候选名 ads_sci_*（A01/A02/A05/C04）", "storage 约定：gkxlumenx_ads 下物理表名不带 ads_ 前缀（如 enterprise_score）"],
     "suggestion": "物理名 gkxlumenx_ads.sci_*；ads_sci_* 仅作逻辑名/文档别名", "decide_by": LW, "cards": []},
    {"id": "CF-C05-08", "topic": "talent_coop / research_coop 端点语义", "sides": ["ENT 既有 ent→talent / ent→inst", "三要素需要 talent↔talent / inst↔inst（CF-C04-04）"],
     "suggestion": "同名边多端点类型（Nebula 允许），用 coop_type 区分；ADS 真源分别在 TAL-404 / X-460", "decide_by": LW, "cards": ["INT-C-X-490", "INT-C-TAL-404"]},
    {"id": "CF-C05-09", "topic": "technology_id 发号方", "sides": ["C04 WB-C04-03：我方 ADS 主表发号", "A03 TECH-211：若 104/105 改 API 需双向同步回推久新"],
     "suggestion": "我方发号；久新产出以 auto 层候选入表，经 TECH-426 合并；久新侧 ID 进映射列", "decide_by": LW + " / 久新（待确认）", "cards": ["INT-C-TECH-420"]},
    {"id": "CF-C05-10", "topic": "全景页实体属性编辑 vs 三方库只读", "sides": ["SRS-45 可改实体名称/类型", "人才/机构主数据来自三方只读库，C01/C03 持有"],
     "suggestion": "仅作全景图作用域覆盖（X-462），不回写主数据", "decide_by": "产品 / " + LW, "cards": ["INT-C-X-462"]},
    {"id": "CF-C05-11", "topic": "图版本表三处提法", "sides": ["A02 snapshot_version 回放对比", "A03 graph_version + 版本快照", "CHAIN industry_chain_graph_snapshot 全景发布快照"],
     "suggestion": "三要素统一 sci_graph_version（graph_scope 区分技术图/全景图）；与产业链快照不混表", "decide_by": LW, "cards": ["INT-C-TECH-428"]},
    {"id": "CF-C05-12", "topic": "结果快照：统一长表 vs 每指标一表", "sides": ["B01 IP-11 横切单一快照", "A05 创新价值/影响预测各自快照", "CHAIN：Analysis Job Snapshot 禁止混表"],
     "suggestion": "久新/模型「指标值」回流用统一长表 X-480（metric_id+snapshot_version）；用户触发的分析 Job 结果仍按任务表 result_ref 隔离（TECH-433），不混入发布快照", "decide_by": LW, "cards": ["INT-C-X-480"]},
    {"id": "CF-C05-13", "topic": "地理维粒度缺口", "sides": ["code_region 只到区县，无街道", "region_scope gba 只含 9 内地市，港澳另议", "深圳 大鹏新区 code 为空", "DS-14 要 市→区→园区；DS-13 要 全球→国家→省州→城市"],
     "suggestion": "code_region 加 level=4 街道；港澳台按 GB/T 2260 码补；大鹏新区用统计用区划码或我方扩展码（标注）；园区走 region_scope member_type=park；境外 admin1 见 OI-C05-04", "decide_by": "甲方（行政区划精度为业务口径）/ " + LW,
     "cards": ["INT-C-X-474", "INT-C-X-475"]},
    {"id": "CF-C05-14", "topic": "成果模型 vs innov 事件模型", "sides": ["A05 SRS 成果五分类", "innov ads_innovation_event（importance_score 事件）"],
     "suggestion": "新建 sci_achievement；事件模型保留给 innov 存量", "decide_by": "产品 / " + LW, "cards": ["INT-C-X-464"]},
    {"id": "CF-C05-15", "topic": "快照键 metric_id 重复登记", "sides": ["M_INNOV_DS_04_* 与 M_INNOV_ACHIEVE_VALUE / IMPACT_SCORE / IMPACT_FORECAST 重复（A05）", "前端自造 M_INNOV_*_RT"],
     "suggestion": "快照只用 registry 正式 metric_id；重复项由 data-agent 正名后再落快照", "decide_by": "data-agent / " + LW, "cards": ["INT-C-X-480", "INT-C-X-472"]},
    {"id": "CF-C05-16", "topic": "Java 自有写表 vs 「Java 只读 ADS」", "sides": ["收藏/分组/订阅/模板/填报为用户态数据，需 Java 写", "公约：Java 只读 ADS"],
     "suggestion": "用户态表放 gkxlumenx_cfg / upms（非 ADS），Java 可写；ADS 仍只读。请李伟确认库归属", "decide_by": LW,
     "cards": ["INT-C-TECH-434", "INT-C-X-467", "INT-C-X-469", "INT-C-X-470", "INT-C-X-471"]},
    {"id": "CF-C05-17", "topic": "机构 vs 载体", "sides": ["C03 research_org（org_uid）", "innov dim_carrier / dim_carrier_org_rel", "A05 成果–载体桥"],
     "suggestion": "载体作 org 的子类型或经 dim_carrier_org_rel 映射到 org_uid；桥表保留 carrier_id 可空列", "decide_by": LW, "cards": ["INT-C-ORG-440", "INT-C-ORG-442"]},
    {"id": "CF-C05-18", "topic": "innovation_point 新 Tag", "sides": ["A05 TECH-418 提 innovation_point tag / LOCATED_IN edge", "C04 九卡未收；storage 决策#7 一张 G 只增 Tag"],
     "suggestion": "先评估用 technology + sci_factor_geo（X-466）落点表达，不新增 Tag；确需时经 C04 同 space 追加", "decide_by": LW, "cards": ["INT-C-X-490", "INT-C-X-466"]},
    {"id": "CF-C05-19", "topic": "主数据落 DIM 还是 ADS", "sides": ["C01/C02 写「dwd/ads」", "C03 dim_research_org", "公约 Java 只读 ADS；innov 存量 Java 读 dim schema"],
     "suggestion": "主数据真源 gkxlumenx_dim.*（Python 写），另出 ADS 只读投影给 Java；若李伟认可 Java 读 DIM 则可省投影", "decide_by": LW,
     "cards": ["INT-C-TAL-400", "INT-C-TECH-420", "INT-C-ORG-440"]},
]

geo_dim_plan = {
    "conclusion": "不新建地理主维：复用 gkxlumenx_dim.code_region / region_scope / code_country / city；扩展街道级、港澳台、大鹏新区码与园区成员，并新增一张地名/区划归一映射表；全球省州级（admin1）待定",
    "levels": [
        {"level": "global", "carrier": "region_scope scope_code=global（国家集合）", "card": "INT-C-X-475", "status": "existing"},
        {"level": "country", "carrier": "code_country（ISO alpha-3）", "card": "INT-C-X-476", "status": "existing"},
        {"level": "admin1（境外省/州）", "carrier": "unknown（ISO 3166-2 候选）", "card": None, "status": "missing", "open_item": "OI-C05-04"},
        {"level": "province / city / district（中国）", "carrier": "code_region level 1–3（GB/T 2260）", "card": "INT-C-X-474", "status": "existing"},
        {"level": "street（深圳街道）", "carrier": "code_region level=4（统计用区划 9/12 位码）", "card": "INT-C-X-474", "status": "existing_alter"},
        {"level": "park（园区）", "carrier": "region_scope member_type=park（边界/码源 unknown）", "card": "INT-C-X-475", "status": "existing_alter", "open_item": "OI-C05-05"},
        {"level": "湾区 / 京津冀 / 长三角 / 热点城市", "carrier": "region_scope（gba 缺港澳）", "card": "INT-C-X-475", "status": "existing_alter"},
    ],
    "mapping": "三方 dwd_dim_admin_area.cur_code（C03 INT-C-ORG-222）、人才履历地名文本、境外城市名 → map_region_alias（INT-C-X-477）→ region_code / country_code",
    "boundary_assets": "GIS 边界（GeoJSON/瓦片）为前端静态资产或天地图服务，不入 MySQL 维表；与 region_code 对齐即可",
    "prior_art": "innov vendor dim_admin_division 已有 level 4 街道 / 5 园区 设计（demo 库、仅城市级种子）——只作参考，lumen 不读 demo 表",
    "page_needs_low_confidence": {"DS-13": "全球→国家→省州→城市 四级缩放与分布计数", "DS-14": "中国 省→市；深圳 市→区→街道/园区"},
    "structure_escalation": True,
    "escalate_to": LW,
    "business_decision": "行政区划精度属业务口径（公约 §3.8），按团队临时默认值先跑（🟡），须登记客户决策清单",
}

domain_dim_plan = {
    "conclusion": "技术领域单一真源 gkxlumenx_dim.tech_domain（domain_code），人才研究领域 / 机构领域 / 技术点共用；外部分类经锚点映射桥表挂接；产业维复用 industry_cluster，不与技术领域混用",
    "tables": [
        {"card": "INT-C-TECH-421", "name": "tech_domain", "role": "领域码树 + is_focus 重点技术领域（DS-14 人工智能、生物医药…）"},
        {"card": "INT-C-TECH-422", "name": "map_tech_domain_anchor", "role": "IPC/CPC、学科 GB/T 13745、项目 discipline_code、论文 WoS/scope → domain_code"},
        {"card": "INT-C-X-478", "name": "industry_cluster（存量）", "role": "产业维，企业/产业链用；不并入技术领域"},
    ],
    "taxonomy_choice": "unknown：IPC / 学科 / 自建 三选一（= C02 OI-C02-02；供应方 TECH-P0-2 未回）",
    "conflict": "CF-C05-05（innov demo dim_tech_domain 同名异构）",
    "jiuxin": f"久新模型领域码须对齐 domain_code；对端是否接受我方码表：{JX}",
    "structure_escalation": True,
    "escalate_to": LW,
}

jiuxin_result_backflow = {
    "principle": "久新所有交付行均「待确认」。结果一律回流到我方 gkxlumenx_ads（Python/ETL 写，Java 只读）；lumen 链路禁止落 demo_* 库（D12，CF-C05-03/04）",
    "by_form": [
        {"form": "SQL", "pattern": "IP-06", "executor": "我方 GDF/ETL 执行久新 SQL",
         "landing": ["INT-C-TAL-405 sci_talent_base", "INT-C-TECH-431 sci_tech_base", "INT-C-ORG-443 sci_org_base", "INT-C-X-472 sci_kpi_agg", "INT-C-X-466 sci_factor_geo"],
         "version": "batch_id + as_of（数据截至）+ sql_version（久新脚本版本/哈希），批次登记 INT-C-X-482",
         "retention": "业务表保留当前版 + 按 as_of 月末版历史（建议 24 个月，待确认）", "status": JX},
        {"form": "Python", "pattern": "IP-07", "executor": "并入 lumen-algo-py Job（/internal/*）",
         "landing": ["INT-C-X-480 sci_result_snapshot（指标值）", "INT-C-TECH-429/430 图算法快照", "INT-C-TAL-404 / INT-C-TECH-424 关系真源", "INT-C-TECH-426 auto 层候选（104/105/110）", "INT-C-TAL-401 消歧映射"],
         "version": "run_id + model_version + snapshot_version + as_of；published 版本号登记 INT-C-X-482，Java 只读 published",
         "retention": "published 保留最近 3 版 + 每月首版；retired 90 天后清理（建议，待确认）", "status": JX},
        {"form": "API", "pattern": "IP-08", "executor": "lumen-algo-py 适配层（凭据只在 Python K8s Secret；令牌桶 5 QPS；超时 2s/10s；熔断读快照）",
         "landing": ["INT-C-X-481 jx_api_cache（Redis，TTL=freshness）", "INT-C-X-480 sci_result_snapshot source=jx_api（仅当甲方 DN-09 允许落库）"],
         "version": "fetched_at + 响应哈希 + jx_api_version；落库时同样分配 snapshot_version",
         "retention": "缓存按 TTL；不允许落库时熔断期间无快照 → IP-10 空态 + 角标", "status": JX},
    ],
    "decision": "DN-C05-09 / B01 DN-09（甲方）：久新 API 结果是否允许缓存/落库",
    "structure_escalation": True,
    "escalate_to": LW,
}

OPEN = [
    {"id": "OI-C05-01", "priority": "P1", "item": "未完成叶 A06–A15、B02–B09 的 structure_escalation 提法未纳入本次归并 → 待 Z01 补归并（C05-check 打印当前已出现产物的提法数，供 Z01 参考）", "owner": "coordinator → Z01"},
    {"id": "OI-C05-02", "priority": "P0", "item": "主数据持有方（人才 scholar_id / 技术点 technology_id / 机构 org_uid）未定，所有主键草案依赖它（DN-C05-01/04/07）", "owner": LW},
    {"id": "OI-C05-03", "priority": "P0", "item": "lumen 链路 demo_* 风险：三要素图 space（CF-C05-02）、lumen-algo-py K8s 库名（CF-C05-04）、innov 读 demo 库（CF-C05-03）", "owner": LW},
    {"id": "OI-C05-04", "priority": "P2", "item": "全球省/州 admin1 维是否引入（ISO 3166-2）及数据源", "owner": "产品 / " + LW},
    {"id": "OI-C05-05", "priority": "P2", "item": "深圳街道码源与园区边界/编码来源 unknown", "owner": "data-agent / 甲方"},
    {"id": "OI-C05-06", "priority": "P1", "item": "久新 API 结果缓存/落库合规（DN-09）", "owner": "甲方"},
    {"id": "OI-C05-07", "priority": "P1", "item": "技术领域分类体系选型（OI-C02-02）", "owner": "甲方 / 供应方"},
    {"id": "OI-C05-08", "priority": "P2", "item": "快照/历史保留策略数值（24 月 / 3 版 / 90 天）为建议值", "owner": LW},
    {"id": "OI-C05-09", "priority": "P2", "item": "人才态势 DS-13～16 预判卡（TAL-405/406/407、X-466 等）confidence=low；DS-15/16 未逐叶核（画像隐私分级、成本数据源、团队组合 missing）", "owner": "A13–A15 / Z01"},
    {"id": "OI-C05-10", "priority": "P2", "item": "华人占比、荣誉奖项、出访记录、最新动态 feed 无已知源表（unknown）", "owner": "data-agent / 甲方"},
    {"id": "OI-C05-11", "priority": "P2", "item": "主数据落 DIM 还是 ADS、Java 能否读 DIM（CF-C05-19）；用户态表库归属（CF-C05-16）", "owner": LW},
]

risks = [
    {"id": "R-C05-01", "level": "high", "desc": "lumen-algo-py K8s 写 demo_gkxlumenx_*：本清单所有 Python 写表上线即落 demo 库（D12）", "cards": ["INT-C-X-480"]},
    {"id": "R-C05-02", "level": "high", "desc": "C04 方案在 demo_gkx_chain 追加三要素 Tag/Edge；若 lumen 环境沿用即违反 D12（禁止 demo_* 进入 lumen 链路）", "cards": ["INT-C-X-490"]},
    {"id": "R-C05-03", "level": "high", "desc": "gkxlumen-innov（lumen）读 demo_gkxlumenx_ads/dim（A05 发现，helm values-lumen.yaml 佐证）", "cards": ["INT-C-X-464"]},
    {"id": "R-C05-04", "level": "medium", "desc": "主数据 ID 未定前建 ES/收藏/图 VID，后续全量迁移", "cards": ["INT-C-X-463", "INT-C-X-470"]},
    {"id": "R-C05-05", "level": "medium", "desc": "人工层写入口若被实现成 Java 直写 ADS / 直连 nGQL 即违反铁律；写口必须经 Python /internal/*", "cards": ["INT-C-TECH-425", "INT-C-TAL-403"]},
]

esc_cards = sum(1 for c in cards if c["structure_escalation"])
doc = {
    "task_id": "SCI-INT-C05",
    "layer": "data",
    "counterpart_name": "北京久新（旧写「九新」）",
    "scope_count": len(MAP),
    "card_count": len(cards),
    "gap": [],
    "scope_note": "scope_count = C05-collect 采集的原始 structure_escalation 提法数（B01/C01–C04/A01–A05）；card_count = 归并后的规范结构卡数",
    "summary": {
        "raw_mentions": len(MAP),
        "raw_by_kind": {"card": sum(1 for r in RAW if r["kind"] == "card"), "top": sum(1 for r in RAW if r["kind"] == "top")},
        "canonical_by_kind": {k: sum(1 for c in cards if c["canonical"]["kind"] == k) for k in KIND_CN},
        "structure_escalation": esc_cards,
        "conflicts": len(conflicts),
    },
    "cards": cards,
    "dedup_map": dedup_map,
    "geo_dim_plan": geo_dim_plan,
    "domain_dim_plan": domain_dim_plan,
    "jiuxin_result_backflow": jiuxin_result_backflow,
    "conflicts": conflicts,
    "risks": risks,
    "open_items": OPEN,
    "structure_escalation": esc_cards,
}
out = BASE / "SCI-INT-C05.yaml"
header = ("# SCI-INT-C05 标准层结构清单（ADS / ES / 维表 / 快照）· 生成：_work/C05-build.py · 校验：_work/C05-check.py\n"
          "# 对端 = 北京久新；久新行全部「待确认」；新结构一律 structure_escalation → human:李伟（草案，未评审）\n")
out.write_text(header + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
print("wrote", out.name, "cards", len(cards), "raw", len(MAP), "esc", esc_cards)
