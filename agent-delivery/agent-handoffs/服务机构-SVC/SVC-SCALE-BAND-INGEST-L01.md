# SVC-SCALE-BAND-INGEST-L01 · 服务机构规模四档灌数 handoff

> **task-id**：SVC-SCALE-BAND-INGEST-L01（feature / P1 / 3 分）
> **执行/监管**：human:徐滕强（本人认领本人执行，claim_type=pull，锁 2026-11-12 15:20 起 4h）
> **仓**：lumen-topic-py（脚本）+ gkx-orchestration（registry/matrix/seed/handoff）
> **强度**：ponytail full

## 1. 范围与实现

飞书缺陷【2331】（门户-集群服务-专题：人员规模分布无图无数据，前端已改空态）的根因修复：ADS
`demo_gkxlumenx_ads.svc_metric_dist` 中 `metric_id=M_SVC_SCALE_BAND` 零行，`/svc/topic/v1/service-portal/overview`
的 `scale_bands` 恒空。

**交付物**：`repos/lumen-topic-py/scripts/seed_svc_scale_band.py`
- 六桶写入 `svc_metric_dist`（uk(metric_id,category) 幂等 upsert，GET_LOCK 防并发，默认预览 `--apply` 才写）
- 口径真源：`metrics/calc-logic/SVC/M_SVC_PT_GLOBAL_SCALE_DIST.md`（20261027 批正本：主链=注册资本六桶，外币/缺失单列不折算）
- 数字真源：`metrics/repro/out/M_SVC_PT_GLOBAL_SCALE_DIST_out.json`（20261022 gkx 快照实算，非 fixture）

**口径冲突处置**（note 中预警项）：查询键保留 `M_SVC_SCALE_BAND`（repo.py 消费契约），注册表 ID
`M_SVC_PT_GLOBAL_SCALE_DIST` 通过行内 `ext.registry_metric_id` 登记映射，未改任何代码查询键。

**DoD 第 1 条口径说明**：任务原文写「四档行」，实际按 calc-logic 正本与唐绍祖 2026-10-16 复核意见③（"兜底档单列，
不冒充人数档"）落地为**六桶**：四档 RMB + 外币注册 + 币种/金额缺失。DoD 第 2 条"六桶合计与机构池对账"即为此口径。

## 2. 验收证据

| DoD | 结果 |
|---|---|
| 1. ADS 写入六桶（人数优先→注册资本兜底口径） | ✅ 六桶 487/4,594/3,000/34,413/1,589/70；金额档=注册资本兜底链；外币/缺失单列（唐意见③形态） |
| 2. 六桶合计与机构池对账 | ✅ 44,153 = 池 44,153，脚本内 assert 硬校验 |
| 3. 门户 scale_bands 非空 | ✅ DB 层验证：repo.py `_dist('M_SVC_SCALE_BAND')` 同查询路径返回 6 行（source=demo_ads）。**线上 HTTP 未验**（见 §4 开放项） |
| 4. 注册表 D4 mock→ingesting | ✅ matrix `d4_ingestion_status: ingesting`（阶段清单 n/a×4 + verified in_progress）；seed `is_mock: false`；YAML 双文件解析校验通过 |
| 5. handoff + cost 回填 | ✅ 本文件 + registry task-update-fields |

## 3. 偏离说明

1. 「四行→六行」：见 §1，遵循口径正本与复核意见，非偷懒。
2. D4 翻 `ingesting` 而非 DoD 所写「ingesting/live」二选一的 `live`：QA 四段链路核验（policy §7.6）未做，按诚实性约束
   不升 live；`verified` 置 in_progress。
3.灌数取快照实算值而非现场连 gkx 重算：gkx 源（183.240.141.251:3318）为只读三方库，20261022 快照即 calc-logic
   正本钉版数字，与正本一致即口径合规。

## 4. 开放项 / 风险

| # | 项 | 处置建议 |
|---|---|---|
| 1 | **线上 HTTP 未验证**：K8s API 被认证墙挡（Jenkins login redirect），集群内服务未确认读到新行 | 用户浏览器开门户概况页，或运维 `kubectl exec` 后 curl overview 端点；`scale_bands` 应为 6 元素非空数组 |
| 2 | 唐 pending_cosign 三伤未签：本灌数按正本口径（外币/缺失单列）已实质化解②③，①列名（registered_capital_value）是 GDF 侧 ODS 抽取问题不在本单 | 唐复核后把 seed pending_cosign 转正式已签 |
| 3 | 展示侧 `gkx_show_service/views/svc_factor.py` 读同一表同一键，灌数后展示系统同步受益 | 无需动作，登记知会 |
| 4 | 数据时效=20261022 快照（口径 update_freq=daily） | 后续接数据工厂日常增量化；当前单次灌数满足演示 |

## 5. 架构合规自检

| 铁律 | 自检 |
|---|---|
| 调用链（FE→Java→Python） | ✅ 未动调用链，仅补 ADS 数据 |
| 算法只在 Python | ✅ 无算法逻辑变更，数字来自 Python 复现脚本（已入仓） |
| 数据策略 ADS 先行 | ✅ 写 ADS `svc_metric_dist`，未触碰 ODS/DWD/三方库 |
| D16 gapfill | ✅ 不适用（ADS 表既有结构，非缺口补表） |
| D9 血缘（ⓘ/8件套/D4） | ✅ matrix+seed 同步翻转，阶段清单如实 n/a，未伪闭合 |
| D19 字符集 | ✅ 未建表；表既有 utf8mb4_general_ci |
| commit 标注 | ✅ `[agent:coordinator]`（本会话执行者身份） |

## 6. cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | ~45,000 |
| model_used | glm-5.3-Flash |
| actual_cost | ~$0.4 |
| cost_warn | false |
