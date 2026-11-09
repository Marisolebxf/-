# 技术产品成熟度（M_INNOV_POT_MATURITY）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_POT_MATURITY |
| 指标名称 | 技术产品成熟度 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 产业发展潜力指标展示 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

按授权比例、发明占比、市场渗透综合评分，取值 0—100。分数越高越成熟。本指标对象为 IPC 前 4 位；`M_INNOV_POT_COMPOSITE` 复用同一三维时按选定产业汇总。不另建生命周期阶段或渗透率字段。

## 计算逻辑说明

采用加权平均，三维：授权比例（授权专利/专利）/ 发明占比（发明专利/专利）/ 市场渗透（转移专利/专利）。

### 第一步：入集

页面年窗、空间（可选）、领域（可选，IPC 前 4 位或关键词落到 `main_classification_ipcr`）。

专利：`dwd_patent` 按 `pn` 去重；`apdt_year` 落年窗；领域键 = `main_classification_ipcr` 前 4 位。空间或产业：`first_applicant_name` 对齐 `dwd_org_base_info.name_cn` 后取 `province`/`city`，或 `industry` / `dwd_org_industry_tags.industry_code`。无命中不剔除领域，只缩小计入的专利。

一行一个 IPC4。本批至少 2 个领域才做极值归一。

### 第二步：三个子项

同一维在**本批领域**内极值归一。分母为 0 的领域该维缺测。

1. **授权比例**  
   `granted_number` 非空的专利去重件数 / 该领域专利去重件数。

2. **发明占比**  
   `kind` 为 A、B 或文本含「发明」的专利去重件数 / 该领域专利去重件数。

3. **市场渗透**  
   该领域专利命中 `dwd_patent_transfer` 的去重件数 / 该领域专利去重件数。`transfer_effective_date` 落窗；无转移行当 0。

生命周期阶段只作展示标签，由三子项组合：授权比例与发明占比均 ≥ 本批中位数且近窗专利增速 < 0 记「成熟」；近窗增速 ≥ 1 记「成长」；授权比例 < 本批 P30 记「导入」；近窗件数相对基线下降且授权比例 ≥ 中位数记「衰退」；其余「成长」。

### 第三步：合成

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
技术产品成熟度=\frac{norm(授权比例)+norm(发明占比)+norm(市场渗透)}{3}\times 100
$$

缺测维不补 0，剩余维权重重归一。

输出：一行一个 IPC4，含三子项原始值、`maturity_score`（0—100）、阶段标签。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 技术产品成熟度 | 授权比例 | 授权专利占全部专利比。 | 授权专利数 / 专利数 | dwd_patent(pn, main_classification_ipcr, granted_number, apdt_year) — IPC领域,授权号,申请年 | 无 |
| 技术产品成熟度 | 发明占比 | 发明专利占全部专利比。 | 发明专利数 / 专利数 | dwd_patent(pn, main_classification_ipcr, kind, apdt_year) — IPC领域,申请类型,申请年 | 无 |
| 技术产品成熟度 | 市场渗透 | 发生转移的专利占比。 | 转移专利数 / 专利数 | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_patent(pn, main_classification_ipcr, apdt_year) — 专利分母,IPC领域 | 无 |

## 源表字段

- dwd_patent(pn, kind, granted_number, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请类型,授权号,申请人对齐,IPC领域,申请年
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日
- dwd_org_base_info(org_id, name_cn, external_id, industry, city, province, reg_status) — 名称对齐,空间过滤,产业切片
- dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签

## 待建字段

- 无

## 参考资料

[1] 技术产品成熟度｜大连理工大学｜国家自然科学基金项目（71473028）｜栾春娟，程昉. 技术的市场潜力测度与预测——基于技术颠覆潜力与技术成熟度综合指标[J]. 科学学研究, 2016, 34(12): 1761-1768+1816.
