# SYNTH-DEMO-ACCEPT-LOOP Handoff — 综合智能分析演示实例反复验收（常驻验收单）

- **任务**：`SYNTH-DEMO-ACCEPT-LOOP`（产品实现规程 §6.5.2 验收单；tech_task / qa-agent）
- **监管**：`supervised_by=human:徐滕强`（§6.5.7 当次会话真人；`done` 操作人以 registry 闸门为准）
- **仓**：gkx-orchestration（registry only；本单不改业务代码、不写库）
- **强度**：ponytail: full
- **日期**：2026-11-07

## 运行 2026-11-07（第一轮）

### 环境与令牌

- 令牌：监管人提供 curl 提取 access_token → 写入 `~/.gkx/topic-loop-token`（600 权限；不进 git / handoff / 日志正文）
- 锚点探测：`POST /tts/svcz/api/enterprise/topic/v1/recommend`（监管人提供的现网请求）→ **HTTP 200**，令牌有效、网关前缀可用

### 探测（§6.5.3）+ 分层诊断（根因定位）

| # | 层 | URL | 结果 |
|---|---|---|---|
| 1 | 域名网关（企业专题面） | `GET /tts/svcz/api/enterprise/topic/v1/synth/vitality/batch-snapshot` | 404 `path=/topic/v1/...`（demo 面网关，非本服务） |
| 2 | 域名网关（lumen 面） | `GET /tts/lumen/api/topic/v1/synth/vitality/batch-snapshot` | 404 `path=/v1/synth/...`（**网关剥 `/topic` 转发**） |
| 3 | NodePort 30895 直打 | `GET /topic/v1/synth/vitality/batch-snapshot` | 404 `path=/v1/synth/...`（同上，证实网关剥前缀行为） |
| 4 | **服务直打 svc 7092** | `GET /topic/v1/synth/vitality/batch-snapshot` | **HTTP 200 + 快照数据正确**（`snapshotId=snap:mock_20261106_vit_seed_index_main`，`cache_key=深圳\|全国重点城市\|最近3年\|INDEX_MAIN`） |

**根因**：`gkxlumen-platform-topic` 服务按**完整 `/topic/v1` 前缀**注册映射（直打 200 验证）；lumen 网关按**剥 `/topic` 前缀**转发（StripPrefix）→ 服务收到 `/v1/synth/**` 无此映射 → 404。服务与数据全正常，纯网关-服务路由前缀错配。

**修复二选一（监管人裁决）**：
- **方案 A（devops）**：网关为 `gkxlumen-platform-topic` 的路由改为不剥前缀（保留 `/topic/**` 直转）——注意需评估其他已按剥前缀工作的 topic 接口（#102–#109 任务链等）兼容性
- **方案 B（api）**：服务侧按网关契约把 controller 映射改发布为 `/v1/**`（Java `gkxlumen-topic` `server.servlet.context-path` 或 controller 调整）

> 运行注记：第 2/3 步属 ENV 分层诊断（同意图探测 2 次 + 变路径对照 1 次，未超熔断纪律）；第 4 步命中前按「服务内部真实映射」假设验证，非重复探测。

### 处置（按规程，未越线）

- 验收单 → `blocked`（note 只写映射不存在事实 + 已通知监管人）；**不建子任务、不开第二轮**
- LOOP 计划状态行已回写（「最近一轮：R1 探测 / 退出=ENV」）
- 同意图探测合计 2 次，未第三次猜路由（熔断纪律）

### 给监管人的路由澄清选项（下一轮开工前二选一确认）

1. 现网尚未发布 `gkxlumen-topic` SYNTH 路由（demo 库数据在、K8s dev 服务在、但 `edu.itic-sci.com` 网关未挂该服务/路径）
2. 网关前缀另有其值（既非 `/tts/svcz/api/enterprise` 也非 `/tts/lumen/api`）

澄清后由监管人重说「按 LOOP 跑」，验收单再转回执行。

## 架构合规自检

- ✅ 纯后端两段制（只读探测）；未写任何库；未建缺口子任务（ENV 类不建单）
- ✅ 令牌未写入 git/handoff/日志；探测合计 2 次未空转
- ✅ 未把 404 改写成通过；未把 ENV 归入 DATA/QUERY/ALGO

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 30000 |
| model_used | glm-5.3-flash |
| actual_cost | 0.04 |
| cost_warn | green |

## ponytail

ponytail: full——单 handoff 复用验收单生命周期；探测记录即运行记录，不另建运行日志文件。
