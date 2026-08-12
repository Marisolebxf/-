# 管道 · DWD → Elasticsearch

> S2 回填

## 意图

`enterprise_base` 等 DWD → ES 索引（检索别名 `gkx_enterprise`）。

## 脚本指针（仓内真实入口）

| 项 | 路径 |
|---|---|
| 仓 | `${GKX_ROOT}/repos/lumen-etl-es-py` |
| README | `lumen-etl-es-py/README.md` |
| CLI | `scripts/run_etl.py` · `scripts/create_enterprise_index.py` |
| 模块示例 | `etl/modules/reg_info.py`（从 `enterprise_base` 抽字段） |
| API | `app/main.py` → `/internal/etl/*` |
| 设计 | `data-design/企业/企业搜索-ES索引设计.md` · `企业搜索-ES更新机制.md` |
| storage 契约 | [`../stores/elasticsearch/`](../stores/elasticsearch/) |

## 调度

批：DWD 门禁通过后触发；失败不发布半成品索引（见流图失败语义）。具体 cron → 并入 OPEN-ENT-FLOW-01。
