# {域中文名} — 给三方供应方的问题清单

```yaml
---
doc_id: {DOMAIN}-SUPPLIER-QUESTIONS
element: {DOMAIN}
role: source
status: draft
version: "YYYY-MM-DD"
updated: YYYY-MM-DD
owner: human:淮政玮
audience: 三方供应方（书面回复） / PM 转发
---
```

> 本文件放在 `question/` 根目录作空壳。复制到 `{维度目录}/{DOMAIN}-SUPPLIER-QUESTIONS.md`（**文件名不加日期**）后，下列相对路径生效。  
> 方法见 [../README.md](../README.md)。只问入站 `dwd_*` 表.列与主键。不问 `related_entities`、不问项目 DWD/ADS、不问甲方 Q-*、不请对方替我们算指标。  
> 供应方约束：[`../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)。  
> sidecar：缺口概要 upsert [`../source-gap-index.yaml`](../source-gap-index.yaml)（`summary`≤80 字）。

请对方**逐条**按文末模板回复。发给对方时以「现行待回复」为主；分析日志可一并转发以便对日期。

---

# 现行待回复（滚动）

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 |
|------|--------|-----------|--------|------------------|------------|
| | P0 / P1 / P2 | `dwd_*.col` | （draft 标「随口径修订」） | `M_…` | YYYY-MM-DD |

<!-- 一行一列。多指标卡同一列 → 同一 Q-id，metric_id 并列。MIXED 本波不进本表。 -->

---

# 分析日志（新的在上）

## YYYY-MM-DD

- 本批算法类型：STAT n / COMPUTE n / GRAPH n / MODEL n / third_party n / UNKNOWN n
- 本批指标：
  - （`metric_id` 列表或附件路径；禁止超本叶 /goal 清单）
- D1 快照：aligned n / draft n（本批；MCP 只读）
- 入站抽样：库 / 表 / 过滤（默认 `is_deleted=0`）/ 行数
- 问题表：

| Q-id | 入站表.列 | 现象（空值率、样例） | 请对方确认 |
|------|-----------|----------------------|------------|
| | `dwd_*.col` | | |

- 声明：草案口径标「随口径修订」
- sidecar：本批 upsert 的 metric_id（无则写「无，仅日志」）

---

## 请对方每条按此格式回

| 项 | 内容 |
|----|------|
| 问题编号 | Q-id |
| 现状 | 字段 / 表 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：对方主键 + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |
