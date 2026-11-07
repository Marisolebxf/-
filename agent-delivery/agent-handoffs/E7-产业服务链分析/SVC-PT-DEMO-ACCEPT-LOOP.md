# SVC-PT-DEMO-ACCEPT-LOOP（门户专题服务演示样本反复验收）

- 规程：`agent-delivery/产品实现规程.md` §6.5（只追加，每轮一节，不回写历史节）
- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-PT-合规演示用例.md`（11 行）
- 计划：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/编排计划/SVC-PT-LOOP计划.md`
- 监管人：`human:徐滕强`；执行：`agent:qa-agent`；强度：ponytail full

## 运行 2026-11-07

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-PT-合规演示用例.md`（本日 17:20–17:45 查库节之后无重灌迹象，直接按用例期望）
- 库：只读（入口连接 `demo-gkxlumenx-ods`，目标跨库 `demo_gkxlumenx_ads`；本步连接失败，未读到任何表，零写操作）
- 样本满足：否
- 停止：ENV（只读库 SELECT 连续失败 2 次，即停；未做第 3 次，未探活）

### 四步结果

| 步 | 结果 |
|---|---|
| ① 探测 | ✅ HTTP 200，`code=0`；`POST /tts/svcz/api/enterprise/topic/v1/recommend {"count":1}`（头 `authorization: Bearer <本机 token 文件>` + `systemcode: topic`）返回 `enterprise/topic/v1/recommend` 真实推荐企业结构（`items[0]` 含 org_id / social_credit_code / name_cn / province=广东省 / industry_chain_names_flat=软件与信息服务 等）。token 有效，未打印、未入档。接口映射存在 |
| ② 只读库 | ❌ 失败 2 次即停：第 1 次 information_schema 列名确认查询 ETIMEDOUT（约 6.8s）；第 2 次同查询 `Can't add new command when connection is in closed state`。未触及任何 svc_* 业务表 |
| ③ 接口对照 | ⛔ 未执行（前置步 ② 受阻即停；11 行对照与双轨核对顺延下一轮） |
| ④ 缺口分类 | 本轮仅 1 条 ENV（见下表），ENV 不派生 DATA/QUERY/ALGO，不建子任务 |

### 11 行判定

11 行（97/98/99/33.2/33.3/33.4/100/101/102/103/104）本轮**均未判定**：接口对照与库核对依赖步 ②，步 ② ENV 受阻即停轮。页面常量轨期望值全部以用例「期望输出」列为准（未改写）；双轨核对（类型全塌企业 43,296/0/0、规模四档档距、区域 12 国 vs 种子 5 国、深圳十区按 `M_SVC_PT_SZ_REGION_ORG` 单行口径）整体顺延下一轮执行。

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `ENV.database.demo-gkxlumenx-ods.conn` | ENV | 入口连接 `demo-gkxlumenx-ods` SELECT 超时（ETIMEDOUT ~6.8s）后连接池进入 closed state；连续 2 次失败 | 只读连接可用，跨库限定名可查 `demo_gkxlumenx_ads.svc_*` | 监管人检查该 database-mcp 连接（网络/连接池）可用性后，重新说「按 LOOP 跑」开下一轮；本轮不重试第 3 次、不建子任务（ENV 不派单） | —（不建单，§6.5.4） |

### 子任务

无（ENV 停轮不建 DATA/QUERY/ALGO 子任务）。

### 下一轮建议

1. 监管人 `human:徐滕强` 确认 `demo-gkxlumenx-ods` 连接恢复后，重说「按 LOOP 跑」。
2. 下一轮直接从步 ② 开始（步 ① 探测按规程仍需先打一笔，token 仍读同一本机文件）。
3. 双轨核对按用例「数据情况」列逐行展开：97/98/99 类型规模两轨、33.3 区域两轨（12 国 vs 5 国 150 行种子）、103 十区缩放比（禁跨 metric 求和）、33.4 榜 vs `svc_tech_power_score` 恒定分。

