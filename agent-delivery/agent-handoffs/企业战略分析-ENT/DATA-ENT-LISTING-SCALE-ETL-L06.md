# Handoff：DATA-ENT-LISTING-SCALE-ETL-L06

- **task-id**：`DATA-ENT-LISTING-SCALE-ETL-L06`
- **执行**：`agent:data-agent`
- **监管**：`human:淮政玮`
- **认领**：`coordinator_dispatch` · `claimed_at=2026-07-29T20:25:00+08:00`
- **性质**：实现类（`cicd: required` · 主改 `lumen-etl-es-py`，辅改 `demo-svc-topic-py`）
- **状态建议**：`done`（coordinator 2026-07-29T21:45 条件验收关单）
- **日期**：2026-07-29

> **Coordinator 验收纪要（2026-07-29T21:45）**：Q059/Q058 派生 + ES 写入 + 单测证据齐；`lumen-etl-es-py@9214c81`、`demo-svc-topic-py@13a7073`。残差：org_id 双空间、规上工业门类过滤 — 记开放项不挡关单。前端接线归 `FE-ENT-DICT-WIRE-L05`（非 L04）。


---

## 1. 范围与实现（对照 DoD）

| DoD | 状态 | 证据 |
|-----|------|------|
| Q059 企业级 `listing_status` 派生（有在市→上市；全退市→退市；无证券→未上市）；与 meta 枚举一致 | ✅ | `etl/derive_listing_scale.py`；文案「上市」不加「已」 |
| Q058 `is_above_scale` 可被检索过滤；口径写清 | ✅ | ES boolean + topic-py `_FIELD_STRATEGY`；门槛 工业营收≥**2000 万元** |
| 样例校验 + 本 handoff | ✅ | ODS 10996 行派生分布 + 多值样例；unittest 9 passed |
| 不做前端 / 全量国标 / Java Facade | ✅ | 契约字段名无破坏性变更；**通知 JAVA/FE**：新增可筛字段 `is_above_scale`（boolean） |

**上游**：`DATA-ENT-DICT-IMPL-L02` done；Q058/Q059 🟢。

---

## 2. 落地层（检索可用）

| 层 | 说明 |
|----|------|
| **派生模块** | `lumen-etl-es-py/etl/derive_listing_scale.py` |
| **同步作业** | `etl/listing_scale.py` → `POST /internal/etl/listing-scale?mode=both` |
| **ES mapping** | `conf/es/gkx_enterprise_mappings.json`：`listing_status` keyword；**新增** `is_above_scale` boolean、`stock_types` keyword、`stock_securities` nested |
| **现网 put_mapping** | 作业启动时 `ensure_listing_scale_mapping()`（不重建索引） |
| **检索过滤** | `demo-svc-topic-py` `enterprise_search._FIELD_STRATEGY["is_above_scale"]`；列表 `_source` 含该字段；布尔值 `"true"/"1"` 可规范化 |

### 2.1 Q059 派生规则

源：`gkxlumenx_ods.dwd_org_base_info.stock_type` / `listed_status`（逗号多值、位置对齐）。

1. zip 拆证券明细；清洗空状态 / 去重；「已上市」归一为判定用「上市」
2. 企业级：`任一上市 → 上市`；`有证券且全退市 → 退市`；`无有效证券 → 未上市`
3. 多市场「上市,退市」→ **上市**（Q059 甲方确认）
4. `stock_types`：规范化板块列表（在市优先），**不**塞进上市状态枚举

### 2.2 Q058 规上口径

| 项 | 值 |
|----|-----|
| 字段 | `is_above_scale`（boolean，可与 `enterprise_scale` 四档叠加） |
| 门槛 | 工业营收 ≥ **2000 万元**（调查范围；对齐客户决策 Q058） |
| 现网源字段 | `gkxlumenx_dwd.enterprise_base.revenue_latest`（**万元**） |
| 备选 | ODS `operating_revenue`（元）/10000；现网年度财务表为空 |
| 开放 | **未做行业门类=工业过滤**（无可靠工业门类字段时先按营收门槛；handoff 标注） |

---

## 3. 样例校验（2026-07-29 · 10.50.11.76）

### 3.1 ODS 全量派生分布（write_es=false / true 一致）

| listing_status | 行数 |
|----------------|-----:|
| 未上市 | 10898 |
| 上市 | 79 |
| 退市 | 19 |
| **合计** | **10996** |

### 3.2 多值样例

| 企业 | stock_type 原串 | listed_status 原串 | 派生 |
|------|-----------------|-------------------|------|
| 开普云信息科技 | 上交所科创板A股,新三板 | 上市,退市 | **上市** |
| 北京首都在线 | 深交所创业板A股,新三板 | 上市,退市 | **上市** |
| 深圳市巅峰科技 | 新三板 | 退市 | **退市** |

### 3.3 ES 写入

| mode | indexed | errors |
|------|--------:|-------:|
| ods（upsert） | 10996 | 0 |
| dwd（现网 ORG* 120 文档补 `is_above_scale`/`listing_status`） | 120 | 0 |

