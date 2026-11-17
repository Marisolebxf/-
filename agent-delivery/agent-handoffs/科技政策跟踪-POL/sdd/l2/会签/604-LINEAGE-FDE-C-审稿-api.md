# 604-LINEAGE-FDE · 波次 C · 审稿 · api-agent

- 日期：2026-11-16
- 身份：api-agent
- 总单：`POL-L2-PC1-LINEAGE-FDE-L01`
- 被审：说明书「#### 604」（`sdd/科技政策跟踪-系统详细设计说明书.md`）+ `POL-L2-PC1-LINEAGE-ARCH.md` 2026-11-16 补段 + `会签/604-LINEAGE-FDE-B-读法方案.md`
- 对照（只读，本轮不改）：`sdd/l2/POL-L2-PC1-LINEAGE-API.md` 的 `lineage-index`；现网 `GET /display/v1/policy/governance/lineage-index`（display 委托 element，SQL 列即响应行）
- 口径：`.cursor/skills/gkx-fde-design-change/审稿硬清单.md` api-agent 四问
- 本稿只记异议。不改说明书、ARCH、API、代码、用例、task-registry，不 commit

已知且本波已写明、不另开缺陷：三个动作不新接口；不打开 617；复核不落库、不新建表；605 / 602 本波不改口径。

## 硬清单（四问）

1. **界面条件 → 请求参数**  
   说明书「#### 604」界面上的拣行条件只有一条：先选一条政策。它对应已有查询参数 `policyId`。条款号、结论键不是本叶界面条件，留在同一条 GET 上，不另开资源。  
   **对不上的是必选性**：API 稿仍写 `policyId`「否；核增演示默认一条可演」。ARCH §5.1 旧句「不选则读全部」已标被说明书取代，API 稿没有跟着改。现网 `policyId` 可空，空则不加 `policy_id` 条件，`records` 是全表。见异议 API-2。

