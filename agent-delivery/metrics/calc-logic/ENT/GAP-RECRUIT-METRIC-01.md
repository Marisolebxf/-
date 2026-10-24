# 深圳连接度（GAP-RECRUIT-METRIC-01）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/GAP-RECRUIT-METRIC-01.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-RECRUIT-METRIC-01.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-RECRUIT-METRIC-01_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | GAP-RECRUIT-METRIC-01 |
| 指标名称 | 深圳连接度 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业招引 |
| 更新频率 | 未定义 |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技专题服务系统 → 企业综合竞争力评估 / 招引企业推荐 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/GAP-RECRUIT-METRIC-01.md` |

## 口径定义

「深圳连接度」问的是「这家企业与深圳有多少经济联系」，本质是一个**比例**：对端落在深圳的关系数 ÷ 全部关系数。三类边（投资、股东、子公司）在 gkx 都有真实行，底册有 `city` 可判属地，比例当场可算；唯一缺的是「供应链」这一类边，而它是旧稿的第三个推测维、不是需求原文的必需维。因此判**完全转换支持**，同时把「只用资本/组织边」「子公司用名称代理」两条边界写在发布口径里。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/GAP-RECRUIT-METRIC-01.md` §二（GAP-RECRUIT-METRIC-01.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_base_out`
- `dwd_org_base_info`
- `dwd_org_invest_info`
- `dwd_org_shareholder_info`
- `dwd_org_subsidiary_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：「深圳连接度」问的是「这家企业与深圳有多少经济联系」，本质是一个**比例**：对端落在深圳的关系数 ÷ 全部关系数。三类边（投资、股东、子公司）在 gkx 都有真实行，底册有 `city` 可判属地，比例当场可算；唯一缺的是「供应链」这一类边，而它是旧稿的第三个推测维、不是需求原文的必需维。因此判**完全转换支持**，同时把「只用资本/组织边」「子公司用名称代理」两条边界写在发布口径里。
- **基期声明**：截面件：投资/股东/子公司三类边均无统一发布年度键，不构成年度序列，不做同比/CAGR，也不把缺失年摊 0。
- **复现实测耗时**：约 15.9 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/GAP-RECRUIT-METRIC-01.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-RECRUIT-METRIC-01.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-RECRUIT-METRIC-01_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

