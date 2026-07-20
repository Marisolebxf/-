# ENT-EVAL-ALGO-METRIC-ALIGN-L01 —— 企业评估指标与权重对齐算法定义

> **任务**：ENT-EVAL-ALGO-METRIC-ALIGN-L01
> **执行人**：algorithm-agent（human:唐绍祖）
> **日期**：2026-07-20
> **仓**：`demo-ui-topic`
> **状态**：✅ 完工

---

## 1. 对齐矩阵

### 1.1 技术力（technology / E-23）

| 指标 key | 中文名 | group | metricId | 默认权重 | 算法源字段 | entanHelp Tab |
|----------|--------|-------|----------|---------|------------|---------------|
| `talent` | 技术人才 | 技术力五维 | `M_ENT_TECH_POWER_SCORE` | **20**（原 0） | `settings.yaml#tech_power_weights.talent=0.20` | tech |
| `innovation` | 技术创新 | 技术力五维 | `M_ENT_PATENT_GRANT_COUNT` | **25**（原 30） | `settings.yaml#tech_power_weights.innovation=0.25` | tech |
| `transfer` | 技术转化 | 技术力五维 | `M_ENT_TECH_POWER_SCORE` | **20**（原 0） | `settings.yaml#tech_power_weights.transfer=0.20` | tech |
| `cooperation` | 技术合作 | 技术力五维 | `M_ENT_TECH_POWER_SCORE` | **15**（原 0，不可用） | `settings.yaml#tech_power_weights.cooperation=0.15` | tech |
| `investment` | 技术投入 | 技术力五维 | `M_ENT_RD_INVESTMENT_RATIO` | **20**（原 35） | `settings.yaml#tech_power_weights.investment=0.20` | tech |

- **算法权重真源**：`demo-algo-ent-analysis/conf/settings.yaml` → `tech_power_weights`
- **默认权重合计**：20+25+20+15+20 = 100（×100 整数展示，原 settings.yaml 和为 1）
- **旧 indicators 移除**：tech-score(25)、tech-rank(10)、patent-grant(30)、patent-citation(GAP)、rd-ratio(35)、rd-personnel-ratio(GAP)、core-tech-coverage(GAP)
- **旧 GAP metric** 保留在 `cfg_metric-ENT-seed.yaml` 中，UI 层不再展示为可选指标

### 1.2 商业力（business / E-24）

| 指标 key | 中文名 | group | metricId | 默认权重 | 算法源字段 | entanHelp Tab |
|----------|--------|-------|----------|---------|------------|---------------|
| `market` | 市场 | 商业力六维 | `M_ENT_BUSINESS_POWER_SCORE` | **22**（原 0） | `settings.yaml#biz_power_weights.market=0.22` | biz |
| `product` | 产品 | 商业力六维 | `M_ENT_BUSINESS_POWER_SCORE` | **16**（原 0） | `settings.yaml#biz_power_weights.product=0.16` | biz |
| `brand` | 品牌 | 商业力六维 | `M_ENT_BUSINESS_POWER_SCORE` | **16**（原 0） | `settings.yaml#biz_power_weights.brand=0.16` | biz |
| `cooperation` | 技术合作 | 商业力六维 | `M_ENT_BUSINESS_POWER_SCORE` | **14**（不可用） | `settings.yaml#biz_power_weights.cooperation=0.14` | biz |
| `chain_coverage` | 产业链覆盖率 | 商业力六维 | `M_ENT_BUSINESS_POWER_SCORE` | **16**（原 0） | `settings.yaml#biz_power_weights.chain_coverage=0.16` | biz |
| `chain_keynode` | 关键环节参与度 | 商业力六维 | `M_ENT_BUSINESS_POWER_SCORE` | **16**（原 0） | `settings.yaml#biz_power_weights.chain_keynode=0.16` | biz |

- **算法权重真源**：`demo-algo-ent-analysis/conf/settings.yaml` → `biz_power_weights`
- **默认权重合计**：22+16+16+14+16+16 = 100
- **旧 indicators 移除**：business-score(25)、revenue(25)、revenue-growth(25)、profit-margin(25)、market-share(GAP)、customer-concentration(GAP)、brand-voice(GAP)

### 1.3 综合竞争力（competitiveness / E-30）

