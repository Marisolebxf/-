# PORTAL-POL · 政策扶持长任务总控

> **日期**：2026-10-24  
> **授权**：`human:淮政玮`（本管线监管人；后续认领 **不必再问**）  
> **目标**：政策扶持从计算、Java 读接口到门户页和运维可视化全部接通。十条出数、力度排名、最新政策时间线都走正式链。  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)  
> **执行 agent 按本文件已拍板项继续**，禁止把「等用户」当默认阻塞。

| 段 | 仓 | 分支 | 任务 | 状态门 |
|----|-----|------|------|--------|
| A | `gkx-orchestration` | `origin/dev` | `SYSINT-POL-ADS-REQ-L01` | 2026-10-24 已开工。只写需求，不加工 |
| A2 | `gkx-orchestration` | `origin/dev` | `SYSINT-06-17-L01` | 无派单包。有包且执行结果回传后再算灌通。不挡 B/C/D |
| B1 | `lumen-algo-py` | `origin/dev` | `ALGO-LIB-POL-PORTAL-LUMEN-L01` | 不依赖 `SYSINT-ADS-02-L01`。2026-10-24 淮政玮确认可并行开工 |
| B2 | `lumen-algo-py` | `origin/dev` | `SYSINT-03-04B-L01` | 2026-10-24 已到 integration。排名只用 `M_POLICY_INTENSITY_SCORE`，十条保留 |
| C1 | `lumen-svc-platform` | `origin/dev` | `SYSINT-03-04C-L01` | `LUMEN-POLICY-C-SEARCH-FILTER-L01` 已 done。2026-10-24 开工。本叶不调 Python |
| C2 | `lumen-svc-platform` | `origin/dev` | `SYSINT-04-05-API-L01` | 2026-10-24 已到 integration。`GET /topic/v1/policy/portal` |
| D1 | `lumen-ui-topic` | `origin/dev` | `SYSINT-04-05-L01` | 政策查询两张单已 done。仍等 C2 ≥ `integration`。不要与 D2 同时改这个仓 |
| D2 | `lumen-ui-topic` | `origin/dev` | `SYSINT-03-08-L01` | D1 有 handoff 且 ≥ `integration`。不要与 D1 同时改这个仓 |
| D3 | `lumen-ui-algo-apiview` | `origin/dev` | `ALGO-LIB-POL-APIVIEW-PORTAL-L01` | B1 ≥ `integration`。与 D1/D2 不同仓，可以并行 |
| E | devops + qa | K8s `dev` | 本文件 §4 | D1、D2、D3 都 ≥ `pending_test` 后一次冒烟 |

调用链：页面 → Java `GET /topic/v1/policy/indicators` 与时间线读接口 → `lumen-algo-py` `/internal/*`。禁止调用 `demo-*`。Java 不写算法。

厚包：[`派单说明-政策扶持闭环.md`](../../工程过程/04-系统集成/03-专题系统集成/派单说明-政策扶持闭环.md) 里与本文件冲突的「十条返回空」作废，以本文件和注册表完成标准为准。金路径见 §4。

---

## 1. 无人值守规则（违反才停）

1. **监管已授权**：`supervised_by=human:淮政玮`，`claim_type=coordinator_dispatch`。升 ready 后直接认领开工。  
2. **已拍板不回问**：仓、`origin/dev`、上面的调用链、废作清单、菜单挂点。  
3. **QC / 甲方 🟡**：源表没有行就空态并写原因，不停工等纪要。QPOL-02 不在本管线拍板。相近指标不填进十条。  
4. **结构歧义**：`blocked` + 升级 `human:李伟`；同段其它叶继续。  
5. **缺数据**：不无闸门写正式库。读空则空态。mock 必须能关掉。`USE_MOCK` 关闭时页面不写 fixture。  
6. git：lumen 只推 `origin/dev`；禁止 force；commit `[agent:<role>]`。  
7. 每叶 handoff + `ponytail: full` + cost 四字段。`ready_to_sign→done` 可积压，不挡下一叶。  
8. **段 E**：不逐叶派 QA。D 之后 E0→E1。QA 不改代码。期望未发生必红。

锁：`lock_hours=24`。lease 过期则同一监管人续领，不改设计。

