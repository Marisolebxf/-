【本波先重跑】本条 yaml 已经有了。先无头重跑这一份，不要先改它。绿了就停。只有页面已经打开、断言仍红，才执行后面的 rewrite-wave-child.md。

1. 不改 yaml，不读 repos/lumen-ui-topic，不打开用例册。试跑命令用后面【试跑】那一条，run-dir 写成 agent-delivery/qa/as-built/runs/rewrite-FUNC-五位-404。日志必须出现 headless=true。禁止 --headless false。
2. 试跑绿：status=pass，note=30892 重跑绿。落表后停。不要执行 rewrite-wave-child.md 的【怎么做】。
3. 整站连不上、5xx 或登录失败：写 agent-delivery/qa/as-built/.env-down（一行原因），本条 blocked，不改 yaml，停。
4. 只有本条入口打不开，或失败文字仍是 SPA 404 / 页面不存在：blocked，note 必须写成 ENV-30892-ENTRY-404。禁止再写 ENV-EDU。不改 yaml。不要执行后面的改写。
5. 页面已经打开，但断言红：从这里起执行后面 rewrite-wave-child.md。按那里的【页面源码】【怎么做】【断言】【禁止】改脚本再试。试跑仍最多两次，禁止第 3 次。收场 note 里不要出现 ENV-EDU。
