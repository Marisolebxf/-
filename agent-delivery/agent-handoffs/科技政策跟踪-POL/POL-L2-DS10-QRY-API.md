# POL-L2-DS10-QRY-API · 科创政策全景多维检索后台接口设计

ponytail: off

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 任务已是 in_progress。本单只写接口设计，不改注册表，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过调用链、501 与空列表的差别、以及内部委托这条偏离。

## 范围与实现

科创政策全景 · 二级「多维检索查询」。只覆盖 SRS 序号 197–202，用户故事 `US-DS-POL-01`。

浏览器只打 `/display/v1/policy/**`。公开资源六条，全部是 GET：

| 序号 | 公开资源 | 读法 |
|---|---|---|
| 197、198、200 | `GET /display/v1/policy/panorama/stats` | 同步。内部委托 metrics + indicators |
| 197、198、200 | `GET /display/v1/policy/panorama/search` | 同步。内部委托 search + search/options。普通排序留在本资源 |
| 197、198、200 | `GET /display/v1/policy/panorama/{id}/detail` | 同步。内部委托 docs/{id} |
| 199 | `GET /display/v1/policy/panorama/rank` | 当前 501。接通后委托门面新增排序入口 |
| 201 | `GET /display/v1/policy/panorama/favorites` | 当前 501。接通后无记录是空列表 |
| 202 | `GET /display/v1/policy/panorama/share` | 当前 501。接通后委托门面新增导出与分享入口 |

197 / 198 / 200 由 `gkxlumen-display` 同步委托已提交的 `gkxlumen-topic-policy`：stats ← `GET /topic/v1/policy/metrics` 与 `GET /topic/v1/policy/indicators`；search ← `GET /topic/v1/policy/search` 与 `GET /topic/v1/policy/search/options`；detail ← `GET /topic/v1/policy/docs/{id}`。无行则统计卡或列表空，不造 0。D4 仍是 mock。

199 的智能排序只有相关性、时效性、重要性。Java 不打分，不返回 `smartScore`。发布时间、效力级别、浏览量留在 search 的 `order`。

201 入口未接上时 display 返回 501。入口接上且该用户没有记录时，历史列表和收藏列表是空列表，不是 501。localStorage 不是本资源。

202 入口未接上时 display 返回 501。接通后仍是这一条 GET，展示不组装文件。

199 / 201 / 202 接通后浏览器仍打这三条展示资源。内部委托门面新增入口（排序、历史与收藏、导出与分享）。子路径不在本分册冻结。未提交的门面改动不是本单输入。

本分册是 `BE-POL-CONTRACT-01` 的输入。不另建契约文件，不写实现代码。序号 203–218 不在本分册。

## 偏离

原 DoD 写「不复用 `/topic/v1/policy`」。签收口径：这句指浏览器不改打专题 URL，不禁止这次内部委托。`gkxlumen-display` 内部委托 `gkxlumen-topic-policy` 是 A1 的本二级例外，不改 `ARCH-DISPLAY-01` 的全局 A1。`E-E7-POLICY-M1-L06` 仍不是展示前端联调单。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-QRY-API.md`
- 本 handoff：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-QRY-API.md`

## 验收证据

两份文档已落盘。公开六条 GET、197/198/200 的同步委托、199/201/202 的当前 501 与接通后路径、收藏空列表与 501 的差别，都写在接口分册。定义单，无业务代码，无 PR。文档随本次提交进入 `origin/dev`。状态进入 `integration`。会签未完成，不标 done。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本分册不写算法。智能排序接通后由门面转 `/internal/policy`，Java 不打分，不返回 smartScore |
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/**`。展示内部委托专题门面，不直连 Python，不直连库 |
| 图谱 | ✅ 本分册不读图，不写 nGQL。graph / timeline / portal 不进本二级 |
| 可观测 | ✅ 同步三条沿既有展示链带 traceId。501 在 display 返回，不另起算法 span，不新设计观测点 |
| CI/CD | ✅ 定义文档随 `origin/dev` 提交，未 force |
| D12 | ✅ 不调用 demo 服务，不把 demo 门面写成契约 |
| D9 | ✅ 不新造 metric_id，不改 D4，不把 mock 写成已上线 |
| D14 | ✅ 本分册不写对象存储。导出目录只复述架构稿已有落点，不新造桶或顶层目录 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.04 |
| cost_warn | green |

无控制台分项。按本单 `estimated_tokens` 8000、api-agent 80/20、B 档 `$3/$15` 回填：`8000×0.80×3/1e6 + 8000×0.20×15/1e6 = 0.043`，记 `0.04`。

## 未做事项

- 未写实现代码，未改 lumen-svc-platform、lumen-algo-py
- 未改 `E-E7-POLICY-M1-L08` / `L09` / `L10`
- 未改架构稿、说明书、WBS、契约输入清单、调用链、指标分册、数据分册
- 未把未提交门面改动写成契约
- 未另建 API-POL
- 未把序号 203–218 写入本分册
- 未 commit，未 push，未改注册表，未标 done

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS10-QRY-ARCH-SEQ` |
| 图 diff | 本分册不改图。沿用架构稿：197/198/200 内部委托；199/201/202 当前进入 501 |
| 会签态 | 源文件无 frontmatter，记 `draft` |
| 说明 | 图在 `sdd/l2/POL-L2-DS10-QRY-ARCH.md` 第 2 节。本分册只补查询参数和两种读法 |

## 修改内容

- `sdd/l2/POL-L2-DS10-QRY-API.md`
- 本 handoff
