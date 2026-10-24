# 全球服务机构总数（M_SVC_PT_GLOBAL_TOTAL）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_GLOBAL_TOTAL.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_GLOBAL_TOTAL.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_GLOBAL_TOTAL_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_PT_GLOBAL_TOTAL |
| 指标名称 | 全球服务机构总数 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（全球供给面 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·专题服务门户 SVCCHAIN-PORTAL（TOPIC-PT-004）；展示侧呼应科技信息展示系统·产业服务链分析→服务机构库 §1.1.1.2.4.2.7.2（全球总量计数位） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [1951, 2025] |
| 缺失年份 | [1953, 1955, 1961, 1963, 1964, 1966, 1969, 1971, 1975, 1976, 1977] |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_PT_GLOBAL_TOTAL.md` |

## 口径定义

境内口径的存量值（44,153）与成立年累积序列（75 期，其中 64 个有值年，期末 44,132）在 gkx 全部可现转且对账闭合（44,132＋无成立年 21＝44,153）。卡点在「全球」二字的境外侧：`dwd_forg_base_info` 虽有 20,000 行，但只有 GB/US/CA 三个国别值、country 列全空、与机构主档无对齐键，不是服务机构名录，无法并入总量。因此本件判 **部分支持**——不是算不出数，而是只能出「境内全量」这一格。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_GLOBAL_TOTAL.md` §二（M_SVC_PT_GLOBAL_TOTAL.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_base_info`
- `dwd_org_base_info`
- `dwd_org_org_product_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：境内口径的存量值与成立年累积序列均可现转（池 44,153 家、可回查率 99.95%、64 个有值年份、期末 44,132＋无年份 21＝池全对账）；但「全球」所需的境外服务机构名录在 gkx 无源——dwd_forg_base_info 20,000 行只有 GB/US/CA 三个国别值且与服务机构池无对齐键，故海外轴无法并入 → 部分支持
- **基期声明**：存量序列按成立年累积，库内真实有出生记录的年份为 1951—2025（64 个有值年）；区间内 11 个年份零出生（不补 0、不进分母），无成立年的 21 家机构计入存量值但不进序列（值−序列期末＝21，口径差而非缺失）。2025 年之后无出生记录是底册登记滞后所致，不解读为「新增归零」。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_GLOBAL_TOTAL.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_GLOBAL_TOTAL.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_GLOBAL_TOTAL_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版（王惠模拟，引废弃 svc_global_dist）
- 2026-08-28: 侯佳伟改锁 1C 2国内 3A（未落 seed）
- 2026-10-13: 徐滕强拍板四疑点，seed v0.2.0 部分闭合（本文重写）
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

