# 产业服务链（SVC）· 底座后全量长任务总控（草案）

> **状态**：已授权 · `human:侯佳伟`（2026-08-18 聊天确认拍板并开工）  
> **日期**：2026-08-18  
> **目标站**：http://111.198.38.90:50892/（`lumen-ui-topic`）  
> **对标原型**：`demo-ui-topic` service-portal / service-center；算法台参考 http://111.198.38.90:50100  
> **前置结论**：上一轮 A–E 只打通链路；本轮 **先底座（Gate-0）再全量（Gate-1）**，中间不断档  
> **铁律**：只写 `demo_gkxlumenx_*`；调用链 FE→Java→Python；D12 禁 demo-*；Q-SVC-010 待核验不伪闭合

---

## 0. 一句话策略

**以 `storage/SVC` 契约表为唯一真源 → 50100（`svcseed`）按临时规则从 Demo ODS 抽取并灌满契约 → 50892 按原型补齐读面与交互。**  
禁止再手抄原型 24 家当主路径；禁止 50100 旧表与契约双真源长期并存。

---

## 1. 为什么这样切（避免长任务中断）

| 风险 | 若不先底座 | Gate-0 先做完 |
|------|------------|---------------|
| 表双轨 | FE/算法各改各的，联调反复空 | 只认契约表 |
| 口径未定 | 做到一半卡 Q-SVC-010 | 临时基线已签字 |
| 门户无数 | 视觉做完仍空壳 | L2 聚合已有数 |
| 50100 与 50892 对不上 | 灌了算法台专题仍空 | 同一流水线写同一套表 |

**硬闸门**：Gate-0 DoD 全绿之前，**不开** Gate-1 全量编码长任务。

> **Gate-0 进度（2026-08-18）**：叶 `DEMO-SVC-BASE-GATE0-L01` **外网已绿**（search-py `9b86f81` / deploy **22686**；overview trend×8 + scale×4；search total=35 + 卡面字段）。任务 `ready_to_sign`。**Gate-1 已开**：见 `DEMO-SVC-GATE1-全量派单.md`。

---

## 2. Gate-0 · 底座（必须先完工）

### 2.1 临时拍板包（人审 · 半天内签）

写入 `客户决策清单` 升 🟡 项目基线（上线前再换甲方 🟢）：

| ID | 临时默认（建议文案） |
|----|----------------------|
| Q-SVC-010 | Demo 准入 = 读 `demo_gkxlumenx_ods.dwd_org_base_info`，`business_scope`（及可用字段）**关键词词典**圈定；一律 `pending_client_confirm`；正式准入等供方 |
| Q-SVC-008 | Demo 类型展示优先 **企业/高校/科研院所**（贴原型）；六类工业标签有则打 type_tag，无则空 |
| Q-SVCCHAIN-06 | 门户全球/区域等聚合：**可由圈定池确定性聚合**；池过小不足以撑图时，允许 **同规则缩放因子** 写 series（标 mock+GAP，禁止无来源乱数） |
| Q060 / Q-SVCCHAIN-01 | 技术力 = 五维等权归一（演示） |
| Q061 / 短板 | 阈值沿用设计说明临时默认 |
| 产业级联 | 复用政策门户产业树 → `field-*` |

**授权句模板**：「按本拍板包执行 Gate-0；通过后开 Gate-1 全量，后续认领不必再问。」

### 2.2 契约表补齐（Demo DDL）

以 `storage/SVC/stores/mysql/ads.md` + `dwd-svc.md` 为准，**补建缺失表**（现网已有 profile/ranking/service_org*）：

| 表 | 用途（顶 50100 / 门户） |
|----|-------------------------|
| `svc_metric_fact` | KPI 单点 |
| `svc_metric_series` | 历年趋势 / 新增 |
| `svc_metric_dist` | 类型、规模四档、产业分桶 |
| `svc_region_dist` | 全球/省/市/深圳十区 |
| `svc_tech_power_score` | 六类/能力榜 |
| `svc_chain_gap_score` | 短板分析 |

DWD 保持：`service_org`（含 `service_org_code`）、type_tag、chain_rel、org_rel、financing。  
**废弃为非真源**（可旁路保留）：`dwd_service_org`、`svc_industry_layout`、`svc_global_dist`、`svc_invest_stat`、`svc_new_org_stat`、`svc_sz_*`（过渡期可视图映射，Gate-0 结束标 deprecated）。

### 2.3 重写 50100 灌数主链（`demo-algo-ent-analysis`）

改造 `entan/svcseed.py` + `/internal/svc/run-pipeline`：

```text
demo ODS dwd_org_base_info
  → 临时规则圈定（待核验）
  → DWD service_org* 
  → ADS profile / metric_* / region / tech_power / chain_gap / ranking
```

硬性要求：

1. `connect(plane="svc")`，只写 `demo_*`  
2. **禁止**随机 `_orgs()` 作为主路径  
3. `/v1/svc/indicators` 改为读契约表（或兼容视图）  
4. 一键灌数后：50100 基础指标有数 **且** 50892 overview/search 可读同一批  

### 2.4 Gate-0 DoD（全绿才放行 Gate-1）

