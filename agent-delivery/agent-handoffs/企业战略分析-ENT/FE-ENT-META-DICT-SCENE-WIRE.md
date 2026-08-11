# FE-ENT-META-DICT-SCENE-WIRE · 企业码表场景接线

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull`（由 `human:曹丽影` 改派） |
| 说明 | 派单包：`FE-ENT-META-DICT-SCENE-WIRE-派单包.md`；吸收原 PATH-FIX 草稿 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单 `/goal` 一致；未用 YAGNI 跳过调用链 / Design / D10；本单无新增裸统计数字（D9 N/A） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 Cursor 未挂载 headroom；task-registry 用 CLI 应急通道 |

---

## 1. 范围与实现（对照派单包 DoD）

| DoD | 状态 | 证据 |
|-----|------|------|
| 深圳现状产业链下拉请求带 `scope=future`，八大规范名 | ✅ | `entMetaChains.ensureLoaded({ scope:'future' })`；Network：`POST .../meta/chains` body `{"scope":"future"}`（监管人冒烟确认） |
| 高企/上市等类型筛选用 `/meta/tags`，未误用 `company-types` | ✅ | 重点分析仍走 `entTagDictionary` / `compareBasketTypeOptions`；未改工商 `company-types` 用途 |
| 结果区/重点分析：region-scopes 四根；全国可选到区且反显；`region_id` 正确 | ✅ | `RegionValue.path` + Cascader 全路径；`regionPathToKeyAnalysisParams`；监管人确认全国可选到区 |
| 场景删减矩阵：深圳现状裁剪；查企业/重点分析全开 | ✅ | `filterRegionCascaderByScene`；SZ 页注入 `sz-status`；search/key-analysis 全开 |
| region-scopes 缓存 key bump | ✅ | `ent.regionScopes.cascader.v2`；chains 分 scope：`ent.metaChains.v2.{scope}` |
| 不直连 Python；不改 Java/Python 契约真源 | ✅ | 仅 `lumen-ui-topic`；经 Java `.../search/meta/**` |
| handoff | ✅ | 本文件 |
| push `origin/dev`；冒烟写入 | ✅ | 见 §CI/CD；冒烟见 §3 |

**不做（已遵守）**：改 Java/Python 契约、高筛 `/meta/regions` 大改、后端场景裁剪 API、demo-ui 改动。

---

## 2. 修改内容

- **types**：`EntMetaChainsRequest.scope?`；`EntRegionScopeRequest.expand_national?`
- **entMetaChains**：默认/强制 body `{ scope }`；按 scope 分缓存；Pinia HMR
- **entRegionScopes**：cache `v1` → `v2`
- **RegionSelect**：`RegionValue.path` 支持全国 ≥4 段反显
- **regionScopeScene**：场景裁剪 + path→`region_id` 纯函数
- **接线**：深圳现状 / 重点分析 / 查企业结果区
- **mock**：`scope=future` 八大；national 省市区样例
- **selfcheck**：`scripts/selfcheck-fe-ent-meta-dict.mjs`

---

## 3. 测试结果

| 项 | 结果 |
|----|------|
| `node scripts/selfcheck-fe-ent-meta-dict.mjs` | ✅ ok |
| `npx vue-tsc --noEmit -p tsconfig.app.json` | ✅ |
| 深圳现状 Network `meta/chains` | ✅ body 含 `scope=future`（human:孔东） |
| 重点分析全国 Cascader 选到区 | ✅（human:孔东） |
| 调用链无 Python `/internal/*` | ✅ |

冒烟步骤：

1. 打开深圳企业现状 → DevTools Network 筛 `chains` → Request Payload 为 `{"scope":"future"}`；下拉为八大。
2. 打开重点企业分析 → 区域 Cascader：全国 → 省 → 市 → 区可选且反显；请求参数 `region_id` 为叶国标码。
3. 查企业结果区 RegionSelect：全球/全国/区域/热门四根均在。

---

## 4. 遗留风险

| 项 | 说明 |
|----|------|
| 联调环境 Java 偏旧无 `scope` 透传 | 派单包已声明为部署回灌，非本单开发范围 |
| sessionStorage 命中时不发 `chains` 请求 | 清 `ent.metaChains.v2.future` 或等 TTL；勿与 `region-scopes` body 混淆 |
| 高筛 industry_chain 全量 | 本单未改高筛 chains；需全量时另调 `ensureLoaded({ scope:'all' })` |

---

## 5. CI/CD（必填）

- 分支：`dev`（`lumen-ui-topic`）
- commit：`12f896c`
- pipeline URL / ID：push 后等 GitLab CI（仓 `lumen-ui-topic` · `dev`）
- 部署 namespace / 镜像 tag：K8s dev（CI 触发）
- K8s rollout：待 CI
- dev 测试：本机 `npm run dev` 冒烟通过（见 §3）

---

## 6. 可观测性

- 新请求走既有 `request.ts` 拦截器（`X-Trace-Id`）；未新增越层调用
- 本单无新增业务埋点点位

---

## 7. Design.md / 交互 / D9

| 检查 | 结果 |
|------|------|
| Design.md：Arco Cascader/Select，无新造组件库 | ✅ |
| D10：RegionSelect `aria-label` / change-on-select 保留 | ✅ |
| D9：无新增裸统计数字 | ✅ N/A |

---

## 8. 架构合规自检（§2）

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ N/A |
| 2 | 前端 → Java → Python | ✅ |
| 3 | Nebula | ✅ N/A |
| 4 | 可观测 | ✅ 既有 request 链 |
| 5 | CI/CD | ✅ push origin/dev |
| 6 | demo2 不 merge lumen | ✅ |
| 7 | 共享聚合核心 | ✅ |
| 8 | ADS/Mock | ✅ mock 对齐 |
| 9 | Design.md / Arco | ✅ |
| 10 | D9 血缘 | ✅ N/A（字典接线） |
| 11 | D10 交互 | ✅ |

---

## 9. 涉及文件（`lumen-ui-topic`）

- `src/api/enterprise/types/search.ts`
- `src/stores/entMetaChains.ts` · `entRegionScopes.ts`
- `src/components/search/RegionSelect.vue`
- `src/components/enterprise/keyAnalysis/TypeRegionPanel.vue`
- `src/composables/useKeyEnterpriseAnalysis.ts` · `useSearchBootstrap.ts`
- `src/utils/regionScopeScene.ts` · `keyAnalysisParams.ts`
- `src/views/enterprise/EnterpriseSzStatus.vue`
- `src/fixtures/enterprise/keyAnalysisHelpers.ts`
- `src/mock/enterprise/topicApi.ts` · `keyAnalysisSzStatusApi.ts`
- `scripts/selfcheck-fe-ent-meta-dict.mjs`

编排仓：本 handoff + task-registry 状态/证据回填。
