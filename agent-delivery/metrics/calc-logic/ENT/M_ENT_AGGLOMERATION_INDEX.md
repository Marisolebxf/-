# 集聚指数（M_ENT_AGGLOMERATION_INDEX）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_AGGLOMERATION_INDEX |
| 指标名称 | 集聚指数 |
| 一级模块 | 企业分析 |
| 二级模块 | 企业发展 |
| 三级模块 | - |
| 更新频率 | 年度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 是 |
| 关联Q编号 | Q009 / Q012 |

## 口径定义

在选定的产业范围内，度量企业在全国—省—市逐级区域的空间集聚程度，综合反映企业在地理与产业维度的专业化集聚、均衡程度与集中度，取值 0—100。分数越高表示集聚程度越强。对象=区域企业分布（集聚效应），不是单家企业。

需求文档（算法库「企业基础指标模型构建」ALGO-ENT-BASE-97）仅要求「地区分布延伸、直观反映集聚效应」，未给定具体公式；本版按区域经济学经典方法补齐区位熵、空间基尼系数与赫芬达尔—赫希曼指数三项，学术依据见「参考资料」。

## 计算逻辑说明

采用三维加权：区位熵（专业化集聚）/ 空间基尼系数（地理均衡度）/ 赫芬达尔—赫希曼指数（集中度）。各维极值归一后等权（ΣW=1，可按评估重点改权）。

### 第一步：入集

统计窗默认自然年。区域落到 `dwd_org_base_info.city` / `province` / `area`（区划层级对齐 `dwd_dim_admin_area.cur_level`）。存续：`reg_status` 含「存续」。产业归类以 `industry_l1_code/l2_code/l3_code` 或 `dwd_org_industry_tags.industry_code` 为准。

### 第二步：三个子项

1. **区位熵 LQ（专业化集聚）**
   $$ LQ_{ij} = \frac{E_{ij} / E_i}{E_j / E} $$
   其中 $E_{ij}$ 为区域 $i$ 产业 $j$ 的企业数，$E_i$ 为区域 $i$ 全部企业数，$E_j$ 为全国产业 $j$ 企业数，$E$ 为全国企业总数。$LQ>1$ 表示该区域该产业具有相对专业化集聚优势。可另按注册资本口径计算规模区位熵。

2. **空间基尼系数 G（地理集聚均衡度，Krugman 1991）**
   $$ G = \sum_i (s_i - x_i)^2 $$
   其中 $s_i$ 为区域 $i$ 某产业企业数占全国该产业企业数的比重，$x_i$ 为区域 $i$ 全部企业数占全国企业数的比重。$G$ 越大表示该产业越集中于少数区域。

3. **赫芬达尔—赫希曼指数 HHI（区域集中度）**
   $$ HHI = \sum_i (E_i / E)^2 $$
   取值 (0,1]，越大表示企业区域分布越集中。

维内子项归一等权得维得分，三维等权得指数。输出区域一行，含三维得分与综合集聚指数。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 集聚指数 | 区位熵（专业化集聚） | 企业数量区位熵 | 区域某产业企业占比相对全国的倍数。 | LQ=(E_ij/E_i)/(E_j/E) | dwd_org_base_info(org_id, external_id, city, province, area, industry, industry_l1_code, industry_l2_code, industry_l3_code, reg_status) — 企业区域+行业归类,存续；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业链归类 | 无 |
|  |  | 注册资本区位熵 | 按注册资本规模口径的专业化集聚倍数。 | LQ_cap=(C_ij/C_i)/(C_j/C) | dwd_org_base_info(org_id, external_id, city, province, area, industry, industry_l1_code, industry_l2_code, industry_l3_code, registered_capital_value, reg_status) — 企业区域+行业+注册资本,存续 | 无 |
| 集聚指数 | 空间基尼系数（地理集聚均衡度） | 企业数量空间基尼系数 | 产业企业数在区域间分布的均衡程度。 | G=Σ(s_i-x_i)² | dwd_org_base_info(org_id, external_id, city, province, area, industry_l1_code, industry_l2_code, industry_l3_code, reg_status) — 企业区域+行业,存续 | 无 |
|  |  | 注册资本空间基尼系数 | 按注册资本规模口径的区域分布均衡度。 | G_cap=Σ(cs_i-cx_i)² | dwd_org_base_info(org_id, external_id, city, province, area, industry_l1_code, industry_l2_code, industry_l3_code, registered_capital_value, reg_status) — 企业区域+行业+注册资本,存续 | 无 |
| 集聚指数 | 赫芬达尔—赫希曼指数（区域集中度） | 企业区域分布 HHI | 企业在全国各区域分布的市场集中度。 | HHI=Σ(E_i/E)² | dwd_org_base_info(org_id, external_id, city, province, area, reg_status) — 企业区域,存续；dwd_dim_admin_area(cur_code, cur_name, parent_code, city_code, area_code, cur_level) — 区划层级 | 无 |

## 源表字段

- dwd_org_base_info(org_id, external_id, city, province, area, industry, industry_l1_code, industry_l2_code, industry_l3_code, registered_capital_value, reg_status) — 企业区域+行业+注册资本,存续
- dwd_org_industry_tags(credit_code, industry_code, industry_name) — 企业与产业链归类
- dwd_dim_admin_area(cur_code, cur_name, parent_code, city_code, area_code, cur_level) — 行政区划层级（区划精度对齐 Q012）

## 待建字段

- 无（若需「企业—目标未来产业」精确映射，可依托 industry_l1/l2/l3 分级，无需新建表）

## 参考资料

[1] 区位熵（Location Quotient）| Hoover E.M. | The Location of Economic Activity | 1948 | McGraw-Hill.

[2] 空间基尼系数 | Krugman P. | Geography and Trade | 1991 | MIT Press.

[3] 赫芬达尔—赫希曼指数（HHI）| 美国司法部与联邦贸易委员会 | Horizontal Merger Guidelines | https://www.justice.gov/atr/horizontal-merger-guidelines-08192010.

[4] 企业基础指标模型构建 | 算法库 §1.1.1.1.1.1.1.1 | 需求ID ALGO-ENT-BASE-97 | 关联 Q009 / Q012。
