# TS-L2-M10-GRAPH-PY-IMPL-01 · 维护技术图谱（34–40）Python 写链实现

- 日期：2026-11-13
- 认领：`agent:algorithm` · 仓库：`repos/lumen-algo-py`（`dev`，基线 `4d55693`）
- 设计真源：`sdd/l2/TS-L2-M10-GRAPH-API.md` v2.1、`TS-L2-M10-GRAPH-DATA.md` v2.1、`TS-L2-M10-GRAPH-ARCH.md`、`TS-L2-M10-GRAPH-METRIC.md` §3、`会签/TS-L2-M10-GRAPH-L2-裁定.md`
- 状态：**实现与单测完成，未 commit / 未 push；未连库、未执行 DDL、未跑种子**。

## 1. 改动文件

| 文件 | 改动 |
|---|---|
| `vendor/entan-py/api/tech_graph_maintain_routes.py` | 重写维护写链：10 op 白名单；`_validate_ops` / `_validate_structure`；提交幂等与版本冲突；publish/rollback 在 `GET_LOCK('m10_graph_publish',10)` 下单事务执行；回执 `publish_results`、节点映射、`kind` / `snapshot_status`；版本列表/详情/回滚预览/回滚；`/current` 支持 `tech_edges[]` / `layout` 且缺 `graph_tech_edge` 时降级为空数组；impact 增 `tech_edge_count` 与 `panorama_hidden_relation_count`；软删复活；1062/1213/1205 映射；删除 `_project_nebula` / `_project_ads` / `GKX_NEBULA_MAINTAIN_SPACE`；50301 不再产生 |
| `vendor/entan-py/api/tech_graph_snapshot.py` | 新增快照公共模块：七表有序 `TABLE_SPECS`、`schema_version=m10-graph-1`、8MB/2000/50000 阈值与写入前超限判定、按版本读写、整表还原、预览/回滚共用的求差函数 `diff_tables` |
| `scripts/seed/seed_technology_panorama_score.py` | METRIC §3.4 fail-closed：运行期断言读图结果不得含工作集表名 / overlay 键；`check()` 增加源码直接读工作集表与读图总入口的拦截及自检 |
| `tests/test_technology_panorama_score.py` | 补 fail-closed 拒绝与 Nebula-only 放行用例 |
| `vendor/entan-py/test_graph_maintain.py` | 重写测试：10 op 契约、错误封套、`/current` 缺表降级、impact、校验、幂等/冲突、publish 锁与回执、add_edge 复活/重复、软删级联 operator、快照求差/超限/还原、版本端点、回滚预览/执行/守卫、原有推荐回归 |

> 未改动：`lumen_common/algorithms/tech_graph_read.py`、`lumen_algo_service/views/tech_graph_read.py`、`lumen_common/algorithms/tech_graph_overlay.py`、`tests/test_tech_graph_read.py`（另一会话负责全景叠加）。

## 2. 关键实现口径

- **单写者与事务**：Python entan-py 仍是唯一写者；publish / rollback 全程同一事务，外层 `GET_LOCK('m10_graph_publish', 10)`，`finally` 释放；不写 Nebula。
- **操作集**：`add_node` / `add_edge` / `delete_edge` + 原 7 op，共 10 个；`client_op_id` 必填，单批 ≤50；批量内临时节点 id 两段式解析。
- **幂等**：`client_batch_id` 唯一；已发布批次重放直接返回原回执；同批次不同内容 409；`base_version` 不一致拒绝。
- **版本**：`graph_version.kind` 取 `save/rollback/seed/ent`；每版发布后按七表全量写快照（含 deleted 行），超 8MB / 主表 active >2000 / 任表 >50000 则 `snapshot_status='skipped_oversize'`，发布仍成功。
- **回滚**：整表 DELETE + 显式主键 INSERT，跳过生成列 `name_cn_active` 与 `updated_at`；ADS `version_id` 重写；预览与回滚共用同一求差函数，`counts.total` 与 `results.succeeded` 同源。
- **名称唯一**：仅 active 生效，依赖 DDL 生成的 `name_cn_active` + `uk_name_cn_active`；soft-delete 后同名可重建，复活走 UPDATE。
- **审计**：`graph_change_log` 按对象写行；删除节点级联软删技术边时单独写 `object_type='tech_edge'`、`op='delete_edge'`、`after.reason='cascade'`，operator 取 `change_set.operator`（裁定 B17），不硬编码 `'py'`。
- **缺表降级**：`/current` 中 `graph_tech_edge` 不存在（1146）时仅 `tech_edges: []`，ENT 节点/实体边照常返回；impact 的 `tech_edge_count` 缺表为 0。
- **Nebula 只读**：`panorama_hidden_relation_count` 用 entan 自有会话 `session(use_space=False)` + 显式 `USE demo_gkx_chain`，space 不以 `demo_gkx_` 开头即拒绝；只做 MATCH/计数，失败返回 `null`，不挡删除。
- **错误映射**：schema 缺 → 50302；死锁/锁等待 1213/1205 → 40901；唯一键 1062（技术边）→ 40901，名称等 → 42201；其余 50001；50301 已退役。

## 3. 测试命令与结果

```bash
cd /Users/liujianfeng/Code/gkx-lumen/repos/lumen-algo-py/vendor/entan-py
/tmp/gkx-venv/bin/python -m pytest -q -p no:cacheprovider test_graph_maintain.py
# 43 passed

cd /Users/liujianfeng/Code/gkx-lumen/repos/lumen-algo-py
/tmp/gkx-venv/bin/python -m pytest -q -p no:cacheprovider --ignore=vendor
# 918 passed, 7 skipped in 234.62s
```

根目录全量包含并行会话的全景读图测试，本次全绿（`test_tech_graph_read.py` 未失败）。厂商维护测试 **43 passed / 0 failed**；根目录 **918 passed / 7 skipped / 0 failed**。

## 4. 偏差与未执行项

- **未执行**：未连接 MySQL / Nebula，未执行 DDL，未跑种子，未 commit/push（按派单要求）。
- **DDL 与种子**：单独见 `TS-L2-M10-GRAPH-SEED-L01.md`；本单只完成 Python 写链。
- **快照**：按 DATA §4 实现为“每版全量七表”，阈值前置判断；未在真实数据量下压测 8MB/2000/50000 边界。
- **`strength_auto` / `rel_code`**：写链返回与 `/current` 不输出；仅有快照/回滚内部保留，评分脚本已 fail-closed 禁止读取。
- **无契约冲突**；50301 退役、`kind` 四值、回执字段均按 API v2.1 落地。

## 5. cost 估算

约 210k input / 55k output tokens（三份设计稿 + 裁定精读、写链重写、快照模块、测试改造与全量回归）；实际耗时约 1.5 小时（含根目录全量 234s）。按平台计价约 $1.5–2 当量。
