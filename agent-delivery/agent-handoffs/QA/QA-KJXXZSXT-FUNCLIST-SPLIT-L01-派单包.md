# 派单包：QA-KJXXZSXT-FUNCLIST-SPLIT-L01

- **派单方**：coordinator（本会话 · 2026-08-18）
- **执行 / 监管**：`human:黄敬洲`（可带 `qa-agent`；claimed_by 写真人）
- **Agent 角色**：`qa-agent`
- **状态**：`claimed` · `claim_type` 语义 = coordinator_dispatch
- **仓 / 产物落点**：`agent-delivery/qa/total-set/KJXXZSXT/`
- **Sprint**：未挂（勿 silent 加活；需进 Sprint 请 PM 写入）
- **强度**：ponytail full（写测 / 生成脚本）
- **对标**：`QA-KJZTFWXT-FUNCLIST-SPLIT-L01` as-built（需规唯一源、不写步骤、不裁条数）

---

## 1. 目标

按 **需求规格说明书功能清单** 对 **科技信息展示系统（KJXXZSXT）** 做最细颗粒度功能点拆分，产出符合总集模板的 FUNC Excel。

输入真源：

`原始文档/国际科技信息中心项目_需求规格说明书功能清单-v1.2(1).xlsx`  
sheet：**科技信息展示系统**

方法真源：

- 门户《最细颗粒度功能点拆分原则》
- 专题已落地方法：`qa/total-set/KJZTFWXT/科技专题战略分析-最细颗粒度功能点拆分原则-v1.md`（只换系统/模块，不换拆法）

## 2. 范围（功能清单 L3，catalog 七模块作对照）

| 对照模块（catalog / bid） | 本单处理 |
|---|---|
| 科技发展态势 | 新拆 |
| 科技政策跟踪 | 新拆（含政策对比核增时以功能清单该 sheet 是否收录为准） |
| 科技人才态势 | 新拆 |
| 科技数据资源 | 新拆 |
| 科技知识图谱 | 新拆 |
| 科技成果展示 | 新拆 |
| 科技服务全景 | 新拆 |

以 **功能清单该 sheet 的 L3/L4/L5/L6 名 + 需规全文** 为准。catalog / bid 只作对照，不得用来增减功能点。

监管人可在开工后收窄到指定 L3/L4；收窄须写 handoff 偏离，不得把部分合表标成全系统总集。

## 3. 产物

| 产物 | 建议路径 |
|------|----------|
| 合表 Excel | `qa/total-set/KJXXZSXT/6.国际科技信息中心项目_科技信息展示系统_功能点拆分_v1.xlsx`（版本随迭代） |
| 编号 | `ZNFWJQ-KJXXZSXT-v1.0-FUNC-#####` |
| 列 | 对齐专题 v8：用例编号 / 功能模块 / 子功能模块 / 功能项 / 子功能项 / 页面 / 功能点 / 拆分维度 / 规则来源 / 需规描述；测试内容、前置条件、测试步骤、预期结果留空 |
| 五级工作稿 | `qa/total-set/KJXXZSXT/fp-split-run/`（`work/` `review/` `prompts/`） |
| 本系统原则 | `qa/total-set/KJXXZSXT/` 下另写一份（从专题原则改系统/模块，不另起拆法） |
| handoff | `agent-handoffs/QA/QA-KJXXZSXT-FUNCLIST-SPLIT-L01.md` |

本单约定：**Excel-only 合表**；测试步骤不写。

## 4. 编写原则（与专题 as-built 一致）

1. 拆点唯一需求源 = 五级/六级名称 + 需规全文。需规怎么写就怎么拆。
2. **禁止**读 `demo-ui-science`、产品五件套、旧用例来增减功能点。五件套加严留给以后写测试步骤。
3. 不写测试内容 / 前置 / 步骤 / 预期。
4. 数量超出不裁。
5. 建议按五级拆工作单元；先锁金样再全量并行。
6. 一条功能点 = 一个动作 + 一个对象 + 一条可验收规则或结果。禁止笛卡尔积、套话、未点名指标。

## 5. DoD（与 registry 一致）

1. 功能清单该 sheet 范围内有总集 FUNC 合表，列与编号合规  
2. 未收窄则覆盖全部 L3；若收窄则 handoff 写偏离  
3. 不写测试步骤；超条数不裁  
4. handoff 含范围 / 偏离 / 产物 / 架构合规 / cost 四字段 / `ponytail:` 行  
5. 经 MCP 推进；**勿自行 `done`**；勿 silent 加 Sprint  

## 6. 必读

- `agent-delivery/qa-test-case-spec.md`
- `agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md`（范围对照，不当地图发明点）
- `原始文档/最细颗粒度功能点拆分原则(1).md`
- 专题原则 v1 + 专题 `fp-split-run/prompts/_template.md`（改系统路径后复用）
- 专题合表：`qa/total-set/KJZTFWXT/6.国际科技信息中心项目_科技专题服务系统_功能点拆分_v8.xlsx`

不要把 `repos/demo-ui-science` 当拆点源。

## 7. 进度

| 日期 | 状态 |
|------|------|
| 2026-08-18 | 建单 ready → claimed（黄敬洲）；派单包落盘 |
