# DATA-POLICY-STORAGE-DEMO-FLOW-L01 · 政策维灌数流程重理 + 数据流图

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`（长任务总控：后续认领不必再问） |
| 说明 | 用户指令：重理政策维灌数流程，画清晰数据流图到 `etl/pipeline-demo-mock.md` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类，不改代码） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只改编排仓 Markdown，未挂载 Headroom |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-ETL-DEMO-MOCK`（本叶新增三张 Mermaid；拓扑会签图 `POLICY-STORAGE-FLOW` **未改**） |
| 图 diff | 加 as-built 灌数总图（mockgen → ODS/DWD → ADS 15 → Nebula）；加 `run_all_policy` 15 步时序；加 replace/append 分流；正式 GDF E0→T2 画虚线。禁止事项未变。 |
| 会签态 | `01-data-flow.md` frontmatter 仍为 `approved`（本叶不翻签）；本文件 `status: as-built` |
| 说明 | 本叶是 ETL 全景说明图，不是 S1 拓扑会签图 |

## 范围与实现

对照 `bid-reference` 政策维数据链路：本叶只重写 Demo 灌数全景说明（`pipeline-demo-mock.md`），把 as-built（`run_all_policy` 15 步）与正式 GDF 目标态画清。不接供应库、不灌数、不改 `polan`。

## 偏离

无范围偏离。叙述纠偏（旧稿「九张表 / 先 ODS 再映射 / L4 直读 DWD」改为 as-built）属文档诚实性，不是施工范围膨胀。

## 产物清单

- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-demo-mock.md`（重写 · 三张 Mermaid）
- `etl/README.md` · `etl/pipeline-mock-to-ads.md` · `CHANGELOG.md`（指针同步）
- 本 handoff

## 验收证据

- 图节点与 `scripts/run_all_policy.py` `build_steps()` 15 步一一对应
- `replace` 写入方向回源 `generate.py`（DWD 先、ODS 镜像）
- 国际行同表回源 `level=0`；L4 源表回源 `nebula_loader`（ADS 图两表）
- 会签通过：文档与 as-built 对齐，待 `human:淮政玮` 签收

## 问题清单

- 正式 GDF E0→E1→T2 仍未施工（`OPEN-POLICY-FLOW-01`）
- `dwd_global_policy_base` 仅存在于贴源 DDL / 映射稿，mockgen 零写入
- `replace` 写入方向与设计 T2 相反（内存→DWD→ODS 镜像），接正式厂时不得把现网 replace 当工厂作业

## 修改内容

- 重写 `etl/pipeline-demo-mock.md`：以 as-built 对照 `run_all_policy.py` / `mockgen` 画清灌数全景
- 纠正旧稿「九张指标表」「先 ODS 再映射」「L4 直读 DWD」三处过时叙述
- 同步 `etl/README.md` 管道状态、`CHANGELOG.md`、`pipeline-mock-to-ads.md` 指针
- **不灌数、不改 `polan`、不翻签 S1 流图**

## 测试结果

- 对照 `scripts/run_all_policy.py` `build_steps()` 15 步名称与顺序一致
- 对照 `polan/mockgen/generate.py`：`replace` 先 `INSERT` DWD 再 `_write_ods`；国际行 `level=0` 同表；非 mysql 不写 ODS
- 对照 `pipeline-dwd-to-ads.md` / `pipeline-to-nebula.md`：ADS 15 张、L4 读图镜像

## 遗留风险

- 读者若只看旧记忆「E0→E1→T2」会以为现网已接供应库；图中已用实线/虚线切开
- SQLite 默认后端看不到 ODS 层，联调须显式 `POLAN_DB_BACKEND=mysql`

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`（本叶未提交，待用户指示）
- commit：—
- pipeline URL / ID：文档叶，无业务 CI
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A（只改 Markdown）

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- traceId：N/A
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-demo-mock.md`
- `agent-delivery/data/data-design/storage/POLICY/etl/README.md`
- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-mock-to-ads.md`
- `agent-delivery/data/data-design/storage/POLICY/CHANGELOG.md`
- `agent-delivery/agent-handoffs/DATA-POLICY-STORAGE-DEMO-FLOW-L01.md`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 未改 Java |
| 调用链 前端→Java→Python `/internal` | ✅ 图中 Java 只读 ADS；联调台虚线保持 |
| 图谱仅 Nebula `demo_gkx_chain` | ✅ 禁止 `gkx_policy` / 写 `gkx_chain` |
| 可观测 | N/A 文档叶 |
| CI/CD | N/A 文档叶 |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / Java 不写算法 | ✅ |
| 数据策略 ADS 先行 | ✅ ADS 由 DWD 全量重算 |
| D8 / D10 | N/A |
| D9 指标 8 件套 | ✅ 未改口径；图注明 15 张 ADS |
| D12 lumen 不调 demo 服务 | ✅ 展示 fixture 保持虚线 |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 45000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.18 |
| cost_warn | green |
