# 产业链节点服务机构数（M_SVC_PT_CHAIN_NODE_ORG）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_CHAIN_NODE_ORG.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_CHAIN_NODE_ORG.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_CHAIN_NODE_ORG_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_PT_CHAIN_NODE_ORG |
| 指标名称 | 产业链节点服务机构数 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（产业链节点供给） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·专题服务门户 SVCCHAIN-PORTAL 产业链节点视图；展示侧呼应科技信息展示系统·产业服务链分析→节点服务机构 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_PT_CHAIN_NODE_ORG.md` |

## 口径定义

产业 × 环节交叉格可出数（**12 个产业 × 6 环节 = 72 格，66 格非零**），但两张分面都是代理：环节轴的正式成员表（机构 × 产业 × 环节服务记录，SVC-P0-3）在 gkx 与 live 均不存在，产业轴覆盖率只有 40.58% 且换过词典 → **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_CHAIN_NODE_ORG.md` §二（M_SVC_PT_CHAIN_NODE_ORG.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_industry_tags`
- `dwd_org_org_product_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：产业×环节交叉格可出数（12 个产业 × 6 环节 = 72 格，其中 66 格非零），但两张分面都是代理：环节轴的正式成员表（机构×产业×环节服务记录，SVC-P0-3）在 gkx 与 live 均不存在，产业轴覆盖率只有 40.58% 且换了词典 → 部分支持
- **基期声明**：截面宽表：产业×环节交叉计数是当前存量的预统计，不含年度分母；tags 表与经营范围词表都没有可用的服务记录年份，本件不做年度序列（补 0 会把未采集年当零供给）。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_CHAIN_NODE_ORG.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_CHAIN_NODE_ORG.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_CHAIN_NODE_ORG_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-13: v0.2.0 落盘（预统计宽表 15×6=90 格；「选定产业」归查询层；术语澄清；与 SEGMENT 同源两消费禁顶替；D3=none 挂 Q-SVCCHAIN-08+SVC-P0-3）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

