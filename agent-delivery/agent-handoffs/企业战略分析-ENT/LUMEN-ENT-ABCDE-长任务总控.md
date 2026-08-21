# 企业 A–E · 长任务总控（立基线体检）

> **日期**：2026-08-21  
> **授权**：`human:淮政玮`（本管线监管人；后续认领 **不必再问**）  
> **目标**：用段 E 金路径给**已建成的企业实现**取一次客观验收证据，把 registry 与实际代码对齐  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md) v1.13  
> **参照**：[`DEMO-CHAIN-ABCD-长任务总控.md`](../产业链分析-CHAIN/DEMO-CHAIN-ABCD-长任务总控.md)（格式）· [`long-task-e-defect-pack.md`](../../templates/long-task-e-defect-pack.md)（缺陷包）

## 0. 本管线和产业链**不是**同一件事

产业链是「从零建 A→B→C→D→E」。**企业已经建完大半**：Java 门面 141 端点、Python 双路、前端 11 个菜单页已复刻。缺的是**客观验收证据**——`lumen-ui-topic/e2e/` 下只有 `chain-gold.spec.ts`，企业一条冒烟都没有。

所以本总控 **不重走 A–D**，只做两件事：

1. **段 E 立基线**：金路径打已发布环境，拿 PASS/FAIL 事实。
2. **对账**：把「代码已实现但 registry 仍挂 `ready`/`backlog`」的单收口；把「registry 有单但页面根本没建」的升级为范围缺口。

> ⚠️ 本文件 §4 金路径表中标 **`[待确认]`** 的期望原文，须经授权人过目定稿后才可开跑。按规约 §11.4，期望写错 = **C4**，会停循环。

---

## 1. 段位现状（体检基线 · 2026-08-21）

| 段 | 仓 / 制品 | 现状 | 本管线动作 |
|----|-----------|------|------------|
| A 灌数 | `demo_gkxlumenx_*` | `DEMO-ENT-UI-SEED-ODS-L01` = `pending_test`；企业灌数主路径已接约定 ODS | 不重做 |
| B Python | 检索 `lumen-topic-py`（`/internal/gkx-search/**`）· 算法 `lumen-algo-py/vendor/entan-py`（`/internal/*`，`ENTAN_EXPOSE_PUBLIC_API=0`） | 已迁；Java Feign 已指向，禁 `demo-platform-search-py` | 不重做，仅 E0 核健康 |
| C Java | `lumen-svc-platform/gkxlumen-topic-enterprise` + `gkxlumen-topic-async-service` | **门面齐全**，141 端点契约见 `API-ENT-full-catalog.md`；网关 `/enterprise/**` + `/topicAsync/**` | 不重做，仅金路径穿透验证 |
| D 前端 | `lumen-ui-topic/src/views/enterprise/**` | **11 个菜单页已复刻** + 详情页；`src/api/enterprise/` 封装完整 | 不重做；缺口见 §5 |
| **E 冒烟** | `lumen-ui-topic/e2e/` | **空白**——无任何企业 spec | **本管线唯一施工段** |

已发布前端：`http://192.168.88.50:30892`（企业与产业链同一前端）。网关 NodePort `30899`。K8s ns `dev`。联调库 `demo_gkxlumenx_*`。

---

## 2. 14 子模块 × 实现落点（覆盖全集）

