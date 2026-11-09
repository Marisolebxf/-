# SVCCHAIN-DC-M3-REC-L01 handoff｜产业服务链分析 · 机构招引培育域合规演示用例 + LOOP 计划

> **任务**：`SVCCHAIN-DC-M3-REC-L01`（总控：`SVCCHAIN-合规演示用例-长任务总控.md` 段 M3c）
> **agent**：doc-agent｜**监管人**：human:徐滕强｜**强度**：ponytail full
> **日期**：2026-11-07
> **依赖**：M1（`SVCCHAIN-需规条目矩阵.md` §2.3）+ M2（`SVC-数据调研-20261107.md`）
> **产物**：
> 1. `agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-REC-合规演示用例.md`
> 2. `agent-delivery/工程过程/04-系统集成/03-专题系统集成/编排计划/SVC-REC-LOOP计划.md`

`ponytail:` full——按金样 POL-L2-DS10-QRY 体例最小交付：两份文件零自造脚手架；覆盖表 8 列金样结构；期望值全部来自实查/快照真值，不造数；不建单不跑 LOOP；历史 as-built 文件零改写。

## 1. 范围与实现

- **用例**：REC 域 4 主行（7.6.1–7.7.2）100% 落覆盖表 + 3 行 I2-12 行为补充行（切条件不自动起任务 / 单飞复用 / 当天复用与重新分析）；金样 8 列结构；每行期望写具体值（taskId 形态 / `result_payload` 字段级真值 / 榜表行 rank+名称+指数 / rec-list 请求体）；一条主路径串 6 步（受理→诚实空→正样本→培育配置门控→培育名单→I2-12 复用）；文头带规程指针 + 历史记录不改写声明 + 双面数据面口径（Job 快照面 / rec-list 读面）。
- **LOOP 计划**：按总控 §4 全要素——建议 ID `SVC-REC-DEMO-ACCEPT-LOOP`（只写不建）、域数据面备忘、通过线表、token（`~/.gkx/topic-loop-token` + `systemCode: topic`）、一轮四步（探测→签发+只读库→对照→缺口分类 DATA/QUERY/ALGO/ENV）、缺口分类表 + 不派单情形、每轮 ≤3 张（`SVC-REC-DEMO-FIX-R{YYYYMMDD}-*`）、同缺口两轮不进则停、报告 handoff 路径（只追加）、状态行「覆盖已齐，未执行。等人说『按 LOOP 跑』」。
- **接口地址真源**：lumen as-built 只读对照——网关 `/topicAsync/topic/v1/**`（`AnalysisTaskPaths`）→ `gkxlumen-topic-async-service` analysis/tasks 三件套（Create/详情轮询/result）→ 结果读面 `POST /svc/topic/v1/service/rec-list`（`LUMEN-SVC-P-JAVA-API-REC-LIST-L01` SEQ：Feign 复用 `lumen-topic-py` `POST /internal/gkx-svc/portal/ranking`，kind=attract|cultivate → list_type=ATTRACT|CULTIVATE → Python 读 ADS 两榜）。

## 2. 查库实勘（只读，零写操作）

