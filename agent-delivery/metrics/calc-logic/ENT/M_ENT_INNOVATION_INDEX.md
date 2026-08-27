# 创新能力指数（M_ENT_INNOVATION_INDEX）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_INNOVATION_INDEX |
| 指标名称 | 创新能力指数 |
| 一级模块 | 企业分析 |
| 二级模块 | 企业评估 |
| 三级模块 | 综合竞争力评估 |
| 更新频率 | 年度/模型版本发布时 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q014 |


## 口径定义

企业创新能力评估的综合得分，满分0—100分，综合反映企业在创新投入、创新产出及可持续发展能力的综合水平。

## 计算逻辑说明

$$
第一步：各指标层得分
指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij}为企业 i 在第 j 个指标上的原始值，min(x_j)和max(x_j)分别为该指标在同产业所有企业中的最小值和最大值。
$$

$$
第二步：准则层得分
准则层得分_{ik} = \sum_{j \in S_k} w_j \times 指标得分_{ij}
$$

$$
其中，S_k为第 k 个准则层下的指标集合，w_j为各指标权重。
$$

$$
第三步：创新能力指数综合得分
创新能力指数_i = \sum_{k=1}^{3} W_k \times 准则层得分_{ik}
$$

$$
其中，W_k为各准则层权重，i为企业编号。
$$



| 指标一级         | 指标二级               | 指标三级                   | 计量方式                                                     | 源表字段 |
| :--------------- | :----------------------- | :--------------------------- | :----------------------------------------------------------- | -------- |
| **企业创新能力** | **创新投入能力**         | 研发投入占比                 | 研发投入 / 营业收入                                          | gkx.dwd_org_annual_financial_info(org_id, `arch development am`, operating_revenue, year) — 研发投入占比=`arch development am`÷营业收入×100%，优先年报 |
|                  |                          | 资本化研发投入占比           | 资本化研发投入 / 研发投入                                    | gkx.dwd_org_annual_financial_info(org_id, `arch development am`, year) — 研发投入总额（分母）<br>gkx 现库无资本化研发投入字段（待建）— 资本化研发投入 |
|                  |                          | 科研平台数量                 | 实验室（国家级、省级）及流动站的数量                         | gkx 现库无科研平台/实验室记录表（待建）— 科研平台数量 |
|                  |                          | 技术人员占比                 | 技术人员人数 / 员工总人数                                    | gkx.dwd_org_annual_financial_info(org_id, development_employee, employees_number, year) — 技术人员占比=研发人员数÷从业人数×100%，优先年报 |
|                  |                          | 本科及以上学历员工占比       | 本科及以上学历人数 / 员工总人数                              | gkx.dwd_org_annual_financial_info(org_id, employees_number, year) — 员工总人数（分母）<br>gkx 现库无学历结构字段（待建）— 本科及以上学历人数 |
|                  | **创新产出能力**         | 专利申请数量                 | 专利申请数量                                                 | gkx.dwd_patent(patent_id, pn, first_current_assignee_name) — 专利申请数量 |
|                  |                          | 专利质量                     | 有效发明专利数量 / 有效专利数量                              | gkx.dwd_patent(patent_id, pn, kind, first_current_assignee_name) — 专利类型与申请人<br>gkx.dwd_patent_legal(patent_id, status) — 法律状态过滤有效专利 |
|                  |                          | 专利申请增长率               | （本期专利申请数量 / 上期专利申请数量）- 1                   | gkx.dwd_patent(patent_id, pn, first_current_assignee_name) — 专利申请数量<br>gkx.dwd_patent_legal(patent_id, isdt_year) — 按年份分组计算同比 |
|                  |                          | 软件著作权数量               | 企业目前拥有的软件著作权数量                                 | gkx 现库无软件著作权表（待建）— 软件著作权数量 |
|                  |                          | 技术型无形资产占比           | 技术型无形资产账面价值 / 总资产账面价值                      | gkx.dwd_org_annual_financial_info(org_id, total_assets, year) — 总资产（分母）<br>gkx 现库无形资产明细字段（待建）— 技术型无形资产账面价值 |
|                  |                          | 技术型无形资产占比增长率     | （本期技术型无形资产占总资产比率 / 上期技术型无形资产占总资产比率）- 1 | gkx.dwd_org_annual_financial_info(org_id, total_assets, year) — 总资产（分母）<br>gkx 现库无形资产明细字段（待建）— 技术型无形资产账面价值 |
|                  |                          | 科技获奖数量                 | 国家级、省级获奖数量                                         | gkx.dwd_org_tech_tag(org_id, org_tag) — 资质/荣誉标签筛选获奖类标签 |
|                  | **创新的可持续发展能力** | 总资产增长率                 | （本期总资产 / 上期总资产）- 1                               | gkx.dwd_org_annual_financial_info(org_id, total_assets, year) — 按年报年度同比计算，优先年报 |
|                  |                          | 营业收入增长率               | （本期营业收入 / 上期营业收入）- 1                           | gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 按年报年度同比计算，优先年报 |
|                  |                          | 净利润增长率                 | （本期净利润 / 上期净利润）- 1                               | gkx.dwd_org_annual_financial_info(org_id, pure_profit, year) — 按年报年度同比计算，优先年报 |
|                  |                          | 研发投入增长率               | （本期研发投入 / 上期研发投入）- 1                           | gkx.dwd_org_annual_financial_info(org_id, `arch development am`, year) — 按年报年度同比计算，优先年报 |
|                  |                          | 本科及以上学历员工占比增长率 | （本期本科及以上学历员工占比 / 上期本科及以上学历员工占比）- 1 | gkx.dwd_org_annual_financial_info(org_id, employees_number, year) — 员工总人数<br>gkx 现库无学历结构字段（待建）— 本科及以上学历人数 |

## 源表字段

gkx.dwd_org_annual_financial_info(org_id, operating_revenue, total_profit, pure_profit, total_assets, `arch development am`, development_employee, employees_number, year) — 创新投入维度（研发投入占比、技术人员占比）、创新产出维度（技术型无形资产占比）、可持续发展维度（总资产增长率、营业收入增长率、净利润增长率、研发投入增长率），优先年报，覆盖非上市企业
gkx.dwd_patent(patent_id, pn, kind, first_current_assignee_name) — 创新产出维度（专利申请数量、专利质量、专利申请增长率）
gkx.dwd_patent_legal(patent_id, status, isdt_year) — 创新产出维度（法律状态过滤有效专利、按年份计算增长率）
gkx.dwd_org_tech_tag(org_id, org_tag) — 创新产出维度（科技获奖数量，资质/荣誉标签筛选）
资本化研发投入字段 — 现库无此字段，待建
科研平台/实验室记录表 — 现库无此表，待建
学历结构字段 — 现库无此字段，待建
软件著作权表 — 现库无此表，待建
无形资产明细字段 — 现库无此字段，待建

注：创新能力指数由创新投入能力、创新产出能力、创新的可持续发展能力三个准则层加权汇总，各指标经极值归一化后按权重加权计算，权重待甲方确认（Q014）。结果表 ads_ent_innovation_index(score, org_id, 待建)。

## 待建字段

资本化研发投入字段 — 现库无此字段，待建
科研平台/实验室记录表 — 现库无此表，待建
学历结构字段 — 现库无此字段，待建
软件著作权表 — 现库无此表，待建
无形资产明细字段 — 现库无此字段，待建
