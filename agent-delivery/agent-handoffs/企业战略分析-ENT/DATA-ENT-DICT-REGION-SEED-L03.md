# Handoff：DATA-ENT-DICT-REGION-SEED-L03

- **task-id**：`DATA-ENT-DICT-REGION-SEED-L03`
- **执行**：`agent:data-agent`
- **监管**：`human:淮政玮`
- **认领**：`coordinator_dispatch` · `claimed_at=2026-07-29T20:25:00+08:00` · `in_progress→review`
- **性质**：数据灌数（`cicd: skip`；编排仓 SQL/脚本 + MySQL 现网）
- **日期**：2026-07-29
- **状态建议**：`done`（coordinator 2026-07-29T21:05 验收关单；补推产物）

> **Coordinator 验收纪要（2026-07-29T21:05）**：现网 code_region 3349 / 深圳区县 bind / Q056 Mock 扩种证据充分。执行侧曾漏 push 编排产物，由 coordinator 一并补提交。

---

## 1. 范围与实现（对照 DoD）

| DoD | 状态 | 证据 |
|-----|------|------|
| `gkxlumenx_dim.code_region` 灌入可用省→市→区县树（非仅 11 行样例） | ✅ | 现网 **3349** 行；level1=32 / level2=342 / level3=2975 |
| `region_scope.bind_admin_code` / `region_scope_member` 与国标码对齐（含深圳区县） | ✅ | bind 全命中；深圳 9 区码齐全；member 15 行均存在于 code_region |
| G20 / 热门科创城市 Mock 扩种（Q056） | ✅ | hot-city **19**；global-all G20 **30**；`city` **46** |
| handoff + 架构自检 + cost 四字段 | ✅ | 本文件 |
| 不做前端 / Java / meta 契约 / listing·规上 ETL | ✅ | 未改业务仓代码 |

**上游**：`DATA-ENT-DICT-IMPL-L02` done；设计 `ENT-DICT-CATALOG-L01`；决策 Q056🟢。

---

## 2. 现网执行结果（2026-07-29 · MySQL `192.168.88.43`）

| 对象 | 灌数前 | 灌数后 |
|------|--------|--------|
| `gkxlumenx_dim.code_region` | 11（样例：中国+10 城，无区县） | **3349** |
| `gkxlumenx_dim.region_scope` | 47 | **69** |
| `gkxlumenx_dim.region_scope_member` | 15 | **15**（法定边界未改成员集合；码均可 join） |
| `gkxlumenx_dim.city` | 25 | **46** |

### 2.1 code_region 层级

| level | 含义 | 行数 |
|-------|------|------|
| 1 | 中国根 `100000` + 31 省/直辖市/自治区 | 32 |
| 2 | 地级市（直辖市「市辖区」展示为省级名） | 342 |
| 3 | 区县 | 2975 |

树结构：省/中国 `parent='0'` → 市 → 区县。与 `/meta/regions` Cascader（空 parent → 顶级）兼容：顶级含「中国」+ 各省。

### 2.2 深圳区县（`parent=440300`）

| code | name |
|------|------|
| 440303 | 罗湖区 |
| 440304 | 福田区 |
| 440305 | 南山区 |
| 440306 | 宝安区 |
| 440307 | 龙岗区 |
| 440308 | 盐田区 |
| 440309 | 龙华区 |
| 440310 | 坪山区 |
| 440311 | 光明区 |

`region_scope` 对应 district 节点 bind 已与上表对齐；`dapeng`（大鹏新区）仍无民政部县级码，`bind_admin_code=NULL`。

### 2.3 Q056 Mock 扩种

- **热门科创城市**：原 9 城 + 南京补 bind；新增西安/合肥/长沙/青岛/厦门/天津/重庆/无锡/宁波/东莞 → **19**
- **G20**：原 18 + 大阪/芝加哥/洛杉矶/米兰/罗马/莫斯科/墨西哥城/约翰内斯堡/布宜诺斯艾利斯/伊斯坦布尔/雅加达/墨尔本 → **30**
- **dim.city**：同步扩种至 **46**（海外城市 `admin_code` 为空，靠 `bind_city_code`）

---

## 3. 产物清单

