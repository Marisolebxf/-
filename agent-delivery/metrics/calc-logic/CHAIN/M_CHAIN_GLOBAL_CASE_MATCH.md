# 全球成功案例匹配（M_CHAIN_GLOBAL_CASE_MATCH）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_GLOBAL_CASE_MATCH |
| 指标名称 | 全球成功案例匹配 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 年度 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 否 |
| 关联Q编号 | - |

## 口径定义

从全球同类产业成功发展案例库中，识别与目标产业链在产业结构、发展阶段、要素禀赋上相近的典型案例，并输出匹配程度评分，取值 0—100。对象=全球可对标成功案例，用于为区域产业发展路径提供借鉴。本指标算法库 13 叶无专叶，为 OPEN draft 身份，口径为学术补定义。

## 计算逻辑说明

算法库「产业链深度分析模型」13 叶中无「全球成功案例匹配」叶子，V1 不宣称正式交付，本指标仅以学术定义落档。按案例对标法（Benchmarking）与产业转移雁行理论（Flying-Geese，Akamatsu），以三维修补：案例匹配数量、产业结构相似度、阶段可迁移度。

### 第一步：构建案例库

以全球同类产业成功案例为对象，暂借 `dwd_global_policy_base`（全球政策/报告）、`dwd_forg_base_info`（海外企业）、`chain_global_dist`（全球产业分布）辅助构建候选案例集。正式案例库需待建。

### 第二步：三个子项

1. **案例匹配数量**：与目标产业链标签匹配的全球成功案例去重数。
2. **产业结构相似度**：案例产业与目标产业在环节结构上的相似度（环节集合 Jaccard 相似度）。
3. **阶段可迁移度**：案例产业所处发展阶段与目标产业阶段的可比/可借鉴程度（阶段邻近度评分）。

### 第三步：综合评分

各子项 min-max 归一到 0—100，加权求和：
$$
全球成功案例匹配 = W_1×案例匹配数量得分 + W_2×产业结构相似度得分 + W_3×阶段可迁移度得分
$$

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 全球成功案例匹配 | 案例匹配数量 | 全球案例去重数 | 与目标产业标签匹配的全球成功案例去重数 | COUNT(DISTINCT case_id WHERE 产业标签匹配) | dwd_global_policy_base(id, title, category, country) — 全球案例/政策报告；chain_global_dist(chain_id, country, enterprise_count) — 全球分布 | 全球成功案例库表 |
|  | 产业结构相似度 | 环节结构相似度 | 案例产业与目标产业环节集合 Jaccard 相似度 | \|A∩B\|/\|A∪B\|，A/B=案例/目标环节集合 | dwd_industry_chain_info(industry_code, industry_link_code) — 目标环节；dwd_forg_base_info(org_id, country, industry_code) — 海外产业结构 | 案例产业结构表 |
|  | 阶段可迁移度 | 阶段邻近度评分 | 案例产业阶段与目标产业阶段可比程度 | 阶段邻近度评分（0-100） | chain_stage(chain_id, cycle_stage, sub_stage) — 目标阶段；chain_cycle(chain_id, cycle_stage, trend) — 周期趋势 | 案例发展阶段字段 |

## 源表字段

- dwd_global_policy_base(id, title, category, country, year, theme) — 全球政策/报告（案例辅助）
- dwd_forg_base_info(org_id, name_en, country, industry_code, incorporation_year) — 海外企业/机构（案例主体）
- chain_global_dist(chain_id, chain_name, country, enterprise_count, institution_count) — 全球产业分布
- dwd_industry_chain_info(industry_code, industry_name, industry_link_code) — 目标产业链环节
- chain_stage(chain_id, chain_name, cycle_stage, sub_stage) — 目标产业阶段
- chain_cycle(chain_id, chain_name, cycle_stage, trend) — 周期趋势

## 待建字段

- 全球成功案例库表（案例ID、产业标签、环节结构、发展阶段、成功要素）
- 案例产业结构环节明细字段
- 案例发展阶段字段
- 匹配权重与相似度阈值（学术补定义，待甲方确认）

## 参考资料

[1] 对标管理 Benchmarking｜Robert C. Camp｜Benchmarking: The Search for Industry Best Practices that Lead to Superior Performance（1989）。

[2] 产业转移雁行理论｜Akamatsu K.｜A Historical Pattern of Economic Growth in Developing Countries（1962）。

[3] 全球产业链案例对标｜国务院发展研究中心｜产业国际竞争力对标分析框架（案例匹配数量/结构相似度/阶段可迁移度）。
