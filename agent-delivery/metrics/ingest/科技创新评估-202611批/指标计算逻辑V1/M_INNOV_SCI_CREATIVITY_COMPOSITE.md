# 科学创造力综合评估（M_INNOV_SCI_CREATIVITY_COMPOSITE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_SCI_CREATIVITY_COMPOSITE |
| 指标名称 | 科学创造力综合评估 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 科学创造力指标展示 |
| 口径版本 | V2.0-20261108 |
| 更新频率 | 待确认（pending） |

## 口径定义

将科学论文数量、科学网络中心性、科学研究前沿性与趋势预测四维按权重合成的科学创造力评分。对象=选定领域或区域，取值 0—100。

## 计算逻辑说明

### 第一步：入集

领域论文按题名或关键词命中领域词表入集（`dwd_zh_paper` / `dwd_en_paper` 的 `zh_name`、`en_name`，配合 `dwd_zh_paper_classification.keywords`、`dwd_en_paper_classification.keywords`）。区域口径改按 `dwd_zh_author.institution` / `dwd_en_author.institution` 对齐 `dwd_org_base_info` 的 `city` 过滤。

### 第二步：四维取值

| 维度 | 指标ID | 默认权重 |
| --- | --- | --- |
| 科学论文数量 | M_INNOV_SCI_PAPER_VOLUME | 0.25 |
| 科学网络中心性 | M_INNOV_SCI_CENTRALITY | 0.25 |
| 科学研究前沿性 | M_INNOV_SCI_FRONTIER | 0.25 |
| 科学创造力趋势预测 | M_INNOV_SCI_FORECAST | 0.25 |

### 第三步：合成

$$
score=\sum_{i=1}^{4} w_i\cdot norm(x_i)\times 100,\qquad
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

权重默认值如上，页面支持用户自定义权重，改写后同级重新归一，权重落配置表不硬编码。趋势预测维度在序列不足 8 个期次时不计入，其余三维按比例重新归一。

## 源表字段

- dwd_zh_paper(id, zh_name, en_name, cover_year_start, publication_id) — 中文论文去重,题名,发表年
- dwd_en_paper(id, zh_name, en_name, cover_year_start, publication_id) — 英文论文去重,题名,发表年
- dwd_zh_paper_classification(id, keywords, scope) — 中文关键词,学科
- dwd_en_paper_classification(id, keywords, scope, sub_scope) — 英文关键词,学科
- dwd_zh_author(paper_id, author_id, zh_name, institution, affiliation) — 中文作者,单位,地址
- dwd_en_author(paper_id, author_id, zh_name, institution, affiliation) — 英文作者,单位,地址

## 待建字段

- 无

## 备注

本节点为 V2 新增（V1 无科学创造力综合评估行）。四维权重为初拟值，待专家赋权确认（Q-MO-DS07-01）。

## 参考资料

[1] 对应 BID §1.1.1.1.4.1.7.1「科学创造力指标展示」。
