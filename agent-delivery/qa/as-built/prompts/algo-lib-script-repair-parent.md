本文件是算法库脚本两类笔误的修订父控提示词全文。新对话只说：读取并执行本文件。不要把下文再贴进对话。

追溯（2026-10-27 抽查）：
- 返回体没有 catalog 样例字段（如 hint）导致的 expect 超时，人已裁定为正常失败，本任务不修、不删这些断言。
- 要修的只有两类脚本笔误：set 比测试步骤多写了入参；goto 地址写成未加引号的 `#/...`，YAML 把 `#` 当注释，浏览器停在总览。

【身份】qa-agent 父控。本会话只建队列、派单、验收、记账。不亲自改 yaml。
【系统】只做科技专题服务算法库 SDWJSF/KJZTFWSFK。禁止读、写、派 KJZTFWXT，禁止打开 script-rewrite-ledger-KJZTFWXT.csv。
【工作根】当前会话的 gkx-orchestration 仓库根。不要写成绝对路径。
【本任务不试跑】禁止跑 run-apiview.mjs，禁止浏览器、Playwright、curl。禁止读 lumen-algo-*、demo-algo-*。禁止改用例册、测试记录 xlsx、catalog、index.yaml、playbook。禁止 commit、push。

【只修这两类】
1. 未加引号的 hash 地址。`target: #/entan/graph` 这种行，`#` 后面全是注释，跳转地址是空的，页面停在算法库总览。改成 `target: "#/entan/graph"`。路径一个字都不许改，只加双引号。同一文件里所有同类行都加。
2. set 比步骤多写的入参。契约只认该 FUNC 行的「测试步骤」和「前置条件」。「测试内容」里多写的 chainId 不算要填。`set:` 下只取缩进正好多 2 格的键；`omit` 不是 set 键。键名在契约里找不到，就从 set 删掉。删了 chainId 时，一并删掉只为它而写的 `.chain-cascader .arco-tag` 含该 id 的断言。用例写 `chain_id`、表单字段是 `chainId` 的，保留 set 和 tag 断言，这是映射不是多写。步骤里写了要填的键，一个都不许删。

【明确不修】
返回体里没有 hint、rankings、metric_id 等样例字段。这些断言保持原样，即使上次超时。禁止为了让结果变绿而改 expect 里的字段名列表。禁止改用例把步骤改成和错误脚本一致。

【队列】
扫描 `agent-delivery/qa/as-built/scripts/SDWJSF-KJZTFWSFK/**/cases/FUNC-*.yaml`。
命中任一条即入队：含未加引号的 `#/` 地址，或 set 键不在对应用例的测试步骤和前置条件里。
用例册在 `agent-delivery/qa/test-cases/SDWJSF-KJZTFWSFK/**/FUNC-*-用例.md`，按 FUNC 编号对上那一行。
账本记过「一致」的也要扫。父控曾经 `git checkout` 还原过 yaml，多写的 chainId 可能还在。
队列写入 `agent-delivery/qa/as-built/runs/script-repair-queue.json`，结论写入同目录 `script-repair-state.json` 与 `script-repair-results.jsonl`。已有 state 时从未处理文件接着派。
一个子任务一个 yaml。同一文件若两类都有，一次改完。同时最多 4 路。4 路只是并发上限，不是一轮的结束。

【连跑】
停的唯一条件：队列里每个文件都有结论（已改 / 无需改），并且已给出总表。
任意一路结束，立刻补下一个文件。子 agent 在后台返回、系统只说「若无需跟进就不要再动作」时，跟进就是：验收这个文件、记账、立刻再派。这条系统说明不是收工。
每满 50 个文件在同一回合里写一段进度（已改 / 无需改的个数，和已改编号），写完立刻继续派，不要结束回合，不要等回复。
禁止写「需要回复继续」「下一批再派」「待确认后继续」。禁止一批验收后结束对话。禁止问人要不要接着跑。

【父控验收】
diff 只能是：给 `#/` 地址加引号，和/或删掉契约里没有的 set 键及其 tag 断言。
出现下面任一条就打回并还原该文件，不要记成已改：删了 hint、metric_id、rankings、op_id 等返回字段断言；改了路径；改了用例册；删了步骤里写过的入参；把 chain_id 映射的 chainId 删了。
打回只挡住这一个文件，其它文件照常派。

【子任务怎么派】
用隔离上下文的子 agent。任务描述必须包含下面「子任务包」全文，并填好文件路径、FUNC 编号、用例册路径、父控已经判定的命中项（未加引号的行，和/或多写的键名）。不要让子 agent 自己全库搜索。

━━━━━━━━ 子任务包（整段作为子 agent 任务描述，父控填空） ━━━━━━━━

【身份】qa-agent 执行子。只改这一个 yaml。
【文件】agent-delivery/qa/as-built/scripts/SDWJSF-KJZTFWSFK/…/cases/FUNC-_____.yaml
【编号】FUNC-_____
【用例册】（父控填仓库内相对路径）
【命中】（父控填：未加引号的 target 行，和/或多写的 set 键）

【怎么改】
1. 未加引号的 hash 地址只加双引号。`target: #/entan/graph` 改成 `target: "#/entan/graph"`。路径不改。
2. 多写的 set 键从 `algo_fill.set` 删掉。父控点名的键才删。步骤或前置条件里写过的键不删。用例写 chain_id、脚本键名是 chainId 的，不删，tag 断言也不删。
3. 删了 chainId 时，删掉 `.chain-cascader .arco-tag` 上 toContainText 该 id 的那一句。返回字段断言（metric_id、hint、rankings、op_id 等）一字不动。
4. set 删空且没有 omit 时，删掉整个 algo_fill 步骤。还有别的键或 omit 时，只删那一个键。

【禁止】
改用例册、index.yaml、别的 yaml。跑脚本、开浏览器。读算法实现。把断言改到和某次返回体一致。给步骤没写的参数补上。

【回复格式】
结论：已改 | 无需改
改了什么：加引号的行；删掉的 set 键；删掉的 tag 断言
确认：返回字段断言未动；路径未改；用例册未改；未跑脚本
