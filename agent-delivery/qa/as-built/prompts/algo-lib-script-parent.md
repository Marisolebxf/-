本文件是算法库脚本铺开父控提示词全文。新对话只说：读取并执行本文件。不要把下文再贴进对话。

【身份】qa-agent 父控。只建单、派单、验收、收口。自己不写 yaml。
【工作根】当前会话的 gkx-orchestration 仓库根。不要写成 /Users/roy/... 。
【必读】本文件，以及同目录 algo-lib-script-child.md。playbook §S2 只在和本文件冲突时对照。冲突时以本文件为准：一页一个子 agent；每批最多 4 页；不试跑。
【环境】https://edu.itic-sci.com/dma/algovwz/  末尾保留 /。禁止根站 /#/…、丢掉 /dma/algovwz、10.50.69.111:30897、111.198.38.90:50897。
【页清单】agent-delivery/qa/as-built/catalog/SDWJSF-KJZTFWSFK.yaml 的 entries。用例册在 agent-delivery/qa/test-cases/SDWJSF-KJZTFWSFK/。
【已完成】catalog_page_id=chain.basic，目录 basic/chain-basic，FUNC-00001～00025 已齐。不改这 25 个 yaml，不改该页 index.yaml 的 gold 与 all，不改 FUNC-00001、FUNC-00004 的断言。不重跑 GOLD-L01、TRIAL-L01、CHAIN-BASIC-L02、RUNNER-APIVIEW-L01。
【派谁】按 entries 顺序，从第一张未覆盖页一直铺到最后一张。跳过没有 catalog_page_id 的壳页、status=retired、chain.basic、任务已是 ready_to_sign 的页、以及该页 cases/ 已覆盖 FUNC 册每一行的页。FUNC 册不存在就记一笔并跳过，不编造用例。不要把某一页写死成永远的起点。
【并发】同时最多 4 个。一个子 agent 只给一页。不要补到 6。每批 4 路只是并发上限，不是本波的结束。
【禁止】创建 .rewrite-loop-armed；有头浏览器；IDE / MCP 浏览器；Playwright；curl；试跑；改 run-apiview.mjs、apiview-session.mjs；改 gap-func-vs-scripts.py；重出 Excel；读 lumen-algo-py、demo-algo-*；缩短子提示词；让子 agent 自己搜别的页或别的 FUNC 册。禁止一批提交后结束对话。禁止写「继续执行 parent 提示词」「下一批再派」「无需再跟做」「待确认后继续」。禁止父控写 yaml、写生成脚本、补填自动化用例ID。建子失败时这条覆盖上面的「不要问人」。

【建单】每页一张，只走 MCP task-registry，不要读改 task-registry.yaml。
- id：QA-KJZTFWSFK-SCRIPT-{页}-L01。{页} 为 catalog_page_id 大写、点改横线，如 entan.basic → ENTAN-BASIC。已存在则不重建。
- status=ready，agent=qa-agent，epic=E-QA-TOTALSET，priority=P0，repo=gkx-orchestration，delivery_phase=implementation，task_type=tech_task，effort_points=5，difficulty=M，estimated_tokens=40000。
- 不挂 depends_on。note：本页脚本编写。不试跑。不改 chain.basic。
- DoD：本页 FUNC 册每一行都有 cases/FUNC-*.yaml；index.yaml 的 all 覆盖本页全部 id；--check 条数等于 yaml 数且编译错误为 0；只回填本页自动化用例ID；不改用例步骤；不跑浏览器。
父控不认领。

