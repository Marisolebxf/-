本文件是「门户拆册 22 条改挂号」父控提示词全文。新对话只说：读取并执行本文件。不要把下文再贴进对话。先停掉还在派单的其它父控，避免两份父控同时改登记表。

【身份】qa-agent 父控。任务 QA-KJZTFWXT-BLINE-SCRIPT-REWRITE-L01。只编排和改编排表。不写脚本，不跑 run-scripts，不判断步骤对错。
【工作根】当前会话的 gkx-orchestration 仓库根。不要写成 /Users/roy/... 。
【必读】本文件，以及同目录 rewrite-wave-child.md。与 rewrite-wave-parent.md、rewrite-wave-parent-404.md 冲突时以本文件为准：本波只写下面 22 个新号的脚本。
【环境】http://10.50.69.111:30892/  无 path 前缀。禁止 edu.itic-sci.com、10.50.69.111:30888、111.198.38.90:50892。
【派单表】agent-delivery/qa/as-built/script-rewrite-ledger-KJZTFWXT.csv
【只派这 22 个号】05490–05511。对应关系：
- 05490 服务机构区域分布，原 03897，entry svc-portal-region，脚本目录 service/portal-region
- 05491–05496 服务机构技术能力，原 03898、03899、03900、03901、03902、03913，entry svc-portal-capability，脚本目录 service/portal-capability
- 05497–05511 深圳产业服务介绍，原 01320、01323、01327、03904、03905、03906、03907、03908、03909、03918、03919、03920、03921、03922、03925，entry svc-portal-shenzhen，脚本目录 service/portal-shenzhen
门户册里的原号不派、不改、不覆盖其 yaml。其它 pending、blocked、fail、pass 不派。
【派谁】上面 22 个号里 status=pending 的才派。其中 05491、05492、05493、05495 已有 yaml，那是旧能力榜脚本，和改挂后的用例步骤不一致，照样派，让子 agent 按抄来的步骤覆盖这一个文件。pass 不重写。不要按 gap 队列派单。
【并发】同时最多 3 个。不要补到 6。不要和另一份父控叠跑。
【禁止】创建 .rewrite-loop-armed；改 .cursor/hooks/rewrite-loop-stop.py；git push；有头浏览器；IDE / MCP 浏览器；--headless false；未打印 playwright-ok 和 login-ok 就派子 agent；缩短子提示词；让子 agent 自己打开用例册、entry-seed、catalog、别的 yaml；改门户册原号的 yaml。

【开工停手】登记表里若已有 running，先确认不是另一个父控留下的。是别的父控还在派：本对话停止，不要改那些行。

【Playwright】派任何子 agent 之前，父控自己做一次。不要派子 agent 去装。探活只用无头 Chromium。不要用 networkidle 判定整站。
1. export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; nvm use 24
   node -v 必须是 v24。禁止 Homebrew node，禁止 Cursor 自带 node。
2. 在 agent-delivery/qa/as-built/tools 执行：
   node -e "const {chromium}=require('playwright'); chromium.launch({headless:true}).then(async b=>{const v=await b.version(); await b.close(); console.log('playwright-ok', v);}).catch(e=>{console.error('playwright-bad', e); process.exit(1);})"
3. 未打印 playwright-ok：只由父控在 tools 目录处理。缺模块则 npm install；缺浏览器则 npx playwright install chromium。修完再跑第 2 步。仍失败就停止派发。
4. 仍在 tools 目录做无头探活。看到登录字样即 login-ok：
   node -e "const {chromium}=require('playwright'); (async()=>{const b=await chromium.launch({headless:true}); const p=await b.newPage(); const r=await p.goto('http://10.50.69.111:30892/login',{timeout:45000,waitUntil:'domcontentloaded'}); await p.waitForFunction(()=>/用户名|密码|登录/.test(document.body?.innerText||''),{timeout:20000}); const t=await p.locator('body').innerText(); console.log('probe', r&&r.status(), t.replace(/\s+/g,' ').slice(0,120)); await b.close(); if(!r||r.status()>=500||!/用户名|密码|登录/.test(t)) process.exit(1); console.log('login-ok');})().catch(e=>{console.error('probe-bad',e); process.exit(1);})"
   连不上、5xx、没有登录字样：写 agent-delivery/qa/as-built/.env-down（一行原因），停止派发。单条入口 404 不算整站停机。login-ok 后若 .env-down 已存在，删掉它再派。子 agent 看到 .env-down 会整批 blocked，所以未 login-ok 不得派。
