# handoff · SYSINT-CHAIN-ELEM-LINK-02-L01

> 任务：产业链节点 × 三要素（技术/人才/机构）关联可行性深调。WBS-02-17，spike，P0。
> 认领/执行：human:淮政玮（2026-11-04 认领，doc-agent 执笔）。监管人：human:唐绍祖。
> 状态：**integration**（判定记录已产出，待监管人复核）。
> ponytail: off（调研任务，判定完整性优先）。

## 范围与实现

产出 [`调研/CHAIN-ELEM-LINK可行性判定记录.md`](../调研/CHAIN-ELEM-LINK可行性判定记录.md)：链节点粒度上技术/人才/机构三要素挂链的三条候选通路逐一判定 + 供给缺口清单（喂阶段二圈表）。

核心结论：

| 要素 | 通路 | 判定 | 说明 |
|---|---|---|---|
| 技术 | `dwd_tech_node_industry_map` 直读 | **绿** | 表已存在且有 **20,257 行 / 159 产业 / 全部挂 technology_node_id**——WBS-02-12 产物已落库，XJOIN 判定记录中「本仓未实装」的说法过时，需更正 |
| 人才/机构 | 通路② GB 码对 GB 码 | **黄** | 久新两侧挂接点均为 GB/T 4754（talent `industry_activity` 39.8 万行 / institution `industry_industry` 135 万行，taxonomy `CN_GB4754_IPC`）；我方链是自造 INB 码，INB→GB 对照表由我方建（≤1,220 行，GB 公开标准），久新抽查 |
| 兜底 | 通路① LLM 层 L0 归并 | 可用 | `subfield_topic_map` 89 个 node_id **89/89 命中**链节点树（零码域偏差），12 根族全覆盖；节点级仅 7.3%（89/1220），回退 L0 聚合须界面标注粒度 |
| 两跳 | 链→学科→集群映射 | 不作独立通路 | 只作通路①的交叉校验源 |

## 偏离说明

无范围偏离。一处**对既有判定的更正**：XJOIN 判定记录写「`dwd_tech_node_industry_map` 本仓未实装」，本叶实查发现该表已落 20,257 行——场景 2 的技术侧挂链状态应由红→黄上调为绿（表级），质量核验归 WBS-02-12 签收流程。已在本判定记录留痕，XJOIN 记录不改原文（其自带「重跑出增补记录」约定）。

## 产物清单

- 判定记录：`agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/CHAIN-ELEM-LINK可行性判定记录.md`
- 探针（只读）：`chainlink_our.py`（我方链盘点）/ `chainlink_bridge.py`（两侧码域）/ `chainlink_hitrate.py`（命中率）
- registry：claimed → in_progress → integration（本日）

## 验收证据

- 三通路均有两侧实查数据支撑：命中率 89/1220 与 12/12 根族、GB 码层级实测、久新两张挂接表行数字段实测。
- 供给缺口清单 4 项，逐项落责任方（我方建桥/我方圈表/久新抽查/我方核验）。
- 未建映射、未写业务代码、全程只读。

## 架构合规自检

- 探针只读（SELECT/SHOW），密码走环境变量/helm values，不落 git。✅
- 诚实性红线写死：L0 回退须标聚合粒度；GB 桥建成前不得假节点级过滤；tech map 未签收不得当已验收源。✅
- D12：未引入 demo 调用。✅ D9：不触指标库。✅

## 后续承接

| 结论 | 去向 |
|---|---|
| 技术侧挂链 | WBS-02-12 签收流程补质量核验（20,257 行置信度 + 159 产业对 12 根族覆盖） |
| GB 桥 | 新建小叶（INB→GB 对照 ≤1,220 行）或并入阶段二圈表任务；对照质量抽查并入 51 行回复 |
| 圈表增补 | `ads_talent_industry_activity`、`ads_institution_industry` 进主文档 §4 阶段二圈表清单（附页 A 增补） |
| 演示 | 人才/机构按链节点的区块：GB 桥建成前走 L0 聚合 + 粒度标注，不空态（通路①兜底） |

## 成本

actual_tokens ≈ 50000（3 轮探针 + 判定撰写）；model_used = glm-5.3-flash；actual_cost ≈ $0.05；cost_warn = green。

## 签收

待 human:唐绍祖 复核 → human:淮政玮 签收。演示前（11-15）判定不变即闭环；GB 桥落地后本记录的「黄」两项升绿，出增补记录。
