# 下游环节数（M_CHAIN_DOWNSTREAM_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DOWNSTREAM_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DOWNSTREAM_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DOWNSTREAM_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DOWNSTREAM_COUNT |
| 指标名称 | 下游环节数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 二级模块 | 产业链全景 |
| 更新频率 | 日 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_DOWNSTREAM_COUNT.md` |

## 口径定义

下游环节数 = 每链编码序位最大的 L1 分支下全部后代节点数（含该 L1 自身；容器节点与其下叶子各计 1）；这是结构代理口径，不是 chain_stage='downstream' 的官方口径

> 一句话口径（源件 §0.3）：`gkx.dwd_industry_chain_info` 没有 `chain_stage` 字段，本件按“每链编码序位最大的 L1 分支 = 末段分支”给出结构代理值 **256 个下游环节**（含末段 L1 自身，容器与叶子都计），并同时披露全末端叶子 954 个作为上界；因“下游”的阶段语义靠编码序位假设、且传感器与低空两条链出现反例，判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DOWNSTREAM_COUNT.md` §二（M_CHAIN_DOWNSTREAM_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：本件回答“12 条产业链各有多少个下游环节”。源表没有阶段字段，无法按 `chain_stage='downstream'` 直接筛选；
- **基期声明**：截面指标，无年度基期；快照 2026-10-22，链树无版本列

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DOWNSTREAM_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DOWNSTREAM_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DOWNSTREAM_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

