# 研究领域重叠度（M_INNOV_RES_OVERLAP）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_RES_OVERLAP |
| 指标名称 | 研究领域重叠度 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 研究领域分析 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

衡量两家企业在研究领域上的重叠程度，取值 0—1。对象=企业对。集合从专利 IPC、专利/论文关键词、所属学者现表抽取，不另建关键词集合。重叠度越高，两家企业研究领域越接近。`M_INNOV_RES_GRADE`、`M_INNOV_RES_CI_LEVEL` 复用本合成值。

## 计算逻辑说明

选定企业入集。采用加权平均，三维：IPC 重叠 / 关键词重叠 / 学者重叠（均为 Jaccard）。

### 第一步：入集

页面年窗、空间（可选）。用户选择至少 2 家企业（`org_id`）。

机构：`dwd_org_base_info` 按 `org_id` 去重；`reg_status` 含「存续」。名称用 `name_cn`。

专利：`dwd_patent` 按 `pn` 去重；`apdt_year` 落年窗；`first_applicant_name` 对齐机构名。  
论文：`dwd_zh_paper` / `dwd_en_paper` 按 `id` 去重；`cover_year_start` 落年窗；作者 `institution` 对齐机构名。  
学者：`dwd_scholar.scholar_org_name_zh` / `scholar_org_name_en` 按分号、顿号切开后对齐机构名。

不用机构-专利 / 作者-机构关系表。每家企业至少一个非空集合才与其他企业成对。一行一个无序企业对（\(i<j\)）。

### 第二步：三个集合

词切分：小写去空白，长度 ≥ 2。

1. **IPC 集合**  
   `main_classification_ipcr` 前 4 位，并与 `further_classification_ipcr` 各条前 4 位取并。

2. **关键词集合**  
   专利 `keywords`；中文论文 `dwd_zh_paper_classification.keywords`；英文论文 `dwd_en_paper_classification.keywords` 的 `ch_name`/`en_name`。

3. **学者集合**  
   对齐到该企业的 `scholar_id` 去重。

### 第三步：Jaccard 与合成

$$
J(A,B)=\frac{|A\cap B|}{|A\cup B|}\qquad(\text{并集为空则该维缺测})
$$

默认三维等权，页面可改，须 \(\sum w=1\)。缺测维不补 0，剩余维权重重归一。

$$
重叠度=w_1\cdot J_{\mathrm{IPC}}+w_2\cdot J_{\mathrm{关键词}}+w_3\cdot J_{\mathrm{学者}}
$$

输出：一行一个企业对，含三集合大小、三 \(J\)、`overlap`（0—1）。可供矩阵/热力可视化。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 研究领域重叠度 | IPC重叠 | 两家企业专利 IPC4 集合的 Jaccard。 | \|A∩B\| / \|A∪B\| | dwd_patent(pn, first_applicant_name, main_classification_ipcr, further_classification_ipcr, apdt_year) — 申请人对齐,主分类,附加分类,申请年；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 企业入集,名称对齐 | 无 |
| 研究领域重叠度 | 关键词重叠 | 两家企业专利与论文关键词集合的 Jaccard。 | \|A∩B\| / \|A∪B\| | dwd_patent(pn, keywords, first_applicant_name, apdt_year) — 专利关键词,申请人对齐；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 研究领域重叠度 | 学者重叠 | 两家企业所属学者集合的 Jaccard。 | \|A∩B\| / \|A∪B\| | dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 企业入集,名称对齐,空间过滤
- dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, further_classification_ipcr, apdt_year) — 专利去重,关键词,申请人对齐,主分类,附加分类,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_classification(id, keywords) — 中文论文关键词
- dwd_en_paper_classification(id, keywords) — 英文论文关键词
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名

## 待建字段

- 无

## 参考资料

[1]研究领域重叠度｜浙江工商职业技术学院，首都经济贸易大学工商管理学院｜国家社会科学基金重大项目（19ZDA077）；浙江省哲社规划项目（15NDJC162YB）｜朱正浩，戚聿东，赵志栋. 技术生态位对企业绩效的影响研究：技术宽度和技术重叠度整合视角[J]. 南方经济, 2021(4): 86-105. DOI: 10.19592/j.cnki.scje.380866.

