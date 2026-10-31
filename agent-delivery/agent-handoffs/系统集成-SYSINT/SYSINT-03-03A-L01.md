# Handoff · SYSINT-03-03A-L01 专题服务运营正文（前端 lumen-ui-topic）

> **任务**：`SYSINT-03-03A-L01`（feature / P1 / M / 5分）· 执行 `agent:frontend-agent` · 监管/签收 `human:孔东`
> **需规真源**：bid-reference L7955–7995（产业服务内容管理）；**契约**：`agent-delivery/agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-专题服务.md`（草案，字段禁改）
> **Java 侧 API 叶**：`SYSINT-03-03A-JAVA-L01`（agent:api-agent，监管 human:徐滕强；2026-10-24 交付，CI pipeline 2847 绿）——写侧 7 端点 `/cms-ops/v1/topic-service/content/svc-business-domain`（POST 新建/PUT 编辑/publish/unpublish/GET 列表/GET 详情/DELETE 软删）+ shenzhen 页 `data.cms` 合并块；**前端版接口文档**：`产物/SYSINT-03-03A-接口文档-前端版.md`（2026-10-26）
> **状态**：2026-10-27 14:40 转入 **integration（联调）**。初版 `2be3717` + 本单增量 `5436e8b` 均已推 origin/dev；认证策略 `587a039`（iframe 强制真实鉴权）为联调前置。
> **人工验收闸门**：`5436e8b` 经监管人 human:孔东 2026-10-27 14:39 指令「代码commit、push dev」放行推送（AGENTS.md ⚠️ 闸门的派单授权例外）。

