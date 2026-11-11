# 2020 专利地图 2025 Demo 补数

## 写入范围

- 数据库：`demo_gkxlumenx_dwd`
- 表：`enterprise_patent_history`
- 年份：仅 `2025`
- 行数：202
- 选取规则：2024 年每个大湾区城市按 `patent_apply_count` 取 Top 50 企业
- 数值规则：2024 年值按固定比例缩放，确定性、可重复
- 不改表结构，不新增表/列，不写久新供应方库

## 批次

```text
mock_patent_geo_2025_20261111
```

行级 `org_id` 清单和值见 `seed-rows-2025.json`。

## 执行

```bash
GKX_PY_APP=<GKX_ROOT>/repos/lumen-topic-py \
  python3 seed_patent_geo_2025.py
```

脚本使用 `ON DUPLICATE KEY UPDATE`，可幂等重跑。

## 清理

```bash
GKX_PY_APP=<GKX_ROOT>/repos/lumen-topic-py \
  python3 cleanup_patent_geo_2025.py
```

清理只删除 manifest 中列出的 `org_id` 在 `data_year=2025` 的记录。
