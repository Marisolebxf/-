# 关键节点数（M_CHAIN_KEY_NODE_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_KEY_NODE_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_KEY_NODE_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_KEY_NODE_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_KEY_NODE_COUNT |
| 指标名称 | 关键节点数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 / 产业诊断 / 关键环节识别 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链全景页「关键环节」计数卡 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_KEY_NODE_COUNT.md` |

## 口径定义

王惠 V2 的三因子（附加值率、技术壁垒、CR4）里，**只有「企业规模」一维**能在 gkx 得到：916 个有企业的叶级环节全部有企业数，12 条链都能算；附加值率与 CR4 需要环节级营收（gkx 只有企业级年报且只覆盖上市主体），技术壁垒需要环节—专利键（专利只有 IPC/申请人）。三因子缺两维，本件改用企业数分位代理，得 **463/916 = 50.55%**——这个比例由中位数规则**构造**出来，不是产业事实，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_KEY_NODE_COUNT.md` §二（M_CHAIN_KEY_NODE_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_annual_financial_info`
- `dwd_org_industry_tags`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：12 条链的叶级环节企业数均可得（916/954 个叶级环节有企业），但王惠 V2 的三因子里只有「企业规模」一维可算；附加值率与 CR4 卡在环节级营收、技术壁垒卡在环节—专利键，故只能给分位代理值（463，占比 50.55% 由中位数规则决定），不是三因子结论，判部分支持。
- **基期声明**：截面指标：统计当前存量，不设年度分母。
- **复现实测耗时**：约 0.01 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_KEY_NODE_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_KEY_NODE_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_KEY_NODE_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