---

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` + `agent:frontend-agent`（本会话增补执行） |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |

说明：复用既有 `CmsEditDrawer`/`persistRecord`/`cmsTypeSchema` 通用件，删自建整屏表单（净 -1 文件）；DoD（D8 表单框架、指标角标不涉及——CMS 管理页无统计数字）、可观测口径已确认（见下）。未用 YAGNI 跳过任何公约项。

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（CMS 管理页 UI 叶，无架构/存储流图改动） |

## 问题清单

1. **需规 6 块功能只有 1 块进本页**（契约草案冻结）：WBS-03-03 把 L7955–7995 切为三份——03-03a 只认 `svc_business_domain.body_html` 一处 CMS；分布/榜单/深圳档案走 03-03b 指标与主数据；已发布正文回写 DWD 走 03-03c。映射详表见本仓会话规划（2026-10-27），要点：
   - L7967 前半（基础档案：名称/成立时间/服务类型）→ 机构主数据，CMS 只读引用
   - L7967 后半（专家综合能力评估意见）→ `body_html` 语义内 ✅
   - L7969/7971（产业与区域分布）→ 03-03b 指标服务
   - L7977（技术力评估维度）→ 算法/指标侧（权重缺口 Q-SVCCHAIN-01）
   - L7981（Top30 榜单）→ `M_SVC_ORG_TECH_SCORE` + 算法 TECH 分；WBS 明文「CMS 不另维护重点名单」
   - L7989（深圳档案）→ 03-03b
2. **两个文字性缺口（均出自需规原文，非门户页观察）**，建议契约确认会登记进 PORTAL-CMS-专题服务.md 缺口节：
   - 榜单评述：L7983「评估理由、专家评述及相关服务案例」——展示侧（tech 页只有名次/机构/分数）与 CMS 侧均无字段
   - 竞争力分析：L7995「记录专家对深圳……优势、短板及发展潜力的分析意见」——shenzhen 页（全指标）与 CMS 侧均无字段

## 修改内容（本会话三轮，均在初版 2be3717 之上）

1. **整屏编辑改右侧抽屉**（用户 2026-10-27 10:30 指令）：`ServiceCmsWorkspace.vue` 挂通用 `CmsEditDrawer`（即 DoD「编辑页套通用表单框架」），草稿/发布/下架/非空校验逻辑收进工作台；**删除** `ServiceDomainForm.vue`（净 -1 文件）。`CmsEditDrawer.vue` 加可选 `hideTitle` prop（svc 标题由 `org_id` 派生，隐藏标题输入框；企业/全景默认不受影响）。
2. **页面式 CMS 返回按钮加左箭头 icon**（10:38 指令）：`EnterpriseCmsWorkspace.vue`（4 屏）+ `PanoramaCmsWorkspace.vue`（1 屏）`<IconLeft />返回`。服务 CMS 已抽屉化不涉及。
3. **列表状态筛选 + DoD 提示文案**（10:57 批示第 2 项）：查询区加状态下拉（全部/未维护/草稿/已发布，走查询/重置）；`CmsEditDrawer.vue` 加可选 `hint` prop（`a-alert`），服务 CMS 传入「正文仅描述业务领域与专家服务能力评估；法定名称、领导人、名次、分数不进正文。」

## 测试结果

- `npm run type-check`（vue-tsc --build）✅ 通过（每轮改动后各跑一次）
- eslint：两个新改文件 ✅ 干净；`CmsEditDrawer.vue` 有 5 个 `vue/no-mutating-props` **存量报错**（stash 对照原版确认，非本次引入，行号因插 prop 平移）
- 浏览器实测（dev server https://localhost:3000）：
  - 抽屉：打开/保存草稿（「已下架」提示+列表标签草稿）/重新发布还原 ✅；演示数据已还原（已发布/未维护）
  - 返回按钮：企业 `ent-edit-bar`、全景 `pano-edit-bar` 各渲染 1 个 svg 左箭头 ✅
  - 筛选：未维护 → 1 行、重置 → 2 行 ✅；抽屉 DoD 文案渲染 ✅

## 遗留风险

1. **写接口接线联调中**：`persistRecord` 仍写本地 mock store（接线点单点收口）。Java 侧 7 端点已交付（见页首 API 叶关联），联调条件核查见「联调状态与条件」节——**当前阻塞：deploy:cms 未确认 + 网关前缀待定 + 本机网关不可达**。
2. **机构清单仍为 mock**：`CMS_MOCK_ORGS` 仅 2 个占位；等 Java 侧机构主数据 API（用户批示：数据读取统一走 Java 接口）。
3. 门户展示侧尚未消费 `svc_business_domain`（`body_html` 目前只在 CMS 管理）；shenzhen 页 Java 合并已上线，前端消费是展示联调叶范围。
4. 两个文字性缺口未登记（见问题清单 2），待契约确认会。

## CI/CD（必填）

- 分支：`dev`（lumen-ui-topic）
- commit：初版 `2be3717` → **本单增量 `5436e8b`**（2026-10-27 推送，含抽屉化/状态筛选/DoD 提示/企业箭头；全景箭头随并行会话 `284e01c` 入库）；联调前置 `587a039`（iframe 强制真实鉴权）
- pipeline URL / ID：随 dev push 自动触发（GitLab CI 前端轨）
- 部署 namespace / 镜像 tag：K8s dev（CI 触发）
- K8s rollout：随 CI
- dev 测试 URL：https://localhost:3000/service/portal-cms（本地实测）；K8s dev 前端待 CI 发布后走查

## 联调状态与条件（integration 入口快照，2026-10-27 14:30 核查）

**接口契约对齐度 ✅**（对照 `产物/SYSINT-03-03A-接口文档-前端版.md`）：

| 文档条目 | 页面现状 | 对齐 |
|---|---|---|
| A1–A5 七端点（新建/编辑/发布/下架/列表/详情/删除） | 抽屉三动作 + 列表筛选，`persistRecord` 单点待换 | ✅ 映射一一对应 |
| 字段 `org_id`+`industry_id`+`body_html` 三必填 | schema formFields + showBody | ✅ 一致 |
| A4 过滤 `industry_id`/`org_id`/`publish_status` | 产业切换 + 机构关键字 + 状态筛选 | ✅ 已预备 |
| 白名单 sanitize | 前端 htmlWhitelist 预过滤 + 服务端黑名单兜底 | ✅ 分层一致 |
| 管道/鉴权/埋点 | 主干 `@/utils/request`（systemCode=topic、Bearer、X-Trace-Id/traceparent 自动注入） | ✅ 无 CMS 特例 |

**联调阻塞项（3 项待外部）**：

1. 写侧部署：接口文档自述「Part A 待 `deploy:cms` 后可调」（Java 叶只到 pipeline 2847 build 绿，deploy:cms 未确认）——**需徐滕强侧确认**
2. 网关路由前缀：文档写 `/cms-ops/v1/**` 直连；企业叶经验是临时路由 `/cms/cms-ops/v1/**`（2026-10-23 批准）——两前缀待确认走哪个
3. 本机到 dev 网关 `10.50.69.111:30895` 当前不通（2026-10-27 14:30 探测全超时，含已部署 shenzhen 对照组）——网络/VPN 恢复后复测

**非阻塞依赖**：`CMS_MOCK_ORGS` 2 个假码占位（真实机构码清单等 03-03b 主数据 API；联调可先手工种真码冒烟）；登录态（`cms-ops` 401 fail-closed，需真实用户中心 token，认证策略 `587a039` 已强制 iframe 真实鉴权）。

**接线工作量预估**：新增 api 模块（7 端点薄封装）+ `persistRecord` 换实现 + 列表加载从 A4 拉——小时级。

## 可观测性（建议）

- 口径确认（用户 10:57 批示第 3 项）：CMS 接口与外部主干同一套调用/埋点规则——走 `@/utils/request` 即自动继承 `X-Trace-Id`/`traceparent` 注入与上报（`src/utils/observability`），无 CMS 侧特例。当前 mock 阶段无请求产生。
- OTEL_SERVICE_NAME：复用仓内既有前端配置；traceId 抽样：接写接口后补。

## 涉及文件

| 文件 | 变更 |
|---|---|
| `repos/lumen-ui-topic/src/views/cms/service/ServiceCmsWorkspace.vue` | 抽屉化 + 状态筛选 + DoD hint 传入 |
| `repos/lumen-ui-topic/src/views/cms/service/ServiceDomainForm.vue` | **删除** |
| `repos/lumen-ui-topic/src/components/cms/CmsEditDrawer.vue` | +`hideTitle` / +`hint` 两个可选 prop（默认关闭，不影响企业/全景既有用法） |
| `repos/lumen-ui-topic/src/views/cms/enterprise/EnterpriseCmsWorkspace.vue` | 返回按钮 +IconLeft（4 处） |
| `repos/lumen-ui-topic/src/views/cms/panorama/PanoramaCmsWorkspace.vue` | 返回按钮 +IconLeft（1 处） |