| 路径 | 说明 |
|------|------|
| `agent-delivery/data/seeds/admin-divisions/{provinces,cities,areas}.json` | 国标源快照（modood/Administrative-divisions-of-China） |
| `agent-delivery/data/scripts/seed_code_region_l03.py` | 灌数 + bind 校正 + Mock 扩种 + 校验脚本 |
| `agent-delivery/data/ddl/gkxlumenx_dim_code_region_seed_l03.sql` | code_region 全量 DELETE+INSERT 产物 |
| `agent-delivery/data/ddl/gkxlumenx_dim_region_scope_seed_l03.sql` | region_scope/city L03 补丁 SQL |
| `agent-delivery/data/ddl/gkxlumenx_dim_code_region.sql` | 表结构 DDL（未改契约） |
| `agent-delivery/data/ddl/gkxlumenx_dim_region_scope.sql` | L02 建表+Wave0 种子（保留；扩种见 L03 补丁） |

**未改**：`demo-svc-topic-py`（含 `meta.py`）、listing/规上 ETL、Java、前端。

---

## 4. 校验脚本与结果

```text
# Windows PowerShell 示例（密码勿入库；见 algo-mysql-connection-info.md）
$env:INNOV_MYSQL_PASSWORD = "<见连接真源>"
python agent-delivery/data/scripts/seed_code_region_l03.py
→ built rows=3349 skipped_area_dup=3
→ inserted code_region=3349
→ VALIDATION
   code_region_total: 3349
   by_level: {1:32, 2:342, 3:2975}
   orphan_parents: 0
   shenzhen_codes_ok: True
   bind_miss: ()
   member_miss: ()
   hot_city_count: 19
   g20_count: 30
   city_total: 46
→ PASS
```

抽检 SQL（可复跑）：

```sql
SELECT COUNT(*) FROM gkxlumenx_dim.code_region;                 -- 3349
SELECT level, COUNT(*) FROM gkxlumenx_dim.code_region GROUP BY level;
SELECT code,name FROM gkxlumenx_dim.code_region WHERE parent='440300' ORDER BY code;
SELECT COUNT(*) FROM gkxlumenx_dim.region_scope rs
  LEFT JOIN gkxlumenx_dim.code_region cr ON cr.code=rs.bind_admin_code
  WHERE rs.bind_admin_code IS NOT NULL AND cr.code IS NULL;     -- 0
SELECT COUNT(*) FROM gkxlumenx_dim.region_scope_member m
  LEFT JOIN gkxlumenx_dim.code_region cr ON cr.code=m.admin_code
  WHERE cr.code IS NULL;                                         -- 0
```

---

## 5. 偏离说明

1. **东莞/中山等无县级单元**：源数据区县码与市码相同（3 条），跳过插入避免 PK 冲突；市节点仍可筛选。
2. **港/澳/台**：本波源为大陆 31 省区划，未含 71/81/82；大湾区 member 仍为内地九市初始化（同 L02）。
3. **顶级含「中国」**：`100000` 与各省同为 `parent='0'`，供 `national`/`china-all` bind；Cascader 顶级会多一个「中国」节点（可前端隐藏，本单不改 FE）。
4. **大鹏新区**：非标准县级码，保持无 bind（开放项）。

---

## 6. 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ 本单无算法 |
| 2 | 调用链 FE→Java→Python `/internal/*` | ✅ 未改接口层 |
| 3 | NebulaGraph | ✅ 不涉及 |
| 4 | 可观测性 | ✅ 不涉及 |
| 5 | CI/CD | ✅ `cicd: skip`（编排 SQL） |
| 6 | demo 不 merge lumen | ✅ 仅编排仓 |
| 7 | 共享聚合 / Java 不写算法 | ✅ |
| 8 | 数据策略 ADS/码表 | ✅ 码表在 `gkxlumenx_dim`；`region_scope` 与 `code_region` **分表** |
| 9 | Design.md | ✅ 无前端 |
| 10 | 数据血缘 D9 | ✅ 字典码表灌数；指标卡不涉及 |
| 11 | 交互规范 D10 | ✅ 无 UI |

---

## 7. Cost 四字段（回填 registry）

| 字段 | 值 |
|------|-----|
| `actual_tokens` | ~120000（估） |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | ~3.0（估 USD） |
| `cost_warn` | green |

---

## 8. 开放项

1. 大鹏新区过滤策略（运营确认是否映射宝安/盐田或独立虚拟码）。
2. Cascader 是否隐藏顶级「中国」——交 FE-L05。
3. 港/澳编码纳入大湾区 member——运营可改 `region_scope_member`。
4. 国标源年度更新：重跑 `seed_code_region_l03.py`（先更新 `seeds/admin-divisions/*.json`）。
