# 深圳机构区域分布（M_SVC_PT_SZ_REGION_ORG）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_SZ_REGION_ORG.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_SZ_REGION_ORG.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_SZ_REGION_ORG_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_PT_SZ_REGION_ORG |
| 指标名称 | 深圳机构区域分布 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（深圳供给面 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技专题服务系统·专题服务门户 SVCCHAIN-PORTAL 深圳专题；展示侧呼应科技信息展示系统·产业服务链分析→服务机构库（区块筛选位） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_PT_SZ_REGION_ORG.md` |

## 口径定义

深圳切片的区级分布可现转且闭合：**25,597** 家，9 个有值行政区 25,587＋未分配 10＋区外/异名 0＝25,597，与 `M_SVC_PT_SZ_TOTAL` 同数；区字段非空率 99.96%。无代理维度、无外部依赖 → **完全转换支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_SZ_REGION_ORG.md` §二（M_SVC_PT_SZ_REGION_ORG.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_org_product_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：深圳切片的区级分布可现转且闭合：切片 25597 家，9 个行政区＋未分配 10＋区外/异名 0 ＝25597（与 M_SVC_PT_SZ_TOTAL 同池同数）；区字段非空率 99.96%，未分配单列不剔除
- **基期声明**：截面指标：区级分布是当前时点存量的空间切分，不含年度分母；切片总量与成立年序列由 M_SVC_PT_SZ_TOTAL 承担。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_SZ_REGION_ORG.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_SZ_REGION_ORG.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_SZ_REGION_ORG_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-13: v0.2.1 修正取数链（dwd_service_org.district → dwd_org_base_info.area）+ 落真数 14,033/十区分布；口径（十区全集/未分配/数随池联动）不动。
- 2026-10-13: v0.2.0 落盘（标准十区、空值单列「未分配」）。
- 2026-08-21: 初版（模拟王惠调研产出，基于旧池 3,525，已作废）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

