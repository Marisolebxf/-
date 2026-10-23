# 产业链竞争力指数（M_CHAIN_COMPETITIVENESS_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_COMPETITIVENESS_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_COMPETITIVENESS_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_COMPETITIVENESS_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_COMPETITIVENESS_INDEX |
| 指标名称 | 产业链竞争力指数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链总览／链间比较 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链对比页「产业链竞争力」排序、链详情页五子项条形图 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_COMPETITIVENESS_INDEX.md` |

## 口径定义

八项依赖里，**五项**（人均营收、研发强度、论文、人才、机构）要么分子分母交集不足、要么没有「主体—链」桥；**两项**（有效专利、融资事件）全量可用；**一项**（政策覆盖）连链标签都没有。合成只能用「企业规模 + 创新密度 + 创新广度 + 资本活跃 + 环节覆盖」五条代理，故按 §〇 判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_COMPETITIVENESS_INDEX.md` §二（M_CHAIN_COMPETITIVENESS_INDEX.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_financing_info`
- `dwd_org_industry_tags`
- `dwd_org_stock_finance_info`
- `dwd_patent`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：王惠三维八项里只有 2 项在 gkx 有全量源（有效专利、融资事件），企业维的另外两项（人均营收、研发强度）字段存在但不可用：研发额仅 876 家企业有正值（0.46%）；人均营收的分子分母都存在但交集极小——employees_number 在 stock 表 40,239 行中 0 行有值、annual 表 3,170 行 >0，operating_revenue 在 annual 表 2,191 行 >0，两者同时 >0 仅 1,288 行 / 850 家企业（底册 0.45%），且 operating_revenue 同表内量级跨 12 个数量级（0.06 → 2.72e10，含 -443.71 负值），人均值 0.0059—93,967,560 元/人，不可横比。学术维三项（论文、人才、机构）则不可得：营收记录 41586 行按企业名挂链仅 27350 行（65.77%）、论文机构 2070 家中仅 1 家能挂链、学者的链标签与政策的链标签在库内无字段。本件用 5 条可算子项（企业规模、专利密度、专利广度、融资密度、环节覆盖）做等权合成，指数 12 条链全部有值，但缺 5 项意味着「竞争力」只剩规模与创新两面，学术与政策两面缺失。故判部分支持。
- **基期声明**：截面指数：5 个子项全部取全库存量，无年度分母。专利侧只用存量申请量，不构造年度序列，因此不涉及 2021 年以前零行的问题。
- **复现实测耗时**：约 0.2 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_COMPETITIVENESS_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_COMPETITIVENESS_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_COMPETITIVENESS_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

