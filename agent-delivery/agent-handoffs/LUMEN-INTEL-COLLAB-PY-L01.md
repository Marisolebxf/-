# LUMEN-INTEL-COLLAB-PY-L01 · handoff

- 任务：综合智能分析协同 — 装包 + batch_meta 持久化 + 策略 LLM
- Epic：E8-综合智能分析 ｜ 执行：agent:algorithm-agent ｜ 监管：human:徐滕强
- 仓：`repos/lumen-algo-py`（origin/dev，commit `849f357`，**未 push**——任务文明示不 push）
- 日期：2026-11-05
- 强度：ponytail full
- 真源：`agent-delivery/agent-handoffs/综合智能分析-SYNTH/sdd/l2/SYNTH-L2-COLLAB.md` v1.0.8；`综合智能分析-SYNTH/LUMEN-INTEL-MOCK-INV-L01.md`（CollabResult 契约）；`LUMEN-INTEL-COLLAB-DDL-L01.md`（表实况：8 张，relation_input 3 行 is_mock=1，其余 7 张 0 行）

## 1. 范围与实现（对照 COLLAB 册 v1.0.8 / 任务书 6 条）

| 要求 | 实现 |
|---|---|
| collaboration 装包：读 4 张指标表只读 succeeded 最新批按 calc_batch_created_at | ✅ `entan/synth_collab/pack.py` `_latest_batch`（先 MAX(calc_batch_created_at) 再取该批全部行，禁 calc_batch_id 字符串比大小）；缺行 null+reason+confidence，禁补 0 |
| relation_input 读 canonical（metric_id=M_SYNTH_COLLAB_RELATION_INPUT） | ✅ `_read_relation_input` 只读 canonical 行、取最新 succeeded 批；`relationInput` 三键 jointPatent=6477/project=0/talentFlow=18553（co_project=0 合法实测，不补 0）；caliber/source_has_year 载荷透出 |
| 三窗空态：index/完整度/中心度/密度 = null + no_year_on_source；密度不读 191 | ✅ `_cell` 包装（值缺 → null+`no_year_on_source`）；密度只读本表 `stat_type='density'`，响应无 191 数值来源（自检断言 metrics 无 `M_SYNTH_191_1` 键）；读表行为保留（C-05 解锁后有行即透出，非接口写死，D18） |
| clusters=[]+cluster_rule_unclosed（不派生）；不写 node/edge 行 | ✅ 固定空态+reason；全程无 node/edge 写入（实查 0 行） |
| CollabResult 其余字段按 MOCK-INV | ✅ 顶层 24 字段齐（自检断言）；effectEval 三态（none/insufficient/ok）诚实，无批 `status='none'+reason=batch_not_published`，insufficient 行不出系数/散点 |
| batch_meta 持久化（§3.1 核心）：发布成功写 synth_collab_batch_meta | ✅ `_publish_batch_meta`：任务链（task_id+有批）发布写一行九列（snapshot_id/calc_batch_id/graph_batch_id/cache_key/region/compare/window/published_at/is_latest）；缺任一必填列或写库失败 → 拒绝发布（不标 succeeded）；snapshotId 不可变（task:{task_id}） |
| AR-9 包内事务：cache_key→最新 snapshotId / is_latest | ✅ INSERT→UPDATE 新行置 1→UPDATE 旧行翻 0 同一连接 commit（任一步失败 rollback 整组）；未传 snapshotId 读 `cache_key+is_latest=1`；指定 snapshotId 无映射 → `batchMetaReason=batch_meta_missing` 不回落最新批（册 §3.2） |
| 策略 LLM（141③）：装包时实时生成、证据锚定、degraded 降级、无表落地 | ✅ `build_strategies`：`_evidence_facts` 只引用 relation_input/output_corr 实际行拼 facts → `entan/common/llm_client.py` GLM（temperature 0.1/timeout 20s/retry 1）；失败/未配/解析失败 → `strategies=[]+strategiesReason=strategy_llm_unavailable`（`narrative.py` 同款降级契约）；产物带 `reviewStatus='待审核'`（Q-SYNTH-C-04）；无表（v0.4 废止 strategy 表） |
| 路由：jobs 加 leaf=collaboration 分支；GET batch-snapshot；analysis_fp 三段 | ✅ `synth_jobs_routes.py` 加 `elif leaf == "collaboration"`（vitality/elements 行为不变）；新路由 `api/synth_collab_routes.py` GET `/internal/v1/synth/collaboration/batch-snapshot`（仿 elements：200/400，snapshot_id 可选回读）；analysis_fp=region|compare|window 三段（窗归一中文在装包入口） |
| 五阶段文案逐字 MOCK-INV §2 协同行 | ✅ `COLLAB_STAGES` 与 `region_innovation_collaboration` 行逐字一致（自检断言） |
| 自检（仿 check_synth_elements.py） | ✅ `scripts/check_synth_collab.py` 50 断言 6 组全过（见 §4） |

## 2. 偏离说明