## 运行 2026-11-07（第 2 轮）

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-PT-合规演示用例.md`（本轮复核批次未变：svc_metric_* / svc_region_dist / svc_global_dist 仍 `svc-fseed-20261020`，svc_chain_gap 仍 `svcmodels_20261107_155402`，无重灌，直接按用例期望）
- 库：只读（入口连接 `demo-gkxlumenx-ods`，跨库 `demo_gkxlumenx_ads`；本轮 2 笔 information_schema + 13 笔 SELECT 全部成功，**0 失败，零写操作**；第 1 轮 ENV 已解除）
- 样本满足：**是（11/11 行 ✅）**
- 停止：无（四步全走完）
- git：按派单「禁止 git」，本报告与 LOOP 计划状态行改动**停在工作区未 commit**，待 coordinator/监管人收口（第 1 轮惯例 f826bddb）；task-registry 的认领/建单写后 commit+push 为多会话保护铁律要求，不属此禁令

### 四步结果

| 步 | 结果 |
|---|---|
| ① 探测 | ✅ `POST /tts/svcz/api/enterprise/topic/v1/recommend {"count":1}`（头 `authorization: Bearer <本机 token 文件>` + `systemcode: topic`）HTTP 200、`code=0`，返回真实推荐结构（`items[0]` 含 org_id / social_credit_code / name_cn / province=广东省 / industry_chain_names_flat=软件与信息服务）。token 有效，未打印未入档；接口映射存在 |
| ② 只读库 | ✅ 第 1 次即成功，本轮 0 失败：svc 表清单 23 张；`svc_metric_fact` 6 行（`M_SVC_PT_GLOBAL_TOTAL`=43,296 slice=all / `M_SVC_PT_SZ_TOTAL`=14,033 slice=city）；`svc_metric_dist` 142 行（类型全球 43,296/0/0、深圳 14,033/0/0，规模 >500=19,030 / 200-500=13,773 / 50-200=6,980 / <50=1,611 / 未知=1,902）；`svc_metric_series` 228 行（GLOBAL 49 行 1978–2026 / SZ 47 行 1979–2026，2025=423、2026=14 非年增量复现）；`svc_global_dist` 5 国 150 行种子（中国 90 / 美 15 / 新 15 / 德 15 / 日 15）；`svc_region_dist` 24 行（province 3 省 43,292/3/1 + sz_district 九区每区 2 metric_id 同值行复现）；`svc_chain_gap` 6 行（研发 28,842 最厚 / 中试熟化 0=blank，q061_pending_client=1 全量）；`svc_org_card` 本轮 `COUNT(*)`=43,350（fseed 批 43,296 未重灌 + NULL 批 54，较用例 17:20 记录 43,343 增 7 行，今日模型批后增量，**非 fseed 重灌**）；`svc_tech_power_score` 300 行在场 |
| ③ 接口对照 | ⚠️ 用例 11 行接口地址=前端路由（无后端 REST，用例既定）：门户 5 路由 `/service-portal/{overview,industry-distribution,region-map,capability-rank,shenzhen}`（均带 `industry=CL-SEI-01`）在网关主用 `/tts/lumen/api` 与备选 `/tts/svcz/api` **双前缀 GET 均 404**（网关结构化 404 `No static resource service-portal/…`），两处都 404 → 按派单记「映射不存在」，非 401/424 停轮条件，页面常量轨不受影响；11 行期望逐值对照=**页面常量轨全部一致 ✅**（97 KPI 10,310/621/10,310、98 类型环 6,731/2,152/1,427、99 规模四档 5,443/3,038/1,289/541、33.2 六卡研发 2,860 最厚合计 10,310、33.3 全球 12 国中国 2,462 首位 + 全国 12 省 644 首位、33.4 在库 15 家榜首 75.0、100 KPI 700/71/3、101 类型环 506/147/47、102 条形研发 196 最厚合计 690、103 南山 217 首位、104 三卡 75.0/73.6/66.2 + 抽屉四板块） |
| ④ 缺口分类 | DATA×7 项两轨差（挂 Q-SVCCHAIN-06/07/08）→ 汇 1 张 `…DATA-TWOTRACK`；QUERY×1（门户读面 REST 映射 404）→ `…QUERY-PORTAL-REST`；ALGO×1（svc_tech_power_score 恒定分）→ `…ALGO-TECHSCORE`；ENV×2：`ENV.portal-REST-404`（并入 QUERY 单登记）+ 第 1 轮 `ENV.database…conn` 本轮 0 失败**闭合**。全部 task-query 去重通过（`SVC-PT-DEMO-FIX` 模块 0 匹配） |

### 11 行判定

判定基准：门户页读数=前端确定性常量集（用例既定，「可演=页面按常量渲染」），本轮按常量轨期望逐值对照；库 ADS 轨差异**只记录不判业务对错不判缺**（Q-SVCCHAIN-06/07/08 演示口径已声明）。±1 取整尾差不判失败。

| 行 | 期望（用例） | 判定 | 两轨差异要点（库 ADS 轨） |
|---|---|---|---|
| 97 | KPI 10,310/621/10,310；折线 8 点末点 10,310 | ✅ | `M_SVC_PT_GLOBAL_TOTAL`=43,296，series 49 行 1978–2026；轴/总量两轨差 |
| 98 | 类型环 6,731/2,152/1,427 | ✅ | `M_SVC_PT_GLOBAL_TYPE_DIST` 全塌企业 43,296/0/0 |
| 99 | 规模四档 5,443/3,038/1,289/541 | ✅ | `M_SVC_PT_GLOBAL_SCALE_DIST` 5 档 19,030/13,773/6,980/1,611/1,902，档距大 |
| 33.2 | 六环节卡研发 2,860 最厚、合计 10,310、覆盖 6/6 | ✅ | 领域×环节无库面（Q-SVCCHAIN-08）；旁证 `svc_chain_gap` 研发 28,842 最厚 |
| 33.3 | 全球 12 国中国 2,462 首位（23.9%）；全国 12 省 644 首位 | ✅ | `svc_global_dist` 仅 5 国 150 行种子（Q-SVCCHAIN-07）；省级仅 3 省 43,292/3/1 |
| 33.4 | 在库 15 家 · 展示 15 家；榜首 75.0/73.6/66.2 | ✅ | `svc_tech_power_score` 300 行恒定分 40/20 无个体区分度（Q-SVCCHAIN-01） |
| 100 | KPI 700/71/3；折线末点 700 | ✅ | `M_SVC_PT_SZ_TOTAL`=14,033；series 2025=423/2026=14 非年增量口径差 |
| 101 | 类型环 506/147/47 | ✅ | `M_SVC_PT_SZ_TYPE_DIST` 全塌企业 14,033/0/0 |
| 102 | 条形研发 196 最厚、合计 690 | ✅ | 同 33.2（无库面；`svc_chain_gap` 旁证） |
| 103 | 十区南山 217 首位、页序南山>宝安>龙岗>福田 | ✅ | `M_SVC_PT_SZ_REGION_ORG` 单行口径 3,655/2,850/2,039/1,829/1,795/798/553/388/0/121，**排名序一致**；禁跨 metric 求和（`M_SVC_SZ_DISTRICT` 同值复用行本轮复现） |
| 104 | 3 卡 75.0/73.6/66.2；抽屉四板块 | ✅ | 扩展档案无库表；旁证 `svc_org_card` emp 填充 95.5% / rev 95.4%（43,350 行）未接线 |

### 缺口与子任务

| 缺口键 | 类 | 现况 | 子任务（均 bugfix、ready、只建单不认领） |
|---|---|---|---|
| `DATA.two-track.{type,scale,region,total,district,field-stage,profile}` | DATA | 7 项两轨差逐行登记（上节），挂 Q-SVCCHAIN-06/07/08，不灌数不判对错 | `SVC-PT-DEMO-FIX-R20261107-DATA-TWOTRACK`（repo=demo-algo-ent-analysis） |
| `ENV.portal-REST-404`（映射不存在） | QUERY | 5 路由双前缀 404（网关结构化 404，非 401/424）；核对是否按 ADS 面新增门户读接口 | `SVC-PT-DEMO-FIX-R20261107-QUERY-PORTAL-REST`（repo=lumen-svc-platform） |
| `ALGO.techscore-no-variance` | ALGO | 库面恒定分无个体区分度 vs 页面常量榜；模型升级不在 LOOP 内 | `SVC-PT-DEMO-FIX-R20261107-ALGO-TECHSCORE`（repo=lumen-algo-py） |
| `ENV.database.demo-gkxlumenx-ods.conn`（第 1 轮） | ENV | 本轮 13+2 笔 0 失败，缺口**闭合**（第 1 轮「并发连接池瞬时争用」判断成立） | —（闭合不建单） |

### 下一轮建议

1. 三张修单走 LOOP 外正常任务流：data/api/algorithm agent 认领执行（执行前另行 MCP 认领，监管人 `human:徐滕强`）；qa-agent 只建单不改码。
2. 同缺口两轮停规则自本轮起计数（第 1 轮 ENV 停轮未触缺口分类）；本轮无「两轮停」缺口。
3. 库面本轮快照可直接复用（批次未变）；无新灌批/新决策不自动开第 3 轮，再验收由监管人重说「按 LOOP 跑」。
