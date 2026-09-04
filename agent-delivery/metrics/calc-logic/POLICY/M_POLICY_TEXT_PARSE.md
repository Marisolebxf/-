# 政策文本解析（M_POLICY_TEXT_PARSE）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-POLICY-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_TEXT_PARSE |
| 指标名称 | 政策文本解析 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 政策分析 |
| 三级模块 | - |
| 更新频率 | 日 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | QPOL-02 |

## 口径定义

对 DWD 未删除政策的正文/摘要做结构化要素抽取、自动摘要与标签，输出结构化要素、摘要与标签集合。统计窗口=最新 `calc_batch` 快照，对象=`dwd_policy_base.is_deleted=0` 且 `is_history=0`（当前版）的政策。

## 计算逻辑说明

采用「结构化要素抽取 + 自动摘要 + 自动标签」三支，输入为政策正文/摘要，抽取由 NLP 模型执行，结果落 `ads.policy_text_parse`。

### 第一步：入集

取最新 `calc_batch` 快照内未删除、当前版的 DWD 政策：

```sql
SELECT id, title, abstract, content, keywords, theme, keypoints, policy_support
FROM gkx.dwd_policy_base
WHERE is_deleted = 0 AND is_history = 0;
```

### 第二步：结构化要素抽取

对 `content` / `abstract` 抽取政策目标、扶持措施、责任主体、申报条件、支持力度、时间节点等要素。要素实体落 `policy_entity(policy_id, entity_type, entity_name, attributes, confidence)`，实体间关系落 `policy_entity_relation(policy_id, entity_id, relation_type, relation_weight)`。结构化结果字段以 `ads.policy_text_parse.structured_elements` 输出。

### 第三步：自动摘要

对 `content` 生成摘要，输出 `ads.policy_text_parse.summary`；`abstract` 可作为摘要种子。

### 第四步：自动标签

基于 `keywords`、`theme`、`keypoints` 及抽取要素生成自动标签，输出 `ads.policy_text_parse.auto_tags`。

```sql
-- 入集（最新 calc_batch 快照）
SELECT p.id, p.title, p.abstract, p.keywords, p.theme, p.keypoints
FROM gkx.dwd_policy_base p
WHERE p.is_deleted = 0 AND p.is_history = 0;

-- 抽取结果关联（要素/关系）
SELECT pe.policy_id, pe.entity_type, pe.entity_name, pe.confidence, pe.calc_batch_id
FROM gkx.policy_entity pe
WHERE pe.policy_id = :policy_id;
```

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 政策文本解析 | 结构化要素抽取 | 政策目标/扶持措施/责任主体/申报条件/支持力度/时间节点 | 从正文/摘要抽取结构化要素及实体。 | 实体抽取：NER/规则 → policy_entity；关系：→ policy_entity_relation | dwd_policy_base(id, title, abstract, content, keywords, theme, keypoints, policy_support) — 政策正文/摘要/关键点；policy_entity(policy_id, entity_type, entity_name, attributes, confidence, source_field, calc_batch_id) — 政策实体；policy_entity_relation(policy_id, entity_id, relation_type, relation_weight, relation_desc, confidence) — 实体关系 | 政策实体关系实际数据（现表 0 行） |
|  | 自动摘要 | 政策摘要 | 生成政策内容自动摘要。 | summary = LLM/抽取式摘要(content) | dwd_policy_base(id, title, content, abstract) — 政策正文/摘要 | 摘要模型产出字段（输出表 summary） |
|  | 自动标签 | 政策标签 | 基于关键词/主题/关键点生成自动标签。 | auto_tags = keywords ∪ theme ∪ 抽取要素标签 | dwd_policy_base(id, keywords, theme, keypoints, type) — 关键词/主题/关键点/类型 | 标签模型产出字段（输出表 auto_tags） |

## 源表字段

- dwd_policy_base(id, title, abstract, content, keywords, theme, keypoints, policy_support, type, province, city, rank, is_deleted, is_history) — 政策正文/摘要/关键词/主题/关键点（有数据）
- policy_entity(policy_id, entity_type, entity_name, attributes, source_field, confidence, model_version, calc_batch_id) — 政策实体（结构化要素，有数据）
- policy_entity_relation(policy_id, entity_id, relation_type, relation_weight, relation_desc, extract_rule, confidence) — 政策实体关系（表结构存在，0 行）
- policy_entity_type(type_code, type_name, type_desc, parent_id) — 政策实体类型字典（表结构存在，0 行）
- policy_base_info(policy_id, title, abstract, keywords, content, elements, keypoints, factors, sci_tech_attribute, application_conditions, execution_cycle, execution_entity, related_entities, is_deleted) — DWD 政策解析层（结构化要素目标字段）

## 待建字段

- `policy_entity_relation`、`policy_entity_type` 实际数据（现均 0 行，仅表结构）。
- `ads.policy_text_parse` 的 `summary`、`structured_elements`、`auto_tags` 为模型产出输出字段（输出表，非源表）。

## 参考资料

[1] 智能政策拆解.md｜序号 606—609（政策语义理解：深度语义解析、意图识别与条款分类；条款精细化拆解：拆分章节/条目/细则，提取政策目标、扶持措施、保障机制、责任主体；关键指标自动提取：抽取量化指标、补贴标准、资质要求、时间节点；政策实体关联：关联发布主体、适用领域、关联政策、服务对象）。

[2] 政策效果推演.md｜序号 237 政策文本智能解析（利用 NLP 和深度学习提取政策关键词、核心内容、支持对象、申报条件、支持力度）。

[3] 政策实体识别构建｜科技专题服务算法库.md｜1.1.1.1.1.1.1.2.5（规则识别、词典识别、实体维护更新与属性提取）。

[4] 政策实体关系抽取｜科技专题服务算法库.md｜1.1.1.1.1.1.1.2.6（抽取政策与政策主题、政策目标、实施主体、受益对象、监管机构等关系）。