- 入口连接 `demo-gkxlumenx-ods`（M2 同款绕行连接），跨库限定名查 `demo_gkxlumenx_ads` / `demo_gkxlumenx_dwd` / `demo_gkxlumenx_dim` / `gkxlumenx_topic_enterprise`；2026-11-07 17:00–17:40（UTC+8）。SELECT 失败 2 次（`rank_no` 列名误用 ×2），修正后全部成功。
- **招引榜** `svc_attraction_recommend`：50 行，批次 `svcmodels_20261107_155402` / `svc_proxy_v1.3`、weights 35/30/20/15、rank_no 1–50 连续、指数 88.60–90.00、全 `high`。首行 rank 1 广东奥飞数据科技股份有限公司（广州）90.0000。
- **培育榜** `svc_cultivation_recommend`：**50 行（⚠️ 与 M2 §2.6「3 行」不一致——M2 定稿后 17:01 被新批次 `svc_rec_cultivate_wanghui_20261107_170132` / `wanghui_v1_signed20261022` 覆盖，批次 weights=等权 25×4）**。首行 rank 1 深圳市福中达投资控股有限公司 95.3634（scale 90.7669 / marketGap 99.96 / innovation、effect=NULL，`dims_available=2`，`advice_gen=llm`）；2 名万城节能 92.5801、3 名比达文化 89.3121；50 家 JOIN 卡面 city：深圳市 43 + 无 city 7；`growth_stage` 全 NULL。
- **Job 记录** `gkxlumenx_topic_enterprise.analysis_task`：REC 两类 success 91（attract 56 / cultivate 35）、failed 0，`result_data` 列全 NULL（快照不落独立表=M2 受阻项④实锤）。正样本锚点：`SVC-20261107-010`（attract@INB2503：status=ads_ready、count=6、top 90.7805、narration ok 含「演示口径/不作对外招商承诺」）、`SVC-20261107-007`（cultivate 全量：count=50、top 95.3614、own_gaps 含 25/30/25/20）、`SVC-20261107-008`（attract 全量：count=50、top 90.784）、`SVC-20261107-015/018`（INB1303：status=empty、count=0、narration skipped）。
- **挂链** `demo_gkxlumenx_dwd.enterprise_industry_chain`：INB1309 186,964 / INB2503 5,267 / INB1354 921 / INB1204 1,110（含 2 行脏数据 chain_name='电池'）/ INB1209 32 / INB1323 67 / INB2505 51；**INB1303 / INB1306 / INB1333 = 0 行（Q-SVC-011 现状未变）**。榜表交集：招引榜∩INB2503=7 家（rank 5/13/15/30/33/44/46，指数 90.0–88.6）、∩INB1309=50、∩INB1303/1306/1333=0；培育榜∩INB1309=50、∩INB2503=0。
- 码表 `demo_gkxlumenx_dim.industry_cluster_map` 15 行与前端 seed 一致（CL-SEI-02→INB2503）。指标 MCP 只读：`M_SVC_REC_ATTRACT_SCORE` / `M_SVC_REC_CULTIVATE_SCORE` 均 D1=aligned / D2=partial(provisional) / D3=partial / D4=mock。
- **前端模型值校核（非业务仓改动，仅本地跑数）**：把 demo-ui-topic `serviceRecommendModel.ts` 纯函数用 esbuild 打包实跑——招引 35/30/20/15 手工复算与函数输出一致（ext-cand-001=86.2）、培育默认筛选 field-bio 出 12 行（首行华大基因 84.5）——**结论：demo 沙箱本地模型与部署真身数据面不同源，用例期望全部按 lumen 真身（ADS 榜表 + Job 快照）写，demo 本地模型值不入期望**。临时脚本在 /tmp，未入仓。

## 3. 4 行判定汇总

| 需规 | 判定 | 依据摘要 |
|---|---|---|
| 7.6.1 招引模型与指标 | **可演** | REC Job 受理链路 56 条 success 同型；权重 Tag 35/30/20/15（svc_proxy 批次 weights 同值）；ⓘ D4 mock 🧪；⚠️ Q-SVCCHAIN-05 |
| 7.6.2 推荐名单生成 | **可演（正样本 + 诚实空双切片）** | 正样本锚点 SVC-20261107-010 + 榜表实查；诚实空切片锚点 SVC-20261107-015；INB1303/1306/1333 挂链 0 行=Q-SVC-011，空态本身可演 |
| 7.7.1 培育模型与筛选 | **可演** | SVC-20261107-007 同条件成功在库；筛选空集门控 as-built P0 系列实证；权重 Tag 25/30/25/20（页面口径）；⚠️ Q-SVCCHAIN-05 + 权重双口径并存（见 §4） |
| 7.7.2 培育名单与建议 | **可演** | 培育榜 50 行实查（首行 95.3634）；建议结构 `advice_gen=llm` + `suggestion_items`（载体对接/规模提升等分组）实测；入篮目标表现存 6 行 guest |

**合计：可演 4 / 覆盖不到 0 / 设计无资源 0**（诚实空切片按「空态可演」落行，缺口引用 Q-SVC-011；M2 预判的「Job 快照不落库→覆盖不到」按任务口径改为「受理成功 + wait_view 快照字段对照」写法，仍可演）。

## 4. 偏离说明

