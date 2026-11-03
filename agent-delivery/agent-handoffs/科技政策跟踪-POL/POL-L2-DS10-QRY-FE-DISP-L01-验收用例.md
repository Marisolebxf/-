# POL-L2-DS10-QRY-FE-DISP-L01 · 人工验收用例集

> 页面：展示系统 `/display/policy/panorama`（科创政策全景 → 政策检索页签）
> 代码基线：`lumen-ui-science-pc` `origin/dev` `57b6339`（b35f87a + 合规测试）
> 监管人：human:淮政玮 · 编写：frontend-agent · 2026-11-03
> 本文档为交付二，供人工照做验收。截图要求中的键名、菜单路径、按钮文案均抄自源码（`index.vue` / `displayPanoramaQuery.ts`），未编造。

## 全局前置条件

| 项 | 值 |
|----|----|
| 构建开关 | `VITE_APP_USE_MOCK = false`（除 E 组外全部用例；E 组单独切换 true） |
| 后端 | 网关 `gkxlumen-display` 已 rollout **含 70abaa79** 的版本。**当前线上还是旧进程，`/display/v1/policy/panorama/**` 会 404**（证据 trace：`bde5d782e0f1e2b3555c8102b9514ce1`） |
| 登录态 | C 组与 B1 需要已登录（带 token）；其余组可匿名 |
| 菜单路径 | 展示系统左侧导航 → **科创政策全景** → 页签 **政策检索**（页签名源码 `SUB_TABS = [{ key: 'search', label: '政策检索' }...]`） |
| DevTools 常用 | Network 面板过滤词 `panorama`；响应头 `X-Trace-Id`；Application → Local Storage 键 `gkx-policy-display-favorites:v1` |

## ⚠️ rollout 前的预期表现（重要）

**C 组与 B1 必须在 rollout 之后执行。** rollout 前执行 C 组（保存历史 / 点历史重查 / 收藏）预期看到提示「收藏失败」「再次检索失败」+ Network 中对应请求 404——这是**前端诚实失败，不算用例失败**；记录 404 的 trace 后跳过等 rollout 再验。A/D 组的 404 同理：看到「政策查询失败」提示且列表保持空即为诚实失败，不算用例失败，但需在 rollout 后复验。

---

## A 组 · 目录与详情（DoD-1、DoD-2）

### A1 关键词检索

| 项 | 内容 |
|----|------|
| 前置 | 已登录或匿名；后端已 rollout |
| 输入 | 检索框输入 `人工智能`，点搜索按钮（SearchHub 模式「关键词搜索」） |
| 步骤 | 1. 输入关键词 2. 点搜索 3. 打开 DevTools → Network，过滤 `panorama` |
| 预期 | ① Network 出现 `GET /display/v1/policy/panorama/search?...keyword=人工智能...`（query 同时含 `keyword` 与 `q`）② 随后自动发 `POST /display/v1/policy/panorama/favorites/history`（体里无 `user_id`）③ 目录卡片正常渲染 ④ 检索条件条（政策来源/类别/行业/部门/地区/级别）在下拉变化后 80ms 内触发新一发 search |
| 截图 | ①Network 列表（panorama 过滤，含 search + favorites/history 两条）②任一 search 响应头 `X-Trace-Id` |

### A2 空结果不回退种子（DoD-2 核心）

| 项 | 内容 |
|----|------|
| 前置 | 同 A1 |
| 输入 | 输入一个必然无结果的词，如 `zzqqxx无此政策` |
| 步骤 | 点搜索，等待响应 |
| 预期 | ① 列表区显示空态（`a-empty` 文案「无检索结果，不可排序 / 二次筛选 / 按类别分组 / 分享」）② **不得**出现 demo 种子政策（如「深圳AI新政」「专精特新」等种子名单标题）③ 统计卡「当前命中」= 0 |
| 截图 | ①空态整页截图 ②Network 中 search 响应 JSON（items: []）+ `X-Trace-Id` |

### A3 详情抽屉

| 项 | 内容 |
|----|------|
| 前置 | A1 已有命中结果 |
| 步骤 | 1. 点任一结果行「查看」按钮 2. 观察右侧抽屉 |
| 预期 | ① 发 `GET /display/v1/policy/panorama/{policy_id}/detail` ② 抽屉从右侧滑出（Teleport 到 body）③ 后端无正文时抽屉内容为空，**不出现种子全文**；提示「没有政策正文」 |
| 截图 | ①抽屉打开态 ②detail 请求的 Network 条目 + `X-Trace-Id` |

### A4 二次筛选