5. 子 agent 交卷写了 .env-down、原因是登录超时或网络中断：父控按第 4 步再探一次。login-ok 就删掉 .env-down，把该条改回 pending，然后继续派。不要把一次抖动当成整站停机。

【路由种子】三入口侧栏都不显示，进入方式一律深链。步骤里的「点击页签」原样留在【用例步骤】，不要改成侧栏。
- svc-portal-region、svc-portal-capability 已有 fixtures/entry-seed.yaml，父控只抄，不改。
- svc-portal-shenzhen 没有 entry-seed.yaml。派深圳任何一条之前，父控写一次 agent-delivery/qa/as-built/scripts/KJZTFWXT/service/portal-shenzhen/fixtures/entry-seed.yaml，内容只这些字段：entry_id=svc-portal-shenzhen，catalog_path=/service-portal/shenzhen，menu_path 空，menu_leaf 空，sibling_for_sidebar_entry=/service-portal/overview/overview，forbidden_paths 空。写完再抄进子提示词。不要每条重写。
用例册「路由route」和 catalog_path 不一致时，子提示词仍填 catalog_path。

【死 running】仅处理本波这 22 个号里的 running。run 目录没有 result.yaml、对话已死：改回 pending。已有 result.yaml：按 verdict 补记，不要改回原号。

【子提示词】只下发 rewrite-wave-child.md，从【身份】起整份。不要下发 rewrite-wave-child-404.md。禁止删段。子 agent 没有上一轮记忆，下面这些必须替换文件里的【】，不能让它自己查：
- 编排表这一行：FUNC_ID、优先级、entry_id、script_rel、上次 note
- 用例只读编排表 case_md 指向的那一册里的这一行。不要读门户册里的原号行。功能项作标题。测试步骤原样填进【用例步骤】，前置原样填进【前置条件】，前置为空就写「无」。不要把前置改写成点击，不要加「当前在深链落地页」，不要自己补「查看结果」或产业选择
- 进入方式填：深链：steps 里 goto 只写 catalog_path
- 05491、05492、05493、05495 的【上次失败】写：目录里已有 yaml，是旧能力榜脚本，和本条用例步骤不一致。按本次抄来的步骤覆盖这一个文件。不要读旧 yaml
- 确认该目录 testdata.yaml 的 base_url 已是 http://10.50.69.111:30892/ 。不对由父控改，不派子 agent 改
发出前自检：提示词里必须同时有「别的 cases/*.yaml」「失败时主区文字」「禁止 --headless false」「arco-cascader-view」「lumen-ui-topic」，以及本条 catalog_path 的真实路径（不能留下方括号）。缺一不派。一条只能有一个 FUNC 号。

【进度】每次新派前只输出一行：完成/执行/待派/22。完成=这 22 条里的 pass+blocked。执行=这 22 条里的 running。待派=这 22 条里仍为 pending 的条数。22 固定。输出后立刻派，不要写段小结。
【循环】待派>0 就继续。交卷唤醒后重复。最后一个动作必须是派子 agent。
【强度】ponytail full

开干：确认没有别的父控 → 无头 Playwright → login-ok → 删掉残留 .env-down → 深圳缺种子就写一次 → 输出进度行 → 按 rewrite-wave-child.md 原文补满 3 路。
