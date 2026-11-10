# 监测异常点识别（M_INNOV_FACTOR_ANOMALY）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_FACTOR_ANOMALY |
| 指标名称 | 监测异常点识别 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.4-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

对选定范围内的科创要素监测时序，识别**异常点**（相对序列中枢的离群期）与**突变点**（邻期跳变过大的期次）。输出命中的期次与标签。

## 计算逻辑说明

### 第一步：确定监测对象与切片

页面传入：`factor_type`（patent / paper / scholar / org）、空间（`province`/`city`，可选）、领域（专利 IPC 前 4 位，可选）、统计频度（默认**年**）。

| factor_type | 实体主键 | 观测值 y_t 定义 |
| --- | --- | --- |
| patent | 切片整体（或按 IPC4 分组） | 统计年 `COUNT(DISTINCT pn)`，年键=`apdt_year` |
| paper | 切片整体（中英文合并） | 统计年 `COUNT(DISTINCT 中文id)+COUNT(DISTINCT 英文id)`，年键=`cover_year_start` |
| scholar | `scholar_id` | 该学者存量 `paper_nums`（无则用 `citation_nums`）；学者无入驻年时，不做逐年序列，改对该批学者截面做离群检测（见第四步备选） |
| org | `org_id` | 统计年该机构专利去重数：`first_applicant_name` 对齐 `name_cn` 后 `COUNT(DISTINCT pn)` |

空间过滤：机构用 `dwd_org_base_info.province/city`；专利落到第一申请人机构所在地（`first_applicant_name`→`name_cn`→省市区）；论文落到作者单位 `institution`→`name_cn`→省市区。无命中不剔除对象，只缩小计入 y_t 的记录集合。

### 第二步：拼装监测时序

对每个监测对象，按年键升序得到序列：

$$
\{(t_i,y_i)\}_{i=1}^{n},\quad t_1<t_2<\cdots<t_n
$$

缺年不插值、不补 0（避免假突变）。

- **新增计数型**（patent、paper、org的年专利申请量/论文量）：首尾年之间缺年补0
- **存量累计型**（scholar的论文存量）：缺年不补0

输出中增加 `series_type` 字段：`count`（新增计数型）或 `stock`（存量累计型）。

有效期数要求：

- **n ≥ 8**：进入第三、四步时序检测；
- **n < 8**：该对象本指标不出时序异常/突变行，仅 `scholar` 类型可走截面备选，并标记 `skip_reason=short_series`；`patent`/`paper`/`org` 类型因补0后 n 已 ≥ 8，不走截面备选。

### 第三步：异常点（默认 MAD）

对序列 \(\{y_i\}\) 计算：

$$
m=\mathrm{median}(y_1,\ldots,y_n)
$$

$$
\mathrm{MAD}=\mathrm{median}\big(|y_1-m|,\ldots,|y_n-m|\big)
$$

若 `MAD=0`（序列几乎常数），直接输出 `label=no_anomaly`，`algo=mad_constant`，**不触发孤立森林**。孤立森林仅在业务显式指定 `algo=iforest` 时启用，不作为 MAD=0 的默认行为。

否则稳健 Z 分数：

$$
z_i=\frac{0.6745\cdot|y_i-m|}{\mathrm{MAD}}
$$

判定规则（默认阈值 `k=3.0`，允许页面动态调整；科研产出监测建议 2.5—3.0）：

$$
\text{anomaly}_i=\mathbf{1}(z_i>k)
$$

输出字段：`period=t_i`，`y=y_i`，`z=z_i`，`label=anomaly`，`algo=mad`。

### 第四步：突变点（邻期跳变）

对相邻有效期（按序列下标，不要求年份连续）计算：

$$
\Delta_i=y_i-y_{i-1},\quad i=2,\ldots,n
$$

**改用局部窗口 MAD**，不再使用全局 MAD：

对每个位置 `i`，取窗口 `[i-w, i+w]`（排除当前点）计算局部MAD，窗口大小 `w` 默认 3 期。窗口内有效点数不足 4 时，用全局 MAD 兜底。

判定条件：
$$
\text{change}_i=\mathbf{1}\big(|\Delta_i|>3\cdot\mathrm{MAD}\big)
$$

