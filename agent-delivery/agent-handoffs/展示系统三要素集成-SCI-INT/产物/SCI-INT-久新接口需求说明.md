# 久新接口需求说明

对端：久新。确认状态一律为待确认。本文件只写需求。会签未做。

## SRS-96 技术基础指标模型构建

- 确认状态：待确认
- 谁消费：INT-A-TECH-015（page，A01，M_TECH_BASE_96_1）；INT-A-TECH-023（page，A01，M_TECH_BASE_96_1）；INT-A-TECH-110（page，A02，M_TECH_BASE_96_1|M_TECH_PAPER_PATENT_CNT）；INT-A-X-0800（page，A09，M_TECH_BASE_96_1）；INT-A-X-0804（page，A09，M_TECH_BASE_96_1）；INT-B-TECH-500（metric，B06，M_TECH_BASE_96_1）；INT-C-TECH-150（data，C02，M_TECH_BASE_96_1）；INT-C-TECH-431（data，C05，M_TECH_BASE_96_1）
- 模式：IP-06；TBD
- 同步/异步：同步读；同步；未标明
- 输入字段：time_range、region_code、discipline_code、group_by、tech_id、domain_code、technology_id、region_scope、as_of
- 输出字段：metric_id、factor_type(paper|patent)、region_code、period、value、yoy、share、citation_sum、paper_count、influence_value、paper_cnt、patent_cnt、talent_cnt、org_cnt、payload、technology_id、growth、as_of、domain_code、stat_year、doc_type、doc_cnt

## SRS-104 技术实体识别构建

- 确认状态：待确认
- 谁消费：INT-A-TECH-103（page，A02，M_TECH_GRAPH_104_1）；INT-A-TECH-203（page，A03，无 metric_id）；INT-A-TECH-211（page，A03，无 metric_id）；INT-A-TECH-418（page，A05，无 metric_id）；INT-B-TECH-501（metric，B06，M_TECH_GRAPH_104_1）；INT-B-TECH-507（metric，B06，M_TECH_GRAPH_STRUCT）；INT-C-TECH-151（data，C02，M_TECH_DEEP_130_1|M_TECH_GRAPH_104_1）；INT-C-TECH-300（data，C04，M_TECH_DEEP_130_1|M_TECH_DEEP_131_1|M_TECH_GRAPH_104_1|M_TECH_GRAPH_STRUCT|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY）；INT-C-TECH-420（data，C05，M_TECH_DEEP_130_1|M_TECH_GRAPH_104_1|M_TECH_GRAPH_STRUCT|M_TECH_ENTITY_INFLUENCE|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY|M_TECH_DEEP_131_1）；INT-C-TECH-425（data，C05，无 metric_id）；INT-C-TECH-426（data，C05，M_TECH_DEEP_130_1|M_TECH_GRAPH_104_1|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_GRAPH_STRUCT|M_TECH_REL_STRENGTH）；INT-C-X-466（data，C05，无 metric_id）；INT-C-X-480（data，C05，M_TALENT_DEEP_162_1|M_TALENT_GRAPH_110_1|M_TECH_DEEP_130_1|M_TECH_GRAPH_104_1|M_TECH_COMPOSITE_SCORE）；INT-C-X-490（data，C05，M_TALENT_GRAPH_110_1|M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET|M_TECH_DEEP_130_1|M_TECH_ENTITY_INFLUENCE|M_TECH_GRAPH_104_1|M_TECH_GRAPH_STRUCT|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_REL_STRENGTH|M_TECH_DEEP_131_1|M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK|M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_114_1|M_ORG_GRAPH_115_1）
- 模式：IP-07；IP-10；IP-09；TBD；IP-05/IP-07/IP-08/IP-09；IP-07/IP-11；IP-11；IP-01/IP-05；IP-07/IP-08/IP-11；IP-05
- 同步/异步：异步；无对端调用；同步；未标明；同步读 / 异步
- 输入字段：domain_code、tech_id、depth、tombstone(technology_id, aliases[], reason, operator)、run_id、auto_items[]、manual_overrides[]、tombstones[]、point_ids|since、source_id、technology_id、region_scope、time_range、as_of、technology_id | domain_code
- 输出字段：nodes[vid, name, category, level, source]、suppressed_count、conflict_items[]、merged_count、conflict_items[(object_id, field, auto_value, manual_value)]、run_status、point_id、anchor_vid、link_confidence、model_version、as_of、metric_id、period、algo_version、entity_id、nodes、edges、parent_seq、technology_id（待定）、name、aliases、domain_code、source_doc_refs、vid、technology_id、centrality、is_key_node、source、name_cn、name_en、aliases[]、parent_technology_id、change_set_id、graph_scope(tech|panorama)、ops_json、status(draft|submitted|approved|published|rejected)、operator、reviewer、object_type(node|edge)、object_key、field_name、manual_value、tombstone、priority(manual>jx>rule)、factor_type(paper|patent|talent|org|meeting|project|innovation_point|user_fill)、factor_id、region_code、geo_level、lat、lng、entity_type(talent|tech|org|region|none)、dims_json、TAG technology / talent / institution(ALTER)、EDGE tech_relation / produces / talent_coop / work_at / educated_at / research_coop、innovation_point（A05 提，C04 未收，待定）

## SRS-105 技术实体关系抽取

- 确认状态：待确认
- 谁消费：INT-A-TECH-104（page，A02，M_TECH_GRAPH_105_1|M_TECH_EDGE_STRENGTH）；INT-A-X-109（page，A02，M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_GRAPH_104_1）；INT-A-X-114（page，A02，M_TECH_ENTITY_REL|M_TECH_GRAPH_105_1）；INT-A-TECH-205（page，A03，无 metric_id）；INT-A-X-213（page，A03，M_TECH_GRAPH_105_1）；INT-A-X-216（page，A03，M_TECH_GRAPH_105_1）；INT-A-X-218（page，A03，无 metric_id）；INT-A-TECH-316（page，A04，M_TECH_GRAPH_105_1）；INT-A-TECH-317（page，A04，M_TECH_REL_STRENGTH）；INT-B-TECH-502（metric，B06，M_TECH_GRAPH_105_1）；INT-B-TECH-503（metric，B06，M_TECH_EDGE_STRENGTH）；INT-B-TECH-505（metric，B06，M_TECH_ENTITY_REL）；INT-B-TECH-506（metric，B06，M_TECH_ENTITY_TOP5）；INT-B-TECH-511（metric，B06，M_TECH_REL_STRENGTH）；INT-C-TECH-152（data，C02，M_TECH_DEEP_130_1|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_GRAPH_STRUCT|M_TECH_REL_STRENGTH）；INT-C-TECH-340（data，C04，M_TECH_DEEP_130_1|M_TECH_DEEP_131_1|M_TECH_EDGE_STRENGTH|M_TECH_GRAPH_105_1|M_TECH_GRAPH_STRUCT|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY|M_TECH_REL_STRENGTH）；INT-C-TECH-341（data，C04，M_TECH_ENTITY_INFLUENCE|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_REL_STRENGTH）；INT-C-TECH-424（data，C05，M_TECH_DEEP_130_1|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_GRAPH_STRUCT|M_TECH_REL_STRENGTH|M_TECH_ENTITY_INFLUENCE|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY|M_TECH_DEEP_131_1）；INT-C-TECH-426（data，C05，M_TECH_DEEP_130_1|M_TECH_GRAPH_104_1|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_GRAPH_STRUCT|M_TECH_REL_STRENGTH）；INT-C-X-490（data，C05，M_TALENT_GRAPH_110_1|M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET|M_TECH_DEEP_130_1|M_TECH_ENTITY_INFLUENCE|M_TECH_GRAPH_104_1|M_TECH_GRAPH_STRUCT|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_REL_STRENGTH|M_TECH_DEEP_131_1|M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK|M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_114_1|M_ORG_GRAPH_115_1）
- 模式：IP-07；IP-09；TBD；IP-05/IP-07/IP-08/IP-09；IP-05/IP-07/IP-09；IP-05/IP-07；IP-11；IP-05
- 同步/异步：异步；同步；未标明
- 输入字段：domain_code、tech_id、depth、min_strength、entity_types、top_n、entity_ids、time_range、base_version、op=delete_edge、edge_key、technology_id|domain_code、entity_types[人,机构,论文,专利]、sort_by(strength|time|name)、keyword、pairs[(entity_type, entity_id, technology_id)]、op=delete_entity_edge、domain_codes、technology_ids、start_year、end_year、rel_type、technology_id、region_scope、as_of、entity_type、topN
- 输出字段：relations[source, target, relation_type, strength, first_seen_year]、entities[entity_id, entity_type, name, strength]、edges[source, target, relation_type, strength, year]、change_set_id、edge_source(auto|manual)、entity_id、entity_type、name、strength、year、in_panorama、metric_id、technology_id、evidence_count、algo_version、impact_note、source_technology_id、target_technology_id、source_name、target_name、relation_type、source_domain_code、target_domain_code、snapshot_id、period、src_id、dst_id、rel_type、weight、parent_seq、nodes、edges、data、algorithm、graph、src、dst、source、src_type(tech|ent|inst|talent)、dst_technology_id、rel_type(evolve|depend|contain|substitute|rd|apply|industrialize|master)、evidence_ids、object_type(node|edge)、object_key、field_name、manual_value、tombstone、priority(manual>jx>rule)、TAG technology / talent / institution(ALTER)、EDGE tech_relation / produces / talent_coop / work_at / educated_at / research_coop、innovation_point（A05 提，C04 未收，待定）

