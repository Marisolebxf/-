# ALGO-LIB-METRIC-DEPS-L01 三方 ODS 缺口清单

- 截止日：2026-08-25
- 已确认不满足：40 条
- 待核验：334 条
- 全量五档：full=1，partial=3，none=37，pending_ods=334，n/a=94

## 已确认不满足（none / partial）

| gap_id | metric_id | 指标 | 输入 | 状态 | 缺什么 | 影响 |
|---|---|---|---|---|---|---|
| ODS-GAP-001 | M_ENT_KEY_TOTAL | 重点企业总数 | 专利数据 | partial | 三方专利原始表空表 | 双阈值中的专利阈值暂不可用 |
| ODS-GAP-002 | M_ENT_TYPE_COUNT | 企业类型分布 | 企业类型标签 | partial | 企业类型标签源不完全 | 类型分布不能完全真实计算 |
| ODS-GAP-003 | M_ENT_DOMAIN_COVERAGE_COUNT | 企业领域分布 | 产业领域标签 | partial | 领域分类体系待确认 | 领域分布统计口径存疑 |
| ODS-GAP-004 | TEMP_ALGO_ALGO-ENT-BASE-97_4 | 重点资讯统计 | 资讯数据 | none | 缺资讯/新闻原始表 | 重点资讯统计无法真实计算 |
| ODS-GAP-005 | TEMP_ALGO_ALGO-ENT-DEEP-142_1 | 企业发展历程模型 | 新闻与行业资讯数据 | none | 缺“新闻与行业资讯数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-ENT-DEEP-142_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-006 | M_ENT_PAINPOINT_COUNT | 企业发展痛难点识别模型 | 招聘信息 | none | 缺“招聘信息”的稳定 ODS 表与字段 | M_ENT_PAINPOINT_COUNT 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-007 | M_ENT_BUSINESS_POWER_SCORE | 企业商业力评估模型 | 行业研究数据 | none | 缺“行业研究数据”的稳定 ODS 表与字段 | M_ENT_BUSINESS_POWER_SCORE 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-008 | M_ENT_BUSINESS_POWER_SCORE | 企业商业力评估模型 | 市场调研数据 | none | 缺“市场调研数据”的稳定 ODS 表与字段 | M_ENT_BUSINESS_POWER_SCORE 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-009 | M_ENT_BUSINESS_POWER_SCORE | 企业商业力评估模型 | 品牌影响力数据 | none | 缺“品牌影响力数据”的稳定 ODS 表与字段 | M_ENT_BUSINESS_POWER_SCORE 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-010 | M_ENT_CULTIVATION_INDEX | 培育企业综合推荐模型 | 市场调研数据 | none | 缺“市场调研数据”的稳定 ODS 表与字段 | M_ENT_CULTIVATION_INDEX 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-011 | TEMP_ALGO_ALGO-CHAIN-DEEP-119_1 | 产业发展路线历程模型 | 专家观点数据 | none | 缺“专家观点数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-CHAIN-DEEP-119_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-012 | TEMP_ALGO_ALGO-CHAIN-DEEP-119_1 | 产业发展路线历程模型 | 新闻报道数据 | none | 缺“新闻报道数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-CHAIN-DEEP-119_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-013 | TEMP_ALGO_ALGO-CHAIN-DEEP-120_1 | 产业热点领域识别模型 | 新闻报道数据 | none | 缺“新闻报道数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-CHAIN-DEEP-120_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-014 | TEMP_ALGO_ALGO-CHAIN-DEEP-120_1 | 产业热点领域识别模型 | 行业研究报告数据 | none | 缺“行业研究报告数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-CHAIN-DEEP-120_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-015 | TEMP_ALGO_ALGO-CHAIN-DEEP-125_1 | 产业瓶颈堵点识别模型 | 市场调研数据 | none | 缺“市场调研数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-CHAIN-DEEP-125_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-016 | TEMP_ALGO_ALGO-CHAIN-DEEP-125_1 | 产业瓶颈堵点识别模型 | 专家访谈信息 | none | 缺“专家访谈信息”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-CHAIN-DEEP-125_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-017 | TEMP_ALGO_ALGO-CHAIN-DEEP-127_1 | 深圳问题识别模型 | 新闻舆情数据 | none | 缺“新闻舆情数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-CHAIN-DEEP-127_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-018 | TEMP_ALGO_ALGO-SVC-DEEP-176_1 | 人力资源服务机构技术力评价模型 | 客户反馈数据。 | none | 缺“客户反馈数据。”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-SVC-DEEP-176_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-019 | TEMP_ALGO_ALGO-TECH-DEEP-132_1 | 技术发展历程模型 | 技术新闻数据 | none | 缺“技术新闻数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TECH-DEEP-132_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-020 | TEMP_ALGO_ALGO-TECH-DEEP-132_1 | 技术发展历程模型 | 媒体报道量 | none | 缺“媒体报道量”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TECH-DEEP-132_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-021 | TEMP_ALGO_ALGO-TECH-DEEP-134_1 | 技术前沿热点领域识别模型 | 新闻与技术博客信息 | none | 缺“新闻与技术博客信息”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TECH-DEEP-134_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-022 | TEMP_ALGO_ALGO-TECH-DEEP-135_1 | 技术产业化潜力识别模型 | 市场调研数据 | none | 缺“市场调研数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TECH-DEEP-135_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-023 | TEMP_ALGO_ALGO-TECH-DEEP-137_1 | 技术阶段分析模型 | 市场调研数据 | none | 缺“市场调研数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TECH-DEEP-137_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-024 | TEMP_ALGO_ALGO-TECH-DEEP-138_1 | 深圳技术发展问题识别模型 | 新闻动态数据 | none | 缺“新闻动态数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TECH-DEEP-138_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-025 | TEMP_ALGO_ALGO-TALENT-DEEP-157_1 | 人才流动追踪模型 | 社交网络数据 | none | 缺“社交网络数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-157_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-026 | TEMP_ALGO_ALGO-TALENT-DEEP-157_1 | 人才流动追踪模型 | 招聘网站数据 | none | 缺“招聘网站数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-157_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-027 | TEMP_ALGO_ALGO-TALENT-DEEP-157_1 | 人才流动追踪模型 | 简历数据库数据 | none | 缺“简历数据库数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-157_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-028 | TEMP_ALGO_ALGO-TALENT-DEEP-157_1 | 人才流动追踪模型 | 招聘信息特征 | none | 缺“招聘信息特征”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-157_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-029 | TEMP_ALGO_ALGO-TALENT-DEEP-159_1 | 深圳重点人才优势和短板分析模型 | 招聘网站信息 | none | 缺“招聘网站信息”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-159_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-030 | TEMP_ALGO_ALGO-TALENT-DEEP-159_1 | 深圳重点人才优势和短板分析模型 | 社交网络数据 | none | 缺“社交网络数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-159_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-031 | TEMP_ALGO_ALGO-TALENT-DEEP-160_1 | 人才关系链模型 | 招聘平台信息 | none | 缺“招聘平台信息”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-160_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-032 | TEMP_ALGO_ALGO-TALENT-DEEP-160_1 | 人才关系链模型 | 社交媒体数据 | none | 缺“社交媒体数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-160_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-033 | TEMP_ALGO_ALGO-TALENT-DEEP-160_1 | 人才关系链模型 | 研究报告数据 | none | 缺“研究报告数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-160_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-034 | TEMP_ALGO_ALGO-TALENT-DEEP-161_1 | 人才供需分析评价模型 | 招聘数据 | none | 缺“招聘数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-161_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-035 | TEMP_ALGO_ALGO-TALENT-DEEP-162_1 | 人才学术力评估模型 | 人才招聘平台信息 | none | 缺“人才招聘平台信息”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-162_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-036 | TEMP_ALGO_ALGO-TALENT-DEEP-163_1 | 人才产业力评估模型 | 招聘网站数据 | none | 缺“招聘网站数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-163_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-037 | TEMP_ALGO_ALGO-TALENT-DEEP-163_1 | 人才产业力评估模型 | 社交媒体数据 | none | 缺“社交媒体数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-163_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-038 | TEMP_ALGO_ALGO-TALENT-DEEP-164_1 | 招入人才推荐模型 | 社交网络信息 | none | 缺“社交网络信息”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-164_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-039 | TEMP_ALGO_ALGO-TALENT-DEEP-164_1 | 招入人才推荐模型 | 招聘系统数据 | none | 缺“招聘系统数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-164_1 的相关子项无法用当前 gkx ODS 完整计算 |
| ODS-GAP-040 | TEMP_ALGO_ALGO-TALENT-DEEP-165_1 | 培育人才布局模型 | 人才招聘平台数据 | none | 缺“人才招聘平台数据”的稳定 ODS 表与字段 | TEMP_ALGO_ALGO-TALENT-DEEP-165_1 的相关子项无法用当前 gkx ODS 完整计算 |

