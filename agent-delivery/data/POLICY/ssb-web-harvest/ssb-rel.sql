-- 固态电池 8 条：产业关联 + 条款
-- 产业码：Demo 产业链 dwd_industry_chain_info 共 157 个节点，没有名为「固态电池」的节点。
-- 对应节点是「动力电池」industry_link_code=INB17060102，产业「智能网联新能源汽车」INB1706。
-- 关联表存的是图谱 VID：segment:INB17060102。
-- 条款写入 ads.policy_text_parse.structured_elements，不另建表。日本条无正文，只写产业关联。
-- 只追加。重复执行不会插出第二条未删除的同一链码。

-- demo_gkxlumenx_dwd.policy_industry_rel  已有同一 policy_id + 链码的未删除行则跳过
INSERT INTO demo_gkxlumenx_dwd.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-gov-5556716', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_dwd.policy_industry_rel
  WHERE policy_id = 'cn-gov-5556716' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_dwd.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-gov-5737584', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_dwd.policy_industry_rel
  WHERE policy_id = 'cn-gov-5737584' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_dwd.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-gov-7041785', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_dwd.policy_industry_rel
  WHERE policy_id = 'cn-gov-7041785' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_dwd.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-gov-7067354', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_dwd.policy_industry_rel
  WHERE policy_id = 'cn-gov-7067354' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_dwd.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-gov-6999382', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_dwd.policy_industry_rel
  WHERE policy_id = 'cn-gov-6999382' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_dwd.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-zh-3840797', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_dwd.policy_industry_rel
  WHERE policy_id = 'cn-zh-3840797' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_dwd.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-sd-10344208', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_dwd.policy_industry_rel
  WHERE policy_id = 'cn-sd-10344208' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_dwd.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'gl-meti-20220831', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_dwd.policy_industry_rel
  WHERE policy_id = 'gl-meti-20220831' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);

-- demo_gkxlumenx_ads.policy_industry_rel  已有同一 policy_id + 链码的未删除行则跳过
INSERT INTO demo_gkxlumenx_ads.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-gov-5556716', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_industry_rel
  WHERE policy_id = 'cn-gov-5556716' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_ads.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-gov-5737584', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_industry_rel
  WHERE policy_id = 'cn-gov-5737584' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_ads.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-gov-7041785', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_industry_rel
  WHERE policy_id = 'cn-gov-7041785' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_ads.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-gov-7067354', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_industry_rel
  WHERE policy_id = 'cn-gov-7067354' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_ads.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-gov-6999382', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_industry_rel
  WHERE policy_id = 'cn-gov-6999382' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_ads.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-zh-3840797', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_industry_rel
  WHERE policy_id = 'cn-zh-3840797' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_ads.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'cn-sd-10344208', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_industry_rel
  WHERE policy_id = 'cn-sd-10344208' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);
INSERT INTO demo_gkxlumenx_ads.policy_industry_rel
  (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time)
SELECT 'gl-meti-20220831', '动力电池', 'segment:INB17060102', 0, NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_industry_rel
  WHERE policy_id = 'gl-meti-20220831' AND industry_link_code = 'segment:INB17060102' AND is_deleted = 0
);