## SRS-130 全景技术链模型

- 确认状态：待确认
- 谁消费：INT-A-TECH-102（page，A02，M_TECH_DEEP_130_1|M_TECH_GRAPH_STRUCT）；INT-B-TECH-400（metric，B05，M_TECH_DEEP_130_1）；INT-C-TECH-153（data，C02，M_TECH_DEEP_130_1|M_TECH_DEEP_131_1）
- 模式：IP-08；TBD
- 同步/异步：异步；未标明
- 输入字段：domain_code、tech_id、depth、time_range、region_code、technology_id、region_scope、as_of
- 输出字段：nodes[id, name, category, level]、relations[source, target, relation_type, strength]、snapshot_version、snapshot_id、period、algo_version、source、metric_id、payload、technology_id、chain_nodes、chain_edges、region_scope、as_of

## SRS-131 深圳技术链模型

- 确认状态：待确认
- 谁消费：INT-B-TECH-401（metric，B05，M_TECH_DEEP_131_1）；INT-C-TECH-153（data，C02，M_TECH_DEEP_130_1|M_TECH_DEEP_131_1）
- 模式：IP-08；TBD
- 同步/异步：异步；未标明
- 输入字段：region_code、time_range、domain_code、technology_id、region_scope、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、technology_id、chain_nodes、chain_edges、region_scope、as_of

## SRS-132 技术发展历程模型

- 确认状态：待确认
- 谁消费：INT-B-TECH-402（metric，B05，M_TECH_DEEP_132_1）；INT-C-TECH-154（data，C02，M_TECH_DEEP_132_1）
- 模式：IP-08；TBD
- 同步/异步：异步；未标明
- 输入字段：region_code、time_range、domain_code、technology_id、region_scope、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、technology_id、events[]、as_of

## SRS-133 深圳细分领域分布模型

- 确认状态：待确认
- 谁消费：INT-B-TECH-403（metric，B05，M_TECH_DEEP_133_1）；INT-C-TECH-155（data，C02，M_TECH_DEEP_133_1|M_TECH_DEEP_140_1|M_TECH_SZ_ASSESS）
- 模式：IP-08；TBD
- 同步/异步：异步；未标明
- 输入字段：region_code、time_range、domain_code、technology_id、region_scope、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、domain_code、share / score、recommend_rank、as_of

## SRS-134 技术前沿热点领域识别模型

- 确认状态：待确认
- 谁消费：INT-A-TECH-326（page，A04，M_TECH_DEEP_134_1）；INT-B-TECH-404（metric，B05，M_TECH_DEEP_134_1）；INT-B-TECH-609（metric，B07，M_TECH_HEAT_INDEX）；INT-B-TECH-615（metric，B07，M_TECH_TOPIC_HEAT）；INT-C-TECH-156（data，C02，M_TECH_DEEP_134_1|M_TECH_HEAT_INDEX|M_TECH_TOPIC_HEAT）
- 模式：IP-08；IP-09；TBD
- 同步/异步：异步；同步；未标明
- 输入字段：domain_codes、time_window、keyword_weight、heat_threshold、region_code、time_range、domain_code、threshold、technology_id、horizon、region_scope、as_of
- 输出字段：accepted_params、rejected_params、snapshot_id、period、algo_version、source、metric_id、payload、heat_index、topic_key、heat、technology_id / topic_id、growth、term、as_of

## SRS-135 技术产业化潜力识别模型

- 确认状态：待确认
- 谁消费：INT-B-TECH-405（metric，B05，M_TECH_DEEP_135_1）；INT-B-TECH-612（metric，B07，M_TECH_POTENTIAL_SCORE）；INT-C-TECH-157（data，C02，M_TECH_DEEP_135_1|M_TECH_POTENTIAL_SCORE|M_TECH_SZ_ASSESS）
- 模式：IP-08；IP-09；TBD
- 同步/异步：异步；同步；未标明
- 输入字段：region_code、time_range、domain_code、technology_id、region_scope、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、potential_score、technology_id、dims、as_of

## SRS-136 技术转化瓶颈堵点原因识别模型

- 确认状态：待确认
- 谁消费：INT-B-TECH-406（metric，B05，M_TECH_DEEP_136_1）；INT-B-TECH-608（metric，B07，M_TECH_CONVERT_BOTTLENECK）；INT-C-TECH-158（data，C02，M_TECH_CONVERT_BOTTLENECK|M_TECH_DEEP_136_1）
- 模式：IP-08；IP-09；TBD
- 同步/异步：异步；同步；未标明
- 输入字段：region_code、time_range、domain_code、technology_id、region_scope、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、bottleneck、reason、technology_id、bottlenecks[]、reasons[]、as_of

## SRS-137 技术阶段分析模型

- 确认状态：待确认
- 谁消费：INT-A-TECH-327（page，A04，M_TECH_DEEP_137_1）；INT-B-TECH-407（metric，B05，M_TECH_DEEP_137_1）；INT-B-TECH-610（metric，B07，M_TECH_LIFE_STAGE）；INT-B-TECH-611（metric，B07，M_TECH_MATURITY_LEVEL）；INT-B-TECH-613（metric，B07，M_TECH_STAGE_JUDGE）；INT-C-TECH-159（data，C02，M_TECH_DEEP_137_1|M_TECH_LIFE_STAGE|M_TECH_MATURITY_LEVEL|M_TECH_STAGE_JUDGE|M_TECH_SZ_ASSESS）
- 模式：IP-08；IP-09；TBD
- 同步/异步：异步；同步；未标明
- 输入字段：technology_ids、maturity_thresholds、stage_rules、region_code、time_range、domain_code、maturity_threshold、technology_id、period、region_scope、as_of
- 输出字段：accepted_params、rejected_params、snapshot_id、period、algo_version、source、metric_id、payload、stage、maturity、bottleneck、potential、technology_id、life_stage、maturity_level、as_of

