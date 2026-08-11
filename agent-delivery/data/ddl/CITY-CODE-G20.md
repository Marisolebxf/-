# G20 / 运营城市码口径（2026-08-11）

> 真源任务：`PY-ENT-REGION-SCOPE-G20-COUNTRY-L01`（L05）  
> 配套 DDL：`gkxlumenx_dim_region_scope_g20_city_l05.sql`

## 分层

| 层级 | 字段 | 标准 | 例 | 查询用途 |
|------|------|------|----|----------|
| 国家 | `bind_country_code` / ES `country_code` | ISO 3166-1 **alpha-3** | `JPN` | 整国 OR |
| 海外城市 | `bind_city_code` / ES `city_code` | **UN/LOCODE** 五位紧凑（alpha-2+3，无连字符） | `JPTYO` | 城市叶 OR |
| 中国城市 | `bind_admin_code` / ES `region_id` | 民政部 6 位 | `110000` | 国内叶 OR |
| 中国城市镜像 | `bind_city_code` | 国内运营码 `CN-*`（与热门枝共用 `dim.city`） | `CN-1100` | 不进 ES 主筛；维表对齐 |

## 为何不用旧 `JP-TYO`

- 连字符运营码 ≈ LOCODE 但非标准书写，ETL/外部数据难对齐  
- 国家已定 alpha-3，城市再用私有 `XX-YYY` 两套方言  
- `CN-1100` 与国标 6 位混在同一 `bind_city_code` 语义不清

## 为何中国不改成 `CNBJS`

- 「全国热门」已绑 `CN-1100` 等；G20 下北京/上海/深圳应**共用**同一 `dim.city` 行  
- 国内过滤主路径永远是 `region_id` ← `bind_admin_code`，不必为国际码拆 PK

## 新加坡

- 旧 Mock 有 `g20-singapore`，但 **非 G20 2020 主权国** → `is_active=0`，不挂 `g20-c-*`

## 选码语义（产品已确认）

```
选 g20-c-jpn     → country_codes: ["JPN"]     # 整国，不是样例城市并集
选 g20-tokyo     → city_codes: ["JPTYO"]
选 g20-beijing   → region_ids: ["110000"]
选 hot-city/北京 → region_ids: ["110000"]     # 与 G20 中国城分枝，不合并名单
```

## 旧码兼容

- `dim.city` 中 `JP-TYO` 等历史行可保留，**region_scope 不再引用**  
- 新灌数 / ES `city_code` 只认 UN/LOCODE 五位  
- **禁止**在 L04/L05 之后重跑 `gkxlumenx_dim_region_scope_seed_l03.sql` §3（会把 `bind_city_code` 打回连字符旧码）
