# 湾区创新能力威胁因素（M_INNOV_GBA_SWOT_THREAT）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_SWOT_THREAT |
| 指标名称 | 湾区创新能力威胁因素 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

识别该城政策退坡、竞争挤压与结构风险，给出威胁清单与应对策略。

## 计算逻辑说明

对近窗相对基线做恶化检测。三维：政策退坡 / 竞争挤压 / 结构风险。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 政策退坡 |  | 失效政策相对有效政策的比例。 | 近窗失效政策数 / max(近窗有效政策数, 1) ≥ 0.3 | dwd_policy_base(id, city, province, status, expire_date, publish_year) — 政策去重,湾区城市,有效失效,到期日 |
| 竞争挤压 |  | 该城专利份额是否下滑。 | 近窗份额 − 基线份额 ≤ −0.02 | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年 |
| 结构风险 |  | 专利领域是否过度集中。 | HHI(IPC4) ≥ 0.25 | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 申请人对齐,IPC领域,申请年 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集；dwd_policy_base(id, city, province, status, expire_date, publish_year) — 政策有效失效,到期日；dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC集中度,申请年

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|湾区创新监测.md|序号 103「识别并分析粤港澳大湾区创新能力发展的威胁因素，如竞争加剧、技术壁垒、政策变化、环境风险」。禁改挂 M_CHAIN_TECH_BARRIER_*。库 missing 保持。参考权威机构方案。
