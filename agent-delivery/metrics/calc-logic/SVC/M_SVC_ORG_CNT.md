# 全球服务机构分布（按国家计数）（M_SVC_ORG_CNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_CNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_CNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_CNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_ORG_CNT |
| 指标名称 | 全球服务机构分布（按国家计数） |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（全球服务机构分布） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·全球服务机构分布（§1.1.1.2.4.2.2）/ 算法库·服务机构基础指标模型（序号 101） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_ORG_CNT.md` |

## 口径定义

「全球分布」在 gkx 侧只能闭合国内一格：44,132 家经省级归并全部落在中国，21 家未回联底册单列「未判定」；覆盖国家数为 1。海外格没有任何与六类服务机构口径闭合的名录（`dwd_forg_*` 是英国偏企业名录与全球科研机构名录，语义不闭合），因此国家轴只能给「中国一格 + 空集」，按四档如实落 **部分支持**。本件与 `M_SVC_ORG_TOTAL`、`M_SVC_NEW_CNT`、`M_SVC_ORG_NEW_COUNT`、`M_SVC_ORG_MARKET_HEAT`、`M_SVC_INVEST_Y`、`M_SVC_ORG_TECH_SCORE`、`M_SVC_ORG_COVERAGE_BREADTH`、`M_SVC_ORG_COVERAGE_DEPTH` 共用同一机构池（44,153 家），池规则见 `M_SVC_ORG_TOTAL` §2.2。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_CNT.md` §二（M_SVC_ORG_CNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_`
- `dwd_org_base_info`
- `dwd_org_org_product_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：国内格可完整闭合（44,132 家经 province→中国归并、省级 drill-down 可对账）；但 gkx 底册无 country 列、无与六类服务机构口径闭合的海外名录，国家轴海外格始终无源，按四档落部分支持
- **基期声明**：截面分布指标：国家格与省级 drill-down 均为当前存量，无年度分母。趋势能力依赖成立年序列（见 M_SVC_NEW_CNT），本件不摊年。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_CNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_CNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_CNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

