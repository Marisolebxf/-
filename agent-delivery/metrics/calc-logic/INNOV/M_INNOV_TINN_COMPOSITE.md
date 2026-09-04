# 技术创新力综合评估（M_INNOV_TINN_COMPOSITE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_TINN_COMPOSITE |
| 指标名称 | 技术创新力综合评估 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

将规模（专利数量）、质量（专利质量）、潜力（技术市场潜力）按自定义权重计算的技术创新力综合得分与排名。对象=选定领域（IPC 前 4 位），取值 0—100。分数越高技术创新力越强。

## 计算逻辑说明

选定领域入集。采用加权平均，三维：专利数量（专利申请量/专利授权量） / 专利质量（家族规模/权利要求数/被引次数/技术宽度/法律状态稳定性） / 技术市场潜力（转让/许可/诉讼/质押/开放许可）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 专利数量（规模） |  | 从专利申请量和专利授权量评估专利规模。 | 维内两项极值归一后等权。 | dwd_patent(pn, main_classification_ipcr, granted_number, apdt_year) — IPC领域,授权号,申请年 |
| 专利数量（规模） | 专利申请量 | 统计期专利申请去重件数。 | COUNT(DISTINCT pn) | dwd_patent(pn, main_classification_ipcr, apdt_year) — IPC领域,申请年 |
| 专利数量（规模） | 专利授权量 | 统计期授权专利去重件数。 | COUNT(DISTINCT pn WHERE granted_number 非空) | dwd_patent(pn, main_classification_ipcr, granted_number, apdt_year) — IPC领域,授权号,申请年 |
| 专利质量 |  | 从家族规模、权利要求数、被引次数、技术宽度、法律状态稳定性评估专利质量。 | 维内五项极值归一后等权。与 M_INNOV_TINN_PATENT_QUALITY 同一五级。 | dwd_patent(pn, first_applicant_name, main_classification_ipcr, further_classification_ipcr, claims, other_Versions, apdt_year) — 专利去重,申请人对齐,主分类,附加分类,权利要求,同族,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent_legal(pn, status, expiration_year) — 专利状态,到期年；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤 |
| 专利质量 | 家族规模 | 领域专利平均同族成员数。 | 同族成员数合计 / 专利数 | dwd_patent(pn, main_classification_ipcr, other_Versions, apdt_year) — 同族专利,IPC领域 |
| 专利质量 | 权利要求数 | 领域专利平均权利要求项数。 | 权利要求项数合计 / 专利数 | dwd_patent(pn, main_classification_ipcr, claims, apdt_year) — 权利要求,IPC领域 |
| 专利质量 | 被引次数 | 领域专利被后续专利引用的总次数。 | SUM(cited_by_nums) | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent(pn, main_classification_ipcr, apdt_year) — 专利去重,IPC领域 |
| 专利质量 | 技术宽度 | 单件专利覆盖的 IPC 小类广度。 | 每件专利 IPC4 去重数合计 / 专利数 | dwd_patent(pn, main_classification_ipcr, further_classification_ipcr, apdt_year) — 主分类,附加分类 |
| 专利质量 | 法律状态稳定性 | 仍处于授权/有效且未失效的专利占比。 | 稳定专利数 / 专利数 | dwd_patent_legal(pn, status, expiration_year) — 专利状态,到期年 |
| 技术市场潜力 |  | 从转让、许可、诉讼、质押、开放许可评估技术市场潜力。 | 维内五项极值归一后等权。与 M_INNOV_TINN_MARKET 同一五级。 | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年；dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_patent_legal(pn, legal_events) — 法律事件（许可,诉讼,质押,开放许可）；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤 |
| 技术市场潜力 | 转让 | 发生权利转移的专利占比。 | 转移专利数 / 专利数 | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_patent(pn, main_classification_ipcr, apdt_year) — 专利分母,IPC领域 |
| 技术市场潜力 | 许可 | 实施许可（不含开放许可）的专利占比。 | 许可专利数 / 专利数 | dwd_patent_legal(pn, legal_events) — 法律事件 |
| 技术市场潜力 | 诉讼 | 涉及诉讼或无效宣告的专利占比。 | 诉讼专利数 / 专利数 | dwd_patent_legal(pn, legal_events) — 法律事件 |
| 技术市场潜力 | 质押 | 发生质押登记的专利占比。 | 质押专利数 / 专利数 | dwd_patent_legal(pn, legal_events) — 法律事件 |
| 技术市场潜力 | 开放许可 | 声明开放许可的专利占比。 | 开放许可专利数 / 专利数 | dwd_patent_legal(pn, legal_events) — 法律事件 |

## 源表字段

dwd_patent(pn, kind, granted_number, first_applicant_name, main_classification_ipcr, further_classification_ipcr, claims, other_Versions, apdt_year) — 专利去重,授权号,申请人对齐,主分类,附加分类,权利要求,同族,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent_legal(pn, status, expiration_year, legal_events) — 专利状态,到期年,法律事件；dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|科技创新评估.md|序号 143「将技术创新力的各项指标进行综合展示，用户可自定义指标权重，系统根据权重计算综合得分，提供技术创新力的综合评估结果」。二级来自 seq 140-142（专利数量/专利质量/技术市场潜力）。05 无「技术创新力综合」专叶。自定义权重是交互壳，不另开 n/a_ops。
