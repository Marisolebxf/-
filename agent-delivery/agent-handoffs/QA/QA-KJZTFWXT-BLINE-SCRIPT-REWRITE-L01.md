# QA-KJZTFWXT-BLINE-SCRIPT-REWRITE-L01 · 专题脚本重写中途交接

> 2026-10-21 叫停时的续跑说明。任务未完成，状态保持 `in_progress`。算法库不在本单。

## 续跑（新对话先读这段）

1. 父控只编排。提示词用 `agent-delivery/qa/as-built/script-backfill-playbook.md` 文首「0. 新对话 Kickoff」原文。子 agent 用同文件「重写波 · 子 agent」原文，一条一个 FUNC。
2. 派单表只认 `agent-delivery/qa/as-built/script-rewrite-ledger-KJZTFWXT.csv`。`pass` 不重派。`pending` 才是还要写脚本的队列。
3. 开工前先探活 `https://edu.itic-sci.com/tts/svcz/` 和 `/login`。页面算打开：不是连不上、不是 5xx，且约 8 秒内能看见登录框或侧栏/主区。HTTP 200 但空白或错误壳，与 5xx 同样算没打开。探活失败就停，不要派。
4. 登记表 note 里曾写 `http://10.50.69.111:30888/` 已探活。那是过时备注。环境以 playbook 文首 edu 为准。
5. 自动续跑 hook 当前未武装（没有 `agent-delivery/qa/as-built/.env-down`，也没有 `.rewrite-loop-armed`）。新父控对话若要武装：先把 `.cursor/hooks/rewrite-loop-stop.py` 里的 `PARENT` 改成新对话 id（现为旧父控 `573eb243`），再创建 `.rewrite-loop-armed`。不要在本交接对话里武装。
6. 进度行格式：`完成/执行/待派/总`。完成 = pass + blocked，执行 = running，待派 = pending + fail。同时最多 6 路。

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
- `.cursor/hooks/rewrite-loop-stop.py` 仅在 `.rewrite-loop-armed` 存在且对话 id 匹配时补派。当前未武装。

## 测试结果

- 2026-10-21 03:22 核对：`running=0`，父控对话 `573eb243` 最后一句话是不补派，之后无新子 agent、无新用例 yaml。
- 企业查询抽测（历史）：深链 goto 能打开；失败在控件断言，不是 catalog 路由 404。

## 遗留风险

- 旧父控对话若有人重建 `.rewrite-loop-armed` 且不改 `PARENT`，hook 会把补派打回 `573eb243`。
- blocked 里还有非 404 的环境缺口（对比篮、评估历史、结果壳等）。环境恢复后按 note 里的 `ENV-*` 复跑，不要重写。
- 其它入口的 `/enterprise-center/overview` 未做批量替换。新脚本以 catalog / entry-seed 为准。

## CI/CD

- 分支：`gkx-orchestration` `dev`
- commit：见本提交
- pipeline：编排仓无业务 CI
- 部署：无
- 试跑环境：`https://edu.itic-sci.com/tts/svcz/`

## 涉及文件

- `agent-delivery/qa/as-built/script-rewrite-ledger-KJZTFWXT.csv`
- `agent-delivery/qa/as-built/script-backfill-playbook.md`
- `agent-delivery/qa/as-built/prompts/_script.md`
- `agent-delivery/qa/as-built/scripts/KJZTFWXT/**`
- `.cursor/hooks.json`
- `.cursor/hooks/rewrite-loop-stop.py`
