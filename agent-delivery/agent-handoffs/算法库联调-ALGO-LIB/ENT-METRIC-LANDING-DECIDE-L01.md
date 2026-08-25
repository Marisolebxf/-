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
| 会签态 | N/A |
| 说明 | 注册表字段落地，无 Mermaid 契约图 |

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

- formula 仍写旧表名（`dwd_org_industry_chain_dtl` / `dwd_org_tag_info` / `dwd_company_honor_tags` 等），与 `source_tables` 暂时不一致——D6 冻结 formula，handoff 记漂移，不改公式。
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

## 遗留风险

- formula ↔ `source_tables` 漂移，需后续 formula 会签叶（唐绍祖）一起改。
- `chain_score` / `node_stage` 仍写在部分 `source_tables` 字段后缀上（本单只改表名）；D3 不因此升 full。
- `SZ_COUNT` 产品侧 `region_id=440300` vs formula `headquarters_city` 仍开放。
- 招引/培育四 ID 并存，等 Q015。
- C10 供应链边表未裁；`SUPPLY_CHAIN_RISK` D3=`none`。
- GDF-ENT-WORKPACK-v2.1 仍暂缓对外投递。

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
- 矩阵 6 条 D3 与 §5 D5 一致；未 🟡→🟢；未 D4→live。
- 未 commit（用户未要求）。

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
| D9 8 件套 / 四维 | ✅ 只改白名单字段；D1 定义正文未伪齐；D3 按 A/B/C 诚实降级 |

## CI/CD（必填）

- 分支：`dev`（未 push）
- commit：无（用户未要求提交）
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

- 定义叶进入 **integration（会签中）**：口径/formula 未改，代签栏空置，**不写会签通过**。
- formula 会签 / `SZ_COUNT` 区划字段 / Q015 招引培育合并，另开叶。
- 需要 commit 时由 `human:徐滕强` 明示后再提交 `origin/dev`。
