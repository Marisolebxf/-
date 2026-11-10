# 603-STRUCT-FDE · 波次 A · product-agent 任务单

总单：`POL-L2-PC1-STRUCT-FDE-L01`。监管人 `human:淮政玮` 于 2026-11-10 确认执行计划后开工。  
本单只做波次 A 的产品设计。你是 product-agent，独立会话。不定档、不选读法、不改业务仓代码、不改 Storage、不改注册表、不 commit。

## 先读

- `agent-delivery/产品实现规程.md` §4.2（含 §4.2.0 / §4.2.3）
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` 中 **603 政策库结构化**（总表行 + 正文能挂上的节）
- 架构现状（只读，本波次不改定稿）：`sdd/l2/POL-L2-PC1-STRUCT-ARCH.md`
- 展示现状（只读）：
  - `repos/lumen-ui-science-pc/src/views/policy/governance/index.vue`（政策选择器、「演示政策」、结构化摘要、分类标签表、字段映射表）
  - `repos/lumen-ui-science-pc/src/api/policy.ts`（`fetchGovernanceLive`：live 下 `fieldMappings=[]`、缺 `structureTaxonomy`）
  - `repos/lumen-ui-science-pc/src/mock/modules/policyPcSeed.ts`（`structureTaxonomy` / `fieldMappings` 种子）
- 中台对照（只读，不改中台仓）：`repos/demo-ui-system-test/src/views/policy/pages/ClausePage.vue` 按钮「抽取条款」→ `structurePolicyClauses` → `POST …/clauses/enrich`

路径相对 `gkx-orchestration/`；业务仓在 `${GKX_ROOT}/repos/`。

## 监管人已锁定的意图（不要改、不要扩）

- 改哪一叶：展示系统 · 智能政策库构建 · **603 政策库结构化**页签
- 改成什么样：
  1. 条件栏文案「演示政策」→ **「政策选择」**；下拉 **可按关键字检索**
  2. **同一行**增加按钮 **「结构化抽取」**
  3. 选定政策后：**已结构化** → 下方加载该政策结构化摘要（及页签约定的下方区块）；**未结构化过** → 下方不加载业务摘要，**只能先点「结构化抽取」**
  4. 按钮执行逻辑 **同中台「抽取条款」**（展示侧经 Java `POST /display/v1/policy/parse/clauses` 转发算法 enrich；不直连 Python、不打开中台页）
  5. **「政策分类标签体系」表**与 **「元数据规范 · 字段映射规则」表不得为空**（Wave0：页面常驻有数；根因是 live 适配器漏灌种子）
- 为什么：治理页可演示「选 → 抽 → 看」闭环；标签/映射体现需规统一管理与字段规范，不能空表演示

## 要改的范围

改说明书 603 相关节，满足规程 §4.2.3：

- 功能点编号建议挂在 603 下拆分（如 `603-sel-1` / `603-ext-1` / `603-tax-1`…）；每点写「界面上必须看见什么」，能被截图验证
- 状态清单至少覆盖：未选政策、已选且已结构化、已选且未结构化（摘要未加载 + 按钮可点）、抽取进行中、抽取失败、抽取成功后摘要出现、两表有数据（与是否选政策无关的常驻态）
- 影响清单：至少 `POL-L2-PC1-STRUCT-ARCH`（现行「只读呈现、不重跑」将被本 FDE 扩展为可触发单条抽取）、`POL-L2-PC1-STRUCT-API`（若需声明 parse/clauses 复用）、合规演示用例、前端治理页；旧处标「已被说明书 2026-11-10 取代」
- 文末变更记录追加一行白话
- 另写一页短线框（`sdd/l2/会签/603-STRUCT-FDE-线框.md`）：政策选择行（标签+可搜下拉+结构化抽取按钮）与下方摘要门控、两表常驻；不画架构时序、不写接口字段、不写建表

## 回复（压成 8 行以内）

改了说明书哪一节；功能点几个；选择/抽取门控/两表各怎么写的；影响清单几条；待裁定是否为零。