| 项 | 内容 |
|----|------|
| 前置 | A1 已有命中结果 |
| 步骤 | 1. 结果卡「检索结果筛选与分类」条中，政策类型下拉选一个值 2. 观察提示行 |
| 预期 | ① 触发新一发 `search`，query 带 `policy_type` ② 提示行显示「主检索命中 X 项 · 二次筛选后 Y 项」③ 类型/地域二次筛走服务端；发布时间起止仍在前端按字符串收窄 ④ 点「清空二次筛选」恢复 |
| 截图 | ①二次筛选后的提示行 + Network 新 search 请求 |

---

## B 组 · 智能排序（DoD-1、DoD-2）

### B1 三因子排序（需 rollout 后验）

| 项 | 内容 |
|----|------|
| 前置 | A1 已有命中结果；已登录 |
| 步骤 | 1. 结果卡右上「检索结果智能排序」下拉，依次选「相关性」「时效性」「重要性」 2. 观察列表顺序与 Network |
| 预期 | ① 每次选择发 `GET /display/v1/policy/panorama/rank?...factor=relevance|timeliness|importance`（query 含当次检索条件）② 列表按返回 `policy_id` 名次重排 ③ **卡片上不出现 smartScore 字样** ④ 下拉只有「默认/相关性/时效性/重要性」四项，**没有**「发布时间/效力级别/浏览量」 |
| 截图 | ①下拉展开态（四选项）②rank 请求 + 响应（items 数组）+ `X-Trace-Id` ③重排后列表首屏 |

### B2 空名次不清目录（DoD-2 核心）

| 项 | 内容 |
|----|------|
| 前置 | A1 已有命中结果（rollout 前后都可验：rank 404 时同样触发兜底） |
| 步骤 | 1. 选「相关性」排序 2. 若后端返回空名次（`items: []` 或 `honesty.empty: true`）或请求 404 失败 |
| 预期 | ① 目录条数不变、不空白 ② 出现提示「该排序暂无名次」（404 时为「排序失败，已保留当前目录」）③ 切回「默认」恢复当次 search 顺序 |
| 截图 | ①提示「该排序暂无名次」在场 + 列表仍在的整页截图 |

---

## C 组 · 历史与收藏（⚠️ 需 rollout 含 70abaa79 后执行）

> **rollout 前执行本组预期看到「收藏失败」「再次检索失败」+ 404（trace bde5d782e0f1e2b3555c8102b9514ce1 为证），算前端诚实失败，不算用例失败。**

### C1 保存历史无 user_id

| 项 | 内容 |
|----|------|
| 前置 | 已登录；rollout 后 |
| 步骤 | A1 检索一次后，看 Network 中 `POST /display/v1/policy/panorama/favorites/history` 的请求体 |
| 预期 | ① 请求体只含检索条件（keyword/q/level/region/policy_type 等），**无 `user_id`/`userId`/`items`/`smartScore`/`format`/`channel`** ② 单值数组收成标量（如 `region:"深圳"`），多值保持数组 |
| 截图 | ①请求体 Payload 视图 ②响应 `X-Trace-Id` |

### C2 点历史重查

| 项 | 内容 |
|----|------|
| 前置 | C1 已保存过历史 |
| 步骤 | 1. 刷新页面 2. 检索历史区出现历史芯片（格式「人工智能 · 国家级」）3. 点击芯片 |
| 预期 | ① 发 `POST /display/v1/policy/panorama/favorites/history/{id}/search` ② 用返回目录**替换**当前结果（不是前端本机过滤）③ 排序下拉回到「默认」 |
| 截图 | ①历史芯片在场 ②replay 请求 + 响应 + `X-Trace-Id` |

### C3 收藏走服务端

| 项 | 内容 |
|----|------|
| 前置 | 已登录；rollout 后 |
| 步骤 | 1. 结果行点「收藏」按钮（空心→实心红心）2. 打开顶部统计卡「收藏政策」抽屉 3. 匿名场景（未登录）重复点收藏 |
| 预期 | ① 发 `POST /display/v1/policy/panorama/favorites`（体 `{policy_id}`），成功提示「已收藏」，收藏数 +1 ② 收藏抽屉列表来自服务端 favorites；再点「取消收藏」提示「收藏以服务端记录为准，本页不能在本地取消」③ 匿名时提示「请先登录」，**不写本地** ④ Application → Local Storage：`USE_MOCK=false` 时**不出现** `gkx-policy-display-favorites:v1` 新写入（该键只在 Mock 态使用） |
| 截图 | ①收藏请求 + 响应 ②收藏抽屉列表 ③Local Storage 键视图（证明无本地回退） |

### C4 匿名空列表 + 请先登录

