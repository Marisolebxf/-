# acceptance-catalog

本目录存放从 **`2-概要设计/2-1需求分析`** 功能点 CSV 导出的验收清单。

**范围优先级**：范围真源为 `../bid-reference/*.md`（第一），本目录功能点台账为澄清/验收清单（第二），冲突以 bid-reference MD 为准（见 `../scope-baseline.yaml#precedence`）。**不读取** 招标 PDF。

**范围基线 ≠ 本目录条目数**：本目录是**明细功能点索引**（共 221 条：展示 30 + 专题 191）；工作范围基线以 `../scope-baseline.yaml` 的 **58 个 MD 叶子**（展示 30 + 专题 13 + 算法 15）+ ±10% 为准。专题明细条目回溯到 MD「战略分析 / 算法库」章节，**不单独计入** ±10% 基线。

## 生成方式

```bash
cd E:\gkx_src\agent-delivery\scripts
python extract_feature_catalog.py
```

## 产出文件

| 文件 | 内容 |
|------|------|
| `catalog-index.yaml` | 总条目数、tier 统计 |
| `catalog-display-7modules.yaml` | 展示系统 7 模块（DS-xx） |
| `catalog-topic-*.yaml` | 产业链/企业/机构/政策专题功能点 |

## 每条记录字段

```yaml
- id: DS-04
  source: req-analysis-display
  module: 科技发展态势
  title: 全球创新监测
  tier: FULL          # FULL | INTEG | DEMO | TBD
  route: /innov
  task_id: E-INNOV-M1-L08
  demo_id: null
```

## 验收覆盖率

功能点台账范围内：`has_route / entries_total = 100%` 为合规底线。

## 已废弃

- `catalog-service-cluster.yaml` / `catalog-cognitive-brain.yaml`（PDF 提取，不再使用）
- `scripts/extract_acceptance_catalog.py`
