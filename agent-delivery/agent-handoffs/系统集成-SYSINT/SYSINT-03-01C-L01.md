# SYSINT-03-01C-L01 · Handoff · 企业发展非 CMS 生成（两个 LLM 端点）

> **🔍 走查指引（给 human:徐滕强）**：核心逻辑只在 2 个文件——
> `lumen_common/algorithms/enterprise/narrative.py`（素材 SQL + LLM prompt + 降级，约 280 行）、
> `lumen_algo_service/views/enterprise.py`（路由 + 信封 + 入参校验，约 80 行）；
> `llm_client.py`（100 行）与 `main.py`（3 行注册）是纯接线。单测 17 例即行为规格说明，
> `tests/test_enterprise_narrative.py` 5 分钟可过。curl 证据见 §5。
> **Bugbot 审查（2026-10-24）**：首轮 3 项（2 高 1 中）+ 复审 1 项（镜像行双计）已全部修复并加回归用例，见 §10。

> **任务**：SYSINT-03-01C-L01（`task_type=feature`，E-PM-DELIVERY / SYSINT-03 子域）
> **执行**：`agent:algorithm-agent` · **监管/签收**：`human:徐滕强`
> **仓库**：`${GKX_ROOT}/repos/lumen-algo-py`（origin/dev · **本地未提交未推送**，等人工验收）
> **日期**：2026-10-23 · **强度**：ponytail full
> **契约真源**：`agent-delivery/agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-企业发展.md` §1.2/§1.3/§2.6/§2.13（已确认）
> **姊妹叶**：SYSINT-03-01A-JAVA-L01（内容管理写接口，本叶与其无代码耦合，llm 文案不进 CMS）

---

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过：OTel（复用进程级 TraceHeaderMiddleware + current_trace_id 入信封）、幂等（两端点纯读无副作用，天然幂等）、失败降级（无 Key/LLM 失败/格式不符/无数据四路全空串，实测见 §5）。新增依赖零——httpx 仓内已有（industry_embed/innov 先例）。 |

## 1. 前置勘察：复用清单 + 增量边界

### 复用（零重复造轮）

| 既有资产 | 复用方式 |
|---|---|
| `lumen_common/algorithms/chain/demo_guard.py` `connect_chain_readonly` | 直接 import：demo 库闸门 + 只读连接（链域标准入口） |
| `lumen_common/algorithms/svcan/engine.py` 码域桥接口径 | 逻辑移植（非 import，因 svcan 绑定 SVCReadDB）：`_industry_key` 取末段码、`dim.industry_cluster_map` 码→名候选、链名「任一互为前缀」匹配——本叶 `_chain_name_candidates`/`_chain_name_cond` 同口径 |
| `lumen_common/algorithms/svcan/assembly/graph.py` 供应链语义 | supplier→对方向己方供货、customer→己方为客户供货（`_collect_supply_edges` 同语义，只取统计不取边集） |
| `lumen_common/algorithms/real_data.py` 企业解析语义 | enterprise_code 兼容 org_id/统一信用码（`enterprise_base.org_id=%s OR enterprise_code=%s`） |
| `vendor/innov-py/.../llm/base.py` `OpenAICompatibleClient` | 形状复刻（generate(system,user)、glm thinking disabled、重试退避），两处差异：① response_format 不锁 json（自然语文案）② env 沿用 entan 先例 `ENTAN_LLM_*` 并加 `GKX_LLM_*` 别名 |
| `vendor/entan-py/entan/svcgraph_ops.py` 降级先例 | 无 Key → 规则兜底改读为空串兜底（本任务契约禁止规则文案，必须空） |
| `lumen_common/observability.py` | `current_trace_id()` 进响应信封 trace_id 字段 |

**不引用 `vendor/entan-py/entan/common/llm_client.py`**：该模块在本仓 0 文件（svcgraph_ops 的 import 是悬空的，真身在别处/未合入）——仿其接口自建 50 行客户端，避免引入悬空依赖。

### 增量（新建 4 文件 + 2 处接线）