| # | 前缀 | 中文名 | 已发布路由 | 实现状态 | 进 E1？ |
|---|------|--------|-----------|----------|---------|
| 1 | `SEARCH` | 企业查询 | `/enterprise/enterprise-search` | 已复刻 | ✅ #1 |
| 2 | `PROFILE` | 企业详情/画像 | `/enterprise/:orgId`（侧栏隐藏） | 已复刻 | ✅ #2 |
| 3 | `COMPARE` | 对比篮 | 浮层 `SystemCompareBasketLayer`；整页 `EnterpriseCompare.vue` **router 未注册** | 组件在·路由缺 | ✅ #3（含负例） |
| 4 | `KEYENT` | 重点企业分析 | `/enterprise/key-enterprise-analysis?workspace=type\|domain` | 已复刻 | ✅ #4 |
| 5 | `EVAL` | 企业评估 | `/enterprise/evaluation?workspace=technology\|business\|competitiveness` | 已复刻（异步任务） | ✅ #5 |
| 6 | `SZSTATUS` | 深圳企业现状分析 | `/enterprise/shenzhen-enterprise-status-analysis` | 已复刻 | ✅ #6 |
| 7 | `RECRUIT` | 引育推荐 | `/enterprise/attraction?workspace=attraction\|cultivation` | 已复刻 | ✅ #7 |
| 8 | `RISK` | 风险洞察 | `/enterprise/risk?workspace=supply-chain\|pain-points` | 已复刻 | ✅ #8 |
| 9 | `OVERVIEW-E32` | 企业整体概况 | — | **页未建**，菜单未挂 | ❌ 范围缺口 |
| 10 | `KEYPANO` | 重点企业概览（E-33） | — | **页未建** | ❌ 范围缺口 |
| 11 | `STAR` | 明星企业介绍（E-34） | — | **页未建**（Java `star-enterprise/*` 已有） | ❌ 范围缺口 |
| 12 | `SHENZHEN` | 深圳企业介绍（E-35） | — | **页未建**（Java `shenzhen/*` 已有） | ❌ 范围缺口 |
| 13 | `OPS` | 维护管理 | — | **页未建**；产业链/服务链都有，唯独企业没挂 | ❌ 范围缺口 |
| 14 | `EXPORT` | 分析导出 | `/topicAsync/topic/v1/analysis/tasks/{id}/asset` | **已知缺陷** `ENT-JAVA-ANALYSIS-ASSET-STREAM-FIX`（`/asset` 返回空 `{}`） | ❌ 已有修单 |

证据：`lumen-ui-topic/src/router/menu.ts`（注释「缺页企业发展/维护管理不挂」）· `src/api/enterprise/paths.ts`。

**9–13 是范围缺口，不是缺陷**：Java 侧 `stats/overview/*`、`key-enterprise/*`、`star-enterprise/*`、`shenzhen/*` 端点都在，前端页没建。按 §11.4 属 **C4**（用例/总控错）而非 C1，**不派 bugfix**，另开补页叶。

---

## 3. 无人值守规则（违反才停）

1. **监管已授权**：`supervised_by=human:淮政玮`，`claim_type=coordinator_dispatch`，`lock_hours=24`。
2. **已拍板不回问**：前端 `lumen-ui-topic`；Java `gkxlumen-topic-enterprise` + `async-service`；检索 `lumen-topic-py`；算法 `lumen-algo-py/vendor/entan-py`。**不重走 A–D**。
3. **QA 不改业务代码**（规约 §11.1）。coordinator / 分诊助手同样无提交权（§11.5.1）。
4. **期望未发生必红**（§11.3）：§4 表里期望没发生 → FAIL。空态只有写进该行才算过。禁止用「诚实降级」改判 PASS。
5. **红了先分类**（§11.4）C1–C6，再决定派不派修。并列取更停：C5 > C6 > C4 > C2 > C1。
6. **结构歧义**（新表/改主键/新 ES）：`blocked` + 升级 `human:李伟`；其余条目继续。
7. **禁止无闸门写正式 `gkxlumenx_*`**；联调只用 `demo_gkxlumenx_*`。
8. **D12**：前端不得打到 `demo-*`。e2e 必须带 `demo-*` 请求守卫（照 `chain-gold.spec.ts`）。
9. git：`origin/dev`；禁止 force；commit `[agent:<role>]`。每叶 handoff + `ponytail:` + cost 四字段。
10. 签收 `ready_to_sign→done` 可积压，不插主链。

---

## 4. 段 E1 · 企业金路径（8 条 · 只点已发布 URL）

> 规约 §11.3。禁止 localhost / `pnpm dev`。登录照 `chain-gold.spec.ts`：先 `goto /login` 点「登录」（mockLogin），再进业务页。  
> **`[待确认]` = 授权人尚未定稿的期望原文，跑之前必须定。**

