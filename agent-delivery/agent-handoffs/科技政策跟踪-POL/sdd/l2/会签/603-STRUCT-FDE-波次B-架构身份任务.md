# 603-STRUCT-FDE · 波次 B · arch-agent 任务单

总单：`POL-L2-PC1-STRUCT-FDE-L01`。波次 A 已收口（说明书「#### 603」+ 线框）。  
你是 arch-agent，独立会话。不定产品功能点、不改业务仓代码、不改 Storage、不改注册表、不 commit。

## 先读

- `agent-delivery/产品实现规程.md` §4.2（轻/中/重分档）
- 说明书「#### 603」整节（含功能点、状态、影响清单）
- `sdd/l2/会签/603-STRUCT-FDE-线框.md`
- `sdd/l2/POL-L2-PC1-STRUCT-ARCH.md`（现行二级 ARCH：只读呈现、不重跑 C2；影响清单点名将被本 FDE 扩展）
- 只读对照：展示 `POST /display/v1/policy/parse/clauses`（`PolicyParseController` / `PolicyParseService` → Feign enrich）；中台「抽取条款」`ClausePage` → `structurePolicyClauses`

## 监管人已锁定（不要改）

政策选择可搜；同行「结构化抽取」；未结构化不加载摘要须先抽；逻辑同中台抽取条款（经 display 转发，不直连 Python、不打开中台）；两表 Wave0 常驻有数。

## 要产出

写 `sdd/l2/会签/603-STRUCT-FDE-B-读法方案.md`，一屏内够用：

1. **定档**：轻 / 中 / 重 + 一句理由（计划建议轻：复用已有 `parse/clauses`；两表前端 seed；不新建 ADS）
2. **动哪些层**：本轮是否 FE 为主；display/API 是否仅确认复用 clauses、是否要改 STRUCT-API 正文；Python enrich 是否不动
3. **「已结构化」判定**：与 `hasClauses` / 条款行是否一致；选政策后读哪条资源（`governance/results` 摘要 vs 另调）
4. **两表非空**：Wave0 前端 seed 灌入 live 适配器是否可接受；是否禁止接口直接返回空数组冒充「无规范」
5. **影响清单回应**：ARCH 本轮要不要改正文（扩展「可触发单条抽取」），还是实现后再 as-built；合规用例 / FE 何时动
6. **未闭合 / 停机项**：没有就写「无」；有则写成决策卡素材一句

不写建表、不写 OpenAPI 字段表、不改说明书正文（产品真源已定）。

## 回复（5 行以内）

定档；动哪几层；ARCH 改不改；未闭合几条。
