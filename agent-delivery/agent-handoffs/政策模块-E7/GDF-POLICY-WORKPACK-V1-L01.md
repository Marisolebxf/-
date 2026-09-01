# GDF-POLICY-WORKPACK-V1-L01 · 政策维 GDF 派单包 v1 — 贴源 + Mapping

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 口头「认领并执行」；监管人与 Owner 均为淮政玮 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义叶，派单禁止 ponytail 行 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | **未改**拓扑。写库方正式边仍是 GDF Wave A/B；Demo `ods_sync` 保持虚线 as-built，不进产线 DAG |
| 会签态 | 源文件 frontmatter：`approved`（S1 流图；细表 stores 仍 draft） |
| 说明 | 本叶只出派单包，不改 `01-data-flow.md` |

## 范围与实现

对照 bid / 厚包：政策域 **只做** Wave A 贴源 + Wave B Mapping。

新建 `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v1/`：

| DoD | 结果 |
|---|---|
| README/00/01/02/03/04/06/09明细/10/11，对标产业链 v1 | ✅ |
| Wave A：两张 P0 + `is_deleted`/`is_history` 过滤 | ✅ `02` |
| Wave B：两源洗入一张 `policy_base_info`（`policy_id`←ODS `id`） | ✅ `09` §2.1 / §3 |
| 作废 Demo ods_sync、`dwd_zck_*`、旧 v1 37 列、PG | ✅ `00` / `11` |
| 回写 `派单包/README.md` 政策现行包 | ✅ |
| 不含写 ES / ADS / Nebula；CDC 预填不在本叶 | ✅ |

## 偏离说明

- DWD 细表 `stores/mysql/dwd.md` 仍 draft。`10/` 冻结的是 **产线目标列快照**（含 `source_plane`、省市区、`policy_support` JSON），不是 Demo as-built（`ext1`/`gis_location`）。未假装 stores 已 approved。
- `OPEN-POLICY-MAP-01` 已由 `human:淮政玮` 2026-09-01 拍板：**方案 A 永远分 UK** `(source_plane, policy_id)`；禁止 `gbl:` 改键。
- `parse_workpack.py` 仍不认 `policy_base_info` 字段矩阵（与 CHAIN 同类缺口）。本叶按 DoD **不**出 CDC 预填。

## 产物清单

- `data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v1/`（全套）
- `data/GDF/派单包/README.md`（政策行改为现行 v1.0）
- 本 handoff

## 验收证据

- 包内 `02` + `09` + `10` 齐全；国内/国际均指向同一 `policy_base_info`
- 主键规则：`policy_id`←ODS `id`；平面切片 `domestic`/`global`
- 无业务仓代码改动；无 CI / K8s

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本叶无算法 |
| 调用链 前端→Java→Python | ✅ 未越层 |
| 图谱 Nebula | ✅ 本叶不写图 |
| 可观测 | N/A 文档叶 |
| CI/CD | N/A `cicd: skip` 类定义产物 |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / Java 不写算法 | ✅ |
| 数据策略 ADS 先行 | ✅ 本叶停在 DWD Mapping，不伪写 ADS |
| D8 Design | N/A |
| D9 8 件套 | N/A 本叶无新指标数字 |
| D10 交互 | N/A |
| D12 lumen 不调 demo | ✅ 禁止 `demo_gkxlumenx_*` 当产线 |

## 测试结果

- 文档结构对照产业链 v1 文件清单：齐。  
- 未跑 `gkx-gdf-cdc-workpack`（DoD 明确本叶不预填）。  
- 未改 `01-data-flow.md`。

## 遗留风险

- `OPEN-POLICY-MAP-01` **已关**（永远分 UK）。  
- `OPEN-POLICY-MAP-02` / QPOL-01 类别码化不在本包。  
- `OPEN-POLICY-FLOW-01` 正式 DAG 名待产线回写。  
- `content` 体积大，Wave A 必须流式（已写进 `04`）。  
- 下一叶：胡森泉 CDC 预填（须先补解析或按 09 人工配）。

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`
- commit：（提交后回填）
- pipeline URL / ID：无业务 CI
- 部署 namespace / 镜像 tag：无
- K8s rollout：N/A
- dev 测试 URL：N/A

## 可观测性（建议）

- OTEL_SERVICE_NAME：无
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v1/**`
- `agent-delivery/data/GDF/派单包/README.md`
- `agent-delivery/agent-handoffs/政策模块-E7/GDF-POLICY-WORKPACK-V1-L01.md`
