# ENT-METRIC-LANDING-DECIDE-L01 · 企业域三方结论落到指标注册表

> 格式参考 `templates/handoff-template.md`。定义叶；**不写业务仓代码**。口头「按草案落库」（2026-08-25 16:30）后按决策包 §5 白名单直改 ENT seed / 矩阵。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:徐滕强` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 企业模块架构师 lead 本机裁决并落库 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义·注册表落地；不以缩 YAML 为目标。D9 四维就绪度按裁决改 D3，不跳过 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 定义裁决；本叶不压缩会签原文 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 未改调用链 / 存储流图 |
| 会签态 | **会签通过**（`human:徐滕强` 口头 2026-08-25 18:51「可以」） |
| 说明 | 注册表字段落地，无 Mermaid 契约图。公式不在本单，移交 `ENT-SYNTH-METRIC-COVER-P01` |

---

## 范围与实现

对照决策包 `metrics/request/专题系统/ENT-三方结论-注册表落地决策包-20260825.md` §5（六问已齐 + 已签落库）：

- **D1 P-map**：B→D3 `partial`；C→D3 `none`；A 不升 `full`；D4 保持 `mock`。
- **D2**：`TOTAL_COUNT` / `SZ_COUNT` 结论 A；`TOTAL` 维持 `pending_ods`；`SZ_COUNT` `full`→`pending_ods`。本轮不改 formula。
- **D3 六 ID**：`SZ_SCALE_DIST` / `SEARCH_RESULT_COUNT` 不收录；四个王惠短名正名到已有 ID（不新建）；招引/培育并存不合并；额外 37 + 5 `GAP-*` 全部保留、0 retired。
- **D4 seed 仅 `source_tables`**：更名 / 替代 / 只删名；同表去重；`BUSINESS_POWER_SCORE` 补 `dwd_industry_chain_info(节点字典)`。不挂 `dwd_patent`。
- **D5**：3 条 B→`partial`；2 条 C→`none`；改判 A 的现 `full` 维持；漏网 11 条本轮不降。`d3_gap` 前缀 `[ENT-20260822]`。
- **D6**：不改 D2 schema / definition / formula / `algorithm_type`；D4 不升 live；lifecycle 不升 `kit_complete`；🟡 不升 🟢。

注册表原 DoD「本单不改 seed/矩阵 YAML」已被口头「按草案落库」+ 决策包文首授权 supersede。

## 偏离说明

- formula 仍写旧表名（`dwd_org_industry_chain_dtl` / `dwd_org_tag_info` / `dwd_company_honor_tags` 等），与 `source_tables` 暂时不一致——D6 冻结 formula，**会签确认本批不做**，移交 `ENT-SYNTH-METRIC-COVER-STAT-L01`（137 Wave1，与其余 STAT 一次改，避免单独开 L01 公式叶）。
- `M_ENT_PATENT_TOTAL` 的 `source_tables` 删掉不存在的 `dwd_org_rd_achiev_info` 后只留逻辑字段 `dwd.enterprise.patent_grant_count`（不换挂 `dwd_patent`）。
- `M_ENT_GROWTH_POTENTIAL` 第二条专利 ODS 整项删除（原只绑 `rd_achiev`）。
- 代签栏空置：口径正文未代王惠改 definition；formula/`algorithm_type` 未代唐绍祖改。

## 修改内容

### seed `source_tables`（26 条）

| 动作 | 旧名 | 新名 / 处理 |
|------|------|-------------|
| 更名 | `dwd_org_reg_info` | `dwd_org_base_info` |
| 更名 | `dwd_org_tag_info` / `dwd_company_honor_tags` | `dwd_org_tech_tag`（去重） |
| 更名 | `dwd_company_industry_tags` | `dwd_org_industry_tags` |
| 替代 | `dwd_org_industry_chain_dtl` | `dwd_org_industry_tags` |
| 替代 | `dwd_org_industry_chain_prod_dtl` | `dwd_org_industry_product_tags` |
| 替代 | `dwd_company_location_tags` | `dwd_org_base_info`（与 reg_info 并入后去重） |
| 只删名 | `dwd_org_industry_chain_pat_dtl` | 不换表 |
| 只删名 | `dwd_org_rd_achiev_info` | 不换表 |

`source_tables` 行旧名清零。`formula` / `source_systems` / `db_verified` 未改。

### 矩阵 D3（6 条）

| metric_id | D3 原 | D3 现 |
|-----------|-------|-------|
| `M_ENT_RD_INVESTMENT_RATIO` | full | **partial** |
| `M_ENT_PAINPOINT_SEVERITY` | full | **partial** |
| `M_ENT_KEY_NODE_COUNT` | full | **partial** |
| `M_ENT_INDUSTRY_MATCH_SCORE` | full | **none** |
| `M_ENT_SUPPLY_CHAIN_RISK` | full | **none** |
| `M_ENT_SZ_COUNT` | full | **pending_ods** |

未动：`TOTAL_COUNT`/`NEW_COUNT_Y` 仍 `pending_ods`；`HIGH_TECH_COUNT`/`PATENT_TOTAL`/`CHAIN_COMPLETENESS`/`GROWTH_POTENTIAL` 等改判 A 维持 `full`；漏网 11（`DEV_HISTORY`、`SZ_CHAIN_POSITION`、STAR×4、KEYPANO 四兄弟）维持 `full`。D4 全部仍 `mock`。

## 测试结果

- `loadCatalog`：ENT seed `parsed=79` = `declared_total`。
- `getMetric` 抽样：上表 6 条 D3 与 `SZ_COUNT`/`TOTAL_COUNT`/`HIGH_TECH_COUNT` 一致；D4=`mock`。
- `node scripts/metric-mcp-selfcheck.mjs`：catalog / join / query 断言通过；`metric-progress-export` 调 Python 写 xlsx 挂起（`python exit null`），与本叶 YAML 解析无关，未强行覆写进度表。

## 会签补记（2026-08-25 18:18 · live `gkx`）

分析源改为三方入站 **MySQL `gkx` @ `183.240.141.251:3318`** 的 `dwd_*`（只读），不再用项目 `gkxlumenx_dwd` 或 08-22 纸面行数当「能不能算」真源。

**A/B/C 尺子（`human:徐滕强` 锁定，后续 137 第一波同用）**

| 类 | 判定 | D3 |
|---|---|---|
| **A** | 结构在；已有行上要用的列有值。主档 `org_id` 对不上、样本少 **仍 A** | 已 `full` 的维持；A 不升 `full` |
| **B** | 结构在，已有行上部分列空。真数灌入后也可能缺字段 | `partial` |
| **C** | 缺表或缺维 | `none` |

live 抽检（`is_deleted=0`）：主表 40,000；深圳 `city='深圳市'` 17,552；高企标签有数但回连主档 85 家；年报资产销售额近满但 `jgid` 对主档 71 家；规范财务营收有数 286、研发金额 0；专利申请人名对主档 14 家。旧名 `reg_info` / `tag_info` / `chain_dtl` 等已不在本库。

**本轮 YAML 不再改。** 回连稀疏不是算错：`HIGH_TECH_COUNT` / `PATENT_*` / `REVENUE_*` / `PROFIT_MARGIN` 维持 D3=`full`（A）。`RD_INVESTMENT_RATIO` 维持 `partial`（年报 `yftrje` / 财务 `arch_development_am` 空）。`INDUSTRY_MATCH_SCORE` / `SUPPLY_CHAIN_RISK` 维持 `none`。D4 全部 `mock`。A ≠ live。

开放（不挡本叶会签）：`CHAIN_COMPLETENESS` 的 `industry_link_code` 约 24% 为 `[]`——若把「部分行该列空」算 B，137 第一波再裁；本叶不改。`SZ_COUNT` 公式字段仍开放。

## 遗留风险

- formula ↔ `source_tables` 漂移，**不挡本单会签**；移交 `ENT-SYNTH-METRIC-COVER-STAT-L01`（唐绍祖公式会签，与 137 Wave1 一次改）。
- `chain_score` / `node_stage` 仍写在部分 `source_tables` 字段后缀上（本单只改表名）；D3 不因此升 full。
- `SZ_COUNT` 产品侧 `region_id=440300` vs formula `headquarters_city` 仍开放；live 主表无 `region_id`，深圳用 `city`。
- 招引/培育四 ID 并存，等 Q015。
- C10 供应链边表未裁；`SUPPLY_CHAIN_RISK` D3=`none`。
- GDF-ENT-WORKPACK-v2.1 仍暂缓对外投递。
- 高企/年报/专利与主档 `org_id` 几乎不重叠：标 A 只表示结构可算，灌齐同一批 ID 之前不能当 4 万家真数。

## 产物清单

| 产物 | 路径 |
|------|------|
| 决策包（§5 已签落库） | `metrics/request/专题系统/ENT-三方结论-注册表落地决策包-20260825.md` |
| ENT seed | `metrics/registry/cfg_metric-ENT-seed.yaml` |
| ENT 矩阵 | `metrics/registry/metric-readiness-matrix-ENT.yaml` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/ENT-METRIC-LANDING-DECIDE-L01.md` |

