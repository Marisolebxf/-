# POL-L2-PC1-CLEAN-FDE-B2 · api-agent 审稿

- 身份：`agent:api-agent`（独立审稿，非起草）
- 日期：2026-11-10
- 被审：`sdd/l2/会签/POL-L2-PC1-CLEAN-FDE-B2-读法方案.md`
- 口径：说明书「#### 602」、`sdd/602-选择政策-线框.md`、审稿硬清单 api-agent 4 条
- 只读方案、说明书和现有读口。不改方案、说明书、代码。

结论：有条件支持方案第 4.1 款（贴源候选由 Python 同步只读，六条规则按无加工事实返回空）。下面四条不闭合，波次 C 不能按这版写 API 稿。

## 异议

[api-agent] API-1 · 问题：第 4 节三款都没有把界面条件写成请求参数。智能搜索词、政策 ID、国内已选、海外已选是四类条件，两表 `id` 各自主键，已选必须是「来源 + id」多值，只传 id 会串源。海外表没有 `publish_code`、`ministry`，智能搜索的「文号 / 发文部门」在海外没有列；4.1 把这件事推给数据稿，请求侧没有对应参数。六条启停也没钉死：4.1 写「启用的规则行仍返回」，第 6 节又要求查询参数带六条启停。现口只有单值 `policyId` 和 `script_state.status`，对不上这批条件。 · 依据：线框条件栏（智能搜索、按政策 ID、国内多选、海外多选、六条开关）；说明书 276–279、259 行；方案 3.1（约 64 行）、4.1（约 105–106 行）、第 6 节 API 行；`storage/POLICY/sources/ods-ddl.md` 国内 `publish_code`/`ministry`、海外 `organ`/`report_number`（无文号、无发文部门）；display `PolicyGovernanceController` 第 29–30 行；`POL-L2-PC1-CLEAN-API.md` 查询参数表。 · 建议：4.1 的候选按源请求，参数为 `source`、可选 `q`、可选精确 `id`。海外 `q` 匹配 `title` 与 `organ`。本批请求用来源与 id 的多值，有值才表示已选。4.1 不把六条启停放进请求，启停留在页面；第 6 节改成这一句。若以后改走 4.2，本批 GET 再加六条启停，停用的不进汇总。

[api-agent] API-2 · 问题：第 4 节没有响应字段，功能点要看见的值对不上号。候选行缺来源、id、标题和辅列，也缺分源原因（这一源还没有贴源数据 / 该 ID 不在贴源 / 这次没搜到 / 读取失败）。本批缺命中、脱敏样例、更新时间、状态。3.2 把规则名、作用范围、开关放在页上，4.1 又说接口返回规则行，规则文案会有两份。批次名没有来源。 · 依据：说明书功能点 602-1 至 602-8（约 240–249 行）、状态清单（约 253–261 行）；线框批次明细；方案 3.1 列表列、3.2 表（约 84–89 行）、4.1（约 105 行）。 · 建议：候选响应分国内、海外两块，每块带原因码；行内带来源、id、标题和该表辅列（国内文号、发文部门、发布日期；海外发布机构、发布日期）。规则名、作用范围、「应合并」「待标准化」只留在页面。本批只回命中、脱敏样例、更新时间、状态；无加工事实时这四项为 null，状态不写「成功」。批次名由页面按当前勾选生成，接口不另造批次号。

[api-agent] API-3 · 问题：4.1 是同步读，和「不建清洗 Job」一致，但空态没有写成空数组或 null。现有失败路径会造 0：element 的 `countOrZero`，display 在 Feign 失败时 `emptyResults` 写入 `totalPolicyCount=0`；`/internal/policy/search` 失败时 `items` 为空且 `total` 为 0。未选、无加工事实、读取失败会收成同一种 0。4.3 在同一次请求里现算，响应里会出现判定条数，说明书要求这时命中空白，也没有可复查的更新时间。 · 依据：方案 4.1（约 101–107 行）、4.3（约 125–128 行）、时序图（约 43–48 行）；说明书约 234、256、261 行；element `PolicyGovernanceController` 第 59、177–181 行；display `PolicyGovernanceService` 第 41–48、72–78 行；`policy_routes.py` 约 1216–1224 行。清单第 3 条：空数组，不造 0。 · 建议：候选和本批都是同步 GET，这次请求不触发作业。未选不发本批请求。无行用空数组，条数和命中用 null。读取失败用单独原因码，已经返回的另一块保持原样。本批响应按 4.1 的空事实返回，不采用 4.3 的当次现算。

[api-agent] API-4 · 问题：第 4 节只写「经现有 entan-py Feign 增加一条候选检索，Python 新开只读路由」，公开路径没有名字。治理读面现在不调 Python。`RemotePolicySyncClient` 只打同步历史、仿真兜底和条款拆解，其中有写操作，候选检索不能挂在这只客户端上。`/internal/policy/search` 读 DWD `policy_base_info` 或缺项目录，复用会把政策主表行带进候选。第 6 节又说 602 与 603 仍在同一条 `results` 上拆区块；贴源候选若塞进 `results`，会带上 603 的 `structure` 和页眉 `totalPolicyCount`。 · 依据：方案第 2 节、4.1（约 105–106 行）、3.1（约 70–72 行）、第 6 节 API 行；display `PolicyGovernanceService` 第 16–27 行；`RemotePolicySyncClient` 第 14–22、32–55 行；`policy_routes.py` 文件头与 `policy_search`（约 1149–1173 行）；display `PolicyGovernanceController` 第 21–31 行。清单第 4 条。 · 建议：Python 为 602 候选单独增加只读路由，查询仍读 `{ods}` 两表的当前行。display 另建一只只读 Feign，服务仍是挂有 `/internal/policy/**` 的 entan-py。公开路径放在 `/display/v1/policy/governance/` 下，与 `results` 并列。`results` 继续给 603 和页眉，保留现有单值 `policyId`。602 的候选和本批不改这条响应。
