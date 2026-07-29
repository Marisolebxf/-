# 企业检索/筛选 — 字典与码表盘点 + 落库建议（DATA-ENT-DICT-CATALOG-L01）

> **任务**：`DATA-ENT-DICT-CATALOG-L01`  
> **执行**：`agent:data-agent` · **监管**：`human:淮政玮`  
> **日期**：2026-07-29  
> **范围**：盘点 + DDL 设计 + 种子策略；**不做**前端改码 / Java / 全量国标灌数  
> **实测库**：MySQL `192.168.88.43`（`gkxlumenx_dim` / `gkxlumenx_dwd`）

---

## 1. 总览结论

| 类别 | 结论 |
|------|------|
| **结果区地域级联**（全球/全国/区域/热门城市/深圳区县） | **必须落表**：`gkxlumenx_dim.region_scope` + `region_scope_member` |
| **高级筛选省市区** | **已有表**：`gkxlumenx_dim.code_region`（仅 11 行样例）→ 全量灌数另开 L02 |
| **innov 行政区划** | **已有表**：`gkxlumenx_dim.admin_division`（11 行）→ 与 code_region **并存、勿混读** |
| **全球城市** | **已有表**：`gkxlumenx_dim.city`（14 行）→ 可被热门城市 `bind_city_code` 引用，**不替代**运营级联 |
| **标签** | **已有表但契约漂移**：`gkxlumenx_dwd.tag_dict`（7 行；缺 `tag_level`/`is_active`/`sort_order`）→ ALTER 对齐 + 补种子 |
| **公司类型 / 规模 / 上市 / 经营状态** | **保持 Python 固定枚举**；口径已由 Q057–Q059 确认（见 §5 / §7） |
| **产业级联 / 风险类型等** | 本单记录；产业走 ES facets/产业链 follow-up；`risk_type_dict` 已建空表 |

---

## 2. 字典/码表清单

| dict_id | 中文名 | 消费位置 | 现状 | 建议落库 | 优先级 | 备注 |
|---------|--------|----------|------|----------|--------|------|
| ENT-DICT-REGION-SCOPE | 结果区运营地域级联 | `RegionSelect` / `ResultToolbar`；源 `regionOptions.ts` | **前端写死** | **新建** `gkxlumenx_dim.region_scope` + `region_scope_member` | **P0** | **Q056🟢**：法定初始化+运营可改；全球=G20；热门需 Mock |
| ENT-DICT-CODE-REGION | 省市区国标树 | Python `/internal/.../meta/regions`；高筛 Cascader | **已有表** 11 行样例 | **保持** `gkxlumenx_dim.code_region` | P0（灌数 L02） | 非运营「区域」字典 |
| ENT-DICT-ADMIN-DIV | innov 行政区划维 | innov `/dict/regions`；GIS/边界 | **已有表** 11 行 | **保持** `gkxlumenx_dim.admin_division` | P1 | 企业检索勿直读 |
| ENT-DICT-CITY | 全球城市维 | innov；可被运营热门/G20 绑定 | **已有表** 14 行 | **保持** `gkxlumenx_dim.city` | P2 | G20 Mock 扩种 |
| ENT-DICT-TAG | 资质/荣誉标签 | `/meta/tags`；高筛 `tags_flat` | **已有表** 7 行；schema≠meta.py | **对齐** `gkxlumenx_dwd.tag_dict` | **P0** | **Q057🟢**：与工商类型分字段 |
| ENT-DICT-COMPANY-TYPE | 工商注册类型 | `/meta/company-types` | **Python 固定 9 项** | **保持固定枚举** | P1 | **Q057🟢**：仅工商；勿混标签 |
| ENT-DICT-SCALE | 企业规模 | `/meta/enterprise-scales` | **Python 曾 5 项互斥** | **固定枚举改四档** + `is_above_scale` | P1 | **Q058🟢**：规上可叠加 |
| ENT-DICT-LISTING | 上市状态 | `/meta/filters.listing_statuses` | 文案漂移；ODS 为多值串 | **固定枚举**：上市/未上市/退市 | P1 | **Q059🟢**：ETL 派生；不含拟上市 |
| ENT-DICT-OPERATING | 经营状态 | `/meta/filters.operating_statuses`；FE mock | **Python 固定** 在营/注销/迁出/吊销 | **保持固定枚举** | P2 | 闭合稳定，无需落表 |
| ENT-DICT-RISK-TYPE | 风险类型 | 风险筛选 / 画像 | **已有表空** `gkxlumenx_dwd.risk_type_dict` | **保持表**；灌数另开 | P2 | 非检索主路径 |
| ENT-DICT-INDUSTRY | 所属产业级联 | FE `filterFieldSchema.INDUSTRY_CASCADE` | **前端写死**；亦可被 `/meta/filters.industries` 覆盖 | **不新建 DIM**；优先 ES facets / 产业链字典 | P1 | follow-up 与 chain 对齐 |
| ENT-DICT-SUPPLY-ROLE 等 | 供应链角色/招引状态… | FE 字段库写死 | 前端写死 | Wave0 **保持前端/固定枚举** | P3 | 算法口径未定 |