## SRS-138 深圳技术发展问题识别模型

- 确认状态：待确认
- 谁消费：INT-B-TECH-408（metric，B05，M_TECH_DEEP_138_1）；INT-B-TECH-614（metric，B07，M_TECH_SZ_ASSESS）；INT-C-TECH-160（data，C02，M_TECH_DEEP_138_1|M_TECH_DEEP_139_1|M_TECH_SZ_ASSESS）
- 模式：IP-08；IP-09；TBD
- 同步/异步：异步；同步；未标明
- 输入字段：region_code、time_range、domain_code、technology_id、region_scope、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、potential、stage、advice、technology_id / domain_code、issues[] / opportunities[]、as_of

## SRS-139 深圳技术发展机遇识别模型

- 确认状态：待确认
- 谁消费：INT-B-TECH-409（metric，B05，M_TECH_DEEP_139_1）；INT-C-TECH-160（data，C02，M_TECH_DEEP_138_1|M_TECH_DEEP_139_1|M_TECH_SZ_ASSESS）
- 模式：IP-08；TBD
- 同步/异步：异步；未标明
- 输入字段：region_code、time_range、domain_code、technology_id、region_scope、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、technology_id / domain_code、issues[] / opportunities[]、as_of

## SRS-140 深圳技术发展重点布局领域推荐模型

- 确认状态：待确认
- 谁消费：INT-B-TECH-410（metric，B05，M_TECH_DEEP_140_1）；INT-C-TECH-155（data，C02，M_TECH_DEEP_133_1|M_TECH_DEEP_140_1|M_TECH_SZ_ASSESS）
- 模式：IP-08；TBD
- 同步/异步：异步；未标明
- 输入字段：region_code、time_range、domain_code、technology_id、region_scope、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、domain_code、share / score、recommend_rank、as_of

## SRS-99 科研机构基础指标模型构建

- 确认状态：待确认
- 谁消费：INT-A-ORG-017（page，A01，M_ORG_BASE_99_1）；INT-A-ORG-022（page，A01，M_ORG_BASE_99_1）；INT-B-ORG-800（metric，B09，M_ORG_BASE_99_1）；INT-B-ORG-803（metric，B09，M_ORG_ATTENTION_TREND）；INT-B-ORG-807（metric，B09，M_ORG_INDUSTRY_COVER）；INT-B-ORG-808（metric，B09，M_ORG_NEW_TREND）；INT-B-ORG-811（metric，B09，M_ORG_SZ_STATUS）；INT-C-ORG-250（data，C03，M_ORG_ATTENTION_TREND|M_ORG_BASE_99_1|M_ORG_INDUSTRY_COVER|M_ORG_NEW_TREND|M_ORG_SZ_STATUS）；INT-C-ORG-443（data，C05，M_ORG_BASE_99_1）
- 模式：IP-06；IP-09；IP-06/IP-09
- 同步/异步：同步读；同步；同步读 / 异步
- 输入字段：time_range、region_code、org_type、group_by、top_n、domain_code、org_uid[]、industry_code
- 输出字段：metric_id、region_code、period、value、yoy、share、org_id、score、rank、as_of、payload、new_org_cnt、growth_rate、parent_seq、cover_cnt、new_cnt、org_uid、metric_code、region、org_category、domain_code、stat_year、paper_cnt

## SRS-114 科研机构实体识别构建

- 确认状态：待确认
- 谁消费：INT-A-ORG-420（page，A05，M_ORG_GRAPH_114_1）；INT-B-ORG-801（metric，B09，M_ORG_GRAPH_114_1）；INT-C-ORG-251（data，C03，M_ORG_GRAPH_114_1）；INT-C-ORG-320（data，C04，M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_114_1|M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK）；INT-C-ORG-440（data，C05，M_ORG_ATTENTION_TREND|M_ORG_BASE_99_1|M_ORG_INDUSTRY_COVER|M_ORG_NEW_TREND|M_ORG_PERF_QUERY|M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_114_1|M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK）；INT-C-X-490（data，C05，M_TALENT_GRAPH_110_1|M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET|M_TECH_DEEP_130_1|M_TECH_ENTITY_INFLUENCE|M_TECH_GRAPH_104_1|M_TECH_GRAPH_STRUCT|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_REL_STRENGTH|M_TECH_DEEP_131_1|M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK|M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_114_1|M_ORG_GRAPH_115_1）
- 模式：IP-07；IP-07/IP-08/IP-09；IP-01/IP-07；IP-05
- 同步/异步：异步；同步读 / 异步
- 输入字段：point_id、entity_types=org、domain_code、source_id、org_uid[]、industry_code、region_code、time_range、org_uid
- 输出字段：org_vid、org_id、name、rel_type、metric_id、period、algo_version、entity_key、raw_name、org_uid、score、vid、institution_type、source、src_refs[{system,table,org_id}]、credit_code、school_code、name_cn、name_en、TAG technology / talent / institution(ALTER)、EDGE tech_relation / produces / talent_coop / work_at / educated_at / research_coop、innovation_point（A05 提，C04 未收，待定）

## SRS-115 科研机构实体关系抽取

- 确认状态：待确认
- 谁消费：INT-B-ORG-802（metric，B09，M_ORG_GRAPH_115_1）；INT-C-ORG-252（data，C03，M_ORG_GRAPH_115_1）；INT-C-ORG-360（data，C04，M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_115_1）；INT-C-X-460（data，C05，M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_115_1）；INT-C-X-490（data，C05，M_TALENT_GRAPH_110_1|M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET|M_TECH_DEEP_130_1|M_TECH_ENTITY_INFLUENCE|M_TECH_GRAPH_104_1|M_TECH_GRAPH_STRUCT|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_REL_STRENGTH|M_TECH_DEEP_131_1|M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK|M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_114_1|M_ORG_GRAPH_115_1）
- 模式：IP-07；IP-07/IP-08/IP-09；IP-05
- 同步/异步：异步
- 输入字段：domain_code、rel_type、org_uid[]、industry_code、region_code、time_range、org_uid、depth、coop_type
- 输出字段：metric_id、period、src_key、dst_key、rel_type、src_org_uid、dst_org_uid / doc_id、weight、src、dst、coop_type、coop_count、strength、graph_version_id、vid、entity_type、entity_id、label、props_json、TAG technology / talent / institution(ALTER)、EDGE tech_relation / produces / talent_coop / work_at / educated_at / research_coop、innovation_point（A05 提，C04 未收，待定）

## SRS-149 科研机构重点技术领域布局模型

- 确认状态：待确认
- 谁消费：INT-B-ORG-700（metric，B08，M_ORG_DEEP_149_1）；INT-B-ORG-812（metric，B09，M_ORG_TECH_LAYOUT）；INT-C-ORG-253（data，C03，M_ORG_DEEP_149_1|M_ORG_TECH_LAYOUT）
- 模式：IP-08；IP-09；IP-08/IP-09
- 同步/异步：异步；同步
- 输入字段：domain_code、time_range、org_uid[]、industry_code、region_code
- 输出字段：metric_id、period、algo_version、snapshot_id、payload、domain_code、org_cnt、parent_seq、org_uid、count / share、as_of

## SRS-150 科研机构发展历程模型

