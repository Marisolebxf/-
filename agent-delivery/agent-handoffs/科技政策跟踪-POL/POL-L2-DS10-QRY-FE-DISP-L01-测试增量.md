# POL-L2-DS10-QRY-FE-DISP-L01 · 测试增量交接

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮`（沿用接线单认领，本轮未 task-claim、未改状态） |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`。开工时已是 `in_progress`，测试轮不改 registry |
| 说明 | 本会话只做测试（交付一仓内合规测试 + 交付二验收用例文档），不修代码、不标 done |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 合规测试沿用仓内既有 node 直跑 .mjs 自检风格（FE-POL-01A/01B 的 assert + 源码静态断言写法），fixture 全内联，未引测试框架、未加依赖、未改 pnpm-lock。验收用例文档只写一份，不重复 handoff 内容 |

## 交付

### 交付一：仓内单元测试

新增 `lumen-ui-science-pc/src/views/policy/panorama/search/displayPanoramaQuery.compliance.test.mjs`（272 行），11 组用例逐条标注 DoD 编号：

1. `buildPanoramaSearchQuery`：关键词/类型/地域/级别/部门中文映射进查询参数；高级 NOT 条件不产生独立参数、值不泄进任何参数（DoD-1）
2. `mapSearchItem`/`mapCatalog`：目录行映射卡片；源带 `smartScore` 时卡片不出现该键；空响应（items/records/null）保持空列表（DoD-2）
3. `rankFactorOf`：relevance/timeliness/importance 三值映射；default/发布时间（代码与中文）返回 null（DoD-1）
4. `applyRankOrder`：有名次按 policy_id 重排；honesty.empty / 名次空数组时返回「该排序暂无名次」且条数不变；缺 policy_id 行沉底不炸（DoD-2）
5. `historyBody`：剥离 user_id/userId/items/smartScore/format/channel；多值数组保留、单值收成标量（源码语义）（DoD-1）
6. `historyViews`/`favoriteViews`：匿名 honesty（unavailable:anonymous）返回空行+anonymous 标记；正常行解析历史芯片与去重收藏 id（DoD-2）
7. `docItem`：匿名 honesty 返回 null 不造假详情（DoD-2）
8. `presentShare`：share_url+note 透出；mail unavailable 给出「邮件不可用，不发送邮件」；匿名给「请先登录」；返回值无「已下载/已在本页下载」表述（DoD-2）
9. `allowsLocalFileExport(false)===false`；`displaySearchResultUtils.ts` 存在 `assertLocalDemo` 守卫且导出函数调用守卫，守卫文案「USE_MOCK=false 不在浏览器生成导出文件」（DoD-2）
10. `shareRequestQuery`：format=excel|pdf 与 channel=link 拼装正确，user_id 剥离（DoD-1）
11. 静态合规断言：`index.vue`/`policy.ts` 不含 `/policy/topic/v1` 与 `/topic/v1/policy`；ShareModal 的 example.com 仅出现在 live=false 三元假支；`handleExport` 内 exportPolicies 调用点被 `allowsLocalFileExport(USE_MOCK)` 包裹；`seedInboxItems` 与 `matchPoliciesToSubscription` 仍在（DoD-3）

### 交付二：验收用例文档

`agent-delivery/工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS10-QRY-FE-DISP-L01-验收用例.md`：A 目录与详情（4 条）/ B 智能排序（2 条）/ C 历史与收藏（4 条）/ D 导出分享（3 条）/ E Mock 回退与四页签（2 条），每组含前置、输入、步骤（菜单路径「科创政策全景→政策检索」、按钮真实文案抄自源码）、预期、截图要求（Network panorama 过滤、X-Trace-Id、Local Storage 键 `gkx-policy-display-favorites:v1`）。已标注 C 组与 B1 需先 rollout gkxlumen-display（含 70abaa79），当前线上旧进程 404（trace bde5d782e0f1e2b3555c8102b9514ce1）期间执行为前端诚实失败不算用例失败。

## 测试结果（命令与退出码）

| 命令 | 退出码 | 结果 |
|------|--------|------|
| `node src/views/policy/panorama/search/displayPanoramaQuery.compliance.test.mjs`（新增） | 0 | 全绿 |
| `node src/views/policy/panorama/search/displayPanoramaQuery.selfcheck.mjs` | 0 | ok |
| `node src/views/policy/panorama/FE-POL-01A.test.mjs` | 0 | 全绿 |
| `node src/views/policy/panorama/FE-POL-01B.test.mjs` | 0 | 全绿 |
| `pnpm exec vue-tsc --build` | 0 | 无类型错误 |

未执行 `pnpm install`（任务禁令）。

## 发现的问题

本轮未发现前端缺陷。部署时序风险（非 bug）：`gkxlumen-display` 未 rollout 含 70abaa79 的版本前，线上 `/display/v1/policy/panorama/**` 404（trace `bde5d782e0f1e2b3555c8102b9514ce1`），C 组/B1 及 A/D 组真连验证须等 rollout 后执行。

## 截图情况

仓内无 playwright/puppeteer 依赖且禁止 install/加依赖，未自动截图；验收用例文档内 E1/E2 预留【Mock 模式截图：xxx】标注位并写明未截原因；A–D 组截图要求 rollout 后人工截取，禁止 Mock 冒充。

## CI/CD

| 仓 | commit | push |
|----|--------|------|
| lumen-ui-science-pc | `57b6339` `test(policy): 展示政策检索 DoD 合规验收测试 [agent:frontend-agent]` | 已推 `origin/dev`（b35f87a..57b6339） |
| gkx-orchestration（本文档 + 验收用例，经临时 worktree 提交） | 见本 commit | 推 `origin/dev` |

主工作区有他人未提交的 `task-registry.yaml`，按多会话保护规则未触碰，文档提交在临时 worktree `worktrees/orch--pol-l2-ds10-accept`（基于 origin/dev 8788e241）完成，用后 remove。

## 架构合规自检

- 调用链：测试断言 `USE_MOCK=false` 只打 `/display/v1/policy/panorama`，静态断言无 `/policy/topic/v1`、`/topic/v1/policy` ✅
- D9：未新造 metric_id，未改 D4 ✅
- D12：展示前端只经已有网关前缀 ✅
- 可观测：沿用 `X-Trace-Id`，验收用例把响应头 Trace-Id 列为截图要求 ✅
- 未改动向/舆情/比对/订阅数据源（静态断言 seedInboxItems/订阅引擎在场）✅
- 未跑浏览器操作（rollout 未完成 + 无自动化工具），界面层验证留给验收用例人工执行——本轮诚实记录为未覆盖面
