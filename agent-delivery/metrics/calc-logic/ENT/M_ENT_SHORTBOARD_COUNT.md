# 短板指标数（M_ENT_SHORTBOARD_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SHORTBOARD_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SHORTBOARD_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SHORTBOARD_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_SHORTBOARD_COUNT |
| 指标名称 | 短板指标数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／企业评估／综合竞争力 |
| 更新频率 | 年 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业竞争力画像「短板指标数」卡 + 短板明细｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_SHORTBOARD_COUNT.md` |

## 口径定义

6 个 L3 可在 gkx 年报财务表上真算，765 家企业判出短板数（均值 2.51，8.10% 为零短板）；另外 3 个 L3 无原料，且判定年度集中在 2014—2015，故判部分支持。

## 计算逻辑说明

```text
shortboard_count_i = COUNT(L3_j | x_ij 存在 AND 同链同年均值存在(n>=5) AND 方向判定为更差)
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SHORTBOARD_COUNT.md` §二（M_ENT_SHORTBOARD_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_market`
- `dwd_org_annual_financial_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：九个 L3 里 6 项可从 gkx 年报财务表算出、3 项无原料（学历无字段 / 研发人员整列为空 / 市占率仅 15 行），且能判定的企业只占底册的极小比例；同链同年均值在本库是小样本，按 min_peers=5 有大量 cell 不判。结构与数据都在，但覆盖不足 → 部分支持。
- **基期声明**：本件是截面口径（每企业取 L3 覆盖面最广的一年，并列取较晚年），不是多期均值；财报表年份覆盖 2013—2025，判定实际落到 [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]。没有任何年份被按 0 摊进分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SHORTBOARD_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SHORTBOARD_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SHORTBOARD_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

