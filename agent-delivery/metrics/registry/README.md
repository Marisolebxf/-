# metrics/registry/ —— 指标身份证 + 就绪度（机器真源）

> 模型：`../../data-lineage-policy.md` §2（8 件套 v1.5 含 `algorithm_type`）+ §2.3（四维就绪度）。
> **FE / API / 镜像脚本只认本目录 YAML**（不再认 `metrics/` 根上的同名文件）。

| 文件                                  | 角色                                                                                                                                                       | Owner                                                   |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `cfg_metric-{域}-seed.yaml`         | 8 件套注册表（齐备态 9 项；OPEN 允许`D1=draft` + `algorithm_type=UNKNOWN`）。域代码在文件名；展示用中文枚举（`scripts/lib/metric-domain-enum.json`） | data-agent                                              |
| `metric-readiness-matrix-{域}.yaml` | 四维就绪度 + 可选`lifecycle_stage`                                                                                                                       | data-agent（D2：lineage-subcoord）                      |
| `metric-srs-map.yaml`               | 需求来源`srs_refs[]`（需规分册+序号+简要描述）                                                                                                           | data-agent（`node scripts/build-metric-srs-map.mjs`） |
| `metric-spec-POLICY.yaml`           | 政策域算法定义卡（模型/权重；不是第二条 seed）                                                                                                             | data-agent / algorithm-agent                            |

现网 seed：ENT / POLICY / CHAIN / SYNTH / TNIE / INNOV / TECH / ORG / TALENT / SVC / COMMON。
现网矩阵：ENT / CHAIN / SVC / SYNTH / INNOV / TECH / ORG / TALENT / COMMON / POLICY。
`cfg_metric-SVC-seed.yaml` 于 `METRIC-SEED-REGISTER-L01` 只登记 OPEN 新号（2 条）；B 轨 29 条 `calc-logic/SVC/` **未**全量灌入本 seed。

`algorithm_type` 枚举与派单见梳理 §2.1。存量 seed **未回填**，未写视为 `UNKNOWN`。

查询走 MCP `metric-registry`（`metric-get` → `kit` / `readiness` / `extras.srs_refs`）。不要整文件读本目录 YAML。说明：[`../metric-mcp-usage-guide.md`](../metric-mcp-usage-guide.md)。需求来源 sidecar 由 `node scripts/build-metric-srs-map.mjs` 从 A1 表1 + A2 mapped 页生成。

飞书「指标与数据开发进度」离线包：说「指标进度统计」→ MCP `metric-progress-export`（skill `gkx-metric-progress`）→ [`export/指标与数据开发进度.xlsx`](export/指标与数据开发进度.xlsx)。配额不够时用这张表；禁止回写本目录 YAML。

带需求来源的完整表：说「导出指标需求来源」→ MCP `metric-srs-export`（skill `gkx-metric-srs-export`）→ [`export/指标需求来源.xlsx`](export/指标需求来源.xlsx)。与进度表分文件，禁止往飞书同列表加列。空来源 = 尚未从 A1/A2 回填。
