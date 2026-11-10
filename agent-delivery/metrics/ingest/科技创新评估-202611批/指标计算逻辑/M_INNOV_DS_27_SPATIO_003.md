# 热点区域自动识别与预警（M_INNOV_DS_27_SPATIO_003）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_27_SPATIO_003 |
| 指标名称 | 热点区域自动识别与预警 |
| 使用位置 | 科技专题服务系统 / 科技专题战略分析 / 空间布局分析 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

按区县识别创新热点并给出预警等级。区域主键就是 `city`+`area`，创新密度 = (专利+论文+项目) / 机构数；密度 ≥ P70 为热点；预警：热点且近窗突增 ≥1 为 2，热点或突增 ≥0.5 为 1。

## 计算逻辑说明

不用核密度、不用机构-专利/作者-机构关系表。成果落到机构所在区县。经纬度只供落图。

### 第一步：入集并落区

存续机构：`dwd_org_base_info`、`dwd_research_institute_base_info` 按 `org_id` 去重，`reg_status` 含「存续」。页面可筛 `province`/`city`。名称用 `name_cn`。

区域主键 `region_key` = `city` + `area`（`area` 空则只用 `city`）。无 `city` 不入集。

统计年成果按名称对齐后继承机构区县：专利 `first_applicant_name`/`apdt_year`；论文作者 `institution`/`cover_year_start`；项目 `funded_institution`/`approval_year`。

### 第二步：三个子项

1. **创新密度**

$$
创新密度=\frac{专利数+论文数+项目数}{该区县存续机构数}
$$

机构数为 0 的区县不出行。

2. **热点标签**  
   本批有效区县（机构数 ≥ 3）内，密度 ≥ 第 70 百分位记 1，否则 0。有效区县 < 5 时标签空。

3. **预警等级**  
   近窗 \($T-2,\ldots,T$\) 相对基线 \($T-7,\ldots,T-3$\) 的成果件数增幅：

$$
\mathrm{burst}=\frac{\bar{y}_{\mathrm{recent}}-\bar{y}_{\mathrm{base}}}{\max(\bar{y}_{\mathrm{base}},1)}
$$

| 条件 | 等级 |
| --- | --- |
| 热点且 burst ≥ 1 | 2 预警 |
| 热点或 burst ≥ 0.5 | 1 关注 |
| 其他 | 0 无 |

输出：一行一个区县，含 `region_key`、密度、`is_hotspot`、`burst`、`alert_level`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 热点区域自动识别与预警 | 创新密度 | 区县单位机构的成果件数。 | (专利数+论文数+项目数) / 存续机构数 | dwd_org_base_info(org_id, name_cn, city, province, area, reg_status) — 机构入集,区县主键；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_zh_project(id, funded_institution, approval_year) — 受资助机构,立项年 | 无 |
| 热点区域自动识别与预警 | 热点标签 | 密度是否达到本批高位。 | 密度 ≥ P70 且机构数≥3 记 1 | 同上密度结果 — 分位判定 | 无 |
| 热点区域自动识别与预警 | 预警等级 | 热点叠加近窗突增。 | 热点且burst≥1 为 2；热点或burst≥0.5 为 1；否则 0 | 同上年序列 — 近窗相对基线 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, addr_lng, addr_lat) — 机构入集,区县主键,名称对齐,落图
- dwd_research_institute_base_info(org_id, name_cn, city, province, area, reg_status) — 科研机构入集
- dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_zh_project(id, funded_institution, approval_year) — 受资助机构,立项年

## 待建字段

- 无

## 参考资料

[1] 统计学习（聚类/预测）|Stanford University|—|James G, Witten D, Hastie T, Tibshirani R. An Introduction to Statistical Learning[M]. New York: Springer, 2013.
