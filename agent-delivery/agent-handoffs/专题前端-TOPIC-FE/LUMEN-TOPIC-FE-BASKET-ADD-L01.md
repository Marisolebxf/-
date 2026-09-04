# LUMEN-TOPIC-FE-BASKET-ADD-L01 · 系统对比篮·篮内新增改为弹窗智能检索

> 格式参考 `templates/handoff-template.md`。空篮 CTA 不再跳查询页。区域 Tab 不在本单。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 用户确认「认领开工」后转 `in_progress`；人测后待签收。registry 闸门 `ready_to_sign→done` 只认 `human:淮政玮`，按孔东当面授权代签写入 `done`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `compareBasket` / 现有 Java 智能检索口；只加一个弹窗与行映射。未用 YAGNI 跳过 D8/D9/D10、调用链。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂 Headroom。 |

## 范围与实现

仓：`lumen-ui-topic`。企业 / 产业 / 服务机构三 Tab 共用 `CompareBasketAddModal`。区域 Tab 仍为开发中空页。`USE_MOCK=false` 禁止 fixture 填数。

### DoD 1 · 篮内「新增」

有列表且未达容量时，重置后增加 `type="text"`「新增」。企业 FilterBar：搜索与类型下拉同宽（最多 280px），重置 / 新增靠右；新增用 `IconPlus`。满员隐藏。产业 Tab 任一 `industry` / `industry_chain` 未满即可新增。

### DoD 2 · 空篮 CTA

「去企业查询 / 去产业查询 / 去服务机构查询」统一改为「新增」。点击只开弹窗，不 `router.push` 查询页、不 `closeSurface`。

### DoD 3 · 同一弹窗 · 智能检索

| Tab | 默认 | 有关键词 |
|-----|------|----------|
| 企业 | `entRecommend` | `#8 entSearchSmart` |
| 产业（含产业链） | `industrySearch({ mode: 'smart' })`；空关键词且无 records 回落 `industryCatalog` | 同上 smart |
| 服务机构 | `svcSearchOrgs` 空关键词优先 `recommended`，否则 `items` | 同接口带 keyword |

弹窗 body 定高 500px，表格拉满；关键词 + 列表 + 分页；无高级筛选。

### DoD 4 · 行操作

行：名称、详情、加入/移出对比篮。加/移走 `compareBasket.add/remove`（服务机构仍走 `/svc/.../compare-basket`；`source` 含 `external` 由 store 拒绝）。篮内列表靠 Pinia 当帧同步。

### DoD 5 · 不做

- 区域 Tab 不接
- 查询页行内「加入对比篮」保留；结果栏「对比篮」按钮已按人测要求隐藏（右下角浮层仍在）

## 偏离说明

- 满员时 store 仍弹「最多添加 N 项」；加失败不再误报「已移出」。
- 产业/服务「详情」仍会关浮层并跳走；空篮「新增」本身不关浮层。
- `serviceOrgBasket.selfcheck.mjs` 改为断言弹窗。

## 会话附带（非本单 DoD，同仓一并交付）

- 查询结果栏 `ResultToolbar` 隐藏「对比篮」入口。
- 招引复核空态去掉「mock 关闭时不会使用 fixtures 兜底」。
- 痛难点诊断 `#102`：`diagnosisScope` 改为扁平 `["tech_rd","market_expand","financing","management"]`，不再套 `dimensions`。读回兼容旧 `{ dimensions }`。

## 产物清单

- `src/utils/compareBasketAddSearch.ts` + `compareBasketAddSearch.selfcheck.mjs`
- `src/components/enterprise/compare/CompareBasketAddModal.vue`
- `src/components/enterprise/CompareBasketFilterBar.vue`
- `src/views/enterprise/EnterpriseCompareBasketView.vue`
- `src/components/enterprise/compare/IndustryCompareBasketPanel.vue`
- `src/components/enterprise/compare/ServiceOrgCompareBasketPanel.vue`
- `src/views/service/serviceOrgBasket.selfcheck.mjs`
- `src/components/search/ResultToolbar.vue`
- `src/components/enterprise/recruit/CandidatePanel.vue`
- `src/config/enterpriseRisk.ts` + `enterpriseRisk.selfcheck.mjs`
- `src/composables/useEnterpriseRisk.ts` / `enterpriseRiskHelpers.ts`
- `src/api/enterprise/types/riskInsight.ts`
- 本 handoff

## 验收证据

- `node src/utils/compareBasketAddSearch.selfcheck.mjs` → ok
- `node src/views/service/serviceOrgBasket.selfcheck.mjs` → ok
- `node src/config/enterpriseRisk.selfcheck.mjs` → ok
- `npx vue-tsc --build` → 绿
- 人测：弹窗检索/加篮、筛选行布局、弹窗定高、痛难点 `diagnosisScope` 扁平数组 — 监管人孔东确认，**联调通过**

## 遗留风险

- 推荐/智能检索 Java 空包时弹窗诚实空。
- 产业空关键词若 `industrySearch` 抛错，不会回落 catalog。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未改算法 |
| 2 调用链 前端→Java | ✅ 只调已有 Java 检索 / 任务创建口 |
| 3 Nebula | ✅ 未改图谱存储 |
| 4 可观测 | ✅ 新请求走现有 `request`（traceId 已注入） |
| 5 CI | ⏳ push `origin/dev` 后看 Pipeline |
| 6 demo2 不 merge lumen | ✅ |
| 7 共享聚合 / 只调 Java | ✅ |
| 8 数据策略 | ✅ 失败/空列表不补假数 |
| 9 D8 Design | ✅ 按钮 `type=text` + 控件高 32 |
| 10 D9 指标 | N/A 本叶无新统计数字 |
| 11 D10 交互 | ✅ 弹窗可关；详情/加篮走 Arco 按钮 |
| 12 D12 禁 demo-* | ✅ 未指向任何 `demo-*` |

## CI/CD（必填）

- 分支：`lumen-ui-topic` / `gkx-orchestration` 均 `dev`
- commit：`lumen-ui-topic` `b0ea3de`；orchestration SHA 随本仓 push
- pipeline URL / ID：push 后由 GitLab CI 生成
- 部署 namespace / 镜像 tag：CI 触发 K8s dev
- K8s rollout：待 Pipeline
- dev 测试 URL / 命令与结果：selfcheck 三条 ok；`vue-tsc --build` 绿；人测联调通过

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用现有前端 request
- traceId（dev 抽样）：未采
- Tempo / Loki：无

## 涉及文件

见上文产物清单。
