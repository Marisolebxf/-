# ENT-YIJI-INFER-PANEL-L01 · 推理入库独立面板 + 新边闪烁

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | GraphView 配置重组；过程明细用已有 infer 返回；写入后新边闪烁 60s |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未新开组件文件；闪烁用 setInterval 改 ECharts lineStyle，避免每次 force 重布局 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 |

## 问题清单

- 现网须等 `gkx-demo-ui` + `demo-platform-entan-py` 新 CI 绿。
- 未写联调通过。

## 修改内容

- 顶栏只留浏览图谱；推理入库单独卡片：1 选文档 2 正则/LLM 3 预览/写入。
- 过程展示五步中文状态 + extracts / drops / 新边表。
- 写入后合并 infer_edges 到当前图，红边闪烁 60 秒后自动取消。
- pipeline 步骤 detail 改为中文长说明（预览 vs 写入）。

## 测试结果

- `from entan.yiji_sim.pipeline import run_graph_infer` → PIPE-OK
- GraphView / K8s：**未现网点写入闪烁**

## 遗留风险

- 若 Nebula 未灌上，前端仍 overlay 新边以便看见闪烁。
- 浏览器最小化时 interval 仍跑满 60s。

## CI/CD（必填）

- 分支：`dev`（push 后填 SHA）
- 部署：`gkx-demo-ui` + `demo-platform-entan-py`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| Demo 直连 `/v1/graph/infer` | ✅ 未新开 Java |
| 正则 infer.py | ✅ 未改 |
| D12 | ✅ 只改 demo-* |

## 涉及文件

- `repos/demo-ui-system-test/src/views/entan/components/GraphView.vue`
- `repos/demo-algo-ent-analysis/entan/yiji_sim/pipeline.py`
