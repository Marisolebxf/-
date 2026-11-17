# POL-L2-PC3-PC4-FE-L01 · 多维对比与研报改读对比行

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时已是 in_progress。本叶不重新认领，不改 task-registry。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 接在已有对比页和隐藏研报路由上。浏览器只打 `/display/v1/policy/compare/runs`。关 mock 不回退种子表、种子图、种子研报。未把「智能研报生成」加回侧栏。 |

## 修改内容

- 点「运行对比」改为 `POST /display/v1/policy/compare/runs`。有行才画对比表、四类识别、柱状图、雷达图、知识图谱、摘要、结论。失败或没有行时清空这些块，空态为「这次对比没有写出来，可稍后重试」。某一维原文是「这次对比没有识别出…」或「这次对比还没有这张图」时按字显示。
- 分析对比记录改读 `GET /display/v1/policy/compare/runs`。已完成可查看过程、查看结果、查看报告。进行中时后两个不可点。`USE_MOCK=true` 仍用本机会话记录。
- 「查看报告」打开已有隐藏路由 `policy-insight-report`，正文只读该行研报：深度四块、四类洞察、章节、双向溯源。没有行时写「还没有这次对比的研报」。
- PDF 与 Word 用同一套章节，带该行分析正文和雷达、柱状、知识图谱。正文去掉「演示」「mock」。没有行时导出按钮不可点。
- 停在研报页时侧栏仍高亮「多维政策对比」。未改菜单，未把智能研报生成加回侧栏。

## 测试结果

- `.\node_modules\.bin\vue-tsc.cmd --build --pretty false`：退出码 0。
- `node src/views/policy/compare/compareRun.test.mjs`：通过。
- `node src/views/policy/compare/FE-POL-06A.test.mjs`：通过。
- 未跑整包生产构建。

## 遗留风险

- 新的对比条件若当天还没有完成行，POST 会等算法写行，前端超时放到 200 秒。写不出来就只留空态。
- 关 mock 后，演示轨的种子表、种子图、种子研报不再出现。`USE_MOCK=true` 仍走原来的会话演示。

## CI/CD（必填）

- 分支：`origin/dev`
- 未改 Nacos，未改 Java，未改 Python，未改 task-registry
- 完工即推。流水线由 push 触发。

## 涉及文件

- `repos/lumen-ui-science-pc/src/api/policy.ts`
- `repos/lumen-ui-science-pc/src/views/policy/compare/index.vue`
- `repos/lumen-ui-science-pc/src/views/policy/compare/PolicyCompareWorkbench.vue`
- `repos/lumen-ui-science-pc/src/views/policy/compare/compareRecords.ts`
- `repos/lumen-ui-science-pc/src/views/policy/compare/compareRun.ts`
- `repos/lumen-ui-science-pc/src/views/policy/compare/compareRun.test.mjs`
- `repos/lumen-ui-science-pc/src/views/policy/compare/FE-POL-06A.test.mjs`
- `repos/lumen-ui-science-pc/src/views/policy/insight-report/index.vue`
