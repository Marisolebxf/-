# SYSINT-03-03A-WIRE-L01 · 专题服务门户内容管理 · 页面布局与接口联调

> **任务**：`SYSINT-03-03A-WIRE-L01`（feature / P1 / M / 5分）· 执行 `agent:frontend-agent` · 认领/监管 `human:孔东`
> **前置**：`SYSINT-03-03A-JAVA-L01`（integration，Java 写侧七端点已交付）、`SYSINT-03-15-L01`（ready_to_sign，网关统一用户中心）
> **状态**：2026-11-10 16:31 完工推 `origin/dev`（`c6effe0`），转 **integration**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` + `agent:frontend-agent`（本会话执行） |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `CmsContentFrame`/`CmsEditDrawer`/`persistRecord`/`cmsTypeSchema`/`IndustryThreeLevelCascader` 既有通用件，本单零新增依赖、零新增文件（净改动全落在既有组件/工具内）。未用 YAGNI 跳过 D8/D9/D10（CMS 管理页无统计数字，ⓘ/角标不涉及）、可观测（走 `@/utils/request` 主干自动埋点）、架构铁律（前端只调 Java REST）。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（CMS 管理页 UI 联调叶，无架构/存储流图改动） |

## 问题清单

1. **布局走查承接**：本单承接 `SYSINT-03-03A-L01`（布局与抽屉化）后的写侧联调收尾。L01 遗留的三大联调阻塞（deploy:cms 未确认 / 网关前缀待定 / 本机网关不可达）期间由并行会话+本单逐步消化：写侧已按 `/cms/cms-ops/v1/**` 网关前缀接线（`CMS_OPS_PREFIX` 四模块常量），PUT/DELETE 已按 `LUMEN-GATEWAY-METHOD-RESTRICT-L01` 改 POST。
2. **`CMS_OPS_UNSUPPORTED` 已清空**：七类 `svc_*` content_type 写接口全部就位（`40c3b68` 四页对接 cms-ops 写接口），enterprise 族双榜单/维度同步接入（`67605d1`/`08afdb6`）。
3. **机构主数据已切真实字典**：`be85bed` `/org-options` 联想+屏1列表+org 筛选；`d13ec24` org-options 失败时禁 mock 兜底（fail-closed，不再造假数据）。
4. **本单收尾两缺陷**（用户 2026-11-10 会话指认）：
   - 门户四页（企业/产业服务/全景/政策）进页即打全部 Tab 接口 → `a029cd2` 改 Tab 激活才建 store（任务 7164514233）；`2ccfe12` 空产业 Tab 不拉数+静默空表；`7964441` gate 后恢复区块间距。
   - 政策 CMS 产业级联越级 + 勾产业查询全空 → `4387323` 收敛两级（`maxLevels=2`，L0 即叶子）+ slug→目录 INB 码归一匹配；`c6effe0` 勾集群后二级禁用 + 两级模式彻底断链/节点接口（`:load-more` 不传 + tag 文案解析改走 Q068 目录，勾选后 0 个 `/search/meta/industry-chains|nodes` 请求）。

## 修改内容

**本单收尾轮（2026-11-10，6 commits）**：

| commit | 内容 |
|---|---|
| `d13ec24` | org-options 失败禁 mock 兜底 + 产业筛选不挡新增 |
| `2ccfe12` | 门户四页空产业 Tab 不拉数 + 静默空表修复 |
| `acc7849` | 服务榜单空产业过滤与查询刷新修复 |
| `224da56` | 服务机构榜单 org_id 提交丢失修复 |
| `a029cd2` | 门户四页接口按需拉取（Tab 激活才建 store，`useCmsOpsLoadGate` 懒建） |
| `7964441` | 三 Tab 包 gate 后恢复区块纵向间距 |
| `4387323` | 产业级联收敛两级 + 勾产业查询全空修复（`cmsListFilters.ts` slug→INB 归一；`CmsContentFrame` 传 `:max-levels="2"`） |
| `c6effe0` | 勾集群后二级禁用 + 两级模式彻底断链/节点接口（`IndustryThreeLevelCascader.vue`） |

**写侧接线主线（2026-11-03 ~ 11-07，承接 L01 后并行会话+本单）**：

| commit | 内容 |
|---|---|
| `c94852f` | 03A D-2 落地：产业服务 5 子功能 UI 补齐、四屏工作台 |
| `40c3b68` | 四页对接 cms-ops 写接口与列表失败门控（`CMS_OPS_UNSUPPORTED` 起点） |
| `c83b559` | 网关 PUT/DELETE 限制：16 处改 POST（含 CMS 运营） |
| `08afdb6` | 企业 CMS 接入真实企业与持久化编辑 |
| `67605d1` | 企业双榜单与维度维护页面接通 |
| `be85bed` | 机构字典切真实主数据 `/org-options`（DoD「不得长期仅 2 家 mock」闭环） |
| `9e8a589` | 独立态接入真实菜单权限 + 名次/排序正整数 |
| `f9dad50`/`6bb7458` | 屏1产业查询三改（默认空=全量/集群展开/编辑落点精确 INB） |
| `d28cc8a` | 列表产业列真实 INB 码显名（先查 Q068 目录） |
| `c5ecf6a`/`43dc16e` | 通用筛选栏对齐其他页交互 + 一级 Tab 布局 |
| `e966210` | 机构编码列展示统信码 + 抽屉持久错误提示 |

## 测试结果

- `pnpm type-check`（vue-tsc --build）✅ 2026-11-10 16:2x 通过（级联改动后复跑）
- `pnpm build` ✅ 2026-11-10 16:2x 通过（vite build 24.19s，4322 modules）
- `node src/views/cms/enterprise/cmsTabFetchFix.selfcheck.mjs` ✅（门户四页 Tab 拉取回归 A1–A5 + 按需拉取断言）
- `node src/views/policy/policyCmsGapFix.selfcheck.mjs` ✅（B-4/B-5/C-3 + 两级级联/slug 匹配断言）
- 浏览器实测（dev server https://localhost:3000/policy/news-cms，CDP）：
  - 关键词「大发疯」查询 3 行 → 2 行 ✅（本地过滤生效，查询=快照不打接口，对齐其他 CMS 页交互）
  - 勾「新一代信息技术」集群 → 表内集成电路记录全保留 ✅；展开面板二级（集成电路/传感器/人工智能等）全部 `disabled` ✅
  - 两级模式勾选后 Network 0 个 `industry-chains`/`industry-nodes` 请求 ✅
- CRUD 端到端：写侧 `persistRecord` 单点 → `createCmsOps`/`updateCmsOps`/`publishCmsOps`/`unpublishCmsOps`/`deleteCmsOps`（POST 化）；列表 `listAllCmsOps` 分页拉全；机构 suggest `/org-options` 真实主数据

## 遗留风险

1. **USE_MOCK 开关**：`getCmsEnterpriseStore` 按 `USE_MOCK` 分流 mock/ops store；当前 dev 构建 `USE_MOCK=false` 无 fixture 填数（DoD 合规），mock store 仅留本地联调通道。
2. **L01 问题清单 2 的两个文字性缺口**（榜单评述/深圳竞争力分析字段）仍未登记契约缺口节，待契约确认会。
3. **`CmsEditDrawer` 存量 5 个 `vue/no-mutating-props` eslint 报错**（L01 期已存在，非本单引入，行号平移）。
4. 签收权在监管人：本单停在 integration，不自行 done。

## CI/CD（必填）

- 分支：`dev`（lumen-ui-topic）
- commit：本单收尾 `c6effe0`（tip）；push `ffccc28..c6effe0`（含 rebase 远端增量）
- pipeline URL / ID：随 dev push 自动触发（GitLab CI 前端轨）
- 部署 namespace / 镜像 tag：K8s dev（CI 触发）
- K8s rollout：随 CI（push 后自动）
- dev 测试 URL：https://localhost:3000/policy/news-cms、/service/portal-cms（本地实测）；K8s dev 待 CI 发布后走查

## 可观测性（建议）

- OTEL_SERVICE_NAME：复用仓内前端配置
- 埋点：CMS 接口走 `@/utils/request` 主干，`X-Trace-Id`/`traceparent` 自动注入上报（systemCode=topic），无 CMS 特例
- Tempo / Loki：dev 有（随网关链路）

## 涉及文件（本单收尾轮）

| 文件 | 变更 |
|---|---|
| `src/components/filter/IndustryThreeLevelCascader.vue` | `maxLevels` 两级模式：L0 即叶子、勾集群后二级 disabled、不传 load-more、tag 解析走 Q068 目录零接口 |
| `src/components/cms/CmsContentFrame.vue` | 产业级联传 `:max-levels="2"` |
| `src/components/cms/cmsListFilters.ts` | slug→中文名→目录 INB 码归一匹配（勾产业查询全空修复） |
| `src/components/cms/useCmsOpsLoadGate.ts` + 四工作台 | Tab 激活才建 store（按需拉取）；空产业 Tab 不拉数；gate 后间距恢复 |
| `src/views/policy/PolicyNewsCmsPage.vue` | sections 懒建 store（工厂 getter） |
| `src/views/policy/policyCmsGapFix.selfcheck.mjs` | +两级级联/slug 匹配断言 |
| `src/views/cms/service/ServiceCmsWorkspace.vue` | 双 `</section>` 合并冲突残留修复（vite build 阻塞） |
| `src/views/cms/service/ServiceCmsRankTab.vue` / `ServiceCmsShenzhenTab.vue` / `enterprise/EnterpriseCmsKeySetTab.vue` | Tab 拉取与提交字段修复 |
