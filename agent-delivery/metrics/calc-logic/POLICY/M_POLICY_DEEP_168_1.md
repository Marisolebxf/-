# 政策效果评估模型（M_POLICY_DEEP_168_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_DEEP_168_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DEEP_168_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DEEP_168_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_DEEP_168_1 |
| 指标名称 | 政策效果评估模型 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务算法库 → 深度分析模型 → 政策效果评估 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | ["2016", "2017", "2018", "2019", "2020", "2021"] |
| 缺失年份 | ["2023"] |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_DEEP_168_1.md` |

## 口径定义

三维里 D1（执行）只剩「有效占比」，而 `status` 全表 20,000 行都是「有效」，这个 100% 是**样本框构造**而不是治理成效；及时性子项因实施日与失效日全是 `0000-00-00` 而不可算。D2（社会经济效应）需要「政策—企业」关联键与企业营收/就业序列，两样都没有，整维缺失。D3（环保导向）靠 25 词闭集在正文里命中 4,116 条（20.58%），是唯一有真值的一维。故落**部分支持**，且对外只发布 D3。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_DEEP_168_1.md` §二（M_POLICY_DEEP_168_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三维里 D1 只剩有效占比（且是样本构造性 100%）、及时性子项因零日期不可算；D2 社会经济效应在库内无表无键；D3 环保导向可用。缺一个必需维 + 一个子项 → 部分支持。
- **基期声明**：政策级指数为截面口径，不涉时序分母；分年环保导向率只用 2016—2021 六个连续年份。2023 年库内 0 行、2022 年 289 条残片、2024 年 1 条均不入分母（DATA_FACTS §3.16）。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_DEEP_168_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DEEP_168_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DEEP_168_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