1. **effectEval 增 `reason` 键（MOCK-INV DTO 无此键）**：诚实空态披露（none/insufficient 各自原因），FE 忽略不影响契约字段；对齐 D9/D18 诚实性。
2. **graph_batch_id 采用 `graph:{calc_batch_id}` 派生格式**：本期只生成不落图行（node/edge 0 行，C-05 单解锁实装），独立图谱批号机制（如 UUID）届时由 C-05 单定；meta 行语义不受影响（uk(snapshot_id) 唯一）。
3. **快照路由非默认三元组不 404**：册 §3.1「404 非默认三元组」是 Java `/topic/v1` 门面层职责（FE `isSynthDefaults`）；Python `/internal/*` 层入参合法即 200（无批 → null+reason），与 ELEM 单同轨（其 handoff 已登记同款口径）。
4. **`relationInput` 全缺行时为 null 而非空对象**：canonical 行全缺（如换区无行）→ `relationInput=null`，不伪造空对象；默认三元组恒有 3 行不受影响。
5. **散点 `points` 行格式待 C-05 实算对齐**：sufficient 行出散点（period_end/value_num/value_json.joint_patents）；本期 output_corr 0 行无实据，不预编格式样本。

## 3. 产物清单

| 文件 | 说明 |
|---|---|
| `vendor/entan-py/entan/synth_collab/pack.py` | 装包实现（读表/空态/batch_meta/策略 LLM/主函数） |
| `vendor/entan-py/entan/synth_collab/__init__.py` | 模块出口（同构 synth_elements） |
| `vendor/entan-py/api/synth_collab_routes.py` | GET `/internal/v1/synth/collaboration/batch-snapshot`（200/400） |
| `vendor/entan-py/api/synth_jobs_routes.py` | 共享 POST 路由增 `leaf=collaboration` 分支（vitality/elements 不变） |
| `vendor/entan-py/api/main.py` | 挂载 synth_collab_routes（+8 行） |
| `vendor/entan-py/scripts/check_synth_collab.py` | 自检：50 断言 6 组（实连 demo 库，探针自清幂等重跑） |
| `agent-delivery/agent-handoffs/LUMEN-INTEL-COLLAB-PY-L01.md` | 本 handoff |

commit：`849f357 feat(vendor/entan-py): 综合智能协同装包+batch_meta持久化+策略LLM [agent:algorithm]`（6 files，+983/-6；未 push）
工作区他人未提交文件（`scripts/mock_stage_health_scores.py`、`scripts/seed_supply_chain_relations.py`）未触碰。

## 4. 验收证据（demo 库 10.50.11.76 实跑）

`ENTAN_MYSQL_HOST=10.50.11.76 python3 vendor/entan-py/scripts/check_synth_collab.py` → **50 断言全过，`{"ok": true, "passes": "all"}`**：

```
[1] 同构：顶层 24 字段齐 MOCK-INV §1；effectEval DTO 齐；relationInput=6477/0/18553；
    snapshotId 含批次不可变；外壳 computedAt/methodVersion
[2] 三窗空态：1y/3y/5y 指数/完整度/中心度/密度全 null+reason=no_year_on_source；
    clusters=[]+cluster_rule_unclosed；nodes/edges=[]；密度无 191 键；
    node/edge/cluster 实查 0 行；relation_input canonical 3 行
[3] batch_meta：探针批读回（指数 66.6666/密度 0.4242）；insufficient 行 →
    effectEval.status=insufficient；任务发布落 meta 九列齐 is_latest=1；
    按 snapshotId 回读 graph_batch_id 一致；无映射 snapshotId → batch_meta_missing
    不回落最新批（指标读数仍为该条件最新批，仅 meta 缺映射不伪 404）
[4] cache_key 改指：A/B 两批发布 → 同 cache_key 两 meta 行，AR-9 新行 1/旧行 0；
    A 的 snapshotId 仍回读原 graph_batch_id（A/B 图谱不串）
[5] 策略 LLM：未配 key → strategies=[]+strategy_llm_unavailable；
    mock 成功 → 待审核 Tag+evidenceRefs 证据锚定
[6] 端到端（TestClient）：快照 200/400×2；jobs 202/400；vitality/elements 邻叶 202 不回归
```

探针残留复查：自检后 `synth_collab_index/network_stat/output_corr/batch_meta/node/edge` 全部 0 行、relation_input 恒 3 行（探针批/探针 meta 幂等清除）。

## 5. CollabResult 对照 MOCK-INV 差异

