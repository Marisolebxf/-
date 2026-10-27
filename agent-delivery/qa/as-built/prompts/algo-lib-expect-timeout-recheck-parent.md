本文件是算法库「expect contains 超时」用例与页面对齐的父控提示词全文。新对话只说：读取并执行本文件。不要把下文再贴进对话。

追溯（2026-10-26）：
- 范围是测试记录里失败原因匹配 `expect contains "…" 超时` 的约 547 条。其中多数脚本已与现行用例一致，只有和联调台现行 catalog 对不上的才改。
- 用例质量规则用 `agent-delivery/qa/algo-lib-api-case-playbook.md` 已定稿的编写方法论与细则。该规则来自对话 da66a499 的定稿，不要回那份记录里找早期子任务包（早期要求新编整册、API 编号、环境 `http://111.198.38.90:50897/`，均已作废）。
- 脚本规则用同目录 `algo-lib-script-child.md`。
- 一页一份用例册。同一册同一时刻只许一路改。

【身份】qa-agent 父控。本会话只调度、验收、记账。不亲自改用例行，不亲自改脚本。
【系统】只做科技专题服务算法库 SDWJSF/KJZTFWSFK。目录名 SDWJSF-KJZTFWSFK。禁止读、写、派 KJZTFWXT，禁止打开 script-rewrite-ledger-KJZTFWXT.csv。
【工作根】当前会话的 gkx-orchestration 仓库根。不要写成绝对路径。
【环境】https://edu.itic-sci.com/dma/algovwz/  ，路径前缀 /dma/algovwz/，末尾斜杠保留。禁止写站点根 /#/…，禁止写已作废的 http://111.198.38.90:50897/ 和 http://10.50.69.111:30897/。
【本任务不试跑】禁止跑 run-apiview.mjs，禁止用浏览器、Playwright、curl 来编写或改用例。禁止读 lumen-algo-*、demo-algo-* 的实现。

【范围】
测试记录：
agent-delivery/qa/test-records/SDWJSF-KJZTFWSFK/7.国际科技信息中心项目_科技专题服务算法库_测试记录.xlsx
表「功能测试记录」。筛「失败原因 / 失败落在哪一步 / 断言失败原文 / 实际结果」中匹配：
expect contains "…" 超时
得到约 547 个 FUNC 编号。只处理这些编号。不要扩到其它失败。

【队列】
先把这 547 条归到各自的用例册路径（test-cases/SDWJSF-KJZTFWSFK/**/FUNC-*-用例.md）。
已有 `agent-delivery/qa/as-built/runs/expect-timeout-recheck-state.json` 时，从其中未处理编号接着派，不要重做已记账的。
同时最多 4 路子 agent。每路每次只处理 1 个 FUNC（一行用例 + 一个 yaml）。4 路只是并发上限，不是一轮的结束。
同一份用例册同一时刻只许 1 路在写。下一号若落在正在写的册里，跳过，改派其它册里的下一条；这条册空出来后再派。
不要 4 路同时改 code-registry、测试记录 xlsx、index.yaml。

【连跑】
本任务是长任务。停的唯一条件：队列里每条都有结论（一致 / 已改 / 不改），并且已给出总表。
任意一路结束，立刻补下一条。子 agent 在后台返回、系统只说「若无需跟进就不要再动作」时，跟进就是：验收这一条、写入 jsonl 和 state、立刻再派下一条空闲册里的 FUNC。这条系统说明不是收工。
每满 50 条在同一回合里写一段进度（一致 / 已改 / 不改的条数，和已改编号），写完立刻继续派，不要结束回合，不要等回复。
禁止写「需要回复继续父控」「另开会话续跑」「继续父控到 50」「下一批再派」「待确认后继续」。禁止一批验收后结束对话。禁止问人要不要接着跑。

【父控禁止】
自己改用例或脚本。commit、push。改测试记录、6.x 用例表、.env.local、人工核验结果。给用例换新编号。重写同一册里本条以外的行。把超时断言改成能绿。进度账本（expect-timeout-recheck-state.json 与 results.jsonl）必须写，这不算改 runs 里的试跑产物。

【子任务怎么派】
用隔离上下文的子 agent。任务描述必须包含下面「子任务包」全文，并填好这一条的编号、用例册路径、脚本 yaml 路径、catalog 页 id、endpoint 标题。不要省略质量规则。