- 确认状态：待确认
- 谁消费：INT-B-ORG-701（metric，B08，M_ORG_DEEP_150_1）；INT-C-ORG-254（data，C03，M_ORG_DEEP_150_1）
- 模式：IP-08
- 同步/异步：异步
- 输入字段：time_range、org_uid[]、industry_code、region_code
- 输出字段：metric_id、period、algo_version、snapshot_id、payload、org_uid、events[{date, type, desc}]

## SRS-151 深圳科研机构优势分析模型

- 确认状态：待确认
- 谁消费：INT-B-ORG-702（metric，B08，M_ORG_DEEP_151_1）；INT-B-ORG-809（metric，B09，M_ORG_SZ_ADVANTAGE）；INT-C-ORG-255（data，C03，M_ORG_DEEP_151_1|M_ORG_SZ_ADVANTAGE）
- 模式：IP-08；IP-09；IP-08/IP-09
- 同步/异步：异步；同步
- 输入字段：region_code、time_range、domain_code、org_uid[]、industry_code
- 输出字段：metric_id、period、algo_version、snapshot_id、payload、parent_seq、industry_code、org_uid、dims[成果/经费/人才]、report

## SRS-152 深圳科研机构痛难点识别模型

- 确认状态：待确认
- 谁消费：INT-B-ORG-703（metric，B08，M_ORG_DEEP_152_1）；INT-B-ORG-810（metric，B09，M_ORG_SZ_PAINPOINT）；INT-C-ORG-256（data，C03，M_ORG_DEEP_152_1|M_ORG_SZ_PAINPOINT）
- 模式：IP-08；IP-09；IP-08/IP-09
- 同步/异步：异步；同步
- 输入字段：region_code、time_range、domain_code、org_uid[]、industry_code
- 输出字段：metric_id、period、algo_version、snapshot_id、payload、parent_seq、industry_code、org_uid、dims[项目/转化/人才/产业合作]、suggestions

## SRS-153 科研合作关系链条模型

- 确认状态：待确认
- 谁消费：INT-A-X-0817（page，A09，M_ORG_DEEP_153_1）；INT-B-ORG-704（metric，B08，M_ORG_DEEP_153_1）；INT-B-ORG-805（metric，B09，M_ORG_COLLAB_CHAIN）；INT-C-ORG-257（data，C03，M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1）；INT-C-ORG-360（data，C04，M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_115_1）；INT-C-X-460（data，C05，M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_115_1）；INT-C-X-490（data，C05，M_TALENT_GRAPH_110_1|M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET|M_TECH_DEEP_130_1|M_TECH_ENTITY_INFLUENCE|M_TECH_GRAPH_104_1|M_TECH_GRAPH_STRUCT|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_REL_STRENGTH|M_TECH_DEEP_131_1|M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK|M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_114_1|M_ORG_GRAPH_115_1）
- 模式：IP-10；IP-08；IP-09；IP-08/IP-09；IP-07/IP-08/IP-09；IP-05
- 同步/异步：无对端调用；异步；同步
- 输入字段：time_range、domain_code、org_key、org_uid[]、industry_code、region_code、org_uid、depth、coop_type
- 输出字段：metric_id、period、algo_version、snapshot_id、payload、strength、coop_type、parent_seq、nodes[org_uid]、edges[src, dst, strength, type]、centrality、src、dst、coop_count、graph_version_id、vid、entity_type、entity_id、label、props_json、TAG technology / talent / institution(ALTER)、EDGE tech_relation / produces / talent_coop / work_at / educated_at / research_coop、innovation_point（A05 提，C04 未收，待定）

## SRS-154 科研机构引入推荐模型

- 确认状态：待确认
- 谁消费：INT-B-ORG-705（metric，B08，M_ORG_DEEP_154_1）；INT-B-ORG-804（metric，B09，M_ORG_ATTRACT_SCORE）；INT-C-ORG-258（data，C03，M_ORG_ATTRACT_SCORE|M_ORG_DEEP_154_1）
- 模式：IP-08；IP-09；IP-08/IP-09
- 同步/异步：异步；同步
- 输入字段：region_code、domain_code、org_uid[]、industry_code、time_range
- 输出字段：metric_id、period、algo_version、snapshot_id、payload、score、parent_seq、org_uid、dims[学术影响力/科技成果/团队实力]、reason

## SRS-155 科研机构扶持推荐模型

- 确认状态：待确认
- 谁消费：INT-B-ORG-706（metric，B08，M_ORG_DEEP_155_1）；INT-B-ORG-806（metric，B09，M_ORG_CULTIVATE_SCORE）；INT-C-ORG-259（data，C03，M_ORG_CULTIVATE_SCORE|M_ORG_DEEP_155_1）
- 模式：IP-08；IP-09；IP-08/IP-09
- 同步/异步：异步；同步
- 输入字段：region_code、domain_code、org_uid[]、industry_code、time_range
- 输出字段：metric_id、period、algo_version、snapshot_id、payload、score、parent_seq、org_uid、dims[成果/经费效率/人才结构]、plan_text

## SRS-98 人才基础指标模型构建

- 确认状态：待确认
- 谁消费：INT-A-TAL-016（page，A01，M_TALENT_BASE_98_1）；INT-A-TAL-1100（page，A12，M_TALENT_BASE_98_1）；INT-A-TAL-1101（page，A12，M_TALENT_BASE_98_1）；INT-A-TAL-1102（page，A12，M_TALENT_BASE_98_1）；INT-A-TAL-1104（page，A12，M_TALENT_BASE_98_1）；INT-A-TAL-1106（page，A12，M_TALENT_BASE_98_1）；INT-A-TAL-1107（page，A12，M_TALENT_BASE_98_1）；INT-A-TAL-1108（page，A12，M_TALENT_BASE_98_1）；INT-A-X-1200（page，A13，M_TALENT_BASE_98_1）；INT-A-X-1202（page，A13，M_TALENT_BASE_98_1）；INT-A-X-1203（page，A13，M_TALENT_BASE_98_1）；INT-A-X-1204（page，A13，M_TALENT_BASE_98_1）；INT-A-X-1205（page，A13，M_TALENT_BASE_98_1）；INT-A-X-1206（page，A13，M_TALENT_BASE_98_1）；INT-A-X-1207（page，A13，M_TALENT_BASE_98_1）；INT-A-X-1208（page，A13，M_TALENT_BASE_98_1）；INT-A-X-1209（page，A13，M_TALENT_BASE_98_1）；INT-B-TAL-200（metric，B03，M_TALENT_BASE_98_1）；INT-B-TAL-208（metric，B03，M_TALENT_ORG_DIST）；INT-B-TAL-209（metric，B03，M_TALENT_REGIONAL_DIST）；INT-B-TAL-211（metric，B03，M_TALENT_SUPPLY_STRUCT）；INT-C-TAL-040（data，C01，M_TALENT_BASE_98_1）；INT-C-TAL-405（data，C05，M_TALENT_BASE_98_1）
- 模式：IP-06；IP-09；TBD
- 同步/异步：同步读；异步；同步；未标明
- 输入字段：time_range、region_code、discipline_code、group_by、domain_code、geo_level、talent_type、q、q_type、format、top_n、org_sector、region_scope、keyword、compare_regions、city_scope、period_grain、org_type、scholar_id、org_id、as_of
- 输出字段：metric_id、region_code、period、value、yoy、share、region_name、headcount、snapshot_id、edu_breakdown、top_orgs、hit_type、org_id、bbox、job_id、parent_region_code、org_name、rank、org_sector、matched、domain_code、payload、talent_cnt、ratio、parent_seq、geo_code、year、bachelor_cnt、master_cnt、doctor_cnt、scholar_id / 分组键、as_of、geo_level(country|admin1|city|district|street)、org_type、degree_level、stat_year

