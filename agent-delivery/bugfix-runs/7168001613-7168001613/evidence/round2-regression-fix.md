# 7168001613 第二轮：用户复测反馈两处回归（2026-11-14 14:12 已推）

## 用户反馈（2026-11-14 13:31）

1. 选「生物产业」后产业集群排名只剩 1 项（生物医药 575），12 链列表消失。
2. 企业分布情况「无相关产业数据」/ 接口报错。

## 症状 2 根因（线上 500 复现闭环）

探针（dev 网关 `https://edu.itic-sci.com/tts/lumen/api/enterprise/topic/v1/stats/distribution`）：

| 探针 | 结果 |
|---|---|
| `national` + `chain_code=INB2503` | **500** |
| `global` + chain（无 dim JOIN） | 200 |
| `district-heat` + 链码（同库 JOIN，无 dim） | 200 |
| `/meta/regions`（读同表 `dim.code_region`） | 200 |
| 假码 `ZZZ9999` + national | 仍 500（结构性） |

根因：`_distribution_by_chain` 的 `cr.name = eb.province/city/district` 跨库列对列 JOIN 未显式对齐排序规则 → MySQL 1267（D19）。Python `RealDataUnavailable`→503，Java Feign 转 500。仓内先例：`eco.py:519`、`geo_indicator.py:612`、`gkx_svc_service/repo.py:708` 均显式 COLLATE。

## 症状 1 根因（第一轮修复的回归）

前端把 `chain_code` 传给 `industry-comparison` → 后端按链过滤 → 列表收窄成 1 项。评审口径 = 全 12 链列表 + 高亮所选（缺陷原文「共 12 个产业」）。KPI/趋势/分布按链收窄是正解，仅排名列表不该收窄。

## 修复与验证

- `lumen-topic-py@eac9906`：三维度 JOIN 两侧补 `COLLATE utf8mb4_general_ci`；`test_overview_chain_scope.py` 补 3 维度断言。pytest 4 passed；全量 410 passed（10 失败均为他人模块既有问题，git log 归属核对无交集）。**push `6118d13..eac9906`**
- `lumen-ui-topic@219dab0`（merge 后 `ca1faef`）：`entStatsOverviewIndustryComparison()` 不传链码。type-check 绿。**push `8598cce..ca1faef`**（远端并行提交 `71c9fc0/8598cce` 只碰 keyAnalysis 三文件，`pull --no-rebase` 合入无冲突；并行会话 7 个 `ServicePortal*` WIP 文件未动）

## 遗留观察（非本单范围）

- 现网 `global`+chain 探针曾返回旧形状（4 行 CHN、字符串计数、无 chain_code 回显）→ 滚动部署多副本混存，等 CI 部署齐后自然收敛；COLLATE 修复部署后建议复测 `national`+chain。
