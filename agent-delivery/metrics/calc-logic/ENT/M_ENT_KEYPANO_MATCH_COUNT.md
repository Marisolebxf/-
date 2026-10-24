# 匹配企业数（M_ENT_KEYPANO_MATCH_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_MATCH_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_MATCH_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_MATCH_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_KEYPANO_MATCH_COUNT |
| 指标名称 | 匹配企业数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 重点企业全景 → 选定链位后的「匹配企业数」KPI 与链级汇总 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_KEYPANO_MATCH_COUNT.md` |

## 口径定义

COUNT 这个动作本身没有技术难度：上链边在、名单在、链位能定，一条 `GROUP BY` 就能出。难的是**三个分母**——名单是谁（库里没有）、链位是什么（库里没有）、格子能不能加（不能）。前两条让本件从「直算」退到「代理算」，第三条让「总数」这个最常见的问法失效。故按 §〇 判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_MATCH_COUNT.md` §二（M_ENT_KEYPANO_MATCH_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：COUNT 本身可以算完：上链边 2,283,762 行在，按 chain×node_stage 去重出 31 个非空格，去重企业 2,105 家、格内合计 5,196 人次；链级去重 12 条、合计 4,464 对。但分子两端都不是库里的现成事实：①重点名单不存在——280 张表八个名单模式扫描只命中新闻表，只能用专利授权≥50 的 4,561 家代理，命中率 50.2302% 是「代理名单的上链率」，不是「重点企业上链率」；②链位不存在——industry_tags 无 node_stage、chain_info.level 全 0，上中下游是自建映射。两维都靠自建，故判部分支持。
- **基期声明**：截面件：名单按专利授权累计量（>=50）一次性截取，上链关系、链位、区域、资质均无年度键，产物与参数中不存在年份窗口，故 used/missing 均为空。不是「缺年按 0 摊入」的情形，也不得用 created_time 反推年份。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_MATCH_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_MATCH_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_MATCH_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

