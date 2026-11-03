# 派单 · POL-L2-DS10-QRY-ARCH

- 任务：`POL-L2-DS10-QRY-ARCH`
- 日期：2026-11-03
- 认领：`agent:arch-agent`
- 监管：`human:淮政玮`
- 认领类型：`coordinator_dispatch`（MCP 无此字段，以本文件与 note 为准）
- 锁：24 小时
- 强度：ponytail off（定义任务，不缩文档）
- 仓：`gkx-orchestration`。不 commit，不 push，不改注册表，不改 WBS，不改 lumen / demo

## 范围

科创政策全景 · 二级「多维检索查询」。只覆盖 SRS 序号 **197–202**。

| 序号 | 叶子 | 已有判定 |
|---|---|---|
| 197 | 多维度检索条件设置 | 可接统计读面。`M_POLICY_TOTAL_COUNT`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST`、`M_POLICY_NATIONAL_DIST`、`M_POLICY_SZ_DIST`。D4=mock |
| 198 | 高级检索功能 | 可接统计读面。`M_POLICY_TIMESERIES`、`M_POLICY_NATIONAL_DIST`、`M_POLICY_LEVEL_DIST`、`M_POLICY_TYPE_DIST`、`M_POLICY_VALIDITY_RATE`。布尔组合无独立 metric_id。D4=mock |
| 199 | 检索结果智能排序 | 501。未见排序模型。按发布时间、效力级别、浏览量排序是查询参数，不是新指标 |
| 200 | 检索结果筛选与分类 | 可接统计读面。`M_POLICY_TYPE_DIST`、`M_POLICY_NATIONAL_DIST`。二次筛选无独立 metric_id。D4=mock |
| 201 | 检索历史与收藏 | 501。未见用户态服务。页面 localStorage 不是本资源 |
| 202 | 检索结果导出与分享 | 501。未见导出或邮件服务。前端表格和打印窗不是本资源 |

不写 203–218，不写评价、推演、核增。

## 产物

只写这两个文件：

1. `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-QRY-ARCH.md`
2. `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-QRY-ARCH.md`（handoff）

架构稿写实现架构和整体流程。六叶都要有：同步还是 501、读哪条已有资源、空态、明确不做什么。

本二级只用全景资源里的这五条，不新开路径：

| 叶子 | 资源 | 流程 |
|---|---|---|
| 197、198、200 | `GET /display/v1/policy/panorama/stats`、`GET /display/v1/policy/panorama/search`、`GET /display/v1/policy/panorama/{id}/detail` | 同步。前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → ADS。无行则统计卡或列表空，不造 0。对齐前数值仍是 mock |
| 199 | `GET /display/v1/policy/panorama/rank` | 501。列表仍可按发布时间、效力级别、浏览量排。不返回演示权重 `smartScore` |
| 201 | `GET /display/v1/policy/panorama/favorites` | 501。空态。不把 localStorage 写成收藏服务 |
| 202 | `GET /display/v1/policy/panorama/share` | 501。空态。不把前端导出或打印窗写成分享服务 |

`panorama/jobs`、`ingest`、`subscriptions`、`feedback`、`assessment-report`、`version-diff`、`benchmark-report` 不属于 197–202，本叶点名排除。

## 必读

- `agent-delivery/bid-reference/srs/02-科技信息展示系统/科技政策跟踪/科创政策全景.md`（只读序号 197–202 的需规）
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` 第 2 节 DS-10 与第 3–6 节
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/调用链与边界.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/契约输入清单.md` 全景五条
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/survey/DS-10.md` 序号 197–202
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-DISPLAY-长任务总控.md`

## 禁令

- 不写 OpenAPI 字段表、请求体、响应体、枚举。那是 `POL-L2-DS10-QRY-API`，本单不提前写。
- 不新造 `metric_id`，不改 D4，不把 mock 写成已上线。
- 不把 `E-E7-POLICY-M1-L06` 写成展示路径。不复用 `/topic/v1/policy`。
- 不改 `FE-POL-01A`，不新建前端单，不重开 GDF。
- 不把 `GDF-POLICY-MOCK-GATE-L01`（blocked）写成已解开。正式值仍是 mock。
- 不把本单标 done。handoff 写完即停。会签不在本单。

## DoD

- 架构稿六叶都有流程：同步读 ADS，或 501 空态。
- 调用链服从 `/display/v1/policy`。Java 读 ADS。199/201/202 不进 Python。
- handoff 含范围、产物路径、与 203–218 的边界、未做事项。
