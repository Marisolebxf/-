# 湾区创新能力短板因素（M_INNOV_GBA_SWOT_WEAKNESS）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_GBA_SWOT_WEAKNESS |
| 指标名称 | 湾区创新能力短板因素 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新能力分析（SWOT） |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

在选定湾区城市下，从四子指数的 12 个分项中识别相对落后的短板因素，给出清单、表现与改进建议。本指标不是 0—100 评分。

## 计算逻辑说明

湾区 11 城、入集、12 个分项与优势因素完全相同，只改入选方向。分项原始值复用四子指标。

### 第一步：取分项并排名

同优势因素：每城 12 个分项在 11 城内降序排名 `rank`（1 最好）。页面传入城市（默认深圳）。看湾区整体时：某分项在 ≥4 城进入短板则记为湾区短板。

### 第二步：三个子项

1. **短板清单**：该城 `rank ≥ 9` 的分项。无命中则取 `rank` 最大的 1 项，并标记 `weak_signal=1`。
2. **表现**：该分项原始值 + 11 城排名。
3. **改进建议**：按分项固定映射，不另跑模型。

| 分项 | 改进建议 |
| --- | --- |
| 专利资源 | 加大专利申请与布局 |
| 论文资源 | 加强论文产出与合作发表 |
| 研发投入 | 提高研发人员或上市研发经费 |
| 载体数量 | 引入和培育创新主体 |
| 载体产出 | 提升机构专利与论文产出 |
| 科技型机构 | 推动高企认定与科研院所建设 |
| 联合专利 | 推动多主体联合申请 |
| 合作项目 | 增加多机构立项 |
| 成果转化 | 提高专利转移占比 |
| 政策供给 | 完善地方创新政策供给 |
| 政策覆盖 | 拓展政策主题覆盖 |
| 高企密度 | 提高高新技术企业占比 |

输出：一行一个短板分项，含 `city`、`factor`、`raw`、`rank`、`advice`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 湾区创新能力短板因素 | 短板清单 | 该城相对落后的分项。 | 11 城排名 ≥ 9 | 见四子指标分项计算结果 — 入选 | 无 |
| 湾区创新能力短板因素 | 表现 | 分项原始值与排名。 | 原始值；rank | 同上 — 展示 | 无 |
| 湾区创新能力短板因素 | 改进建议 | 按分项给出动作。 | 分项→建议映射表 | 同上 — 建议 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集
- dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 专利去重,共申请人,申请人对齐,申请年
- dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 合作项目
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入
- dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员
- dwd_org_tech_tag(org_id, org_tag) — 高新技术标签
- dwd_policy_base(id, city, province, status, expire_date, publish_year, rank, theme) — 政策供给,主题,有效

## 待建字段

- 无

## 参考资料

[1]湾区创新能力短板因素｜中国科学学与科技政策研究会｜《中国区域创新能力评价报告2025》｜2025-09-27｜https://www.casssp.org.cn/news_Detail_1/1073.html.

[2]湾区创新能力短板因素｜中国科学技术发展战略研究院｜《中国区域科技创新评价报告2025》｜2025-09-23｜http://casted.org.cn/zlyxw/20250922/268981.html.

