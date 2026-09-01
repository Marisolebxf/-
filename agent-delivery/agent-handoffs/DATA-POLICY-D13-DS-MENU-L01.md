# DATA-POLICY-D13-DS-MENU-L01 · D1–D3 注册 + DS-07/11 管线覆盖 + 算法库菜单

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`（长任务总控：后续认领不必再问） |
| 说明 | 用户指令：4 条 DS-07/11 本管线要算；D1–D3 注册指标库；demo-ui-system-test 政策算法库拆菜单 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full`（菜单拆分复用 TextAnalysis + 两张组合页嵌已有 C 页，不另写算法/不灌数） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶改 registry YAML + 文档 + 算法库菜单，未走 Headroom |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-ETL-DEMO-MOCK` §2.1 |
| 图 diff | 叶指标图加 D1–D3 三节点；「本管线不覆盖 4」改为「展示页组合读面 4」；S1 `POLICY-STORAGE-FLOW` **未改** |
| 会签态 | `01-data-flow.md` 仍 `approved`；本文件 `status: as-built` |

## 范围与实现

对照 `run_all_policy` as-built：

1. 注册 `M_POLICY_TEXT_PARSE` / `M_POLICY_MATCH` / `M_POLICY_SIMULATE` 入 seed + 矩阵（D1=`draft`，D2/D3/D4 不改绿）。
2. 4 条 DS-07/11 从「不覆盖」改为组合读面：D1 摘要 / D3 推演 / C1+C6 引导力 / C2+C3 保障力；**不顶替 166–171**。
3. `demo-ui-system-test` 政策算法库菜单拆出 parse / match / simulate，并增加引导力 / 保障力。
4. 更新 `pipeline-demo-mock.md` §2.1。**不洗数、不改 polan、不给 D 三表加 `metric_id` 列。**

授权：直接编辑 `metrics/registry` YAML（公约 §6，沿用 `DATA-POLICY-METRIC-REGISTRY-FIX-L01` 监管人授权；副本改完再拷回）。

## 偏离

无。旧稿把 4 条 DS 标「不覆盖」、D1–D3「有表无叶」——按本叶用户指令纠正。`srs_map` 未给新三叶补 sidecar（不在本叶 DoD；`metric-srs-export` 另跑）。

## 产物清单

- `agent-delivery/metrics/registry/cfg_metric-POLICY-seed.yaml`（35 条）
- `agent-delivery/metrics/registry/metric-readiness-matrix-POLICY.yaml`（35 条，与 seed 闭合）
- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-demo-mock.md` §2.1
- `agent-delivery/data/data-design/storage/POLICY/CHANGELOG.md`
- `repos/demo-ui-system-test/src/views/policy/policyMenuConfig.ts`
- `repos/demo-ui-system-test/src/router/index.ts`
- `repos/demo-ui-system-test/src/views/policy/components/TextAnalysis.vue`（`meta.tab` + 指标挂正）
- `repos/demo-ui-system-test/src/views/policy/components/policyHelp.ts`
- `repos/demo-ui-system-test/src/views/policy/components/GuideEval.vue`
- `repos/demo-ui-system-test/src/views/policy/components/GuardEval.vue`
- 本 handoff

## 验收证据

- MCP `metric-query domain=政策` → **35** 条；seed 35 / 矩阵 35 / 差集空
- 新叶 D1=`draft`、D4=`mock`：`M_POLICY_TEXT_PARSE` / `MATCH` / `SIMULATE`
- 4 条 DS seed `source_tables` 已指向本管线 ADS，不再 `pending_ods`
- 菜单：`/policy/parse` · `/match` · `/simulate` · `/guide` · `/guard`；旧 `/policy/text` 重定向到 parse
- 会签通过：覆盖表与 as-built / 用户定向对齐，待 `human:淮政玮` 签收

## 问题清单

- D1–D3 与 4 条 DS 的 formula 仍 `pending_cosign`（唐绍祖）/ QPOL-02/03，未改绿
- 新三叶 `srs_map=false`，需求来源 Excel 需另跑 `metric-srs-export`
- 算法库菜单改动未提交、未起本地 Vite 做浏览器点选（本机未挂 demo-ui-system-test 开发服）

## 修改内容

- seed/矩阵补 3 叶、改 4 条 DS 读面说明
- §2.1：32→35；叶 22 + 身份 9 + 组合读面 4
- 政策算法库拆 D1–D3 菜单 + 引导力/保障力组合页

## 测试结果

- 35 = 22 + 9 + 4 算术闭合
- Python YAML 解析 seed/矩阵均 35 且 ID 对齐
- 未改 `polan`、未灌数

## 遗留风险

- 组合读面没有独立 ADS `metric_id` 行，UI 只是嵌已有 C/D 页；权重未会签前数字不能当终态 KPI
- Vue 同组件多路由复用 TextAnalysis，靠 `route.meta.tab` 切默认页签

## CI/CD（必填）

- 分支：`gkx-orchestration` / `demo-ui-system-test` `dev`（本叶未提交，待用户指示）
- commit：—
- pipeline URL / ID：文档+注册表+菜单，未推 CI
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：MCP `metric-query domain=政策` matched=35

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A（未改业务运行时）

## 涉及文件

- 见产物清单

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 未改 polan |
| 调用链 | ✅ 菜单页仍走 Java/已有 `/v1/policy/*` |
| 图谱仅 Nebula 一张 G | ✅ 未改图 |
| 可观测 | N/A |
| CI/CD | 本叶未推 |
| demo2 不 merge lumen | ✅ 只改 demo-ui-system-test |
| Java 不写算法 | ✅ |
| 数据策略 ADS 先行 | ✅ 读已有 ADS，不洗数 |
| D8 / D10 | N/A（算法库后台 Element Plus，未改视觉 token） |
| D9 指标 8 件套 | ✅ 新叶入 seed+矩阵；D2/D3/D4 不改绿；匹配列错挂 INDUSTRY_FIT 已纠正为 MATCH |
| D12 | ✅ lumen 未动 |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 72000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.35 |
| cost_warn | green |
