# 产业链完整度评分（M_CHAIN_COMPLETENESS_SCORE）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_COMPLETENESS_SCORE |
| 指标名称 | 产业链完整度评分 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | QC01 |

## 口径定义

指定产业链在统计窗内的完整度综合评分，从环节覆盖完整度、企业覆盖均匀度、产值覆盖度三维评定，取值 0—100。分数越高表示产业链结构越完整、断点越少。对象=产业链整体完整度，不是单环节完整度。口径对应 QC01，待甲方冻结。

## 计算逻辑说明

采用加权平均。三维：环节覆盖完整度 / 企业覆盖均匀度 / 产值覆盖度。算法库「产业链全景模型构建」（1.1.1.1.1.1.1.3.1，约 431 行）提出「识别产业链完整性与断点」及「动态更新保持完整性」，但未给出独立完整度公式；按产业链完整性评价学术惯例补齐三维，默认等权（ΣW=1）。

### 第一步：入集

按 `dwd_industry_chain_info.industry_code` 定链，标准环节树由 `industry_link_code`/`level`/`parent_code` 构成；已落地环节由 `chain_node`/`chain_panorama` 提供。

### 第二步：三个子项

1. **环节覆盖完整度**：已覆盖环节数 ÷ 标准全链环节数 × 100。分子=`chain_panorama.node_count`，分母=该链 `dwd_industry_chain_info` 去重 `industry_link_code` 数。
2. **企业覆盖均匀度**：各环节企业分布的均匀程度。用各环节企业数在链上的变异系数（CV=σ/μ）反向映射：均匀度=100×(1−CV)。环节企业数来自 `chain_enterprise` 按节点聚合。
3. **产值覆盖度**：有产值/营收数据的环节占比。分子=能关联到 `chain_market.total_revenue` 的环节数，分母=全链环节数。

### 第三步：综合得分

各子项 min-max 归一到 0—100，等权求和：
$$
产业链完整度评分 = \frac{1}{3}(环节覆盖完整度得分 + 企业覆盖均匀度得分 + 产值覆盖度得分)
$$

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 产业链完整度评分 | 环节覆盖完整度 | 环节覆盖率 | 已覆盖环节数占标准全链环节数比重 | 已覆盖环节数/全链环节数×100 | chain_panorama(chain_id, node_count) — 已覆盖环节数；dwd_industry_chain_info(industry_code, industry_link_code, level) — 标准全链环节 | 标准全链环节权威基准 |
|  | 企业覆盖均匀度 | 环节企业分布均匀度 | 各环节企业数的离散程度反向映射 | 100×(1−CV)，CV=环节企业数标准差/均值 | chain_enterprise(chain_id, enterprise_id, city, district) — 环节企业聚合；chain_node(node_id, chain_id, node_name) — 环节 | 无 |
|  | 产值覆盖度 | 产值覆盖环节占比 | 有营收/产值数据的环节占比 | 有产值环节数/全链环节数×100 | chain_market(chain_id, total_revenue, enterprise_count) — 产业链产值；dwd_industry_chain_info(industry_code, industry_link_code) — 全链环节 | 环节级产值字段 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, level, parent_code, node_company_count) — 标准环节树
- chain_panorama(chain_id, chain_name, node_count, edge_count, enterprise_count) — 全景已落地环节/企业（gkxlumenx_ads / demo_gkxlumenx_ads）
- chain(chain_id, chain_name, industry_code, node_count) — 产业链主表（gkxlumenx_dwd）
- chain_node(node_id, chain_id, node_name, position) — 环节
- chain_enterprise(chain_id, enterprise_id, enterprise_name, city, district) — 链上企业
- chain_market(chain_id, chain_name, stat_year, total_revenue) — 产业链产值

## 待建字段

- 标准全链环节权威基准字段（应覆盖环节数，由业务/QC01 冻结）
- 环节级产值字段（现 `chain_market` 仅产业链粒度）
- 完整度计算阈值与权重（QC01 待甲方确认）

## 参考资料

[1] 产业链全景模型构建｜科技专题服务算法库 1.1.1.1.1.1.1.3.1（完整性与断点识别、动态更新）。

[2] 产业链完整度评价｜工业和信息化部｜《关于提升产业链供应链韧性和安全水平的指导意见》，以环节覆盖、企业布局、产值覆盖衡量产业链完整性。

[3] 产业链完整性测度｜中国电子信息产业发展研究院（赛迪）｜产业链现代化水平评估指标体系（环节覆盖度/企业均匀度/产值覆盖度）。
