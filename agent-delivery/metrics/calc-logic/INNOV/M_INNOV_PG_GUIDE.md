# 发展战略引导力（M_INNOV_PG_GUIDE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PG_GUIDE |
| 指标名称 | 发展战略引导力 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q144 / Q-MO-DS07-05 |

## 口径定义

从前瞻性、系统性、针对性综合评分，取值 0—100。三性与 M_POLICY_DS_07_POLICY_GUARD_001 同一套覆盖率。

## 计算逻辑说明

选定城市入集。采用加权平均，三维：前瞻性（战略顶层规划覆盖率） / 系统性（政策承接完整度） / 针对性（精准扶持措施覆盖率）。与 M_POLICY_DS_07_POLICY_GUARD_001 同一套三性公式。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 前瞻性 |  | 政策是否包含规划/纲要/远景等顶层设计词。 | 四字段含「规划」或「纲要」或「远景」的政策数 ÷ 政策总数 | dwd_policy_base(title, keywords, keypoints, theme) — 四字段命中 |
| 系统性 |  | 政策是否明确引用或承接过往相关政策。 | quote_policy 非空且不为空数组的政策数 ÷ 政策总数 | dwd_policy_base(quote_policy) — 政策承接 |
| 针对性 |  | 政策是否包含明确扶持细则。 | policy_support.support_way 至少 1 条非空的政策数 ÷ 政策总数 | dwd_policy_base(policy_support.support_way) — 扶持措施 |

## 源表字段

dwd_policy_base(id, title, keywords, keypoints, theme, quote_policy, policy_support, city, province, publish_year, status, expire_date) — 四字段前瞻词,政策承接,扶持措施,有效,发布年,空间

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技创新评估.md|序号 152「评估战略规划的前瞻性、系统性和针对性，用户可以查看战略规划的关键内容、实施路径和预期目标」。三性默认一条 ID（Q-MO-DS07-05 / PG-B03）。政策 9 叶无引导力专叶。参考权威机构方案。
