# 服务机构投融资动态（M_SVC_INVEST_Y）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_INVEST_Y.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_INVEST_Y.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_INVEST_Y_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_INVEST_Y |
| 指标名称 | 服务机构投融资动态 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（投融资动态资讯） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·投融资动态（§1.1.1.2.4.2.3）/ 算法库·服务机构基础指标模型（序号 101） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025] |
| 缺失年份 | [2026] |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_INVEST_Y.md` |

## 口径定义

需求要的是「投融资数量 + 金额」，gkx 只能兑现**融资事件计数**：`dwd_org_financing_info` 25,654 行，池内 24,391 件、覆盖 5,910 家机构，日期锚 100%，峰值 2016 年 3,704 件；投资侧无事件表、金额列整列为空、无 INVEST/FINANCING 类型列，故落 **部分支持**。本件与 `M_SVC_ORG_TOTAL` 等九件同池（44,153 家），池规则见其 §2.2。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_INVEST_Y.md` §二（M_SVC_INVEST_Y.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_financing_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：融资事件年度序列可现转（24,391 件、43 个年份、日期锚 100%）；但 gkx 只有 dwd_org_financing_info， INVEST 侧无事件表，且金额列整列为空，需求中的「投融资数量+金额」只能兑现融资事件计数
- **基期声明**：趋势表取 2000—2025；2026 只有 233 件、采集时点未过完，按残年处理不进趋势。1980—1999 年段事件极少，只进全量序列、不作趋势

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_INVEST_Y.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_INVEST_Y.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_INVEST_Y_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

