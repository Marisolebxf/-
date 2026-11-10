# 技术市场潜力（M_INNOV_TINN_MARKET）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_TINN_MARKET |
| 指标名称 | 技术市场潜力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 技术创新力指标展示 |
| 口径版本 | V2.0-20261108 |
| 更新频率 | 待确认（pending） |

## 口径定义

选定技术领域的市场潜力。从转让、许可、诉讼、质押、开放许可综合评分，取值 0—100。分数越高市场活动越活跃、潜力越大。`M_INNOV_TINN_COMPOSITE` 技术市场潜力维复用本五级。不另建许可/诉讼/质押专表。

## 计算逻辑说明

按 IPC 前 4 位入集技术领域。采用加权平均，五维：转让（转移专利/专利）/ 许可 / 诉讼 / 质押 / 开放许可（后四项由 `legal_events` 解析）。

### 第一步：入集

页面年窗、空间（可选）、领域（可选，IPC 前 4 位或关键词落到 `main_classification_ipcr`）。

专利：`dwd_patent` 按 `pn` 去重；`apdt_year` 落年窗；领域键 = `main_classification_ipcr` 前 4 位。空间：`first_applicant_name` 对齐 `dwd_org_base_info.name_cn` 后取 `province`/`city`。

一行一个 IPC4。本批至少 2 个领域才做极值归一。

### 第二步：五个子项

同一维在**本批领域**内极值归一。分母为 0 的领域该维缺测。无命中当 0，不另建字段。

`legal_events` 为 JSON 数组，每个元素含 `code`、`date`、`description_en`、`description_original`；按**码值优先 + 英文关键词补漏**双轨匹配，`date` 落年窗才计入，同一专利命中多条按 `pn` 去重。完整码表见《专利法律事件码表.md》。

1. **转让**  
   该领域专利命中 `dwd_patent_transfer` 的去重件数 / 专利去重件数。`transfer_effective_date` 落窗；无转移行当 0。码值 `TA01`/`TR01`/`PC`/`PC1` 或关键词 TRANSFER OF PATENT、ASSIGNMENT 作交叉校验。

2. **许可**  
   本期不计算：视为无数据源，指标字段保留，不参与合成。

3. **诉讼**  
   本期不计算：视为无数据源，指标字段保留，不参与合成。

4. **质押**  
   本期不计算：视为无数据源，指标字段保留，不参与合成。

5. **开放许可**  
   本期不计算：视为无数据源，指标字段保留，不参与合成。

### 第三步：合成

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
技术市场潜力=norm(转让)\times 100
$$

缺测维不补 0，剩余维权重重归一。按 `score` 降序排名。

输出：一行一个 IPC4，含五子项原始值、`score`（0—100）、`rank`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 技术市场潜力 | 转让 | 发生权利转移的专利占比。 | 转移专利数 / 专利数；与 legal_events 中 TA01/TR01/PC/PC1 交叉校验 | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_patent_legal(pn, legal_events) — 交叉校验；dwd_patent(pn, main_classification_ipcr, apdt_year) — 专利分母,IPC领域 | 无 |
| 技术市场潜力 | 许可 | 实施许可（不含开放许可）的专利占比。 | 本期不计算：无结构化事件码 | 无 | dwd_patent_legal.legal_event_code — 许可事件码值 |
| 技术市场潜力 | 诉讼 | 涉及诉讼或无效宣告的专利占比。 | 本期不计算：无结构化事件码 | 无 | dwd_patent_legal.legal_event_code — 诉讼事件码值 |
| 技术市场潜力 | 质押 | 发生质押登记的专利占比。 | 本期不计算：无结构化事件码 | 无 | dwd_patent_legal.legal_event_code — 质押事件码值 |
| 技术市场潜力 | 开放许可 | 声明开放许可的专利占比。 | 本期不计算：无结构化事件码 | 无 | dwd_patent_legal.legal_event_code — 开放许可事件码值 |

## 源表字段

- dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日
- dwd_patent_legal(pn, legal_events) — 法律事件（许可,诉讼,质押,开放许可）
- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

- `dwd_patent_legal.legal_event_code` — 许可/诉讼/质押/开放许可四类事件的结构化码值（现仅有描述文本）

## 备注

V2.2-20261108：① 原引用的 `dwd_patent.claims` 在数据字典中不存在，权利要求数改为待建字段；② 许可/诉讼/质押/开放许可四项按业务确认视为**无数据源**，指标字段保留、不参与合成，缺测维按剩余权重归一；③ 转让仍按 `dwd_patent_transfer` 计算，并用 `legal_events` 中 TA01/TR01/PC/PC1 做交叉校验；④ 专利授权量按授权公布年 `pbdt_year` 过滤。

## 参考资料

[1]技术市场潜力｜大连理工大学｜国家自然科学基金项目（71473028）｜栾春娟，程昉. 技术的市场潜力测度与预测——基于技术颠覆潜力与技术成熟度综合指标[J]. 科学学研究, 2016, 34(12): 1761-1768+1816.
