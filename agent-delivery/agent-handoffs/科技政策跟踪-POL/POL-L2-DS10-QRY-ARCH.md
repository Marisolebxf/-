# POL-L2-DS10-QRY-ARCH · 科创政策全景多维检索架构

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 只写多维检索查询的实现架构。不改注册表，不标 done，不会签 |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过调用链、501 空态和与 203–218 的边界。

## 范围

科创政策全景 · 二级「多维检索查询」。只覆盖 SRS 序号 197–202，用户故事 `US-DS-POL-01`。

| 序号 | 叶子 | 流程 |
|---|---|---|
| 197 | 多维度检索条件设置 | 同步读 ADS |
| 198 | 高级检索功能 | 同步读 ADS |
| 199 | 检索结果智能排序 | 501 空态 |
| 200 | 检索结果筛选与分类 | 同步读 ADS |
| 201 | 检索历史与收藏 | 501 空态 |
| 202 | 检索结果导出与分享 | 501 空态 |

197、198、200 读已有 `GET /display/v1/policy/panorama/stats`、`search`、`{id}/detail`。链路是前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → ADS。无行则统计卡或列表空，不造 0。D4 仍是 mock。

199 读 `GET /display/v1/policy/panorama/rank`，501。列表仍可按发布时间、效力级别、浏览量排，该顺序留在 `search`。不返回 `smartScore`。

201 读 `GET /display/v1/policy/panorama/favorites`，501。localStorage 不是收藏服务。

202 读 `GET /display/v1/policy/panorama/share`，501。前端导出和打印窗不是分享服务。

199、201、202 在 display 直接返回，不进 Python，不进 element。

## 产物路径

`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-QRY-ARCH.md`

## 与 203–218 的边界

本叶不写 203–218 的流程。点名排除 `panorama/jobs`、`ingest`、`subscriptions`、`feedback`、`assessment-report`、`version-diff`、`benchmark-report`。

| 序号 | 边界 |
|---|---|
| 203 | 入库列表走 `ingest`。不重开 GDF |
| 204 | 订阅走 `subscriptions`。不是收藏 |
| 205 | 趋势另叶复用时序。热点、影响、深度报告走 `jobs` |
| 206 | 动态可视化另叶。本叶不实现 |
| 207 | 页内并列查看另叶。深度对比不在本五条 |
| 208 | 只消费已有子图。本叶不读图，不走 `E-E7-POLICY-M1-L06` |
| 209 | 实施效果走 `jobs`，501 |
| 210 | 受众反馈走 `feedback`，501 |
| 211 | 评估报告走 `assessment-report`，501。不是 202 |
| 212 | 匹配与推送走 `jobs`，501。不改去打 `/topic/v1/policy` |
| 213 | 新旧对比走 `version-diff`，501 |
| 214 | 详情对比的力度走 `jobs`，501 |
| 215 | 部门件数另叶，复用政策总数 |
| 216 | 标杆力度另叶。本叶不把支持力度写成检索结果 |
| 217 | 对标报告走 `benchmark-report`，501。与 `share` 分开 |
| 218 | 对标可视化走 `jobs`，501 |

`stats` 上的 `M_POLICY_INDUSTRY_COVERAGE`、`M_POLICY_SUPPORT_STRENGTH` 不改挂到 197–202。

## 未做事项

- 未写 OpenAPI 字段表、请求体、响应体、枚举。留给 `POL-L2-DS10-QRY-API`
- 未新造 `metric_id`，未改 D4，未把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开
- 未改 `FE-POL-01A`，未新建前端单，未重开 GDF
- 未消费 `/topic/v1/policy`，未把 `E-E7-POLICY-M1-L06` 写成展示路径
- 未改说明书、WBS、注册表、调研分册
- 未 commit，未 push
- 未把本单标 done。会签不在本单

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS10-QRY-ARCH-SEQ` |
| 图 diff | 新增多维检索一条：197/198/200 同步到 element / ADS；199/201/202 在 display 进入 501。禁止边：`/topic/v1/policy`、Python、`L06`、本叶新开路径 |
| 会签态 | 本叶新图。源文件无 frontmatter，记 `draft`。不自填绿 |
| 说明 | 图在架构稿第 2 节 |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | green |

未回写注册表。

## 修改内容

- 新增 `sdd/l2/POL-L2-DS10-QRY-ARCH.md`
- 新增本 handoff

未 commit，未 push。
