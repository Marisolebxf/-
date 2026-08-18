# 培育推荐指数（M_ENT_CULTIVATION_INDEX）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 本指标含 7 行子指标（L1+L2+L3），已合并为单文件。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## L1 指标元数据

- **指标ID**：`M_ENT_CULTIVATION_INDEX`
- **指标名称（一级）**：培育推荐指数
- **一级模块**：企业分析
- **二级模块**：引育推荐
- **三级模块**：培育推荐
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **是否在数据库（L1）**：是
- **关联Q编号**：Q015

## L1 口径定义

对区域优质中小企业培育推荐工作成效进行综合量化评价的指数，综合反映企业在产业相关度、政策匹配度、企业潜力三个维度的培育价值。依照需求文档提供的构建方法。

## L1 计算逻辑说明

```
将产业相关度、政策匹配度、企业潜力三个维度的得分按权重加权求和，得出培育推荐指数综合得分。
```

**计算公式文件**：`M_ENT_CULTIVATION_INDEX.md`

## L1 源表字段

```
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
```

## L1 备注

1.1.1.2.4.2.3.7 + 算法库5.8；依照需求文档提供的构建方法

## 子指标详情（L2 / L3）

### L2：产业相关度

#### L3：产业链融入度

- **口径定义**：从企业与目标产业链融入度评估企业产业相关度。
- **计算逻辑**：`【同产业匹配度M_ENT_INDUSTRY_MATCH_SCORE计算逻辑】`
- **源表字段**：`gkx.dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 企业与产业链节点关联<br>gkx.dwd_org_annual_financial_info(org_id, main_business_revenue, year) — 行业收入占比（c_i 权重）<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 企业行业归属（上游度映射）<br>gkx.dwd_org_shareholder_info(org_id, inv_org_id) — 股东关系（产业链图谱边）`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q015
- **是否在数据库**：是
- **备注**：1.1.1.2.4.2.3.7 + 算法库5.8；依照需求文档提供的构建方法

### L2：政策匹配度

#### L3：行动型契合

- **口径定义**：从行动型契合、话语型契合维度评估企业政策匹配度。
- **计算逻辑**：`构建政策词典提取政府工作报告、人民日报等文本中的政策关键词，借助GPT分类框架对企业年报中的相关表述进行识别，从企业实际行动层面衡量其与政策目标的匹配程度，重点关注企业在产能扩张、研发投入、环保合规等具体经营活动上是否响应政策号召。`
- **源表字段**：`gkx.dwd_policy_base(content, keywords, theme, policy_support) — 政策词典与关键词提取<br>gkx.dwd_org_org_product_info(org_id, description, main_activities) — 企业经营行为文本（GPT识别行动型契合）`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q015
- **是否在数据库**：是
- **备注**：1.1.1.2.4.2.3.7 + 算法库5.8；依照需求文档提供的构建方法；政策库匹配待建

#### L3：话语型契合

- **口径定义**：从行动型契合、话语型契合维度评估企业政策匹配度。
- **计算逻辑**：`构建政策词典提取政府工作报告、人民日报等文本中的政策关键词，借助GPT分类框架对企业年报中的相关表述进行识别，从企业公开表述层面衡量其与政策话语的匹配程度，重点关注企业年报中关于战略定位、发展展望、行业分析等叙述性内容是否与政策话语保持一致。`
- **源表字段**：`gkx.dwd_policy_base(content, keywords, theme) — 政策词典与关键词提取<br>gkx.dwd_org_org_product_info(org_id, description) — 企业对外传播文本（GPT识别话语型契合）`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q015
- **是否在数据库**：是
- **备注**：1.1.1.2.4.2.3.7 + 算法库5.8；依照需求文档提供的构建方法；政策库匹配待建

### L2：企业潜力

#### L3：企业资产总额

- **口径定义**：从资产总额、盈利能力、研发投入维度评估企业成长性与创新能力。
- **计算逻辑**：`直接取自企业资产负债表中“资产总计”科目期末余额`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, total_assets, year) — 资产总额`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q015
- **是否在数据库**：是
- **备注**：1.1.1.2.4.2.3.7 + 算法库5.8；依照需求文档提供的构建方法

#### L3：企业盈利能力

- **口径定义**：从资产总额、盈利能力、研发投入维度评估企业成长性与创新能力。
- **计算逻辑**：`净利润 ÷ 营业收入 × 100%`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, pure_profit, total_assets, total_liabilities, year) — 净利润与平均净资产`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q015
- **是否在数据库**：是
- **备注**：1.1.1.2.4.2.3.7 + 算法库5.8；依照需求文档提供的构建方法

#### L3：企业研发投入

- **口径定义**：从资产总额、盈利能力、研发投入维度评估企业成长性与创新能力。
- **计算逻辑**：`研发费用 ÷ 营业收入 × 100%`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, `arch development am`, operating_revenue, year) — 研发投入金额与营业收入`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q015
- **是否在数据库**：是
- **备注**：1.1.1.2.4.2.3.7 + 算法库5.8；依照需求文档提供的构建方法

---
*生成自王惠 20260816 Excel 底稿（7 行），data-agent 正式化 2026-08-18*
