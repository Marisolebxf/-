# LUMEN-POLICY-PY-BOOT-L01 · polan 迁入 lumen-algo-py `/internal/policy`

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-PY-B-总派单.md`](./LUMEN-POLICY-PY-B-总派单.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h；本叶不做 HARNESS |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短工作 diff：不新开 `vendor/polan` 镜像/Deployment，as-built 挂现网已 COPY 的 `vendor/entan-py/polan`；未改算子 `run()` / 打分 / 抽词；未做分片 harness |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 对照复制 + settings，无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | Python 生产者由 `demo-algo-ent-analysis polan` 改为 `lumen-algo-py vendor/entan-py/polan`；Java Feign 标 `/internal/policy`；联调台 `demo-ui-system-test` → demo polan 改虚线。工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改；`gkx_policy` 仍虚线废作 |
| 会签态 | `approved`（`01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

- 对照仓 `demo-algo-ent-analysis` @ `6b3e47d01373782cdcbe22482099a9c9da7434da` **复制**（禁止 git merge）。
- as-built 路径：`lumen-algo-py/vendor/entan-py/polan`（Dockerfile.entan-api / -worker 已 `COPY polan`；镜像 `gkxlumen-entan-py-*` / Deployment `gkxlumen-platform-entan-py`）。总控 `vendor/polan` 不另起树。
- settings：`demo_gkxlumenx_ods/dwd/ads`，`nebula.space=demo_gkx_chain`，`vid_length=80`。非该 space 运行时拒绝。
- 对外专题链路仅 `/internal/policy/**`。`/v1/policy/**` 仍挂在 router 上供联调台；`ENTAN_EXPOSE_PUBLIC_API=0` 时 HTTP 层 404。**专题前端禁用 `/v1`**。
- 挂接 VID：图上链码（`chain:` / `segment:` 等）；`match_industry_anchors` 禁止名称当 VID。本叶未改该函数体（与 demo SHA 相同）。
- 本叶 **不做** HARNESS 分片。
- OTel：镜像 `ENTRYPOINT opentelemetry-instrument` + 已有 `TraceHeaderMiddleware`；`polan.graph.ops` 调用点外 span 随 demo 一并迁入，算子公式未改。

## 修改内容

| 路径 | 动作 |
|------|------|
| `vendor/entan-py/polan/**` | 对照复制（含 `focus_one` / `ops` / `nebula_query` / `metrics` / `ods_sync`） |
| `vendor/entan-py/conf/settings_policy.yaml` | `space: demo_gkx_chain` |
| `vendor/entan-py/api/policy_routes.py` | 同步 `/internal/policy/**` |
| `vendor/entan-py/conf/cfg_model_registry.yaml` | 补 POLICY_DS_GUIDE / GUARD |
| `vendor/entan-py/scripts/run_all_policy.py` 等 | 同步灌数脚本 |
| `vendor/README.md` · `SOURCE.txt` | as-built 说明 + 源 SHA |
| `agent-delivery/data/data-design/storage/POLICY/01-data-flow.md` | Python 边改指 lumen-algo-py |

## SOURCE.txt / 算子冻结自检

| 项 | 值 |
|----|-----|
| 对照仓 commit | `6b3e47d01373782cdcbe22482099a9c9da7434da` |
| `polan/SOURCE.txt` SHA256 | `BE36659DCA4157845E3CE5A4579C25DA8D6851504F593B269CD07644D2967327` |
| eval/basic/graph/text/models vs demo | 逐文件 SHA256 **SAME**（含 `focus.py` = `C10C498F…C4B55D`） |
| 未改 | 算子 `run()` / 打分 / 抽词函数体；无一次 load 全表优化 |

遗留注释：demo 源 `polan/__init__.py`、`eval/focus.py` 文档字符串仍写 `gkx_policy`（复制原样、未改函数体）。**运行时** `SPACE` / `settings` / `conf()` 均为 `demo_gkx_chain`。

## 测试结果

本地（`PYTHONPATH=vendor/entan-py`）：

- `python -m compileall -q polan api/policy_routes.py` → 0
- `settings()['nebula']['space']` = `demo_gkx_chain`；ods/dwd/ads = `demo_gkxlumenx_*`
- `GKX_NEBULA_SPACE=gkx_policy` → `RuntimeError` 拒绝
- `TestClient GET /internal/policy/status` → **HTTP 200**，`backend=mysql`，ADS `policy_focus=47082` 等与 A 退出门一致

现网验证（镜像滚动后）：

```text
kubectl -n dev exec deploy/gkxlumen-platform-entan-py -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/internal/policy/status').read().decode()[:400])"
```

entan 镜像 **默认不随 api+worker 自动发**（需 `FULL_PIPELINE=true` 或手动 `.deploy-set-image`）。Java 可继续打现网 Deployment；本叶代码已在 `origin/dev`。

## CI/CD（必填）

- 分支：`lumen-algo-py` `origin/dev`
- commit：`0338a489d57b68c95d44faeab88e05e956eafb4a`
- pipeline：push 后 GitLab `dev`；`image:entan-api` / `image:entan-worker` 默认 manual
- 部署：`gkxlumen-platform-entan-py`（ns `dev`）
- 本叶未改 helm JDBC、未 CREATE SPACE、未写 `gkx_chain`

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-entan-py-api`（Dockerfile）
- HTTP：`TraceHeaderMiddleware` → `X-Trace-Id` / `traceparent`
- 图谱写入：`gkx.polan.policy.graph` tracer（`ops.execute` 外包一层，公式未改）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ |
| 前端→Java→Python `/internal/*` | ✅ 本叶提供 `/internal/policy/**` |
| 图谱 Nebula `demo_gkx_chain` | ✅ 禁 `gkx_policy` 目标态、禁写 `gkx_chain` |
| 可观测 | ✅ instrument + TraceHeader |
| CI/CD | ✅ 推 `origin/dev`；entan 制品独立 |
| demo2 不 merge lumen | ✅ 对照复制 |
| 共享聚合 / Java 不直连 nGQL | ✅ |
| 数据策略 ADS `demo_gkxlumenx_*` | ✅ 未改正式 `gkxlumenx_*` |
| D8 / D10 | N/A 无 UI |
| D9 8 件套 | N/A 本叶不改口径 |
| D12 lumen 不调 demo **服务** | ✅ 本叶是 Python；数仓共用 demo 源是总控 §0 #6 |

## 遗留风险

- 专题 Job 分片留给 `LUMEN-POLICY-PY-HARNESS-L01`。
- 现网 `gkxlumen-platform-entan-py` 需滚到本 SHA 后 Java 才能吃到新 `/internal/policy/graph` 写入与 `focus_one`。
- `/v1/policy` 仍在代码中；专题禁用，联调台可留。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 95000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.64 |
| cost_warn | green |
