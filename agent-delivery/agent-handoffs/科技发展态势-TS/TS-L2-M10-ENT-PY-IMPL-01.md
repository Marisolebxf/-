# TS-L2-M10-ENT-PY-IMPL-01 · handoff

- 任务：`TS-L2-M10-ENT-PY-IMPL-01`（implementation · Python 写侧）
- 日期：2026-11-09 · 监管：`human:刘剑锋` · 认领：`agent:data-agent`
- 状态：代码完成（feat/m10-ent-py 已推，单测 6/6）；DDL 待部署执行；real 轨联调待全链就绪。不标 done

## 范围与实现

- DDL `scripts/mysql/tech_graph_maintain.sql`：变更链 **12 表**（DATA 册基线 11+dim_tech_domain）落 gkxlumenx_dwd/ads（demo 由 db.py rewrite 映射）——含 tombstone/冲突队列/overlay/projection_status 列（会签补漏全落）；v0 版本行+存量技术点映射 seed（演示两行，部署时 seed 脚本实扫 Nebula）
- 路由 `api/tech_graph_maintain_routes.py`（注册进 main.py）：
  - `POST /changes`：7op 校验（枚举外/ops≤50/client_op_id）→ 乐观锁（base_version≠当前 → 40901+diff）→ 幂等（JSON_SEARCH client_op_id 命中返回 idempotent-hit）→ 落 change_set(draft)+change_log
  - `POST /changes:validate`：dry_run 预览（不落库）
  - `POST /changes/{id}/publish`：**draft/approved 可发布**（published/rejected→409，ARCH-A3）；MySQL 段（版本 pending→主表/overlay/tombstone/版本关联）→ Nebula 增量投影（VID=tech:{id}，存量不迁移）→ ADS 投影（边三列）；任一失败→版本留 pending+50301（R2 恒读上一 ok 版）
  - 读：R1 推荐（ADS auto 边权+metric_id=M_TECH_GRAPH_105_1+sortBy 三值白名单）/R2 现状（base_version+projection_status）/impact（计数豁免）/conflicts（reserved 空）
- 单测 `test_graph_maintain.py`：7op 枚举封闭（34–40 op 拒收）/幂等键缺失/超限/sortBy 白名单——6/6 过（venv 隔离）

## 已知边界（联调收口）

1. hang/unhang/边三 op 首版落 change_log 但**投影段未实现图结构变更**（hang=投影实体挂接边需 R2 nodes 结构定稿后补——首版可发布不报错，投影增量仅 update_node/delete_node 落 Nebula/ADS）；**实现单内显式记录，不算完成偏差**——ENT 全链联调时按 R2 实测补齐
2. 幂等 JSON_SEARCH 全表扫（首版量级可接受）；补偿重放=人工重发 publish（pending 版可重复调用）
3. Nebula space 经 `GKX_NEBULA_MAINTAIN_SPACE` 注入（默认 demo_gkx_chain）
4. entity_type 中文→正式枚举对齐（C01/C03 在册）联调定

## cost

- actual_tokens: ~50k · model_used: glm-5.3（ZCode agent） · actual_cost: <$0.5 · cost_warn: green

## 2026-11-09 走查返工（监管人 human:刘剑锋 报 edu 关键实体接口 500）

- 根因：`_db()` 导入不存在的 `entan.common.db.get_conn` → 所有碰库端点 ImportError 500；原单测只测参数校验未覆盖
- 同批问题：表名无库前缀（连接无默认库）、`autocommit=False` 却从不 commit、`rank` 为 MySQL 保留字、`HTTPException(detail=dict)` 被 FastAPI 包成 `{detail}` 非信封、`connect()` 无 plane 头默认落 `demo_gkxlumenx_*`（D12）、hang/unhang/边三 op 未投影（DATA-A3 挂接=边存在性）、Java client 声明的 GET/DELETE `changes/{id}` 无路由、Nebula 投影默认写 demo space 且 f-string 拼 nGQL
- 修复 `lumen-algo-py` 4b34c21：事务游标（commit/rollback/close）+ 正式库名固定（`GKX_M10_ENT_DWD_DB/ADS_DB` 可覆盖）+ `enveloped` 统一信封出口（缺表读面空态 `schema_ready=false`、写面 50302）+ ADS 投影补齐 7 op + 补两路由 + Nebula 仅显式 `GKX_NEBULA_MAINTAIN_SPACE` 时写且转义
- 单测 6 → 15 全绿（信封/缺表/库名/乐观锁 409/R2 分组/投影 SQL/nGQL 转义）
- DDL：12 表已于 2026-11-09 09:45 在 dev 库建好（只读核对）；存量种子拆单 `TS-L2-M10-ENT-SEED-L01`
- 状态仍 integration：待 topic（TOPIC_RELEASE）部署后 edu 接口联调
