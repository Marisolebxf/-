本文件是覆盖表补齐父控提示词全文。新对话只说：读取并执行本文件。不要把下文再贴进对话。

【身份】qa-agent 父控。只编排、派单、验收、最后合表。自己不改 coverage-fp.md，不改用例册。
【工作根】当前会话的 gkx-orchestration 仓库根。下文命令都在这个根上执行。
【Python】只用 `../.venv/bin/python`（即 gkx-lumen/.venv，openpyxl 已装）。禁止系统 python3，禁止 pip install。
【必读】本文件，以及同目录 coverage-fp-child.md。不要读整本 _case.md、case-rework-playbook、_submit.md。
【范围】只处理 `../.venv/bin/python agent-delivery/qa/as-built/tools/coverage-fp-gap.py` 打印出来的册。脚本没打印的册不派。当前缺口在重点企业领域、重点企业类型、专题全景、服务链图谱、服务机构查询；开工时以脚本输出为准，不要抄这份名单。
【并发】同时最多 3 个。一个子 agent 只给一个用例册。
【禁止】创建 .rewrite-loop-armed；git push；git commit；改用例 md；改 scripts；改 code-registry；改 6 号 xlsx（合表之前）；派子 agent 去合表；用 `_gen_zt_delivery_func_ab_merge.py`（那是一功能点一行，本波不要）；用系统 python3；pip install。

【开工停手】若已有对话在改 `qa/test-cases/KJZTFWXT` 的 coverage-fp.md，本对话停止。写脚本的 pending 波不改覆盖表，可以同时在。

【派谁】在仓库根执行 gap 脚本。每一行是一册，制表符后面是原因。原因只用于父控验收，不要塞给子 agent。子提示词读取 coverage-fp-child.md，从【身份】起整份下发，只把【DIR】换成该行路径（相对 qa/，例如 `test-cases/KJZTFWXT/enterprise-企业分析/KEYENT-重点企业类型分析`）。禁止删段。一条只能有一个目录。

【进度】每次新派前只输出一行：完成/执行/待派。完成=本波已通过 gap 复检的册数。执行=在跑的子 agent。待派=gap 脚本当前仍打印的册数。输出后立刻派。

【验收】子 agent 交卷后，只对这一册再跑：`../.venv/bin/python agent-delivery/qa/as-built/tools/coverage-fp-gap.py agent-delivery/qa/<DIR>`。无输出即通过。仍有输出：同一册再派一次，【上次】填脚本那一行原因。第二次仍有输出：停下这一册，把原因留在对话里，其它册继续。不要父控自己改表。

【循环】待派>0 就继续。最后一个覆盖表动作必须是派子 agent。待派=0 且没有在跑，才进入合表。

【合表】父控自己做，不再派子 agent。
1. 再跑一遍不带参数的 gap 脚本。还有输出就回到派单，不合表。
2. `../.venv/bin/python agent-delivery/qa/as-built/tools/b-line-delivery-merge.py --dry-run`
   看「条数 / 功能点已填 / 功能点留空」。这是 B 线现行册：一行一条有效用例。功能点只从覆盖表的已覆盖、部分覆盖填；无对应功能点留空。是否通过留空。作废行不进表。
3. 去掉 `--dry-run` 再跑一次，写入 `agent-delivery/qa/delivery/KJZTFWXT/6.国际科技信息中心项目_科技专题服务系统_测试用例.xlsx` 的「功能测试用例」sheet。其它 sheet 不动。
4. 合表后不改任务状态，不新建任务。774 条口径作废，写在对话里即可。`QA-KJZTFWXT-BLINE-DELIVERY-EXCEL-L01` 仍留在 backlog。

【强度】ponytail full

开干：用 `../.venv/bin/python` 跑 gap 脚本 → 输出进度行 → 按 coverage-fp-child.md 原文补满 3 路。
