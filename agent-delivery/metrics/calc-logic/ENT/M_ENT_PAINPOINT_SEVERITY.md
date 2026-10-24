# 痛难点严重度（M_ENT_PAINPOINT_SEVERITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PAINPOINT_SEVERITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PAINPOINT_SEVERITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PAINPOINT_SEVERITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_PAINPOINT_SEVERITY |
| 指标名称 | 痛难点严重度 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·企业深度分析「企业发展痛难点识别模型」（算法库 §1.1.1.1.1.1.1.5.3，需求 ID ALGO-ENT-DEEP-143；SRS 需规序号 143 同族）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_PAINPOINT_SEVERITY.md` |

## 口径定义

无结果面 + 分档依赖的阈值配置表缺（Q014——偏离度分档的档界即阈值）+ 人才维全空、财务七列 2–3% 填充 → 按第 3 档归**部分支持**（脚本机判一致；行业 P25 代理 + 等权降级轨 34 家可算、6 家存在偏离，分档演示完成）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PAINPOINT_SEVERITY.md` §二（M_ENT_PAINPOINT_SEVERITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `ads_ent_painpoint_severity`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：阈值配置表（Q014）在 live 开发库 gkxlumenx_dwd/ads 均无——王惠口径的分档依赖阈值，缺配置即无法正式出档；人才维研发人员全空（0 行）+ 财务原料填充 2-3%（营收 2.41%）不足以支撑全国企业分档；降级轨：行业 P25 代理 + 等权下可对 34 家出偏离度，其中 6 家存在偏离（分档分布 {'无偏离(轻0)': 28, '轻度(0-20%)': 0, '中度(20-50%)': 1, '重度(>50%)': 5}）
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PAINPOINT_SEVERITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PAINPOINT_SEVERITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PAINPOINT_SEVERITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

