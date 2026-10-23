# 竞争力-配套环境（M_CHAIN_REG_COMP_SUPPORT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_COMP_SUPPORT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_COMP_SUPPORT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_COMP_SUPPORT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_COMP_SUPPORT |
| 指标名称 | 竞争力-配套环境 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | CHAIN（产业链区域指数） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 产业链区域指数 → 竞争力 → 配套环境 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_REG_COMP_SUPPORT.md` |

## 口径定义

融资事件表有企业标识、有日期、有金额与轮次，链桥覆盖 35,046 家企业，48 个链×城单元全部有事件（最少 2 次、最多 5,462 次），政策池可算同链同城覆盖率作为副值 → 结构与数据都够，现在就能转换得到 → **完全转换支持**。本档位与 `code/M_CHAIN_REG_COMP_SUPPORT_out.json` 的 `support_judgment.data_support_level` 一致。

## 计算逻辑说明

```text
Support(c,r)=COUNT(DISTINCT financing_event) over 链上企业(c,r)，一行融资记录=一次事件
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_COMP_SUPPORT.md` §二（M_CHAIN_REG_COMP_SUPPORT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_financing_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：主值所需的三个输入全部在 gkx 闭合：链归属 `dwd_org_industry_tags → dwd_org_base_info` 命中 35,046 家链上企业，区域轴 `city` 已规范到市级，融资事件表 `dwd_org_financing_info` 25,654 行 / 6,503 家。按「一行=一次事件」落 48 个链×城单元，48/48 单元非零，事件数 2—5,462（中位 305.5），48 个单元 48 个不同取值，结构、当前量、当日现转三条同时成立。覆盖边界的披露不改变档位：融资记录只覆盖 3.44% 的底册企业，其中 49.39% 可落链，故数值应读作「有融资披露的链上企业事件数」，不是全链融资总量。
- **基期声明**：由产物中实际出现的年度键反推：used=[2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。
- **复现实测耗时**：约 0.5 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_COMP_SUPPORT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_COMP_SUPPORT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_COMP_SUPPORT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