## SRS-110 人才实体识别构建

- 确认状态：待确认
- 谁消费：INT-A-TAL-419（page，A05，M_TALENT_GRAPH_110_1）；INT-A-TAL-1114（page，A12，M_TALENT_GRAPH_110_1）；INT-A-TAL-1117（page，A12，M_TALENT_GRAPH_110_1）；INT-A-X-1324（page，A14，M_TALENT_GRAPH_110_1）；INT-A-X-1327（page，A14，M_TALENT_GRAPH_110_1）；INT-A-X-1418（page，A15，M_TALENT_GRAPH_110_1）；INT-B-TAL-201（metric，B03，M_TALENT_GRAPH_110_1）；INT-C-TAL-041（data，C01，M_TALENT_GRAPH_110_1）；INT-C-TAL-310（data，C04，M_TALENT_DEEP_157_1|M_TALENT_DEEP_160_1|M_TALENT_FLOW_TRACK|M_TALENT_GRAPH_110_1|M_TALENT_RELATION_NET）；INT-C-TAL-400（data，C05，M_TALENT_BASE_98_1|M_TALENT_GRAPH_110_1|M_TALENT_DEEP_157_1|M_TALENT_DEEP_160_1|M_TALENT_FLOW_TRACK|M_TALENT_RELATION_NET）；INT-C-TAL-401（data，C05，M_TALENT_GRAPH_110_1）；INT-C-X-480（data，C05，M_TALENT_DEEP_162_1|M_TALENT_GRAPH_110_1|M_TECH_DEEP_130_1|M_TECH_GRAPH_104_1|M_TECH_COMPOSITE_SCORE）；INT-C-X-490（data，C05，M_TALENT_GRAPH_110_1|M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET|M_TECH_DEEP_130_1|M_TECH_ENTITY_INFLUENCE|M_TECH_GRAPH_104_1|M_TECH_GRAPH_STRUCT|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_REL_STRENGTH|M_TECH_DEEP_131_1|M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK|M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_114_1|M_ORG_GRAPH_115_1）
- 模式：IP-07；TBD；IP-07/IP-08/IP-09；IP-01/IP-07；IP-07/IP-08/IP-11；IP-05
- 同步/异步：异步；未标明；同步读 / 异步
- 输入字段：point_id、entity_types=scholar、scholar_id、talent_key、field_code、depth、domain_code、source_id、org_id、region_code、time_range、as_of、coop_type
- 输出字段：scholar_vid、scholar_id、name、rel_type、org_name、title、field_tags、tag、tag_code、score、model_version、talent_key、field_code、snapshot_id、reason、metric_id、period、algo_version、entity_id、data、algorithm、graph、vid、main_org_uid、source、name_zh、name_en、orc_id、gender、nationality_code(code_country)、src_system、src_person_key、method(rule|jx110|manual)、confidence、version、entity_type(talent|tech|org|region|none)、region_code、domain_code、dims_json、TAG technology / talent / institution(ALTER)、EDGE tech_relation / produces / talent_coop / work_at / educated_at / research_coop、innovation_point（A05 提，C04 未收，待定）

## SRS-111 人才实体关系抽取

- 确认状态：待确认
- 谁消费：INT-A-TAL-1118（page，A12，M_TALENT_GRAPH_111_1）；INT-B-TAL-202（metric，B03，M_TALENT_GRAPH_111_1）；INT-C-TAL-042（data，C01，M_TALENT_GRAPH_111_1）；INT-C-TAL-350（data，C04，M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET）；INT-C-TAL-351（data，C04，M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK|M_TALENT_GRAPH_111_1）；INT-C-TAL-352（data，C04，M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET）；INT-C-TAL-402（data，C05，M_TALENT_DEEP_157_1|M_TALENT_DEEP_164_1|M_TALENT_FLOW_TRACK|M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET）；INT-C-TAL-404（data，C05，M_TALENT_GRAPH_111_1|M_TALENT_DEEP_160_1|M_TALENT_RELATION_NET）；INT-C-X-490（data，C05，M_TALENT_GRAPH_110_1|M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET|M_TECH_DEEP_130_1|M_TECH_ENTITY_INFLUENCE|M_TECH_GRAPH_104_1|M_TECH_GRAPH_STRUCT|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_REL_STRENGTH|M_TECH_DEEP_131_1|M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK|M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_114_1|M_ORG_GRAPH_115_1）
- 模式：IP-07；TBD；IP-07/IP-08/IP-09；IP-02/IP-07；IP-05/IP-07；IP-05
- 同步/异步：异步；未标明；同步读 / 异步
- 输入字段：scholar_id、depth、domain_code、rel_type、org_id、region_code、time_range、as_of、coop_type
- 输出字段：node_id、node_name、edge_type、org_id、snapshot_id、metric_id、period、src_id、dst_id、rel_type、src_scholar_id、dst_type、weight、evidence、src、dst、coop_type、coop_count、strength、start_year、end_year、is_current、degree、grad_year、scholar_id、from_org_uid、to_org_uid、from_region_code、to_region_code、move_year、dst_type(talent|inst|ent|project)、rel_type(coauthor|project|mentor|educated_at)、first_year、TAG technology / talent / institution(ALTER)、EDGE tech_relation / produces / talent_coop / work_at / educated_at / research_coop、innovation_point（A05 提，C04 未收，待定）

## SRS-156 重点人才识别模型

- 确认状态：待确认
- 谁消费：INT-B-TAL-100（metric，B02，M_TALENT_DEEP_156_1）；INT-C-TAL-043（data，C01，M_TALENT_DEEP_156_1|M_TALENT_ORG_DIST|M_TALENT_REGIONAL_DIST）
- 模式：IP-08；TBD
- 同步/异步：异步；未标明
- 输入字段：region_code、time_range、domain_code、scholar_id、org_id、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、scholar_id、is_key、score、reasons、as_of

## SRS-157 人才流动追踪模型

- 确认状态：待确认
- 谁消费：INT-A-TAL-1103（page，A12，M_TALENT_DEEP_157_1）；INT-A-TAL-1109（page，A12，M_TALENT_DEEP_157_1）；INT-A-TAL-1113（page，A12，M_TALENT_DEEP_157_1）；INT-A-X-1201（page，A13，M_TALENT_DEEP_157_1）；INT-B-TAL-101（metric，B02，M_TALENT_DEEP_157_1）；INT-B-TAL-207（metric，B03，M_TALENT_FLOW_TRACK）；INT-C-TAL-044（data，C01，M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK）；INT-C-TAL-351（data，C04，M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK|M_TALENT_GRAPH_111_1）；INT-C-TAL-402（data，C05，M_TALENT_DEEP_157_1|M_TALENT_DEEP_164_1|M_TALENT_FLOW_TRACK|M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET）；INT-C-X-490（data，C05，M_TALENT_GRAPH_110_1|M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET|M_TECH_DEEP_130_1|M_TECH_ENTITY_INFLUENCE|M_TECH_GRAPH_104_1|M_TECH_GRAPH_STRUCT|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_REL_STRENGTH|M_TECH_DEEP_131_1|M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK|M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_114_1|M_ORG_GRAPH_115_1）
- 模式：IP-08；IP-09；TBD；IP-07/IP-08/IP-09；IP-02/IP-07；IP-05
- 同步/异步：异步；同步；未标明；同步读 / 异步
- 输入字段：domain_code、time_range、from_region、to_region、direction、event_type、region_scope、flow_type、region_code、industry_code、scholar_id、org_id、as_of
- 输出字段：from_region、to_region、flow_count、period、event_def_version、snapshot_id、region_code、direction、event_type、metric_id、algo_version、source、payload、year、inflow、outflow、retain、parent_seq、scholar_id、from_org_id、to_org_id、as_of、src、dst、start_year、end_year、is_current、from_org_uid、to_org_uid、from_region_code、to_region_code、move_year、TAG technology / talent / institution(ALTER)、EDGE tech_relation / produces / talent_coop / work_at / educated_at / research_coop、innovation_point（A05 提，C04 未收，待定）

