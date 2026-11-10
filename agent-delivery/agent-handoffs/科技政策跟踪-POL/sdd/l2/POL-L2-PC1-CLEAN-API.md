# POL-L2-PC1-CLEAN-API · 政策数据治理 · 系统引用政策源数据清洗 · 后台接口设计

- 任务：`POL-L2-PC1-CLEAN-API`
- 日期：2026-11-08
- 重写：2026-11-10
- 状态：已按当日裁定重写。本稿不写会签结论，不把本单标 done
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-07`
- 上游：`sdd/l2/POL-L2-PC1-CLEAN-ARCH.md`（本分册以它为准）；说明书「#### 602」
- SRS 序号：**602**

本分册只定 602 的后台接口。候选、执行是两条新的公开读口，都在 `/display/v1/policy/` 下，同步。路径由本稿定名，本波不改名。不复用 `GET /display/v1/policy/governance/results`。内部不复用 `GET /internal/policy/search`，也不复用 `RemotePolicySyncClient`。`governance/results` 继续给 603 和页眉，本稿不改它的 603 区块。

不写 OpenAPI 字段表，不写实现代码。参数和响应只写到能区分第 5 节的空态。准确性由 element 只读 ADS 演示表 `policy_accuracy_demo`。

Java 不写贴源 SQL。浏览器只打这两条公开读口。`gkxlumen-display` 只调 element，不直连 Python，不直连库。

## 1. 公开资源

前缀 `/display/v1/policy/`。浏览器经网关打 `gkxlumen-display`。不另开页。两条都与 `governance/results` 并列，都是同步读：一次请求里算完再返回。不进 `gkxlumen-topic-async-service`，不新建清洗 Job，不返回 501。这次不写 `{ods}`、DWD、ADS、供应方库 `gkx`、`script_state`。

| 动作 | 公开资源 | 何时发 |
|---|---|---|
| 候选 | `GET /display/v1/policy/governance/clean-candidates` | 智能搜索，或按政策 ID。可以发生在点「执行」之前。候选不是清洗，响应里没有批次明细 |
| 执行 | `POST /display/v1/policy/governance/clean-execute` | 只在点「执行」时发一次。没点不发。用 POST 是因为请求体要带多值勾选和当时启用的规则；这次仍然只读 |

602 不用单值 `policyId` 做过滤，也不用 `script_state.status` 六值（`done` / `empty` / `no_match` / `degraded` / `failed` / `llm_unavailable`）做过滤。

`GET /display/v1/policy/governance/results` 继续给 603 和页眉。602 不使用它，也不把候选或本批写进去。本稿不改这条资源的 603 区块。

## 2. 候选

`GET /display/v1/policy/governance/clean-candidates`。同步。display 只调 element。element Feign 只读内部路由 `GET /internal/policy/clean-candidates`，只读演示贴源的当前行。国内、海外分块，不合成一把。只出现贴源里的政策。不直连 Python，不复用 `RemotePolicySyncClient`。

查询只带到能分清空态：

| 参数语义 | 必选 | 作用 |
|---|---|---|
| 入口 | 是 | 智能搜索，或按政策 ID 精确查。两条入口进同一个多选集合 |
| 来源 | 否 | 国内，或海外。不传则两源都查，仍分块返回 |
| 搜索词 | 智能搜索时必选 | 国内对 `title`、`publish_code`、`ministry`。海外只对 `title`。没有的列不参与搜索，也不说成该 ID 不存在。海外发布机构只出现在列表上，不参与搜索 |
| 贴源 id | 按政策 ID 时必选 | 该源的政策 ID。不是旧的单值 `policyId` 过滤 |

当前行过滤写进这次候选。`is_deleted` 与 `is_history` 都在时，当前行是 `is_deleted = 0` 且 `IFNULL(is_history, 0) = 0`。`is_history` 不在时只滤 `is_deleted = 0`。

每一源只落下面一种：

| 该源情况 | 该块 |
|---|---|
| 有可勾的行 | 候选行。国内：标题，辅以文号、发文部门、发布日期。海外：标题，辅以发布机构、发布日期。业务键是贴源 id |
| 表在，且当前行为 0 | 贴源无数。文案「这一源还没有贴源数据」。不把刚输入的 ID 说成不存在 |
| 表在，有当前行，精确查对不上 | ID 不在贴源。文案「该 ID 不在贴源」。不改去政策主表找。没参与搜索的列不对成这一句 |
| 表在，有当前行，智能搜索没有可勾的行 | ID 未命中。文案「这次没搜到」。已经勾上的政策不由本响应改掉。海外没按文号、发文部门搜，也不写成该 ID 不存在 |
| 表不存在，或这一块读不出来 | 读取失败。文案「读取失败」。已经显示出来的区块保持原样 |

候选响应不带规则命中，不带批次明细，不写成功，不造 0。

## 3. 执行

`POST /display/v1/policy/governance/clean-execute`。同步。没点「执行」不发本批。请求体只带点下去那一刻的勾选和当时启用的规则。启停不落库。本稿不设启停保存口。启停不进这次请求体以外的保存。重新打开时六条都启用，由页面初值完成，不读库。

| 参数语义 | 必选 | 作用 |
|---|---|---|
| 勾选 | 是，可多值 | 每一项是来源（国内或海外）+ 贴源 id。用点下去那一刻的集合 |
| 当时启用的规则 | 是 | 六条里当时启用的那些：去重合并、格式标准化、噪声过滤、完整性校验、一致性校验、准确性校验。没带上的是停用 |

一条都没选时不发。已经勾上、还没点时也不发。请求若没有勾选，不返回批次明细，也不造 0。同一选择在这次响应回来之前不再发第二次。当时一条都没启用：勾选仍进批次头，六条都标明停用，不读准确性，不造 0。

响应是这一次的批次明细，不落成六条正式事实表。display 只调 element，把 element 返回的五条判定和准确性放进同一次响应。五条由 element Feign 只读路由得到。准确性由 element 只读 `policy_accuracy_demo`。

| 块 | 谁读 | 该块怎么区分 |
|---|---|---|
| 批次头 | 随这次勾选 | 有批次名。条数等于这次勾选的条数。没点之前不出现。本批状态写在这次响应里，三句见本节末，不写成算法公式 |
| 五条里当时启用、且可判定 | element Feign `POST /internal/policy/clean-judge`，下游只 SELECT 演示贴源两表，结果留在这次响应 | 命中条数。每条规则有「脱敏失败样例」：作用范围有列且判定出失败时，从该列脱敏后放进这次响应。更新时间是这一次响应的时刻，标明是这次请求，不是贴源行的 `updated_time`。去重合并写「应合并」，格式标准化写「待标准化」。不改贴源原文 |
| 五条里当时启用、但没有可判定结果 | 同上，请求已经完成 | 无加工事实。命中 null。脱敏失败样例为 null，不造示例句。缺列、噪声过滤、一致性校验没有可判定列时，样例同样为 null。不写成功、部分、失败。不造 0。更新时间留空。缺列走这一句，不走读取失败 |
| 请求体没带的规则 | 不计入 | 规则停用。行仍在，标明停用，本批不计入它的命中。脱敏失败样例留空，不造示例句 |
| 准确性，当时启用 | element 只读 `policy_accuracy_demo`，按来源 + 贴源 id。display 不直连库 | 对上的行才返回演示条数，并标明演示。不得写成已经按原文核过。没点之前不出现命中。当时停用则不读、不出现命中。表不存在或查询失败是读取失败。表在但这一条没有行：不返回数，不返回 0，不写成无加工事实，不写成已经核过。界面用「这一条还没有演示数」 |
| 转发失败或超时，或准确性这张表不存在、或查询失败 | 该块读不出来 | 读取失败。不用命中 null 代替。不返回 0。不改写成无加工事实。不写成「这一条还没有演示数」。不写入 `governance/results` |

本批状态写在执行响应里，不写成算法公式。能判定的都过了、没有失败样例 = 成功。既有过的也有失败样例，或者有的能判定、有的仍无加工事实 = 部分。能判定的都带失败样例 = 失败。读取失败和无加工事实不占用这三句。

读取失败和命中 null 是两种响应。已经显示出来的区块保持原样，不改写成成功，也不改写成无加工事实。

执行中不是一种落库状态，也不是本响应里的一种命中。它只指这条同步请求还没返回：界面锁住勾选、清空和规则开关，「执行」不能再点出第二遍。先不写成成功，不造 0。刷新之后，执行中只在这次请求还没结束时成立。五条结果不在库里，刷新后不能从库里把这一批再读出来。

跑完之后再改勾选或开关：不自动再发。旧结果留在页面上，标明还不是最新一次。再点「执行」才按新的那一刻重发。清空选择后回到未选，不发本条。

## 4. 内部委托

浏览器不直连 Python，不直连贴源。display 只调 element，不直连 Python，不直连库。Java 不写贴源 SQL，不读供应方库 `gkx`。不复用 `RemotePolicySyncClient`。`GET /internal/policy/clean-candidates` 与 `POST /internal/policy/clean-judge` 本波不改名。

| 公开资源 | 内部 |
|---|---|
| `GET …/governance/clean-candidates` | display 只调 element。element Feign 新建只读路由 `GET /internal/policy/clean-candidates`。下游只读 `{ods}.dwd_policy_base`、`{ods}.dwd_global_policy_base` 的当前行。不走 `GET /internal/policy/search`，不读政策主表，不复用 `RemotePolicySyncClient` |
| `POST …/governance/clean-execute` 的五条 | display 只调 element。element Feign 新建只读路由 `POST /internal/policy/clean-judge`。与候选分成两条只读入口。只 SELECT 上面两表。禁止对 `{ods}`、DWD、ADS、供应方库、`script_state` 写入。结果留在这次响应。不复用 `RemotePolicySyncClient` |
| 同一次执行里的准确性 | 当时启用才读。element 只读 `policy_accuracy_demo`，按来源 + 贴源 id。Python 写入演示行发生在点击之外，这次不现造。表不存在或查询失败则这一块是读取失败，不用写死的数顶上。表在但这一条没有行，不返回数，界面用「这一条还没有演示数」 |

trace 沿既有展示链走。display 往下游带 traceId。本稿不新设计观测点。

## 5. 空态

分开写。无加工事实只在点过「执行」之后。读取失败不返回 0，也不改写成无加工事实。表不存在是读取失败，不是贴源无数。

| 状态 | 请求 | 响应上怎么分 |
|---|---|---|
| 未选 | 不发执行 | 规则区和批次明细都空。不出现 0，不出现「成功」 |
| 未执行 | 不发执行 | 批次明细空。不写成功，不写成已经清洗过，也不写成无加工事实 |
| 执行中 | 执行已发，响应未回 | 不把未返回写成成功，不造 0。同一选择不再发第二次 |
| 贴源无数 | 候选 | 表在且当前行为 0。该源「这一源还没有贴源数据」。表不存在不走这一句 |
| ID 不在贴源 | 候选 | 该源表在且有当前行，精确查对不上，「该 ID 不在贴源」。没参与搜索的列不对成这一句 |
| ID 未命中 | 候选 | 该源表在且有当前行，搜索没有可勾的行，「这次没搜到」。海外只搜了 `title`，不把没搜的列说成该 ID 不存在 |
| 规则停用 | 执行请求体没带这条 | 标明停用，本批不计入 |
| 无加工事实 | 执行已完成 | 命中 null。脱敏失败样例 null。不写成功、部分、失败。不造 0。更新时间留空。只在点过之后 |
| 这一条还没有演示数 | 执行已完成，准确性当时启用 | 表 `policy_accuracy_demo` 在，但这一条来源 + 贴源 id 没有行。不返回数，不返回 0，不写成无加工事实，不写成已经核过 |
| 读取失败 | 候选或执行的那一块 | 「读取失败」。表不存在或查询失败走这一句。不是命中 null，不是 0，不改写成无加工事实，也不写成「这一条还没有演示数」 |

## 6. 页眉与相邻资源

页眉库级计数不走候选读口，也不随这一选改口径。它继续由 `GET /display/v1/policy/governance/results` 返回。这个数的 `metric_id` 仍是 `M_POLICY_TOTAL_COUNT`，D4=mock。`results` 里的计数不得写成已经接入，也不得替代本批条数。本稿不重写它的读法。

清洗页从 `results` 只取页眉这个数。`qualityAgg` 不进 602 的批次明细，不挂有效率指标 `M_POLICY_VALIDITY_RATE`。本批命中条数只来自 `clean-execute`，不注册成指标。

| 资源 | 本分册 |
|---|---|
| `governance/results` 的 603 区块 | 归 `POL-L2-PC1-STRUCT-API`。本稿不改 |
| `governance/lineage-index` | 604，本分册不实现 |
| `governance/indicator-library` | 605，本分册不实现 |

## 7. 明确不做

- 不写 OpenAPI 字段表，不写实现代码。准确性表名用已定的 `policy_accuracy_demo`，不另起名。
- 不把单值 `policyId`、`script_state.status` 六值留成 602 的过滤条件。
- 不复用 `governance/results`，不复用 `/internal/policy/search`，不复用 `RemotePolicySyncClient`。公开路径和这两条内部路径本波不改名。
- 不让浏览器直连 Python。不让 display 直连 Python 或库。不让 Java 写贴源 SQL。
- 不建六条正式事实表。不把准确性演示数和五条现算写进同一张表。
- 不允许接口直接返回写死的质量分数。
- 不把 `qualityAgg` 写进 602 批次，不挂有效率指标。
- 不把本单标 done。

## 8. 可实现

| 需规要点 | 可实现的做法 |
|---|---|
| 多源候选 | `GET …/governance/clean-candidates`。display 只调 element，element Feign 只读路由。国内搜 `title`、`publish_code`、`ministry`，海外只搜 `title`。当前行过滤后，表在且为 0 才是空源文案 |
| 点执行才有本批 | `POST …/governance/clean-execute`。没点不发。五条经 element Feign 只 SELECT，结果在这次响应。成功、部分、失败按第 3 节三句写入执行响应 |
| 准确性 | 当时启用才由 element 按来源 + 贴源 id 只读 `policy_accuracy_demo`。对上的行返回演示条数并标明演示。没有行时返回「这一条还没有演示数」 |
| 空态 | 第 5 节分开。读取失败、无加工事实、没有演示行是三种响应 |
| 页眉 | `M_POLICY_TOTAL_COUNT`，D4=mock。`qualityAgg` 不进本批，不挂有效率指标 |

接口直接返回写死的质量分数，或把 602 仍滤在 `governance/results` 上，本单不可签收。

## 变更记录

2026-11-10：按当天裁定重写。602 改为两条新的公开读口：`GET /display/v1/policy/governance/clean-candidates`、`POST /display/v1/policy/governance/clean-execute`。602 不再使用 `governance/results`。内部改为 `GET /internal/policy/clean-candidates` 与 `POST /internal/policy/clean-judge`，不复用 `/internal/policy/search`。去掉单值 `policyId` 和 `script_state.status` 六值过滤。空态按说明书分开。准确性表名见 DATA 稿，本稿不取名。

2026-11-10：波次 C 回应。display 改为只调 element。候选与五条仍由 element Feign 上述两条只读路径，路径不改名，不复用 `RemotePolicySyncClient`。准确性表名写 `policy_accuracy_demo`。国内搜索三列，海外只搜 `title`。候选写入当前行过滤；表在且当前行为 0 才是空源文案，表不存在是读取失败。执行响应补脱敏失败样例、本次响应时刻，以及成功、部分、失败三句。没有演示行时返回「这一条还没有演示数」。页眉保持 `M_POLICY_TOTAL_COUNT`，D4=mock。`qualityAgg` 不进 602 批次。
