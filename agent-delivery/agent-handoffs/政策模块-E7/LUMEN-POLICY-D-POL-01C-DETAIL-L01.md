# LUMEN-POLICY-D-POL-01C-DETAIL-L01 · 政策专题 D · 查询页详情抽屉对齐 demo PolicyDetailDrawer

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-FE-D-总派单.md`](./LUMEN-POLICY-FE-D-总派单.md)  
> 复刻：[`fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)  
> 前序：[`LUMEN-POLICY-D-POL-01C-L01.md`](./LUMEN-POLICY-D-POL-01C-L01.md) `fbfe737`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。对照 demo `/policy/search` 右侧详情抽屉，不对照门户 ElementProfile。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 抽 `PolicyDetailDrawer.vue`；复用 SectionPanel / StatusTag / `@/review` MetricSpecCard · MockBadge · TraceInfoIcon；未贴 JSX；未改 POLICY-STORAGE-FLOW 工厂拓扑；详情仍只调 Java `GET /policy/topic/v1/policy/docs/{id}`。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 前端仍走图上已有读边：`lumen-ui-topic` → gateway `/policy/topic/v1/policy/docs/{id}` → `gkxlumen-topic-policy`。工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。 |
| 会签态 | `approved`（`storage/POLICY/01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

`/policy/search` 点「查看详情」对齐 demo `PolicyDetailDrawer`：

1. 抽屉宽 **960**；title = 政策标题 + 级别 Tag（`--sci-primary-soft`）+ 状态 Tag（已发布绿）。
2. Tab：概览 / 政策原文 / 条款结构化（本仓 `analysis-tabs` 三列皮肤）。
3. 概览：`a-descriptions` column=2 `layout=inline-vertical`：政策ID、政策级别、政策类型、发布机关、所属地区、发布时间。
4. 政策摘要：12px 灰标签 + 14px 正文。
5. 关键词 / 要素：紫底 `--sci-elem-policy-soft` / `--sci-elem-policy`。
6. 支持强度构成四卡横排；HelpPopover + Trace + 数字旁 ⓘ 只读 catalog `M_POLICY_SUPPORT_STRENGTH`。Java 无数字字段则「暂无」，禁止写死 92/70/55/85。
7. footer：outline「打开政策原文（新窗口）」+「关闭」。无加入对比篮、无深度分析。
8. 政策原文 Tab：有 Java `content` 才展示；无数诚实空 + 评审 MockBadge。禁止 Demo 分章 fixture。
9. 条款结构化 Tab：仅当 Java 返回条款数组才出表；`elements`/`keypoints` 不当表。

检索页卡片与 SearchHub 未改（V1–V7 保留）。

## 偏离说明

- DWD `factors` 多为要素名 CSV，不是 `{fund,tax,land,talent}` 分值；四卡诚实空，不把要素名映射成分数。
- 无 `url` 时「打开政策原文」禁用，不伪造来源。
- 条款无 expand 行，原文片段作列（Arco Vue 表无 Demo `expandedRowRender`）。
- `M_POLICY_SUPPORT_STRENGTH` 前端 seed 未登记：评审 ⓘ 为未入库存红问号，不伪绿。

## 产物清单

- 代码：`lumen-ui-topic` `d5ea3f7a62683fe6338a5abf04329c7a00007f09` → `origin/dev`
- 本文 handoff

## Java 调用

| 动作 | 方法 | 路径 |
|------|------|------|
| 详情 | `policyDocs` GET | `/policy/topic/v1/policy/docs/{id}` |
| Mock 开 | `registerApiMock` 诚实空 `item=null` | 页内无 `MOCK_` |

## 验收证据

- `node src/views/policy/policyDetailDrawer.selfcheck.mjs`：`policyDetailDrawer.selfcheck ok`
- `node src/router/menu.selfcheck.mjs`：`svc-shell ok` + `policy-shell ok`（宽 960 / Tab / 禁钮 / 无 fixture）
- `npx vue-tsc --build`：零 error
- USE_MOCK=false：只渲染 Java 实包；无分值 / 无正文 / 无条款 = 可见空态

### 复刻五维 R1–R5

| # | 结果 |
|---|------|
| R1 布局 | ✅ 宽 960、标题+双 Tag、三 Tab、概览两列 Descriptions、摘要、紫关键词、四卡、footer 双钮 |
| R2 交互 | ✅ 详情 loading / 失败重试 / 诚实空；Tab 切换；无 url 禁用打开原文 |
| R3 样式 | ✅ `--sci-*`、analysis-tabs、SectionPanel 蓝条、已发布绿 Tag |
| R4 评审 | ✅ `@/review`：`POLICY-SEARCH-DETAIL-SUPPORT-TRACE` + MetricSpecCard + MockBadge；关评审零泄漏 |
| R5 Mock | ✅ 关开关不引用 `@/mock/**` / Demo fixture；开仍走诚实空包 |

### 检索皮肤 V1–V7（检索页已有，本叶保留）

| # | 结果 |
|---|------|
| V1 | ✅ 页底 `--sci-bg-page` / `#D8E7FC` 未改 |
| V2 | ✅ SearchHub 皮肤未改 |
| V3 | ✅ 卡内标题+摘要横向书写未改 |
| V4 | ✅ 未叠 `industry-search-result-card` |
| V5 | ✅ 主列 `min-width: 0` 未改 |
| V6 | ✅ 无数诚实空 / 有数出卡未改 |
| V7 | ✅ 结果 `article` 不含 `industry-search-result-card` |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 前端不解析条款、不算支持强度 |
| 前端→Java→Python `/internal/*` | ✅ 只调 `policyDocs` |
| 图谱 Nebula | ✅ 本叶不 new 地图、不直连 nGQL |
| 可观测 | ✅ 复用 `request.ts` `X-Trace-Id` |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ Vue 重写，未贴 JSX |
| D8 / D10 | ✅ token + Arco；交互对照 demo 抽屉 |
| D9 8 件套 | ✅ 四卡数字旁 ⓘ 只读 catalog；无数不造假 |
| D12 lumen 不调 demo **服务** | ✅ 无 `demo-*` URL |

## 测试结果

- 自检 + `vue-tsc --build` 通过。
- 联调通过：详情路径仍是 C-SEARCH `GET /policy/topic/v1/policy/docs/{id}`；空/失败诚实，不 5xx 填数。

## 遗留风险

- 现网 DWD 多数无四维分值 / 全文 / 条款数组，抽屉会诚实空；不是回落 fixture。
- K8s `gkxlumen-topic-policy` 若未发布，详情 404，前端失败可重试。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`d5ea3f7a62683fe6338a5abf04329c7a00007f09`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines?ref=dev
- 部署：随仓既有 CI；本叶不改 helm
- dev URL：`http://192.168.88.50:30892/policy/search`（发布后点「查看详情」）

## 可观测性

- 复用前端 `request.ts` `X-Trace-Id` / `traceparent`
- Tempo / Loki：随平台；本叶未抽样

## 修改内容

| 路径 | 动作 |
|------|------|
| `src/components/policy/PolicyDetailDrawer.vue` | 新增 960 抽屉 |
| `src/views/policy/PolicySearchPage.vue` | 挂抽屉，去掉 560 单列 Descriptions |
| `src/views/policy/policySearchModel.ts` | keywords / factors / clauses 解析 |
| `src/views/policy/policyDetailDrawer.selfcheck.mjs` | 诚实空自检 |
| `src/components/common/StatusTag.vue` | 已发布/现行 → 成功绿 |
| `src/router/menu.selfcheck.mjs` | 抽屉断言 |

未改 `DefaultLayout.vue`。未改 vite / package.json / `.gitignore`。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 160000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.05 |
| cost_warn | green |
