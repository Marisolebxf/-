# 深圳技术链模型（M_TECH_DEEP_131_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_DEEP_131_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DEEP_131_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DEEP_131_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_DEEP_131_1 |
| 指标名称 | 深圳技术链模型 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·深圳技术链视图（TOPIC-TECH-05 / DS-02-TECHGRAPH）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_DEEP_131_1.md` |

## 口径定义

深圳切片可当日重切：2021—2024 有 IPC 的专利归属次 890,009 件、覆盖 609 个 IPC4 域、占全国有 IPC 专利 2,420,915 件的 36.76%；区级矩阵覆盖深圳有 IPC 专利的 99.996%；企业数与科技资质可算。但产业规模无域级营收字段、应用领域经信用代码桥仅覆盖 12.99%、区级矩阵是「全期截面」而非逐年、论文与标准无深圳切片源——属地多维属性始终缺维，落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_DEEP_131_1.md` §二（M_TECH_DEEP_131_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_industry_product_tags`
- `dwd_org_stock_finance_info`
- `dwd_org_tech_tag`
- `dwd_patent`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：深圳切片（890,009 件归属次、609 域）、区级矩阵（覆盖有 IPC 专利 99.996%）、企业数与科技资质可复算；但产业规模无域级字段、应用领域经信用代码桥仅覆盖 12.99%、区级年度序列与论文/标准切片缺源——属地多维属性始终缺维。
- **基期声明**：dwd_patent.apdt_year 全库只有 2021—2026；2025（440,401）与 2026（74,810）为采集残年，不进入同比与基期。2017—2020 零行，不得按 0 摊入分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_DEEP_131_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DEEP_131_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DEEP_131_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

