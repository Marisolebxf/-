# 区域分布（M_ENT_KEYPANO_REGIONAL_DISTRIBUTION）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_REGIONAL_DISTRIBUTION.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_REGIONAL_DISTRIBUTION.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_REGIONAL_DISTRIBUTION_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_KEYPANO_REGIONAL_DISTRIBUTION |
| 指标名称 | 区域分布 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 重点企业全景 → 区域分布柱图 / 区县排行榜 / 地图气泡 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_KEYPANO_REGIONAL_DISTRIBUTION.md` |

## 口径定义

`GROUP BY chain_code, region_key` 是标准 SQL，行政码表在、量足，公式可完整执行。问题全部在分母与维度上：**分母**必须用同母体（该链上链企业数，不是全库 189,116）；**区域维**退化成一省四市；**复合区域维**在 gkx 不存在，只能自建。按 §〇 判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_REGIONAL_DISTRIBUTION.md` §二（M_ENT_KEYPANO_REGIONAL_DISTRIBUTION.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_org_base_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：区域分布公式可完整执行：12 条链 × 区域键共 309 行非空格，含 12 个全国格、12 个省格、48 个市格、225 个区县格、12 个复合区域格；市级格逐链相加等于该链上链企业数（12/12 通过），说明口径闭合。缺口在依赖侧：①重点名单不存在，4,561 家为专利阈值代理名单，且全部落在广东省 4 市，区域分布只可能是「一省四市 23 区县」的切片，全国格恒等于该链上链企业数、省格与全国格恒等、大湾区格与省格恒等——三层数值完全重合，分布图退化为两级；②复合区域维表不存在，scope 成员按规划纲要行政范围自建；③区县维有 339 家上链企业无法落格（区县名空白 289 + 区县名有而码未匹配 50），使区县层格数之和小于链级。按定义判部分支持。
- **基期声明**：截面件：名单按专利授权累计量（>=50）一次性截取，上链关系、链位、区域、资质均无年度键，产物与参数中不存在年份窗口，故 used/missing 均为空。不是「缺年按 0 摊入」的情形，也不得用 created_time 反推年份。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_REGIONAL_DISTRIBUTION.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_REGIONAL_DISTRIBUTION.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_REGIONAL_DISTRIBUTION_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

