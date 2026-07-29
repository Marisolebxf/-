# ENT-MOD-KEYPANO-METRIC-OPEN-L01 —— 重点企业概览指标语义与 ODS/DWD 数据缺口核对

> **任务**：ENT-MOD-KEYPANO-METRIC-OPEN-L01
> **执行人**：algorithm-agent（human:唐绍祖）+ data-agent
> **日期**：2026-07-29
> **状态**：✅ 完工

---

## 1. 产出物清单

| 文件 | 路径 | 说明 |
|------|------|------|
| METRIC-OPEN-ENT-KEYPANO-核对记录.md | agent-handoffs/产品整体定义/E-20_E-22-重点企业分析/ | #4/#5适用性、8 metric口径摘要、指标×贴源矩阵、PDR-05/06自检、唐绍祖会签 |
| ENT-KEYPANO-data-gap-catalog.yaml | agent-handoffs/产品整体定义/E-20_E-22-重点企业分析/ | UI 缺口文案真源, 8 条 metric ≥2条 ≥80字 pending_hint |
| cfg_metric-ENT-seed.yaml | metrics/ | KEYPANO 相关条目已更新 8 件套字段（由下游 ALGO-METRIC-ALIGN 任务统一处理） |

## 2. 核心产出

- 8 个 KEYPANO metric 全部完成 definition/formula/source_tables/mapping_status 评估（0 ✅ / 6 🔧 / 2 ⚠️ / 0 ❌）
- KEYPANO 核心判定：**门户概览模块，不计算新算法，全部指标为对已入库数据的聚合、分组和 JOIN 消费**
- 明确了 KEYPANO 的消费链路：企业识别(Q038) → 产业链映射 → 资质分组(Q010) → 区域聚合(Q012) → 领域映射(Q013/Q047)
- 6 个开放项 + 3 个 GAP 登记为 🟡/❌ 不伪闭合：Q010/Q012/Q013/Q038/Q039/Q047, GAP-KEYPANO-REGIONAL-SCALE, GAP-KEYPANO-REGIONAL-RATIO, GAP-KEYPANO-CHAIN-MAPPING
- 整链资质分布的口径约束已明确：4 资质类型 × 3 地域层级交叉分组矩阵，完整嵌套口径（深圳市/广东省/全国独立计数，非增量堆叠），固定顺序、零值显示 0、只读不筛选企业列表

## 3. 范围证明

- ✅ 仅处理 KEYPANO 门户展示指标口径（E-33 重点企业概览）
- ✅ 不替甲方闭合 Q010/Q012/Q013/Q047 最终业务口径
- ✅ 不产生新算法模型——全部指标为聚合/分组/消费已计算结果
- ✅ KEYPANO 不展示企业评分、风险评级、推荐排名——对应指标不在本模块注册
- ✅ 不包含 Java/Python 算法实现
- ✅ 不修改 demo 页面或数据库表结构

## 4. 架构合规自检

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 仅改动 agent-delivery 文档,未动 demo 页面或数据库 | ✅ |
| 2 | metric 口径引用 PDR/Decision/四件套,非新拍板 | ✅ |
| 3 | pending_hint ≥80 字（≥3 条达标） | ✅ |
| 4 | 唐绍祖 §1.4.1 会签 | ✅ |
| 5 | cost 四字段已填写 | ✅ |
| 6 | KEYPANO 不计算算法,全部指标归类为聚合消费 | ✅ |
| 7 | 整链资质分布使用完整嵌套口径,非增量堆叠 | ✅ |
| 8 | 领域指标不占位 Q013 未闭合的广度/深度/多元化 | ✅ |
| 9 | 未新增 Bid 叶子或产品增强 | ✅ |
| 10 | 企业评分/风险/推荐不在 KEYPANO 范围 | ✅ |

## 5. 已知限制与下游提示

| 限制 | 影响范围 | 提示 |
|------|---------|------|
| 产业链→企业映射表需 ADS 构建 | M_ENT_KEYPANO_MATCH_COUNT, M_ENT_KEYPANO_ENTERPRISE_LIST | 数据 agent 需建立 ads.enterprise_keypano_chain_node 视图 |
| 资质×地域交叉矩阵需预计算 | M_ENT_KEYPANO_QUAL_DISTRIBUTION | 数据 agent 需构建 12 格二维聚合表 |
| 关键词→领域映射规则未闭合 | M_ENT_KEYPANO_DOMAIN_SUMMARY | 依赖 Q013/Q047 闭合后由数据 agent 更新映射规则表 |
| 区域企业规模/占比无正式 metric_id | M_ENT_KEYPANO_REGIONAL_DISTRIBUTION | 业务模式省略，不得用高企占比代替 |
| Q038 企业识别阈值影响全量 | 所有 M_ENT_KEYPANO_* | 变更阈值后需刷新全部 ADS 聚合表 |

## 6. 下游待解锁

| 任务 ID | 状态 |
|---------|------|
| ENT-MOD-KEYPANO-PDR-G1-RECLOSE | → **ready**（METRIC-OPEN 完工后解除阻塞） |
| ENT-MOD-OVERVIEW-PDR-G1 | → **ready**（KEYPANO + STAR + SHENZHEN 汇总门1） |
| DATA-ENT-CMS-VS-APP-PARTITION-L01 | → 可并行（E-33 CMS vs APP 分区独立） |

## 7. Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 100_000 |
| actual_tokens | 72_000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.43 |
| cost_warn | green |

## 8. Commit info (pending)

| 字段 | 值 |
|------|-----|
| branch | pending commit |
| commit_hash | pending commit |
| pushed | pending commit |
