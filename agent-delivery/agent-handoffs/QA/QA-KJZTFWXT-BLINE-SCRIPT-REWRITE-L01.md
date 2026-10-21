# QA-KJZTFWXT-BLINE-SCRIPT-REWRITE-L01 · 专题脚本重写中途交接

> 2026-10-21 晚：写法已改到提示词文件。任务未完成，状态保持 `in_progress`。算法库不在本单。下文「叫停时进度」是凌晨快照，不要按那段的地址和并发续跑。

## 续跑（新对话先读这段）

1. 新对话只说：读取并执行 `agent-delivery/qa/as-built/prompts/rewrite-wave-parent.md`。先停掉还在派单的旧父控，避免两份父控同时改登记表。已发出的 `_dispatch-FUNC-*.md` 是当时的副本，不会跟着模板变。
2. 环境 `http://10.50.69.111:30892/`（无 path 前缀）。禁止 `edu.itic-sci.com/tts/svcz`、`10.50.69.111:30888`、`111.198.38.90:50892`。
3. 本波并发 3。只派还没有 `cases/FUNC-xxxxx.yaml` 的 `pending`。不重写已有 pass / blocked / fail。不重派 `FUNC-02593`、`FUNC-03535`。
4. 父控整份下发 `prompts/rewrite-wave-child.md`，只替换【】。测试步骤、前置原样抄。不把前置改成点击，不写「当前已在某页」。
5. 子 agent 写 yaml 前只读 `repos/lumen-ui-topic` 里本条路由对应的一个页面文件：`src/router/menu.ts` 对上 path 和 workspace；该项没写 component 就读同一 path 上写了 component 的项；页面按 workspace 转到另一组件时只再读那个分支文件。不读 `demo-ui-topic`，不顺着 import 读级联、过程页、记录表。源码只落实步骤里已有的点击；按钮可见名和源码不一致时点源码里的名字，仍算同一步。源码和 30892 不一致时，以「失败时主区文字」为准。
6. 无头试跑，最多两次。红了可改失败的那条 assert，或按「失败时主区文字」补一次点击。禁止第 3 次。禁止 `--headless false`、IDE / MCP 浏览器。
7. 不要创建 `.rewrite-loop-armed`，不要恢复 rewrite-loop hook。
8. 用例册还没按红线 3.1 改。现行短步骤仍会停在配置页或过程页。本阶段不改用例正文。

## 阶段结论（2026-10-21）

17:28 之后抽查的 fail，多数是脚本没有把页面点到预期要看的状态。用例把路径写成前置里的状态句，步骤只剩最后一下。父控不知道中间点击，不能代补。完整点击应写在用例测试步骤里，第一条是 `goto`（`prompts/_case.md` 红线 3.1）。本阶段只改说明，不改用例册。

子 agent 顺序：按抄来的步骤写 yaml（写前只读上面那一个页面文件）→ 一次无头试跑 → 红则只读失败时主区文字 → 第二次试跑 → 改自己那一行登记表后停。没有实勘、复勘、单独验收。试跑绿即 pass。

`run-scripts.mjs` 在 fail / blocked 时把 `main`（否则 `body`）正文前 1500 字写入 `steps.md`「失败时主区文字」。

本阶段提交不含登记表、在途 yaml、`_dispatch-FUNC-*.md`。那些是波次现场。

## 凌晨叫停记录（历史，不要按这里续跑）

1. 当时父控提示词嵌在 playbook「0. 新对话 Kickoff」。该段已撤下，改指向 `rewrite-wave-parent.md`。
2. 当时环境写成 edu，并发写成 6。这两条都已作废。
3. 自动续跑 hook 当时已删除。不要再创建 `.rewrite-loop-armed`。

## 叫停时进度（2026-10-21 03:14 之后未再派）

**1217/0/363/1580**

| status | 条数 | 续跑 |
|--------|------|------|
| pass | 540 | 不重派，不改 yaml |
| blocked | 677 | 不重写。其中约 502 条 note 含 `ENV-EDU-TTS-SVCZ-404-001` 或 SPA 404，脚本多已落盘，等环境恢复后另开复跑，不要当待写 |
| fail | 2 | `FUNC-02593`（industry-center/overview）、`FUNC-03535`（industry-center/regional-compete）。note 已是环境 404，续跑改为 blocked，不要当脚本错误回炉 |
| pending | 361 | 这才是接着写的队列 |
| running | 0 | 无在途子 agent |

