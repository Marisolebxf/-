# 技术市场潜力（M_INNOV_TINN_MARKET）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_TINN_MARKET |
| 指标名称 | 技术市场潜力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 技术创新力指标展示 |
| 口径版本 | V1.5-20260901 |
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

`legal_events` 为 JSON 数组，逐条取 `code`、`event`（及 details 文本）做关键词匹配；`date` 落年窗才计入。

1. **转让**  
   该领域专利命中 `dwd_patent_transfer` 的去重件数 / 专利去重件数。`transfer_effective_date` 落窗；无转移行当 0。

2. **许可**  
   `legal_events` 含「许可」或 license，且不含「开放许可」的专利去重件数 / 专利去重件数。

3. **诉讼**  
   `legal_events` 含「诉讼」「无效宣告」「无效」「invalidation」的专利去重件数 / 专利去重件数。

4. **质押**  
   `legal_events` 含「质押」或 pledge 的专利去重件数 / 专利去重件数。

5. **开放许可**  
   `legal_events` 含「开放许可」的专利去重件数 / 专利去重件数。

### 第三步：合成

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
技术市场潜力=\frac{norm(转让)+norm(许可)+norm(诉讼)+norm(质押)+norm(开放许可)}{5}\times 100
$$

缺测维不补 0，剩余维权重重归一。按 `score` 降序排名。

输出：一行一个 IPC4，含五子项原始值、`score`（0—100）、`rank`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 技术市场潜力 | 转让 | 发生权利转移的专利占比。 | 转移专利数 / 专利数 | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_patent(pn, main_classification_ipcr, apdt_year) — 专利分母,IPC领域 | 无 |
| 技术市场潜力 | 许可 | 实施许可（不含开放许可）的专利占比。 | 许可专利数 / 专利数 | dwd_patent_legal(pn, legal_events) — 法律事件 | 无 |
| 技术市场潜力 | 诉讼 | 涉及诉讼或无效宣告的专利占比。 | 诉讼专利数 / 专利数 | dwd_patent_legal(pn, legal_events) — 法律事件 | 无 |
| 技术市场潜力 | 质押 | 发生质押登记的专利占比。 | 质押专利数 / 专利数 | dwd_patent_legal(pn, legal_events) — 法律事件 | 无 |
| 技术市场潜力 | 开放许可 | 声明开放许可的专利占比。 | 开放许可专利数 / 专利数 | dwd_patent_legal(pn, legal_events) — 法律事件 | 无 |

## 源表字段

- dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日
- dwd_patent_legal(pn, legal_events) — 法律事件（许可,诉讼,质押,开放许可）
- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1]技术市场潜力｜大连理工大学｜国家自然科学基金项目（71473028）｜栾春娟，程昉. 技术的市场潜力测度与预测——基于技术颠覆潜力与技术成熟度综合指标[J]. 科学学研究, 2016, 34(12): 1761-1768+1816.
