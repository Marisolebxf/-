# 痛点主题（M_ENT_PAINPOINT_TOPIC）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PAINPOINT_TOPIC.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PAINPOINT_TOPIC.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PAINPOINT_TOPIC_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_PAINPOINT_TOPIC |
| 指标名称 | 痛点主题 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业服务／企业诊断／痛点归因 |
| 更新频率 | 建议月度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业画像「痛点主题」标签 + 主题分布饼图｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_PAINPOINT_TOPIC.md` |

## 口径定义

699,003 条痛点记录可归入 9 个规则主题，债务违约占 89.61%；但主题只覆盖合规侧、无经营主题与语义聚类，判部分支持。

## 计算逻辑说明

```text
topic = f(风险表, 结构化原因字段)；records = Σ 命中条数；share = 该主题条数 / 全部痛点条数
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PAINPOINT_TOPIC.md` §二（M_ENT_PAINPOINT_TOPIC.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_company_abnormal`
- `dwd_org_company_illegal`
- `dwd_org_company_punish`
- `dwd_org_risk_shixin`
- `dwd_org_risk_zhixing`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：痛点诊断结果面不存在，但主题构造所需的结构化原因字段在库内是真实的：经营异常 5,862 条带 abn_reason 原文（可拆四类），失信 76,035、被执行 550,334、处罚 65,997、严重违法 247、税务处罚 528 都能直接映射主题，合计 69.9 万条。规则主题可复现、可对回原始记录，故判部分支持；缺少经营侧痛点与语义主题，主题体系只覆盖合规侧。
- **基期声明**：风险表是事件流水，本件按「截至抓取时点的累计条数」归类，不做年度切分，故无基期年份；表内带发生日期，年度主题迁移需另做按年聚合。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PAINPOINT_TOPIC.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PAINPOINT_TOPIC.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PAINPOINT_TOPIC_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

