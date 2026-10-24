# 深圳服务机构规模（M_SVC_SZ_SCALE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_SZ_SCALE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_SCALE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_SCALE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_SZ_SCALE |
| 指标名称 | 深圳服务机构规模 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（产业服务链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技信息展示系统·产业服务链分析·深圳对比页规模结构柱（§1.1.1.2.4.2.7）/ 科技专题服务系统·算法库·服务机构基础指标模型（§1.1.1.1.1.1.1.1.4） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_SZ_SCALE.md` |

## 口径定义

「深圳服务机构规模」要的是深圳服务机构在大中小微四档上的分布。两库都没有规模分布结果表，但底册的 `org_size` 枚举在深圳切片上覆盖 99.88%、五档合计与切片逐位闭合，资本列覆盖 99.91% 可作合理性校验，结构与数据量均足，当日即可现转，故判 **完全转换支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_SZ_SCALE.md` §二（M_SVC_SZ_SCALE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_org_product_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：规模档（org_size）在深圳切片上 25,566/25,597 有值（99.88%），未知 31 家可单列；gkx 无 svc_metric_fact 结果面，但底册字段 + 当前数据量足以现转出五档分布与交叉分面，且五档合计与切片逐位闭合，故判完全转换支持。
- **基期声明**：本件是截面（当期规模档分布），无年度序列，不使用基期年份；规模档不随年份回溯，年报员工/营收序列不在本件指标范围内（覆盖仅 3.18%/2.63%，见 gaps）。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_SZ_SCALE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_SCALE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_SCALE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

