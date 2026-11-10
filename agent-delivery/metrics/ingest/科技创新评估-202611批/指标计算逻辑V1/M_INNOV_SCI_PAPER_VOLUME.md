# 科学论文数量（M_INNOV_SCI_PAPER_VOLUME）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_SCI_PAPER_VOLUME |
| 指标名称 | 科学论文数量 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 科学创造力指标展示 |
| 口径版本 | V2.0-20261108 |
| 更新频率 | monthly |

## 口径定义

统计期内选定领域科学论文的发表数量及其变化，反映科学创造力的产出规模。

## 计算逻辑说明

维内三项极值归一后等权：论文总量 0.40 / 领域论文量 0.35 / 论文增长率 0.25。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 科学论文数量 | 论文总量 | 统计年内中英文论文篇数合计。 | COUNT(DISTINCT dwd_zh_paper.id WHERE cover_year_start=@year) + COUNT(DISTINCT dwd_en_paper.id WHERE cover_year_start=@year) | dwd_zh_paper(id, cover_year_start)；dwd_en_paper(id, cover_year_start) | 无 |
| 科学论文数量 | 领域论文量 | 题名或关键词命中领域词表的论文篇数。 | 论文总量 JOIN dwd_zh_paper_classification ON id，keywords/scope 命中领域词表；英文同构 | dwd_zh_paper_classification(id, keywords, scope)；dwd_en_paper_classification(id, keywords, scope, sub_scope) | 无 |
| 科学论文数量 | 论文增长率 | 相对上一年的总量增速。 | (COUNT(@year) − COUNT(@year−1)) ÷ NULLIF(COUNT(@year−1), 0) × 100% | dwd_zh_paper(id, cover_year_start)；dwd_en_paper(id, cover_year_start) | 无 |

### 计数口径

中英文库 `id` 互不重叠，可直接相加；同一论文在关系表中出现多次时按 `id` 去重。分母为 0 时返回空值而非 0，避免把「无基数」误读为「无增长」。

### 区域口径

评价对象为区域时，需经 `dwd_zh_author.institution` / `dwd_en_author.institution` 对齐 `dwd_org_base_info.name_cn` 后取 `city` 过滤；未匹配的论文不计入，并输出匹配率。

## 源表字段

- dwd_zh_paper(id, zh_name, en_name, cover_year_start, publication_id) — 中文论文去重,题名,发表年
- dwd_en_paper(id, zh_name, en_name, cover_year_start, publication_id) — 英文论文去重,题名,发表年
- dwd_zh_paper_classification(id, keywords, scope) — 中文关键词,学科
- dwd_en_paper_classification(id, keywords, scope, sub_scope) — 英文关键词,学科
- dwd_org_base_info(org_id, name_cn, province, city) — 机构名称对齐,空间

## 待建字段

- 无

## 备注

V1 第 54 行「科学论文数量」口径误写为「学者已发表论文数」，且模块说明挂在科技全域态势。本版按论文篇数重写并归位到科技创新评估。

## 参考资料

[1] 对应 BID §1.1.1.1.4.1.7.1.1「科学论文数量分析」。
