# QA-KJZTFWXT-FUNCLIST-SPLIT-L01 · 需求功能清单功能点拆分-专题系统

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:黄敬洲` |
| supervised_by | `human:黄敬洲` |
| claim_type | `coordinator_dispatch` |
| 说明 | 本轮按监管人确认口径执行：只拆战略分析 5 个四级；测试步骤不写；超条数不裁。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（QA 拆点 / 合表文档；生成脚本仅合表，未新造业务抽象） |
| 说明 | 拆点未用 YAGNI 跳过公约要求的 handoff / cost；本次不写 UI，D8/D9/D10 不适用。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未把 Headroom 用于本任务。 |

## 范围与实现

- 系统：科技专题服务系统
- 功能模块：科技专题战略分析
- 四级（5）：产业服务链分析、产业链分析、企业分析、政策分析、综合智能分析
- 工作单元：32 个五级（T01–T32），金样 T11 锁定后全量并行
- 需求源：功能清单 v1.2 sheet「科技专题服务系统」五级/六级名称 + 需规全文
- 产出：总集 FUNC Excel **v8**，1298 条；编号 `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00001`–`01298`
- 列：用例编号 / 功能模块 / 子功能模块 / 功能项 / 子功能项 / 页面 / 功能点 / 拆分维度 / 规则来源 / 需规描述；测试内容、前置条件、测试步骤、预期结果留空

对照 bid-reference：科技专题战略分析叶子功能点拆分（本轮不含数据查询 / 项目管理 / 信息发布 / 运营中心 / 系统管理）。

## 偏离说明

| registry / 派单包原文 | 本轮 as-built | 理由 |
|---|---|---|
| 覆盖 6 个 L3 | 只拆战略分析 5 个四级 | 开工后监管人收窄范围 |
| 战略分析补技术链 / 科研机构 / 人才 | 未拆这 3 个四级 | 同上 |
| 内容用八件套 + 原型完善 | 拆点禁止读五件套 / demo-ui-topic | 监管人指定需规为唯一需求源；五件套加严留给以后写步骤 |
| 用例正文（前置/步骤/预期） | 不写 | 监管人确认本任务不写测试步骤 |
| 目标 1140–1260 条 | 合表 **1298** 条，不裁 | 监管人确认数量超出没关系 |
| 复用 v1.3 五册文案 | 未复用；按需规重拆功能点 | 功能点列锁需规，不锁旧用例 Excel |

后续若要覆盖其余 L3 / 3 个四级 / 写测试步骤，应另开任务，不要把本 v8 当成全系统总集。

## 产物清单

| 产物 | 路径 |
|------|------|
| 正式合表 v8 | `agent-delivery/qa/total-set/KJZTFWXT/6.国际科技信息中心项目_科技专题服务系统_功能点拆分_v8.xlsx` |
| 五级工作稿 | `agent-delivery/qa/total-set/KJZTFWXT/fp-split-run/work/T01.md`–`T32.md` |
| 五级自检 | `fp-split-run/review/T01.md`–`T32.md` |
| 提示词 | `fp-split-run/prompts/` |
| 原则 | `科技专题战略分析-最细颗粒度功能点拆分原则-v1.md` |
| 合表脚本 | `agent-delivery/scripts/_merge_fp_split_work.py` |
| 本 handoff | `agent-delivery/agent-handoffs/QA/QA-KJZTFWXT-FUNCLIST-SPLIT-L01.md` |

合表前试验稿（v1–v7 Excel、v1.0–v1.3 旧用例册）监管人已删，不纳入本交付。

## 验收证据

- 32/32 五级 `work`+`review` 落盘；自检均为通过；抽检未见误用原型/五件套
- v8：`功能测试用例` 数据行 1298，编号无重复；测试步骤列全空
- 按四级：产业链 305 / 企业 384 / 政策 127 / 产业服务链 327 / 综合智能 155

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | N/A（无代码算法） |
| 2 | 前端 → Java REST → Python `/internal/*` | N/A |
| 3 | 图谱 NebulaGraph | N/A |
| 4 | 可观测性三件套 | N/A |
| 5 | CI/CD | `cicd: skip`（编排仓文档 / Excel） |
| 6 | demo2 不 merge 进 lumen | N/A |
| 7 | 共享聚合核心 | N/A |
| 8 | 数据策略 ADS / Mock | N/A（拆点不取数） |
| 9 | D8 Design / Arco | N/A |
| 10 | D9 指标 8 件套 | N/A（本轮不写页面指标卡） |
| 11 | D10 交互规范 | N/A |

## Cost（必填）

| 字段 | 值 |
|------|-----|
| actual_tokens | 2200000（估算；source: session_estimate，非 console 精确值） |
| model_used | grok-4.6 |
| actual_cost | 11.88（按 qa 默认 80/20、Sonnet 公开价 $3/$15 每百万 token 折算，仅作量级） |
| cost_warn | orange（>$10；32 个五级并行子 agent + 编排会话） |

未暂停：监管人要求开全量并行；本任务为拆点合表，已收工。

## CI/CD（必填）

- 分支：编排仓当前工作区默认分支
- commit：本 handoff 同批提交
- pipeline URL / ID：skip（文档 / Excel）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL：N/A

## 遗留风险

- registry 原文 DoD 仍写 6 个 L3 + 写步骤；签收本任务 = 签收「战略分析 5 个四级功能点表」，不是全系统总集
- 写测试步骤时需另锁五件套 + 原型；与需规冲突标缺口，不当 Fail

## 问题清单

- 无阻塞。勿自行 `done`；tech_task 请 coordinator / 签收人推进。
