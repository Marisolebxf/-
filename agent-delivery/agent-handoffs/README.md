# Agent handoffs

各子 agent 完成任务后在此目录提交结构化报告。已按**业务/功能**汉字子目录归集，方便人工浏览。

- **格式参考**：`../templates/handoff-template.md`、`../formal-docs-registry.yaml`（章节/版式）
- **内容**：按 task 实测填写；读 V6 **样式** 用 officecli（见 `../officecli-doc-workflow.md`）
- **过程稿归档**：`../_archive/2026-08/`（非执行真源）

## 子目录索引

| 子目录 | 业务/Epic | 说明 |
|--------|-----------|------|
| [`软科学成果展示-DS25/`](./软科学成果展示-DS25/) | DS-25 | 试点 UX/UI + PILOT |
| [`科技人才态势-DS15/`](./科技人才态势-DS15/) | DS-15 | 首次试点 + D8 retrofit |
| [`科技创新生态展示-DS26/`](./科技创新生态展示-DS26/) | DS-26 | 生态展示 trial |
| [`大型科学仪器共享-DS28/`](./大型科学仪器共享-DS28/) | DS-28 | 仪器共享 trial |
| [`科技新闻-TECH-NEWS/`](./科技新闻-TECH-NEWS/) | TECH-NEWS IE/ENTITY | 科技新闻抽取与实体里程碑 handoff |
| [`高端智库-ZHIKU/`](./高端智库-ZHIKU/) | E-ZHIKU-PROTOTYPE-110 | S0–S6 脚手架 + R1–R6 模块重跑；定义包见 `产品整体定义/E-ZHIKU-新型高端智库/` |
| [`展示对齐-DISPLAY/`](./展示对齐-DISPLAY/) | E-DISPLAY-ALIGN | FE-DISPLAY-* 符合度对齐 handoff；截图见 `evidence/` |
| [`企业战略分析-ENT/`](./企业战略分析-ENT/) | ENT | 企业专题全角色 + READINESS/OPS/KEYENT |
| [`产业链分析-CHAIN/`](./产业链分析-CHAIN/) | E-CHAIN / SVCCHAIN | 产业链 + TOPIC-SVCCHAIN |
| [`综合智能分析-SYNTH/`](./综合智能分析-SYNTH/) | E8 / TOPIC-SYNTH | SYNTH-MOD Pack/HIFI + TOPIC-SYNTH/STRAT |
| [`政策模块-E7/`](./政策模块-E7/) | E7-POLICY / DS10-12 | 政策 Pack/UX + DS10-12 handoff |
| [`算法库联调-ALGO-LIB/`](./算法库联调-ALGO-LIB/) | ALGO-LIB / FIX-TOPIC-SEARCH | 算法联调、DWD 前缀修复、PG→MySQL |
| [`平台基建-PLATFORM/`](./平台基建-PLATFORM/) | PLATFORM/ORCH | 仓库/流水线等基础设施 |
| [`编排方法论/`](./编排方法论/) | ORCH / D9 / 清理 | 看板、D9、孤立 MD 清理 handoff |
| [`产品整体定义/`](./产品整体定义/) | 定义包 | USM/IA/Wireframe/TRACE（非实现 handoff） |
| [`交付覆盖/`](./交付覆盖/) | 交付验证 | handoff.md + validation-report |
| [`服务机构-SVC/`](./服务机构-SVC/) | SVC | 服务机构相关 |
| [`运维事件/`](./运维事件/) | INCIDENT | 事件复盘 |
| [`evidence/`](./evidence/) | 证据附件 | 截图/JSON 等（按 task-id 子目录） |

## 命名与归集规范

1. **文件名**：`{角色或Epic}-{描述}.md`（保持既有 task-id 文件名，便于 registry 对照）
2. **归集**（coordinator 派单时 evidence 路径必须带子目录）：

   | 文件名前缀 | 归集目录 |
   |------------|----------|
   | `E-TECH-NEWS-*` | `科技新闻-TECH-NEWS/` |
   | `E-ZHIKU-*` | `高端智库-ZHIKU/` |
   | `FE-DISPLAY-*` | `展示对齐-DISPLAY/` |
   | `*-DS-25-*` / `PILOT-DS-25-*` | `软科学成果展示-DS25/` |
   | `*-DS-15-*` / `D8-DS-15-*` | `科技人才态势-DS15/` |
   | `*-ENT-*` / `ENT-*` / `E-ENT-*` | `企业战略分析-ENT/` |
   | `*-CHAIN-*` / `CHAIN-*` / `TOPIC-SVCCHAIN-*` | `产业链分析-CHAIN/` |
   | `TOPIC-SYNTH-*` / `SYNTH-MOD-*` / `TOPIC-STRAT-*` | `综合智能分析-SYNTH/` |
   | `E-E7-POLICY-*` / `POLICY-*` / `DS10-*` | `政策模块-E7/` |
   | `FIX-TOPIC-SEARCH-*` / `algo-*` / `innov-java-*` | `算法库联调-ALGO-LIB/` |
   | `E-INNOV-*` / `E-PLATFORM-*` | `平台基建-PLATFORM/` |
   | `ORCH-*` / `D9-*` / `ORPHAN-MD-*` / `PM-DECISION-*` | `编排方法论/` |
   | `INCIDENT-*` | `运维事件/` |
   | 新业务 epic | coordinator 新建汉字子目录并更新本表 |

3. **本目录根只保留 `README.md`**，不放具体 handoff 文件（2026-08-10 P3 已收口）
4. **空目录用 `.gitkeep` 占位**
5. registry `handoff`/`evidence` 请写完整相对路径，例如  
   `agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-KG-SERVICE-ALIGN-L01.md`  
   （旧简写 `agent-handoffs/<file>.md` 在 P3 后失效，需 MCP 批量改指针）
