# POL-L2-DS10-SUB-FE-L01 · 科创政策全景 · 政策订阅前端接线真实接口

- 任务：`POL-L2-DS10-SUB-FE-L01`
- 日期：2026-11-03
- 监管：`human:淮政玮`（已授权完工即推）
- 认领：`agent:frontend-agent`
- 强度：ponytail full
- 代码仓：`lumen-ui-science-pc` @ `origin/dev` commit **f92ea3c**（4 文件，+281/−17）
- 伴单：后端已就绪——`/display/v1/policy/panorama/subscriptions`（GET/POST/PUT {id}/DELETE {id}），库表 `gkxlumenx_topic_policy.policy_subscription`（当前 0 行）

## 1. 交付范围

订阅中心（我的订阅抽屉 + 订阅弹窗 + 动向 Tab 订阅摘要 + 匹配推送入口）从 localStorage 演示态切到真实接口；`USE_MOCK=true` 完整保留 D7 localStorage 演示轨道（种子文件零改动）。改动 4 文件：

| 文件 | 改动 |
|---|---|
| `src/api/policy.ts` | 新增 `panoramaPut`/`panoramaDelete` 封装（对齐既有 `panoramaGet`/`panoramaPost` 的 optional+skipErrorToast）；订阅 4 方法 + 契约类型 `PanoramaSubscriptionItem`/`PanoramaSubscriptionBody`/`PanoramaSubscriptionsResponse` |
| `src/views/policy/panorama/index.vue` | 订阅族双轨改造（详见 §2–§4） |
| `components/SubscribeTab.vue` | 仅文案条件化（USE_MOCK 显示「本地 Mock」、真实态显示「外发通道未上线」）；**props/emits 零改动** |
| `components/SubscribeModal.vue` | 仅成功提示分流（mock 乐观提示 / 真实态 loading 交由提交结果反馈）；**props/emits 零改动** |
| `subscriptionContract.selfcheck.mjs`（新增） | 静态契约自检（§5） |

## 2. CRUD 接线（DoD-1）

| 操作 | mock 轨道（保留） | 真实轨道（USE_MOCK=false） |
|---|---|---|
| 列表 | `readSubscriptions()` localStorage | `GET /display/v1/policy/panorama/subscriptions` → `data.subscriptions[]` |
| 新建 | 写 localStorage + 演示收件箱通知 | `POST /subscriptions` body=契约字段；`item=null` 显式报「服务端未受理」不造假行 |
| 修改 | 写 localStorage | `PUT /subscriptions/{id}`（编辑 id 取自 `subscribeEditing`，在置空前捕获） |
| 取消 | 删 localStorage 行 | `DELETE /subscriptions/{id}` → 响应为取消后有效列表，直接 `refreshSubscriptions()` |

挂载初始化：`USE_MOCK=true` 读 localStorage（含 `seedInboxItems` 假种子保留）；false 时空列表起步 + `refreshSubscriptions()`。

## 3. 字段映射表（DoD-2，以 `PolicySubscriptionService.fieldsOf` 为准）

### 3.1 前端 → 契约（`toSubscriptionBody`）

| 本地字段（SubscriptionRow） | 契约字段 | 转换 |
|---|---|---|
| `categories[]`（policyCategories key） | `policy_type: string[]` | 原样（后端 join 逗号存库） |
| `industries[]` | `industry_code: string[]` | `normalizeSubscriptionIndustries` 归一后传 |
| `departments[]` | `publish_organization: string[]` | 原样 |
| `regions[]` | `province[]` / `city[]` / `region[]` | 按 policySeed.regionOptions 字典归类：national/beijing/shanghai/guangdong/jiangsu/zhejiang → province；shenzhen/overseas → city；其余原样 → region |
| `frequency`（daily/weekly/monthly） | `frequency: 'day'｜'week'｜'month'` | 字典互转；未知值兜底 `week`（后端只收三值，其他整条拒绝） |
| `notifyMethods[]`（inbox/email/sms） | `channels: string[]`（system/email/sms） | `inbox → system`；email/sms 同名 |
| （不传） | `user_id` | **前端不传**（自检断言请求体构造函数无 `user_id`） |

### 3.2 契约 → 前端（`fromSubscriptionItem`，展示）

| 契约字段 | 本地字段 | 转换 |
|---|---|---|
| `policy_type`（逗号串） | `categories[]` | split |
| `industry_code` | `industries[]` | split |
| `publish_organization` | `departments[]` | split |
| `province`+`city`+`region` | `regions[]` | 三串 split 后合并去重（往返一致） |
| `frequency`（day/week/month） | `frequency` | `day→daily` 等，展示层复用 `formatFreqLabel` |
| `channels[]`（system/…） | `notifyMethods[]` | `system→inbox`，展示层复用 `formatNotifyLabel` |
| `id`（数值） | `id`（String 化） | mock 行 id 是字符串，统一 String |
| `last_outbound_at` | `updatedAt` | 展示「更新于」 |
| —（无 name 列） | `name` | 后端表无订阅名列：会话内 `subNameCache`（保存时写入 name→id 映射），未命中回显「订阅方案 #id」。刷新后名称丢失是已知诚实取舍（§7） |

## 4. 诚实态（DoD-3）

