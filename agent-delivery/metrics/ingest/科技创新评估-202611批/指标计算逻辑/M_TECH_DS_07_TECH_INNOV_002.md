# 专利质量评估（M_TECH_DS_07_TECH_INNOV_002）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_TECH_DS_07_TECH_INNOV_002 |
| 指标名称 | 专利质量评估 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 技术创新力指标展示 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

选定技术领域的专利质量。从家族规模、权利要求数、被引次数、技术宽度、法律状态稳定性综合评分，取值 0—100。分数越高专利质量越高。与 `M_INNOV_TINN_PATENT_QUALITY` 同一五维，`M_INNOV_TINN_COMPOSITE` 专利质量维复用本口径。

## 计算逻辑说明

按 IPC 前 4 位入集技术领域。采用加权平均，五维：家族规模（other_Versions）/ 权利要求数（claims 项数）/ 被引次数（cited_by_nums）/ 技术宽度（IPC4 去重数）/ 法律状态稳定性（授权且未失效）。

### 第一步：入集

页面年窗、空间（可选）、领域（可选，IPC 前 4 位或关键词落到 `main_classification_ipcr`）。

专利：`dwd_patent` 按 `pn` 去重；`apdt_year` 落年窗；领域键 = `main_classification_ipcr` 前 4 位。空间：`first_applicant_name` 对齐 `dwd_org_base_info.name_cn` 后取 `province`/`city`。

一行一个 IPC4。本批至少 2 个领域才做极值归一。

### 第二步：五个子项

同一维在**本批领域**内极值归一。分母为 0 的领域该维缺测。

1. **家族规模**  
   该领域专利 `other_Versions` 数组成员数合计 / 专利去重件数。空数组或空值该件记 1。

2. **权利要求数**  
   该领域专利 `claims` 项数合计 / 专利去重件数。`claims` 为 JSON 数组取长度，为文本按编号项计数；空记 0。

3. **被引次数**  
   该领域专利命中 `dwd_patent_cited` 的 `cited_by_nums` 合计。无引用行当 0。

4. **技术宽度**  
   每件专利 IPC4 去重数 = `{main_classification_ipcr 前 4 位}` ∪ `{further_classification_ipcr 各条前 4 位}` 的个数；领域值 = 该去重数合计 / 专利去重件数。附加分类空则该件记 1。

5. **法律状态稳定性**  
   命中 `dwd_patent_legal` 且 `status` 含「授权」或「有效」、不含「无效」「终止」「失效」「撤回」「放弃」，且 `expiration_year` 空或 ≥ 统计年的专利去重件数 / 专利去重件数。无法律状态行不当稳定。

### 第三步：合成

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
专利质量=\frac{norm(家族规模)+norm(权利要求数)+norm(被引)+norm(技术宽度)+norm(法律状态稳定性)}{5}\times 100
$$

缺测维不补 0，剩余维权重重归一。按 `score` 降序排名。

输出：一行一个 IPC4，含五子项原始值、`score`（0—100）、`rank`。

| 一级指标 | 二级指标       | 指标说明                            | 计算公式                          | 源表字段                                                     | 待建字段 |
| -------- | -------------- | ----------------------------------- | --------------------------------- | ------------------------------------------------------------ | -------- |
| 专利质量 | 家族规模       | 领域专利平均同族成员数。            | 同族成员数合计 / 专利数           | dwd_patent(pn, main_classification_ipcr, other_Versions, apdt_year) — 同族专利,IPC领域 | 无       |
| 专利质量 | 权利要求数     | 领域专利平均权利要求项数。          | 权利要求项数合计 / 专利数         | dwd_patent(pn, main_classification_ipcr, claims, apdt_year) — 权利要求,IPC领域 | 无       |
| 专利质量 | 被引次数       | 领域专利被后续专利引用的总次数。    | SUM(cited_by_nums)                | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent(pn, main_classification_ipcr, apdt_year) — 专利去重,IPC领域 | 无       |
| 专利质量 | 技术宽度       | 单件专利覆盖的 IPC 小类广度。       | 每件专利 IPC4 去重数合计 / 专利数 | dwd_patent(pn, main_classification_ipcr, further_classification_ipcr, apdt_year) — 主分类,附加分类 | 无       |
| 专利质量 | 法律状态稳定性 | 仍处于授权/有效且未失效的专利占比。 | 稳定专利数 / 专利数               | dwd_patent_legal(pn, status, expiration_year) — 专利状态,到期年 | 无       |

## 源表字段

- dwd_patent(pn, first_applicant_name, main_classification_ipcr, further_classification_ipcr, claims, other_Versions, apdt_year) — 专利去重,申请人对齐,主分类,附加分类,权利要求,同族,申请年
- dwd_patent_cited(pn, cited_by_nums) — 专利被引次数
- dwd_patent_legal(pn, status, expiration_year) — 专利状态,到期年
- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1] 专利价值评估|华中科技大学|—|万小丽, 朱雪忠. 专利价值的评估指标体系及模糊综合评价[J]. 科研管理, 2008, 29(2): 185-191.
