# ALGO-LIB-ODS-MOCK-POLICY-L01 · 政策 Mock 列表搜索 + 列头/码值中文

> 对照 SPEC `ALGO-LIB-ODS-MOCK-SPEC-L01.md` §政策；只升级现页 `/policy/mock`，不重做攒货。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 用户授权连跑；本会话 algorithm-agent 独自完成，不问人。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短 diff：复用现页/现 API，只补 `list_policies` SQL AND 过滤 + 搜索条 + 列头/码值。未用 YAGNI 跳过调用链、X-Trace-Id、空表诚实空态。未改 LLM 填表 / 差集追加 / rebuild。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶范围已锁 SPEC，无需压缩检索。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（本叶不改存储流图拓扑） |
| 图 diff | 写库方仍 = Demo ODS `demo_gkxlumenx_ods.dwd_policy_base`；禁止写 DWD/ADS/正式库。 |
| 会签态 | 抄源：POLICY `01-data-flow.md` 已 `approved`。 |

## 范围与实现

对照 SPEC 已锁政策行：

1. 表：`demo_gkxlumenx_ods.dwd_policy_base`，业务键 `id`，API 仍暴露 `policy_id`。
2. **升级现页** `/policy/mock`，不新建菜单。
3. 搜索走服务端 AND（查询参数可空）：`q_title` / `q_ministry` / `q_publish_code` / `q_rank` / `q_type`。禁止前端只滤已拉 200 条。
4. 列头中文：政策ID / 标题 / 发布机构 / 发布日期 / 来源标记 / 层级 / 类型 / 状态。
5. 码值：`rank` 国家级/省级/市级/区县级（数字 1–4 与中文互认）；`ingest_status` pending→待追加 / ingested→已入库；`type` 自由文本原文。详情对话框未改，仍可见原始码。
6. 空表：HTTP 200 + `list=[]`。

未做：ENT/CHAIN/SVC 叶；`lumen-ui-*`；seed/矩阵 YAML；replace 灌 600 条。

## 偏离说明

无范围偏离。`publish_organization` 仍在列表 JSON 中回传（= `ministry`），避免旧调用方断裂。

## 产物清单

| 产物 | 路径 |
|------|------|
| Python 搜索 SQL | `demo-algo-ent-analysis/polan/mockgen/incr.py`（`policy_list_where` + `list_policies`） |
| API 查询参数 | `demo-algo-ent-analysis/api/policy_routes.py` `GET /v1/policy/mock/policies` |
| 前端 API | `demo-ui-system-test/src/api/policy/index.ts` |
| 现页搜索条 + 中文列 | `demo-ui-system-test/src/views/policy/pages/PolicyMockPage.vue` |
| 本 handoff | `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-ODS-MOCK-POLICY-L01.md` |

## 测试结果

- 本地 `python -c "from polan.mockgen.incr import self_check; self_check()"`：**OK**（`id=MOCK20260901e14d1f`）。断言覆盖：`policy_list_where` 四字段 `LIKE %s` + `rank IN (...)`；`q_title=___NOHIT___` → `list=[]`；标题命中返回刚写入行。
- SSH `10.50.69.111` 现网 `demo-platform-entan-py`（ClusterIP `10.97.63.95:8000`，镜像仍为 push 前）：
  - `GET /v1/policy/mock/policies?limit=5` → **HTTP 200**，`data.list=[]`，`ods_count=0`，`X-Trace-Id=a00c61dc869ff6cd911e4d887e8946ed`
  - 带 `q_title=___NOHIT___` 仍 200 + 空列表（现网进程尚未滚本叶代码；空态与 SPEC 一致）
- **50100 未点验**：本机未开联调台；K8s 未见 NodePort 50100。本地验证通过，K8s 待滚后再点 50100 搜索条。

## 遗留风险

- 政策 ODS 现网仍为 0 行：搜索命中需有数后回归；空态已验收。
- 本叶 push 后需等 `demo-platform-entan-py` + `demo-ui-system-test` CI rollout，现网 API 才会真正吃 `q_*`。

## CI/CD（必填）

- 分支：`dev`（两业务仓 + 编排仓 handoff）
- commit：`demo-algo-ent-analysis` `5c2a9e5bc515b261ee25bb41f8609a9eff3e7f70`；`demo-ui-system-test` `a7a00d4e8c80ca7d29a69591afcb2331204203b8`
- pipeline URL / ID：push 后由 GitLab 触发；本叶未等绿
- 部署 namespace / 镜像 tag：`dev` / 待滚
- K8s rollout：待 push 后自动滚；本叶收尾时现网仍是旧镜像
- dev 测试 URL / 命令与结果：见上「测试结果」；50100 未打

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 `demo-platform-entan-py`
- traceId（dev 抽样）：`a00c61dc869ff6cd911e4d887e8946ed`
- Tempo / Loki：现网响应带 `X-Trace-Id` + `traceparent`；前端 `request.ts` 仍自动注入，未漏

## 涉及文件

- `demo-algo-ent-analysis/polan/mockgen/incr.py`
- `demo-algo-ent-analysis/api/policy_routes.py`
- `demo-ui-system-test/src/api/policy/index.ts`
- `demo-ui-system-test/src/views/policy/pages/PolicyMockPage.vue`
- 本 handoff

## 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ 过滤在 `incr.list_policies` SQL；Java 不写 ODS |
| 2 | 调用链 前端→Java→Python | ✅ 50100 `/policy/**` → 网关 → `/v1/policy/mock/**`；未直连 Python |
| 3 | 图谱 NebulaGraph | ✅ N/A（本叶不写图） |
| 4 | 可观测性 | ✅ 沿用 `X-Trace-Id` / `traceparent` |
| 5 | CI/CD | ✅ push `origin/dev`；未 force |
| 6 | demo 不污染 lumen | ✅ 只改 demo 两仓 + 编排 handoff |
| 7 | 方案 A | ✅ Java 不直连 ODS |
| 8 | 数据走 ADS | ✅ Mock 只读/写 Demo ODS 列表；本叶不写 DWD/ADS |
| 9 | D8 | ✅ 50100 Element Plus 现页增强，未改 Arco |
| 10 | D9/D10 | ✅ N/A（联调台 Mock 工作台，非指标卡页） |
| 12 | D12 lumen 不调 demo | ✅ 禁止改 lumen-ui-* |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 82000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.95 |
| cost_warn | green |

## 明确未做

- 未重做 LLM 填表 / 差集追加 / rebuild
- 未灌 replace 600 条
- 未开工 ENT/CHAIN/SVC
- 未点验 50100 页面（K8s 待滚）
