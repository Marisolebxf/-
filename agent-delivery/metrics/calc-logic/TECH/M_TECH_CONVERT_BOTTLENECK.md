# 技术转化瓶颈诊断（M_TECH_CONVERT_BOTTLENECK）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_CONVERT_BOTTLENECK.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_CONVERT_BOTTLENECK.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_CONVERT_BOTTLENECK_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_CONVERT_BOTTLENECK |
| 指标名称 | 技术转化瓶颈诊断 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术／成果转化 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 技术转化瓶颈页的「瓶颈域排行」、产业布局推荐页的「技术域风险」标签 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_CONVERT_BOTTLENECK.md` |

## 口径定义

三个结构算子能算、排序稳定、区分度正常，但需求点名的「成果转化」一类无源。诊断类指标缺一维就等于缺一类病因，故按 §〇 落**部分支持**，且消费侧必须对缺维加标签。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_CONVERT_BOTTLENECK.md` §二（M_TECH_CONVERT_BOTTLENECK.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_scholar`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：承接集中度、技术陈旧度、收缩度三个结构量在 253 个实质性 IPC4 域上可复算（覆盖有 IPC 专利的 0.9488），判瓶颈率 0.3004 由阈值直接决定，P60/P70/P80 名单 Jaccard 0.7525 / 0.6711，区分度正常且不随规模漂移；但需求三类指标中的成果转化类在 gkx 无源，五维资源框架（人才/市场/技术/政策/资金）只有技术维与市场结构维有算子。始终存在无法补齐的依赖维，故落部分支持。
- **基期声明**：专利表 apdt_year 覆盖 2021—2026（2017—2020 零行，不补 0）。本件只用 2021—2024 四个完整年：2025 有 440,401 件（2024 为 606,468，仅 72.6%）、2026 有 74,810 件，两年均为采集未完年，按缺失年处理、不进分母、不摊 0。增速用 2022→2024 的 CAGR，缺任一端则该域 G 维不摊 0（标 g_missing）。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_CONVERT_BOTTLENECK.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_CONVERT_BOTTLENECK.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_CONVERT_BOTTLENECK_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

