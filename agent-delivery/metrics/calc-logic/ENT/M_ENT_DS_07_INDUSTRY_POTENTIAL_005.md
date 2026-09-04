# 技术影响力评估（M_ENT_DS_07_INDUSTRY_POTENTIAL_005）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_DS_07_INDUSTRY_POTENTIAL_005 |
| 指标名称 | 技术影响力评估 |
| 一级模块 | 企业分析 |
| 二级模块 | 企业评估 |
| 三级模块 | - |
| 更新频率 | 年度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q009 |

## 口径定义

基于专利引用与技术标准数据，评估特定产业的技术影响力，输出技术影响力指标（专利被引次数、标准必要专利数量）的分布情况与排名。对象=产业（领域）的专利技术产出集合，不是单件专利。禁止 mapped 145 / 05 seq 150，禁止 also_in DS-01-FACTORS（见 POT-D05）。

## 计算逻辑说明

两维加权：专利被引影响力 / 标准必要专利（SEP）。

### 第一步：入集

统计窗默认自然年。产业→专利映射：经权利人（`first_applicant_name` / `first_current_assignee_name`）与机构名称对齐，或 `dwd_org_base_info_patent_rel`。专利被引 `dwd_patent_cited.cited_by_nums`。

### 第二步：两个子项

1. **专利被引影响力**：
   - 专利被引总次数 = `SUM(cited_by_nums)`；
   - 篇均专利被引 = 被引总次数 ÷ 专利去重数。
2. **标准必要专利（SEP）**：
   - SEP 数量 = `COUNT(DISTINCT 专利 WHERE SEP标签)`；
   - SEP 占比 = SEP 数量 ÷ 专利去重数 × 100%。

两维极值归一后等权得技术影响力，输出产业分布与排名。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 技术影响力评估 | 专利被引影响力 | 专利被引总次数 | 产业专利被引次数合计。 | SUM(cited_by_nums) | dwd_patent(pn, patent_id, kind, granted_number, first_applicant_name, pbdt_year) — 专利入集,权利人,年窗；dwd_patent_cited(pn, patent_id, cited_by_nums) — 专利被引 | 无 |
|  |  | 篇均专利被引 | 被引总次数 ÷ 专利去重数。 | 被引合计/专利去重数 | dwd_patent(pn, patent_id, kind, first_applicant_name, pbdt_year) — 专利去重；dwd_patent_cited(pn, cited_by_nums) — 专利被引 | 无 |
| 技术影响力评估 | 标准必要专利 | 标准必要专利数量 | 属于标准必要专利的专利去重数。 | COUNT(DISTINCT SEP专利) | dwd_patent(pn, patent_id, kind, first_applicant_name, pbdt_year) — 专利入集 | 标准必要专利标签表 |
|  |  | SEP 占比 | SEP 数量 ÷ 专利去重数。 | SEP数/专利去重数 | dwd_patent(pn, patent_id, first_applicant_name) — 专利去重 | 标准必要专利标签表 |

## 源表字段

- dwd_patent(pn, patent_id, kind, granted_number, first_applicant_name, pbdt_year) — 专利去重,权利人,年窗
- dwd_patent_cited(pn, patent_id, cited_by_nums) — 专利被引次数

## 待建字段

- 标准必要专利（SEP）标签表：现库无标准/SEP 相关表（`standard` 无匹配），需新建 SEP 标签或从专利法律状态/外部标准库标注。

## 参考资料

[1] 技术影响力评估 | 需规 SRS《科技创新评估.md》序号150 | 专利被引次数、标准必要专利数量分布与排名 | 关联 Q009。

[2] 标准必要专利（Standard-Essential Patent）| 欧洲电信标准协会（ETSI）IPR 数据库 | https://ipr.etsi.org/。
