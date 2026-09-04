# 重点布局产业推荐模型（M_CHAIN_DEEP_129_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_129_1 |
| 指标名称 | 重点布局产业推荐模型 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

基于深圳产业优势分析与问题识别，结合专家推荐策略（推荐标准、权重、评估规则），综合计算产业推荐指数，按指数排名筛选重点布局产业，输出重点产业布局建议。对象=深圳重点布局产业，推荐指数越高越优先布局。

## 计算逻辑说明

① 输入：优势得分（advantage_score，复用优势识别）、机遇得分（opportunity_score，复用机遇分析）、政策匹配得分（policy_match_score，产业与深圳政策主题匹配度）。② 综合：三维加权得 recommend_index，按推荐标准与评估规则定级 recommend_level。③ 输出：按 recommend_index 排名生成重点布局产业清单。

- 政策匹配得分 = 归一化(产业主题命中深圳政策数)
- 推荐指数 recommend_index = Σ(Wi × {优势, 机遇, 政策匹配})
- 推荐等级 = 阈值分档(recommend_index)

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 重点布局产业推荐模型 | 优势与机遇 | 优势得分 | 深圳产业优势指数。 | 复用优势识别 advantage_index | chain_sz_advantage(chain_id, chain_name, advantage_index, advantages, weaknesses) | 无 |
|  |  | 机遇得分 | 深圳产业机遇指数。 | 复用机遇分析 opportunity_index | chain_sz_opportunity(chain_id, chain_name, opportunity_index, advantages, weaknesses) | 无 |
| 重点布局产业推荐模型 | 政策匹配 | 政策匹配得分 | 产业与深圳/国家政策主题匹配度。 | 归一化(命中政策数×政策级别) | dwd_policy_base(id, title, publish_year, rank, type, theme, status, province, city) | 政策-产业主题匹配表 |
| 重点布局产业推荐模型 | 推荐判定 | 推荐指数 | 优势/机遇/政策匹配三维加权分。 | Σ(Wi × 三维得分) | gkxlumenx_ads.chain_layout_recommend(chain_id, chain_name, advantage_score, opportunity_score, policy_match_score, recommend_index, recommend_level, rank_overall) | 专家推荐策略参数表（推荐标准/权重/评估规则） |
|  |  | 推荐等级 | 按推荐指数分档的推荐等级。 | 阈值分档(recommend_index) | gkxlumenx_ads.chain_layout_recommend(recommend_level, rank_overall) | 无 |

## 源表字段

- chain_sz_advantage(chain_id, chain_name, advantage_index, advantages, weaknesses, rank_overall) — 优势识别结果
- chain_sz_opportunity(chain_id, chain_name, opportunity_index, advantages, weaknesses, rank_overall) — 机遇分析结果
- chain_competitiveness(chain_id, chain_name, province, competitiveness_index, rank_in_chain) — 竞争力结果
- chain_market(chain_id, chain_name, stat_year, total_revenue, enterprise_count, growth_rate) — 市场规模
- dwd_policy_base(id, title, publish_year, rank, type, theme, status, province, city) — 政策（匹配）
- gkxlumenx_ads.chain_layout_recommend(chain_id, chain_name, advantage_score, opportunity_score, policy_match_score, recommend_index, recommend_level, rank_overall) — 布局推荐结果

## 待建字段

- 政策-产业主题匹配表（政策 theme/keywords 与产业映射）
- 专家推荐策略参数表（推荐标准、权重、评估规则）

## 参考资料

[1] 深圳市「20+8」产业集群行动方案|深圳市人民政府|重点产业布局依据|https://gxj.sz.gov.cn/

[2] 国家竞争优势「钻石模型」|Michael E. Porter, The Competitive Advantage of Nations, 1990.

[3] 产业结构调整指导目录（2024年本）|国家发展改革委|https://www.ndrc.gov.cn/
