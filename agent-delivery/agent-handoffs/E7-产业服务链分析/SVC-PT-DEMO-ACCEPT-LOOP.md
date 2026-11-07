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
