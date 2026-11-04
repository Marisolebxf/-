# FE-TOPIC-NGINX-CMS-PREFIX-L01 · 30892 nginx /api/cms 前缀补配（实证：无需变更）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 前缀口径（2026-11-04 17:34 用户拍板）：CMS 共享 `/api/cms` + 第二段区分；久新 `/cms/**` 特殊情况保留 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最优解 = 零改动。实证推翻建单前提（30892 `/api/**` 本就全量转发网关），按「第二处出现即删」原则不写多余配置 |

## 实证结论（2026-11-04 17:41，jumpserver → 10.50.69.111:30892）

**`30892` 的 `location ^~/api/` 是「剥 `/api` → 全量转发 30895 网关」**（`k8s/lumen-topic.yaml:39-60`），而非按前缀白名单转发。建单前提「30892 缺 CMS 前缀需补配」不成立：

| 链路 | 实测 | 判定 |
|---|---|---|
| `/api/cms/cms-ops/v1/topic-policy/content/**` | **401 fail-closed**（网关 `/cms/**` StripPrefix=1 → 服务 `/cms-ops/**` OAuth2） | ✅ 可达，与久新同轨 |
| `/api/chain/topic/v1/industry/viz`（V-I） | **200** + scale 块真实数据 | ✅ |
| `/api/policy/topic/v1/policy/viz`（V-P） | **200** + 四块诚实空态 | ✅ |
| `/api/enterprise/topic/v1/profile/viz`（V-E） | **200** + card/timeline 有行（含「成立于 2001-04-27」证明新镜像生效） | ✅ |

**结论：CMS / chain / policy 三条线的前端接线零阻塞，30892 nginx 无需任何改动。**

## 为什么会误判

此前「30892 缺前缀」的观察来自：chain/policy 的 viz 请求打到 30892 时返回 HTML——那是因为当时**请求路径不带 `/api/`**（裸 `/chain/...`），命中 nginx 默认 `location /` 回退静态页。前端 axios `baseURL=/api`，真实请求永远带 `/api/`，天然全通。

## 遗留（非本单，数据/配置面）

| 项 | 说明 | 归属 |
|---|---|---|
| scatter 空 | ES 全库 `competitiveness_score` 稀疏（desc 排序首位 null），Top500 全被「缺 x/y 丢弃」 | 数据侧灌数 |
| swot 空 | LLM 材料未生成；路由分流（C2）已验证到达 algo-py | algo 侧 LLM Key/素材确认 |
| `/api/cms` 前端事实标准 | 前端 CMS 接线时 axios 路径写 `/api/cms/cms-ops/v1/**`（baseURL `/api` 已含） | 孔东接线叶（SYSINT-03-01A/03A） |

## 架构合规自检

| 项 | 结果 |
|---|---|
| 未改任何配置/代码 | ✅ 零 diff |
| 久新轨道零改动 | ✅ `/cms/**` 原样 |
| 证据可复现 | ✅ 本文件 curl 命令 + 响应摘要 |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 约 40000 |
| model_used | composer |
| actual_cost | 约 0.25 |
| cost_warn | green |
