# SITUATION-ENT-D1-L01 · 前端切换 USE_MOCK=false + 契约适配 + 本地联调冒烟

> **任务**：科技全域态势·企业维度跑通 D1 叶（管线收口叶）——`lumen-ui-science-pc` 切真实数据
> **角色**：`agent:frontend-agent` · 监管人：`human:李伟`（长任务授权，授权句已生效）
> **状态**：`backlog → claimed → in_progress → integration`（AV-1 目标态，待人工签收）
> **上位**：[SITUATION-ENT-长任务总控](./SITUATION-ENT-长任务总控.md) · 契约 v1.2 · 倚 C1/C2/C3（均 integration）
> **挂接**：WBS §4.3（WBS-05-18-05） · 2026-10-27

---

## 一、交付内容（git 改动面 = 3 文件，视图零 diff）

| 文件 | 改动 | 说明 |
|---|---|---|
| `.env.development` | `VITE_APP_USE_MOCK=false`；`VITE_APP_API_URL=http://127.0.0.1:7099` | 本地联调指向本机 display（U6）。**注释里写明原值/真网关/回滚方法**；mock 种子保留未删（双轨随时切回） |
| `src/api/situation/index.ts` | ① timeline/events/cluster/compare 四端点改走**独立轻量 axios 实例**（`optional()`）：仅把「未上线」类状态（404/405/501）收敛为**手写诚实空态**，其它错误照常抛出；② 注释补契约 v1.2 指针 | 为什么不直接 `post().catch()`：全局拦截器对任何 4xx 都 `Message.error` 弹窗，违反走查第 5 条「无报错弹窗」；改 `@/utils/request` 属公共基建超范围，故在 api 层内自建实例（**发现 `skipToken` 选项后未改用**——本例问题不在 token 而在错误弹窗，见 §三） |
| `vite.config.ts` | 代理 rewrite 增加「**本地直连时剥 `/display` 服务前缀**」（仅 target 为 127.0.0.1/localhost 时生效） | **本叶最重要的环境发现**，见 §二。生产打网关时代理行为不变（网关自己剥），不会双重剥离 |

**`types/situation.ts` / `mock/modules/situation.ts` 零改动**——后端 C1–C3 已按冻结类型出数（这正是 C 段「契约适配前端」的成果），D1 无需类型映射。

## 二、过程中揪出的关键环境缺陷（本地链路 401 的真凶）

**症状**：页面所有 situation 请求 401「访问令牌不存在」（与真实网关的 401 同文），但 curl 直连 7099 无头也 200。

**根因链**：前端请求 `/api/display/v1/situation/**` → vite 代理只剥 `/api` → 到 display 时路径是 **`/display/v1/situation/**`** → 生产上这段 `/display` 由网关（`GkxlumenRequestGlobalFilter`）剥掉，**本地没有网关** → 带前缀的路径不在 `ignore-urls`（`/v1/situation/**`）里 → 被鉴权拦成 401（先修 ignore-urls 后暴露 404，进一步证实是前缀问题）。

**修法**：在 vite 代理的 rewrite 里模拟网关语义——**仅当代理目标是本机**（无网关）时剥 `/display` 前缀；目标是网关时保持原样。**教训：本地联调链路必须逐段对齐「网关剥前缀」这个隐式契约，401 文案与真网关相同极具迷惑性。**

## 三、冒烟结果（playwright-cli 无头浏览器，2026-10-27 18:5x）

**截图**：[SITUATION-ENT-D1-L01-smoke.png](./SITUATION-ENT-D1-L01-smoke.png)（本目录）

| 检查项 | 结果 |
|---|---|
| mock 登录 → 进入 `/trend/tech-overall-situation` | ✅（ENABLE_MOCK_AUTH=true 时任意账密可登，见 `api/auth.ts`） |
| 页面渲染 | ✅ 地图真实气泡（深圳/广州/东莞…）、11 要素图例、热力分级、企业领域分布折线（人工智能 186,842 与 A0 一致）、KPI「独角兽企业 ⓘ **167 家**」真值 + 血缘角标 |
| 报错弹窗（走查第 5 条） | ✅ **无任何 Message.error 弹窗**；console 仅剩 4 条浏览器网络层 404 日志（timeline/events/cluster/compare，属浏览器固有行为，应用已静默收敛为空态，`console.warn` 有据可查） |
| 白屏 | ✅ 无 |
| `views/situation/**`、`styles/demo-situation.css` diff | ✅ **零改动**（git diff 仅 §一 的 3 文件） |
| 三绿 | ✅ `vue-tsc --build` exit 0；`vite build` **✓ built in 57.91s**（dist 产出）；自检=冒烟脚本 |

**留给人工走查的两个观察项**（非本叶缺陷，走查时确认）：
1. 「实时数据监控」KPI 卡片区文本出现「独角兽企业 167 家」重复 5 次且「暂无趋势数据」——疑似视图对真实 type-dist 的取数/去重逻辑与 mock 形状有出入，属视图层（本叶不可改），需孔东侧确认；
2. 「企业领域分布」近乎单域（人工智能 ~98.7%）——A0 已知数据口径事实，非 bug。

## 四、验证环境搭建记录（复现用）

- 本机服务：element :7082（local，PID 见任务各叶）、display :7099（local）**均在运行**，走查可直接用；
- 前端 dev server：`http://127.0.0.1:3600`（vite，后台进程仍在跑；也可自行 `pnpm dev`）；
- 工具链坑（复现三绿必备）：
  1. 仓内无 node_modules，pnpm 9 安装即可（**必须 `--ignore-workspace`**，否则报「packages field missing or empty」）；
  2. Node 须 ≥20.19（Vite 7）——本机 20.18 会静默失败，用便携 Node 22（`%LOCALAPPDATA%\gkx-node`）；
  3. **`oxc-parser` 的 win32 原生 binding 会被 pnpm 漏装**（optional deps 平台包），需手工补 `@oxc-parser/binding-win32-x64-msvc@0.131.0` 到 `node_modules/@oxc-parser/`；
  4. IDE 注入的 `NODE_OPTIONS`（safe-delete shim）会让 pnpm 卡死，清空该变量再装。

## 五、给验收人的走查前置

1. 直接开 `http://127.0.0.1:3600/trend/tech-overall-situation`（dev server 已起；若停了：`pnpm dev`，注意 Node 版本坑 §四）；
2. 登录用任意账密（mock auth）；
3. 走查清单按总控 §4 执行；期望值以 A0/C1/C3 报告为准（189,115 / Top5 榜单 / 167 独角兽）；
4. **`.env.development` 已切本地**：走查后若要打真网关，改回 `VITE_APP_API_URL=http://10.50.69.111:30895` 并取 PigX token（当前 401 卡点）；
5. 遗留缺口清单：4 个未上线端点（诚实空态已就位）、`timeRange/selectedFieldValues` 未过滤（后端如实声明）、KPI 卡重复现象（走查项 1）。

## 六、Cost 四字段

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈ 260k（估，含依赖安装/构建排障与浏览器冒烟） |
| model_used | auto（CodeBuddy） |
| actual_cost | ≈ $1.9（估） |
| cost_warn | green（<$10） |

ponytail: full（401 真凶追到 vite 代理与网关剥前缀的隐式契约；三绿与浏览器冒烟全部真实执行，未以「应该能跑」替代验证）
