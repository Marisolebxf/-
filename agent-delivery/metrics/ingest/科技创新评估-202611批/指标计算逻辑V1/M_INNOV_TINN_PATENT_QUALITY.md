# 专利质量（M_INNOV_TINN_PATENT_QUALITY）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_TINN_PATENT_QUALITY |
| 指标名称 | 专利质量 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 技术创新力指标展示 |
| 口径版本 | V2.0-20261108 |
| 更新频率 | 待确认（pending） |

## 口径定义

选定技术领域的专利质量。从家族规模、权利要求数、被引次数、技术宽度、法律状态稳定性综合评分，取值 0—100。分数越高专利质量越高。`M_INNOV_TINN_COMPOSITE` 专利质量维复用本五级。

## 计算逻辑说明

按 IPC 前 4 位入集技术领域。采用加权平均，五维：家族规模（简单同族）/ 权利要求数（claims 项数）/ 被引次数（cited_by_nums）/ 技术宽度（IPC4 去重数）/ 法律状态稳定性（授权且未失效）。

### 第一步：入集

页面年窗、空间（可选）、领域（可选，IPC 前 4 位或关键词落到 `main_classification_ipcr`）。

专利：`dwd_patent` 按 `pn` 去重；`apdt_year` 落年窗；领域键 = `main_classification_ipcr` 前 4 位。空间：`first_applicant_name` 对齐 `dwd_org_base_info.name_cn` 后取 `province`/`city`。

一行一个 IPC4。本批至少 2 个领域才做极值归一。

### 第二步：五个子项

同一维在**本批领域**内极值归一。分母为 0 的领域该维缺测。

1. **家族规模**  
   按简单同族去重计算：族成员数(f) = COUNT(DISTINCT pn) FROM dwd_patent_family WHERE simple_family_number = f（含本件）；若该表为每族一行，则族成员数 = JSON_LENGTH(simple_family_pn)。同族规模 = Σ族成员数(f) ÷ COUNT(DISTINCT simple_family_number)。

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

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 专利质量 | 家族规模 | 领域专利平均同族成员数。 | 族成员数合计 ÷ 族数（按 simple_family_number 去重） | dwd_patent_family(pn, simple_family_number, simple_family_pn, simple_family) — 简单同族ID,同族成员文献号,成员序号；dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,领域,申请年 | 无 |
| 专利质量 | 权利要求数 | 领域专利平均权利要求项数。 | **暂不可算**：`dwd_patent` 无 claims 字段，`dwd_patent_claim` 仅有整段原文 | dwd_patent_claim(pn, lang, original_text) — 仅有原文，无条数字段 | dwd_patent_claim.claim_count — 权利要求条数 |
| 专利质量 | 被引次数 | 领域专利被后续专利引用的总次数。 | SUM(cited_by_nums) | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent(pn, main_classification_ipcr, apdt_year) — 专利去重,IPC领域 | 无 |
| 专利质量 | 技术宽度 | 单件专利覆盖的 IPC 小类广度。 | 每件专利 IPC4 去重数合计 / 专利数 | dwd_patent(pn, main_classification_ipcr, further_classification_ipcr, apdt_year) — 主分类,附加分类 | 无 |
| 专利质量 | 法律状态稳定性 | 仍处于授权/有效且未失效的专利占比。 | 稳定专利数 / 专利数 | dwd_patent_legal(pn, status, expiration_year) — 专利状态,到期年 | 无 |

## 源表字段

- dwd_patent(pn, first_applicant_name, main_classification_ipcr, further_classification_ipcr, apdt_year) — 专利去重,申请人对齐,主分类,附加分类,权利要求,同族,申请年
- dwd_patent_cited(pn, cited_by_nums) — 专利被引次数
- dwd_patent_legal(pn, status, expiration_year) — 专利状态,到期年
- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

- `dwd_patent_claim.claim_count` — 权利要求条数（现表仅有 original_text 整段原文，需结构化）
- `dwd_patent_legal.legal_event_code` — 许可/诉讼/质押/开放许可四类事件的结构化码值（现仅有描述文本）

## 备注

V2.3-20261108 纠正：原公式取 `dwd_patent.other_Versions` 并「空值按 1 计」。该字段语义为「其他版本」，不含本件，数组非空时只数了其他成员，每件系统性少算 1；改用 `dwd_patent_family` 的简单同族口径（`simple_family_number` / `simple_family_pn`），分母按族去重。

V2.2-20261108：① 原引用的 `dwd_patent.claims` 在数据字典中不存在，权利要求数改为待建字段；② 许可/诉讼/质押/开放许可四项按业务确认视为**无数据源**，指标字段保留、不参与合成，缺测维按剩余权重归一；③ 转让仍按 `dwd_patent_transfer` 计算，并用 `legal_events` 中 TA01/TR01/PC/PC1 做交叉校验；④ 专利授权量按授权公布年 `pbdt_year` 过滤。

## 参考资料

[1] 专利质量|华中科技大学|—|万小丽, 朱雪忠. 专利价值的评估指标体系及模糊综合评价[J]. 科研管理, 2008, 29(2): 185-191.

[2]专利质量｜上海市统计局｜专利申请量与专利授权量｜2009-11-02｜https://tjj.sh.gov.cn/zcjd/20091102/0014-86183.html.

[3]专利质量｜华中科技大学｜国家自然科学基金项目（70633003）｜万小丽，朱雪忠. 国际视野下专利质量指标研究的现状与趋势[J]. 情报杂志, 2009, 28(7): 49-54.
