# 区域科技创新竞争力水平（M_INNOV_KEYD_COMPETITIVENESS）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KEYD_COMPETITIVENESS.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KEYD_COMPETITIVENESS.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KEYD_COMPETITIVENESS_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_KEYD_COMPETITIVENESS |
| 指标名称 | 区域科技创新竞争力水平 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（创新技术 / 城市竞争力） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 · 科技发展态势 · 区域创新比较 · 城市关键技术竞争力 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020, 2025] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_KEYD_COMPETITIVENESS.md` |

## 口径定义

D1 产出与 D2 主体在四城上可算（专利 212.68 万件、论文 11,894 篇、企业 18.91 万家、高企 2.76 万家、机构 2,074 家），D3 政策维四城仅 6.06% 可归属、东莞 8 件惠州 0 件，属源侧覆盖不均，三档里两档可算、一档不可用，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KEYD_COMPETITIVENESS.md` §二（M_INNOV_KEYD_COMPETITIVENESS.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_heis_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：D1/D2 在四城上可算：专利 2,126,758 件（2021—2024 归城）、论文 11,894 篇、企业底册 189,116 家、高企 27,634 家、科研机构 2,074 家；但 D3 政策维量不可用：全表市级可归属 10,294/20,000（51.47%），落到四城的仅 1,212 条（6.06%），东莞 8 件、惠州 0 件，是源侧覆盖不均而不是供给真实差异；论文语料 100,900 篇中广州占 60.3%、且 2024 年单年 32,379 篇是前三年的 4.9 倍（导入痕迹），论文维只能作语料内相对。三档里两档可算、一档结构可用量不可用，判部分支持。
- **基期声明**：专利归城只到 2024（gba_patent.city_year 无 2025）；论文 2025 有 6,548 篇但 2026 仅 2,989 篇，为避免把「导入批次」当增长，窗口统一取 2021—2024；2017—2020 专利零行，未补 0、未外推。论文 2024 年异常单列敏感性（剔除后重算 D1/综合分与排名）。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KEYD_COMPETITIVENESS.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KEYD_COMPETITIVENESS.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KEYD_COMPETITIVENESS_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

