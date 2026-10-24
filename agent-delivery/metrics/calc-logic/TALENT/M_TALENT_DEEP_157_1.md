# M_TALENT_DEEP_157_1（M_TALENT_DEEP_157_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_157_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_157_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_157_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_DEEP_157_1 |
| 指标名称 | M_TALENT_DEEP_157_1 |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才洞察页「区域流入/流出/留存 + 城际流向 + 时间线」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [1998, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025] |
| 缺失年份 | [1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008] |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_DEEP_157_1.md` |

## 口径定义

履历表 57,117 段覆盖 16,718 名有机构记录的学者，且自带 `is_current` 标记，机构序列、城际有向边、深圳三态（流入/流出/留存）都能全量现转；但需求点名的社交网络、招聘网站、简历库三类源在 `gkx` 无表（`dwd_job` 仅 10 行），流动只能用「现机构 vs 历史机构」代理，机构名空 20.41%、与主档仅 10.56% 可挂，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_157_1.md` §二（M_TALENT_DEEP_157_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_job`
- `dwd_org_heis_info`
- `dwd_org_industry_tags`
- `dwd_scholar`
- `dwd_scholar_work_experience`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：履历表 57,117 段覆盖 20,028 名学者，机构序列/城际边/深圳三态可全量现转，流动骨架成立；但需求点名的社交网络、招聘网站、简历数据库三类源在库内无表（dwd_job 仅 10 行），流失与流入只能用「现机构 vs 历史机构」代理，且履历表与身份主档只有 9.27% 可挂（姓名/职称仅在这部分可用），深圳流入年样本集中在少数年份 → 部分支持。
- **基期声明**：流入年分布只用履历 start_time 中**真实出现**的年份（1998—2025，共 18 个有事件的年）；区间内没有事件的年份列入 base_years_missing，不补 0、也不作分母。本指标不做跨年基准或增速，因此不存在「前 N 年均值」这类分母。
- **复现实测耗时**：约 4.7 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_157_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_157_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_157_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