同仓同时只派一张 coding 单：`lumen-svc-platform`、`lumen-ui-topic`。`lumen-ui-algo-apiview` 单独排队。`lumen-algo-py` 上 `SYSINT-ADS-02-L01` 不挡 `ALGO-LIB-POL-PORTAL-LUMEN-L01`（2026-10-24 淮政玮：本单不依赖 ADS-02，可以跑）。两单不改同一批文件。

---

## 2. 依赖（联调闸门，见规约 §6）

```text
A  SYSINT-POL-ADS-REQ-L01（需求，不挡编码）
A2 SYSINT-06-17-L01（无派单包，不挡编码）

B1 ALGO-LIB-POL-PORTAL-LUMEN-L01（不等 ADS-02）
  → B2 SYSINT-03-04B-L01

LUMEN-POLICY-C-SEARCH-FILTER-L01 已 done（2026-10-24）
  → C1 SYSINT-03-04C-L01

B2 + C1
  → C2 SYSINT-04-05-API-L01

LUMEN-POLICY-D-POL-01-L01 与 LUMEN-POLICY-D-POL-01C-FILTER-L01 已 done（2026-10-24）
  且 C2
  → D1 SYSINT-04-05-L01（【门】-政策扶持）
  → D2 SYSINT-03-08-L01（【管】-政策新闻展示）

B1 → D3 ALGO-LIB-POL-APIVIEW-PORTAL-L01
D1 + D2 + D3 ≥ pending_test → E
```

解锁看前序 handoff 且状态 ≥ `integration`，不等签收。

数据叶 `SYSINT-06-17-L01`、`SYSINT-POL-ADS-REQ-L01` 不阻塞本管线。它们完成前，接口允许可关闭的 mock；源表没有行就空态。

废作（不要派、不要当依赖）：

- `ALGO-LIB-POL-APIVIEW-ALIGN-L01`（完成标准仍要求十条为空，已阻塞）
- `SYSINT-06-03-L01`（不写 ADS，不含国内政策）
- 任何 `demo-algo-ent-analysis` / `demo-ui-system-test` 调用
- 【管】-政策新闻内容管理。契约没有 CMS 字段，本管线不单开

`SYSINT-SCHEME-04-L01` 仍是 `in_progress`，不阻塞本管线编码。

---

## 3. 开工顺序

1. 算法仓让出后领 B1，再领 B2。  
2. Java 仓让出后领 C1，B2 与 C1 都到联调闸门再领 C2。  
3. 专题前端仓让出且 C2 到联调闸门后，只领 D1，再领 D2。D3 在 B1 到联调闸门后另仓并行。  
4. D1、D2、D3 都到 `pending_test` → **E0** 发布 → **E1** 金路径。红则按规约 §11.4 分类，C1 才派修。

卡住只允许：真环境不通、正式库误写风险、结构升级项、E 超 3 轮 / cost 硬闸。

---

## 4. 金路径（段 E1）

> 期望未发生必红。空态只有写进本行才算过。

| # | 已发布路由 | 期望（未发生=红） | 允许的空态 |
|---|------------|-------------------|------------|
| 1 | 侧栏【门】-政策扶持 | 页上有概况、地图、覆盖、排名、最新政策、深圳对比六块 | 无 |
| 2 | 同上，十条 | 每条要么有数和序列，要么显示该条原因。响应里的 key 是 portal_gaps 的十条，不是相近 metric_id | 源表无行时该条为空并有原因 |
| 3 | 同上，排名 | 省、市排名来自 `M_POLICY_INTENSITY_SCORE` | 评分表无行时排名为空 |
| 4 | 同上，最新政策与深圳最新政策 | 有记录时只含 policy_id、title、publish_time、region_name、source_url；深圳记录地区含深圳 | 无记录时是空列表 |
| 5 | 侧栏【管】-政策新闻展示 | 与门户页不是同一页，读的是同一个 Java 接口 | 与第 2–4 行相同 |
| 6 | 算法库联调台政策扶持十条 | 十条名称以「政策扶持-」开头，与 Java `kind=all` 的 portal_gaps 一致 | 与第 2 行相同 |

P1 不挡闭环：`SYSINT-04-06-L01` 门户菜单登记、`SYSINT-06-17-L01` 国内政策进 ADS、【管】-政策新闻内容管理。
