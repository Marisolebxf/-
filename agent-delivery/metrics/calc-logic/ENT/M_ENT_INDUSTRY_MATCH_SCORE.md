# 产业匹配度（M_ENT_INDUSTRY_MATCH_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_INDUSTRY_MATCH_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_INDUSTRY_MATCH_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_INDUSTRY_MATCH_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_INDUSTRY_MATCH_SCORE |
| 指标名称 | 产业匹配度 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 算法库「招引企业综合推荐模型」§1.1.1.1.1.1.1.5.7 产业相关度维度（SRS 需规清单序号 147）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_INDUSTRY_MATCH_SCORE.md` |

## 口径定义

无「产业匹配度」结果面（calc-logic 落表 `M_ENT_INDUSTRY_MATCH_SCORE.md` 结果页待建）→ 非完全直接支持；方法核心输入《中国投入产出表》（a_ij 直接消耗系数、Y_i 总产出、X_i 最终消费）**两库皆无**（io 类表空集）——公式 1—2（A 矩阵、A₂）、公式 6（上游度 u_i）无源，ind_link、质心 c、d_f、ind_chain_f 全链不可算；收入权重侧 main_business_revenue 填充 2,046/90,926（2.2%）薄；图谱边 shareholder 400,286/subsidiary 178,900 在（投资边缺既往已证）→ **部分支持**（IO 表为统计局公开可下数据，外采可解，但当前两库均无）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_INDUSTRY_MATCH_SCORE.md` §二（M_ENT_INDUSTRY_MATCH_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_annual_financial_info`
- `dwd_org_industry_tags`
- `dwd_org_invest_info`
- `dwd_org_sc_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：方法核心输入《中国投入产出表》两库皆无（io 类表空集）——a_ij/Y_i/X_i 无源，ind_link（公式1-2/5）、上游度 u_i（公式6）、质心 c、d_f、ind_chain_f 全链不可算；收入权重侧 main_business_revenue 填充 2040/90926（薄）；图谱边 shareholder 400,286/subsidiary 178,900 在（投资边缺既往已证）。IO 表为统计局公开可下（2020 年 153 部门表）——外采可解，但当前两库均无 → 部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_INDUSTRY_MATCH_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_INDUSTRY_MATCH_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_INDUSTRY_MATCH_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