| 文件 | 内容 |
|---|---|
| `lumen_common/algorithms/enterprise/__init__.py` | 包头契约注释 |
| `lumen_common/algorithms/enterprise/llm_client.py` | OpenAI 兼容纯文本客户端（~100 行） |
| `lumen_common/algorithms/enterprise/narrative.py` | 两端点业务逻辑（素材 SQL + prompt + 四路降级） |
| `lumen_algo_service/views/enterprise.py` | `/internal/enterprise/*` 路由 |
| `lumen_algo_service/main.py` | +2 行（import + include_router）、modules 列表 +1 |
| `tests/test_enterprise_narrative.py` | 13 例 FakeDB 单测（不连库不连 LLM） |

## 2. 契约对照（PORTAL-CMS-企业发展.md）

| 契约条款 | 实现 | 证据 |
|---|---|---|
| §1.2 瓶颈/结构解读 = llm，不进 CMS | `POST /internal/enterprise/chain-insight`，入参 `future_industry_code` 必填，出参 `bottleneck_narrative`+`structure_narrative` | §5 curl 1 |
| §1.3/§2.6 生态合作摘要 = llm，不设 star_ecosystem_note | `POST /internal/enterprise/eco-summary`，入参 `enterprise_code`+`future_industry_code`，出参 `cooperation_summary` | §5 curl 3 |
| §2.13 供应链摘要未生成 → 不展示、不补虚假节点 | 全降级路径返回空串；本端点零写图谱（只读） | §5 curl 4 + 单测 no_supply/no_key/llm_down 三例 |
| §1.3 图谱边不用本端点结果画（Q040 未决） | 出参仅文案字段，无边集、无节点 | 代码：narrative.py 返回体 |
| 生成失败 → 前端只隐藏文案 | HTTP 200 + code 0 + 空串（降级是契约不是异常）；仅缺参 400 | §5 curl 2/5 |
| 端点仅集群内 /internal 暴露 | `APIRouter(prefix="/internal/enterprise")`，与 svcan/chain/policy 同惯例，不经网关 | k8s api.yaml 仅 ClusterIP Service |

## 3. 关键设计取舍

| # | 取舍 | 理由 |
|---|---|---|
| 1 | 出参加 `degraded: bool` | 前端/运维可区分「正常无文案」与「系统性故障」；DB 不可达时 degraded=true 仍 200 空串（不 500，契约只要求隐藏文案） |
| 2 | chain-insight LLM 输出格式校验：缺「瓶颈：/结构：」任一行 → 整体空串 | 禁止半截文案上屏；重试 1 次后仍不符即降级 |
| 3 | 素材统计LIMIT 50 万截断、边查询按 500/批分片 | 人工智能链 18.7 万家全量可控；ponytail: 环节分布全内存 dict 聚合，链超 50 万家时需改 SQL GROUP BY，升级路径明确 |
| 4 | enterprise_code 入参兼容 org_id 与统一信用码 | 契约 §0 企业绑定用 enterprise_code，但上游 Java 可能传 org_id；`enterprise_base` 双列等值一次解析 |
| 5 | 无 LLM Key 时直接空串（不再试规则生成） | 契约「禁止编造」优先级高于可用性；entan 的规则兜底模式在此不适用 |

## 4. 测试结果

### 单测（`python3 -m pytest tests/test_enterprise_narrative.py -q`）

18 passed。覆盖：两端点正常路径、缺参 400、上游无数据空串、LLM 异常降级、
LLM 输出格式不符拒绝、DB 异常 degraded=true、信用码入参解析、无供应链边空串、无 Key 降级、
供需方向按列解析（出/入两个视角）、镜像行只计一次、连接关闭前完成企业名解析（真实 pymysql 关闭语义）。

**双环境验证**：本机带 Key 与 `env -u OPENAI_API_KEY`（模拟 CI 无 Key）均 18 passed。

### 全仓回归（同 CI `py:test` 口径）

`python3 -m pytest -q --ignore=vendor` → **486 passed, 6 skipped**（跳过项为既有 live 库标记用例），零回归。

## 5. curl 验证（真实入参出参）

本地起服（与集群同源 demo MySQL 10.50.11.76）：

```bash
cd ${GKX_ROOT}/repos/lumen-algo-py
LUMEN_ALGO_MYSQL_HOST=10.50.11.76 LUMEN_ALGO_MYSQL_PASSWORD='***' \
GKX_LLM_BASE_URL=https://api.deepseek.com/v1 GKX_LLM_API_KEY=$KEY GKX_LLM_MODEL=deepseek-flash \
  python3 -m uvicorn lumen_algo_service.main:app --host 127.0.0.1 --port 8377
```