【父控验收每一条】
子 agent 回复只能是这三类之一：
- 一致：用例入参与出参字段名和现行 catalog 一致。两个文件都没改。
- 已改：点名改了用例哪一格、脚本哪一段。编号未变。同册其它 FUNC 行未被改。
- 不改并说明：页面打不开、点击或填表超时、接口 404、或仅是用例写 chain_id 而表单字段名是 chainId。文件保持不动。
父控核对 diff 只触及这一行和这一个 yaml。不符合就打回这一条，不要把这一条记成通过。打回只挡住这一条，其它册照常派。
进度写法见【连跑】。547 条全部有结论后给总表，在那之前不要用汇报代替派单。

━━━━━━━━ 子任务包（整段作为子 agent 任务描述，父控填空） ━━━━━━━━

【身份】qa-agent 执行子。只处理一条用例和它的一条脚本。
【编号】FUNC-_____
【用例册】（父控填仓库内相对路径）
【脚本】agent-delivery/qa/as-built/scripts/SDWJSF-KJZTFWSFK/…/cases/FUNC-_____.yaml
【catalog 页】entry_id=_____
【接口标题】_____

【质量规则】只认这份，它是 da66a499 那次编写用例定稿后的规则，不要回对话记录里找早期子任务包：
agent-delivery/qa/algo-lib-api-case-playbook.md
读「编写方法论」§1–§5、§7，以及「编写细则」A、C、D、F、G。
要点：步骤只写页面操作并写出具体参数赋值；预期按该接口现行 sampleResponse 与 responseFields 写字段名和类型；反向只动一个参数；不断言 HTTP 状态码当主体；不按 field 一行一条；不读算法实现。
对话记录里这些说法作废，禁止照做：新编整册、改用 API 编号、从 00001 取号、环境 http://111.198.38.90:50897/、打开浏览器盘点。

【页面对应的真源】只读 repos/lumen-ui-algo-apiview：
- src/catalog/*.json 里本 endpoint 的 params、sampleRequest、responseFields、sampleResponse、status
- 本页 Vue 里表单项展示名（与 params 名如何对应）
现行 catalog 与现行用例冲突时，以现行 catalog 为准。一次试跑的返回体不是真源。catalog 仍列出的字段，不得因为上次超时或返回里暂时没有就从预期删掉。

【先判定，再决定动不动文件】
读这一行的测试步骤、前置条件、预期结果、测试内容。对照上面的真源。
下列情况两个文件都不改，回复「不改」并写原因：
- 失败是页面没打开、进页后点击全超时、填表超时，而入参名和出参字段名仍然与 catalog 一致
- 接口 status 或上次结果是 404，catalog 契约没变
- 用例写 chain_id=某 id，脚本填的是表单字段 chainId，catalog 参数就是这个 id。这是字段映射，不是不一致
用例与 catalog 一致时，回复「一致」，不要为了让断言变绿而改字。

只有这些才算不一致，才允许改：
- 步骤多写了 catalog params 里没有的入参，或少写了文档必填入参
- 步骤里的取值不是该参数的合法示例，或选错了接口标题
- 预期点名的字段名不在现行 responseFields / sampleResponse 里，或现行文档有的返回字段预期没写
- 测试内容与步骤互相矛盾（例如步骤和 params 都没有 chainId，测试内容却写填写 chainId）

【改用例】
只改这一行 FUNC-_____ 的单元格。编号、同册其它行、表头、其它接口的组合一律不动。
句式沿用本册已有行和 playbook 正例。步骤写成可独立执行的赋值句。预期写字段名与类型，不写死 sample 里的具体数字当唯一判定。
不新增 FUNC 编号，不改 code-registry，不改 coverage-fp，不改测试记录 xlsx。

【改脚本】
只有用例这一行确实改了，才重写这一个 yaml。没改用例就不要改脚本。
脚本规则用 agent-delivery/qa/as-built/prompts/algo-lib-script-child.md 全文，并遵守：
- 断言只查 .test-workbench .json-viewer 的第一条（.first()），字段名只来自改完后的预期
- 短标题点选用 filter({ hasText: /^\s*短标题\s*$/ })，不要写成 \\s
- chainId 只在改完后的步骤要求填写时才 set，并断言 .arco-tag 含该 id
- 用例写点击调用、按钮是执行接口，差异写 as_built_note
- 禁止改断言去迎合未发布页面或某次失败返回
不要改同目录其它 yaml，不要改 index.yaml。

【回复格式】
结论：一致 | 已改 | 不改
原因：对照了 catalog 的哪几个字段
若已改：用例改了哪些列；脚本改了 set 还是 expect
确认：编号未变；同册其它 FUNC 未改；未跑脚本；未改 xlsx
