# SITUATION-IM · 总派单（厚包）

> 上位文件：[`SITUATION-IM-长任务总控.md`](./SITUATION-IM-长任务总控.md)（裁定 U1–U12、边界铁律、无人值守规则以总控为准）
> 契约真源：[`SITUATION-IM-API-CONTRACT-01.md`](./SITUATION-IM-API-CONTRACT-01.md)
> 前置条件与未决项：[`SITUATION-IM-前置条件与未决项.md`](./SITUATION-IM-前置条件与未决项.md)
> 日期：2026-10-28 · 模式：长任务（coordinator_dispatch，lock 24h）· 授权人 `human:李伟`

---

## 1. 铁律（每叶 `/goal` 必须粘贴）

1. **UI 与实现效果零改动**：`views/situation/**` 的视图结构 / 组件层级 / 布局 / 样式 / `styles/*.css` / Arco 用法一律不动。可动面 = 契约 + 接线层（`api` / `types` / `models` / `stores`）+ 评审层（`review` / `lineage`）+ **角标挂载点**（须满足总控 §0.1 三条，否则判为效果改动退回）。
2. **契约单真源**：以 `SITUATION-IM-API-CONTRACT-01.md` 为准；改契约先 bump 版本，再同步 `types/*.ts` 与 mock 种子（`defineApi` 双轨两侧对齐），**禁两处漂移**。
3. **数值序列化**：所有返回数值字段强制 `int` / `double`（防 Jackson 把 Long 转 String，ECharts 画不出曲线）—— 沿用 `SituationController` L384-410 写法。
4. **降级**：Feign **逐块**降级（某下游挂 → 该块空 + `emptyReason`，其余块照常，仍 200）；`@NoToken` 与下游 `@Inner` 必须配对。
5. **诚实性**：读空出空态；`D4=mock` 挂 🧪、`D2=provisional` 带「待核验」（U8）；**禁止把指标就绪度改绿**；禁止用 demo fixture / `Math.random` / `Date.now` 填数。
6. **数据**：只读 `demo_gkxlumenx_*`；**禁止写正式 `gkxlumenx_*`**；（D3）：Java 不写算法、前端不直连 Python。
7. **git**：默认只 commit **不 push**（U11），走查通过后监管人人工推。
8. 每叶 handoff：`agent-handoffs/科技发展态势-IM/{task-id}.md`，含 `ponytail:` + cost 四字段 + 五类内容（改了什么 / 为什么 / 验证了什么·贴实测 / 遗留 / 下叶坑）。每叶**必须回写契约 §7 实装对照表一行**。

---

## 2. 叶清单与 DoD

### A0 · 数据 / 环境 / 指标映射体检叶（无代码）
**范围**：① `gkxlumen-innov` 现有可用 `/internal/*` 端点清单与行数；② `dwd.enterprise_base` / `ads.enterprise_score` / `ads.tech_power` / 两张 dist 表行数与脏值；③ 三页每个 Tab 逐卡片「有源 / 空态」判定 + 行数量级；④ 需新增 SQL / DAO 清单；⑤ **三页每个统计数字 ↔ `metric-readiness-matrix-INNOV.yaml` 的 `metric_id` 逐条映射表**（映射不上的列出来，走 D1 missing 红问号）；⑥ 天地图 key 与内网瓦片可达性（R1）；⑦ 是否触及结构升级项。
**DoD**：体检报告 + innov 端点清单 + metric_id 映射表（作为 C/R 段基线）。**不写任何代码。**

### R0 · 评审底座叶（前端）
**范围**：① `src/review/`（`feature.ts` 总开关 + `index.ts` 唯一出口 + `README.md` 上线清理清单，照 `lumen-ui-topic/src/review/`）；② `src/stores/review.ts`（评审模式 + 组件自闸）；③ 升级 `src/components/lineage/MetricSpecHint.vue`（现只有 4 项元数据、无就绪度区块、不自闸、ⓘ 为文本符号）→ 8 件套 + version + 就绪度四行 + Arco `IconInfoCircle` + **自闸**；`MockBadge.vue` 补自闸；新增 `SchemaGapBadge` / `PendingBadge`（含 `pending_ods` 蓝钟）/ `IngestingBadge` / `ReviewMetricBadges`；④ **readiness 只读镜像**（从 INNOV yaml 生成，**集中单文件**，头注释注明真源路径 + 同步任务号）；⑤ **新建 `科技发展态势-TS/SITUATION-IM-data-gap-catalog.yaml`**（缺口长文案 `pending_hint` 真源，从 INNOV 矩阵的 `d2_gap` / `d3_gap` / `d4_note` 提取 —— **前端禁硬编码**，见前置条件 B4）。
**DoD**：`type-check` 0 / `pnpm build` 通过；**关闭评审模式 DOM 零泄漏**；组件自闸生效；排列合规（数字 → [ⓘ/？] → [结构] → [⚠️/⏰] → [🧪/⟲]，同点最多 3 枚、间距 4px）；`pending_hint` 禁硬编码。

