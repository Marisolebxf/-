# QA-KJXXZSXT-FUNCLIST-SPLIT-L01 · 需求功能清单功能点拆分-展示系统

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:黄敬洲` |
| supervised_by | `human:黄敬洲` |
| claim_type | `pull` |
| 说明 | 范围锁 606 六级 / 140 五级；金样 T27；不写测试步骤；整表 ≥6000 不裁。 |

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

- 系统：科技信息展示系统（系统码 KJXXZSXT）
- 输入：功能清单 v1.2 sheet「科技信息展示系统」需规区 G–M
- 工作单元：140 个五级 T01–T140（招标七模块 123 + 政策对比核增 17）
- 六级覆盖：**606**（招标七模块 589 + 政策对比核增 17）
- 金样：T27 技术创新力指标展示（92 条，已锁定后全量）
- 需求源：各五级 `prompts/Txx.md` 的五级/六级名 + 需规全文。禁止读 `demo-ui-science`、五件套、专题 v8 Excel、其它 Txx 业务点。金样 `work/T27.md` 只学表头/列/拆法
- 产出：总集 FUNC Excel **v1**，**8378** 条（≥6000）；编号 `ZNFWJQ-KJXXZSXT-v1.0-FUNC-00001`–`08378`
- 列：用例编号 / 功能模块(=三级名) / 子功能模块 / 功能项 / 子功能项 / 页面(=五级名) / 功能点 / 拆分维度 / 规则来源 / 需规描述；测试内容、前置条件、测试步骤、预期结果留空
- 子功能项 = 六级名；政策核增六级为 `/` 时填五级名

对照 bid-reference：展示系统七模块叶子功能点拆分；政策对比核增 17 个五级一并纳入本轮 606。

## 偏离说明

| registry / 派单包原文 | 本轮 as-built | 理由 |
|---|---|---|
| 覆盖该 sheet 全部 L3 | 不含三级「科技信息展示系统数据需求」（73 行） | 监管人锁定功能点范围，数据需求不进 FUNC |
| 覆盖该 sheet 全部 L4 | 不含四级「科技抗疫主题报告（核减需求）」（12 行） | 核减需求不拆 |
| 两层排除后仍剩 684 六级行 | 学习类核增 78 个五级 T141–T218 `skipped`（六级名为 `/`） | 监管人确认本轮 = 招标七模块 589 + 政策对比核增 17 = **606**，不是 684 |
| 建议 ≥6000 | 合表 **8378**，不裁 | 监管人确认可以略多、不能少 |
| 用例正文（前置/步骤/预期） | 不写 | 监管人确认本任务不写测试步骤 |

学习类核增若以后要拆，应另开任务，不要把本 v1 当成含学习路径/知识图谱核增的全 sheet 总集。

## 产物清单

| 产物 | 路径 |
|------|------|
| 正式合表 v1 | `agent-delivery/qa/total-set/KJXXZSXT/6.国际科技信息中心项目_科技信息展示系统_功能点拆分_v1.xlsx` |
| 五级工作稿 | `agent-delivery/qa/total-set/KJXXZSXT/fp-split-run/work/T01.md`–`T140.md` |
| 五级自检 | `fp-split-run/review/T01.md`–`T140.md` |
| 提示词 | `fp-split-run/prompts/` |
| 原则 | `fp-split-run/科技信息展示系统-最细颗粒度功能点拆分原则-v1.md` |
| 控制面 / 队列 / 盘点 | `fp-split-run/00-control.md` · `01-task-list.md` · `02-inventory.md` |
| 合表脚本 | `agent-delivery/scripts/_merge_kjxxzsxt_fp_split_work.py` |
| 表头核对 | `agent-delivery/scripts/_check_kjxxzsxt_fp_work.py` |
| 本 handoff | `agent-delivery/agent-handoffs/QA/QA-KJXXZSXT-FUNCLIST-SPLIT-L01.md` |

## 验收证据

- 140/140 五级 `work`+`review` 落盘；`_check_kjxxzsxt_fp_work.py` 全部 OK；合表 `rows=8378`、`mismatches=[]`；测试步骤列全空
- 编号 `ZNFWJQ-KJXXZSXT-v1.0-FUNC-00001`–`08378` 无重复
- 140 份 review 均含「通过」；抽检「是否误用了原型或五件套」均为否
- 按三级：科技发展态势 2785 / 科技成果展示 1221 / 科技人才态势 1219 / 科技数据资源 915 / 科技知识图谱 753 / 科技政策跟踪 650 / 科技服务全景 573 / 政策对比功能升级（核增需求）262
- 按波次（T27 金样 92 条单独计，波次 3 区间不含 T27 为 848）：

| 波次 | 五级 | 条数 |
|---|---|---:|
| 金样 | T27 | 92 |
| 1 | T01–T10 | 718 |
| 2 | T11–T20 | 758 |
| 3 | T21–T26、T28–T31 | 848 |
| 4 | T32–T41 | 788 |
| 5 | T42–T51 | 779 |
| 6 | T52–T61 | 739 |
| 7 | T62–T71 | 535 |
| 8 | T72–T81 | 555 |
| 9 | T82–T91 | 674 |
| 10 | T92–T101 | 614 |
| 11 | T102–T111 | 557 |
| 12 | T112–T121 | 387 |
| 13 | T122–T131 | 198 |
| 14 | T132–T140 | 136 |
| **合计** | T01–T140 | **8378** |

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | N/A（无代码算法） |
| 2 | 前端 → Java REST → Python `/internal/*` | N/A |
| 3 | 图谱 NebulaGraph | N/A |
| 4 | 可观测性三件套 | N/A |
| 5 | CI/CD | `cicd: skip`（编排仓文档 / Excel） |
| 6 | demo2 不 merge 进 lumen | ✅ 未改任何 demo/lumen 业务仓 |
| 7 | 共享聚合核心 | N/A |
| 8 | 数据策略 ADS / Mock | N/A（拆点不取数） |
| 9 | D8 Design / Arco | N/A |
| 10 | D9 指标 8 件套 | N/A（本轮不写页面指标卡） |
| 11 | D10 交互规范 | N/A |
| 12 | D12 demo/lumen 隔离 | ✅ 未调用、未 merge 任何 `demo-*` 服务或代码进 lumen |

## Cost（必填）

| 字段 | 值 |
|------|-----|
| actual_tokens | 9600000（估算；source: session_estimate。按专题同型任务 32 五级 ≈2.2M 线性外推 140/32；无 Console 精确值） |
| model_used | grok-4.6 |
| actual_cost | 51.84（qa 默认 80/20、Sonnet 公开价 $3/$15 每百万 token：`9600000×(0.8×3+0.2×15)/1e6`） |
| cost_warn | red（>$20；1 父会话 + 约 139 子 agent 全量拆点。registry `estimated_tokens=200000` 严重低估） |

未暂停合表：监管人已要求金样通过后全量并行；拆点与合表已收工。**请 PM / architect 知会本条 red**（预算规约单任务 >$20 须评审是否拆分；本任务范围已锁死且产物已齐，不宜再拆执行）。

## CI/CD（必填）

- 分支：`gkx-orchestration` `origin/dev`
- commit：本 handoff 同批提交
- pipeline URL / ID：skip（文档 / Excel，编排仓无业务 CI）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL：N/A

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A（非运行时代码）
- traceId：N/A
- Tempo / Loki：无

## 遗留风险

- 学习类核增 78 个五级未拆；签收本任务 = 签收「606 六级功能点表」，不是功能清单 sheet 全剩余 684 行
- 写测试步骤时需另锁五件套 + 原型；与需规冲突标缺口，不当 Fail
- cost 为 session_estimate，非 console 精确值；量级 red 属实

## 问题清单

- 无阻塞。勿自行 `done`；`tech_task` 请 `human:淮政玮` 签收推进。