| 字段 | MOCK-INV/mock 值 | 本实现 | 说明 |
|---|---|---|---|
| collabIndex/completeness/centrality/density | 数值 | null+metrics reason=`no_year_on_source` | 三窗空态诚实（v1.0.7）；C-05 解锁后读行透出 |
| deltaVsCompare/yoy | 数值 | null | 对比盘/历史批未落，不编数（同 elements 线） |
| relationInput | 三键对象 | ✅ 同构三键（6477/0/18553） | canonical 读行；全缺行 → null（偏离 4） |
| nodes/edges/centralityTop/clusters/isolates/ranks/trend/strengths/weaknesses | 非空数组 | []（clusters 另带 reason） | 空态契约；node/edge 0 行不回全历史边 |
| effectEval.status | 'ok' | 'none'/'insufficient'（本期） | 无批/样本不足两态诚实；DTO 字段齐+`reason` 键（偏离 1） |
| strategies[].reviewStatus | '待审核'\|'已审核' | '待审核'（LLM 产物恒待审核） | C-04 临时默认；degraded=[]+`strategiesReason` |
| methodVersion（体外壳） | vDemo-collab | synth-collab-v1.0 | 服务端方法版本命名（同 elements 线模式） |
| ➕ graph_batch_id/publishedAt/batchMetaReason/cache_key/calc_batch_id/metrics | 无 | ➕ | §3.1 batch_meta 回显 + D9 追溯块（FE 忽略不影响） |

## 6. 架构合规自检（公约 §2 铁律）

| 铁律 | 自检 |
|---|---|
| 1 算法只在 Python | ✅ 装包/空态/LLM 全在 entan-py；无 Java 算法 |
| 2 调用链 | ✅ Java Feign 专用 `/internal/*`；浏览器禁直打（路由 docstring 声明）；未动 Java/FE |
| 3 NebulaGraph | N/A（本期图谱读 ADS relation_input，不做 Nebula 导出，册 §1；未写 nGQL） |
| 4 可观测性 | ⚠️ 部分——装包日志已记 batch_meta 关键行（logger.warning/error）；OTel 埋点属 Java/FE 段，本单未动（与 ELEM 单同口径） |
| 5 CI/CD | ✅ 仅本地 commit 未 push（任务文明示）；push 由 coordinator/用户统一 |
| 6 demo2 只读 merge | N/A（未动 demo 仓） |
| 7 共享聚合核心 | ✅ 只读 ADS 标准表；Java 不写算法不受影响 |
| 8 ADS 先行+Mock | ✅ ADS 落点；空态=读表结果非接口写死 mock（D18）；relation_input is_mock=1 原样透出 |
| 9 D8 前端规范 | N/A（未动 FE） |
| 10 D9 血缘 | ✅ metrics 块带 metric_id/confidence/reason；batch_meta 列与血缘 COMMENT 对齐（AR-10 映射） |
| 11 D10 交互规范 | N/A |
| 12 D12 demo/lumen 隔离 | ✅ 只写 `demo_gkxlumenx_ads`（apply_plane ent=demo 锁定，正式库拒绝）；未动 lumen 其他仓 |
| 13 D14 对象存储 | N/A |
| 14 D16 gapfill 边界 | ✅ 未写 gapfill/ODS/DWD/供应方库；策略无表落地（不建 strategy 表） |
| 15 D17 合规算法 | ✅ 未触碰唐绍祖锁定闭包；协同指数式与 calc-logic 一致（禁密度×强度） |
| 16 D18 签收条件 | ✅ 接口只读 ADS 表数据+空态读表结果，无写死 mock；batch_meta 为设计内持久化非 mock 表 |

## 7. ponytail 自检

ponytail: full——复用 elements/vitality 全部模式（`entan.common.db.connect`、批次语义 `_latest_batch`、`_cell`/`_metric_meta` 三件套、路由 200/400/500 结构、五阶段 202 包），不新造框架；最小文件集（2 新模块 + 1 新路由 + 2 挂载点 + 1 自检）；LLM 客户端零改动复用 `llm_client.py`，无新依赖；graph_batch 派生格式已注明 ceiling（`graph:{calc_batch_id}`，升级路径=C-05 单独立图谱批号机制）；自检=单脚本 50 断言（含 A/B 批改指反例、LLM 双路径 mock、TestClient 端到端、探针自清）。

## 8. cost（按 budget-estimate.md 四字段）

| 字段 | 值 |
|---|---|
| actual_tokens | ~185000 |
| model_used | glm-5.3-Flash（Cursor 内） |
| actual_cost | ~$0.24 |
| cost_warn | false（< $10 阈值） |

## 9. 后续依赖（不属本单）

- 图谱查询接口 `GET /internal/v1/synth/collaboration/graph`（册 §3.2：Java 门面 + Python，snapshotId 解析 graph_batch_id；本期返回空图 `reason=no_year_on_source`）——COLLAB 册 §8 归线 3 api，本单未实现
- Java Adapter `analysisType=region_innovation_collaboration` 键 + 白名单（`gkxlumen-topic-async-service`，与要素线共改 BE-1 时协调）
- FE 产业筛选 + 图谱 API 接线（`lumen-ui-topic` CollabWorkbench/SynthContextBar，册 §6/§7-8）
- C-05 换源解锁后：实算写入 node/edge/指标行；散点/图谱批号格式对齐；非空验收移 `COLLAB-C05-SRC`
- 正式库 `gkxlumenx_ads` DDL 执行属 DBA；AR-4 批次清理属运维单（含 batch_meta 引用保护）