### 2.1 接口对照（现状）

| API（Python） | 数据源现状 |
|---------------|------------|
| `POST .../meta/regions` | `gkxlumenx_dim.code_region` |
| `POST .../meta/company-types` | 内存 `_COMPANY_TYPES` |
| `POST .../meta/enterprise-scales` | 内存 `_ENTERPRISE_SCALES` |
| `POST .../meta/tags` | 设计意图 `dwd.tag_dict`；SQL 写 `dwd_tag_dict` 且期望列与现网不一致 |
| `POST .../meta/filters` | ES terms + 固定 listing/operating |
| （建议新增）`.../meta/region-scopes` | → `region_scope` 树（L03） |

---

## 3. 边界说明（互不混表）

```text
┌─────────────────────────────────────────────────────────────┐
│ gkxlumenx_dim.region_scope (+ member)                       │
│ 运营 UI 级联：全球/全国/区域包/热门城市/深圳区县 slug        │
│ 可选 bind_admin_code / bind_city_code 引用下方维表           │
└───────────────┬─────────────────────────────┬───────────────┘
                │ bind（可选）                 │ bind（可选）
                ▼                             ▼
┌───────────────────────────┐   ┌─────────────────────────────┐
│ code_region               │   │ city                        │
│ 国标省→市→区县树          │   │ 全球城市（含海外）          │
│ 企业高筛 /meta/regions    │   │ innov + 热门城绑定          │
└─────────────┬─────────────┘   └─────────────────────────────┘
              │ 同源样例/未来全量
              ▼
┌───────────────────────────┐
│ admin_division            │
│ innov 契约 + boundary_geo │
│ 企业专题检索默认不读      │
└───────────────────────────┘

┌───────────────────────────┐   ┌─────────────────────────────┐
│ dwd.tag_dict              │   │ Python 固定枚举             │
│ 资质/荣誉/规模标签 code   │   │ company_type / scale /      │
│ ≠ 工商注册类型            │   │ listing / operating         │
└───────────────────────────┘   └─────────────────────────────┘
```

| 表 | 语义 | 谁读 | 禁止 |
|----|------|------|------|
| `region_scope` | 运营地域导航 | 结果区工具栏 | 塞入国标全量树 |
| `code_region` | 国标行政区划树 | 高筛省市区 | 塞「京津冀/大湾区」运营包为一级节点 |
| `admin_division` | innov 区划+边界 | innov GIS | 企业 `/meta/regions` 直读 |
| `city` | 全球城市点 | 对标/海外 | 替代国内区县树 |
| `tag_dict` | 标签 code→中文 | `/meta/tags` | 与 `company_type` 工商类型混枚举 |
| 固定枚举 | 闭合状态集 | meta company-types/scales/filters | 已确认口径见 Q057–Q059；勿与 tag_dict 混表 |

---

## 4. 新建/对齐 DDL

| 文件 | 内容 |
|------|------|
| `agent-delivery/data/ddl/gkxlumenx_dim_region_scope.sql` | **新建** `region_scope` + `region_scope_member` + Wave0 种子 |
| `agent-delivery/data/ddl/gkxlumenx_dwd_tag_dict_align.sql` | **ALTER 对齐** + 补种子（本单不强制执行） |
| `agent-delivery/data/ddl/gkxlumenx_dim_code_region.sql` | 已有（不改） |