输出字段：`period=t_i`（跳变发生后的期末），`delta=Δ_i`，`label=change`。`algo` 字段区分：局部窗口命中为 `mad_delta_local`，全局兜底为 `mad_delta_global`。

同一期可同时命中异常点与突变点，分两行输出，不合并。

### 第五步：备选算法（孤立森林）

仅在以下情形启用，替代第三步 MAD（突变点仍用第四步，MAD 用原序列重算）：

1. 业务参数显式指定 `algo=iforest`

**MAD=0 时不触发孤立森林**。

做法：将 `{y_i}` 视为一维样本，IsolationForest（默认 `n_estimators=100`，`contamination=‘auto’` 或固定 0.05）。`decision_function` 或 `predict=-1` 的期次标为异常，`algo=iforest`。

学者截面备选：对本批学者的 `(paper_nums, citation_nums, h_index)` 三维做孤立森林，输出离群 `scholar_id`，`period=null`，`label=outlier`，`algo=iforest_cross`。

### 第六步：输出

只输出命中行（异常或突变）。一行一个命中：

| 字段                    | 含义                                                         |
| :---------------------- | :----------------------------------------------------------- |
| factor_type / factor_id | 要素类型与主键（切片整体时 factor_id 用切片键）              |
| period                  | 年（截面检测为 null）                                        |
| $y / delta / z$         | 观测值、邻期差、稳健 Z（有则填）                             |
| label                   | `anomaly` / `change` / `outlier` / `no_anomaly`              |
| algo                    | `mad` / `mad_constant` / `mad_delta_local` / `mad_delta_global` / `iforest` / `iforest_cross` |
| detection_type          | `time_series`（时序检测）或 `cross_section`（学者截面检测）  |
| series_type             | `count`（新增计数型）或 `stock`（存量累计型）                |

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 监测异常点识别 | 异常点 | 相对序列中枢的离群期次。 | \($z_i=0.6745\|y_i-m\|/\mathrm{MAD}>3.5$\)；备选孤立森林 | dwd_patent(pn, apdt_year, first_applicant_name, main_classification_ipcr) — 专利年聚合,申请人对齐,领域切片；dwd_zh_paper(id, cover_year_start) — 中文论文年聚合；dwd_en_paper(id, cover_year_start) — 英文论文年聚合；dwd_zh_author(paper_id, institution) — 论文单位对齐；dwd_en_author(paper_id, institution) — 论文单位对齐；dwd_org_base_info(org_id, name_cn, province, city) — 机构入集,空间过滤,名称对齐；dwd_scholar(scholar_id, paper_nums, citation_nums, h_index) — 学者截面备选 | 无 |
| 监测异常点识别 | 突变点 | 邻期绝对跳变过大的期次。 | \($\|\Delta_i\|>3\cdot\mathrm{MAD}$\) | dwd_patent(pn, apdt_year, first_applicant_name) — 专利年序列；dwd_zh_paper(id, cover_year_start) — 中文论文年序列；dwd_en_paper(id, cover_year_start) — 英文论文年序列；dwd_org_base_info(org_id, name_cn, province, city) — 机构切片与对齐 | 无 |

## 源表字段

- dwd_patent(pn, apdt_year, first_applicant_name, main_classification_ipcr) — 专利去重,申请年聚合,申请人名称对齐,IPC领域切片
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年聚合
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年聚合
- dwd_zh_author(paper_id, institution) — 中文作者单位,挂论文与机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,挂论文与机构对齐
- dwd_org_base_info(org_id, name_cn, province, city, org_type, reg_status) — 机构主键,名称对齐,空间过滤,入集
- dwd_scholar(scholar_id, paper_nums, citation_nums, h_index, status) — 学者存量,截面离群备选

## 待建字段

- 无

## 参考资料

[1] 统计学习（聚类/预测）|Stanford University|James G, Witten D, Hastie T, Tibshirani R. An Introduction to Statistical Learning[M]. New York: Springer, 2013.
[2] 稳健离群检测（MAD）|Leys C, et al. Detecting outliers: Do not use standard deviation around the mean, use absolute deviation around the median[J]. Journal of Experimental Social Psychology, 2013, 49(4): 764-766.