2. **响应能否给出每个功能点要看见的字段**  
   API 稿 §3 写「不写字段表」。现网这一条 GET 的行只有：`id`、`link_kind`、`policy_id`、`policy_title`、`clause_no`、`clause_excerpt`、`conclusion_key`、`conclusion_title`、`conclusion_text`、`is_mock`、`metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。没有政策原文字段，没有洞察标识列。`link_kind=原文条款` 的行 `conclusion_key` / `conclusion_title` / `conclusion_text` 为 null。

   | 功能点要看见的 | 从哪来 | 缺不缺 |
   |---|---|---|
   | 604-1 表列「条款内容」 | 同一行 `clause_no` + `clause_excerpt` | 有 |
   | 604-1 / 604-2「政策原文」 | 行里没有。`policy_title` 是标题，`clause_excerpt` 是条款摘录 | **缺独立原文**，见 API-1 |
   | 604-1 / 604-2「分析结论」 | 同一行 `conclusion_title`、`conclusion_text` | 条款结论行有；原文条款行是 null，该格空，不造句 |
   | 604-2 路径「原文 → 条款 → 结论」 | 浏览器用上面三格拼出来，响应里没有路径字段 | 原文格没有独立字段时，路径两端会变成同一段摘录 |
   | 604-3 查证 · 分析结论 | 被点那一行已返回的 `conclusion_title` / `conclusion_text`，不另请求 | 原文条款行为空 |
   | 604-3 查证 · 洞察标识 | 响应没有洞察列。现网前端把 `conclusion_key` 当成标识 | **合同未钉死**，见 API-3。空则按线框写「这条还没有洞察标识」，不写 0，不去读 617 / `gapfill_policy_report_insight` |
   | 604-4 复核说明、「已复核」 | **不来自响应**。当次页面内存：提交前为空、看不出已复核；提交后只标在被点的那一行。不发写请求，不落 `gapfill_policy_lineage_index`。重开页面后这两项都没有，索引仍只按 `policyId` 再读 | 不缺接口字段；禁止为复核加 POST |

3. **同步还是 Job？空态返回什么**  
   同步。`POL-L2-PC1-LINEAGE-API.md` §1：不进异步，不返回 501。无行时 body 是 `records: []`，不造数字 0。文案「这条政策还没有关联索引」由页面写，不由接口返回。  
   **失败和未选跟「无行」撞形**：element 失败时 display 把缺 `records` 的体收成 `records: []`；未选且不带 `policyId` 时现网返回全表而不是空数组。见 API-2、API-4。不改成 Job。

4. **是否复用已有路径**  
   复用已有 `GET /display/v1/policy/governance/lineage-index`。display → element 只读 `gkxlumenx_gapfill.gapfill_policy_lineage_index`。浏览器不打第二条读口，复核不写回。本叶不要新开平行资源。查证若因没有洞察列改去读 617，就破了这一条，见 API-3。

## 异议

[api] API-1 · 问题：选中政策之后，同一次 `lineage-index` 仍给不出说明书要的「政策原文」。API 稿不写响应字段。现网行只有标题 `policy_title` 和条款摘录 `clause_excerpt`，没有与条款分开的原文字段。604-1 要求表上同时看见原文、条款、结论；604-2 弹层还要列出这三块并写出「原文 → 条款 → 结论」。把 `clause_excerpt` 同时填进原文格和条款格，路径前两段是同一段。`原文条款` 行的结论三列又是 null，该行结论格也是空的。读法方案写「用已返回的原文、条款、结论」，返回行里没有单独的原文。 · 依据：说明书「#### 604」604-1、604-2（功能点表）；线框弹层三块与路径；`POL-L2-PC1-LINEAGE-API.md` §1 只有三个请求参数、§3「不写字段表」；`gkxlumen-element` `PolicyGovernanceController` 的 `LINEAGE_SQL`；`lumen-algo-py/scripts/mysql/gapfill_policy_lineage_index.sql` 列清单（无原文字段；原文条款行结论列为 NULL）；读法方案 §2。 · 建议：仍只复用这一条 GET，不新接口，不读 617 的 `source_excerpt`。会签钉死对照：条款内容 = `clause_no` + `clause_excerpt`；分析结论 = `conclusion_title` / `conclusion_text`（null 则该格空，不造句）。政策原文若接受「摘录即原文」，弹层原文格只用 `clause_excerpt`、条款格只用 `clause_no`，两格不得贴同一段。若原文必须是另一段正文，点名为缺字段，后波补列再由同一读口带出，本波不新资源。这段对照要写进 API 稿，否则「本波不改 API」等于三个动作没有字段合同。

[api] API-2 · 问题：界面「先选一条政策」虽有参数 `policyId`，API 稿仍把它写成可选，并写「核增演示默认一条可演」。这与说明书「未选不列出某一政策的行」和 ARCH 2026-11-16 已取代的「不选则读全部」相反。现网没有服务端默认政策：`policyId` 为空就不加条件，`records` 返回全表，三个按钮会落在未选时不该出现的行上。 · 依据：说明书状态「未选政策」、已定 5；ARCH §5.1「按政策查索引」已被取代句、FDE 补段；`POL-L2-PC1-LINEAGE-API.md` §1 政策 id 行；element `lineageIndex` + `appendEq`（空值不加 WHERE）。 · 建议：未选不发 `lineage-index`。删掉「默认一条可演」。省略 `policyId` 时返回 `records: []`，不要全表。不新增参数，不改成 Job。

[api] API-3 · 问题：查证要看见的「洞察标识」在 API 合同里没有列。现网只有 `conclusion_key`，前端已把它映成 insightId；`原文条款` 行该键为 null。说明书写「分析结论或洞察标识」，线框在没有标识时要写「这条还没有洞察标识」，两处没有钉死用哪一列。实现若改去读 `gapfill_policy_report_insight` 或 617 的 `gapfill_policy_report_trace`，就是新开平行读口。 · 依据：说明书 604-3；线框「查证结果」；API 稿无响应字段；`LINEAGE_SQL` 的 `conclusion_key`；读法方案 §2「不打开 617」、§4 API 不改。 · 建议：查证标识只认本行已返回的 `conclusion_key`（空则按线框那句，不写 0）。分析结论只认本行 `conclusion_title` / `conclusion_text`。禁止为查证再打一条资源。

[api] API-4 · 问题：无行、失败、未选（若按 API-2 收成空列表）三种情况现网都是 `records: []`。无行时页面应写「这条政策还没有关联索引」。失败若画成同一句，就把读失败说成这条政策没有索引。ARCH 只要求失败不清空治理页其他区块，没有把失败和「对不上」分成两种返回。 · 依据：说明书状态「该政策无行」；ARCH §3 失败语义、FDE 补段；读法方案 §3「请求失败」；display `PolicyGovernanceService.lineageIndex` → `recordsBody`（无 `records` 时补空列表）；API 稿 §1「无行则空列表」。 · 建议：保持同步。对不上才是 `records: []`，页面用那句空文案，不造 0。失败不要改成这句：本区块留上次成功行，或只标读取失败，其他区块不动。不为此新开资源，不进 Job。
