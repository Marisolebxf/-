# 湾区创新能力威胁因素（M_INNOV_GBA_SWOT_THREAT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_SWOT_THREAT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SWOT_THREAT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SWOT_THREAT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_SWOT_THREAT |
| 指标名称 | 湾区创新能力威胁因素 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（创新技术 / GBA） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 · 科技发展态势 · 大湾区创新协同 · 技术威胁识别 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_GBA_SWOT_THREAT.md` |

## 口径定义

D2 竞争挤压与 D3 结构风险在 850,656 条 IPC4 归属性上可算，四城威胁分 0.0—50.0 有区分度；但 D1 政策退坡完全不可算，而政策恰是需求最关心的威胁来源，11 城中只有 4 城可评，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_SWOT_THREAT.md` §二（M_INNOV_GBA_SWOT_THREAT.py 零改语义复算）。

## 源表字段

源件未点名任何 dwd_/ads_/ods_ 物理表（纯派生/合成件，输入为兄弟件产物或快照）；依赖清单见源件 §〇/§三。

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：D2/D3 在 850,656 条 IPC4 归属性上可算，四城威胁分 0.0—50.0 有区分度；但 D1 政策退坡三重阻断（status 全有效 20,000 行、无 expire_date 列、近窗 1 条），而政策恰恰是需求最关心的威胁来源。11 城中只有 4 城可评，港澳与珠西五市无数据。
- **基期声明**：基线 2021—2022、近窗 2023—2024（四个完整年）；快照 gba_patent.city_year 只落到 2024，2025/2026 虽有全表件数（440,401 / 74,810，分别为完整年的 72.6% / 12.3%）但未归城，故删失敏感性本件不可算（字段为 null），不拿全国残年冒充四城份额；2017—2020 在 dwd_patent 为零行，未补 0、未外推。政策表日期止于 2024（2024 年 1 条）。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_SWOT_THREAT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SWOT_THREAT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SWOT_THREAT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