### 4.1 `region_scope` 字段语义

| 字段 | 语义 |
|------|------|
| `scope_code` | PK；前端 value（`global`/`jjj`/`nanshan`…） |
| `parent_code` | 父子树；顶级 `''` |
| `node_kind` | `level` \| `scope` \| `district` |
| `level` | 1/2/3 |
| `bind_admin_code` | 过滤企业时映射到 `code_region`（可空） |
| `bind_city_code` | 映射 `dim.city`（可空） |
| `region_scope_member` | 复合区域一对多行政区划成员 |

### 4.2 种子策略

| 对象 | 本单 | Follow-up（口径已确认） |
|------|------|-------------------------|
| `region_scope` Wave0 | SQL 内 INSERT（对齐 `regionOptions.ts`） | 运营可维护；热门城市补 Mock（Q056） |
| `region_scope_member` | Wave0 省/市包种子 | **按法定边界初始化**后运营可改（Q056）；安徽是否入长三角以法定清单为准 |
| `global-all` / G20 | 占位 remark | **G20 国家主要科创城市** Mock → `dim.city` + member/bind（L02/L03） |
| `code_region` 全量国标 | **不做** | **DATA-ENT-DICT-REGION-SEED-L02** |
| `tag_dict` 补种 | ALTER 文件内 INSERT | L03 执行 + Python 改 SQL |
| 规模/上市固定枚举 | 仍在 `meta.py`（待改） | L03：四档+`is_above_scale`；上市=`上市/未上市/退市` |

---

## 5. 保持固定枚举 vs 必须落表（口径已确认 · Q056–Q059 🟢）

| 项 | 处置 |
|----|------|
| 经营状态 | **固定枚举**（不变） |
| 上市状态 | **固定枚举**：`上市` / `未上市` / `退市`；UI 同文案；不含拟上市；多市场有在市→企业级「上市」（**Q059🟢**） |
| 企业规模 | **固定枚举四档**大中小微 + **`is_above_scale` 可叠加**（**Q058🟢**；对齐国标两套体系） |
| 企业类型（工商） | **固定枚举**；与资质标签**分字段**（**Q057🟢**） |
| 资质标签 | **`tag_dict`**；勿与工商类型混枚举 |
| 结果区地域级联 | **必须落表** `region_scope`；区域法定初始化+运营可改；全球=G20；热门运营+Mock（**Q056🟢**） |
| 省市区 | **已落表** `code_region`；全量灌数另开 |
| 标签 | **已落表需对齐** `tag_dict` |

### 5.1 上市状态 ODS 派生（Q059）

源：`dwd_org_base_info.stock_type` / `listed_status` 为逗号多值且位置对齐。

1. ETL 按逗号 zip 拆成证券明细行（清洗重复/空状态）  
2. 企业级 `listing_status`：有任一「上市」→`上市`；仅有证券且全退市→`退市`；无有效证券→`未上市`  
3. 板块筛选用规范化后的 `stock_type`，不塞进上市状态枚举  

---

## 6. Follow-up 任务建议（只建议 ID，不改 registry 状态机）

| 建议 ID | 内容 | Agent |
|---------|------|-------|
| `DATA-ENT-DICT-REGION-SEED-L02` | `code_region` 全量国标；`region_scope_member` 法定边界种子；G20/热门 Mock；校正深圳区县 bind | data-agent |
| `DATA-ENT-DICT-META-API-L03` | 建表执行 + `/meta/region-scopes`；修 `tag_dict`；规模四档+`is_above_scale`；listing=`上市/未上市/退市` | algorithm-agent / topic-py |
| `FE-ENT-DICT-WIRE-L04` | `RegionSelect` 接 meta；工商/资质双字段；规模与上市 UI 对齐 Q057–Q059 | frontend-agent |
| `API-ENT-DICT-JAVA-L05` | Java 透传 `/search/meta/region-scopes`（若需） | api-agent |

---

## 7. 客户决策清单

**Q056–Q059 已全部 🟢**（2026-07-29 `human:淮政玮` 确认）。详见 `客户决策清单跟踪表.md` §2.z。关联开放：Q010（类型判定细则）、Q049（E-35 规模展示与本口径对齐）。
