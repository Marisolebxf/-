# 区域竞争力指数（CI = competitiveness index）（M_INNOV_RES_REGION_CI）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_RES_REGION_CI.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_RES_REGION_CI.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_RES_REGION_CI_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_RES_REGION_CI |
| 指标名称 | 区域竞争力指数（CI = competitiveness index） |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 区域竞争力对比页——四维雷达、区域排名表、差距分解条 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_RES_REGION_CI.md` |

## 口径定义

四维全部能算出数、4 个区域每维都有值（取数齐备率 4 城 × 4 维 = 16/16），但**区域集合只有深圳都市圈 4 市**（占底册 66 个城市取值的 6.06%），结构维的发明占比只有 6.80% 抽样、研发费用只有上市主体口径、政策维东莞 8 条 / 惠州 0 条属采集覆盖不足——按定义「始终有部分依赖维得不到足够数据」，判**部分支持**，不因为脚本跑通就升档。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_RES_REGION_CI.md` §二（M_INNOV_RES_REGION_CI.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_stock_finance_info`
- `dwd_org_tech_tag`
- `dwd_patent`
- `dwd_policy_base`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四维全部能算出数、4 个区域每维都有值（取数齐备率 4 城 × 4 维 = 16/16），但**区域集合只有深圳都市圈 4 市**（占底册 66 个城市取值的 6.06%），结构维的发明占比只有 6.80% 抽样、研发费用只有上市主体口径、政策维东莞 8 条 / 惠州 0 条属采集覆盖不足——按定义「始终有部分依赖维得不到足够数据」，判**部分支持**，不因为脚本跑通就升档。
- **基期声明**：dwd_patent.apdt_year 只有 2021—2026，2017—2020 一行都没有；四维合成本身是 2024 年截面，不涉及时序分母。增速只作规模动态参考、不入合成，且分母只取真实存在的 2021 年，不把缺失年按 0 摊入。2025 年为残年（440,401 件）、2026 年更残，均不进基期也不作终点。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_RES_REGION_CI.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_RES_REGION_CI.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_RES_REGION_CI_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

