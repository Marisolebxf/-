# 企业实体识别构建（M_ENT_GRAPH_108_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_GRAPH_108_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_GRAPH_108_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_GRAPH_108_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_GRAPH_108_1 |
| 指标名称 | 企业实体识别构建 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业服务／企业图谱／实体库 |
| 更新频率 | 建议季度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业图谱页「关联网络」+ 节点详情卡｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_GRAPH_108_1.md` |

## 口径定义

189,116 个节点、117,001 条边可建图，最大连通分量 10,462 家、孤立率 89.54%，但没有文本 NER、节点权重与标注集，判部分支持。

## 计算逻辑说明

```text
节点 = DISTINCT org_id；边 = 投资 + 股东关系；度 = 入边+出边；连通分量 = 并查集
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_GRAPH_108_1.md` §二（M_ENT_GRAPH_108_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_invest_info`
- `dwd_org_shareholder_info`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：graph_node 结果面不存在，但实体库的骨架可以从结构化表直接建起来：189,116 个节点（org_id 唯一）、117,001 条关系边（其中 116,997 条两端都在主档内）、属性覆盖率可逐项统计，图结构（连通分量、度分布、孤立率）也能算。缺的是新闻文本的 NER 抽取与实体链接，以及节点权重与标注集验收，故判部分支持。
- **基期声明**：本件是图结构与属性覆盖的截面统计，不做年度序列，故无基期年份；主档与关系表都是当前快照，无历史版本，无法观察图结构的年度演化。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_GRAPH_108_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_GRAPH_108_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_GRAPH_108_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