**① chain-insight 成功路径（真实 LLM 生成）**

```bash
curl -s -X POST http://127.0.0.1:8377/internal/enterprise/chain-insight \
  -H 'Content-Type: application/json' -d '{"future_industry_code": "INB1309"}'
```

```json
{"code":0,"msg":"ok","data":{"bottleneck_narrative":"链主39144家，占链上企业约20.9%；四环节企业数均在4.66万—4.70万家，最大最小差438家，数量层面未见明显短板，瓶颈更可能体现为链主对四环节的协同效率而非环节企业供给不足。","structure_narrative":"四环节企业数合计186964家，与链上企业数一致；行业应用47035家、数据标注46731家、算力芯片46601家、算法框架46597家，分布接近，行业应用最多、算法框架最少，链结构呈均衡布局。","degraded":false}}
```

**② chain-insight 缺参**

```bash
curl -s -X POST http://127.0.0.1:8377/internal/enterprise/chain-insight \
  -H 'Content-Type: application/json' -d '{}'
```

```json
HTTP 400 {"code":1,"msg":"future_industry_code 必填","data":null}
```

**③ eco-summary 成功路径（真实 LLM 生成，真实供应链企业）**

```bash
curl -s -X POST http://127.0.0.1:8377/internal/enterprise/eco-summary \
  -H 'Content-Type: application/json' \
  -d '{"enterprise_code": "00016d56834c21a9a937795b5a9190d6", "future_industry_code": "INB1309"}'
```

```json
{"code":0,"msg":"ok","data":{"cooperation_summary":"目标企业拥有供货方向关系1条、采购方向关系1条，去重合作对象3个；代表关系显示其作为客户方（customer）与合作对象相连。","degraded":false}}
```

**④ 降级路径（LLM 401 实测，非 mock）**：无 Key/错 Key 时同一入参返回
`{"code":0,"data":{"bottleneck_narrative":"","structure_narrative":"","degraded":false}}`——
服务日志留 `enterprise llm degraded: 401 Unauthorized`（observability JSON 日志带 trace）；
未知企业（`org-not-exist-xyz`）返回 `cooperation_summary:""`。前端按 §2.13 只隐藏文案。

**集群注意**：现网 Pod 的 LLM 环境变量尚未注入（k8s/api.yaml 无 GKX_LLM_*）。集群内已验证
`10.50.11.76:3306` 可达，但出口到 bigmodel/deepseek 的连通性与 Key 分发需 devops 确认；
未注入前两端点行为 = ④ 空串降级（安全态，不会编造）。

## 6. 数据面勘察记录（供联调参考）

| 事实 | 值 |
|---|---|
| future_industry_code 真源 | `dwd.industry_chain.chain_id`，`future_industry_flag=1 AND chain_tier='L0'`：INB1801 未来制造 / INB1802 未来信息 / INB1803 未来能源 / INB1804 未来空间 / INB1805 未来健康 |
| 企业链归属现状 | `enterprise_industry_chain` 集中在旧码域：INB1309 人工智能(18.7万)、INB2503 生物医药(5267)、INB1204 机器人(1110)、INB1354 具身智能(921)、INB2505 合成生物(51)；**INB1801~1805 零覆盖** |
| 兜底 | 码域桥接（dim.industry_cluster_map + 互前缀匹配）后 INB1801 候选名「未来制造」仍无企业命中 → 空串（诚实空态，与 Q062 代理口径一致） |
| 演示可用入参 | 演示/联调用 `INB1309`（人工智能）等有数据的链码；未来产业 L0 等数据工厂回填后自动生效 |
| 供应链 | `enterprise_supply_chain` 共 85,791 条（customer 43,748 / supplier 42,043），本样例企业 1 出 1 入 |

## 7. 架构合规自检

| 铁律 | 自检 |
|---|---|
| 1 算法只在 Python | ✅ 本叶全部在 lumen-algo-py |
| 2 调用链 前端→Java→Python /internal | ✅ 仅 `/internal/*`，不经网关；Java 侧对接属后续叶 |
| 3 NebulaGraph | ✅ 未触图谱（Q040 未决，本端点不产边） |
| 4 可观测 | ✅ 复用进程 OTel；trace_id 入响应信封；降级留结构化日志 |
| 6 demo2 只读 | ✅ 未动 demo 仓 |
| 12 demo/lumen 隔离 | ✅ 只改 lumen-algo-py；vendor 引用只读 |
| 13 对象存储 | ✅ 不涉及 |
| D9 数据血缘 | ✅ 出参为 LLM 文案非统计指标，不挂 metric_id（契约 §1.2 明示 llm 不算指标）；文案内数字均来自 SQL 事实注入 prompt |

