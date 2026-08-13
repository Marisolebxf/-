# 管道 · DWD → Elasticsearch

> S2 回填

## 意图

`enterprise_base` / `enterprise_forg_*` 等 DWD → ES。检索走别名 **`gkx_enterprise`**（国内 + 国外 fan-out）。

## 双索引口径（与 Mapping 明细 §1.4 对齐）

```text
别名 gkx_enterprise
  ├── gkx_enterprise_v1          (国内，IK)
  └── gkx_enterprise_global_v1   (国外，standard)
```

- mapping 字段结构一致，分词器不同；查询走别名。  
- 国内写 `country_code=CHN` + `region_id`；国外填各国代码。  
- `name_cn` / `name_en` 语义见 Mapping 明细 §1.5。

## 脚本指针（仓内真实入口）

| 项 | 路径 |
|---|---|
| 仓 | `${GKX_ROOT}/repos/lumen-etl-es-py` |
| README | `lumen-etl-es-py/README.md` |
| CLI | `scripts/run_etl.py` · `scripts/create_enterprise_index.py` |
| 模块示例 | `etl/modules/reg_info.py`（从 `enterprise_base` 抽字段） |
| API | `app/main.py` → `/internal/etl/*` |
| 设计 | `data-design/企业/企业搜索-ES索引设计.md` · `企业搜索-ES更新机制.md` |
| Mapping / 国内外口径 | `data-design/企业/企业域-ETL-Mapping明细-源表到DWD.md` §1.4–§1.5 |
| storage 契约 | [`../stores/elasticsearch/`](../stores/elasticsearch/) |

## 调度

批：DWD 门禁通过后触发；失败不发布半成品索引。具体 cron → OPEN-ENT-FLOW-01。