## 验收证据

- 口头「按草案落库」2026-08-25 16:30；决策包签字栏已改为已签落库。
- seed `source_tables` 无 `dwd_org_reg_info` / `dwd_org_tag_info` / `dwd_company_honor_tags` / `dwd_company_industry_tags` / `dwd_org_industry_chain_dtl` / `dwd_org_industry_chain_prod_dtl` / `dwd_org_industry_chain_pat_dtl` / `dwd_company_location_tags` / `dwd_org_rd_achiev_info`。
- 会签补记（live `gkx` + ABC 锁定）：本文件「会签补记」节；决策包 §5 增一行。
- 会签通过后推 `origin/dev`（handoff + 决策包 + registry `ready_to_sign`），待 `human:淮政玮` 签收。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 算法 |
| 调用链 | ✅ 未改业务调用链 |
| 图谱 Nebula | ✅ 未引入 Neo4j |
| 可观测 | ✅ N/A（定义叶） |
| CI/CD | ✅ `cicd: skip`（编排仓注册表，无业务 CI） |
| D12 demo/lumen | ✅ 未改业务仓、未 merge demo→lumen |
| 方案 A / ADS | ✅ 表名对齐 Excel 承诺 DWD，Java 仍只读 ADS |
| D8/D10 | ✅ N/A（无前端页） |
| D9 8 件套 / 四维 | ✅ 只改白名单字段；D1 定义正文未伪齐；D3 按锁定尺子：样本少仍 A，列空才 B，缺维才 C |