### C1–C5 · M6 深圳 5 端点（pilot，后端）
**顺序**：`carriers` → `indicator-systems` → `field-distribution` → `city-benchmark` → `operation-timeline`
**每叶范围**：一个 REST 路径。仿 `SituationController` 写法：`scopeOf` 唯一入参翻译层 → Feign（element / innov）→ 逐块 catch 降级 → `emptyReason` + `scopeLabel` + `asOf` + `metricIds` → 数值强转 → `R.ok`；**必须写「哪些入参真的生效」诚实声明注释**（照 `SituationController.java:310-324`）。
**DoD**：端点 curl 自测 ≥3 组入参（无筛选 / 有地域 / 有时间范围）+ 数值与库级计数能对上 + 单测（若适用）；`@NoToken`/`@Inner` 配对；回写契约 §7 一行。

### D1 · M6 前端装配接线（前端）
**范围**：① api 层删裸 fetch → `defineApi` 双轨 + `request` + `BASE='/display/v1/situation'`；② 新增 `models/useSzInnovationDataset.ts`，`Promise.allSettled` 逐块拉 + 逐块 catch → 拼回现有 `SzInnovationDataset` 形状；`index.vue` **只改取数那几行**；③ 页级 store（行政区 / 类型 / 领域 / 创新价值），进 watch key；④ types 入出参 + per-block `emptyReason`；⑤ 每区块可见空态。
**DoD**：三绿（`type-check` / 自检 / `pnpm build`）+ 页面实跑 + tabs 与 styles **零 diff**。

### R1 · M6 角标挂载（前端）
按 A0 映射表逐个统计数字挂 `metric_id` + ⓘ/红问号 + 角标；挂不上的列进遗留（**不跳过、不显伪 8 件套**）。DoD：走查清单 §5/§6 两条全绿。

### C6–C10 · M5 湾区 5 端点 / D2 + R2
端点：`achievements` / `capability` / `swot` / `indicators` / `alerts`。DoD 同 pilot。**注意**：M5 菜单名是「湾区创新监测」，但**契约前缀是 `bay-innovation`**，不要改路径去迁就文件名。

### C11–C15 · M4 全球 5 端点 / D3 + R3
端点：`achievements` / `realtime` / `carriers` / `alerts` / `cities`。**写面 deferred**。`realtime` 的 D2 轮询是否实现以 Open Item 结论为准。

---

## 3. `/goal` 头模板（coordinator 派单时填充）

```text
强度：ponytail {按派单}
仓：{lumen-svc-platform | lumen-ui-science-pc} 分支 origin/dev
监管人：human:李伟
必读：agent-delivery/agent-handoffs/科技发展态势-TS/SITUATION-IM-长任务总控.md
契约：agent-delivery/agent-handoffs/科技发展态势-TS/SITUATION-IM-API-CONTRACT-01.md
本叶：{A0|R0|C1..C15|D1..D3|R1..R3} · 范围与 DoD 见 SITUATION-IM-总派单.md §2
git：默认只 commit 不 push（走查通过后监管人人工推）
```

---

## 4. 环境前置（A0 叶核验 / 部分已由 ENT 实测继承）

| 项 | 现状 | 核验方式 |
|----|------|---------|
| 网关 `192.168.88.50:9999` | **不可达**（ENT A0 实测） | 本管线走本地联调，不依赖它 |
| `gkxlumen-display` 7099 local permitAll | ENT 已跑通 | curl `/v1/situation/*` |
| `gkxlumen-element` 7082 | ENT 已跑通（曾僵死已重建） | curl six 端点 |
| **`gkxlumen-innov`** | **未用于态势页；`RemoteInnovClient` 仅 `health()`** | **A0 首要核验项** |
| 真实 token | `VITE_ENABLE_MOCK_AUTH=true` + `USE_MOCK=false` 组合不挂 Bearer | `.env.development:13-17` |
| 前端 dev server | **端口 3000**（非 3600） | `.env.development:3` + `vite.config.ts:37` |
| 库 | `demo_gkxlumenx_*` 只读 | ENT A0 行数基线可复用 |
| 天地图瓦片 | key 已挪 env，内网可达性待确认 | A0 ⑥ |

> **开工前缺口（Part B）与未决拍板项（Part C）见 `SITUATION-IM-前置条件与未决项.md`。**
