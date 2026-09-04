# 技术产品成熟度（M_INNOV_POT_MATURITY）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_POT_MATURITY |
| 指标名称 | 技术产品成熟度 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

按授权比例、发明占比、市场渗透综合评分，取值 0—100。对象为 IPC 前 4 位；综合评估复用本三维时按产业汇总。

## 计算逻辑说明

采用加权平均，三维：授权比例（授权专利/专利）/ 发明占比（发明专利/专利）/ 市场渗透（转移专利/专利）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 授权比例 |  | 授权专利占全部专利比。 | 授权专利数 / 专利数 | dwd_patent(pn, main_classification_ipcr, granted_number, apdt_year) — IPC领域,授权号,申请年 |
| 发明占比 |  | 发明专利占全部专利比。 | 发明专利数 / 专利数 | dwd_patent(pn, main_classification_ipcr, kind, apdt_year) — IPC领域,申请类型,申请年 |
| 市场渗透 |  | 发生转移的专利占比。 | 转移专利数 / 专利数 | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_patent(pn, main_classification_ipcr, apdt_year) — 专利分母,IPC领域 |

## 源表字段

dwd_patent(pn, kind, granted_number, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请类型,授权号,申请人对齐,IPC领域,申请年；dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_org_base_info(org_id, name_cn, external_id, industry, city, province, reg_status) — 名称对齐,空间过滤,产业切片；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技创新评估.md|序号 147「通过技术生命周期分析、市场渗透率分析等方法，评估特定产业内技术或产品的成熟度」。对照 seq 137 实现类（TOPIC-TECH-05 同叶 third_party）。禁止 B 轨成熟度/阶段 ID 顶替。参考权威机构方案。
