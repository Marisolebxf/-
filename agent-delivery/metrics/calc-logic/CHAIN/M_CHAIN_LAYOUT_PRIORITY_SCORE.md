# 布局优先级评分（M_CHAIN_LAYOUT_PRIORITY_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_LAYOUT_PRIORITY_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_LAYOUT_PRIORITY_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_LAYOUT_PRIORITY_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_LAYOUT_PRIORITY_SCORE |
| 指标名称 | 布局优先级评分 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链（CHAIN |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·产业链分析（布局优先级）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_LAYOUT_PRIORITY_SCORE.md` |

## 口径定义

无现成「布局优先级」结果面 → 非完全直接支持；四指标里 D1 增长、D3 研发强度、D4 规模都能实测（8/12 链出分），但 **D2 市场占有率的分母「全国该产业产值」在库内不存在**（企业底册 99.82% 在广东，省外仅 339 家），**空间可行性维（土地/园区/载体面积）为零** → 四维里一维结构性不可得、一维为零 → **部分支持**。 > > **本版取证数据面（20261021）**：计算全部直连三方库 `gkx`（与 20261020 开发库 ODS 逐表镜像）；live `gkxlumenx_*` 仅用于核对自建派生表。下文「开发库」为四判定口径既定术语，读数以 `gkx` 为准。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_LAYOUT_PRIORITY_SCORE.md` §二（M_CHAIN_LAYOUT_PRIORITY_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_stock_finance_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四指标中 D1/D3/D4 可实测（D3 覆盖 972 家上市公司，2024 年报期 750 条），但 D2 市场占有率的分母『全国该产业产值』在开发库与三方库均无承载，且企业底册 99.82% 在广东，无法构造全国分母；空间可行性维（土地/园区/载体面积）同样为零。四维中一维结构性不可得 + 一维为零 → 按 §〇 判部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 383.3 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_LAYOUT_PRIORITY_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_LAYOUT_PRIORITY_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_LAYOUT_PRIORITY_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

