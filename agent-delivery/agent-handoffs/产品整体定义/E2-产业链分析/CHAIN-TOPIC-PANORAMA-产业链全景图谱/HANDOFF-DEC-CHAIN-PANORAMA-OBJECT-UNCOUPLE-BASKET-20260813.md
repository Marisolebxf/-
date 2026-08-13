# DEC-CHAIN-PANORAMA-OBJECT-UNCOUPLE-BASKET-20260813 · 签字落实

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:product-agent`（落实 Demo 时兼 frontend） |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | **无对应 ready registry 任务**。未劫持 `CHAIN-UX-L06`（ux-agent claimed）。本轮为用户当场签字并要求落实 Demo。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用周期分析 `industryObjectSelect` + Form 三栏；未新造第三套对象控件；未加新依赖。未用 YAGNI 跳过 D8/D9/D10、handoff、架构铁律。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未走 compress；会话内直接改五件套与 Demo。 |

## 问题清单

- 全景「本次分析对象」绑在对比篮/全局圆点上，路径跳跃；与产业周期分析页内 Select 打架。
- 用户拍板：对象在页内选；篮只收藏和分发。

## 修改内容

### 产品签字

- `DEC-CHAIN-PANORAMA-OBJECT-UNCOUPLE-BASKET-20260813.md`：**已拍板**，签字 `human:淮政玮` 2026-08-13。
- 五件套 v1.5：USM / IA / UX-SPEC / Wireframe / TRACE 已同步；挂点 ID 仍为 `CHAIN-PAN-F01-OBJECT-MODAL-TITLE`（宿主改为 Select 标签，避免 TRACE/测试大改 ID）。

### Demo（`demo-ui-topic`）

- 全景顶栏改为与周期分析同构的三栏：分析对象 Select、所属产业链只读、数据截至；空态主 CTA 即 Select，**无**「打开对比篮」、**无**对象 Modal。
- URL 仍为 `object_type` + `object_id`；清空写 `source=cleared` 且不静默写回默认；无对象进页仍可补推荐示例（`source=default`）。
- 落地清掉对比篮 picker 参数，避免旧深链打开全局圆点。
- 产业查询评审文案改为：可直达全景，或加入对比篮供其它分析分发。业务按钮仍是「进入全景图谱」主、「加入对比篮」次。
- 环节详情「加入企业篮」保留；系统对比篮浮层不删；篮仍可分发进入全景。

## 测试结果

```
node --test tests/industry-panorama-five-pack.test.mjs tests/industry-panorama-contract.test.mjs
```

12/12 pass。

产业查询 `industry-search-five-pack.test.mjs` 仍有 2 条与本 DEC 无关的既有失败（`queryExamples` 列表、Wireframe「推荐态复选框」文案），未在本轮扩大范围去改。

## 遗留风险

- 企业评估 / 风险 / 重点企业全景图（E-33）**不在本轮**；对比篮在那些页仍作多对象编组器。
- 未 commit / 未 push（用户未要求）。
- lumen 正式仓未复刻；待 demo 评审后再 Track-MS。

## CI/CD（必填）

- 分支：各仓当前工作区（未提交）
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：未触发
- dev 测试 URL / 命令与结果：见上；本地 `node --test` 全景 12 绿

## 可观测性（建议）

- 本页原无 `observability.ts` 埋点（产业中心诊断页同样未接）；本轮未新增事件名，避免另起清单。
- 换对象仍走 URL `source=select|default|cleared`，可被路由级追踪。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ 未改算法 |
| 2 调用链 前端→Java→Python | ✅ 未越层 |
| 3 NebulaGraph | ✅ 未改图谱引擎 |
| 4 可观测性 | ⚠️ 沿用页面既有缺口，见上 |
| 5 CI/CD | ✅ 未要求 push |
| 6 demo 不 merge lumen | ✅ 只改 demo-ui-topic + 编排文档 |
| 7 共享聚合 / 前端只调 Java | ✅ |
| 8 数据策略 | ✅ Mock 目录 Select |
| 9 D8 Design / Arco | ✅ Arco Select/Form/Input |
| 10 D9 血缘 | ✅ 未删 ⓘ / 未改指标数字 |
| 11 D10 交互 | ✅ 对齐周期分析页内对象栏 |

## cost 回填（无 registry 任务，记在 handoff）

| 字段 | 值 |
|------|-----|
| actual_tokens | ~180k in / ~45k out（跨两轮会话估算） |
| model_used | Cursor Grok 4.6 |
| actual_cost | ~$2（估算，低于 $10 暂停线） |
| cost_warn | false |

## 涉及文件

编排仓：

- `agent-delivery/agent-handoffs/产品整体定义/E2-产业链分析/CHAIN-TOPIC-PANORAMA-产业链全景图谱/DEC-CHAIN-PANORAMA-OBJECT-UNCOUPLE-BASKET-20260813.md`
- 同目录 USM / IA / UX-SPEC / Wireframe / TRACE（v1.5）

`demo-ui-topic`：

- `src/app/pages/industry-center/IndustryPanoramaPage.tsx`
- `src/app/pages/industry-center/industryPanoramaModel.ts`
- `src/app/pages/industry-center/industryTopicAnalysis.css`
- `src/app/pages/industry-center/IndustrySearchPage.tsx`
- `src/app/pages/industry-center/IndustryReviewMount.tsx`
- `src/app/pages/industry-center/industryCenterData.ts`
- `tests/industry-panorama-five-pack.test.mjs`
- `tests/industry-panorama-contract.test.mjs`
- `tests/industry-search-five-pack.test.mjs`
