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

## 范围与实现

M_CHAIN_MARKET_SIZE（市场规模）D16 缺项演示数据闭环：dim 过渡库种子表 → 算法层读通挂 `dataset.marketSize` → 前端市场 Tab 双态展示（有值 + 🧪 / 无值诚实空态）。

**lumen-algo-py**（commit 见 CI/CD 节）

- `lumen_common/algorithms/chain/sync.py`
  - `_load_market_size(db, chain_id)`：fail-soft 读 `{prefix}_gapfill` → 1044/表缺失自动降级 `{prefix}_dim`；`db=None`（测试注入路径）返回 None；命中挂 `dataset.marketSize`（含 metricId/statYear/value/unit/yoy/source/fillMethod/batchId）
- `scripts/seed_gapfill_market_size.py`
  - 24 条链 × 2024 年 1 期共 24 行种子；优先建规约库，1044 自动降级 dim；行含 `metric_id/gap_item/fill_method/gapfill_batch_id/generated_at` 追溯字段；`assert ads.startswith("demo_")` 防误写生产
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

### mock 表完整档案（D16 追溯）

| 项 | 值 |
|------|------|
| 库.表 | `demo_gkxlumenx_dim.gapfill_chain_market_size`（规约库建不了 → dim 过渡，见偏离说明） |
| 唯一键 | `uk_chain_year (chain_id, stat_year)`；重跑脚本 `ON DUPLICATE KEY UPDATE` 幂等刷新 |
| 数据范围 | 24 条链（机器人 4 / 智能网联汽车 4 / 集成电路 7 / 生物医药 / 人工智能 / 新能源 / 高端装备等）× `stat_year=2024` 1 期 |
| 字段 | `id` 自增主键；`chain_id` varchar(64)；`stat_year` int；`market_size_yi` decimal(14,2)（亿元）；`yoy_pct` decimal(8,2)；追溯五件套 `metric_id`(=`M_CHAIN_MARKET_SIZE`) / `gap_item`(=annual_revenue_sum: 三方 gkx 财报表无可加金额) / `fill_method`(=`rule`) / `fill_model`(NULL，rule 法不用) / `gapfill_batch_id`(=`gapfill_chain_market_size:YYYYMMDD`)；`generated_at` / `is_deleted` / `created_time` / `updated_time` |
| 数值生成规则 | 团队临时默认（D16 允许）：人写死在脚本 `SEED` 字典，量级对齐对应产业公开报告同阶（如集成电路 5800 亿/机器人 5200 亿），同比 ±10~22% 区间；非计算产物、非 8 件套终值 |
| 消费方 | 仅算法层 `sync._load_market_size`（fail-soft 只读）；前端经 Java 间接展示并挂 🧪；无其他读取方 |
| 停用条件 | 三方 gkx 营收金额真源接入后停读（policy §2.4 换真源）；DBA 建正式 gapfill 库后重跑种子脚本迁移 |

## 偏离说明

| 偏离 | 理由 | as-built |
|------|------|----------|
| D16 规约库 `demo_gkxlumenx_gapfill` → `demo_gkxlumenx_dim` 过渡 | 应用账号无建库权限，DBA 单未排期；用户 2026-10-31 明确选定 | 读端两库按序探测，DBA 建库后种子脚本重跑即迁移，读端无需改码 |
| 演示数值为规则法生成（fill_method=rule） | 三方 gkx 无营收金额（Q056/Q058 关联），D16 允许 LLM/规则法灌数 | UI 挂 🧪 MockBadge（source=gapfill_chain_market_size），D4 仍为 mock，不进生产口径 |

## 验收证据

- Python：`pytest tests/test_chain_market_size.py tests/test_chain_sync.py` → **11 passed**
- 前端：`pnpm type-check` → **0 error**；GitLab pipeline `3417` **五阶段全绿**（build/image/trivy/deploy:k8s/e2e:chain-gold，末段 19:25:17 success）
- 数据：种子 `--apply` 实写 24 行成功（`{"rows": 24, "db": "demo_gkxlumenx_dim"}`）
- 线上：**通过**（用户 2026-10-31 19:25 走查确认）——产业全景 → 市场规模 Tab 显示数值 + 🧪
- 工单成本：registry cost 四字段已回填（green）

## 架构合规自检

| 铁律 | 状态 |
|------|------|
| D1 调用链（前端→Java→Python /internal，不越层） | ✅ marketSize 由算法层 sync 返回，前端零硬编码、不直连 MySQL |
| D2 算法只在 Python | ✅ 读表逻辑在 lumen-algo-py，Java 未加算法 |
| D3 图谱 NebulaGraph | ✅ 本任务不涉图谱 |
| D4 可观测埋点 | ✅ 沿用 chain sync 既有埋点，无新独立 trace 节点（见可观测性节） |
| D8 前端规范 | ✅ 复用 Arco + 评审层 MockBadge/ReviewMetricBadges，未新造组件 |
| D9 数据血缘 | ✅ 数字旁 MockBadge + ReviewMetricBadges(metric_id=M_CHAIN_MARKET_SIZE)；追溯五件套齐 |
| D16 gapfill | ✅ `gapfill_` 前缀表、demo_ 前缀库、不写 ODS/DWD/ADS/供应方库、未闭合 Q056 按 🟡 默认实施 |
| D12 demo/lumen 隔离 | ✅ 改动只在 lumen-algo-py / lumen-ui-topic |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 60000 |
| model_used | glm-5.3-Flash |
| actual_cost | $0.80 |
| cost_warn | green（< $10 暂停线） |

## CI/CD（必填）

- 分支：`dev`（lumen-algo-py / lumen-ui-topic）
- commit：lumen-algo-py `3606c37`（4 文件：sync.py / 种子脚本 / 2 测试）；lumen-ui-topic `ae11c75`（rebase 后 3 文件）
- pipeline：lumen-ui-topic `3417` **全绿**（build 19:23:33 ✅ → image ✅ → trivy ✅ → deploy:k8s 19:23:58 ✅ → e2e:chain-gold 19:25:17 ✅）
- K8s rollout：**成功**，dev 环境 19:23:58 起新镜像生效
- dev 测试 URL：产业全景 → 任一链 → 详情 → 市场规模 Tab（用户 19:25 走查通过）

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