## CI/CD（必填）

- 分支：`origin/dev`
- commit：会签通过包（handoff + 决策包 + registry）；YAML 落库仍为 `63f9b481`
- pipeline URL / ID：`cicd: skip`
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL：N/A（定义叶）

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- traceId：N/A
- Tempo / Loki：无

## Cost（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 220000 |
| model_used | grok-4.6 |
| actual_cost | 1.80 |
| cost_warn | green |

## 下一步

- **会签通过**（2026-08-25 18:51 `human:徐滕强`）：本单范围 = D1–D6 裁决 + seed `source_tables` + 矩阵 6 条 D3。公式 / 24 条 MODEL·GRAPH live 重裁 / 137 其余指标 **不在本单**。
- 状态：`integration` → `ready_to_sign`。`done` 只等 `human:淮政玮` 签收。
- 移交：`ENT-SYNTH-METRIC-COVER-P01`（137 覆盖父单）+ `ENT-SYNTH-METRIC-COVER-STAT-L01`（Wave1 STAT/COMPUTE：一次过完 live ABC + formula 跟表；L01 已过的 30 条 STAT 不重裁 ABC，只补公式漂移）。
- 会签后可用 `gkx-metric-progress` 刷进度表（不挡签收）。
- 会签材料已按 `human:徐滕强` 要求推 `origin/dev`，待 `human:淮政玮` 签收。