1. **培育权重不一致处置（M1 矩阵勘误 2 延续）**：USM 文档 20/30/25/25 已被 M1 以「代码+实勘双证 25/30/25/20」勘误；本叶实勘发现**第三口径**——培育榜 11-07 17:01 新批次（`wanghui_v1_signed20261022`，王惠 2026-10-22 会签的试点口径）库内 weights=等权 25×4，与页面 Tag 25/30/25/20 并存。处置：不改前端、不改算法、不改 USM；用例页面期望锚 25/30/25/20、榜行期望锚「当期批次 weights 真值」；LOOP §0/§4 明确「双口径各自成立不算缺口、等权正式化走 Q-SVCCHAIN-05 甲方决策、不为本 LOOP 派修」。建议 M4 缺口总表归并时把该并存事实登记（本叶不新造编号）。
2. **M2 §2.6 培育榜「3 行」已过时**：17:01 批次切换致 M2 调研值失效；本叶不改写 M2 文件（历史调研记录），在用例查库节声明差异并以本叶实查为准。
3. **接口地址按 lumen 真身写**：分析任务三件套 `/topicAsync/topic/v1/analysis/tasks*` + 结果读面 `/svc/topic/v1/service/rec-list`；M1 矩阵附录的 demo taskType 键（`service_recommend_attract/cultivate`）与库键 `svc:analysis:attract|cultivate` 的映射在用例文头写明（demo 沙箱 localStorage 任务单 ≠ lumen 服务端任务单，不混写）。
4. **Job 期望写法按任务口径**：受理成功 ≠ 成功——期望按「受理 queued → 轮询 success + wait_view → GET result 读 `result_payload` 字段对照」三段写；快照数值冻结自 2026-11-07 锚点任务，榜表滚动后按「重签发再读」对齐（LOOP §0.3）。
5. **无覆盖不到行**：M2 预判的产业切片缺口（Q-SVC-011）落为「诚实空切片可演」行；svc 域无收藏/历史需规行，两表不存在不影响本域 4 条需规。

## 5. 验收证据

- 两份产物已写入目标路径（ORG/ECO/PT 姊妹产物同目录同体例）。
- 期望值可复核性：每行 taskId/rank/机构名/指数/维度分都能用用例「查库」节的连接与表名以只读 SELECT 复现；快照字段以 `analysis_task.task_id` 直查 `JSON_EXTRACT(target_params,'$.result_payload')`。
- LOOP 计划含总控 §4 全要素核对：建议 ID ✅ / 先决条件 ✅ / token+systemCode ✅ / 一轮四步 ✅ / 缺口四分类 ✅ / 每轮≤3 ✅ / 两轮停 ✅ / 报告路径只追加 ✅ / 状态行 ✅。
- 本任务**只产文档**：未建 LOOP 验收单、未跑 LOOP（未签发任何 Job）、未派修数单、未改 registry seed / 业务仓 / as-built 历史文件。

## 6. 4 行覆盖核对（总控门）

- 需规 7.6.1–7.7.2 共 4 主行，覆盖表 4 主行 + 3 行为补充行（挂 7.6.2/7.7.2 名下，不占需规新行），零缺行 ✅
- 可演行的请求参数值 = 界面输入真源值（产业目录码表实值 / 闭集枚举 / 固定权重 Tag）且引用实查数据 ✅
- 产业切片行引用 Q-SVC-011；演示态行引用 Q-SVCCHAIN-05；全部既有编号，未新造 ✅
- 主路径只串可演行 ✅

## 7. 架构合规自检

| 铁律 | 自检 |
|---|---|
| D12 不触业务仓 | ✅ demo-ui-topic / lumen-ui-topic 只读对照 + /tmp 本地跑数，业务仓零改动零 commit |
| 只读库 | ✅ database-mcp 仅 SELECT / JSON_EXTRACT，零写；失败 2 次均为列名笔误即修正 |
| 调用链（铁律 2） | ✅ 接口地址按 前端→网关 `/topicAsync/**`/`/svc/**`→Java→Feign `/internal/gkx-svc/*`→Python→ADS 写，无越层 |
| D9 指标口径 | ✅ 只引用注册指标 M_SVC_REC_ATTRACT_SCORE / M_SVC_REC_CULTIVATE_SCORE（MCP 实取：D1 aligned / D4 mock），未新造；D2 provisional「待核验」字样已入期望 |
| 不造数 | ✅ 期望全部实查/快照真值；口径未定行（Q-SVCCHAIN-05）按演示态声明；demo 本地模型值明确不入期望 |
| 缺口编号 | ✅ 只引用既有 Q-SVC-011 / Q-SVCCHAIN-05 / Q063，未新造 |
| 不建单/不跑 LOOP/不派单 | ✅ 验收单建议 ID 只写进计划；本轮零 Job 签发 |
| 历史文件不改写 | ✅ as-built rec-attract / rec-cultivate cases 零改动；M2 / M1 文件零改动 |

## 8. cost

- `actual_tokens`: ~260k（估算）
- `model_used`: glm-5.3-Flash
- `actual_cost`: ~$0.9
- `cost_warn`: false（<$10 阈值）
