# 服务关系链密度（M_SVC_RELATION_DENSITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_RELATION_DENSITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_RELATION_DENSITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_RELATION_DENSITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_RELATION_DENSITY |
| 指标名称 | 服务关系链密度 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | 服务机构 |
| 更新频率 | 月度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 服务机构关系图概览卡、城市服务机构网络密度对比 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_RELATION_DENSITY.md` |

## 口径定义

「服务关系链密度」问的是服务机构和它的服务对象之间连得有多密。calc-logic 的语义载体是「服务关系边」，而 gkx 里能连的边只有投资与股东两类股权关系——它们能构造出一张图，也能算出密度，但这张图回答的是「谁持有谁」，不是「谁服务谁」。因此本件把可算的图结构量全部算出来，把不可算的语义维整块登记为缺口，判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_RELATION_DENSITY.md` §二（M_SVC_RELATION_DENSITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_invest_info`
- `dwd_org_org_product_info`
- `dwd_org_shareholder_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：「服务关系链密度」问的是服务机构和它的服务对象之间连得有多密。calc-logic 的语义载体是「服务关系边」，而 gkx 里能连的边只有投资与股东两类股权关系——它们能构造出一张图，也能算出密度，但这张图回答的是「谁持有谁」，不是「谁服务谁」。因此本件把可算的图结构量全部算出来，把不可算的语义维整块登记为缺口，判**部分支持**。
- **基期声明**：截面指标（快照日 2026-10-22），无年度基期；投资/股东边不带可靠年份，不做时间序列。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_RELATION_DENSITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_RELATION_DENSITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_RELATION_DENSITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

