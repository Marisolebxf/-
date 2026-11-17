# FE-TOPIC-SMALL-SVC-SEARCH-L01 — 专题小屏·产业服务链 E（服务机构查询页）

- **状态**：已交付（commit `c16e75b`，已推 `origin/dev`）
- **执行**：agent:frontend-agent；**监管**：human:孔东
- **交付时间**：2026-11-17 23:50 (+08:00)
- **ponytail**: full（PC 检索 DSL/智能解析不移植，首版降级为关键词+固定筛选；自检脚本 1 个）

## 范围与实现（对照 PC ServiceOrgSearchPage.vue）

| 交付物 | 说明 |
|---|---|
| `src/views/service/ServiceOrgSearchView.vue` | 检索页主视图（keyword/field 双模式） |
| `src/router/index.ts` | `/service-center/search` 挂真组件（替 NotAdaptedView） |
| `scripts/svc-org-search.test.mjs` | 防漏自检 |

### 关键实现决策

1. **双模式降级口径**（派单 note 已注明）：keyword 模式 = 关键词检索；field 模式 = 固定字段筛选（服务类型/城市/机构类型/环节/技术力下限，`filters` DSL 直译）。PC 的智能解析（`parseServiceOrgQuery`）与 fixture 字段库不移植。
2. **字典只认 Java**：`svcMeta` 实包填充城市选项；失败不阻断（200+空数组语义），城市下拉降级用结果 items 去重，不造字典。
3. **「加入分析」闭环**：结果卡 checkbox 勾选 → 底部操作栏 → 携 `org_ids[]` + `source=search` 跳 `/service/institution-judgment`（C 单 URL 契约），形成「检索 → 选机构 → 分析」完整链路。
4. **最近查询**：localStorage 暂存（8 条上限），van-tag 点按复用。
5. **空态诚实**：技术力无值显示「暂无」（禁前端算分）；空结果提示调整条件；零 fixture。

## 产物清单

- 代码：commit `c16e75b`（3 文件，+520 行）
- 自检：`node scripts/svc-org-search.test.mjs` ✅
- CI：commit 已推 `origin/dev`

## 验收证据

- `node scripts/svc-org-search.test.mjs` ✅
- `npm run type-check` ✅ 全绿
- K8s dev URL：`/service-center/search`

## 偏离说明

- smart 模式降级为关键词检索（PC 智能解析需 `parseServiceOrgQuery` 全量移植，移动端首版不进；后续按需补）。
- 对比篮（`svcCompareBasket*` API）不在本单——mobile 首版「加入分析」走 URL org_ids[]（API 端点已在任务 A 就位，后续如需服务端篮可平滑接）。

## 架构合规自检

- ✅ 调用链（前端 → Java REST → Python /internal，不可越层）：search/orgs + meta 只调 Java 门面
- ✅ D8 Design：结果卡/筛选面板对齐仓内 Vant token
- ✅ D9 数据血缘：技术力有值才显示，无值「暂无」；禁前端算分
- ✅ D10 交互规范：checkbox/tab/dropdown 键盘可达；空态文案诚实
- ✅ D12 demo/lumen 隔离：零 demo 依赖（未用 fixture 字段库）
- ✅ 可观测埋点：defineApi 走统一 http 封装
- ✅ CI/CD：commit 推 `origin/dev` → Pipeline → K8s dev rollout

## 开放项

- 5 张单（A–E）全部交付。分析记录面板、ⓘ 角标、svc 域报告文档随 P2 批次。

## cost

- actual_tokens ≈ 85k；model_used: glm-5.3；actual_cost ≈ $1.2；cost_warn: green