## 待核验（pending_ods）

未核验 ≠ 已确认缺口。以下条目在 ODS 核验后升格或关闭，不在本次假装满足。

| metric_id | 指标 | 输入 | source_system | evidence |
|---|---|---|---|---|
| M_ENT_KEY_TOTAL | 重点企业总数 | 技术交易额 | 三方科技要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ENT-GRAPH-108_1 | 企业实体识别构建 | 企业实体识别构建所需原始输入 | 三方企业要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ENT-GRAPH-109_1 | 企业实体关系抽取 | 企业实体关系抽取所需原始输入 | 三方企业要素库 | 未核三方入站 |
| M_ENT_COMPETITIVENESS_SCORE | 深圳企业竞争力水平分析模型 | 财务报表数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_COMPETITIVENESS_SCORE | 深圳企业竞争力水平分析模型 | 税务数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_COMPETITIVENESS_SCORE | 深圳企业竞争力水平分析模型 | 人力资源信息 | 三方企业要素库 | 未核三方入站 |
| M_ENT_COMPETITIVENESS_SCORE | 深圳企业竞争力水平分析模型 | 市场表现数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_COMPETITIVENESS_SCORE | 深圳企业竞争力水平分析模型 | 企业调查数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_COMPETITIVENESS_SCORE | 深圳企业竞争力水平分析模型 | 企业规模与分类信息 | 三方企业要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ENT-DEEP-142_1 | 企业发展历程模型 | 企业财务报表数据 | 三方企业要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ENT-DEEP-142_1 | 企业发展历程模型 | 经营数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_PAINPOINT_COUNT | 企业发展痛难点识别模型 | 企业年报数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_PAINPOINT_COUNT | 企业发展痛难点识别模型 | 财务报表数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_PAINPOINT_COUNT | 企业发展痛难点识别模型 | 社保缴纳记录 | 三方企业要素库 | 未核三方入站 |
| M_ENT_SUPPLY_CHAIN_RISK | 企业供应链关系分析模型 | 产业全要素图谱数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_SUPPLY_CHAIN_RISK | 企业供应链关系分析模型 | 企业关系数据库信息 | 三方企业要素库 | 未核三方入站 |
| M_ENT_SUPPLY_CHAIN_RISK | 企业供应链关系分析模型 | 企业专题数据集 | 三方企业要素库 | 未核三方入站 |
| M_ENT_SUPPLY_CHAIN_RISK | 企业供应链关系分析模型 | 供应链核心信息 | 三方企业要素库 | 未核三方入站 |
| M_ENT_TECH_POWER_SCORE | 企业技术力评估模型 | 企业专利数据库数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_TECH_POWER_SCORE | 企业技术力评估模型 | 科技项目库数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_TECH_POWER_SCORE | 企业技术力评估模型 | 研发投入数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_TECH_POWER_SCORE | 企业技术力评估模型 | 企业人才结构档案 | 三方企业要素库 | 未核三方入站 |
| M_ENT_TECH_POWER_SCORE | 企业技术力评估模型 | 技术合作关系数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_BUSINESS_POWER_SCORE | 企业商业力评估模型 | 企业财务数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_BUSINESS_POWER_SCORE | 企业商业力评估模型 | 技术合作及产业链布局信息 | 三方企业要素库 | 未核三方入站 |
| M_ENT_ATTRACTION_INDEX | 招引企业综合推荐模型 | 企业信用信息数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_ATTRACTION_INDEX | 招引企业综合推荐模型 | 行业协会数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_ATTRACTION_INDEX | 招引企业综合推荐模型 | 专利与知识产权数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_ATTRACTION_INDEX | 招引企业综合推荐模型 | 财务数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_ATTRACTION_INDEX | 招引企业综合推荐模型 | 业务领域信息 | 三方企业要素库 | 未核三方入站 |
| M_ENT_CULTIVATION_INDEX | 培育企业综合推荐模型 | 企业基本信息数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_CULTIVATION_INDEX | 培育企业综合推荐模型 | 政策数据 | 三方企业要素库 | 未核三方入站 |
| M_ENT_CULTIVATION_INDEX | 培育企业综合推荐模型 | 行业动态数据 | 三方企业要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-GRAPH-106_1 | 政策实体识别构建 | 政策实体识别构建所需原始输入 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-GRAPH-107_1 | 政策实体关系抽取 | 政策实体关系抽取所需原始输入 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-166_1 | 政策焦点识别模型 | 政策文本信息 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-166_1 | 政策焦点识别模型 | 政策执行数据 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-166_1 | 政策焦点识别模型 | 辅助数据。 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-167_1 | 政策力度评估模型 | 政策文本信息 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-167_1 | 政策力度评估模型 | 政策执行数据 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-167_1 | 政策力度评估模型 | 成本与资源数据 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-167_1 | 政策力度评估模型 | 辅助数据。 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-168_1 | 政策效果评估模型 | 政策原文及相关实施文件 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-168_1 | 政策效果评估模型 | 政策执行过程数据 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-168_1 | 政策效果评估模型 | 宏观经济数据 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-168_1 | 政策效果评估模型 | 环境影响数据。 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-169_1 | 政策短板识别模型 | 政策文本 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-169_1 | 政策短板识别模型 | 执行数据 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-169_1 | 政策短板识别模型 | 辅助分析数据。 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-170_1 | 政策机遇识别模型 | 政策文本信息 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-170_1 | 政策机遇识别模型 | 政策解读与行业分析数据 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-171_1 | 政策布局推荐模型 | 政策机遇识别结果 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-171_1 | 政策布局推荐模型 | 政策短板识别结果 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-POLICY-DEEP-171_1 | 政策布局推荐模型 | 政策数据库数据。 | 三方政策库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-GRAPH-102_1 | 产业实体识别构建 | 产业实体识别构建所需原始输入 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-GRAPH-103_1 | 产业实体关系抽取 | 产业实体关系抽取所需原始输入 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-117_1 | 产业链全景模型构建 | 产业知识图谱数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-117_1 | 产业链全景模型构建 | 企业信息 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-117_1 | 产业链全景模型构建 | 技术数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-117_1 | 产业链全景模型构建 | 人才数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-117_1 | 产业链全景模型构建 | 科研机构数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-117_1 | 产业链全景模型构建 | 服务机构数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-117_1 | 产业链全景模型构建 | 供应链数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-117_1 | 产业链全景模型构建 | 市场数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-117_1 | 产业链全景模型构建 | 行业数据。 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-118_1 | 深圳产业链模型构建 | 产业知识图谱数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-118_1 | 深圳产业链模型构建 | 深圳区域产业基础数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-118_1 | 深圳产业链模型构建 | 企业信息 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-118_1 | 深圳产业链模型构建 | 技术数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-118_1 | 深圳产业链模型构建 | 人才数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-118_1 | 深圳产业链模型构建 | 科研机构信息 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-118_1 | 深圳产业链模型构建 | 服务机构信息 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-118_1 | 深圳产业链模型构建 | 供应链数据。 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-119_1 | 产业发展路线历程模型 | 行业统计信息 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-119_1 | 产业发展路线历程模型 | 政策法规文本 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-120_1 | 产业热点领域识别模型 | 公司公告数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-121_1 | 深圳产业优势识别模型 | 深圳市产业数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-121_1 | 深圳产业优势识别模型 | 全国产业数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-121_1 | 深圳产业优势识别模型 | 政策法规库数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-121_1 | 深圳产业优势识别模型 | 企业信息库数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-122_1 | 产业周期分析模型 | 历史产业数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-122_1 | 产业周期分析模型 | 实时产业数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-122_1 | 产业周期分析模型 | 市场规模数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-122_1 | 产业周期分析模型 | 行业增长率数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-122_1 | 产业周期分析模型 | 利润率数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-123_1 | 产业阶段分析模型 | 生产能力数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-123_1 | 产业阶段分析模型 | 销售规模数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-123_1 | 产业阶段分析模型 | 市场份额数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-123_1 | 产业阶段分析模型 | 利润率数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-123_1 | 产业阶段分析模型 | 政策法规数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-123_1 | 产业阶段分析模型 | 行业统计信息 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-123_1 | 产业阶段分析模型 | 企业财报数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-124_1 | 产业链关键环节识别模型 | 企业财务报表数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-124_1 | 产业链关键环节识别模型 | 产业统计年鉴数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-124_1 | 产业链关键环节识别模型 | 政策法规数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-125_1 | 产业瓶颈堵点识别模型 | 政策法规数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-125_1 | 产业瓶颈堵点识别模型 | 行业分析数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-126_1 | 区域产业指数模型 | 企业信息库数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-126_1 | 区域产业指数模型 | 知识产权数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-126_1 | 区域产业指数模型 | 高校与科研机构统计数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-126_1 | 区域产业指数模型 | 人才数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-126_1 | 区域产业指数模型 | 配套服务数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-126_1 | 区域产业指数模型 | 历史产业数据。 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-127_1 | 深圳问题识别模型 | 深圳产业数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-127_1 | 深圳问题识别模型 | 全国产业数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-127_1 | 深圳问题识别模型 | 政策法规数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-127_1 | 深圳问题识别模型 | 企业财务数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-128_1 | 深圳机遇分析模型 | 年度经济统计数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-128_1 | 深圳机遇分析模型 | 人口普查数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-128_1 | 深圳机遇分析模型 | 重点产业分布数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-128_1 | 深圳机遇分析模型 | 产业优势分析结果 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-128_1 | 深圳机遇分析模型 | 发展问题识别结果 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-129_1 | 重点布局产业推荐模型 | 深圳市产业基础信息数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-129_1 | 重点布局产业推荐模型 | 市场规模数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-129_1 | 重点布局产业推荐模型 | 发展趋势数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-129_1 | 重点布局产业推荐模型 | 政策环境数据 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-129_1 | 重点布局产业推荐模型 | 产业优势分析结果 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-CHAIN-DEEP-129_1 | 重点布局产业推荐模型 | 产业问题识别结果 | 三方产业库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-GRAPH-112_1 | 服务机构实体识别构建 | 服务机构实体识别构建所需原始输入 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-GRAPH-113_1 | 服务机构实体关系抽取 | 服务机构实体关系抽取所需原始输入 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-172_1 | 服务链短板分析模型 | 服务机构基础信息 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-172_1 | 服务链短板分析模型 | 服务质量数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-172_1 | 服务链短板分析模型 | 经营效益数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-172_1 | 服务链短板分析模型 | 服务类型数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-173_1 | 服务关系链模型 | 服务机构专题数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-173_1 | 服务关系链模型 | 关系数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-173_1 | 服务关系链模型 | 辅助信息。 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-174_1 | 金融服务机构技术力评价模型 | 财务数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-174_1 | 金融服务机构技术力评价模型 | 融资数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-174_1 | 金融服务机构技术力评价模型 | 风险数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-174_1 | 金融服务机构技术力评价模型 | 服务数据。 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-175_1 | 知识产权服务机构技术力评价模型 | 专业能力数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-175_1 | 知识产权服务机构技术力评价模型 | 业务范围数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-175_1 | 知识产权服务机构技术力评价模型 | 成功案例数。 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-176_1 | 人力资源服务机构技术力评价模型 | 人才资源相关数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-177_1 | 市场营销服务机构技术力评价模型 | 调研能力相关数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-177_1 | 市场营销服务机构技术力评价模型 | 策划能力相关数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-177_1 | 市场营销服务机构技术力评价模型 | 成功项目案例数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-177_1 | 市场营销服务机构技术力评价模型 | 行业基准与历史数据。 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-178_1 | 咨询服务机构技术力评价模型 | 机构基本信息 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-178_1 | 咨询服务机构技术力评价模型 | 人才密度数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-178_1 | 咨询服务机构技术力评价模型 | 行业经验数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-178_1 | 咨询服务机构技术力评价模型 | 成功案例数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-178_1 | 咨询服务机构技术力评价模型 | 行业声誉数据。 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-179_1 | 科技创新服务机构技术力评价模型 | 合作科研机构数量 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-179_1 | 科技创新服务机构技术力评价模型 | 合作企业数量 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-179_1 | 科技创新服务机构技术力评价模型 | 科技创新成果数量 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-179_1 | 科技创新服务机构技术力评价模型 | 技术转化成果数量 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-179_1 | 科技创新服务机构技术力评价模型 | 历史数据及行业平均水平。 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-180_1 | 服务机构引入推荐模型 | 服务机构基本信息 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-180_1 | 服务机构引入推荐模型 | 财务与市场数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-180_1 | 服务机构引入推荐模型 | 产业相关度数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-180_1 | 服务机构引入推荐模型 | 深圳连接度数据。 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-181_1 | 服务机构培育推荐模型 | 基础信息数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-181_1 | 服务机构培育推荐模型 | 行业与政策数据 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SVC-DEEP-181_1 | 服务机构培育推荐模型 | 潜力数据。 | 三方服务机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-182_1 | 区域科技创新成果综合评价模型 | 区域基础科学成果数据（论文 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-182_1 | 区域科技创新成果综合评价模型 | 学术奖项 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-182_1 | 区域科技创新成果综合评价模型 | 重大科学突破） | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-182_1 | 区域科技创新成果综合评价模型 | 区域应用科技成果数据（高价值专利 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-182_1 | 区域科技创新成果综合评价模型 | 新技术应用 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-182_1 | 区域科技创新成果综合评价模型 | 产业化案例） | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-182_1 | 区域科技创新成果综合评价模型 | 其他参考数据。 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-183_1 | 区域产业创新成果综合评价模型 | 产品服务创新数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-183_1 | 区域产业创新成果综合评价模型 | 企业创新数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-183_1 | 区域产业创新成果综合评价模型 | 服务机构创新数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-183_1 | 区域产业创新成果综合评价模型 | 其他辅助数据。 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-184_1 | 区域产业创新人才综合评价模型 | 人才专题库数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-184_1 | 区域产业创新人才综合评价模型 | 科技成果库数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-185_1 | 区域产业创新政策综合评价模型 | 政策基础数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-185_1 | 区域产业创新政策综合评价模型 | 执行成效数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-185_1 | 区域产业创新政策综合评价模型 | 历史基准数据。 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-186_1 | 区域创新活力综合分析模型 | 区域创新科技数据（专利数量与质量 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-186_1 | 区域创新活力综合分析模型 | 技术成果转化率） | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-186_1 | 区域创新活力综合分析模型 | 区域创新产业数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-186_1 | 区域创新活力综合分析模型 | 区域创新人才数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-186_1 | 区域创新活力综合分析模型 | 区域创新政策数据。 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-187_1 | 区域创新要素类型综合评价模型 | 创新人才数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-187_1 | 区域创新要素类型综合评价模型 | 企业数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-187_1 | 区域创新要素类型综合评价模型 | 政策数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-187_1 | 区域创新要素类型综合评价模型 | 服务机构数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-187_1 | 区域创新要素类型综合评价模型 | 科研机构数据。 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-188_1 | 区域创新要素层次综合评价模型 | 创新人才结构数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-188_1 | 区域创新要素层次综合评价模型 | 企业结构数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-188_1 | 区域创新要素层次综合评价模型 | 政策结构数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-188_1 | 区域创新要素层次综合评价模型 | 服务机构结构数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-188_1 | 区域创新要素层次综合评价模型 | 科研机构结构数据。 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-189_1 | 区域创新要素领域综合评价模型 | 区域产业知识图谱 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-189_1 | 区域创新要素领域综合评价模型 | 技术领域数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-189_1 | 区域创新要素领域综合评价模型 | 区域创新要素数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-190_1 | 区域创新要素综合分析模型 | 区域基础数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-190_1 | 区域创新要素综合分析模型 | 科技创新相关数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-190_1 | 区域创新要素综合分析模型 | 行业和领域统计数据。 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-191_1 | 区域创新协同分析模型 | 创新主体基础数据 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-SYNTH-191_1 | 区域创新协同分析模型 | 合作关系数据。 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-SYNTH-GRAPHAPI-116_1 | 产业全要素图谱API服务开发 | 产业全要素图谱API服务开发所需原始输入 | 三方区域创新数据 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-GRAPH-104_1 | 技术实体识别构建 | 技术实体识别构建所需原始输入 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-GRAPH-105_1 | 技术实体关系抽取 | 技术实体关系抽取所需原始输入 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-130_1 | 全景技术链模型 | 技术分类体系数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-130_1 | 全景技术链模型 | 技术知识图谱 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-130_1 | 全景技术链模型 | 专利数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-130_1 | 全景技术链模型 | 论文数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-130_1 | 全景技术链模型 | 产品信息 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-130_1 | 全景技术链模型 | 企业信息。 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-131_1 | 深圳技术链模型 | 深圳市技术产业分类信息 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-131_1 | 深圳技术链模型 | 技术知识图谱 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-131_1 | 深圳技术链模型 | 行业分类数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-131_1 | 深圳技术链模型 | 企业信息 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-131_1 | 深圳技术链模型 | 产业规模数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-131_1 | 深圳技术链模型 | 应用领域数据。 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-132_1 | 技术发展历程模型 | 专利数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-132_1 | 技术发展历程模型 | 科研论文数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-132_1 | 技术发展历程模型 | 行业资讯数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-132_1 | 技术发展历程模型 | 政策文件发布频率。 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-133_1 | 深圳细分领域分布模型 | 专利数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-133_1 | 深圳细分领域分布模型 | 学术文献数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-133_1 | 深圳细分领域分布模型 | 企业信息 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-133_1 | 深圳细分领域分布模型 | 行业统计数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-133_1 | 深圳细分领域分布模型 | 政策开放数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-133_1 | 深圳细分领域分布模型 | 技术关键词及分类信息 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-133_1 | 深圳细分领域分布模型 | 深圳产业布局与分类数据。 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-134_1 | 技术前沿热点领域识别模型 | 学术论文数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-134_1 | 技术前沿热点领域识别模型 | 专利数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-134_1 | 技术前沿热点领域识别模型 | 行业资讯数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-134_1 | 技术前沿热点领域识别模型 | 技术领域分类信息 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-134_1 | 技术前沿热点领域识别模型 | 专家活动数据。 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-135_1 | 技术产业化潜力识别模型 | 专利数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-135_1 | 技术产业化潜力识别模型 | 学术论文数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-135_1 | 技术产业化潜力识别模型 | 科技期刊信息 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-135_1 | 技术产业化潜力识别模型 | 技术转化案例数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-135_1 | 技术产业化潜力识别模型 | 市场需求数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-136_1 | 技术转化瓶颈堵点原因识别模型 | 专利数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-136_1 | 技术转化瓶颈堵点原因识别模型 | 学术论文数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-136_1 | 技术转化瓶颈堵点原因识别模型 | 成果转化平台数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-136_1 | 技术转化瓶颈堵点原因识别模型 | 技术发展趋势信息 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-136_1 | 技术转化瓶颈堵点原因识别模型 | 成果产出数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-136_1 | 技术转化瓶颈堵点原因识别模型 | 转化效率数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-137_1 | 技术阶段分析模型 | 技术研发报告数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-137_1 | 技术阶段分析模型 | 专利文献数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-137_1 | 技术阶段分析模型 | 领域专题库信息 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-137_1 | 技术阶段分析模型 | 技术成熟度指数 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-137_1 | 技术阶段分析模型 | 技术创新度指数 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-138_1 | 深圳技术发展问题识别模型 | 深圳技术数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-138_1 | 深圳技术发展问题识别模型 | 全国技术数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-138_1 | 深圳技术发展问题识别模型 | 专利信息 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-138_1 | 深圳技术发展问题识别模型 | 技术报告 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-138_1 | 深圳技术发展问题识别模型 | 学术论文数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-139_1 | 深圳技术发展机遇识别模型 | 深圳技术专题库数据（专利申请量 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-139_1 | 深圳技术发展机遇识别模型 | 成果转化率 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-139_1 | 深圳技术发展机遇识别模型 | 创新人才数量） | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-139_1 | 深圳技术发展机遇识别模型 | 全国技术数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-139_1 | 深圳技术发展机遇识别模型 | 企业创新信息 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-139_1 | 深圳技术发展机遇识别模型 | 成果转化案例数据。 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-140_1 | 深圳技术发展重点布局领域推荐模型 | 技术专利数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-140_1 | 深圳技术发展重点布局领域推荐模型 | 科技项目成果数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-140_1 | 深圳技术发展重点布局领域推荐模型 | 技术文献数据 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-140_1 | 深圳技术发展重点布局领域推荐模型 | 深圳技术优势分析结果 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TECH-DEEP-140_1 | 深圳技术发展重点布局领域推荐模型 | 技术协同关系数据。 | 三方技术要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-GRAPH-114_1 | 科研机构实体识别构建 | 科研机构实体识别构建所需原始输入 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-GRAPH-115_1 | 科研机构实体关系抽取 | 科研机构实体关系抽取所需原始输入 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-149_1 | 科研机构重点技术领域布局模型 | 学术论文数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-149_1 | 科研机构重点技术领域布局模型 | 专利数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-149_1 | 科研机构重点技术领域布局模型 | 科研项目数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-149_1 | 科研机构重点技术领域布局模型 | 人才信息数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-149_1 | 科研机构重点技术领域布局模型 | 技术知识图谱结构 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-150_1 | 科研机构发展历程模型 | 科研机构基本信息 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-150_1 | 科研机构发展历程模型 | 科研成果数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-150_1 | 科研机构发展历程模型 | 科研项目数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-150_1 | 科研机构发展历程模型 | 专利数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-150_1 | 科研机构发展历程模型 | 论文数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-150_1 | 科研机构发展历程模型 | 学术会议记录 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-151_1 | 深圳科研机构优势分析模型 | 政府科技管理公开数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-151_1 | 深圳科研机构优势分析模型 | 专业科技数据库信息 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-151_1 | 深圳科研机构优势分析模型 | 科研机构官网数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-151_1 | 深圳科研机构优势分析模型 | 科研成果信息 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-151_1 | 深圳科研机构优势分析模型 | 科研经费投入数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-152_1 | 深圳科研机构痛难点识别模型 | 深圳科研项目数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-152_1 | 深圳科研机构痛难点识别模型 | 科研成果数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-152_1 | 深圳科研机构痛难点识别模型 | 人才队伍数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-152_1 | 深圳科研机构痛难点识别模型 | 企业合作数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-152_1 | 深圳科研机构痛难点识别模型 | 全国科研机构对比数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-153_1 | 科研合作关系链条模型 | 专利数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-153_1 | 科研合作关系链条模型 | 科研项目数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-153_1 | 科研合作关系链条模型 | 学术成果数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-153_1 | 科研合作关系链条模型 | 产业全要素图谱数据。 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-154_1 | 科研机构引入推荐模型 | 学术论文数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-154_1 | 科研机构引入推荐模型 | 专利数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-154_1 | 科研机构引入推荐模型 | 科技项目数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-154_1 | 科研机构引入推荐模型 | 科研人员信息 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-154_1 | 科研机构引入推荐模型 | 机构基本信息 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-154_1 | 科研机构引入推荐模型 | 研究方向数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-154_1 | 科研机构引入推荐模型 | 成果产出分析结果 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-155_1 | 科研机构扶持推荐模型 | 科研机构基础信息 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-155_1 | 科研机构扶持推荐模型 | 科研成果数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-155_1 | 科研机构扶持推荐模型 | 科研经费数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-ORG-DEEP-155_1 | 科研机构扶持推荐模型 | 人才队伍结构数据 | 三方科研机构库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-GRAPH-110_1 | 人才实体识别构建 | 人才实体识别构建所需原始输入 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-GRAPH-111_1 | 人才实体关系抽取 | 人才实体关系抽取所需原始输入 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-156_1 | 重点人才识别模型 | 企业人才库数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-156_1 | 重点人才识别模型 | 科技人才数据库信息 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-156_1 | 重点人才识别模型 | 学术论文数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-156_1 | 重点人才识别模型 | 个人背景信息 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-156_1 | 重点人才识别模型 | 专业领域信息 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-156_1 | 重点人才识别模型 | 科研成果数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-157_1 | 人才流动追踪模型 | 人才关联关系链信息 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-157_1 | 人才流动追踪模型 | 职业轨迹数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-157_1 | 人才流动追踪模型 | 行业与企业标签信息。 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-158_1 | 高校学院新培育人才模型 | 高校数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-158_1 | 高校学院新培育人才模型 | 科研机构数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-158_1 | 高校学院新培育人才模型 | 技术关系图谱数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-158_1 | 高校学院新培育人才模型 | 专题数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-159_1 | 深圳重点人才优势和短板分析模型 | 深圳人才数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-159_1 | 深圳重点人才优势和短板分析模型 | 全国人才数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-159_1 | 深圳重点人才优势和短板分析模型 | 政府人才数据库信息 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-160_1 | 人才关系链模型 | 人才专题数据库数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-160_1 | 人才关系链模型 | 产业全要素图谱数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-160_1 | 人才关系链模型 | 企业人才库信息 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-161_1 | 人才供需分析评价模型 | 人才专题库数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-161_1 | 人才供需分析评价模型 | 产业专题库数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-161_1 | 人才供需分析评价模型 | 人才流动数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-162_1 | 人才学术力评估模型 | 学术论文数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-162_1 | 人才学术力评估模型 | 专利数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-162_1 | 人才学术力评估模型 | 人才成果记录 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-162_1 | 人才学术力评估模型 | 职业技能数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-163_1 | 人才产业力评估模型 | 人才库数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-163_1 | 人才产业力评估模型 | 行业数据库信息 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-164_1 | 招入人才推荐模型 | 专利数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-164_1 | 招入人才推荐模型 | 学术论文数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-165_1 | 培育人才布局模型 | 培训机构数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-165_1 | 培育人才布局模型 | 科研院所数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-165_1 | 培育人才布局模型 | 学术论文数据 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-165_1 | 培育人才布局模型 | 职业背景信息 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-165_1 | 培育人才布局模型 | 学术成果记录 | 三方人才要素库 | 未核三方入站 |
| TEMP_ALGO_ALGO-TALENT-DEEP-165_1 | 培育人才布局模型 | 产业实践案例数据 | 三方人才要素库 | 未核三方入站 |
