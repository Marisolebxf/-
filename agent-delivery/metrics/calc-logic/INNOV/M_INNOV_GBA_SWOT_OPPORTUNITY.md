# 湾区创新能力机会因素（M_INNOV_GBA_SWOT_OPPORTUNITY）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_SWOT_OPPORTUNITY |
| 指标名称 | 湾区创新能力机会因素 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

识别该城政策窗口、新兴技术与外溢合作，给出机会清单与利用建议。

## 计算逻辑说明

对近窗相对基线做放量检测。三维：政策窗口 / 新兴技术 / 外溢合作。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 政策窗口 |  | 近窗政策相对基线是否放量。 | 近窗政策数 / max(基线年均政策数, 1) ≥ 1.5 | dwd_policy_base(id, city, province, status, expire_date, publish_year, theme) — 政策去重,湾区城市,有效,发布年,主题 |
| 新兴技术 |  | 该城突现 IPC 领域。 | burst≥1 且近窗专利≥3 的 IPC4 个数 | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 申请人对齐,IPC领域,申请年 |
| 外溢合作 |  | 跨城联合专利是否加速。 | (近窗跨城联合专利年均 − 基线年均) / max(基线年均, 1) ≥ 0.5 | dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 共申请人,申请人对齐,申请年 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集；dwd_policy_base(id, city, province, status, expire_date, publish_year, theme) — 政策窗口,主题；dwd_patent(pn, applicants, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,共申请人,IPC突现,申请年

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|湾区创新监测.md|序号 102「识别并分析粤港澳大湾区创新能力发展的机会因素，如政策支持、市场需求、技术突破、国际合作」。05 综合叶不输出 Opportunities 象限。库 missing 保持。参考权威机构方案。
