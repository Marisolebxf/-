# 培育推荐指数（M_ENT_CULTIVATION_INDEX）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_CULTIVATION_INDEX |
| 指标名称 | 培育推荐指数 |
| 一级模块 | 企业分析 |
| 二级模块 | 引育推荐 |
| 三级模块 | 培育推荐 |
| 更新频率 | 年度/模型版本发布时 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 是 |
| 关联Q编号 | Q015 |


## 口径定义

用于识别并优选具有高培育价值的企业，通过产业相关度、政策匹配度、企业潜力三个维度构建评价体系，综合计算生成企业培育推荐指数。。

## 计算逻辑说明

第一步：各三级指标标准化

各指标原始数据通过极值归一化法消除量纲，转换为0—100之间的标准化得分：
$$
正向指标（数值越大越好）：指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij}为企业 i 在第 j个指标上的原始值，\min(x_j) 和 \max(x_j) 分别为该指标在所有企业中的最小值和最大值。
$$

第二步：各维度得分计算

各维度得分即该维度下三级指标的加权汇总：

| 一级维度       | 维度得分计算方式                                   |
| :------------- | :------------------------------------------------- |
| **产业相关度** | 直接取产业链融入度的标准化得分                     |
| **政策匹配度** | 行动型匹配得分与话语型匹配得分的加权平均           |
| **企业潜力**   | 资产总额、盈利能力、研发投入三个指标得分的加权汇总 |

第三步：培育推荐指数综合得分

将三个维度的得分加权汇总：
$$
培育推荐指数_i = W_1 \times 产业相关度得分_i + W_2 \times 政策匹配度得分_i + W_3 \times 企业潜力得分_i
$$

$$
其中，W_1、W_2、W_3 为各一级维度权重，可采用等权重（各 1/3）或熵值法确定，i为企业编号。最终得分越高，表明企业培育推荐价值越高。
$$



| 一级维度       | 三级指标     | 指标说明                                                     | 源表字段                                                     |
| :------------- | :----------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **产业相关度** | 产业链融入度 | 指企业在产业链中的融入程度，综合反映企业在产业链中的位置及其与产业链各环节的关联紧密程度。基于公司产业链数据，将产业链抽象为网络结构，测算产业链关联度（反映产业链整体紧密程度）与企业质心度（反映企业在产业链网络中的位置），两者相乘得到企业层面的产业链融入度。**【同产业匹配度M_ENT_INDUSTRY_MATCH_SCORE计算逻辑】** | gkx.dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 企业与产业链节点关联<br>gkx.dwd_org_annual_financial_info(org_id, main_business_revenue, year) — 行业收入占比（c_i 权重）<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 企业行业归属（上游度映射）<br>gkx.dwd_org_shareholder_info(org_id, inv_org_id) — 股东关系（产业链图谱边） |
| **政策契合度** | 行动型契合   | 指企业在实际经营行为、战略投资、政策执行等行动层面与政策目标保持一致的程度。构建政策词典提取政府工作报告、人民日报等文本中的政策关键词，借助GPT分类框架对企业年报中的相关表述进行识别，重点关注企业在产能扩张、研发投入、环保合规等具体经营活动中是否响应政策号召。 | gkx.dwd_policy_base(content, keywords, theme, policy_support) — 政策词典与关键词提取<br>gkx.dwd_org_org_product_info(org_id, description, main_activities) — 企业经营行为文本（GPT识别行动型契合） |
|                | 话语型契合   | 指企业在公开声明、年报、官网等对外传播中与政策话语保持一致的程度。构建政策词典提取政府工作报告、人民日报等文本中的政策关键词，借助GPT分类框架对企业年报中的相关表述进行识别，重点关注企业年报中关于战略定位、发展展望、行业分析等叙述性内容是否与政策话语保持一致。 | gkx.dwd_policy_base(content, keywords, theme) — 政策词典与关键词提取<br>gkx.dwd_org_org_product_info(org_id, description) — 企业对外传播文本（GPT识别话语型契合） |
| **企业潜力**   | 企业资产总额 | 指企业期末拥有的全部资产，反映企业拥有的经济资源总量和经营规模。取自企业资产负债表中"资产总计"科目期末余额。 | gkx.dwd_org_annual_financial_info(org_id, total_assets, year) — 资产总额 |
|                | 企业盈利能力 | 指企业在一定时期内获取利润的能力，通过净资产收益率衡量，反映股东投入资本的获利效率。净资产收益率 = 净利润 ÷ 平均净资产 × 100%。 | gkx.dwd_org_annual_financial_info(org_id, pure_profit, total_assets, total_liabilities, year) — 净利润与平均净资产 |
|                | 企业研发投入 | 指企业在一定时期内投入研发活动的经费总额，反映企业对技术创新的重视程度和资源投入水平。研发投入强度 = 研发费用 ÷ 营业收入 × 100%。 | gkx.dwd_org_annual_financial_info(org_id, `arch development am`, operating_revenue, year) — 研发投入金额与营业收入 |

## 源表字段

gkx.dwd_org_annual_financial_info(org_id, total_assets, total_liabilities, pure_profit, operating_revenue, main_business_revenue, `arch development am`, year) — 资产总额、净资产（=资产总额-负债总额）、净利润、营业收入、研发投入金额（企业潜力三指标 + 产业链收入占比权重）
gkx.dwd_org_base_info(org_id, industry_l1_code) — 企业行业归属（产业链上游度映射）
gkx.dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 企业与产业链节点关联
gkx.dwd_org_shareholder_info(org_id, inv_org_id) — 股东关系（构建产业链图谱边）
gkx.dwd_org_org_product_info(org_id, description, main_activities) — 企业经营行为文本与对外传播文本（GPT识别政策契合度）
gkx.dwd_policy_base(content, keywords, theme, policy_support) — 政策词典与关键词提取（政策契合度匹配）

1.产业链融入度。基于上市公司客户与供应商数据，采用深度优先搜索算法构建全产业链图谱数据库，将产业链抽象为网络结构，测算产业链内部关联度与产业链质心度，两者相乘得到企业层面的产业链融入度：
$$
融入度_i = Link \times Centroid_i
$$

$$
其中，Link为产业链关联度（产业链层面的固定值，同一产业链内所有企业取值相同），Centroid_i 为企业 i 的产业链质心度（企业层面的个体值，反映企业在产业链网络中的位置）。
$$
