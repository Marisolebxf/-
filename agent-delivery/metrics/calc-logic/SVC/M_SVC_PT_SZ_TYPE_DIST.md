# 深圳服务机构类型分布（M_SVC_PT_SZ_TYPE_DIST）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_SZ_TYPE_DIST.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_SZ_TYPE_DIST.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_SZ_TYPE_DIST_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_PT_SZ_TYPE_DIST |
| 指标名称 | 深圳服务机构类型分布 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（产业服务链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·深圳服务机构类型环图 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_PT_SZ_TYPE_DIST.md` |

## 口径定义

三类轴的「企业」一类可由 `city='深圳市'` 直接切出 25,589 家（99.9687%），但「高校」只能靠名称含「大学/学院」的规则识别（8 家，清洗后 6 家），「科研院所」21 家在池内 `city` 与 `prov` 全为空串、按城市切片恒 0——三类中有一类结构性不可得、一类规则不可靠，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_SZ_TYPE_DIST.md` §二（M_SVC_PT_SZ_TYPE_DIST.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_org_product_info`
- `dwd_research_institute_base_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三类轴的「企业」一类可由 `city='深圳市'` 直接切出 25,589 家（99.9687%），但「高校」只能靠名称含「大学/学院」的规则识别（8 家，清洗后 6 家），「科研院所」21 家在池内 `city` 与 `prov` 全为空串、按城市切片恒 0——三类中有一类结构性不可得、一类规则不可靠，故判 **部分支持**。
- **基期声明**：截面指标：口径时点为快照 code/_snapshots21/svc21_facts_20261022.json（dwd_org_org_product_info + dwd_org_base_info 重建池）。不按年度出数，故 used / missing 均为空表；机构类型取底册当前登记状态，不是某年快照。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_SZ_TYPE_DIST.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_SZ_TYPE_DIST.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_SZ_TYPE_DIST_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-13: v0.2.1 补真数修订：city 切片经 dwd_org_base_info JOIN 取（同第 11 条），深圳切片真数 14,033；企业类计数同步为该真数。
- 2026-10-13: v0.2.0 落盘（三类字典维持、高校/院所恒 0、环图单色如实呈现）。human:徐滕强 拍板。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

