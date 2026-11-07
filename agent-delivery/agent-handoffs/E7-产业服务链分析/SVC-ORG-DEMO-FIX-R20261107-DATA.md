# SVC-ORG-DEMO-FIX-R20261107-DATA · 对比篮补回 guest 篮内君智容与星诚优威两行（handoff）

- Epic：E7-产业服务链分析；agent=data-agent；监管人=human:徐滕强；强度=ponytail full
- 缺口来源：`SVC-ORG-DEMO-ACCEPT-LOOP` 第 1 轮步②（`agent-delivery/agent-handoffs/E7-产业服务链分析/SVC-ORG-DEMO-ACCEPT-LOOP.md`）
- 期望真源：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-ORG-合规演示用例.md` 查库节（7.1.1 ②「篮内已有 id 57/60/61 三行可直勾」输入前置）
- 执行时间：2026-11-07 21:22（UTC+8）

## 1. 范围与实现

- 缺口键：`gkxlumenx_topic_enterprise.svc_compare_basket_item` 中 `user_id=guest` 缺 2 行——
  - `004671cda32d4c5eab3909fd5adbb709` 东莞市君智容物联技术有限公司（用例期望篮 id=60）
  - `007d0adc0898c1baa7eed10f7f14c650` 东莞市星诚优威智能科技有限公司（用例期望篮 id=61）
- 修复方式：**纯 SQL 数据修复**（database MCP `demo-gkxlumenx-ods` 连接，read-write，execute_mutation INSERT 两行），**无脚本入仓**（按派单「二选一取最简」，SQL 全文记录于本 handoff §3）。
- 行内容对齐：`org_name` 取 `demo_gkxlumenx_ads.svc_org_card` 主档真实 `name_cn`（见 §3 查证）；`source='对比篮新增'`、`user_id='guest'` 均仿现存行；行 id 取下一可用序列 64/65（允许漂移）。

## 2. 影响面

- 仅 `gkxlumenx_topic_enterprise.svc_compare_basket_item` 新增 2 行（id=64/65），guest 篮由 2 行恢复到 4 行（派单预期 4 行）。
- **不改现存 2 行**（id=62 东劲、id=63 双奉写前后值逐字段一致）；**不改** `demo_gkxlumenx_ads.svc_org_card` 主档；**不写** ODS/DWD/ADS/正式 lumen 库/`gkx-lumen` 桶；**不改** `lumen-svc-platform` 任何代码；**不改**用例期望。
- 下游解锁：`SVC-ORG-DEMO-FIX-R20261107-QUERY`（三家组合 coverage 快照签发）依赖本单修篮，篮内君智容/星诚优威已可直勾。

## 3. 执行证据

### 3.1 修复前只读查证（SELECT，2026-11-07 21:21）

表结构（8 列）：`id, user_id, org_id, org_name, source, operated_at, create_time, update_time`；现存 2 行：

| id | user_id | org_id | org_name | source | create_time |
|---|---|---|---|---|---|
| 62 | guest | 0071aadf76b85d194db1083f01ac78de | 东莞东劲新能源科技有限公司 | 对比篮新增 | 2026-11-07 18:06:09 |
| 63 | guest | 007050fca591f96308b7fd0ced8cffa3 | 东莞双奉科技有限公司 | 对比篮新增 | 2026-11-07 18:06:09 |

id 序列确认：最大 63 → 下一可用 64/65。
主档查证（`svc_org_card` 只读 SELECT，2/2 命中，名称与用例样例清单逐字一致）：
- `004671cda32d4c5eab3909fd5adbb709` → 东莞市君智容物联技术有限公司（INNOV，东莞市）
- `007d0adc0898c1baa7eed10f7f14c650` → 东莞市星诚优威智能科技有限公司（INNOV，东莞市）

### 3.2 修复 SQL（全文，唯一写操作）

```sql
INSERT INTO gkxlumenx_topic_enterprise.svc_compare_basket_item
  (id, user_id, org_id, org_name, source, operated_at, create_time, update_time)