| # | 模块 / 故事 | 已发布路由 | 期望（未发生=红） | 允许的空态（未写=不允许） |
|---|------------|-----------|-------------------|---------------------------|
| 1 | `SEARCH` | `/enterprise/enterprise-search` | 输入关键词触发 `POST /enterprise/topic/v1/search/query`，结果区出记录；可勾选加入对比篮 | 关键词无命中时可诚实空态（可见空态，非 5xx） |
| 2 | `PROFILE` | 从 #1 结果进 `/enterprise/{orgId}` | 画像页拉到 `profile/basic` + `profile/risk/summary`，基础信息区非空 | 风险摘要可空；**基础信息为空 = 红** |
| 3 | `COMPARE` | 对比篮浮层 → 对比 | 篮内 ≥2 家可发起对比并出对比结果 | **[待确认]** 整页路由 `enterprise-compare` 未注册：若期望含"整页可直达"则本条必红（C4 范围缺口）；若只认浮层对比则浮层出结果即过 |
| 4 | `KEYENT` | `/enterprise/key-enterprise-analysis?workspace=type` 与 `?workspace=domain` | 两个 workspace 各自出 KPI 与列表；侧栏高亮跟随 workspace 切换 | 单个维度无数可诚实空；**两个都空 = 红** |
| 5 | `EVAL` | `/enterprise/evaluation?workspace=technology` | **[待确认]** 发起评估任务 → 过程态 → succeeded 后取结果。是否照 CHAIN 要求「必须点『查看结果』才展示、禁止自动跳」需授权人定 | **无。** 任务 failed / 未 succeeded ≠ 空态 |
| 6 | `SZSTATUS` | `/enterprise/shenzhen-enterprise-status-analysis` | 拉 `sz-status/chain-kpi` + `enterprise-list`，KPI 区出数 | 城市对标 `city-benchmark` 可空 |
| 7 | `RECRUIT` | `/enterprise/attraction?workspace=attraction` 与 `?workspace=cultivation` | 招引/培育两 tab 各出推荐列表 | 无候选可诚实空；**接口 5xx = 红** |
| 8 | `RISK` | `/enterprise/risk?workspace=supply-chain` 与 `?workspace=pain-points` | 供应链关系与痛难点两 tab 各自渲染，不串页 | 图谱无边可空；**tab 切换串页 = 红** |

**全条目通用红线**（任一命中即不过，不受上表空态豁免）：HTTP 5xx · 打到 `demo-*`（破 D12）· 白屏 / 错跳 · 侧栏权限码导致整组不可见。

P1 不挡闭环：`search-biz` 收藏/历史写侧 · `filter-template` 模板 CRUD · `EXPORT` 资产下载（已有修单）· 画像 19 个风险细分子接口逐个核对。

---

## 5. 已知缺口（不进 E1，直接登记）

| 缺口 | 类别 | 处置 |
|------|------|------|
| 企业发展组 4 页未建（`OVERVIEW-E32` / `KEYPANO` / `STAR` / `SHENZHEN`） | C4 范围缺口 | Java 端点已就绪，另开前端补页叶；**不派 bugfix** |
| `OPS` 维护管理未建 | C4 范围缺口 | 同上；产业链/服务链已有可参照 |
| `COMPARE` 整页路由未注册 | C4 范围缺口 | 组件在，`menu.ts` 未注册 `enterprise-compare`；一行路由的事，可并入补页叶 |
| `EXPORT` `/asset` 返回空 `{}` | C1 已立单 | `ENT-JAVA-ANALYSIS-ASSET-STREAM-FIX`（`ready`，`api-agent`） |
| 14 模块中 13 个门3 DG 未闭合 | 定义债 | 与实现验收解耦；PDR 归 `E-ENT-SCRUM-PDR` 主线，不挡 E |
| ENT USM 未标「实施权威」 | 定义债 | CHAIN 有该标注；企业若要转「一故事一叶」需先补 |

---

## 6. 段 E 两叶

| 叶 | ID | agent | 干什么 |
|----|----|-------|--------|
| E0 发布门 | `LUMEN-ENT-E-DEVOPS-L01` | `devops-agent` | 点名服务 K8s dev rollout 健康 + 已发布 URL 可达 + D12 不指 `demo-*` |
| E1 冒烟 | `LUMEN-ENT-E-QA-SMOKE-L01` | `qa-agent` | §4 八条金路径；FAIL 必附 `X-Trace-Id` + Tempo；QA 不改代码 |

**E0 点名服务**（未绿则 E1 不开工）：

- 前端 `gkx-lumen-topic`
- Java `gkxlumen-topic-enterprise-biz` · `gkxlumen-topic-async-service`
- Python `gkxlumen-platform-search-py`（检索）· `gkxlumen-entan-py-api`（算法）
- 网关 `gkxlumen-platform-gateway`

**E1 执行方式**：首轮建议 `e2e/ent-gold.spec.ts`（照 `chain-gold.spec.ts` 架子，含 D12 守卫），跑通后再决定是否进 GitLab `e2e` stage。**本轮尚未授权建 spec**——等 §4 期望定稿。

C1 之后按 §11.5.2：点名 deploy 绿 = E0，随后复测只跑失败条目。禁止等聊天「已经滚了」、禁止等黄敬洲领取（§11.5.3）。

---

## 7. 变更记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-08-21 | 立基线体检版：段位现状 + 14 模块矩阵 + 8 条金路径草案（3 处待确认）+ E0/E1 两叶 |
