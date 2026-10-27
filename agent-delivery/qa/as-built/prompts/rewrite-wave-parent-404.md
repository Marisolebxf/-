本文件是「404 已有脚本重跑」父控提示词全文。新对话只说：读取并执行本文件。不要把下文再贴进对话。先停掉还在派单的旧重写父控，避免两份父控同时改登记表。

【身份】qa-agent 父控。任务 QA-KJZTFWXT-BLINE-SCRIPT-REWRITE-L01。只编排和改编排表。不写脚本，不跑 run-scripts，不判断步骤对错。
【工作根】当前会话的 gkx-orchestration 仓库根。不要写成 /Users/roy/... 。
【必读】本文件，以及同目录 rewrite-wave-child-404.md、rewrite-wave-child.md。与 rewrite-wave-parent.md 冲突时以本文件为准：本波只重跑旧 404，不派 pending。
【环境】https://edu.itic-sci.com/tts/svcz/  路径前缀 /tts/svcz/。禁止内网 10.50.69.111:30892、10.50.69.111:30888、111.198.38.90:50892。
【派单表】agent-delivery/qa/as-built/script-rewrite-ledger-KJZTFWXT.csv
【派谁】同时满足才派：status=blocked；note 含 ENV-EDU、svcz，或同时含 404 与 edu / SPA / 页面不存在；脚本目录已有 cases/FUNC-xxxxx.yaml。没有 yaml 的不派。note 已是 ENV-30892-ENTRY-404 的不派。pass、pending、fail、其它 blocked 不派。不要按 gap 队列派单。
【并发】同时最多 3 个。不要补到 6。
【禁止】创建 .rewrite-loop-armed；改 .cursor/hooks/rewrite-loop-stop.py；git push；有头浏览器；IDE / MCP 浏览器；--headless false；未打印 playwright-ok 和 login-ok 就派子 agent；缩短子提示词；让子 agent 先改 yaml 再重跑。

【开工停手】登记表里若已有 running，先确认不是另一个父控留下的。是别的父控还在派：本对话停止，不要改那些行。本波已跑过的不重派：note 为「30892 重跑绿」的 pass、以及 note 已不再含 ENV-EDU / svcz / 旧 404 的 fail 和 blocked，都不派。

【续跑】2026-10-22 01 时许父控探活 networkidle 超时，写了 agent-delivery/qa/as-built/.env-down 后停派。那是网络抖动，不是这批用例仍 404。开工时文件还在：先做下面的探活。打印 login-ok 后删掉 .env-down，再派。探活失败就保留文件并停止。子 agent 看到 .env-down 会整批 blocked，所以未 login-ok 不得派。

【Playwright】派任何子 agent 之前，父控自己做一次。不要派子 agent 去装。探活只用无头 Chromium。
1. export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; nvm use 24
   node -v 必须是 v24。禁止 Homebrew node，禁止 Cursor 自带 node。
2. 在 agent-delivery/qa/as-built/tools 执行：
   node -e "const {chromium}=require('playwright'); chromium.launch({headless:true}).then(async b=>{const v=await b.version(); await b.close(); console.log('playwright-ok', v);}).catch(e=>{console.error('playwright-bad', e); process.exit(1);})"
3. 未打印 playwright-ok：只由父控在 tools 目录处理。缺模块则 npm install；缺浏览器则 npx playwright install chromium。修完再跑第 2 步。仍失败就停止派发。
4. 仍在 tools 目录做无头探活。不要用 networkidle 判定整站。看到登录字样即 login-ok：
   node -e "const {chromium}=require('playwright'); (async()=>{const b=await chromium.launch({headless:true}); const p=await b.newPage(); const r=await p.goto('https://edu.itic-sci.com/tts/svcz/login',{timeout:45000,waitUntil:'domcontentloaded'}); await p.waitForFunction(()=>/用户名|密码|登录/.test(document.body?.innerText||''),{timeout:20000}); const t=await p.locator('body').innerText(); console.log('probe', r&&r.status(), t.replace(/\s+/g,' ').slice(0,120)); await b.close(); if(!r||r.status()>=500||!/用户名|密码|登录/.test(t)) process.exit(1); console.log('login-ok');})().catch(e=>{console.error('probe-bad',e); process.exit(1);})"
   连不上、5xx、没有登录字样：写 agent-delivery/qa/as-built/.env-down（一行原因），停止派发。单条入口 404 不算整站停机。login-ok 后若 .env-down 已存在，删掉它再派。
5. 子 agent 交卷写了 .env-down、原因是登录超时或网络中断：父控按第 4 步再探一次。login-ok 就删掉 .env-down，把该条 note 改回原来的 ENV-EDU 备注、status 改回 blocked，然后继续派。不要把一次抖动当成整站停机。

【死 running】仅处理本波派出去的 running。run 目录没有 result.yaml、对话已死：改回 blocked，note 保持原 404 备注，以便再派。已有 result.yaml：按子 agent 交卷的 verdict 补记，note 不要写回 ENV-EDU。

【子提示词】先整份下发 rewrite-wave-child-404.md（从【本波先重跑】起），再整份下发 rewrite-wave-child.md（从【身份】起）。禁止删段。子 agent 没有上一轮记忆，下面这些必须替换文件里的【】，不能让它自己查：
- 编排表：FUNC_ID、优先级、entry_id、script_rel、上次 note
- 用例册只读这一行：功能项（作标题）、前置条件、测试步骤、预期结果。测试步骤原样填进【用例步骤】，前置原样填进【前置条件】，前置为空就写「无」。不要把前置改写成点击，不要加「当前在深链落地页」，不要自己补「查看结果」或产业选择
- 该目录 fixtures/entry-seed.yaml：catalog_path、menu_path、menu_leaf、sibling_for_sidebar_entry、forbidden_paths。没有 seed 时父控从 catalog/KJZTFWXT.yaml 建一次再抄。步骤写侧栏或菜单进入 → 进入方式填侧栏，否则填深链
- 确认该目录 testdata.yaml 的 base_url 已是 https://edu.itic-sci.com/tts/svcz/ 。不对由父控改，不派子 agent 改
用例册「路由route」和 catalog_path 不一致时，子提示词仍填 catalog_path。
发出前自检：提示词里必须同时有「本波先重跑」「ENV-30892-ENTRY-404」「别的 cases/*.yaml」「失败时主区文字」「禁止 --headless false」「arco-cascader-view」「lumen-ui-topic」，以及本条 catalog_path 的真实路径（不能留下方括号）。缺一不派。一条只能有一个 FUNC 号。

【进度】每次新派前只输出一行：已收/执行/待重跑/pass/本波。已收=本波开跑时在名单里、现在已不再符合【派谁】的条数。执行=running（本波 -404 run_dir）。待重跑=仍符合【派谁】。pass=登记表 note 为「30892 重跑绿」的条数（本波 30892 无头重跑成功）。本波=开跑时数一次，之后不变。输出后立刻派，不要写段小结。
【循环】待重跑>0 就继续。交卷唤醒后重复。最后一个动作必须是派子 agent。
【强度】ponytail full

开干：确认没有别的父控 → 无头 Playwright → login-ok → 删掉残留的 .env-down → 数本波（只数仍符合【派谁】的行）→ 输出进度行 → 按 child-404 再 child 原文补满 3 路。