| 指标 key | 中文名 | group | metricId | 默认权重 | 算法源字段 | entanHelp Tab |
|----------|--------|-------|----------|---------|------------|---------------|
| `innov` | 创新能力 | 综合竞争力三域 | `M_ENT_INNOVATION_INDEX` | **40**（原 20） | `a1_score.py#DOMAIN_WEIGHTS.innov=0.40` | score |
| `operate` | 经营能力 | 综合竞争力三域 | `M_ENT_COMPETITIVENESS_SCORE` | **40**（原 20） | `a1_score.py#DOMAIN_WEIGHTS.operate=0.40` | score |
| `growth` | 成长能力 | 综合竞争力三域 | `M_ENT_COMPETITIVENESS_SCORE` | **20**（原 20） | `a1_score.py#DOMAIN_WEIGHTS.growth=0.20` | score |

- **算法权重真源**：`demo-algo-ent-analysis/entan/realdata/a1_score.py` → `DOMAIN_WEIGHTS = {"innov": 0.40, "operate": 0.40, "growth": 0.20}`
- 与 `entanHelp.ts` score Tab 公式 `S_total = 0.40*innov + 0.40*operate + 0.20*growth` 完全一致
- **旧 indicators 移除**：competitiveness-score(40)、competitiveness-rank(20)、shortboard-count(20)、innovation-index(20)→重映射为 innov(40)、organization-capability(GAP)

---

## 2. 修改内容

### 2.1 `enterpriseEvaluationModel.ts`
- **EVALUATION_MODES**：三模式 indicators 全部替换为算法维度对齐指标（技术力五维、商业力六维、综合竞争力三域），默认权重与 `settings.yaml` 及 `a1_score.py` 一致（×100 整数）
- **BUSINESS_INDUSTRY_PREVIEWS**：预览 key 和 weights 同步更新为新维度键
- **INDICATOR_EXPLANATIONS**：全部替换为算法维度对应的指标说明（14 新条目）

### 2.2 `enterpriseEvaluationResultModel.ts`
- **RESULT_DIMENSIONS**：新增 `business` 六维条目；`competitiveness` 三域从 {技术/市场/组织} 重映射为 {创新能力/经营能力/成长能力}
- **buildDimensionSeries**：类型签名增加 `'business'` 支持

### 2.3 默认权重验证
- `createDefaultEvaluationWeights()` 自动从 `EVALUATION_MODES` 提取，与算法默认一致
- 技术力：talent=20 / innovation=25 / transfer=20 / cooperation=15 / investment=20
- 商业力：market=22 / product=16 / brand=16 / cooperation=14 / chain_coverage=16 / chain_keynode=16
- 综合竞争力：innov=40 / operate=40 / growth=20

---

## 3. 范围证明

```
git diff --stat
 .../pages/enterprise/enterpriseEvaluationModel.ts  | 89 +++++++++++-----------
 .../enterprise/enterpriseEvaluationResultModel.ts  | 16 +++-
 2 files changed, 55 insertions(+), 50 deletions(-)
```

所有修改严格限制在 `src/app/pages/enterprise/` 下的 `enterpriseEvaluation*.ts` 文件，未修改检索、对比篮、画像、风险等其他模块。

---

## 4. 架构合规 7 条自检

| # | 规则 | 状态 | 说明 |
|---|------|------|------|
| 1 | 不改 Java | ✅ | 仅修改 demo-ui-topic TypeScript 文件 |
| 2 | 调用链 | ✅ | 本期仍为 demo Mock 算分，未引用 entan API |
| 3 | 图谱 NebulaGraph | ✅ | N/A |
| 4 | 可观测性 | ✅ | N/A（demo-ui-topic） |
| 5 | CI | ⏳ | push demo-ui-topic `origin/main` 后部署站可见；npm run build 未验证（无 node_modules） |
| 6 | commit 标注 | ✅ | 含 `[human:唐绍祖]` 与 `[agent:algorithm-agent]` |
| 7 | demo2 不 merge lumen | ✅ | 仅 demo-ui-topic 仓修改 |

---

## 5. Cost

| 字段 | 值 |
|------|-----|
| 投入人时 | 1.5 h |
| 仓 | `demo-ui-topic`（dev → origin/main） |
| 文件数 | 2 |
| diff 行数 | +55 / -50（纯 enterpriseEvaluation* 文件） |