## SRS-158 高校学院新培育人才模型

- 确认状态：待确认
- 谁消费：INT-B-TAL-102（metric，B02，M_TALENT_DEEP_158_1）；INT-B-TAL-214（metric，B03，M_TALENT_UNIV_NEW）；INT-C-TAL-045（data，C01，M_TALENT_DEEP_158_1|M_TALENT_UNIV_NEW）
- 模式：IP-08；IP-09；TBD
- 同步/异步：异步；同步；未标明
- 输入字段：region_code、time_range、domain_code、org_id、scholar_id、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、year、trend、direction、parent_seq、univ_org_id、college、new_talent_cnt、as_of

## SRS-159 深圳重点人才优势和短板分析模型

- 确认状态：待确认
- 谁消费：INT-B-TAL-103（metric，B02，M_TALENT_DEEP_159_1）；INT-B-TAL-212（metric，B03，M_TALENT_SZ_STATUS）；INT-C-TAL-046（data，C01，M_TALENT_DEEP_159_1|M_TALENT_SZ_STATUS）
- 模式：IP-08；IP-09；TBD
- 同步/异步：异步；同步；未标明
- 输入字段：region_code、time_range、domain_code、compare_region、scholar_id、org_id、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、count_side、strength、weakness、parent_seq、domain_code、strength / weakness、score、as_of

## SRS-160 人才关系链模型

- 确认状态：待确认
- 谁消费：INT-A-X-1306（page，A14，M_TALENT_DEEP_160_1）；INT-A-X-1308（page，A14，M_TALENT_DEEP_160_1）；INT-A-X-1320（page，A14，M_TALENT_DEEP_160_1）；INT-A-X-1322（page，A14，M_TALENT_DEEP_160_1）；INT-A-X-1323（page，A14，M_TALENT_DEEP_160_1）；INT-A-X-1326（page，A14，M_TALENT_DEEP_160_1）；INT-A-X-1407（page，A15，M_TALENT_DEEP_160_1）；INT-A-X-1408（page，A15，M_TALENT_DEEP_160_1）；INT-B-TAL-104（metric，B02，M_TALENT_DEEP_160_1）；INT-B-TAL-210（metric，B03，M_TALENT_RELATION_NET）；INT-C-TAL-047（data，C01，M_TALENT_DEEP_160_1|M_TALENT_RELATION_NET）；INT-C-TAL-350（data，C04，M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET）；INT-C-TAL-352（data，C04，M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET）；INT-C-TAL-404（data，C05，M_TALENT_GRAPH_111_1|M_TALENT_DEEP_160_1|M_TALENT_RELATION_NET）；INT-C-X-490（data，C05，M_TALENT_GRAPH_110_1|M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET|M_TECH_DEEP_130_1|M_TECH_ENTITY_INFLUENCE|M_TECH_GRAPH_104_1|M_TECH_GRAPH_STRUCT|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_REL_STRENGTH|M_TECH_DEEP_131_1|M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK|M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_114_1|M_ORG_GRAPH_115_1）
- 模式：IP-08；IP-09；TBD；IP-07/IP-08/IP-09；IP-05/IP-07；IP-05
- 同步/异步：异步；同步；未标明
- 输入字段：talent_key、depth、page、size、coop_type、pair_key、time_range、org_id、domain_code、scholar_ref、relation_type、center_id、scholar_id、region_code、as_of
- 输出字段：talent_key、snapshot_id、src、dst、reason、strength、coop_type、evidence_id、peer_key、relation_type、period、metric_id、algo_version、source、payload、node_cnt、edge_cnt、parent_seq、scholar_id、nodes[]、edges[]、as_of、coop_count、degree、grad_year、src_scholar_id、dst_type(talent|inst|ent|project)、dst_id、rel_type(coauthor|project|mentor|educated_at)、first_year、TAG technology / talent / institution(ALTER)、EDGE tech_relation / produces / talent_coop / work_at / educated_at / research_coop、innovation_point（A05 提，C04 未收，待定）

## SRS-161 人才供需分析评价模型

- 确认状态：待确认
- 谁消费：INT-B-TAL-105（metric，B02，M_TALENT_DEEP_161_1）；INT-B-TAL-213（metric，B03，M_TALENT_SZ_SUPPLY_DEMAND）；INT-C-TAL-048（data，C01，M_TALENT_DEEP_161_1|M_TALENT_SUPPLY_STRUCT|M_TALENT_SZ_SUPPLY_DEMAND）
- 模式：IP-08；IP-09；TBD
- 同步/异步：异步；同步；未标明
- 输入字段：region_code、time_range、domain_code、scholar_id、org_id、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、balance_index、gap_or_surplus、trend、parent_seq、domain_code、region_code、supply、demand、gap、as_of

## SRS-162 人才学术力评估模型

- 确认状态：待确认
- 谁消费：INT-A-TAL-021（page，A01，M_TALENT_DEEP_162_1）；INT-A-TAL-1115（page，A12，M_TALENT_DEEP_162_1）；INT-A-TAL-1116（page，A12，M_TALENT_DEEP_162_1）；INT-A-X-1311（page，A14，M_TALENT_DEEP_162_1）；INT-A-X-1313（page，A14，M_TALENT_DEEP_162_1）；INT-B-TAL-106（metric，B02，M_TALENT_DEEP_162_1）；INT-B-TAL-203（metric，B03，M_TALENT_ACADEMIC_SCORE）；INT-C-TAL-049（data，C01，M_TALENT_ACADEMIC_SCORE|M_TALENT_DEEP_162_1）；INT-C-X-480（data，C05，M_TALENT_DEEP_162_1|M_TALENT_GRAPH_110_1|M_TECH_DEEP_130_1|M_TECH_GRAPH_104_1|M_TECH_COMPOSITE_SCORE）
- 模式：IP-08；IP-09；TBD；IP-07/IP-08/IP-11
- 同步/异步：异步；同步；未标明
- 输入字段：scholar_ids|region_code、discipline_code、top_n、scholar_id、time_range、domain_code、talent_key、region_code、scholar_ref、org_id、as_of
- 输出字段：scholar_id、score、rank、model_version、as_of、paper_count、patent_count、project_count、cited_by、snapshot_id、metric_id、h_index、influence_score、hindex_source、talent_key、academic_score、reason、period、algo_version、source、payload、parent_seq、activity、entity_type(talent|tech|org|region|none)、entity_id、region_code、domain_code、dims_json

## SRS-163 人才产业力评估模型

- 确认状态：待确认
- 谁消费：INT-B-TAL-107（metric，B02，M_TALENT_DEEP_163_1）；INT-B-TAL-206（metric，B03，M_TALENT_INDUSTRY_SCORE）；INT-C-TAL-050（data，C01，M_TALENT_DEEP_163_1|M_TALENT_INDUSTRY_SCORE）
- 模式：IP-08；IP-09；TBD
- 同步/异步：异步；同步；未标明
- 输入字段：region_code、time_range、domain_code、scholar_ref、scholar_id、org_id、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、score、rank、parent_seq、scholar_id、industry_score、dims、as_of

## SRS-164 招入人才推荐模型

