# DATA-ENT-ES-FORMER-L01 · 曾用名写入现有 mapping

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |

## 范围与实现

新增模块 `former_names`：读 `enterprise_history_name.history_name`，按 `org_id` 去重后整组替换 ES 已有字段 `former_names`。不新建 mapping 字段，不改别名 `gkx_enterprise`，不建文档（`creates_docs=False`）。

触发：`POST /internal/etl/modules/former_names/sync`。脚本 id：`gkx_former_names`。

## 产物清单

- `etl/modules/former_names.py`
- `etl/scripts.py` / `etl/modules/__init__.py`
- `tests/test_former_names.py`
- 派单包 `12` 改为可触发

## 验收证据

- `python3 -m py_compile` 三文件通过
- 去重逻辑：同名只留一条，空串丢弃
- `lumen-svc-platform` 企业 API 未改

## 偏离

- 本叶只加模块，不代跑全量 sync（需 ES stored script 注册 + 值班触发）

## 测试结果

- compile 通过；本机无 pytest/yaml，未跑框架测试

## 遗留风险

- 上线后需 `put_scripts` 再触发模块；未跑不等于曾用名已灌绿

## CI/CD

- 分支：`lumen-etl-es-py` `origin/dev`
- pipeline：随仓 CI
- K8s：等 CI rollout

## Cost 回填

见下节。

## 成本

- actual_tokens：15000
- model_used：cursor-grok-4.6
- actual_cost：0.08
- cost_warn：green

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 调用链 | ✅ 只加 Python `/internal` 模块 |
| 图谱 | ✅ 未写图 |
| 可观测性 | ✅ 沿用现网 ETL |
| CI/CD | ✅ 推 `origin/dev` |
| demo2 merge | ✅ 无 |
| D12 | ✅ 未调 demo 服务 |
| ES 字段名 / 别名 | ✅ 沿用 `former_names` |
| Java API | ✅ 零 diff |

## 涉及文件

- `etl/modules/former_names.py`
- `etl/scripts.py`
- `etl/modules/__init__.py`
- `tests/test_former_names.py`