- [ ] 临时拍板包已签字进跟踪表  
- [ ] Demo 契约缺表已 CREATE  
- [ ] `run-pipeline` replace 成功；`service_org` / `svc_org_profile_card` ≥ 约定下限（建议 ≥50 或词典命中全量）  
- [ ] `svc_metric_series` / `dist` / `region_dist` 关键 kind 非空  
- [ ] 外网：`POST …/service-portal/overview` 返回 trend + scale_dist + by_type（或等价 sections）  
- [ ] 外网：`POST …/search/orgs` total 与池一致；卡面字段齐  
- [ ] 50100 status 与 50892 抽样 org 可对上（同一 `service_org_code` / `org_id`）  
- [ ] handoff：`DEMO-SVC-BASE-GATE0-L01`  

---

## 3. Gate-1 · 全量长任务（50892 对齐原型）

> 仅当 Gate-0 DoD 全绿。目标：**原型功能有数可点**，不是再打空壳链路。

### 3.1 范围地图（原型 → 50892）

| 原型能力 | 50892 路由 | 数据依赖 | 交付要点 |
|----------|------------|----------|----------|
| 专题·概况 | `/service-portal/overview` | fact/series/dist | 产业**级联**；趋势；类型环；**人员规模四档** |
| 专题·产业分布 | `…/industry-distribution` | dist / chain | 环节分布 + 热力 |
| 专题·区域分布 | `…/region-map` | region_dist | 地图/排行 |
| 专题·技术能力 | `…/capability-rank` | tech_power + ranking | 榜单有数 |
| 专题·深圳 | `…/shenzhen` | region + series | 趋势/区分布/重点机构 |
| 机构查询 | `/service-center/search` | profile | 已有基础 → 字段/筛选贴原型 |
| 机构分析（覆盖/趋势/能力） | institution-judgment | profile + series + Job | 三 workspace 有演示结果 |
| 服务链生态/短板 | chain 工作区 | chain_gap + 关系 | Job 白名单扩；结果可读 |
| 招引/培育 | recommend | ranking | 名单+理由 |
| 运维壳 | maintenance | — | 按原型保留 |

### 3.2 建议叶拆分（可并行仓、同依赖闸门）

| 段 | 叶（建议 ID） | 仓 | 一句话 |
|----|---------------|-----|--------|
| A0 | `DEMO-SVC-BASE-GATE0-L01` | demo-algo-ent-analysis + orchestration | 拍板+DDL+svcseed 契约灌数 |
| B | `DEMO-SVC-PY-PORTAL-AGG-L01` | lumen-topic-py | overview 扩展 sections；indicators 契约读 |
| C | `LUMEN-SVC-JAVA-PORTAL-EXT-L01` | lumen-svc-platform | Feign/门面透传扩展字段（若需新 path） |
| D1 | `LUMEN-SVC-FE-PORTAL-FULL-L01` | lumen-ui-topic | 五 Tab + 产业级联 + 有数图表 |
| D2 | `LUMEN-SVC-FE-ANALYSIS-FULL-L01` | lumen-ui-topic | 分析/生态/招引有数（非空壳） |
| C2 | `LUMEN-SVC-JAVA-JOB-WHITELIST-L01` | lumen-svc-platform | Job 白名单按页扩 |
| B2 | `DEMO-SVC-PY-SVCAN-MODELS-L01` | lumen-algo-py | 短板/技术力等读 ADS 出结果 |
| E | `LUMEN-SVC-E-FULL-SMOKE-L01` | devops+qa | 金路径「有数」验收 |

### 3.3 金路径（Gate-1 · 有数才绿）

| # | 路由 | 期望（未发生=红） |
|---|------|-------------------|
| 1 | overview | 级联可选；趋势≥2 点；类型环；规模四档 |
| 2 | industry / region / shenzhen | 主图有数，不假空 |
| 3 | search | 列表≥池下限；卡面含 segment/patents 等 |
| 4 | 分析三视图 | 配置可点；结果区有演示输出或明确 Job 态 |
| 5 | 短板或招引 | 终态可解释（成功结果或诚实拦截+原因） |

允许 🧪⚠️ + Q-SVC-010；**不允许**「只有壳没有数」宣称完成。

---

## 4. 中间不断档的执行纪律

1. Gate-0 未绿 → coordinator **拒派** Gate-1 叶。  
2. 口径再争议 → 只追加跟踪表 🟡，**不回滚**已灌契约结构。  
3. 50100 过渡：优先硬切 indicators 读契约；若怕空窗最多双写 **1 个迭代**。  
4. 禁止第三套表；禁止前端私藏 Mock 当真源。  
5. 每叶 handoff + cost；lumen push `origin/dev`。

---

## 5. 执行动作（已授权）

1. ✅ 监管人确认 §2.1 拍板包 → 本文件「已授权」。  
2. ✅ 建叶 `DEMO-SVC-BASE-GATE0-L01` 并开工。  
3. Gate-0 绿后，一次性建齐 Gate-1 叶并连夜跑。

---

## 6. 授权栏

> **授权**：`human:侯佳伟`  
> **日期**：2026-08-18  
> **授权句**：按本总控执行；Gate-0 通过后开 Gate-1；后续认领不必再问。