| 项 | 内容 |
|----|------|
| 前置 | 未登录（匿名）；rollout 后 |
| 步骤 | 1. 匿名发起检索 2. 观察检索历史区 3. 匿名点收藏 4. 匿名打开收藏抽屉 |
| 预期 | ① favorites 接口返回 `honesty` 含 `unavailable:anonymous` 时，历史区显示「请先登录」，收藏数为 0 ② 收藏抽屉空态描述「请先登录」③ **不出现**任何种子收藏或伪造历史芯片 |
| 截图 | ①历史区「请先登录」提示 ②收藏抽屉空态 |

---

## D 组 · 导出分享（DoD-1、DoD-2）

### D1 只走 share

| 项 | 内容 |
|----|------|
| 前置 | A1 已有命中结果 |
| 步骤 | 1. 点「导出」下拉 → 「导出 Excel」/「导出 PDF」 2. 点「分享」按钮 |
| 预期 | ① `USE_MOCK=false` 时导出**不弹打印窗、不下载本地 xlsx**，而是发 `GET /display/v1/policy/panorama/share?...format=excel|pdf&channel=link...` ② 分享弹窗标题「分享检索结果」，链接框只显示服务端返回的 `share_url`（不是 `example.com` 演示地址）③ 提示含「响应没有文件字节，未在本页下载」类说明，**无「已下载」字样** |
| 截图 | ①share 请求 + 响应 JSON（share_url/honesty）+ `X-Trace-Id` ②分享弹窗链接态 |

### D2 空目录不生成文件

| 项 | 内容 |
|----|------|
| 前置 | A2 空结果状态 |
| 步骤 | 点「分享」（按钮禁用则先看禁用态；高级检索模式下按钮可点） |
| 预期 | ① 提示「目录为空，未生成文件」 ② Network 无 share 请求 ③ **浏览器无任何文件下载** |
| 截图 | ①提示「目录为空，未生成文件」 ②Network 面板（无新请求） |

### D3 邮件不可用说明

| 项 | 内容 |
|----|------|
| 前置 | A1 已有命中结果 |
| 步骤 | 分享弹窗切「邮件分享」，输入邮箱，点「发送」 |
| 预期 | ① `USE_MOCK=false` 时不真发邮件；服务端 honesty 含 `unavailable` 时提示「邮件不可用，不发送邮件」② 匿名时提示「请先登录」 |
| 截图 | ①「邮件不可用，不发送邮件」提示在场 |

---

## E 组 · Mock 回退与其他四页签数据源未动（DoD-3）

### E1 Mock 本机检索可用

| 项 | 内容 |
|----|------|
| 前置 | `VITE_APP_USE_MOCK = true` 启动 dev server |
| 步骤 | 1. 智能模式输入「深圳近三年市级人工智能扶持政策」解析出维度芯片 2. 关键词模式普通检索 3. 高级检索添加条件（含 NOT）应用 4. 点导出 Excel |
| 预期 | ① 智能解析出「市级/深圳/人工智能」芯片，命中本机种子结果 ② 关键词/高级检索走本机 queryEngine（Network 无 panorama search）③ 导出真的生成 xlsx 文件（本机演示态）④ 分享链接是 `example.com/share/...` 演示地址 |
| 截图 | ①【Mock 模式截图：智能解析芯片 + 命中列表】②【Mock 模式截图：导出成功提示】 |

### E2 四页签数据源未动

| 项 | 内容 |
|----|------|
| 前置 | 任一开关态均可 |
| 步骤 | 依次切「政策动向跟踪」「政策舆情评估」「政策重点比对」页签，打开「我的订阅 / 推送收件箱」抽屉 |
| 预期 | ① 三页签内容与本单改动前一致（数据仍来自本机种子/mock 模块）② 订阅收件箱首启出现两条种子推送（「【每周推送】科创政策周报 · 命中 3 项最新动态」等——`seedInboxItems` 未改）③ Network 中无新增 `/display/v1/policy/panorama` 请求来自这些页签 |
| 截图 | ①任一页签整页 ②收件箱两条种子在场 |

---

## 截图情况说明

- 本轮检查 `package.json`：**无 playwright / puppeteer 等浏览器自动化依赖**，且任务约束禁止 `pnpm install`、禁止加新依赖，故未做自动截图。
- E1/E2 中的「【Mock 模式截图：xxx】」为预留截图位：后续如需补图，以 `VITE_APP_USE_MOCK = true` 启动 `pnpm dev`（端口 3000）后人工截取，并在图注标明「Mock 模式截图」。
- **禁止**拿 Mock 截图冒充 `USE_MOCK=false` 证据；A–D 组全部截图必须在 rollout 后的真连环境截取。

## 发现的问题

（本轮测试未发现前端缺陷；rollout 未完成导致的 404 属部署时序，不算 bug，见顶部说明。若验收中新发现现象，按「现象 / 复现步骤 / 根因初判 / 涉及文件 / 证据 trace」格式登记到《测试增量》文档并回报协调人。）
