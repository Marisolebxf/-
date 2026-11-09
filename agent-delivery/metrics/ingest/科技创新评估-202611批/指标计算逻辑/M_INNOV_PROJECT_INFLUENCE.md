# 项目（含课题）影响力（M_INNOV_PROJECT_INFLUENCE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_PROJECT_INFLUENCE |
| 指标名称 | 项目（含课题）影响力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.3-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

单个科技项目/课题的影响程度。从资助金额、参与机构数、结题完备度综合，取值 0—100。

## 计算逻辑说明

第一步至合成：入集：`dwd_zh_project`/`dwd_en_project` 按 `id` 去重；`approval_year` 落统计年。资助金额：`funded_amount`（空当缺测）；参与机构数：解析 `participating_institution` 去重个数，没有则受资助机构计 1；结题完备：有非空 `final_report_abstract` 记 1，否则 0。三子项本批极值归一等权 ×100。不用项目数=1 充数。

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
项目影响力=\frac{norm(资助金额)+norm(参与机构数)+norm(结题完备)}{3}\times 100
$$

输出：按二级子项给出原始值与合成结果（评分类为 0—100；聚类/异常/预测输出标签或期次）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 项目（含课题）影响力 | 资助金额 | 获资助经费。 | funded_amount | dwd_zh_project(id, funded_amount) — 国内资助金额；dwd_en_project(id, funded_amount) — 国外资助金额 | 无 |
| 项目（含课题）影响力 | 参与机构数 | 参与机构规模。 | COUNT(DISTINCT participating_institution) | dwd_zh_project(id, participating_institution, funded_institution) — 国内参与机构,受资助机构；dwd_en_project(id, participating_institution, funded_institution) — 国外参与机构,受资助机构 | 无 |
| 项目（含课题）影响力 | 结题完备 | 结题摘要有无。 | I(final_report_abstract非空) | dwd_zh_project(id, final_report_abstract) — 国内结题摘要；dwd_en_project(id, final_report_abstract) — 国外结题摘要 | 无 |

## 源表字段

- dwd_zh_project(id, title, funded_amount, participating_institution, funded_institution, final_report_abstract, approval_year) — 国内项目入集,资助金额,参与机构,受资助机构,结题摘要,立项年
- dwd_en_project(id, title, funded_amount, participating_institution, funded_institution, final_report_abstract, approval_year) — 国外项目入集,资助金额,参与机构,受资助机构,结题摘要,立项年

## 待建字段

- 无

## 参考资料

[1]项目影响力｜财政部｜项目支出绩效评价管理办法：财预〔2020〕10号｜2020-02-25｜[财政部关于印发《项目支出绩效评价管理办法》的通知　　项目支出绩效评价管理办法__2020年第15号国务院公报_中国政府网](https://www.gov.cn/gongbao/content/2020/content_5515285.htm).

[2]项目影响力｜科技部办公厅｜国家重点研发计划项目综合绩效评价工作规范（试行）：国科办资〔2018〕107号｜2018-12-14｜[科技部办公厅关于印发《国家重点研发计划项目综合绩效评价工作规范（试行）》的通知-中华人民共和国科学技术部](https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2018/201812/t20181229_144402.html).

