# 湾区创新能力优势因素（M_INNOV_GBA_SWOT_STRENGTH）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_SWOT_STRENGTH.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SWOT_STRENGTH.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SWOT_STRENGTH_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_SWOT_STRENGTH |
| 指标名称 | 湾区创新能力优势因素 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV / 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 湾区创新能力优势因素分析（seq 100）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2019, 2020, 2021, 2022, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_GBA_SWOT_STRENGTH.md` |

## 口径定义

11/12 分项可算，但 4 城上 rank≤3 等价于「不是最后一名」，深圳/广州各 11 项全入选；强优势替代（rank≤2 且 norm≥0.5）得到 9/5/0/0。

## 计算逻辑说明

```text
advantage = 分项在 4 城降序排名 ≤3；impact = 四城 min-max 归一；strong = rank≤2 ∧ norm≥0.5 ∧ 非重复计位
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_SWOT_STRENGTH.md` §二（M_INNOV_GBA_SWOT_STRENGTH.py 零改语义复算）。

## 源表字段

源件未点名任何 dwd_/ads_/ods_ 物理表（纯派生/合成件，输入为兄弟件产物或快照）；依赖清单见源件 §〇/§三。

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：11/12 分项可算、4 城清单全部可出；但面板只有 4/11 城，原规则「11 城 rank≤3」在 4 城上退化为「不是最后一名」，实际入选率 75%（设计 27.3%），2–11 项/城，区分度低；政策覆盖缺失；载体产出与资源维重复计位；联合专利仅 20,000 pn 样本、研发投入仅上市主体。故判部分支持；`strong_advantage` 是可区分替代，但属本件自定义、需甲方确认。
- **基期声明**：分项窗口不同：专利 2021—2024；论文 2021—2023（2024 年论文量属批次断层，排除）；研发投入 2019—2024（上市主体）；项目 2021—2023；转移 2021—2026；政策存量无年度窗口。used 为并集，未把缺年补 0。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_SWOT_STRENGTH.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SWOT_STRENGTH.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SWOT_STRENGTH_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

