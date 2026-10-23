# 城市平均商业力（GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER |
| 指标名称 | 城市平均商业力 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 深圳企业现状分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 多城市横向对标 Tab（城市×指标对比表）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER.md` |

## 口径定义

live `sz_city_benchmark` 0 行（结果面存在但全空，mock 期）→ 非完全直接支持；企业商业力六维中**市场（营收）、产品（产品标签）、产业链参与（主营构成/链环节标签）三维结构可得且已现转出分**（深圳 20,645 家、广州 11,320 家），但 **品牌指标与技术合作指标两维在开发库与三方库均无可用结构**（无驰名商标/品牌声量表、无技术合作合同表），属「始终缺 2/6 维」的持续性维度缺口 → **部分支持**（不因其余维量足而升档）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER.md` §二（GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_main_business_composition_industry`
- `dwd_org_base_info`
- `dwd_org_income_statement`
- `dwd_org_industry_product_tags`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：营收信号覆盖 3076 家、产品标签 2 家、链标签 34969 家、主营构成 374 家；深圳出分企业 20645 家、对标 5 城中 4 城有分。bid §5.6 六维中「品牌指标、技术合作指标」两维在开发库/三方库无可用结构（无驰名商标/技术合作合同表），始终缺 2/6 维 → 按四档定义属部分支持（维度缺口持续，不随量增长消失）；其余维结构+当前数据量足且已现转出分。正式权重与指标库构成待 Q014、ID 注册待何老师。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