> 注：现网 ES 原 120 条为 DWD mock `ORG*`；ODS 为 hash `org_id`。两边 **org_id 空间未对齐**，ODS 文档以 upsert 写入别名 `gkx_enterprise`；后续全量企业同步需统一主键。

### 3.4 单测

```text
# lumen-etl-es-py
python -m unittest tests.test_derive_listing_scale -v
→ 9 passed

# demo-svc-topic-py（Mock 过滤）
pytest tests/test_enterprise_search.py::test_query_tree_is_above_scale_filter \
  ::test_meta_enterprise_scales ::test_query_tree_and_basic \
  ::test_meta_filters_enhanced ::test_query_tree_operator_in -q
→ 5 passed
```

---

## 4. 产物清单

### lumen-etl-es-py（主）

| 文件 | 变更 |
|------|------|
| `etl/derive_listing_scale.py` | Q059/Q058 纯函数 |
| `etl/listing_scale.py` | ODS+DWD 同步作业 |
| `etl/modules/reg_info.py` + `etl/scripts.py` | 模块化 reg_info 改用 Q059「上市」文案 + 写入 `is_above_scale` |
| `app/main.py` | `POST /internal/etl/listing-scale` |
| `app/config.py` / `conf/settings.yaml` | `mysql.ods_db` |
| `conf/es/gkx_enterprise_mappings.json` | `is_above_scale` 等 |
| `tests/test_derive_listing_scale.py` | 9 用例 |
| `README.md` | 接口说明 |

### demo-svc-topic-py（辅 + L02 residual）

| 文件 | 变更 |
|------|------|
| `gkx_search_service/views/enterprise_search.py` | `is_above_scale` 过滤 + 列表字段 + 布尔规范化 |
| `gkx_common/mock.py` / `meta.py` / `enterprise_detail_basic.py` / API 文档 / tests | **含 L02 residual**（meta Q056–Q059 未提交部分一并整理） |

---

## 5. 通知 JAVA / FE（契约）

- **无改名**：`listing_status` 仍为 keyword；枚举值以 meta 为准：`上市`/`未上市`/`退市`（勿再用「已上市」「拟上市」筛）
- **新增筛选项**：`is_above_scale`（boolean；`eq`/`in`；可与 `enterprise_scale` 叠加）
- Java Facade **本单未改**；若需对外 REST 透传，跟 `API-ENT-DICT-JAVA-L05` / FE-L04

---

## 6. 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法/ETL 只在 Python | ✅ |
| 2 | 调用链 FE→Java→Python `/internal/*` | ✅ 新增 `/internal/etl/listing-scale`；检索仍 `/internal/gkx-search/*` |
| 3 | NebulaGraph | ✅ 不涉及 |
| 4 | 可观测性 | ✅ 既有服务；未改入口中间件 |
| 5 | CI/CD required | ⏳ push 后 Pipeline |
| 6 | demo 不 merge lumen | ✅ 双仓各自 push |
| 7 | 共享聚合 / Java 不写算法 | ✅ |
| 8 | 数据策略 | ✅ ODS 真源 + DWD 营收；ES 检索层 |
| 9 | Design.md | ✅ 无前端 |
| 10 | 数据血缘 D9 | ✅ 口径写入本 handoff §2.2 |
| 11 | 交互规范 D10 | ✅ 无 UI |

---

## 7. Cost 四字段

| 字段 | 值 |
|------|-----|
| `actual_tokens` | ~160000（估） |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | ~4.0（估 USD） |
| `cost_warn` | green |

---

## 9. Git 提交

| 仓 | 分支 | SHA | message |
|----|------|-----|---------|
| `lumen-etl-es-py` | `origin/dev` | `9214c8122d149e2045e56562d3cab7ab6bdbaebf` | feat(etl): Q059/Q058 listing_status 与 is_above_scale ODS→ES 派生 |
| `demo-svc-topic-py` | `origin/dev` | `13a70731716ef6a91a7be5bf5529e7555ddcf05d` | feat(search): L06 is_above_scale 检索过滤 + L02 residual |
| `gkx-orchestration` | `origin/dev` | `90eb0956e462f7c5f6c97289703c425efb7e69a7` | chore(handoff): DATA-ENT-LISTING-SCALE-ETL-L06 → review + cost |


1. **org_id 双空间**：ODS hash vs DWD `ORG*` 未对齐；全量检索统一主键待企业主数据贯通
2. **规上行业门类**：当前仅营收门槛，未限制「工业」门类（ODS 工业标识缺失）
3. **ODS 财务表空**：`dwd_org_annual_financial_info` / `stock_finance` 行数 0；规上暂用 DWD `revenue_latest`
4. **前端接线**：`FE-ENT-DICT-WIRE-L04`（规上开关 + 上市枚举文案）
5. **Convoy**：未改 `code_region` / `region_scope` 灌数（归 L03）
