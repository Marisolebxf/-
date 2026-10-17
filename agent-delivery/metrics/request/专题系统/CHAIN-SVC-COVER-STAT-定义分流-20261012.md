# 产业链 + 服务链 STAT/COMPUTE：定义分流（2026-10-12）

接手：`human:徐滕强`。企业 `ENT-SYNTH-METRIC-COVER-STAT-L01` 口径已齐、看板 `integration`（待唐绍祖会签）。  
本文件只分流 **CHAIN / SVC 的 STAT + COMPUTE**。不改 seed。一条一过仍要人点头再写 YAML。  
尺子同企业：团队临时 🟡，不升甲方 🟢，不升 D3 `full` / D4 `live`。

| 模块 | STAT | COMPUTE | D1 已对齐 | 待确定 |
|------|------|---------|-----------|--------|
| 产业链 CHAIN | 29 | 2 | 4 | 27 |
| 服务链 SVC | 21 | 0 | 0 | 21 |

registry 另有 UNKNOWN（CHAIN 20 / SVC 8），**不进本分流**，避免和 STAT 混裁。

---

## 产业链 CHAIN（31）

### A · 口径已清（4）

D1=`aligned`，本轮不当定义问题。

`M_CHAIN_SZ_ENTERPRISE_COUNT` · `M_CHAIN_SZ_ENTERPRISE_RATIO` · `M_CHAIN_SZ_KEY_NODE_COVERAGE` · `M_CHAIN_SZ_PROBLEM_COUNT`

### B · 有公式骨架、无矩阵 D1（22）

seed 里已有 COUNT/占比写法，**缺矩阵行**（查询 D1 为空）。本轮可按企业同款：钉公式 + 补矩阵 D1=`aligned`，Q 仍 🟡。

`M_CHAIN_TOTAL_COUNT` · `ENTERPRISE_COUNT` · `ENTERPRISE_NEW_COUNT` · `INSTITUTION_COUNT` · `PATENT_COUNT` · `PRODUCT_COUNT` · `INVEST_COUNT` · `NEWS_COUNT` · `HOT_NEWS_COUNT` · `NEWS_SENTIMENT_RATIO` · `GLOBAL_REGION_COUNT` · `NATIONAL_REGION_COUNT` · `SZ_REGION_COUNT` · `SZ_INSTITUTION_COUNT` · `SZ_COMPLETENESS` · `MARKET_SIZE` · `MARKET_GROWTH` · `HIGH_VALUE_RATIO` · `LAYOUT_RECOMMEND_COUNT` · `BOTTLENECK_COUNT` · `BOTTLENECK_SEVERITY` · `BOTTLENECK_TYPE_DIST`

### C · 请算法 / 人对（5）

| ID | 现稿 | 请定 |
|----|------|------|
| `M_CHAIN_CONCENTRATION_INDEX` | COMPUTE；`pending_algorithm` HHI 或 CR_N | 用 HHI 还是 CR_N；N=？ |
| `M_CHAIN_INTERNATIONALIZATION_INDEX` | COMPUTE；pending | 公式/分母 |
| `M_CHAIN_SZ_ADVANTAGE_RANK` | draft；QC08 对标城市 | 对标集合 + 排序键 |
| `M_CHAIN_CHOKE_LINK_COUNT` | draft；类型未签 | 卡脖子判定 |
| `M_CHAIN_BASE_95_1` | draft；OPEN 身份 | 是否本波 STAT、还是模型构建说明项 |

---

## 服务链 SVC（21 STAT，0 COMPUTE）

**没有 A。** 21 条矩阵全 `draft`，formula 基本 `pending_cosign: human:唐绍祖`，挂 `GAP-ALGO-TYPE-UNSIGNED`（`TYPE_DIST_QUERY` 另挂 Q-MO-QUERY-04）。

本波不能假装有可执行口径。建议顺序：

1. 唐绍祖先签 **algorithm_type=STAT**（或剔掉不是 STAT 的）。
2. 再按企业一条一过写 formula / `source_tables` / D1。

清单（全待定）：

`M_SVC_ORG_TOTAL` · `ORG_NEW_COUNT` · `ORG_SELECTED_COUNT` · `ORG_COVERAGE_BREADTH` · `TYPE_DIST_QUERY` · `CHAIN_SEGMENT_ORG_COUNT` · `CHAIN_SEGMENT_AVG_DEPTH` · `SZ_CHAIN_COMPLETENESS` · `SZ_COMPARE_METRIC` · `REC_CANDIDATE_CNT` · `PT_GLOBAL_TOTAL` · `PT_GLOBAL_TYPE_DIST` · `PT_GLOBAL_SCALE_DIST` · `PT_SZ_TOTAL` · `PT_SZ_TYPE_DIST` · `PT_SZ_FIELD_DIST` · `PT_SZ_REGION_ORG` · `PT_REGION_ORG` · `PT_CHAIN_NODE_ORG` · `PT_KEYORG_SCALE` · `BASE_101_1`

---

## 建议开工顺序

1. **CHAIN B 22**：先拟改 1 条（建议 `M_CHAIN_TOTAL_COUNT`）给人点头，再铺开。  
2. **CHAIN C 5**：算法/QC08 未答之前不写 YAML。  
3. **SVC 21**：等类型会签；未签不开一条一过。

registry 尚无 CHAIN/SVC 的 COVER-STAT 叶。要建单须 coordinator / PM；未建单前只分流、不改 YAML。

维护：`human:徐滕强`。禁止整批改 CHAIN/SVC seed。
