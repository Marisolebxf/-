# 科学研究前沿性（M_INNOV_SCI_FRONTIER）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_SCI_FRONTIER |
| 指标名称 | 科学研究前沿性 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 科学创造力指标展示 |
| 口径版本 | V1.7-20260902 |
| 更新频率 | 待确认（pending） |

## 口径定义

识别选定领域内的研究前沿和热点方向，并给出前沿主题的时间演变与空间分布。对象=领域主题（共被引簇 / 关键词）。

## 计算逻辑说明

按题名关键词入集领域论文。先搭两张无向加权网：共被引网（前沿）/ 关键词共现网（热点）。再读时间演变与空间分布。引文从现表列表字段现算，不用作者关系表，不另建 citation_network。本指标不建作者合作网（合作网见 `M_INNOV_SCI_CENTRALITY`）。

### 第一步：入集

论文按 `id` 去重。领域：题名关键词落到 `dwd_zh_paper`/`dwd_en_paper` 的 `zh_name`/`en_name`。关键词袋优先取 `dwd_zh_paper_classification`/`dwd_en_paper_classification.keywords`，袋空则从题名切词。年键=`cover_year_start`。

被引次数：中文 `dwd_zh_paper_citation.citation_num`，英文 `dwd_en_paper_reference.citation_count`。被引列表：中文 `citation_id_list`，英文 `cited_reference_id_list`，按 JSON 的值展开为被引论文 `id`（格式 `{序号: 被引id}`，只取 value）。施引论文 = 该行主键 `id`。

作者单位用 `dwd_zh_author`/`dwd_en_author.institution`，对齐 `dwd_org_base_info.name_cn` 后取 `city`/`province`；对齐不上则从 `affiliation` 文本取城名。

### 第二步：搭两张网

**网 A：共被引网（给研究前沿用）**

- 节点：本批被引次数 ≥ P70 的领域论文，节点键=`论文id`。达不到 P70 的论文不进网。
- 边：无向。对每一篇施引论文 C，把它的被引列表与高被引节点集求交，得集合 S。S 中每一对无序论文 `(i,j)` 共被引次数 +1。边权 `w(i,j)` = 同时引用 i 和 j 的施引论文去重数。
- 留边：`w≥2` 才连边。`w=1` 视为偶然同引，不连。
- 不成网：某施引论文的 S 少于 2 个节点，该篇不产生边。孤立高被引点不成簇，不进前沿清单。
- 成簇：在留边后的无向图上取连通分量，一分量 = 一个前沿簇。不跑 Louvain，不跑最短路。

例：论文 C 的被引列表含 A、B、D，且 A、B 在高被引集、D 不在，则只给边 `(A,B)` 加 1。另有论文 E 也同时引用 A、B，则 `w(A,B)=2`，连边。

**网 B：关键词共现网（给热点方向用）**

- 节点：本批领域论文关键词去重，节点键=`关键词`（中英文名归一到同一词）。
- 边：无向。同一篇论文关键词袋里每对词 `(u,v)` 共现次数 +1。边权 = 同时含这两词的论文去重数。
- 留边：`w≥2`。词频低于本批中位数的节点删掉，再删因此变成孤立的边。
- 核心热点：留边后度数 ≥ 1 的节点（至少与另一高频词共现过）。

两张网都在入集结果上现算，不落中间表。

### 第三步：四个子项

1. **研究前沿**  
   读网 A 的连通分量。簇名 = 簇内论文关键词频次最高的 2–3 个词。簇强度 = 簇内论文数 × 簇内总被引。按簇强度降序输出前沿清单。

2. **热点方向**  
   读网 B。词频 = 含该词的论文去重数。核心热点按词频降序输出。

3. **时间演变**  
   对每个前沿簇名 / 热点词，按年统计命中论文数。近窗 = 近 3 年均值，基线 = 前 5 年均值。增幅 = (近窗 − 基线) / max(基线, 1)。同时输出逐年件数。

4. **空间分布**  
   对每个前沿簇 / 热点词，按作者单位所在城统计命中论文去重件数，除以该主题论文总数，得城份额。机构去重数一并输出。

四维分别输出。页面要综合分时，簇强度、热点词频、增幅、头部城份额四项在本批主题内极值归一后等权 ×100。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 科学研究前沿性 | 研究前沿 | 高被引论文为点、同引≥2 连边后的连通簇。 | 节点=被引≥P70 的论文；边权=共同施引数，w≥2 留边；连通分量；簇强度=簇内论文数×总被引 | dwd_zh_paper_citation(id, citation_num, citation_id_list) — 中文被引次数,被引列表；dwd_en_paper_reference(id, citation_count, cited_reference_id_list) — 英文被引次数,被引列表；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词 | 无 |
| 科学研究前沿性 | 热点方向 | 关键词为点、同篇共现≥2 连边后的高频词。 | 节点=关键词；边权=共现论文数，w≥2 留边；词频=COUNT(DISTINCT 论文id) | dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词 | 无 |
| 科学研究前沿性 | 时间演变 | 主题词近窗相对基线的增幅。 | (近3年均值-前5年均值)/max(前5年均值,1) | dwd_zh_paper(id, cover_year_start) — 中文发表年；dwd_en_paper(id, cover_year_start) — 英文发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词 | 无 |
| 科学研究前沿性 | 空间分布 | 主题论文在各城的份额。 | COUNT(该城论文)/COUNT(主题论文) | dwd_zh_author(paper_id, institution, affiliation) — 中文作者单位,地址；dwd_en_author(paper_id, institution, affiliation) — 英文作者单位,地址；dwd_org_base_info(org_id, name_cn, city, province) — 名称对齐,城市 | 无 |

## 源表字段

- dwd_zh_paper(id, zh_name, en_name, cover_year_start) — 中文论文去重,题名入集,发表年
- dwd_en_paper(id, zh_name, en_name, cover_year_start) — 英文论文去重,题名入集,发表年
- dwd_zh_paper_classification(id, keywords) — 中文论文关键词
- dwd_en_paper_classification(id, keywords) — 英文论文关键词
- dwd_zh_paper_citation(id, citation_num, citation_id_list) — 中文被引次数,被引论文列表
- dwd_en_paper_reference(id, citation_count, cited_reference_id_list) — 英文被引次数,被引论文列表
- dwd_zh_author(paper_id, institution, affiliation) — 中文作者单位,地址
- dwd_en_author(paper_id, institution, affiliation) — 英文作者单位,地址
- dwd_org_base_info(org_id, name_cn, city, province) — 机构名称对齐,城市

## 待建字段

- 无

## 参考资料

[1] 研究前沿识别|Drexel University|—|Chen C. CiteSpace II: Detecting and visualizing emerging trends and transient patterns in scientific literature[J]. Journal of the American Society for Information Science and Technology, 2006, 57(3): 359-377.
