# CHAIN · seeds 覆盖样例索引

```yaml
---
doc_id: CHAIN-SEEDS-INDEX
element: CHAIN
role: source
status: draft
version: "2026-08-13"
updated: 2026-08-13
---
```

> 少量样例，先闭环后性能。非第二套 DDL。数据文件 **S3** 落入本目录或脚本旁路 `out/`。

## 覆盖矩阵（骨架）

| 场景 ID | 场景 | 数据特点 | 主要触达表 | 状态 |
|---|---|---|---|---|
| SEED-CHAIN-01 | 单链完整树 | 多层级 `parent_code`；叶子有企业数 | `dwd_industry_chain_info` | 待灌 |
| SEED-CHAIN-02 | 节点挂企业 | 同一 `industry_link_code` 多 `credit_code` | `dwd_org_industry_tags` | 待灌 |
| SEED-CHAIN-03 | 企业×产品 | 一企多产品；含 `product_top5` 空/非空 | `dwd_org_industry_product_tags` | 待灌 |
| SEED-CHAIN-04 | 链上资讯 | 有/无 `publish_date`；长摘要 TEXT | `dwd_industry_chain_news_info` | 待灌 |
| SEED-CHAIN-05 | 跨表关联 | 同一 `industry_code` 贯穿四表 | 四表 | 待灌 |

## 灌数入口（预留）

| 项 | 说明 |
|---|---|
| ODS 建表 | `scripts/run_chain_ods.py`（当前主责 CREATE） |
| 样例 INSERT | S3 扩脚本或 SQL seed；禁止写正式 ODS |

## 开放

| ID | 说明 |
|---|---|
| OPEN-CHAIN-SEED-01 | 样例行业/企业是否用甲方脱敏清单 — 待确认后定具体值 |
