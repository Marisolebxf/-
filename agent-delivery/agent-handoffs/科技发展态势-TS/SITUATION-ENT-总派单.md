# SITUATION-ENT · 总派单（厚包）

> 上位文件：[`SITUATION-ENT-长任务总控.md`](./SITUATION-ENT-长任务总控.md)（裁定 U1–U8、边界铁律、无人值守规则以总控为准）  
> 契约真源：[`SITUATION-ENT-API-CONTRACT-01.md`](./SITUATION-ENT-API-CONTRACT-01.md)  
> 日期：2026-10-27 · 模式：长任务（coordinator_dispatch，lock 24h）

---

## 1. 铁律（每叶 /goal 必须粘贴）

1. **UI 零改动**：`lumen-ui-science-pc/src/views/situation/**` 视图结构、组件、`styles/demo-situation.css` 严禁改；只许动 `src/api/`、`src/mock/`、`src/types/`、`views/situation/overview/models/` 数据装配。
2. **契约单真源**：以 `SITUATION-ENT-API-CONTRACT-01.md` 为准；改契约先 bump 契约文档版本，再同步 `types/situation.ts` 与 mock 种子（`defineApi` 双轨两侧对齐），禁两处漂移。
3. **数值序列化**：后端所有序列化数值字段强制 `int`/`double`（防平台 Jackson 把 Long 转 String，ECharts 画不出曲线）——沿用 `SituationController` L384-410 既有写法。
4. **降级**：Feign 分区降级（下游挂仍 200 诚实空 + emptyReason）；`@NoToken` 与下游 `@Inner` 必须配对。
5. **诚实性**：读空出空态；影响力口径为 `enterprise_score` 占位，缺口记 handoff；禁止把指标就绪度改绿。
6. **数据**：只读 `demo_gkxlumenx_*`；禁止写正式 `gkxlumenx_*`。
7. **git**：按总控 §1.6 —— 默认 commit 可做、**严禁 push**，走查通过后监管人人工推。
8. 每叶 handoff：`agent-handoffs/科技发展态势-TS/{task-id}.md`，含 `ponytail:` + cost 四字段。

## 2. 叶清单与 DoD

### A0 · 数据/环境体检叶（无代码）
**范围**：① curl 直连 `gkxlumen-element` 六端点并记录响应；② 核对 `{dwd}.enterprise_base`(189,115) / `{ads}.enterprise_score`(189,115) / `enterprise_domain_dist`(30) / `enterprise_type_dist`(35) 行数与脏值（空坐标、异常注册日期、空名称）；③ 核验网关 `10.50.69.111:30895` 可达与真实 token 获取方式（`ENABLE_MOCK_AUTH` 组合是否可用）；④ 输出体检报告。
**DoD**：体检报告 + 六端点样本响应（作为 C 段联调对照基线）。**不写任何代码。**

### C1 · element 企业端点补强叶（U3 点位）
**范围**：`gkxlumen-element` 新增对象级点位端点：从 `ads.enterprise_score`（join `enterprise_base` 坐标）出 Top-N 高分企业点位（key/objectTypeKey='enterprise'/name/value/level/coordinates/parentRegionKey），脏坐标剔除。契约见契约文档 §3。
**DoD**：端点 curl 自测通过 + 单测 + 数据口径注释（不含 mock 数值）；不建新表（实时查询或复用现有 DAO）。

### C2 · display map/overview 联调叶（U3 接线）
**范围**：`gkxlumen-display` `/v1/situation/map`：objectPoints 从 C1 新端点经 Feign 聚合，移除「objectPoints 恒空 + emptyReason」占位；保留 Feign 降级路径（element 挂 → objectPoints 空 + emptyReason=UNREACHABLE）。`/overview` 不动。
**DoD**：map/overview 联调 curl 对照 A0 基线；降级路径演练记录（停 element 验证仍 200）。

### C3 · influence 端点实现叶（U1/U2）
**范围**：`gkxlumen-display` 新增 `POST /v1/situation/influence`：入参对齐前端现有 `fetchSituationInfluence` 请求体；出参 count/averageScore/items[{name,score,rank,rankScope,regionKey,factorType…}]，数据源 `ads.enterprise_score`（element 侧新增只读查询端点或复用 Feign 聚合）。契约见契约文档 §2。
**DoD**：端点自测 + 单测 + Long→int 自检；口径注释注明「`M_INNOV_ENTERPRISE_INFLUENCE` 正式算法未上线，本端点为 enterprise_score 占位」。

### D1 · 前端契约适配 + Mock 切换叶（U4）
**范围**：① `types/situation.ts` / `src/mock/modules/situation.ts` / `src/api/situation/index.ts` 按契约文档同步（含 influence、objectPoints）；② `.env.development` 切 `VITE_APP_USE_MOCK=false`（.env.production 维持现状，交付物里单独说明切换步骤）；③ 四端点 404 的空态表现走查（错误处理只可在 api 层收敛，不动视图）；④ mock 种子数据保留不删（双轨），禁改种子数值。
**DoD**：三绿（`pnpm type-check` / 自检 / `pnpm build`）+ **`views/situation/**` 与 `styles/demo-situation.css` 的 git diff 为零** + 走查清单 §4 前置自测记录。

## 3. /goal 头模板（coordinator 派单时填充）

```text
强度：ponytail {按派单}
仓：{lumen-svc-platform | lumen-ui-science-pc} 分支 origin/dev
监管人：human:李伟
必读：agent-delivery/agent-handoffs/科技发展态势-TS/SITUATION-ENT-长任务总控.md
契约：agent-delivery/agent-handoffs/科技发展态势-TS/SITUATION-ENT-API-CONTRACT-01.md
本叶：{A0|C1|C2|C3|D1} · 范围与 DoD 见 SITUATION-ENT-总派单.md §2
git：默认只 commit 不 push（走查通过后监管人人工推）
```

## 4. 环境前置（A0 叶核验，当前未确认项）

| 项 | 现状 | 核验方式 |
|----|------|---------|
| 网关 `10.50.69.111:30895` | health 200（2026-10-27 补验） | `GET /display/actuator/health` |
| element/display 服务运行态 | 未实测 | 服务直连 curl 六端点 |
| 真实 token | mock token 给真网关会 424 | PigX 登录或 `ENABLE_MOCK_AUTH=true + USE_MOCK=false` 组合验证 |
| 库连接 | 默认 `demo_gkxlumenx_dwd` | 行数核对 |
| 本地 dev 联调代理 | `.env.development` `VITE_APP_API_URL` + `/api` 代理 | 走查清单前置 |
