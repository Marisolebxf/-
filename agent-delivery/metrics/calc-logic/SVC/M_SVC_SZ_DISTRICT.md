# 深圳服务机构分布（M_SVC_SZ_DISTRICT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_SZ_DISTRICT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_DISTRICT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_DISTRICT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_SZ_DISTRICT |
| 指标名称 | 深圳服务机构分布 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（产业服务链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技信息展示系统·产业服务链分析·深圳对比页区级分布（§1.1.1.2.4.2.7）/ 科技专题服务系统·算法库·服务机构基础指标模型（§1.1.1.1.1.1.1.1.4） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_SZ_DISTRICT.md` |

## 口径定义

「深圳服务机构分布」要的是深圳服务机构在行政区上的分布，两库都没有现成的区级分布结果表；但 gkx 底册的 `area` 字段在深圳切片上覆盖 99.96%，与机构池按 `org_id` 回联后区级合计 25,587 加未分配 10 严格等于切片 25,597，结构与数据量都足，现在即可经转换得到分布，故判 **完全转换支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_SZ_DISTRICT.md` §二（M_SVC_SZ_DISTRICT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_org_product_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：gkx 280 表中无 svc_region_dist 等结果面（0 张 svc_*），但底册 area 字段在深圳切片上 25,587/25,597 有值（99.96%），未分配 10 家可单列，区级合计与切片严格闭合；结构与数据量均足，当日可经转换出数，故判完全转换支持。
- **基期声明**：本件是截面（当期区级分布），没有年度序列，因此不使用基期年份；成立年维在 M_SVC_PT_SZ_TOTAL 另件处理，本件不摊年、不补 0。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_SZ_DISTRICT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_DISTRICT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_DISTRICT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

