# 产业科学影响力（M_INNOV_POT_SCI_INFL）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_POT_SCI_INFL |
| 指标名称 | 产业科学影响力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 产业发展潜力指标展示 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

选定产业的科学影响力。从论文被引次数、国际合作论文比例综合评分，取值 0—100。分数越高科学影响力越强。`M_INNOV_POT_COMPOSITE` 科学影响力维复用本二维。不另建论文被引或国际合作标记字段。

## 计算逻辑说明

选定产业入集。采用加权平均，二维：论文被引次数（citation_num）/ 国际合作论文比例（作者地址国别 ≥ 2）。

### 第一步：入集

页面年窗、空间（可选）、产业。

机构：`dwd_org_base_info` 按 `org_id` 去重；`reg_status` 含「存续」。产业用 `industry` / `industry_l1_code`，或 `external_id` 对齐 `dwd_org_industry_tags.credit_code`。名称用 `name_cn`。

论文：`dwd_zh_paper` / `dwd_en_paper` 按 `id` 去重；`cover_year_start` 落年窗。作者 `institution` 对齐机构名后继承产业。无命中不剔除产业，只缩小计入的论文。

一行一个产业。本批至少 2 个产业才做极值归一。

### 第二步：两个子项

同一维在**本批产业**内极值归一。分母为 0 的产业该维缺测。

1. **论文被引次数**  
   该产业论文 `dwd_zh_paper_citation.citation_num` 合计。论文级缺测时，作者单位对齐 `dwd_scholar.scholar_org_name_zh` 后用 `citation_nums` 合计。

2. **国际合作论文比例**  
   同一论文作者 `affiliation` 解析出国别，去重国别数 ≥ 2 的论文去重件数 / 该产业论文去重件数。

### 第三步：合成

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
科学影响力=\frac{norm(论文被引)+norm(国际合作比例)}{2}\times 100
$$

缺测维不补 0，剩余维权重重归一。按 `score` 降序排名。

输出：一行一个产业，含两子项原始值、`score`（0—100）、`rank`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 产业科学影响力 | 论文被引次数 | 产业相关论文被引合计。 | SUM(citation_num) | dwd_zh_paper_citation(id, citation_num) — 中文论文被引；dwd_scholar(scholar_id, scholar_org_name_zh, citation_nums) — 学者被引；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 产业科学影响力 | 国际合作论文比例 | 作者地址跨两个及以上国家的论文占比。 | 国际合作论文数 / 论文数 | dwd_zh_author(paper_id, institution, affiliation) — 中文作者单位,地址国别；dwd_en_author(paper_id, institution, affiliation) — 英文作者单位,地址国别；dwd_zh_paper(id, cover_year_start) — 中文论文分母,发表年；dwd_en_paper(id, cover_year_start) — 英文论文分母,发表年 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐
- dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_citation(id, citation_num) — 中文论文被引
- dwd_zh_author(paper_id, institution, affiliation) — 中文作者单位,地址国别
- dwd_en_author(paper_id, institution, affiliation) — 英文作者单位,地址国别
- dwd_scholar(scholar_id, scholar_org_name_zh, citation_nums) — 学者被引

## 待建字段

- 无

## 参考资料

[1]产业科学影响力｜中国医学科学院医学信息研究所｜中央级公益性科研院所基本科研业务费专项（09R0216）｜张玢. 评价学术影响力的引证分析指标研究综述[J]. 医学信息学杂志, 2010, 31(12): 41-46+88.

[2]产业科学影响力｜南京中医药大学图书馆｜江苏省高校哲学社会科学基金项目（2017SJB0503）｜葛敏，刘丽. 科技全球化背景下中国高被引论文国际合作特征分析[J]. 情报探索, 2020(1): 47-54.
