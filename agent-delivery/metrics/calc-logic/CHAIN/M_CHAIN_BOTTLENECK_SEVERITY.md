# 瓶颈严重度（M_CHAIN_BOTTLENECK_SEVERITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_BOTTLENECK_SEVERITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_BOTTLENECK_SEVERITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_BOTTLENECK_SEVERITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_BOTTLENECK_SEVERITY |
| 指标名称 | 瓶颈严重度 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链监测／堵点识别 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链监测页「瓶颈严重度」红黄绿灯与下钻 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | ["2021", "2022", "2023", "2024"] |
| 缺失年份 | ["2025", "2026"] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_BOTTLENECK_SEVERITY.md` |

## 口径定义

四维强度（技术/产品/资本/政策）在 `gkx` 全部可现算、12 条链无空值；旧稿口径的第五维「人才」依赖研发人员占比，而该字段整列为空，属**结构性缺一维**，故判 **部分支持**，不抬档。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_BOTTLENECK_SEVERITY.md` §二（M_CHAIN_BOTTLENECK_SEVERITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_financing_info`
- `dwd_org_industry_product_tags`
- `dwd_org_industry_tags`
- `dwd_patent`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四维强度（技术/产品/资本/政策）在本件全部现算、12 条链全部非空，但旧稿口径的第五维「人才」在 gkx 无链级源：dwd_scholar 的 scholar_org_id 整列为空（0/21,316），学者与高校/院所都无法挂到产业链节点上，因此只能用产品维顶替，维数从 5 降到 4；同时严重度是中位数相对量、阈值 60/40 为本件自定义，未经甲方会签。缺一维 + 阈值未会签 = 部分支持，不抬档。
- **基期声明**：专利维按 application_year ≤2024 截断（2025—2026 公开不全）；产品/融资/政策三维为存量或含 2025 事件，无年度窗口，故不摊年度序列。
- **复现实测耗时**：约 1.36 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_BOTTLENECK_SEVERITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_BOTTLENECK_SEVERITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_BOTTLENECK_SEVERITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

