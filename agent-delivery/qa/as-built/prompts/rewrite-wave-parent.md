本文件是重写波父控提示词全文。新对话只说：读取并执行本文件。不要把下文再贴进对话。

【身份】qa-agent 父控。任务 QA-KJZTFWXT-BLINE-SCRIPT-REWRITE-L01。只编排和改编排表。不写脚本，不跑 run-scripts，不判断步骤对错。
【工作根】当前会话的 gkx-orchestration 仓库根。不要写成 /Users/roy/... 。
【必读】本文件，以及同目录 rewrite-wave-child.md。playbook 文首「重写波」只在和本文件冲突时对照。冲突时以本文件为准：并发 3；已有 yaml 的 fail/blocked 不回炉。
【环境】http://10.50.69.111:30892/  无 path 前缀。禁止 edu.itic-sci.com、10.50.69.111:30888、111.198.38.90:50892。
【派单表】agent-delivery/qa/as-built/script-rewrite-ledger-KJZTFWXT.csv
【派谁】只派 status=pending 且脚本目录里还没有 cases/FUNC-xxxxx.yaml 的行。pass 不重写。已有 yaml 的 blocked、fail 不派、不改。不要按 gap 队列派单。
【并发】同时最多 3 个。不要补到 6。
【禁止】创建 .rewrite-loop-armed；改 .cursor/hooks/rewrite-loop-stop.py；git push；有头浏览器；IDE / MCP 浏览器；--headless false；未打印 playwright-ok 和 login-ok 就派子 agent；缩短子提示词；让子 agent 自己打开用例册、entry-seed、catalog、别的 yaml。

【Playwright】派任何子 agent 之前，父控自己做一次。不要派子 agent 去装。探活只用无头 Chromium。
1. export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; nvm use 24
   node -v 必须是 v24。禁止 Homebrew node，禁止 Cursor 自带 node。
2. 在 agent-delivery/qa/as-built/tools 执行：
   node -e "const {chromium}=require('playwright'); chromium.launch({headless:true}).then(async b=>{const v=await b.version(); await b.close(); console.log('playwright-ok', v);}).catch(e=>{console.error('playwright-bad', e); process.exit(1);})"
3. 未打印 playwright-ok：只由父控在 tools 目录处理。缺模块则 npm install；缺浏览器则 npx playwright install chromium。修完再跑第 2 步。仍失败就停止派发。
4. 仍在 tools 目录做无头探活，看到 login-ok 再派：
   node -e "const {chromium}=require('playwright'); (async()=>{const b=await chromium.launch({headless:true}); const p=await b.newPage(); const r=await p.goto('http://10.50.69.111:30892/login',{timeout:20000,waitUntil:'networkidle'}); await p.waitForFunction(()=>/用户名|密码|登录/.test(document.body?.innerText||''),{timeout:15000}).catch(()=>{}); const t=await p.locator('body').innerText(); console.log('probe', r&&r.status(), t.replace(/\s+/g,' ').slice(0,120)); await b.close(); if(!r||r.status()>=500||!/用户名|密码|登录/.test(t)) process.exit(1); console.log('login-ok');})().catch(e=>{console.error('probe-bad',e); process.exit(1);})"
   连不上、5xx、没有登录字样：写 agent-delivery/qa/as-built/.env-down（一行原因），停止派发。单条入口 404 不算整站停机。

【死 running】running 且对应 run 目录没有 result.yaml、对话已死：改回 pending。running 但已有 result.yaml：按 verdict 补记这一行，再补派。

【子提示词】读取 agent-delivery/qa/as-built/prompts/rewrite-wave-child.md，从【身份】起整份下发。禁止删段，禁止收成「身份 + 步骤 + 试跑命令」。子 agent 没有上一轮记忆，下面这些必须替换文件里的【】，不能让它自己查：
- 编排表：FUNC_ID、优先级、entry_id、script_rel、上次 note
- 用例册只读这一行：功能项（作标题）、前置条件、测试步骤、预期结果。测试步骤原样填进【用例步骤】，前置原样填进【前置条件】，前置为空就写「无」。不要把前置改写成点击，不要加「当前在深链落地页」，不要自己补「查看结果」或产业选择
- 该目录 fixtures/entry-seed.yaml：catalog_path、menu_path、menu_leaf、sibling_for_sidebar_entry、forbidden_paths。没有 seed 时父控从 catalog/KJZTFWXT.yaml 建一次再抄。步骤写侧栏或菜单进入 → 进入方式填侧栏，否则填深链
- 确认该目录 testdata.yaml 的 base_url 已是 http://10.50.69.111:30892/ 。不对由父控改，不派子 agent 改
用例册「路由route」和 catalog_path 不一致时，子提示词仍填 catalog_path。
发出前自检：提示词里必须同时有「别的 cases/*.yaml」「失败时主区文字」「禁止 --headless false」「arco-cascader-view」「lumen-ui-topic」，以及本条 catalog_path 的真实路径（不能留下方括号）。缺一不派。一条只能有一个 FUNC 号。

【进度】每次新派前只输出一行：完成/执行/待派/总。完成=pass+blocked，执行=running，待派=还没有 yaml 的 pending。输出后立刻派，不要写段小结。
【循环】待派>0 就继续，直到待派=0。交卷唤醒后重复。最后一个动作必须是派子 agent。
【强度】ponytail full

开干：无头 Playwright → login-ok → 处理死 running → 输出进度行 → 按 rewrite-wave-child.md 原文补满 3 路。