-- 条款。先更新已有解析行，没有行再插入。
-- cn-gov-5556716 条款 1 条
UPDATE demo_gkxlumenx_ads.policy_text_parse
SET title = '国务院办公厅关于印发新能源汽车产业发展规划（2021—2035年）的通知',
    summary = '实施电池技术突破行动，加快固态动力电池技术研发及产业化。',
    structured_elements = JSON_MERGE_PATCH(COALESCE(structured_elements, '{}'), CAST('{"clauses":[{"no":"专栏1","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"实施电池技术突破行动。开展正负极材料、电解液、隔膜、膜电极等关键核心技术研究，加强高强度、轻量化、高安全、低成本、长寿命的动力电池和燃料电池系统短板技术攻关，加快固态动力电池技术研发及产业化。"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON)),
    model_version = 'clause-rule-v1',
    metric_id = 'M_POLICY_TEXT_PARSE',
    update_time = NOW()
WHERE policy_id = 'cn-gov-5556716';
INSERT INTO demo_gkxlumenx_ads.policy_text_parse
  (policy_id, title, summary, structured_elements, auto_tags, model_version, metric_id, calc_batch_id, create_time, update_time)
SELECT 'cn-gov-5556716', '国务院办公厅关于印发新能源汽车产业发展规划（2021—2035年）的通知', '实施电池技术突破行动，加快固态动力电池技术研发及产业化。', CAST('{"clauses":[{"no":"专栏1","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"实施电池技术突破行动。开展正负极材料、电解液、隔膜、膜电极等关键核心技术研究，加强高强度、轻量化、高安全、低成本、长寿命的动力电池和燃料电池系统短板技术攻关，加快固态动力电池技术研发及产业化。"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON), CAST('[]' AS JSON),
       'clause-rule-v1', 'M_POLICY_TEXT_PARSE', 'ssb-rel', NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_text_parse WHERE policy_id = 'cn-gov-5556716'
);

-- cn-gov-5737584 条款 2 条
UPDATE demo_gkxlumenx_ads.policy_text_parse
SET title = '工业和信息化部等六部门关于推动能源电子产业发展的指导意见',
    summary = '加快研发固态电池、钠离子电池、氢储能/燃料电池等新型电池，并加强固态电池标准体系研究。',
    structured_elements = JSON_MERGE_PATCH(COALESCE(structured_elements, '{}'), CAST('{"clauses":[{"no":"（八）","category":"保障机制","target":"","support_type":"","amount":"","condition":"","excerpt":"寿命高安全性电池体系、大规模大容量高效储能、交通工具移动储能等关键技术，加快研发固态电池、钠离子电池、氢储能/燃料电池等新型电池。推广智能化生产工艺与装备、先进集成及制造技术、性能测试和评估技术。提高锂、镍、钴、铂等关键资源保障能力，加强替代材料的开发应用。推广基于优势互补功率型和能量型电化学储能技术的混合储能系统。支持建立锂电等全生命周期溯源管理平台，开展"},{"no":"（十五）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"家标准、行业标准和团体标准，研究制定锂离子电池全生命周期评价体系及安全标准，加强固态电池、钠离子电池、超级电容器、氢储能/燃料电池等标准体系研究。开展能源电子智能制造与运维、管理控制系统等相关标准研制，加强与现行能源电力系统标准衔接，推动建立产品制造、建设安装、运行监测等环节的安全标准及管理体系。开展国际标准化合作，积极参与国际标准研究制定。"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON)),
    model_version = 'clause-rule-v1',
    metric_id = 'M_POLICY_TEXT_PARSE',
    update_time = NOW()
WHERE policy_id = 'cn-gov-5737584';
INSERT INTO demo_gkxlumenx_ads.policy_text_parse
  (policy_id, title, summary, structured_elements, auto_tags, model_version, metric_id, calc_batch_id, create_time, update_time)
SELECT 'cn-gov-5737584', '工业和信息化部等六部门关于推动能源电子产业发展的指导意见', '加快研发固态电池、钠离子电池、氢储能/燃料电池等新型电池，并加强固态电池标准体系研究。', CAST('{"clauses":[{"no":"（八）","category":"保障机制","target":"","support_type":"","amount":"","condition":"","excerpt":"寿命高安全性电池体系、大规模大容量高效储能、交通工具移动储能等关键技术，加快研发固态电池、钠离子电池、氢储能/燃料电池等新型电池。推广智能化生产工艺与装备、先进集成及制造技术、性能测试和评估技术。提高锂、镍、钴、铂等关键资源保障能力，加强替代材料的开发应用。推广基于优势互补功率型和能量型电化学储能技术的混合储能系统。支持建立锂电等全生命周期溯源管理平台，开展"},{"no":"（十五）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"家标准、行业标准和团体标准，研究制定锂离子电池全生命周期评价体系及安全标准，加强固态电池、钠离子电池、超级电容器、氢储能/燃料电池等标准体系研究。开展能源电子智能制造与运维、管理控制系统等相关标准研制，加强与现行能源电力系统标准衔接，推动建立产品制造、建设安装、运行监测等环节的安全标准及管理体系。开展国际标准化合作，积极参与国际标准研究制定。"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON), CAST('[]' AS JSON),
       'clause-rule-v1', 'M_POLICY_TEXT_PARSE', 'ssb-rel', NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_text_parse WHERE policy_id = 'cn-gov-5737584'
);

-- cn-gov-7041785 条款 1 条
UPDATE demo_gkxlumenx_ads.policy_text_parse
SET title = '国家能源局等部门关于推进能源装备高质量发展的指导意见',
    summary = '推进固态电池关键装备，构建低成本长时液流电池装备体系。',
    structured_elements = JSON_MERGE_PATCH(COALESCE(structured_elements, '{}'), CAST('{"clauses":[{"no":"（六）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"动建立高安全、高可靠电池储能装备体系，研制长寿命、宽温域、低衰减锂电池、钠电池、固态电池关键装备，构建低成本长时钒基、铁基、有机等液流电池装备体系。突破电池管理系统安全监测、隐患预警和主动防护技术，提升储能电池本征安全性能。突破大容量、低成本物理储能技术，研制高水头抽水蓄能机组及大容量变速机组，研发大功率、高参数压缩机及膨胀机等关键装备和低成本、高效率、长寿"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON)),
    model_version = 'clause-rule-v1',
    metric_id = 'M_POLICY_TEXT_PARSE',
    update_time = NOW()
WHERE policy_id = 'cn-gov-7041785';
INSERT INTO demo_gkxlumenx_ads.policy_text_parse
  (policy_id, title, summary, structured_elements, auto_tags, model_version, metric_id, calc_batch_id, create_time, update_time)
SELECT 'cn-gov-7041785', '国家能源局等部门关于推进能源装备高质量发展的指导意见', '推进固态电池关键装备，构建低成本长时液流电池装备体系。', CAST('{"clauses":[{"no":"（六）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"动建立高安全、高可靠电池储能装备体系，研制长寿命、宽温域、低衰减锂电池、钠电池、固态电池关键装备，构建低成本长时钒基、铁基、有机等液流电池装备体系。突破电池管理系统安全监测、隐患预警和主动防护技术，提升储能电池本征安全性能。突破大容量、低成本物理储能技术，研制高水头抽水蓄能机组及大容量变速机组，研发大功率、高参数压缩机及膨胀机等关键装备和低成本、高效率、长寿"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON), CAST('[]' AS JSON),
       'clause-rule-v1', 'M_POLICY_TEXT_PARSE', 'ssb-rel', NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_text_parse WHERE policy_id = 'cn-gov-7041785'
);

-- cn-gov-7067354 条款 1 条
UPDATE demo_gkxlumenx_ads.policy_text_parse
SET title = '鼓励外商投资产业目录（2025年版）',
    summary = '鼓励类包括太阳能电池、燃料电池、钠离子电池、固态电池。',
    structured_elements = JSON_MERGE_PATCH(COALESCE(structured_elements, '{}'), CAST('{"clauses":[{"no":"（二十一）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"锌镍蓄电池、钠盐电池、锌银蓄电池、锂离子电池、太阳能电池、燃料电池、钠离子电池、固态电池 373.电动机采用直流调速技术的制冷空调用压缩机、采用CO2、R290自然工质制冷空调压缩机、应用可再生能源（空气源、水源、地源）制冷空调设备制造，直流调速技术的制冷空调器、环保型冷媒（低GWP冷媒）技术的空调器制造 374.太阳能空调、采暖系统、太阳能干燥"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON)),
    model_version = 'clause-rule-v1',
    metric_id = 'M_POLICY_TEXT_PARSE',
    update_time = NOW()
WHERE policy_id = 'cn-gov-7067354';
INSERT INTO demo_gkxlumenx_ads.policy_text_parse
  (policy_id, title, summary, structured_elements, auto_tags, model_version, metric_id, calc_batch_id, create_time, update_time)
SELECT 'cn-gov-7067354', '鼓励外商投资产业目录（2025年版）', '鼓励类包括太阳能电池、燃料电池、钠离子电池、固态电池。', CAST('{"clauses":[{"no":"（二十一）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"锌镍蓄电池、钠盐电池、锌银蓄电池、锂离子电池、太阳能电池、燃料电池、钠离子电池、固态电池 373.电动机采用直流调速技术的制冷空调用压缩机、采用CO2、R290自然工质制冷空调压缩机、应用可再生能源（空气源、水源、地源）制冷空调设备制造，直流调速技术的制冷空调器、环保型冷媒（低GWP冷媒）技术的空调器制造 374.太阳能空调、采暖系统、太阳能干燥"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON), CAST('[]' AS JSON),
       'clause-rule-v1', 'M_POLICY_TEXT_PARSE', 'ssb-rel', NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_text_parse WHERE policy_id = 'cn-gov-7067354'
);

-- cn-gov-6999382 条款 2 条
UPDATE demo_gkxlumenx_ads.policy_text_parse
SET title = '西部地区鼓励类产业目录（2025年本）',
    summary = '鼓励电池制造，范围包括锂离子电池、钠离子电池、聚合物锂离子电池、半（全）固态电池及电池配套产品。',
    structured_elements = JSON_MERGE_PATCH(COALESCE(structured_elements, '{}'), CAST('{"clauses":[{"no":"20.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"生产，电池材料生产，电池制造（锂离子电池、钠离子电池、聚合物锂离子电池、半（全）固态电池，电池配套产品）"},{"no":"34.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"品的先进生产技术开发及生产，三元前驱体及正极材料、磷酸铁锂前驱体及正极材料生产，固态电池、钠离子电池等新型动力电池及关键材料、设备和管理系统研发制造，低钴/无钴正极材料及固态电池、锂硫电池等先进电池及材料研发制造"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON)),
    model_version = 'clause-rule-v1',
    metric_id = 'M_POLICY_TEXT_PARSE',
    update_time = NOW()
WHERE policy_id = 'cn-gov-6999382';
INSERT INTO demo_gkxlumenx_ads.policy_text_parse
  (policy_id, title, summary, structured_elements, auto_tags, model_version, metric_id, calc_batch_id, create_time, update_time)
SELECT 'cn-gov-6999382', '西部地区鼓励类产业目录（2025年本）', '鼓励电池制造，范围包括锂离子电池、钠离子电池、聚合物锂离子电池、半（全）固态电池及电池配套产品。', CAST('{"clauses":[{"no":"20.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"生产，电池材料生产，电池制造（锂离子电池、钠离子电池、聚合物锂离子电池、半（全）固态电池，电池配套产品）"},{"no":"34.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"品的先进生产技术开发及生产，三元前驱体及正极材料、磷酸铁锂前驱体及正极材料生产，固态电池、钠离子电池等新型动力电池及关键材料、设备和管理系统研发制造，低钴/无钴正极材料及固态电池、锂硫电池等先进电池及材料研发制造"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON), CAST('[]' AS JSON),
       'clause-rule-v1', 'M_POLICY_TEXT_PARSE', 'ssb-rel', NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_text_parse WHERE policy_id = 'cn-gov-6999382'
);

-- cn-zh-3840797 条款 22 条
UPDATE demo_gkxlumenx_ads.policy_text_parse
SET title = '珠海市人民政府办公室关于印发《珠海市推动固态电池产业发展行动方案（2025-2030年）》的通知',
    summary = '印发《珠海市推动固态电池产业发展行动方案（2025-2030年）》，推动固态电池关键技术、材料和场景应用。',
    structured_elements = JSON_MERGE_PATCH(COALESCE(structured_elements, '{}'), CAST('{"clauses":[{"no":"一、","category":"政策目标","target":"","support_type":"","amount":"","condition":"","excerpt":"发展新质生产力，以碳达峰碳中和为目标，助力构建清洁低碳、安全高效的能源体系，紧抓固态电池产业发展的战略机遇期，推动创新链、产业链、资金链、人才链深度融合，稳步推动固态电池关键技术持续进步和应用场景有序拓展，支持产业链上下游协同发展，提升产业基础能力和配套水平，推动固态电池产业集聚发展取得积极成效。"},{"no":"二、","category":"政策目标","target":"","support_type":"","amount":"","condition":"","excerpt":"发展目标 到2027年，着力于固态电池关键材料、关键技术攻坚，推动固态电池行业中试平台建立，聚焦前沿技术驱动、未来高成长性和战略支撑性的产业方向，布局一批技术创新项目，设立5家工程（技术）研究中心、重点实验室等科技创新平台，引进一批具备成长潜力的固态电池企业，引导本地锂电池产业链企业探索布局固态电池关键环节，夯实固态电池产业发展基础。 到2030年，固态电池"},{"no":"（一）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"固态电池电芯制造 聚焦高端消费电子等固态电池率先应用领域，推进半固态电池产业化和全固态电池研发进程。持续优化半固态电池在能量密度、循环寿命、安全性等方面的技术指标，提高半固态电池产品制造良率和生产效率。突破界面电阻高、电导率低、稳定性不足等固态电池技术瓶颈，支持攻关固-固界面导电机理、固态电池内部串联高效集成等固态电池核心问题，攻关固态电池低成本规模化生产关"},{"no":"（二）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"固态电池上游生产设备 依托珠海高端装备制造产业基础，重点发展“低能耗、低成本、高性能”的固态电池设备，提升前、中、后段固态电池生产设备的精度和效率，布局干法电极等下一代电池生产设备，支持开发干法电极高效混料机、干法成膜复合一体机、固态电解质负极复合机、锂金属-铜箔复合机等关键设备。"},{"no":"（三）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"固态电池上游材料 固态电解质。依托固态电池厂商发展氧化物、硫化物、聚合物等多元技术路线，突破超薄固态电解质膜规模化制备技术，开发高电导率和高稳定性的固态电解质。 正负极材料。重点布局富锂锰基正极、高镍三元正极、硅碳负极、锂金属负极等固态电池关键原材料，支持开发电极适配性更高的新型正负极材料，推动正负极材料在固态电池的应用突破。"},{"no":"（一）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"推进固态电池研发创新"},{"no":"1.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"加快关键核心技术攻关。鼓励企业加大对固态电池的研发投入，重点培育能量密度超350Wh/kg的半固态电池和超400Wh/kg的全固态电池项目，推动固态电池产品规模化量产落地。聚焦关键核心技术、行业共性技术、前沿交叉技术领域，发挥应用场景牵引优势，开展半固态/全固态电池示范应用，滚动实施一批重大、重点固态电池科技创新项目，加快技术研发和产业化。（各区、市发展改革"},{"no":"2.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"设技术创新中心、工程（技术）研究中心、重点实验室、创新实践平台等科技创新平台，对固态电池材料、体系、应用孵化等方面进行研究，提升全市固态电池研发的协同性。支持具有重要影响力的技术创新和研发成果在珠海开展工程测试、中试和成果转化，搭建固态电池政产学研用协同创新平台，引导固态电池制造、材料、关键设备、工艺等技术研发储备，促进产学研成果落地。（各区、市科技创新局）"},{"no":"3.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"支持科技研发成果转化。支持企业围绕固态电池前沿技术领域和新型产业生态，前瞻研究相应标准体系。开展固态电池产品专利转化、科技成果转化评价等工作，强化国际知识产权风险预警及纠纷应对指导，促进知识产权创造运用。（市科技创新局、市市场监管局）"},{"no":"（二）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"加快固态电池规模化发展"},{"no":"1.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"竞争力的骨干企业，开展精准招商和靶向招商，对科技含量高、带动性强、发展潜力巨大的固态电池项目予以重点支持。发挥龙头企业带动作用，开展“链式招商”和“以商引商”，吸引上下游企业集聚发展，打造产业招商新势能。引导现有电池制造企业拓展固态电池业务，开展增资扩产与技术改造，推动企业融通创新。（各区、市发展改革局、市工业和信息化局、市投资服务署，各国企）"},{"no":"2.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"优化固态电池产业布局。结合低空经济、云上智城、具身智能等下游应用领域，依托现有的“5.0产业新空间”建设固态电池先导区及集聚区，支持高新区建设固态电池专业园区，在珠海打造具有标杆性、创新性、示范性的固态电池产业集群。（各区、市发展改革局、市工业和信息化局、市国资委、市投资服务署，各国企）"},{"no":"（三）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"拓展固态电池场景应用"},{"no":"1.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"加大终端应用牵引。建立应用牵引协同创新机制，以示范项目带动固态电池在便携终端、智能穿戴等高端消费电子领域率先应用，拓展固态电池在“云上智城”、新型储能、具身智能、低空经济、深海作业等场景中的终端产品应用，推进“固态电池+新场景”创新发展，持续丰富应用生态，扩大固态电池应用场景。（市发展改革局、市工业和信息化局）"},{"no":"2.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"开拓固态电池市场。推动粤港澳大湾区资源协同，积极承接大湾区固态电池产业资源、创新资源、研发资源，在新技术研发、产品研发、检测检验等领域加强合作，引导带动湾区社会资本投入固态电池科研成果的产业化，支持开展产供需用对接，深化区域共同体合作。鼓励固态电池企业与消费电子、低空飞行器、具身智能等终端应用企业建立稳定合作关系，通过技术合作、签订长单、协同研发等方式，推动"},{"no":"（四）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"加强固态电池产业生态营造"},{"no":"1.","category":"保障机制","target":"","support_type":"","amount":"","condition":"","excerpt":"加强产业人才引育。结合国家和省级重大人才工程，引进固态电池领域的创新创业团队，引进培养相关领域高水平科学家、复合型人才、跨学科交叉人才，为人才（团队）提供相关支持。加强中山大学珠海校区、北京理工大学（珠海）等本地高校在固态电池、动力电池等方向的学科建设，鼓励高职院校依据需求进行学科专业设置调整。支持完善技术型企业职称评审制度，鼓励符合条件的技术与研发人员申报"},{"no":"2.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"珠海国有资本等政府投资资金的杠杆和引导作用，充分发挥市新质生产力基金群的作用，为固态电池产业的升级壮大以及向高端价值链延伸等“新质化”提供更为充分的资源支持。聚集天使投资、创业投资等各类机构，为固态电池企业提供全链条金融服务。鼓励金融机构围绕固态电池产业链企业，开展配套中小企业供应链融资行动，支持企业以应收账款、仓单和存货质押等进行融资。（市工业和信息化局，"},{"no":"3.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"培育产业促进机构。成立固态电池产业发展联盟，聚焦关键技术、关键支撑、关键项目、关键资源，推动实现资源共享、优势互补、共促发展，促进上下游企业在珠海集聚发展。鼓励行业协会、研究机构、智库机构等发挥桥梁纽带作用，强化政产学研合作和上下游融通对接，开展标准制定、决策咨询、行业交流等多种形态活动，充分发挥行业组织公共服务和支撑作用，持续引导行业有序规范发展。（市工业"},{"no":"4.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"组织固态电池应用研讨会议。以企业家畅享会、供需对接会等形式，聚焦“应用场景拉动，电芯企业牵引，上下游聚集”，共建珠海固态电池生态，促进企业间交流合作。鼓励固态电池行业组织和各类创新主体，在珠海举办具有影响力且有较强行业示范带动性的应用研讨会、商机对接会、展览等活动。（市工业和信息化局、市商务局，科技集团）"},{"no":"（二）","category":"保障机制","target":"","support_type":"","amount":"","condition":"","excerpt":"平竞争、健康有序的市场发展环境。健全政银企合作机制，鼓励国有企业开展战略投资，为固态电池产业发展提供长期稳定资金。建立适应固态电池发展的统计机制，研究并完善固态电池相关产业分类标准，制订固态电池统计指标体系，健全相应的考核机制。"},{"no":"（三）","category":"保障机制","target":"","support_type":"","amount":"","condition":"","excerpt":"强化要素保障 统筹政府资源为固态电池产业建设提供金融服务、业务指导等服务支撑。积极推送固态电池产业项目、技术创新项目以及示范应用项目纳入省有关奖励、资助清单，支持固态电池项目优先列入市重大项目库。 附件： 1．珠海市人民政府办公室关于印发《珠海市推动固态电池产业发展行动方案（2025-2030年）》的通知（珠府办函〔2025〕99号） .wps"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON)),
    model_version = 'clause-rule-v1',
    metric_id = 'M_POLICY_TEXT_PARSE',
    update_time = NOW()
WHERE policy_id = 'cn-zh-3840797';
INSERT INTO demo_gkxlumenx_ads.policy_text_parse
  (policy_id, title, summary, structured_elements, auto_tags, model_version, metric_id, calc_batch_id, create_time, update_time)
SELECT 'cn-zh-3840797', '珠海市人民政府办公室关于印发《珠海市推动固态电池产业发展行动方案（2025-2030年）》的通知', '印发《珠海市推动固态电池产业发展行动方案（2025-2030年）》，推动固态电池关键技术、材料和场景应用。', CAST('{"clauses":[{"no":"一、","category":"政策目标","target":"","support_type":"","amount":"","condition":"","excerpt":"发展新质生产力，以碳达峰碳中和为目标，助力构建清洁低碳、安全高效的能源体系，紧抓固态电池产业发展的战略机遇期，推动创新链、产业链、资金链、人才链深度融合，稳步推动固态电池关键技术持续进步和应用场景有序拓展，支持产业链上下游协同发展，提升产业基础能力和配套水平，推动固态电池产业集聚发展取得积极成效。"},{"no":"二、","category":"政策目标","target":"","support_type":"","amount":"","condition":"","excerpt":"发展目标 到2027年，着力于固态电池关键材料、关键技术攻坚，推动固态电池行业中试平台建立，聚焦前沿技术驱动、未来高成长性和战略支撑性的产业方向，布局一批技术创新项目，设立5家工程（技术）研究中心、重点实验室等科技创新平台，引进一批具备成长潜力的固态电池企业，引导本地锂电池产业链企业探索布局固态电池关键环节，夯实固态电池产业发展基础。 到2030年，固态电池"},{"no":"（一）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"固态电池电芯制造 聚焦高端消费电子等固态电池率先应用领域，推进半固态电池产业化和全固态电池研发进程。持续优化半固态电池在能量密度、循环寿命、安全性等方面的技术指标，提高半固态电池产品制造良率和生产效率。突破界面电阻高、电导率低、稳定性不足等固态电池技术瓶颈，支持攻关固-固界面导电机理、固态电池内部串联高效集成等固态电池核心问题，攻关固态电池低成本规模化生产关"},{"no":"（二）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"固态电池上游生产设备 依托珠海高端装备制造产业基础，重点发展“低能耗、低成本、高性能”的固态电池设备，提升前、中、后段固态电池生产设备的精度和效率，布局干法电极等下一代电池生产设备，支持开发干法电极高效混料机、干法成膜复合一体机、固态电解质负极复合机、锂金属-铜箔复合机等关键设备。"},{"no":"（三）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"固态电池上游材料 固态电解质。依托固态电池厂商发展氧化物、硫化物、聚合物等多元技术路线，突破超薄固态电解质膜规模化制备技术，开发高电导率和高稳定性的固态电解质。 正负极材料。重点布局富锂锰基正极、高镍三元正极、硅碳负极、锂金属负极等固态电池关键原材料，支持开发电极适配性更高的新型正负极材料，推动正负极材料在固态电池的应用突破。"},{"no":"（一）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"推进固态电池研发创新"},{"no":"1.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"加快关键核心技术攻关。鼓励企业加大对固态电池的研发投入，重点培育能量密度超350Wh/kg的半固态电池和超400Wh/kg的全固态电池项目，推动固态电池产品规模化量产落地。聚焦关键核心技术、行业共性技术、前沿交叉技术领域，发挥应用场景牵引优势，开展半固态/全固态电池示范应用，滚动实施一批重大、重点固态电池科技创新项目，加快技术研发和产业化。（各区、市发展改革"},{"no":"2.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"设技术创新中心、工程（技术）研究中心、重点实验室、创新实践平台等科技创新平台，对固态电池材料、体系、应用孵化等方面进行研究，提升全市固态电池研发的协同性。支持具有重要影响力的技术创新和研发成果在珠海开展工程测试、中试和成果转化，搭建固态电池政产学研用协同创新平台，引导固态电池制造、材料、关键设备、工艺等技术研发储备，促进产学研成果落地。（各区、市科技创新局）"},{"no":"3.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"支持科技研发成果转化。支持企业围绕固态电池前沿技术领域和新型产业生态，前瞻研究相应标准体系。开展固态电池产品专利转化、科技成果转化评价等工作，强化国际知识产权风险预警及纠纷应对指导，促进知识产权创造运用。（市科技创新局、市市场监管局）"},{"no":"（二）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"加快固态电池规模化发展"},{"no":"1.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"竞争力的骨干企业，开展精准招商和靶向招商，对科技含量高、带动性强、发展潜力巨大的固态电池项目予以重点支持。发挥龙头企业带动作用，开展“链式招商”和“以商引商”，吸引上下游企业集聚发展，打造产业招商新势能。引导现有电池制造企业拓展固态电池业务，开展增资扩产与技术改造，推动企业融通创新。（各区、市发展改革局、市工业和信息化局、市投资服务署，各国企）"},{"no":"2.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"优化固态电池产业布局。结合低空经济、云上智城、具身智能等下游应用领域，依托现有的“5.0产业新空间”建设固态电池先导区及集聚区，支持高新区建设固态电池专业园区，在珠海打造具有标杆性、创新性、示范性的固态电池产业集群。（各区、市发展改革局、市工业和信息化局、市国资委、市投资服务署，各国企）"},{"no":"（三）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"拓展固态电池场景应用"},{"no":"1.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"加大终端应用牵引。建立应用牵引协同创新机制，以示范项目带动固态电池在便携终端、智能穿戴等高端消费电子领域率先应用，拓展固态电池在“云上智城”、新型储能、具身智能、低空经济、深海作业等场景中的终端产品应用，推进“固态电池+新场景”创新发展，持续丰富应用生态，扩大固态电池应用场景。（市发展改革局、市工业和信息化局）"},{"no":"2.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"开拓固态电池市场。推动粤港澳大湾区资源协同，积极承接大湾区固态电池产业资源、创新资源、研发资源，在新技术研发、产品研发、检测检验等领域加强合作，引导带动湾区社会资本投入固态电池科研成果的产业化，支持开展产供需用对接，深化区域共同体合作。鼓励固态电池企业与消费电子、低空飞行器、具身智能等终端应用企业建立稳定合作关系，通过技术合作、签订长单、协同研发等方式，推动"},{"no":"（四）","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"加强固态电池产业生态营造"},{"no":"1.","category":"保障机制","target":"","support_type":"","amount":"","condition":"","excerpt":"加强产业人才引育。结合国家和省级重大人才工程，引进固态电池领域的创新创业团队，引进培养相关领域高水平科学家、复合型人才、跨学科交叉人才，为人才（团队）提供相关支持。加强中山大学珠海校区、北京理工大学（珠海）等本地高校在固态电池、动力电池等方向的学科建设，鼓励高职院校依据需求进行学科专业设置调整。支持完善技术型企业职称评审制度，鼓励符合条件的技术与研发人员申报"},{"no":"2.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"珠海国有资本等政府投资资金的杠杆和引导作用，充分发挥市新质生产力基金群的作用，为固态电池产业的升级壮大以及向高端价值链延伸等“新质化”提供更为充分的资源支持。聚集天使投资、创业投资等各类机构，为固态电池企业提供全链条金融服务。鼓励金融机构围绕固态电池产业链企业，开展配套中小企业供应链融资行动，支持企业以应收账款、仓单和存货质押等进行融资。（市工业和信息化局，"},{"no":"3.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"培育产业促进机构。成立固态电池产业发展联盟，聚焦关键技术、关键支撑、关键项目、关键资源，推动实现资源共享、优势互补、共促发展，促进上下游企业在珠海集聚发展。鼓励行业协会、研究机构、智库机构等发挥桥梁纽带作用，强化政产学研合作和上下游融通对接，开展标准制定、决策咨询、行业交流等多种形态活动，充分发挥行业组织公共服务和支撑作用，持续引导行业有序规范发展。（市工业"},{"no":"4.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"组织固态电池应用研讨会议。以企业家畅享会、供需对接会等形式，聚焦“应用场景拉动，电芯企业牵引，上下游聚集”，共建珠海固态电池生态，促进企业间交流合作。鼓励固态电池行业组织和各类创新主体，在珠海举办具有影响力且有较强行业示范带动性的应用研讨会、商机对接会、展览等活动。（市工业和信息化局、市商务局，科技集团）"},{"no":"（二）","category":"保障机制","target":"","support_type":"","amount":"","condition":"","excerpt":"平竞争、健康有序的市场发展环境。健全政银企合作机制，鼓励国有企业开展战略投资，为固态电池产业发展提供长期稳定资金。建立适应固态电池发展的统计机制，研究并完善固态电池相关产业分类标准，制订固态电池统计指标体系，健全相应的考核机制。"},{"no":"（三）","category":"保障机制","target":"","support_type":"","amount":"","condition":"","excerpt":"强化要素保障 统筹政府资源为固态电池产业建设提供金融服务、业务指导等服务支撑。积极推送固态电池产业项目、技术创新项目以及示范应用项目纳入省有关奖励、资助清单，支持固态电池项目优先列入市重大项目库。 附件： 1．珠海市人民政府办公室关于印发《珠海市推动固态电池产业发展行动方案（2025-2030年）》的通知（珠府办函〔2025〕99号） .wps"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON), CAST('[]' AS JSON),
       'clause-rule-v1', 'M_POLICY_TEXT_PARSE', 'ssb-rel', NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_text_parse WHERE policy_id = 'cn-zh-3840797'
);

-- cn-sd-10344208 条款 2 条
UPDATE demo_gkxlumenx_ads.policy_text_parse
SET title = '关于印发《山东省锂电池产业高质量发展行动方案》的通知',
    summary = '到2027年固态电池、钠电池等新产品研发与产业化取得突破；专栏要求开展固态电池固固界面与低成本规模化工艺攻关。',
    structured_elements = JSON_MERGE_PATCH(COALESCE(structured_elements, '{}'), CAST('{"clauses":[{"no":"一、","category":"补贴标准","target":"","support_type":"","amount":"1000亿元","condition":"","excerpt":"安全性能等加快提升。 到2027年，做优一批产业特色，锂电池产业链条进一步完善，固态电池、钠电池等新产品研发与产业化取得突破，锂电池回收利用体系基本完备，构建绿色、高效、智能的锂离子电池产业生态。"},{"no":"1.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"技术，支持开发“充电快、高比能、长寿命、高安全、宽温域、易回收”的先进产品，推动固态电池、钠电池等规模化生产。加强新型材料研发制造，提升先进系统集成、电池系统精细化管理水平。 专栏1 重点产品及核心技术 锂离子电池：强化电池结构设计、老化衰退机理、极端条件稳定性等关键技术研究，推出一批快充型锂电池、长寿命锂电池、全气候锂电池等产品。 钠离子电池：开展钠离子电"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON)),
    model_version = 'clause-rule-v1',
    metric_id = 'M_POLICY_TEXT_PARSE',
    update_time = NOW()
WHERE policy_id = 'cn-sd-10344208';
INSERT INTO demo_gkxlumenx_ads.policy_text_parse
  (policy_id, title, summary, structured_elements, auto_tags, model_version, metric_id, calc_batch_id, create_time, update_time)
SELECT 'cn-sd-10344208', '关于印发《山东省锂电池产业高质量发展行动方案》的通知', '到2027年固态电池、钠电池等新产品研发与产业化取得突破；专栏要求开展固态电池固固界面与低成本规模化工艺攻关。', CAST('{"clauses":[{"no":"一、","category":"补贴标准","target":"","support_type":"","amount":"1000亿元","condition":"","excerpt":"安全性能等加快提升。 到2027年，做优一批产业特色，锂电池产业链条进一步完善，固态电池、钠电池等新产品研发与产业化取得突破，锂电池回收利用体系基本完备，构建绿色、高效、智能的锂离子电池产业生态。"},{"no":"1.","category":"扶持措施","target":"","support_type":"","amount":"","condition":"","excerpt":"技术，支持开发“充电快、高比能、长寿命、高安全、宽温域、易回收”的先进产品，推动固态电池、钠电池等规模化生产。加强新型材料研发制造，提升先进系统集成、电池系统精细化管理水平。 专栏1 重点产品及核心技术 锂离子电池：强化电池结构设计、老化衰退机理、极端条件稳定性等关键技术研究，推出一批快充型锂电池、长寿命锂电池、全气候锂电池等产品。 钠离子电池：开展钠离子电"}],"clause_meta":{"source":"rule","model_version":"clause-rule-v1","llm_tried":false}}' AS JSON), CAST('[]' AS JSON),
       'clause-rule-v1', 'M_POLICY_TEXT_PARSE', 'ssb-rel', NOW(), NOW() FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM demo_gkxlumenx_ads.policy_text_parse WHERE policy_id = 'cn-sd-10344208'
);

-- gl-meti-20220831 无正文，不写条款

