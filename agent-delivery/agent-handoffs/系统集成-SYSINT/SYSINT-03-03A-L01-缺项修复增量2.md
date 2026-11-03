# Handoff · SYSINT-03-03A-L01 专题服务运营正文 · 缺项修复增量（第 2 轮）

> **任务**：`SYSINT-03-03A-L01`（feature / P1 / M / 5分）· 执行 `agent:frontend-agent` · 监管 `human:孔东`
> **本轮范围**：2026-11-03 note「缺项优化补充」中不依赖拍板的 2 项（X-6、R-1/R-3）；只动前端，数据走 mock（用户指令 12:18）
> **前置**：第 1 轮（抽屉化/状态筛选/DoD 提示）见 `SYSINT-03-03A-L01.md`，commit `5436e8b` 已推
> **代码基线**：`lumen-ui-topic` dev @ `220db19` 之上，commit `5776ce5` **停在本地未 push**（用户指令"先 commit 不 push"）
> **对照真源**：`agent-handoffs/专题对齐-TOPIC/门户内容管理-四页前端实现对照.md` v1.1
> **建档**：2026-11-03 · 强度 ponytail full

---

## 修改内容（2 项）

| 缺项 | 文件 | 改动 |
|---|---|---|
| **X-6** DoD 约束只是提示条 | `ServiceCmsWorkspace.vue` | 发布时正文做模式校验（草稿不拦）：分数（`92.5分`/`85点`）、名次（`第x名`/`排名第x`/`Top N`）、领导人（董事长/总经理/CEO/创始人/法定代表人）三类命中即 warning 阻断；带 ponytail 注释：关键词启发式有误报可能，改写文案可绕过——升级路径=接 Java 后服务端校验。DOD_HINT 提示条保留 |
| **R-1/R-3** 死代码 | 删 `CmsOpsPage.vue`、`CmsFrameworkPreview.vue` + `routes.ts` 移除 `cms-framework-preview` 路由 | 全仓 grep 零业务引用（cmsTypeSchema.ts:10 注释中的 `cms-ops/` 是 pathKey 文案说明，非组件引用） |

## 不在本轮（有依赖）

- **A-2 五子功能**（331 档案+专家评价 / 331 分布 / 332 维度+Top30 / 333 深圳档案+竞争力分析）→ **D-2 拍板**（补 UI 约 3-4 人日 or "走主数据、CMS 只做正文"登记）。这是本页最大缺口（全档 3 个整叶 0 UI 中占 2 叶），**建议孔东优先拍**
- 机构无「新增机构」入口 → 等 Java 机构主数据（CMS-JX-SVC-LIST integration 中）；mock 阶段 `CMS_MOCK_ORGS` 2 家占位
- **B-2** 专家署名 → D-7 统一组件

## 测试结果

- `node --experimental-strip-types src/views/cms/service/serviceCmsGapFix.selfcheck.mjs` ✅（X-6 模式命中/正常文案不误报 + R-1/R-3 文件与路由已删）
- `npm run type-check`：CMS 相关 0 错误（vite.config.ts 存量错误非本轮引入）
- `npx eslint src/views/cms/service/ src/router/routes.ts` ✅ 0/0
- **未做浏览器走查**（停本地待孔东验收）

## 验收建议（走查路径）

1. 机构编辑 → 正文粘贴「该机构董事长带队，评估 92.5 分」→ 发布 → 应被拦截并提示改写（X-6）
2. 同内容存草稿 → 应正常保存（草稿不拦）
3. 正常文案（检测认证服务描述）→ 发布 → 通过（无误报）
4. 访问 `#/cms-framework-preview` → 404（R-3 路由已移除）

## 架构合规自检

- 调用链：纯前端 mock ✅；可观测：mock 阶段无请求 ✅
- D8/D9/D10：CMS 管理页无统计数字 ✅
- 未新增依赖、未改配置 ✅

## cost

- actual_tokens: ~35000
- model_used: glm-5.3
- actual_cost: ~$0.3
- cost_warn: green
