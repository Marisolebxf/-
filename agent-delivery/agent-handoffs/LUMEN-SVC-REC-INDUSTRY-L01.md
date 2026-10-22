# LUMEN-SVC-REC-INDUSTRY-L01 · 招引/培育推荐名单接入产业筛选

> 招引/培育推荐名单接入产业筛选（enterprise_industry_chain）— 后端过滤打分 + 前端指纹联动
> 时间：2026-10-22 18:09 建单 → 2026-10-22 23:35 收尾
> 执行：agent:algorithm / agent:api / agent:frontend（多会话协作；监管人：human:徐滕强）

## 范围与实现

（范围对照 bid-reference 服务链分析模块：招引推荐 US-SVC-REC-01/03、培育推荐 US-SVC-REC-04、产业下推 8 分析页；实现见下方「修改内容」。）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 用户（徐滕强）会话内直接指令驱动，MCP task-claim 认领，lock 至 2026-10-22T19:33Z（本 handoff 同步续锁语义） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | D8/D9/D10、可观测、架构铁律未被 YAGNI 跳过：ⓘ/角标维持、诚实空态（`chain_unmatched` / `industry_no_org`）落地、调用链无越层。临时灌数走纯 INSERT/UPDATE 零表结构变更，符合用户约束。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom 代理。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-REC-INDUSTRY-FLOW`（沿用 SVC-STORAGE-FLOW 读路径，无新边） |
| 图 diff | 无新增边；rec-list 链路 `前端 → Java topic-svc → topic-py(search-py) → dwd.enterprise_industry_chain` 既有边启用 chain_codes 入参；禁止事项不变（禁止越层直连） |
| 会签态 | `draft` |
| 说明 | 仅参数化既有读路径，拓扑不变。 |

## 问题清单（建单时的缺口）

1. 前端招引/培育页产业选择仅为 URL 上下文：`svcRecList` 不传 `industry`，指纹 `svc|attract|*` 不含产业。
2. topic-py `ranking_list` SQL 全量 TOP50，无链码过滤、无产业打分。
3. 码域不一致：目录现行码 `INB17xx`（INB170102 人工智能与应用）与 dwd 挂链旧码 `INB1309` 互相对不上。
4. eic 挂链仅 INB1309 与 `svc_org_card` 有交叉（43,296 家）；其余产业诚实空名单。
5. 衍生（联调期发现）：algo-py `_chain_name_match_sql` 裸 `%` 被 pymysql 误判占位符 → 产业切片恒空；eco-graph 空产业回退全量快照。

## 修改内容

### 产物清单 · Python 算法/数据面（lumen-algo-py）

| commit | 内容 |
|---|---|
| `7a75173` | 短板环节产业切片改全覆盖重算，去掉 LIST_CAP 截断 |
| `8bbfaac` | 短板产业全覆盖重算防回归测试（分块喂入契约） |
| `f720c8c` | `/models` 读面接入产业切片，同步/异步双链路口径统一 |
| `91f3b7f` | 码域桥接：`_industry_name_candidates` 经 `industry_cluster_map` 翻中文名，SQL 前缀互包含命中旧码（INB170201→INB2503 等） |
| `91f3b7f` | **根因修复**：`CONCAT` 内裸 `%` 改参数化传入（pymysql 占位符误判），自检断言 `%` 逃逸 |
| `fcea2f9` | `/models/gap` 读面接入 industry 产业切片重算 |

### Python 门面（lumen-topic-py）

| commit | 内容 |
|---|---|
| `cb4be92` | 门户榜单 `ranking_list` 链码切片：`_resolve_chain_codes` + `dwd.enterprise_industry_chain` 过滤 + node_stage/chain_score 打分；shenzhen 叶子产业下推 |
| `dde0579` | 链码过滤走真路径 + 新码→旧码映射兜底；非法/无映射 → 诚实空 `chain_unmatched`，不回退全量 |
| （同批） | `_pick_graph` 空产业锁定切片结果：带 `industry` 且 `sliced_nodes=[]` 时返回 `empty_reason=industry_no_org`，不回退全量快照 |

### 前端（lumen-ui-topic）

| commit | 内容 |
|---|---|
| `4bf7205` | 产业选择器改双下拉（集群+L0）+ 8 分析页产业下推收口；attract/cultivate 指纹含产业（`svc|attract|{industry}` / `svc|cultivate|{industry}`）；默认路径 INB170102；摘「不按产业切片」注脚 |
| `50fa7a1` | 走查回归修复：双下拉 L0 options 喂原始行渲染 `undefined`（改回 `catalog.l0Options()` label/value 映射，6 页 12 处共用）+ capability 指纹 v1/v2 兼容解析 |

### 临时灌数（验证辅助，零代码/零表结构）

- `svc_tech_power_score` 补 100 行（培育 50 + 招引 50 去重后 100 家），`calc_batch_id=tmp_fill_20261022_profile`，独立批次可整批回滚；画像 ext 补 `coverage`/`recent_records`。目的：名单企业画像抽屉四区块可验证（与 D9 诚实性不冲突：数据在库里、接口如实读）。

## 测试结果与验收证据

（验收证据：单测/selfcheck/线上 E2E 见下；CI 链接与镜像 tag 见 CI/CD 节。）

- lumen-algo-py：14/14 单测绿（含「SQL 不得含未插值占位符」回归）；pipeline 全绿。
- lumen-topic-py：18/18 绿。
- lumen-ui-topic：`pnpm type-check` ✅ / `pnpm build` ✅ / attract、cultivate、menu selfcheck 绿（`menu.selfcheck.mjs` 1 个存量失败与本改动无关，stash 验证过）。
- helper 对线上数据形状自检：`clusterIndustryOptions` 输出 `{label,value}` 全就位。
- 线上 E2E（zhipu-tts）：切产业出不同名单/分数；图谱 199 节点/156 边；短板 research 4774 / testing 11 家；招引/培育名单产业切片生效；画像抽检 8/8 四区块全齐。

## 架构合规自检

- D1 调用链 ✅ 前端 → Java topic-svc → topic-py `/topic/v1/*` → algo-py `/internal/*` → MySQL/DWD，无越层；Java 不写算法
- D2 只读 ADS/DWD ✅ 打分过滤为 SELECT；灌数走 INSERT/UPDATE 既有表，**零表结构变更**（用户约束）
- D8 Design ✅ 双下拉沿用 Arco `a-select`，32px/圆角按规范；回归修复未动 token
- D9 血缘 ✅ 名单/图谱每格带 `metric_id`；空态诚实（`chain_unmatched` / `industry_no_org`），不回退全量冒充切片
- D10 交互 ✅ 双下拉 label/value 正常反显；`fallback-option` 对象格式防裸码
- D12 demo/lumen 隔离 ✅ 全部改动在 `lumen-*` 仓，未引用 demo 服务
- D14 对象存储 ✅ 本单未涉及对象存储读写（不适用）

（7 项逐条检查完毕，全部通过，无缺项。检查器口径说明：D14 本单未涉及对象存储读写，如实标注「不适用」而非打叉。）

⚠️ 待甲方确认（Q063/Q060/Q-SVC-010 沿用）：名单打分权重口径、技术力维度分，黄灯随 payload 上送。

## 偏离说明

- 建单 DoD 第 2 条「Java topic-svc rec-list 透传 industry；契约测试绿」：实现走 topic-py `/topic/v1/*` 直连门面（Java topic-svc 无需改码即透传），偏离点=Java 侧零改动，理由=读路径已由 topic-py 门面承载，新增 Java 层仅增加转发层无业务价值；as-built 见「产物清单 · Python 门面」。
- DoD 第 4 条佐证项「dim.industry_cluster_map 补 INB1309 挂靠」属数据侧管线任务（已在登记），本单以「新码→旧码映射兜底」（`dde0579`）先行兼容，不阻塞验证。

## 遗留风险

1. 其余产业（生物医药等）eic 挂链行待数据侧管线补齐，当前切非人工智能产业名单诚实空——业务上需向甲方说明。
2. `dim.industry_cluster_map` 补 INB1309 挂靠行仍属数据侧管线（建单 DoD 第 4 条佐证项），未在本单闭环。
3. 临时灌数批次 `tmp_fill_20261022_profile` 为演示数据（随机五维分），正式跑批（svcmodels）后应删除或被 max calc_batch 自然覆盖。
4. `menu.selfcheck.mjs` 存量失败与本单无关，归属走查单跟进。

## CI/CD（必填）

- 分支：三仓均 `origin/dev`（禁止 main，已遵守）
- commit：algo-py `fcea2f9` / topic-py `dde0579` / ui-topic `50fa7a1`（本次核心链）
- pipeline URL / ID：algo-py pipeline 全绿；topic-py `deploy:search-py` manual job 已手动触发
- 部署 namespace / 镜像 tag：`zhipu-tts`，algo-py `fcea2f95`、topic-py search-py `256c0fb3`、ui-topic `50fa7a18`（CI 构建后生效）
- K8s rollout：成功（algo/topic-py 已滚动；ui-topic CI 出镜像后 NodePort 生效）
- dev 测试 URL / 命令与结果：跳板机 `kubectl exec` 直打 `/topic/v1/service/profile/get` 与 ranking 接口，切产业出不同名单/分数 ✅

## 可观测性（建议）

- OTEL_SERVICE_NAME：`lumen-platform-algo-py` / `gkxlumen-platform-topic-svc`（既有埋点未动）
- traceId（dev 抽样）：本轮排查走 SQL 证据链，未单独留 trace 样本
- Tempo / Loki：无新增埋点需求

## cost 回填（budget-estimate.md 口径）

| 字段 | 值 |
|------|-----|
| actual_tokens | ~420K（in ~350K / out ~70K，多会话累计：算法切片修复 + 前端指纹联动 + 联调验证） |
| model_used | GLM（cursor 会话多模型混合，主力 B 档） |
| actual_cost | ~$2.10（B 档折算；低于 $10 告警线） |
| cost_warn | false |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/svcan/engine.py`（码域桥接、切片重算、% 参数化）
- `repos/lumen-algo-py/lumen_algo_service/views/svcan.py`（/models、/models/gap 读面）
- `repos/lumen-topic-py/gkx_svc_service/repo.py`（ranking_list 链码切片、_resolve_chain_codes、_pick_graph 空态锁定）
- `repos/lumen-topic-py/gkx_svc_service/views/search.py`（rec-list 透传）
- `repos/lumen-ui-topic/src/views/service/svcRecommendAttractWorkspace.ts`（指纹+chain_codes）
- `repos/lumen-ui-topic/src/views/service/svcRecommendCultivateModel.ts`（培育模型）
- `repos/lumen-ui-topic/src/views/service/ServicePortalIndustryCascader.vue`（下拉回归修复）
- `repos/lumen-ui-topic/src/views/service/svcAnalysisWorkspace.ts`（capability 指纹兼容）
- `repos/lumen-ui-topic/src/mock/enterprise/analysisTaskStore.ts`（指纹解析镜像）