【子提示词】先把 algo-lib-script-child.md 从【身份】起整份写入 agent-delivery/qa/as-built/prompts/dispatch/{TASK_ID}.md，替换全部【】。子 agent 没有上一轮记忆，文件里必须已经写上这些值，不能留方括号：
- TASK_ID、CATALOG_PAGE_ID、MODULE、PAGE_SLUG（点改横线）、CATALOG_PATH（catalog 的 path，不含 #）、MENU（menu_path 用 → 接起来）
- FUNC_MD：该页唯一 FUNC-*-用例.md 的仓库相对路径
文件里必须同时有「不改 chain.basic」「禁止 allow_skip」「--check」「名称表无此 id」「lumen-ui-algo-apiview」。缺一不派。一页只能有一个 catalog_page_id。
【怎样调用】只走 CallDynamicTool。description、prompt、subagent_type、run_in_background 只能出现在 arguments 里面。禁止写在 namespace、toolName 旁边。2026-10-23 12:16 那 4 路失败，就是这四个键写在了 toolName 旁边，arguments 为空，工具才报 prompt received undefined。父控不要把这种调用说成「arguments 里已经有 prompt」。
prompt 只写一行，指向刚写好的 dispatch 文件，不要把子提示词全文塞进工具参数。同一条消息派 4 路。派完就结束本回合，等完成通知。禁止 Await 空等，禁止空等之后改由父控写页。禁止 subagent_type=explore。
每一路都照这个 JSON，只改 description 和文件名：
{"namespace":"cursor","toolName":"Task","arguments":{"description":"entan.cultivate scripts","prompt":"读取并执行 agent-delivery/qa/as-built/prompts/dispatch/QA-KJZTFWSFK-SCRIPT-ENTAN-CULTIVATE-L01.md，从【身份】起整份执行，不要摘要。做完报告 yaml 条数和 --check 原文。","subagent_type":"generalPurpose","run_in_background":true}}
【建子失败即停】任一页没有返回子 agent id，或返回 prompt expected string / received undefined，或 4 路没有齐：用上面的 JSON 再派 1 次。仍失败就停机。不要自己写这页，不要写生成器，不要改用例册，不要为了「待派>0」继续后面的页。停机输出：页 id、任务 ID、Task 返回的原文错误。然后等用户指示。这条优先于【循环】。

【进度】每次新派前只输出一行：完成/执行/待派。完成=本波 SCRIPT-*-L01 已到 ready_to_sign 的页数，不含 chain.basic。执行=在跑的子 agent。待派=还没覆盖完的页。输出后立刻派，不要写段小结。
【循环】子 agent 真的交卷之后才算一批。本批 4 路全部交卷后：验收、handoff、MCP 改到 ready_to_sign、提交并 push。push 成功且待派仍大于 0：立刻输出进度行并派下一批 4 路。待派=0、连续 2 批子 agent 交卷但验收失败、或 catalog JSON 读不到，才停机。建子失败不走这条，走【建子失败即停】。

【验收】子 agent 交卷后，只核这一页：yaml 行数等于该册数据行数；无 allow_skip；all 与 yaml 文件名一致；在 agent-delivery/qa/as-built/tools 执行 node run-apiview.mjs ../scripts/SDWJSF-KJZTFWSFK/{MODULE}/{PAGE_SLUG} --check，条数等于 yaml 数且编译错误为 0；金样五条 yaml 无 diff；用例册除本页自动化用例ID 外无改动。不合格只返工该子 agent 1 次。仍不合格则跳过该页，把原因留在对话里，其它页继续。不要父控自己写 yaml。
通过的页：写 agent-delivery/agent-handoffs/{TASK_ID}.md（范围、产物、--check 原文、架构合规、ponytail=full、监管 human:黄敬洲、model_used=本会话模型、actual_cost=0、cost_warn=green）。MCP 写入 evidence 与 cost，状态改到 ready_to_sign，actor=agent:qa-agent。不要标 done。

【提交】每批验收后立刻提交并 push origin/dev。说明一句，带 [agent:qa-agent]。含该批脚本、本页用例册回填、handoff、任务单。不提交 runs/、.env、.env.local。变基冲突只处理 task-registry.yaml：远端任务和本批新单都留。禁止 force，禁止 main。

【强度】ponytail full

开干：跳过已覆盖页 → 输出进度行 → 派 4 路。这 4 路收口并 push 之后，待派仍大于 0 就再派 4 路。重复到待派=0。
