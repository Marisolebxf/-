# DATA-POLICY-D13-POLAN-WIRE-L01 · D1–D3/组合读面 polan 全链路写出

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`（长任务总控：后续认领不必再问） |
| 说明 | 用户：为什么没改 polan？需要全链路 demo 以便前端测试 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full`（复用 policy_effect scope_type，不新表；ensure_columns 只补列） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 编码叶，未走 Headroom |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-ETL-DEMO-MOCK` 十五步时序 |
| 图 diff | C6 后加 C7 组合读面；D1–D3 写出 `metric_id` |
| 会签态 | `01-data-flow.md` 仍 `approved` |

## 范围与实现

上一叶 `DATA-POLICY-D13-DS-MENU-L01` DoD 写「不改 polan、不洗数」，只注册表+拆菜单。本叶补写出：

1. D1–D3 ADS 表加 `metric_id`；`init_schema` 对已有表 `ALTER` 补列。
2. `parse`/`match`/`simulate` 写出 `M_POLICY_TEXT_PARSE` / `MATCH` / `SIMULATE`。
3. 新步 C7 `polan.eval.ds_composite`：引导力读 C1+C6、保障力读 C2+C3，写入 `policy_effect` `ds_guide`/`ds_guard`，**不顶替 166–171**。
4. API `GET /v1/policy/analysis/guide|guard`；模型注册补 `metric_ids` + 两个 DS 模型。
5. 前端引导力/保障力页先画组合分表，再嵌原 C 页。

## 偏离

本机连 `192.168.88.43` MySQL 超时，未在 Demo 库实灌。前端要测：部署本仓 Python 后，在算法库「基础指标」点 **灌数据（重建或追加）**。

## 产物清单

- `repos/demo-algo-ent-analysis/polan/common/db.py`
- `repos/demo-algo-ent-analysis/polan/text/{parse,match,simulate}.py`
- `repos/demo-algo-ent-analysis/polan/eval/ds_composite.py`
- `repos/demo-algo-ent-analysis/scripts/run_all_policy.py`
- `repos/demo-algo-ent-analysis/api/policy_routes.py`
- `repos/demo-algo-ent-analysis/conf/cfg_model_registry.yaml`
- `repos/demo-algo-ent-analysis/conf/settings_policy.yaml`
- `repos/demo-algo-ent-analysis/tests/test_policy_ds_composite.py`
- `repos/demo-ui-system-test` GuideEval / GuardEval / BasicPage / api/policy
- `pipeline-demo-mock.md` C7 节点
- 本 handoff

## 验收证据

- `pytest tests/test_policy_ds_composite.py` → **3 passed**
- 组合步写入 `metric_id` 分别为 `M_POLICY_DS_07_POLICY_GUARD_001` / `008`
- 会签通过：调用链仍 前端 → 已有 `/v1/policy/*` → polan 写 ADS

## 问题清单

- Demo MySQL 未在本机灌上；需部署后点灌数据
- 公式权重仍 QPOL-02 临时，未改绿 D2/D3/D4

## 修改内容

见范围。未发明第二套 166–171。

## 测试结果

- 3 个 pytest 过（权重 + schema 列 + sqlite 写出组合行）
- 未跑 600 条全量 replace（本机未连上 Demo MySQL）

## 遗留风险

- 旧版 Python 镜像不认识 `analysis/guide`，新前端表会空/报未知模型，必须先发算法服务再灌数
- `CREATE IF NOT EXISTS` 旧表靠 `_ensure_columns` 补列；权限不足会在灌数 Schema 步失败

## CI/CD（必填）

- 分支：`demo-algo-ent-analysis` / `demo-ui-system-test` / `gkx-orchestration` `dev`（本叶未提交）
- commit：—
- pipeline URL / ID：未推
- K8s rollout：待推送后
- 前端测：算法库 `/policy/parse` `/match` `/simulate` `/guide` `/guard`；基础指标页灌数据

## 可观测性（建议）

- OTEL_SERVICE_NAME：未改

## 涉及文件

- 见产物清单

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 组合分在 `polan.eval.ds_composite` |
| 调用链 | ✅ 前端 → `/v1/policy/analysis/*` → ADS |
| 图谱仅 Nebula 一张 G | ✅ 未改图 |
| 可观测 | N/A |
| CI/CD | 未推 |
| demo2 不 merge lumen | ✅ |
| Java 不写算法 | ✅ |
| 数据策略 ADS 先行 | ✅ 写 Demo ADS |
| D8 / D10 | N/A |
| D9 | ✅ metric_id 写出；不改绿 |
| D12 | ✅ lumen 未动 |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 55000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.28 |
| cost_warn | green |
