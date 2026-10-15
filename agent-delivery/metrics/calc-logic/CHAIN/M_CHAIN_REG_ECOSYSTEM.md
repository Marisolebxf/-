# M_CHAIN_REG_ECOSYSTEM 区域产业生态（配套生态完备度）计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（方案A=区域链上环节覆盖度；分母=L1 环节）
- **类型**：STAT（比例，0—100%）
- **is_mock**：true（链桥仅 INB1309 mock 灌数；全量挂链 CHAIN-P0-5 交付后转 live）

## 1. 原始定义档案

- **页面语境**：专题系统 · 产业链分析 · 区域产业评价页（`TOPIC-REG-020`），支撑力叶子（QC11 四力：支撑力=服务机构/政策覆盖率/**配套生态**，权重 8/100）；UI 描述"**配套设施与生态完备度**"，来源标签"配套生态库"；A1 需规 `ALGO-CHAIN-DEEP-126`（配套生态竞争力，输入含配套服务数据）。
- **白话**：这个区域的企业在链上的环节铺得全不全——链条 6 个大环节（L1）里，本地企业实际占了几个。占得越全，说明本地配套越不用依赖外地，生态越完备。
- **旧稿问题（本版废除）**：v1 seed formula = `COUNT(DISTINCT credit_code)`，与 `M_CHAIN_ENTERPRISE_COUNT` 完全同数（企业数复述），"生态完备度"语义为空；且未入 `M_CHAIN_SUPPORT_POWER` 合成（8 分权重孤儿叶子）。

## 2. 指标定义（v0.2.0，方案A）

**区域配套生态完备度 = 区域内链上企业挂点归一覆盖的 L1 环节数 / 该链 L1 环节总数 × 100%。**

- **分母（拍板：L1）**：`industry_chain_node` 中该链 `node_level=1` 的环节全集（同页 `M_CHAIN_REG_POLICY_COVERAGE` 分母同尺；INB1701 实测 L1=6，全局 15 链 L1 合计 28）；
- **分子**：链桥 `enterprise_industry_chain.node_id` 挂点，**挂 L2 的向上归一到 L1**（`COALESCE(n.parent_node_id, e.node_id)`），去重计数——挂点深度不齐（L1/L2 混挂）鲁棒；
- **区域轴**：链桥 `org_id` JOIN 主档 `dwd_org_base_info.org_id AND city = :region_city`（org_id 全键，禁名称匹配，2026-10-14 通则）；
- **同族区分注记**：与 `M_CHAIN_SZ_COMPLETENESS`（深圳专题、六环节服务链轴）不同族、不同轴；与 ENT 域 `M_ENT_CHAIN_COMPLETENESS`（全域跨链、叶子分母）语义不同构，不强行对齐。

## 3. Formula（SQL）

```sql
SELECT ROUND(100 * cov.covered / denom.total, 1) AS ecosystem_pct
FROM (SELECT COUNT(*) AS total
      FROM demo_gkxlumenx_dwd.industry_chain_node
      WHERE chain_id = :chain_code AND node_level = 1 AND is_deleted = 0) denom,
     (SELECT COUNT(DISTINCT COALESCE(n.parent_node_id, e.node_id)) AS covered
      FROM demo_gkxlumenx_dwd.enterprise_industry_chain e
      JOIN demo_gkxlumenx_ods.dwd_org_base_info b
        ON b.org_id = e.org_id AND b.is_deleted = 0 AND b.city = :region_city
      LEFT JOIN demo_gkxlumenx_dwd.industry_chain_node n
        ON n.node_id = e.node_id AND n.is_deleted = 0
      WHERE e.chain_code = :chain_code AND e.node_id IS NOT NULL) cov;
```

- 链桥 0 行或环节字典缺该链 → 覆盖 0，如实 0% + ⚠️ PendingBadge，不造数。
- 注：挂点为 L1 时 `parent_node_id` 为空/NULL → `COALESCE` 取自身；挂点为 L2 时取父。若现网存在 L3+ 挂点，归一改用递归向上（首版按两级写，实测挂点最深 L2）。

## 4. 表依赖与实核（2026-10-14 demo）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd.enterprise_industry_chain` | 分子链桥（挂点+区域键） | INB1309 链 2000 行 mock 已灌（1984 家）；深圳×INB1309 = 1004 家（org_id→city 全键实测通）；其他链 0 行 |
| `dwd.industry_chain_node` | 分母环节字典 | DDL 实核（node_id/node_level/parent_node_id/is_deleted，INB 升格主键）；链桥选点同源于此表，**同编码空间免映射** |
| `dwd_org_base_info` | 区域轴 city | 189,116 行 org_id 全唯一（同族指标共用实核） |

## 5. 缺口分型

| 项 | 分型 | 处置 |
|---|---|---|
| 链桥仅 1 链 mock 灌数 | 数据未灌（DWD DDL 在案） | 不报缺；CHAIN-P0-5 全量挂链交付灌入即真数，口径不动 |
| `is_mock: true` | mock 挂链产物 | INB1309 现值为演示值（弱对齐+确定性选点），标注 D4=mock + 🧪 MockBadge |
| L1 饱和（强市 6/6=100%） | 口径特性（非缺口） | 如实接受；演进路径（不进首版）：企业数饱和加权 hit/(hit+k) 或 UI 并列绝对数"覆盖 6/6 环节"，与政策覆盖率加权演进（v0.3）同路 |
| 环节全集层级 | D1 决策点 | 已拍板 L1（human:徐滕强 2026-10-14）；正式签名挂 pending_cosign: human:唐绍祖 |

## 6. 验证记录（2026-10-14）

- 分母字典：INB1701 L1=6 / L2=26 实测在库；全局 L1 合计 28（15 链）。
- 分子链路：深圳×INB1309 org_id 全键 1004 家实测通（CAST utf8mb4_0900_ai_ci 归一连通，collation 统一通则）。
- 端到端复跑：当前环境不在内网（192.168.88.43/.90 不通），回内网/公网通道后按 §3 SQL 复跑 INB1309×深圳 出演示真值；其他链预期 0% + ⚠️。
