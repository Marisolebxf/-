# 技术热点热度指数（M_TECH_HEAT_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_HEAT_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_HEAT_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_HEAT_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_HEAT_INDEX |
| 指标名称 | 技术热点热度指数 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术热点看板（TOPIC-TECH-01 / DS-02-TECHHEAT）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_HEAT_INDEX.md` |

## 口径定义

以**深圳**为唯一主体、IPC4 主分类前 4 位为技术点，取 2021—2024 年四个完整年，用「规模 lnN（0.40）+ 平滑 CAGR（0.35）+ 近端占比（0.25）」z 标准化加权后 min-max 到 0—100，在 **238 个 2024 年不少于 100 件的合格域**上给出五档热度；全国 IPC4 只作 LQ 分母、分表列示。专利侧三维齐备、指数非退化，但需求点名的论文、新闻与博客、行业资讯、专家活动四类输入在库内都没有能挂到「技术点」上的键，故按四档口径落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_HEAT_INDEX.md` §二（M_TECH_HEAT_INDEX.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：专利单源的规模/增长/近端三维齐备，238 个域全部可算、指数非退化；需求点名的多源输入（学术论文、新闻与技术博客、行业资讯、专家活动）四项在库内均无「技术点」回连字段，无法合成，故落部分支持。
- **基期声明**：基期与末期为库内真实存在的 2021 与 2024；CAGR 分母只用 2021（真实件数），2017—2020 在 dwd_patent 零行，不按 0 摊入、不做外推；2025/2026 属采集残年（全国 2025 覆盖 72.63%、2026 仅 12.33%），不进入窗口。
- **复现实测耗时**：约 153.7 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_HEAT_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_HEAT_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_HEAT_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

