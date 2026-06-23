# Handoff —— DATA-POLICY-db-design

- **任务**: POLICY-PROTO-L01（Epic: E-POLICY-PROTOTYPE）
- **角色**: data-agent ｜ **日期**: 2026-06-23 ｜ **Wave**: 0（标准表先行 + Mock）
- **commit 标记**: `[agent:data]`

## 1. 范围与实现

产出政策域数据库设计 **`data/政策域数据库设计(v1).md`**，参照企业域设计格式（无现存企业域设计文件，
按 D9 + registry 约定自定结构），覆盖 DWD 标准明细层、ADS 应用聚合层、NebulaGraph 图谱、Mock 策略、
ETL 阶段建议、架构合规自检、风险。同步在 `data-source-mapping-registry.yaml` 追加政策标准表登记。

### 交付内容
- **DWD**：`dwd.policy_base_info`（37 字段，完全照映射报告 §4；映射状态 ✅19/🔧4/⚠️4/🟦10）
- **ADS（9 张）**：`ads_policy_level_dist` / `ads_policy_type_dist` / `ads_policy_timeseries` /
  `ads_policy_national_dist` / `ads_policy_sz_dist` / `ads_policy_focus` / `ads_policy_intensity` /
  `ads_policy_effect` / `ads_policy_metric_timeseries`（均给出列定义 DDL 草案 + metric_id 关联）
- **NebulaGraph space `gkx_policy`**：7 tag（policy/industry/tech/enterprise/talent/org/service）
  + 4 edge（support 扶持 / apply_to 适用 / regulate 监管 / cite 引用谱系），含 nGQL 草案
- **Mock 策略**：batch=mock_20260623，仅 Python 写 ADS，固定种子，贴近真实分布/空值率
- **ETL 三阶段**：直接映射加载 → 轻量加工 → 国际政策接入

## 2. 与 bid / 映射报告对照

- DWD 37 字段 1:1 照搬映射报告 §4，覆盖率 85.2%（23/27 有源）。
- ADS 9 张表覆盖 5 基础指标 + 门户扶持 + 深度模型 + 三维框架全部 19 个 metric_id。
- 图谱 tag/edge 对应 bid §1.1.1.1.1.1.1.2.5/2.6（政策实体识别 + 政策实体关系抽取）。
- ODS 字段名差异（现行 DDL vs 映射报告逻辑名）已在设计 §2 注明 ETL 对齐规则。

## 3. 架构合规自检（§2 十条）

| # | 铁律 | 自检 |
|---|------|------|
| 1 | 算法只在 Python | ✅ 评分/图算法标 🔧 交 Python；DDL 不含算法 |
| 3 | 图谱 NebulaGraph(gkx_policy) 禁 Neo4j | ✅ space gkx_policy + 7tag/4edge |
| 7 | Java 只读 ADS / 不直连 nGQL | ✅ ADS 供 Java 只读；图节点 PG 镜像双写 graph_node/edge |
| 8 | 标准表先行 + Mock | ✅ ADS 先行 + mock_20260623 |
| 10 | D9 8 件套 | ✅ 每张 ADS 带 metric_id 关联 cfg_metric-POLICY-seed.yaml |

（4/5/9 由 api/前端/CI 落地，设计类制品 cicd: skip；6 不动 lumen）

## 4. 阻塞与风险

| 风险 | 缓解 | 责任 |
|------|------|------|
| QPOL-01/02/03 口径未定 | 临时默认 + 标 ⚠️/🔧；上线前甲方确认 | PM/算法 lead+甲方 |
| 效果/落地执行数据无 ODS 来源 | Wave0 Mock，source_tables 标"待采购" | PM+数据 lead |
| 深度字段(elements/pedigree…) 格式未确认 | 与供方确认 JSON schema | data-agent+供方 |
| 国际政策口径差异 | level='国际'+source 区分，或单建 dwd.policy_intl_ext | data-agent |
| 标题超长(源1000>DWD500) | ETL LEFT(title,500) 截断 | data-agent |

均不阻塞设计产出；接力 algorithm-agent（formula/图算法）+ P1 数据工厂（填 source 侧映射）。

## 5. 产物清单

- `agent-delivery/data/政策域数据库设计(v1).md`
- `agent-delivery/data-source-mapping-registry.yaml`（追加 dwd.policy_base_info + 9 ADS + gkx_policy 登记）

## 6. 接力

- **algorithm-agent**：在 NebulaGraph gkx_policy 实现关联度/图算法；实现评分类 ADS 的 formula。
- **mock 脚本**：`mock/policy_ads_generator.py`（Python，seed=42）按 §5 策略生成 9 张 ADS 的 Mock。
- **api-agent**：gkxlumen-metrics 暴露上述 metric_id catalog/lineage。
- **P1 数据工厂**：三方源就绪后填 registry 的 source 侧字段，状态 pending_source → mapped → verified。
