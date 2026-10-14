# prompts-used（QA-RUNNER-CALIBRATION-L01 摘录）

- 命令行：`node run-scripts.mjs <功能目录> [--run-dir] [--only] [--headless false] [--baseline] [--check]`
- 读 gold.yaml + scripts.yaml（includes 展开，同 id 去重金样在前）+ fixtures/testdata.yaml
- Playwright chromium 1920×1080@1；headless 默认 true；context acceptDownloads
- 登录：跳 /login 才填 fixtures.login，已在业务页跳过
- action 枚举：goto/login_if_needed/click/fill/press/wait/snapshot/screenshot/assert_visible/assert_url/assert_absent/evaluate/select_option/reload/network_assert
- resolveTarget 启发式（heading/button/textbox/switch/语义区块），失败重试 ≤2 次后降级 getByText，仍失败记 fail 原因继续
- 每步截图（X6）：screenshots/{02d}-{slug}.png
- expect 双层：{note,assert} 于 {page,expect} 求值；{note,manual:true}→pending_manual；裸字符串按「」词转译可见性，转译不了 warning 不判 fail
- allow_skip → n/a；判定 pass/fail/blocked(C6)；跑完自动产出 COMPARISON.md 对照基准 20261014-50892-keytype-r2
