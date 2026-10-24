# 深圳产业服务机构数量（M_SVC_PT_SZ_TOTAL）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_SZ_TOTAL.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_SZ_TOTAL.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_SZ_TOTAL_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_PT_SZ_TOTAL |
| 指标名称 | 深圳产业服务机构数量 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（深圳供给面） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技专题服务系统·专题服务门户 SVCCHAIN-PORTAL（TOPIC-PT-004）深圳专题；展示侧呼应科技信息展示系统·产业服务链分析→服务机构库（深圳切片） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [1979, 2025] |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_PT_SZ_TOTAL.md` |

## 口径定义

深圳切片的数量、成立年累积序列、区级对账三面在 gkx 全部可现转：切片 **25,597** 家、序列 47 期（1979—2025）、区级 25,587＋未分配 10＝25,597、序列期末＋无年份＝25,597。「结构 + 当前数据量」双足，当日即可转换出数 → **完全转换支持**。这也是本批九件里唯一不依赖海外轴、且三面闭合的两件之一（另一件是 `M_SVC_PT_SZ_REGION_ORG`）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_SZ_TOTAL.md` §二（M_SVC_PT_SZ_TOTAL.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_org_product_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：深圳切片的数量、成立年累积序列、区级对账三面在 gkx 全部可现转：切片 25597 家、区级分布加总与切片完全一致（25587＋未分配 10＝25597）、序列期末＋无年份＝切片；依赖字段（city/incorporation_year/area）覆盖 99.96% 以上，「结构+当前数据量」双足，当日即可转换出数
- **基期声明**：深圳切片成立年序列覆盖 1979—2025（47 个有值年，区间内 0 年零出生不补 0）；0 家无成立年者计入切片值但不进序列。2025 年之后无出生记录是底册登记滞后，不解读为新增归零。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_SZ_TOTAL.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_SZ_TOTAL.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_SZ_TOTAL_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-13: v0.2.1 补真数修订：city 经 dwd_org_base_info JOIN 取（池表无 city 列，企业最全信息主档）；现池深圳真数 14,033（池 43,296 城市分布：广州 19600/深圳 14033/东莞 7908/惠州 1751/京甬 4，全命中主档）；「43296 全池在深圳」的旧表述作废。
- 2026-10-13: v0.2.0 整文件覆盖旧版（旧版 2026-08-21 模拟王惠调研产出，含已过时 1355/3525 与 svc_metric_fact 旧行引用，一律作废；以本版为准）。human:徐滕强 确认。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

