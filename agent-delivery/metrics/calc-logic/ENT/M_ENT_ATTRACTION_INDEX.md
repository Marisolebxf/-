# 招引推荐指数（M_ENT_ATTRACTION_INDEX）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_ATTRACTION_INDEX |
| 指标名称 | 招引推荐指数 |
| 一级模块 | 企业分析 |
| 二级模块 | 引育推荐 |
| 三级模块 | 招引推荐 |
| 更新频率 | 季度/模型版本发布时 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q015 |


## 口径定义

对企业作为招商引资目标对象的价值进行综合量化评价的指数，综合反映企业在产业相关度、政策匹配度、深圳连接度三个维度的价值。

## 计算逻辑说明

第一步：各三级指标得分

各三级指标原始数据通过极值归一化法消除量纲，将每个指标的实际值转换为0—100之间的标准化得分：
$$
正向指标（数值越大越好）：
指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
逆向指标（数值越小越好）：
指标得分_{ij} = \frac{\max(x_j) - x_{ij}}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij}为企业 i在第 j个指标上的原始值，\max(x_j)和 \min(x_j) 分别为该指标在所有企业中的最小值和最大值。
$$

第二步：各维度得分

将各维度下所有三级指标的标准化得分与对应权重加权求和，得到每个维度的综合得分：
$$
维度得分_{ik} = \sum_{j \in S_k} w_j \times 指标得分_{ij}
$$

$$
其中，S_k 为第 k个维度（产业相关度、政策契合度、深圳连接度）下的指标集合，w_j为各三级指标权重（可采用等权重或熵值法确定）。
$$

第三步：招引推荐指数综合得分

将五个维度的得分与对应权重加权求和，得到企业招引推荐指数最终得分：
$$
招引推荐指数_i = \sum_{k=1}^{3} W_k \times 维度得分_{ik}
$$

$$
其中，W_k 为第 k个维度的权重（可采用等权重或依据评估目标设定），i 为企业编号。最终得分越高，表明企业越值得被优先推荐引进。
$$

### 招引推荐指数指标体系

| 一级维度       | 三级指标     | 指标说明                                                     | 源表字段                                                     |
| :------------- | :----------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **产业相关度** | 产业链融入度 | 指企业在产业链中的融入程度，综合反映企业在产业链中的位置及其与产业链的关联紧密程度。将产业链抽象为网络结构，测算产业链关联度（反映产业链整体紧密程度）与企业质心度（反映企业在产业链网络中的位置），两者相乘得到企业层面的产业链融入度。**【M_ENT_INDUSTRY_MATCH_SCORE同】** | gkx.dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 企业与产业链节点关联<br>gkx.dwd_org_annual_financial_info(org_id, main_business_revenue, year) — 行业收入占比（c_i 权重）<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 企业行业归属（上游度映射）<br>gkx.dwd_org_shareholder_info(org_id, inv_org_id) — 股东关系（产业链图谱边）<br />外部数据-《中国投入产出表》 |
| **政策匹配度** | 行动型契合   | 指企业在实际经营行为、战略投资、政策执行等行动层面与政策目标保持一致的程度。构建政策词典提取政府工作报告、人民日报等文本中的政策关键词，借助GPT分类框架对企业年报中的相关表述进行识别，重点关注企业在产能扩张、研发投入、环保合规等具体经营活动中是否响应政策号召。 | gkx.dwd_policy_base(content, keywords, theme, policy_support) — 政策词典与关键词提取<br>gkx.dwd_org_org_product_info(org_id, description, main_activities) — 企业经营行为文本（GPT识别行动型契合） |
|                | 话语型契合   | 指企业在公开声明、年报、官网等对外传播中与政策话语保持一致的程度。构建政策词典提取政府工作报告、人民日报等文本中的政策关键词，借助GPT分类框架对企业年报中的相关表述进行识别，重点关注企业年报中关于战略定位、发展展望、行业分析等叙述性内容是否与政策话语保持一致。 | gkx.dwd_policy_base(content, keywords, theme) — 政策词典与关键词提取<br>gkx.dwd_org_org_product_info(org_id, description) — 企业对外传播文本（GPT识别话语型契合） |
| **深圳连接度** | 中心度       | 指目标企业在深圳企业供应链网络中的核心程度。基于公司客户与供应商数据，以深圳企业为节点、以企业间的供应关系为边构建深圳企业产业链网络，采用社会网络分析法计算目标企业的度中心度：中心度 = 目标企业直接连接的深圳企业数量 ÷（深圳企业供应链网络节点总数 − 1）。数值越大，表示目标企业在深圳产业链网络中的直接关联越广泛，核心程度越高。 | gkx.dwd_org_base_info(org_id, city, province) — 筛选深圳企业节点<br>外部数据-供应链数据 |
|                | 经济联系强度 | 指深圳与目标企业所在区域之间的经济联系紧密程度。采用引力模型测算：经济联系量 = [√(深圳人口 × 深圳GDP) × √(区域人口 × 区域GDP)] ÷ 两地交通距离。数值越大，表示深圳与目标企业所在区域之间的经济联系越紧密，目标企业与深圳的经济协同潜力越强。 | gkx.dwd_org_base_info(org_id, city, province) — 企业所在区域<br>外部数据（区域人口、GDP、交通距离）— 引力模型计算 |

## 源表字段

gkx.dwd_org_annual_financial_info(org_id, main_business_revenue, year) — 行业收入占比（产业链关联度 c_i 权重）
gkx.dwd_org_base_info(org_id, industry_l1_code, city, province) — 企业行业归属（上游度映射）+ 企业所在区域（深圳连接度）
gkx.dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 企业与产业链节点关联
gkx.dwd_org_shareholder_info(org_id, inv_org_id) — 股东关系（产业链图谱边 + 深圳网络边）
gkx.dwd_org_invest_info(org_id, inv_org_id) — 投资关系（深圳网络边）
gkx.dwd_org_org_product_info(org_id, description, main_activities) — 企业经营行为文本与对外传播文本（GPT识别政策契合度）
gkx.dwd_policy_base(content, keywords, theme, policy_support) — 政策词典与关键词提取（政策契合度匹配）
外部数据（区域人口、GDP、交通距离）— 引力模型计算经济联系强度（现库无此数据）

外部数据-供应链数据

## 待建字段

外部数据（区域人口、GDP、交通距离）— 引力模型计算经济联系强度（现库无此数据）