- **无订阅**：库 0 行/匿名 → `subscriptions=[]` → 空态文案「暂无订阅，可点击新建订阅按条件创建」（既有 a-empty）
- **收件箱**：真实轨道恒空数组起步（不 seed 假种子、不读 localStorage），空态文案「暂无推送；外发通道未上线，通道接通后按订阅频率推送」；抽屉顶部 `a-alert` 显「外发通道未上线：订阅条件已入库保存；…通道接通前，推送收件箱暂无真实推送记录」（由 `honesty.outbound` 是否 `unavailable:` 前缀驱动 `pushChannelUnavailable`）
- **「立即推送」**：真实轨道不再伪造收件箱记录，`Message.info` 诚实提示 + 打开收件箱空态
- **匹配订阅入口**（`?tab=match` 深链）：真实轨道把匹配条件落库为真实订阅（POST，industry 取画像行业）；「推送」模式只提示通道未上线，不写假收件箱
- **失败隔离**：全部请求 `optional: true` + `skipErrorToast`（沿用 panorama 封装），失败只影响订阅 Tab 自身（列表保持现状），时序/入库/检索等其他数据不动；CRUD 失败用局部 `Message.error` 反馈
- **不把外发写成已上线**：所有真实态文案均为「外发通道未上线/通道接通后」，无「已推送」字样；成功保存提示为「订阅已保存；将按设定频率推送（外发通道上线前仅入库不推送）」

## 5. 工程验证（三绿，DoD-4）

| 项 | 命令 | 结果 |
|---|---|---|
| 类型 | `pnpm type-check`（vue-tsc --build） | ✅ exit 0 |
| 构建 | `pnpm build` | ✅ built in 1m18s（chunk 体积警告为存量） |
| 新自检 | `node src/views/policy/panorama/subscriptionContract.selfcheck.mjs` | ✅ OK |
| 既有自检回归 | `portal.selfcheck.mjs` / `request.mockAuthSession.selfcheck.mjs` / `ssoCallback.selfcheck.mjs` | ✅ 3/3 OK |

自检覆盖：4 端点路径锚点（GET/POST/PUT/DELETE）、字段映射断言（policy_type/industry_code/publish_organization/channels inbox↔system/frequency daily↔day）、请求体无 `user_id`、mock 轨道保留（readSubscriptions/saveSubscriptionMock）、诚实态（pushChannelUnavailable 消费 honesty.outbound、立即推送不伪造、「外发通道未上线」文案存在）。

## 6. USE_MOCK 行为说明（DoD-1）

| 场景 | true（演示轨道，行为与改造前一致） | false（真实轨道） |
|---|---|---|
| 订阅列表/收件箱 | localStorage 读写（含 inbox 种子首次播种） | 服务端拉取 / 恒空收件箱 |
| 新建/修改 | 写 localStorage + 演示收件箱通知 | POST/PUT 真实接口，结果反馈 |
| 取消 | 删本地行 | DELETE 真实接口 + 刷新 |
| 立即推送 | 伪造收件箱推送（演示） | 诚实提示通道未上线 |
| 订阅名称 | localStorage 持久 | 会话内缓存（后端无 name 列） |
| 种子文件 | **零改动**（policySubscriptionSeed.ts / policySeed.ts 未触碰） | 不消费（仅复用其 label/归一纯函数） |

## 7. 遗留风险与说明

- **订阅名称不持久**：后端表无 name 列（契约如此）；刷新后回显「订阅方案 #id」。若需要持久名称，须后端加列（另单），前端映射已就位（`subNameCache` 一行可换成回读字段）
- **匿名用户**：后端 list 对匿名返回空列表（envelope 空 subscriptions），前端表现为空态，符合诚实要求；保存对匿名 `item=null` → 前端显式报「服务端未受理」
- **pushes 恒空**：外发通道上线前收件箱永远空态；`honesty.outbound` 变为 `no_push_history` 时抽屉顶部提示自动消失（`pushChannelUnavailable=false`），但 pushes 渲染仍依赖后端真实下发（当前响应结构已含 `pushes[]`，前端收件箱真实轨道暂只显空态+提示，不做 pushes→InboxItem 渲染——通道上线后补一行映射即可，本次不造）
- **编辑判定**：真实轨道「修改」识别 = `subscribeEditing.value?.id`（服务端行 id）；新建走 POST。模态 emit 的对象不带 `source` 字段，故 id 捕获在 `saveSubscription` 置空 `subscribeEditing` 之前完成

## 8. 架构合规自检

- ✅ 调用链：浏览器只打 `/display/v1/policy/panorama/subscriptions**`（展示服务委托专题门面），无越层、无 `/internal`、无直连 demo
- ✅ D12：未引入任何 `demo-*` 依赖；未 merge demo 代码
- ✅ D8/D10：布局、组件结构、交互不动（SubscribeTab/SubscribeModal props/emits 零改动），仅数据源与文案
- ✅ 未改 Java/后端；未改其他 Tab（时序/舆情/比对代码未触碰）；mock 种子文件内容零改动（只新增真实轨道）
- ✅ 不把外发写成已上线（§4）；不标任务 done
- ✅ commit `[agent:frontend-agent]`；push `origin/dev` 一次成功（`73cc1e8..f92ea3c`），无 force

## 9. 产物清单

- `lumen-ui-science-pc` @ dev：**f92ea3c** — `src/api/policy.ts`、`src/views/policy/panorama/index.vue`、`components/SubscribeTab.vue`、`components/SubscribeModal.vue`、`subscriptionContract.selfcheck.mjs`（新增）
- 本 handoff（gkx-orchestration，仅写文件，未碰该仓 git）

## 10. cost 估算

| 项 | 估算 |
|---|---|
| actual_tokens | ~180k（含读码/契约核对/双轨实现/三绿两轮/自检/handoff） |
| model_used | glm-5.3（Cursor agent） |
| actual_cost | ~$1.2（远低于 $10 告警线） |
| cost_warn | false |

ponytail: full —— 映射函数内联在 index.vue（仅此页消费，无第二处使用，不抽 utils）；自检用仓内既有 `*.selfcheck.mjs` 静态断言先例，零框架；SubscribeTab/SubscribeModal 只动文案不动契约，最小 diff。