VALUES
  (64, 'guest', '004671cda32d4c5eab3909fd5adbb709', '东莞市君智容物联技术有限公司', '对比篮新增', NOW(), NOW(), NOW()),
  (65, 'guest', '007d0adc0898c1baa7eed10f7f14c650', '东莞市星诚优威智能科技有限公司', '对比篮新增', NOW(), NOW(), NOW());
```

结果：affectedRows=2；MCP 自动生成回滚快照（2026-11-07T13-22-21-015Z-w3fa，失败可逆）。

### 3.3 修复后全表证据（SELECT，2026-11-07 21:23，4 行=派单预期）

| id | user_id | org_id | org_name | source | create_time |
|---|---|---|---|---|---|
| 62 | guest | 0071aadf76b85d194db1083f01ac78de | 东莞东劲新能源科技有限公司 | 对比篮新增 | 2026-11-07 18:06:09（原行未动） |
| 63 | guest | 007050fca591f96308b7fd0ced8cffa3 | 东莞双奉科技有限公司 | 对比篮新增 | 2026-11-07 18:06:09（原行未动） |
| 64 | guest | 004671cda32d4c5eab3909fd5adbb709 | 东莞市君智容物联技术有限公司 | 对比篮新增 | 2026-11-07 21:22:21（新增） |
| 65 | guest | 007d0adc0898c1baa7eed10f7f14c650 | 东莞市星诚优威智能科技有限公司 | 对比篮新增 | 2026-11-07 21:22:21（新增） |

7.1.1/7.3.1 演示主路径输入前置恢复：双奉(63)/君智容(64)/星诚优威(65) 三行在篮可直勾（行 id 相对用例期望 57/60/61 漂移，符合派单允许）。

### 3.4 偏离说明

- 无实质偏离。用例查库节「6 行」为 2026-11-05 全量操作语义，本轮派单明确收窄为补君智容/星诚优威 2 行（其余 2 行属检索前置步骤产物，不在本 DATA 单范围，id 漂移已获派单允许）。

## 4. 产物清单

- 数据库写操作 1 条（§3.2），回滚快照 1 份（MCP 托管）。
- 本 handoff。**无代码/脚本改动**（demo-algo-ent-analysis 零提交，无 git 操作）。

## 5. 成本（cost 四字段）

| 字段 | 值 |
|---|---|
| actual_tokens | ~42000 |
| model_used | glm-5.3-Flash |
| actual_cost | 0.05（美元，估算） |
| cost_warn | green（远低于 $10 告警线） |

## 6. 架构合规自检（逐条对照团队公约 §2）

| 铁律 | 自检 |
|---|---|
| 1 算法只在 Python | ✅ 本单纯数据 INSERT，无算法逻辑 |
| 2 调用链不可越层 | ✅ 未触碰任何服务代码/接口 |
| 3 图谱 NebulaGraph | ✅ 未涉及图谱 |
| 4 可观测性埋点 | ✅ 不适用（无代码变更） |
| 7 共享聚合核心 | ✅ 未触碰 Java/Python/前端共享面 |
| 8 数据策略（ADS 先行+Mock 填充） | ✅ demo 库数据修复，属演示数据填充范畴 |
| 12 demo/lumen 隔离（D12） | ✅ 仅写 demo 库 `gkxlumenx_topic_enterprise`（demo-gkxlumenx-ods 连接）；未写正式 `gkx*` lumen 库；未触碰 lumen 仓 |
| 14 缺项补齐（D16） | ✅ 未建 gapfill 表、未写供应方库/ODS/DWD/ADS（仅 demo topic 业务演示库篮表） |
| 17/18 演示态诚实性 | ✅ 未伪造主档、未改用例期望；`source` 沿用既有语义 |
| 人机协作 §3.6/3.7 | ✅ 本 handoff + cost 已回填 registry |

## 7. ponytail

ponytail: full——修复取阶梯第 1 档：纯 SQL 一条语句 + 全表 SELECT 证据，零脚本、零新依赖、零代码改动；handoff 即自检记录。

## 8. 任务终态

`in_progress → pending_test`（task-review 自动验收推进），停在 `pending_test` 待 QA 领取；不再往后推（签收 = human:淮政玮）。
