# 科研机构影响力（M_INNOV_ORG_INFLUENCE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_ORG_INFLUENCE |
| 指标名称 | 科研机构影响力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.3-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

科研机构在产出、合作、领域布局上的影响程度。统计对象为科研机构实体，取值 0—100。

## 计算逻辑说明

第一步至合成：入集：`dwd_research_institute_base_info` 或 `dwd_org_base_info` 中科研/高校类，`reg_status` 含存续，按 `org_id` 去重；名称对齐用 `name_cn`。科研产出：专利 `first_applicant_name` 对齐 `name_cn` 的去重 pn 数 + 作者单位 `institution` 对齐的中英文论文去重数；合作广度：统计年项目中 `funded_institution`/`participating_institution` 命中本机构时，同项目其他参与机构去重数；也可加专利 `applicants` 中共申请机构去重邻居数。领域覆盖：命中专利 `main_classification_ipcr` 前 4 位去重数。三维本批极值归一等权 ×100。

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
机构影响力=\frac{norm(科研产出)+norm(合作广度)+norm(领域覆盖)}{3}\times 100
$$

输出：按二级子项给出原始值与合成结果（评分类为 0—100；聚类/异常/预测输出标签或期次）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 科研机构影响力 | 科研产出 | 专利+论文去重件数。 | COUNT(DISTINCT pn)+COUNT(DISTINCT 论文id) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_zh_paper(id, cover_year_start) — 中文论文去重,统计年；dwd_en_paper(id, cover_year_start) — 英文论文去重,统计年 | 无 |
| 科研机构影响力 | 合作广度 | 合作邻居机构数。 | COUNT(DISTINCT 合作机构) | dwd_zh_project(id, funded_institution, participating_institution) — 受资助机构,参与机构；dwd_patent(pn, applicants, first_applicant_name) — 共申请人,申请人对齐 | 无 |
| 科研机构影响力 | 领域覆盖 | IPC 前 4 位去重。 | COUNT(DISTINCT IPC4) | dwd_patent(pn, first_applicant_name, main_classification_ipcr) — 申请人对齐,IPC领域 | 无 |

## 源表字段

- dwd_research_institute_base_info(org_id, name_cn, org_type, reg_status, province, city) — 科研机构入集,名称对齐,类型过滤,存续过滤,空间筛选
- dwd_org_base_info(org_id, name_cn, org_type, reg_status, province, city) — 机构入集补充,名称对齐,类型过滤,存续过滤,空间筛选
- dwd_patent(pn, first_applicant_name, applicants, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,共申请人合作,IPC领域,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,统计年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,统计年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 受资助机构,参与机构,立项年

## 待建字段

- 无

## 参考资料

[1]科研机构影响力｜四川大学公共管理学院｜成都山地所情报分析可持续服务能力建设项目｜谭荣志. ,党跃武.中国科学院研究所科技评价探讨[J]. 现代情报, 2012(9): 155-159.

[2]科研机构影响力｜中国科学院成都文献情报中心｜中国科学院西部之光——西部博士资助项目（Y5C0061001）；中国科学院政策调研课题“中科院科研、人才及政策管理比较研究”（ZYS-2015-05）｜王立娜，陈云伟，徐婧，许轶，方曙. 多因素协同视角下的科研合作能力测度指数构建及应用研究[J]. 情报探索, 2017(7): 1-7.
