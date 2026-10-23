# 关键指标集合（GAP-RECRUIT-METRIC-05）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/GAP-RECRUIT-METRIC-05.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-RECRUIT-METRIC-05.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-RECRUIT-METRIC-05_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | GAP-RECRUIT-METRIC-05 |
| 指标名称 | 关键指标集合 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业招引/培育 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 招引/培育企业推荐分析卡片（E-26/E-27，wireframe 第 6 列）｜ **数据支持度**：**完全转换支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/GAP-RECRUIT-METRIC-05.md` |

## 口径定义

「关键指标集合」不是单一数值指标而是**展示层集合规则**——handoff 明确「每个实际指标带自身 metric_id，不创建笼统总分」（ER-B12）；无现成「集合」结果面 → 非完全直接支持；11 项候选组成指标全部结构可得、当前量>100，脚本已对样例企业**装配成功 3 张完整卡片**（行业/资本/规模/投资/子公司/融资/营收均可取值）→ **完全转换支持**（拼装即可，无独立公式需求）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/GAP-RECRUIT-METRIC-05.md` §二（GAP-RECRUIT-METRIC-05.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_financing_info`
- `dwd_org_income_statement`
- `dwd_org_invest_info`
- `dwd_org_subsidiary_info`
- `dwd_patent`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：候选关键指标 11 项中 11 项有结构、11 项当前量>100；样例企业 3 张卡片装配成功（行业/资本/规模/投资/子公司/融资/营收均可取值）。本 GAP 本质是展示层集合规则：各组成指标可从现库拼装，无需独立公式；最终展示哪几项由 UX 定义（handoff ER-B12 已锁定，不建总分）。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/GAP-RECRUIT-METRIC-05.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-RECRUIT-METRIC-05.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-RECRUIT-METRIC-05_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

