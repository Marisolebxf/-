# 242 政策解读报告 · 生成逻辑（草稿）

- 日期：2026-11-14
- 读者：`human:淮政玮` 确认前有效
- 范围：只描述已落地的生成。确认前不写代码、不改菜单、不改 task-registry
- 对照：`2026-11-14-POL-报告缓存架构.md` 242 行；`sdd/l2/POL-L2-DS12-SIM-ARCH.md` §5.5；`lumen-algo-py` `polan/sim_interpret_job.py` 的 `run_sim_interpret`；`polan/job.py` 分支 `policy_sim_interpret`
- 已拍板：lumen 解读页不改展现。中台只补菜单「政策解读报告」，用这一套生成，先写 demo 库。失败不删旧段落。Java 不写正文、不调模型。前端不直连 Python

## 1. 现状（按代码）

242 已在 lumen 落地，类是正文缓存：有行只读，无行才生成写回，有行要重生必须 `force=true`。205 对齐它，本叶不重做。

| 环节 | 代码里实际在做的事 |
|---|---|
| 读 | 展示 `POST /display/v1/policy/simulation/jobs`，`kind=解读报告`。element 只读 `gkxlumenx_gapfill.gapfill_policy_sim_result`，`row_kind=解读段落`，按政策背景、主要内容、预期效果、实施建议排序。换政策只读，不自动建任务 |
| 生成 | 展示 `POST /display/v1/policy/evaluation/jobs`，`sub_type=policy_sim_interpret`。display 只转发 topic-async → `/internal/policy/jobs/execute` → `run_sim_interpret`。Java 白名单已有该键，不写段落、不调模型 |
| 写回 | 库名写死 `gkxlumenx_gapfill`（不跟 DWD/ADS 的 demo/lumen 平面走）。`is_mock=1`，`fill_method=llm`，`gap_item=242 政策解读报告生成`，`metric_id` 空。至少一段非空才写 |
| 删除 | 只删这一条政策的 `row_kind=解读段落`，再插入，在同一次提交里落地。零段、无密钥、政策不存在、标题摘要正文都空：不进入写入。没有整表 DELETE |
| 中台 | `demo-ui-system-test` 政策子菜单没有「政策解读报告」。`demo-svc-platform`、`demo-algo-science` 没有 `policy_sim_interpret` |

下载不在这条生成里。lumen 页勾选章节后走 `situation/report`（`reportType=policy-interpret-report`），无行不产文件。

和「先写 demo 库」不一致的地方：现函数永远写 `gkxlumenx_gapfill`。DWD/ADS 默认可落到 `demo_gkxlumenx_*`，gapfill 库名不切。demo 账号此前没有 `demo_gkxlumenx_gapfill` 授权。详见 §5。

## 2. 生成逻辑（与现网一致的那一套）

中台菜单和以后迁 lumen，都用下面这一条，不另写函数。

1. 入参要有 `policy_id`。缺了直接结束，`generated=0`。
2. 数该政策已有解读段落。有行且 `force` 不是真：返回已有段数，`skipped=true`，不调模型、不写库。字符串 `false` / `0` / `no` / 空当未强制。
3. 读 DWD `policy_base_info` 的标题、摘要、正文（各截断）。没有这行，或三者都空：结束，不写。
4. 有则拼上 `ads.policy_text_parse`，以及同表「影响范围」「路径环节」摘要。没有也不挡生成。
5. 无模型密钥：`degraded=true`，`generated=0`，不造假段，不删旧段。
6. 有密钥则要四段 JSON：政策背景、主要内容、预期效果、实施建议。空段丢掉，单段最多 2000 字。一段都没有：不写、不删。
7. 至少一段：删该政策旧的解读段落并插入新段（`is_mock=1`，`fill_method=llm`），一次提交。插入没成功则这次删除也不留下。
8. 读面再查 `kind=解读报告`。页面看到的是表里的段，不是模型原文直出。

## 3. 中台菜单看见什么

只加一个菜单，名字「政策解读报告」。页上是操作台，不是展示系统那张解读页。

- 选一条政策（`policy_id`）。
- 没有解读段落：主按钮「生成」。有段落：四段正文照表展示，主按钮「重新生成」（请求带 `force=true`）。
- 四段标题固定：政策背景、主要内容、预期效果、实施建议。
- 进行中显示正在生成。失败或无密钥：若表里还有旧段，旧段仍在；没有旧段则空态，不出现编造正文。
- 不放章节勾选、Word、PDF。下载留在 lumen 解读页。

菜单请求走 Java 转发到已有 `policy_sim_interpret`，不直连 Python，不在 Java 里写正文。写哪一个库见 §5 第 1 项。

## 4. 迁 lumen 时页面怎么保持

不改 lumen 解读页。该页已经接好：打开只读 `simulation/jobs`（`kind=解读报告`）；无行「生成解读报告」、有行「重新生成」走 `evaluation/jobs`（`sub_type=policy_sim_interpret`，重生带 `force=true`）。版式、按钮、章节勾选、Word/PDF 都保持。

迁的时候不新开任务键，不把中台页套进展示页。展示继续读 `gkxlumenx_gapfill` 的解读段落。中台在 demo 库试写，与这张 lumen 表分开，避免试写盖掉展示上已有段落。

## 5. 待确认

1. **写库（推荐）**。中台用同一个 `run_sim_interpret`，写回改到 demo 已授权的库，表仍是 `gapfill_policy_sim_result`，`row_kind=解读段落`，字段与现网相同（`is_mock=1`，`fill_method=llm`）。demo 没有独立 gapfill 库授权时，沿用已有先例落 `demo_gkxlumenx_ads`，不新建库。lumen 解读页继续只读 `gkxlumenx_gapfill`。另一选项：中台也写 `gkxlumenx_gapfill`，和「先写 demo 库」不一致，不推荐。
2. **中台怎么调到这条任务（推荐：demo 菜单 → demo Java 只转发 → 现有 `policy_sim_interpret`）**。Java 不写正文、不调模型；页面不直连 Python。demo 三仓现在都没有这个键，确认前不加菜单、不复制一份生成函数。另一选项：菜单直接打 lumen 的 `evaluation/jobs`，写入会落 `gkxlumenx_gapfill`，和「先写 demo 库」不一致，不推荐。
3. **中台页不带下载（推荐）**。中台只看四段和生成 / 重新生成。Word、PDF、章节勾选留在现有 lumen 解读页。另一选项：中台菜单同时做导出。不推荐，导出不是这条生成。
