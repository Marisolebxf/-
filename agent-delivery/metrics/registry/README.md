# metrics/registry/ —— 指标身份证 + 就绪度（机器真源）

> 模型：`../../data-lineage-policy.md` §2（8 件套 v1.5 含 `algorithm_type`）+ §2.3（四维就绪度）。  
> **FE / API / 镜像脚本只认本目录 YAML**（不再认 `metrics/` 根上的同名文件）。

| 文件 | 角色 | Owner |
|------|------|-------|
| `cfg_metric-{域}-seed.yaml` | 8 件套注册表（齐备态 9 项；OPEN 允许 `D1=draft` + `algorithm_type=UNKNOWN`） | data-agent |
| `metric-readiness-matrix-{域}.yaml` | 四维就绪度 + 可选 `lifecycle_stage` | data-agent（D2：lineage-subcoord） |
| `metric-spec-POLICY.yaml` | 政策域算法定义卡（模型/权重；不是第二条 seed） | data-agent / algorithm-agent |

现网 seed：ENT / POLICY / CHAIN / SYNTH / TNIE / INNOV / TECH / ORG / TALENT / SVC / COMMON。  
现网矩阵：ENT / CHAIN / SVC / SYNTH / INNOV / TECH / ORG / TALENT / COMMON。  
`cfg_metric-SVC-seed.yaml` 于 `METRIC-SEED-REGISTER-L01` 只登记 OPEN 新号（2 条）；B 轨 29 条 `calc-logic/SVC/` **未**全量灌入本 seed。

`algorithm_type` 枚举与派单见梳理 §2.1。存量 seed **未回填**，未写视为 `UNKNOWN`。

查询走 MCP `metric-registry`（`metric-get` / `metric-query` / `metric-summary`），不要整文件读本目录 YAML。说明：[`../metric-mcp-usage-guide.md`](../metric-mcp-usage-guide.md)。