- 确认状态：待确认
- 谁消费：INT-A-TAL-1120（page，A12，M_TALENT_DEEP_164_1）；INT-A-X-1402（page，A15，M_TALENT_DEEP_164_1）；INT-A-X-1403（page，A15，M_TALENT_DEEP_164_1）；INT-A-X-1419（page，A15，M_TALENT_DEEP_164_1）；INT-A-X-1421（page，A15，M_TALENT_DEEP_164_1）；INT-B-TAL-108（metric，B02，M_TALENT_DEEP_164_1）；INT-B-TAL-204（metric，B03，M_TALENT_ATTRACT_SCORE）；INT-C-TAL-051（data，C01，M_TALENT_ATTRACT_SCORE|M_TALENT_DEEP_164_1）
- 模式：IP-08；IP-09；TBD
- 同步/异步：异步；同步；未标明
- 输入字段：scholar_id、post_id、talent_key、domain_code、org_id、page、size、region_code、time_range、as_of
- 输出字段：match_score、risk_flags、reason、snapshot_id、talent_key、score、trend、metric_id、name、period、algo_version、source、payload、list_size、parent_seq、scholar_id、recommend_rank、reasons、as_of

## SRS-165 培育人才布局模型

- 确认状态：待确认
- 谁消费：INT-B-TAL-109（metric，B02，M_TALENT_DEEP_165_1）；INT-B-TAL-205（metric，B03，M_TALENT_CULTIVATE_SCORE）；INT-C-TAL-052（data，C01，M_TALENT_CULTIVATE_SCORE|M_TALENT_DEEP_165_1）
- 模式：IP-08；IP-09；TBD
- 同步/异步：异步；同步；未标明
- 输入字段：region_code、time_range、domain_code、scholar_id、org_id、as_of
- 输出字段：snapshot_id、period、algo_version、source、metric_id、payload、score、list_size、parent_seq、domain_code、org_id、layout_score、as_of

## TOPIC-RORG-012 科研机构技术力评价与对比（05 无专叶）

- 确认状态：待确认
- 谁消费：INT-B-ORG-813（metric，B09，M_ORG_TECH_SCORE）；INT-C-ORG-260（data，C03，M_ORG_TECH_SCORE）；INT-C-ORG-360（data，C04，M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_115_1）；INT-C-X-460（data，C05，M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_115_1）；INT-C-X-490（data，C05，M_TALENT_GRAPH_110_1|M_TALENT_DEEP_160_1|M_TALENT_GRAPH_111_1|M_TALENT_RELATION_NET|M_TECH_DEEP_130_1|M_TECH_ENTITY_INFLUENCE|M_TECH_GRAPH_104_1|M_TECH_GRAPH_STRUCT|M_TECH_PATH_CENTRALITY|M_TECH_PATH_KEYNODE|M_TECH_PATH_PRIORITY|M_TECH_EDGE_STRENGTH|M_TECH_ENTITY_REL|M_TECH_ENTITY_TOP5|M_TECH_GRAPH_105_1|M_TECH_REL_STRENGTH|M_TECH_DEEP_131_1|M_TALENT_DEEP_157_1|M_TALENT_FLOW_TRACK|M_ORG_COLLAB_CHAIN|M_ORG_DEEP_153_1|M_ORG_GRAPH_114_1|M_ORG_GRAPH_115_1）
- 模式：IP-08；IP-07/IP-08/IP-09；IP-05
- 同步/异步：异步
- 输入字段：org_keys、indicator_ids、weights、org_uid[]、industry_code、region_code、time_range、org_uid、depth、coop_type
- 输出字段：snapshot_id、period、algo_version、source、metric_id、score、rank、org_uid、weights_in、radar_dims、src、dst、coop_type、coop_count、strength、graph_version_id、vid、entity_type、entity_id、label、props_json、TAG technology / talent / institution(ALTER)、EDGE tech_relation / produces / talent_coop / work_at / educated_at / research_coop、innovation_point（A05 提，C04 未收，待定）

## DS-03-RESULT-001 话题热力图展示

- 确认状态：待确认
- 本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。 B01 初判：M_TECH_DEEP_134_1 同交，主行 SRS-134：前沿热点；展示行 DS-03-RESULT-001/002、DS-09-COMPREHENSIVE-001/002/004 同交 页面卡点名本行，需求并入该页，不单列指标卡：INT-A-TECH-300
- 谁消费：INT-A-TECH-300（page，A04，M_TECH_DEEP_134_1）；INT-C-TECH-156（data，C02，M_TECH_DEEP_134_1|M_TECH_HEAT_INDEX|M_TECH_TOPIC_HEAT）
- 模式：IP-08；TBD
- 同步/异步：异步；未标明
- 输入字段：domain_codes、region_keys、start_year、end_year、topic_keys、technology_id、domain_code、region_scope、time_range、as_of
- 输出字段：topic_key、topic_name、domain_code、year、attention_value、activity_value、snapshot_id、algo_version、source、technology_id / topic_id、heat、growth、term、as_of

## DS-03-RESULT-002 技术话题热度

- 确认状态：待确认
- 本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。 B01 初判：M_TECH_TOPIC_HEAT 同交，主行 SRS-134：只读 ADS；展示行 DS-03-RESULT-002 同交 页面卡点名本行，需求并入该页，不单列指标卡：INT-A-TECH-301
- 谁消费：INT-A-TECH-301（page，A04，M_TECH_TOPIC_HEAT）；INT-C-TECH-156（data，C02，M_TECH_DEEP_134_1|M_TECH_HEAT_INDEX|M_TECH_TOPIC_HEAT）
- 模式：IP-09；TBD
- 同步/异步：异步；未标明
- 输入字段：domain_codes、start_year、end_year、technology_id、domain_code、region_scope、time_range、as_of
- 输出字段：topic_key、topic_name、heat、trend、snapshot_id、technology_id / topic_id、growth、term、as_of

## DS-03-RESULT-004 动态气泡图（阶段/成熟度）

- 确认状态：待确认
- 本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。 B01 初判：M_TECH_DEEP_137_1 同交，主行 SRS-137：技术阶段；展示行 DS-03-RESULT-004/005/006、DS-07-SCI-CREATE-003 同交 页面卡点名本行，需求并入该页，不单列指标卡：INT-A-TECH-309
- 谁消费：INT-A-TECH-309（page，A04，M_TECH_DEEP_137_1）；INT-C-TECH-159（data，C02，M_TECH_DEEP_137_1|M_TECH_LIFE_STAGE|M_TECH_MATURITY_LEVEL|M_TECH_STAGE_JUDGE|M_TECH_SZ_ASSESS）
- 模式：IP-08；TBD
- 同步/异步：异步；未标明
- 输入字段：technology_ids、domain_codes、start_year、end_year、technology_id、domain_code、region_scope、time_range、as_of
- 输出字段：technology_id、technology_name、domain_code、year、stage_code、maturity_value、snapshot_id、algo_version、life_stage、maturity_level、as_of

## DS-03-RESULT-005 技术成熟度

- 确认状态：待确认
- 本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。 B01 初判：M_TECH_MATURITY_LEVEL 同交，主行 SRS-137：展示行 DS-03-RESULT-005；同上 页面卡点名本行，需求并入该页，不单列指标卡：INT-A-TECH-310
- 谁消费：INT-A-TECH-310（page，A04，M_TECH_MATURITY_LEVEL）；INT-C-TECH-159（data，C02，M_TECH_DEEP_137_1|M_TECH_LIFE_STAGE|M_TECH_MATURITY_LEVEL|M_TECH_STAGE_JUDGE|M_TECH_SZ_ASSESS）
- 模式：IP-09；TBD
- 同步/异步：异步；未标明
- 输入字段：technology_ids、start_year、end_year、technology_id、domain_code、region_scope、time_range、as_of
- 输出字段：technology_id、maturity、snapshot_id、life_stage、maturity_level、as_of