## 8. 遗留风险 / 移交事项

1. **集群 LLM 环境变量未配**（见 §5 注意）：需 devops 在 k8s Secret 注入 `GKX_LLM_BASE_URL/GKX_LLM_API_KEY/GKX_LLM_MODEL`（或 ENTAN_LLM_* 同义）。未配前端点恒空串（安全但无文案）。
2. **demo 库无 LLM Key 也属预期态**：契约空态 = 隐藏文案，联调时若要看真实文案需临时注入 Key。
3. `vendor/entan-py/entan/common/llm_client.py` 悬空 import（svcgraph_ops/polan 引用不存在的模块）是**既有问题**，本叶未修（超范围）；已在本叶自建客户端避开。
4. 未来产业 L0（INB1801~1805）企业归属数据待数据工厂回填；回填前该 5 码恒空串，不是 bug。

## 9. 完工状态

- registry：`in_progress` → `integration`（AV-0：本 handoff + evidence 已备）；**禁转 done，签收权 human:徐滕强**
- 代码：本地工作区 **未 commit 未 push**（人工验收闸门 2026-10-20）；验收通过后由监管人安排 push origin/dev
- 变更清单：`git status` → 4 新文件 + main.py 修改（见 §1 增量表）

## 10. Bugbot 审查与修复记录（2026-10-24）

首轮 Bugbot（uncommitted changes）3 项发现，全部确认成立并当轮修复：

| # | 级别 | 发现 | 修复 | 回归用例 |
|---|---|---|---|---|
| 1 | High | `eco_summary` 在 `db.close()` 后才调 `_org_names`，真实 pymysql 关闭后查询抛错被 `_org_names` 内 `except` 吞掉 → 企业名恒空、prompt 退化为裸 org_id | `_org_names` 调用移入 `try` 块（close 前） | `test_org_names_resolved_before_close`（fake DB close 后 query 抛错，断言 close 前 names 已解析且 prompt 含人读名） |
| 2 | High | 单测 monkeypatch 打在 `llm_client` 模块，但 `narrative` 是 from-import 绑定，patch 无效 → CI 无 Key 环境 3 例必红；本机因环境已有 OPENAI_API_KEY 碰巧全绿 | patch 目标改为 `narrative.has_llm_key`；删除对 `llm_mod` 的无效引用 | 全文件双环境（带 Key / `env -u`）跑通；`test_llm_text_no_key_returns_empty` 直测无 Key 分支 |
| 3 | Medium | `_collect_supply_edges` 方向统计只按行内 `relation_type` 计数，目标企业在 `related_org_id` 列时方向颠倒 → 供需事实说反 | 按「目标企业所在列」归一方向：supplier 行=related 供货给 org、customer 行=org 供货给 related（同 svcan graph.py 语义）；samples 归一为 (供货方, 采购方)；partners 排除目标企业自身 | `test_supply_direction_resolved_by_column`（out 视角）+ `test_supply_direction_inbound_when_target_is_org_column`（in 视角） |
| 4 | Medium | （全量复审新增）去重键是原始三元组，镜像行 `(A,B,customer)`/`(B,A,supplier)` 归一化后是同一条供货关系 A→B 却各计一次 → out 双计，且与 samples 按方向对去重的口径自相矛盾（uk_supply_chain 不拦镜像存储） | 去重键改为归一化方向对 `(supplier, customer)`；真实双向互供 A→B 与 B→A 是不同方向对，不受影响 | `test_mirror_rows_counted_once`（镜像两行 → out=1、partners=1、样例恰 1 次） |

修复过程中发现并修正 1 处测试自身错误：`(C, A, supplier)` 行对 A 是出度（A 供货给 C），初版断言方向理解反了，已按 svcan 真实语义改正。

**DB 不可达降级的意外端到端验证**：复检时 `10.50.11.76` 网络不可达（前日可达，环境变化），两端点返回
`200 + code 0 + 空串 + degraded:true`——契约「隐藏文案」行为在真实 DB 故障下成立。
