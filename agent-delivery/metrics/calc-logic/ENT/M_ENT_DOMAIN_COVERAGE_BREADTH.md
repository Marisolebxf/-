# 技术领域覆盖广度（M_ENT_DOMAIN_COVERAGE_BREADTH）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DOMAIN_COVERAGE_BREADTH.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DOMAIN_COVERAGE_BREADTH.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DOMAIN_COVERAGE_BREADTH_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_DOMAIN_COVERAGE_BREADTH |
| 指标名称 | 技术领域覆盖广度 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业服务／企业评价／技术广度 |
| 更新频率 | 建议半年 |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 企业画像「技术领域」卡、技术型企业榜、专利布局分析｜ **数据支持度**：**完全转换支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_DOMAIN_COVERAGE_BREADTH.md` |

## 口径定义

按申请人去重 IPC4 得技术广度：134,152 家企业、634 个 IPC4 类，中位 2、p90 9、最高 429（华南理工），单字段当天可算，判完全转换支持。

## 计算逻辑说明

```text
breadth_i = COUNT(DISTINCT substr(ipc,1,4)) BY 申请人；附带 patents_per_field = 专利数 / breadth
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DOMAIN_COVERAGE_BREADTH.md` §二（M_ENT_DOMAIN_COVERAGE_BREADTH.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：本指标不依赖任何缺失的结果面：dwd_patent 的 main_classification_ipcr 直接给出每条专利的 IPC，取前 4 位后按申请人去重计数即得覆盖广度。库内 2,939,895 条专利、581,585 条企业×IPC4 记录、134,152 个申请人、634 个 IPC4 小类，分布从 1 到 100+ 完整可算，排名、分档、城市均值都能直接产出，无需代理、无需补数。
- **基期声明**：专利表 apdt_year 只有 2021—2026（2017—2020 零行，DATA_FACTS 陷阱 3.13），本件按全期去重计广度，不按年切分；2025/2026 为不完整年，若做年度增量需单列。广度是存量口径，年份窗口只影响「哪些专利被纳入」，不影响字段语义。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DOMAIN_COVERAGE_BREADTH.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DOMAIN_COVERAGE_BREADTH.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DOMAIN_COVERAGE_BREADTH_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