## DS-03-RESULT-006 技术发展阶段

- 确认状态：待确认
- 本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。 B01 初判：M_TECH_LIFE_STAGE 同交，主行 SRS-137：展示行 DS-03-RESULT-006；本页读 ADS，专题跑 Job 写同一结果 页面卡点名本行，需求并入该页，不单列指标卡：INT-A-TECH-311
- 谁消费：INT-A-TECH-311（page，A04，M_TECH_LIFE_STAGE）；INT-C-TECH-159（data，C02，M_TECH_DEEP_137_1|M_TECH_LIFE_STAGE|M_TECH_MATURITY_LEVEL|M_TECH_STAGE_JUDGE|M_TECH_SZ_ASSESS）
- 模式：IP-09；TBD
- 同步/异步：异步；未标明
- 输入字段：technology_ids、start_year、end_year、technology_id、domain_code、region_scope、time_range、as_of
- 输出字段：technology_id、stage_code、stage_label、snapshot_id、life_stage、maturity_level、as_of

## DS-07-INDUSTRY-POTENTIAL-002 技术产品成熟度评估

- 确认状态：待确认
- 本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。 B01 初判：M_TECH_DEEP_135_1 同交，主行 SRS-135：产业化潜力；展示行 DS-07-TECH-INNOV-003、DS-07-INDUSTRY-POTENTIAL-002 同交 仅在调用链下游被点名：INT-C-TECH-159
- 谁消费：INT-C-TECH-159（data，C02，M_TECH_DEEP_137_1|M_TECH_LIFE_STAGE|M_TECH_MATURITY_LEVEL|M_TECH_STAGE_JUDGE|M_TECH_SZ_ASSESS）
- 模式：TBD
- 同步/异步：未标明
- 输入字段：technology_id、domain_code、region_scope、time_range、as_of
- 输出字段：technology_id、life_stage、maturity_level、as_of

## DS-07-TECH-INNOV-003 技术市场潜力分析

- 确认状态：待确认
- 本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。 B01 初判：M_TECH_DEEP_135_1 同交，主行 SRS-135：产业化潜力；展示行 DS-07-TECH-INNOV-003、DS-07-INDUSTRY-POTENTIAL-002 同交；M_TECH_DS_07_TECH_INNOV_004 同交，主行 空：同上；兄弟行 DS-07-TECH-INNOV-003 属久新，非本指标 仅在调用链下游被点名：INT-C-TECH-157
- 谁消费：INT-C-TECH-157（data，C02，M_TECH_DEEP_135_1|M_TECH_POTENTIAL_SCORE|M_TECH_SZ_ASSESS）
- 模式：TBD
- 同步/异步：未标明
- 输入字段：technology_id、domain_code、region_scope、time_range、as_of
- 输出字段：technology_id、potential_score、dims、as_of

## DS-07-SCI-CREATE-003 科学研究前沿性分析

- 确认状态：待确认
- 本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。 B01 初判：M_TECH_DEEP_137_1 同交，主行 SRS-137：技术阶段；展示行 DS-03-RESULT-004/005/006、DS-07-SCI-CREATE-003 同交 仅在调用链下游被点名：INT-C-TECH-156
- 谁消费：INT-C-TECH-156（data，C02，M_TECH_DEEP_134_1|M_TECH_HEAT_INDEX|M_TECH_TOPIC_HEAT）
- 模式：TBD
- 同步/异步：未标明
- 输入字段：technology_id、domain_code、region_scope、time_range、as_of
- 输出字段：technology_id / topic_id、heat、growth、term、as_of

## DS-09-COMPREHENSIVE-001 全球热点技术捕捉 · 热度

- 确认状态：待确认
- 本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。 B01 初判：M_TECH_DEEP_134_1 同交，主行 SRS-134：前沿热点；展示行 DS-03-RESULT-001/002、DS-09-COMPREHENSIVE-001/002/004 同交 页面卡点名本行，需求并入该页，不单列指标卡：INT-A-X-1000
- 谁消费：INT-A-X-1000（page，A11，无 metric_id）；INT-C-TECH-156（data，C02，M_TECH_DEEP_134_1|M_TECH_HEAT_INDEX|M_TECH_TOPIC_HEAT）
- 模式：IP-08；TBD
- 同步/异步：异步；未标明
- 输入字段：domain_code、time_range、ipc4、technology_id、region_scope、as_of
- 输出字段：ipc4、name、heat、growth、period、metric_id、snapshot_id、technology_id / topic_id、term、as_of

## DS-09-COMPREHENSIVE-002 全球热点技术捕捉 · 增速

- 确认状态：待确认
- 本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。 仅在调用链下游被点名：INT-C-TECH-156
- 谁消费：INT-C-TECH-156（data，C02，M_TECH_DEEP_134_1|M_TECH_HEAT_INDEX|M_TECH_TOPIC_HEAT）
- 模式：TBD
- 同步/异步：未标明
- 输入字段：technology_id、domain_code、region_scope、time_range、as_of
- 输出字段：technology_id / topic_id、heat、growth、term、as_of

## DS-09-COMPREHENSIVE-004 技术与产业热点动态跟踪

- 确认状态：待确认
- 本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。 页面卡点名本行，需求并入该页，不单列指标卡：INT-A-X-1002
- 谁消费：INT-A-X-1002（page，A11，无 metric_id）；INT-C-TECH-156（data，C02，M_TECH_DEEP_134_1|M_TECH_HEAT_INDEX|M_TECH_TOPIC_HEAT）
- 模式：IP-08；TBD
- 同步/异步：异步；未标明
- 输入字段：domain_code、time_range、region_code、technology_id、region_scope、as_of
- 输出字段：domain_code、timeline、geo_points、period、snapshot_id、technology_id / topic_id、heat、growth、term、as_of

## DS-08-VIZ-001 专家 H 指数排行

- 确认状态：待确认
- 本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。 B01 初判：M_TALENT_DEEP_162_1 同交，主行 SRS-162：学术力；展示行 DS-08-VIZ-001/004 与本库叶同交 页面卡点名本行，需求并入该页，不单列指标卡：INT-A-TAL-910
- 谁消费：INT-A-TAL-910（page，A10，无 metric_id）；INT-C-TAL-049（data，C01，M_TALENT_ACADEMIC_SCORE|M_TALENT_DEEP_162_1）
- 模式：IP-08；TBD
- 同步/异步：异步；未标明
- 输入字段：domain_code、org_type、region_code、top_n、scholar_id、org_id、time_range、as_of
- 输出字段：scholar_id、name、org_uid、org_name、h_index、citations、publications、field、region_code、snapshot_id、data_as_of、academic_score、activity、as_of

## DS-08-VIZ-004 专家活跃度

- 确认状态：待确认
- 本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。 页面卡点名本行，需求并入该页，不单列指标卡：INT-A-TAL-914
- 谁消费：INT-A-TAL-914（page，A10，无 metric_id）；INT-C-TAL-049（data，C01，M_TALENT_ACADEMIC_SCORE|M_TALENT_DEEP_162_1）
- 模式：IP-08；TBD
- 同步/异步：异步；未标明
- 输入字段：scholar_ids、time_range、scholar_id、org_id、region_code、domain_code、as_of
- 输出字段：scholar_id、month、paper_count、project_count、activity_score、source、snapshot_id、academic_score、h_index、activity、as_of
