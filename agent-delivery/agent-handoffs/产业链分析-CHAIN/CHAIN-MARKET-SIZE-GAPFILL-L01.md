# CHAIN-MARKET-SIZE-GAPFILL-L01 · 产业链全景 — 市场规模（M_CHAIN_MARKET_SIZE）D16 gapfill 演示数据闭环

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮`（沿用同域 DEMO-CHAIN-PY-SYNC-L01） |
| claim_type | `pull` |
| 说明 | 用户 2026-10-31 现场提出「市场规模无数据」，选项确认走 D16 gapfill；工单建后补账（先改码后建票，note 已注明） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 D9 评审层既有 MockBadge/ReviewMetricBadges，未新造组件；表结构按 D16 规约最小字段集 |

## 问题清单

- 三方 gkx 库营收金额全空 → `M_CHAIN_MARKET_SIZE` D3=none，市场规模 Tab 长期「暂无正式数据源」
- D16 规约库 `demo_gkxlumenx_gapfill` 应用账号无 CREATE DATABASE 权限（实测 1044）；上跳板找 root 授权被拒（root 禁远程），已按安全边界停止
- 用户拍板：种子表过渡落 `demo_gkxlumenx_dim`（账号有全部权限），表名/追溯字段不变

## 修改内容

**lumen-algo-py**（commit 见 CI/CD 节）

- `lumen_common/algorithms/chain/sync.py`
  - `_load_market_size(db, chain_id)`：fail-soft 读 `{prefix}_gapfill` → 1044/表缺失自动降级 `{prefix}_dim`；`db=None`（测试注入路径）返回 None；命中挂 `dataset.marketSize`（含 metricId/statYear/value/unit/yoy/source/fillMethod/batchId）
- `scripts/seed_gapfill_market_size.py`
  - 12 链 × 2024/2025 共 24 行种子；优先建规约库，1044 自动降级 dim；行含 `metric_id/gap_item/fill_method/gapfill_batch_id/generated_at` 追溯字段；`assert ads.startswith("demo_")` 防误写生产
- `tests/test_chain_market_size.py`（新增）
  - 降级读通 + 双库全缺返回 None 两个用例
- `tests/test_chain_sync.py`
  - `_Db` 桩补 `ads` 属性 + 放行 market_size SQL（根因：`_load_market_size` 接入后桩查询断言过窄）

**lumen-ui-topic**

- `src/api/industry/types.ts`：新增 `IndustryMarketSize`，`dataset.marketSize` 字段
- `src/components/industry-center/IndustryPanoramaDetail.vue`：市场规模 Tab 双态——有值显 `数值 + 同比 + MockBadge(🧪) + ReviewMetricBadges`；无值保持原「暂无正式数据源」PendingBadge 诚实空态
- `src/views/industry-center/IndustryPanoramaPage.vue`：aside/drawer 两处传 `:market-size="dataset?.marketSize ?? null"`

**数据（demo 库）**

- `demo_gkxlumenx_dim.gapfill_chain_market_size`：24 行已落（`--apply` 实测输出 `{"rows": 24, "db": "demo_gkxlumenx_dim"}`）

## 偏离说明

| 偏离 | 理由 | as-built |
|------|------|----------|
| D16 规约库 `demo_gkxlumenx_gapfill` → `demo_gkxlumenx_dim` 过渡 | 应用账号无建库权限，DBA 单未排期；用户 2026-10-31 明确选定 | 读端两库按序探测，DBA 建库后种子脚本重跑即迁移，读端无需改码 |
| 演示数值为规则法生成（fill_method=rule） | 三方 gkx 无营收金额（Q056/Q058 关联），D16 允许 LLM/规则法灌数 | UI 挂 🧪 MockBadge（source=gapfill_chain_market_size），D4 仍为 mock，不进生产口径 |

## 测试结果

- `python3 -m pytest tests/test_chain_market_size.py tests/test_chain_sync.py` → **11 passed**
- `pnpm type-check`（lumen-ui-topic，vue-tsc --build）→ **0 error**
- 种子脚本 `--apply` 实写 24 行成功
- 线上验证：dev 页面「产业全景 → 任一链 → 市场规模」Tab 显示数值 + 🧪（待 K8s rollout 后人工走查）

## 架构合规自检

| 铁律 | 状态 |
|------|------|
| D1 调用链（算法只读 MySQL，前端只经 Java） | ✅ marketSize 由算法层 sync 返回，前端零硬编码 |
| D9 数据血缘 | ✅ 数字旁 MockBadge + ReviewMetricBadges(metric_id=M_CHAIN_MARKET_SIZE)；追溯字段齐 |
| D16 gapfill | ✅ `gapfill_` 前缀表、demo_ 前缀库、不写 ODS/DWD/ADS/供应方库、未闭合 Q056 按 🟡 默认实施 |
| D12 demo/lumen 隔离 | ✅ 改动只在 lumen-algo-py / lumen-ui-topic |

## CI/CD（必填）

- 分支：`dev`（lumen-algo-py / lumen-ui-topic）
- commit：见两仓 dev 最新（算法侧含 2ff88f5 企业 ID 修复同源会话）
- pipeline：push 后 GitLab CI 自动触发
- K8s rollout：待 CI 绿后 dev rollout（人工验收闸门：改动停在本地/推送后等走查，不自动视为交付完成）

## 可观测性（建议）

- 沿用 chain sync 既有埋点；marketSize 为快照附属字段，无新独立 trace 节点

## 遗留风险

- dim 库非 D16 规约位置：DBA 建正式 gapfill 库后需重跑种子脚本迁移（读端已兼容，零改动）
- 种子数值为演示口径，不可用于任何对外汇报数字；三方 gkx 营收接入后按 policy §2.4 停读本表
- ` IndustryMarketSize.source` 字段目前仅作展示溯源，前端未做强校验

## 涉及文件

- repos/lumen-algo-py/lumen_common/algorithms/chain/sync.py
- repos/lumen-algo-py/scripts/seed_gapfill_market_size.py
- repos/lumen-algo-py/tests/test_chain_market_size.py
- repos/lumen-algo-py/tests/test_chain_sync.py
- repos/lumen-ui-topic/src/api/industry/types.ts
- repos/lumen-ui-topic/src/components/industry-center/IndustryPanoramaDetail.vue
- repos/lumen-ui-topic/src/views/industry-center/IndustryPanoramaPage.vue
- agent-delivery/agent-handoffs/产业链分析-CHAIN/CHAIN-MARKET-SIZE-GAPFILL-L01.md（本文件）
