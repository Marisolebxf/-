# 创新环境指数（M_INNOV_GBA_ENV_INDEX）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_ENV_INDEX |
| 指标名称 | 创新环境指数 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q133 / Q-MO-DS05-02 |

## 口径定义

湾区 11 城政策供给、主题覆盖与高企密度综合分，取值 0—100。

## 计算逻辑说明

采用加权平均。三维：政策供给 / 政策覆盖 / 高企密度。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 政策供给 |  | 该城有效政策件数。 | COUNT(DISTINCT id) | dwd_policy_base(id, city, province, status, expire_date, publish_year, rank) — 政策去重,湾区城市,有效,发布年,级别 |
| 政策覆盖 |  | 政策主题点数。 | COUNT(DISTINCT theme) | dwd_policy_base(id, city, theme) — 政策主题 |
| 高企密度 |  | 高企占存续机构比。 | 高企数 / 存续机构数 | dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_org_base_info(org_id, city, province, reg_status) — 存续机构分母 |

## 源表字段

dwd_policy_base(id, city, province, status, expire_date, publish_year, rank, theme) — 政策去重,湾区城市,有效过滤,发布年,级别,主题；dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,高企分母；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, country, city) — 港澳机构入集；dwd_org_tech_tag(org_id, org_tag) — 高新技术等科技型标签

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|湾区创新监测.md|序号 96「分解为多个子指标（如创新资源指数、创新机构指数、创新机制指数、创新环境指数）」。总指数子指标「创新环境」（xlsx 43）。需求未给内部构成维度，参考权威机构方案。
