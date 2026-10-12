# 短板指标数（M_ENT_SHORTBOARD_COUNT）

> 口径真源：算法 2026-09（同业=同链，空值不判，L3 跟 SCORE）→ `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：挂 `M_ENT_COMPETITIVENESS_SCORE` 的 **L3 实际值 + 同链同年均值**，不用总分。  
> 能算。只缺目标表。SCORE 未出数是上游。Q014 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（标明，不改上游叶）

| 顺序 | 指标 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_COMPETITIVENESS_SCORE`（MODEL，本波不算） | **同一套 L3 实际值** + 同链同年均值。不是 `score` 总分 |
| 2 | 本条 | 数有几条 L3 相对同业更差 |

不改 SCORE 叶。Q014 仍 🟡；L3 清单暂跟 SCORE 现稿，权重闭合后若增删 L3，本条跟着变。

## 元数据

- **指标ID**：`M_ENT_SHORTBOARD_COUNT`
- **指标名称**：短板指标数
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：综合竞争力评估
- **更新频率**：年（随 SCORE 批次）
- **对齐状态**：D1 aligned；同业=同链；能算；只缺目标表
- **是否在数据库**：无短板结果表；SCORE 落表待建
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q014

## 口径定义

**每个企业一条**：综合竞争力指标体系里，表现为短板的 L3 个数。

```
COUNT(L3)
WHERE 该 L3 有值
  AND 同链同年均值有值
  AND 该企该 L3 相对同链更差
```

相对更差：

- 资产负债率：**高于**同链同年均值（负债差）
- 其余 L3：**低于**同链同年均值

空值 / 均值空：**不判**短板（不计入分子，也不当「低于」）。

L3 集合 = SCORE 四维现稿（9 条）：资产总额、从业人员、营收利润率、资产负债率、总资产周转率、本科及以上占比、研发人员占比、市占率、销售收入。

- **禁止**用 `score_total` / 综合分一个数去跟均值比。
- **禁止**另开一套短板指标清单。
- 只国内。同业键=`chain_code`+年，不另按国标行业/规模。

8 件套只留这条 COUNT。下面实现不得改口径。

## 两点分开（强制）

### ① 本条口径

L3 值 + 同链均值在 → 按上式 COUNT。能算。

### ② 依赖评分出不出（另一回事）

SCORE MODEL 本波不算；L3 与同业均值尚未落表。人力/学历/市占等原料空，是 SCORE 叶的事。  
现网没有短板列可抄。demo `enterprise_score` **不当接通**。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | SCORE 出数里的 L3 + 同业均值（随 `ads_ent_competitiveness_score` 或 SCORE 明细） | **上游未建** |
| 目标 | `enterprise_shortboard` 建议名：`org_id + data_year + shortboard_count`（可加 bitset/JSON 列记下是哪几条，本波不强制） | **缺口：无此表** |

源 ≠ 目标。禁止把财务年报当目标。GDF 暂缓。

## 分场景 / 千万级（不进 8 件套）

生产：年批次在 SCORE 出数之后，按链算各 L3 均值，再逐企 COUNT 写入目标表。查询带 `org_id`（+年）。  
禁止请求路径对千万企 × 9 指标现算均值。demo 可扫小表对口径，不算接通。

**计算公式文件**：`M_ENT_SHORTBOARD_COUNT.md`

## 源表字段

二次 STAT：

```
ads_ent_competitiveness_score <- metric: M_ENT_COMPETITIVENESS_SCORE
```

用 L3 + 同业均值，不用总分。左端随 SCORE 落表；不写 `gkx.dwd_*` 当 FROM。

来源系统：国内机构要素库（SCORE 原料侧）。

## 现网探针（2026-08-28；不进 8 件套）

- 无 `enterprise_shortboard`。SCORE 落表未建。
- `enterprise_score` 120 行总分 mock，禁止当短板。
- ODS 年报人力/学历等空：记在 SCORE 叶，不写成本条口径缺口。

## 待建 / 缺口

1. **无独立目标表**（公式只标这一条）。
2. SCORE L3 + 同链均值未出：上游，不进无法执行。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

bid `§1.1.1.2.4.2.3.10`；STAT。与排名同类二次处理。不改 MODEL 叶。

---
*2026-09-07 COVER-STAT-L01：0.3.1 同业=同链；能算；只缺目标表；D1 aligned*