分模块：enterprise 609（pass 437 / blocked 155 / pending 17）；industry-center 477（pass 63 / blocked 362 / fail 2 / pending 50）；service 453（blocked 159 / pending 294）；shell 41（pass 40 / blocked 1）。

pending 头：`service/rec-cultivate` 36，`service/org-capability` 34，`service/org-trend` 28，`service/portal-shenzhen` 28，`service/chain-graph` 27，`service/rec-attract` 27，`service/portal-region` 27，`service/chain-shortboard` 26，`service/sz` 26，`service/portal-capability` 26，`industry-center/report-deep` 18，`enterprise/detail` 12。

## 故障范围（已写进 playbook，续跑必须遵守）

| 看到什么 | 停哪里 |
|----------|--------|
| 首页或登录打不开（连不上、5xx、401/403 重登仍失败、200 但空白/错误壳） | 停整批，写 `.env-down` |
| 首页和登录正常，只有本入口 `catalog_path` 打不开 | 只停该 `script_rel`，其它入口继续。note=`ENV-ENTRY-UNREACHABLE`，不要写 `.env-down` |
| 页面已打开，缺按钮、缺数据、断言不符，或页内单个接口 4xx/5xx | 只停这一条 |
| 429 | 等 20 秒再探一次；仍 429 则本条 `ENV-THROTTLE`，不停整批 |

叫停原因：edu 上大量入口 SPA 404（含登录页），子 agent 仍在写完整脚本后才 blocked，token 空烧。不是 540 条 pass 突然失效。

## 已落地、续跑不要重做

- 企业查询 44 条路由对齐 catalog：`/enterprise/enterprise-search`。禁止再写 `/development/search`。侧栏进入先 goto `/enterprise/attraction` 再点「企业查询」。seed：`scripts/KJZTFWXT/enterprise/search/fixtures/entry-seed.yaml`。
- 子 agent 自己用 `fcntl` 改本行。禁止 `no ledger`。同一条脚本错误最多重跑 1 次。
- 编排表与已生成 `scripts/KJZTFWXT/**` 已在 `origin/dev`。本交接不改这些 yaml。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:黄敬洲` |
| claim_type | 长任务父控编排（registry 已是 `in_progress`，本交接不改状态） |
| 说明 | DoD 未满足：表中仍有 pending/fail。不要把本文件当成签收。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 脚本波按 playbook 执行；本文件只交接，不缩验收。 |

## 问题清单

- edu 环境 SPA 404 未恢复前，不要续派 pending。
- 工作区里另有一批已暂存、未纳入本交接提交的环境地址替换（用例册、catalog、算法库地址、探针删除）。续跑以 playbook 文首为准，不要把那批暂存当成已推送。

## 修改内容

- 本 handoff。
- 随提交带上 playbook 的入口 seed、路由闸门、三层故障范围、子 agent 探活，以及 `_script.md` 路由闸门。
- `.cursor/hooks/rewrite-loop-stop.py` 已删除。当时未武装，且只匹配旧父控 `573eb243`。

## 测试结果

- 2026-10-21 03:22 核对：`running=0`，父控对话 `573eb243` 最后一句话是不补派，之后无新子 agent、无新用例 yaml。
- 企业查询抽测（历史）：深链 goto 能打开；失败在控件断言，不是 catalog 路由 404。

## 遗留风险

- 自动续跑 hook 已删除，不会再把补派打回旧父控 `573eb243`。
- blocked 里还有非 404 的环境缺口（对比篮、评估历史、结果壳等）。环境恢复后按 note 里的 `ENV-*` 复跑，不要重写。
- 其它入口的 `/enterprise-center/overview` 未做批量替换。新脚本以 catalog / entry-seed 为准。

## CI/CD

- 分支：`gkx-orchestration` `dev`
- commit：见本提交
- pipeline：编排仓无业务 CI
- 部署：无
- 试跑环境：`http://10.50.69.111:30892/`（2026-10-21 晚；此前 edu 地址作废）

## 涉及文件

- `agent-delivery/qa/as-built/script-rewrite-ledger-KJZTFWXT.csv`
- `agent-delivery/qa/as-built/script-backfill-playbook.md`
- `agent-delivery/qa/as-built/prompts/_script.md`
- `agent-delivery/qa/as-built/scripts/KJZTFWXT/**`
- `.cursor/hooks.json`（已删）
- `.cursor/hooks/rewrite-loop-stop.py`（已删）
