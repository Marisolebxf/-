# 要素影响力（专利侧）（M_INNOV_DS_FACTORS_014）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_FACTORS_014.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_014.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_014_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_FACTORS_014 |
| 指标名称 | 要素影响力（专利侧） |
| 所属域 | INNOV（创新监测） |
| 一级模块 | DS-FACTORS（科技创新要素） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 创新要素 → 要素影响力（专利） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_FACTORS_014.md` |

## 口径定义

两维的**结构**都在：`gkx.dwd_patent_cited.cited_by_nums`（20,515 行）与 `gkx.dwd_patent.value`（2,939,895 行，非空 1,994,812）。但**被引维的数据量差三个数量级**：被引表只有 475 行（467 件不同专利）能按 `patent_id` 挂回主表，覆盖率 0.0162%；价值维虽 67.85% 填充，却有 81.95% 的值落在 0—5 分桶、只有 362 个离散取值。占 0.80 权重的维度不可用、占 0.20 权重的维度高度退化，按 §〇 判**部分支持**。本档位与 `code/M_INNOV_DS_FACTORS_014_out.json` 的 `support_judgment` 一致。

## 计算逻辑说明

```text
S = (0.80*S_cited + 0.20*S_value) / Σw，缺测维重归一
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_FACTORS_014.md` §二（M_INNOV_DS_FACTORS_014.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_patent`
- `dwd_patent_cited`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：专利影响力按王惠口径为「被引 0.80 + 价值 0.20」，占 0.80 权重的被引维在 gkx 上仅 475 行（467 件不同专利）可与主表对齐（覆盖 0.016157%），按缺测维重归一后退化为「专利价值单维分」，可批量产出但语义已不是影响力；价值维虽 67.8532% 填充，但只有 362 个取值、81.95% 落在 0-5 分桶，区分度不足。故判部分支持：价值维可算（199.48 万件），被引维缺口需甲方补 dwd_patent_cited 全量并与主表统一 ID。
- **基期声明**：由产物中实际出现的年度键反推：used=[2021, 2022, 2023, 2024, 2025, 2026]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_FACTORS_014.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_014.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_014_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

