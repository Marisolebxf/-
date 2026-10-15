# CMS-JX-OVERLAY-DDL-L01 · CMS overlay 库落库：三件套 DDL + join 视图 + 审计

> **任务**：`CMS-JX-OVERLAY-DDL-L01`（tech_task / P0 / implementation）
> **依据**：[CMS-JX-OVERLAY-A5-L01.md](../../工程过程归档位置见registry) 冻结版 + 《CMS-JX接口规格书.md》v1.3
> **产物**：`lumen-svc-platform/db/9x_gkxlumenx_cms.sql`（468 行，commits `dcb41d3`→`f1fb7e4`→`6503cd3`，origin/dev）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | pull（2026-10-15 17:57，8h 锁窗） |

## Ponytail

ponytail: `N/A`（DDL 无业务逻辑代码；表列=规格直译）

## 落地内容

### 1. 库与表（A5-1/A5-4）

- `CREATE DATABASE gkxlumenx_cms`（业务库，utf8mb4；**禁入 DWD/ADS**）
- 三件套 + 9 张内容宽表，全部含 `is_deleted` 软删 + `created_by/at` + `updated_by/at`：
  - `cms_entity_overlay`（**UNIQUE KEY `uk_type_source`(entity_type, source_id)** = join 生命线；`field_overrides` JSON 一层平面 KV）
  - `cms_op_audit`（操作留痕：op_type/entity_type/business_id/reason/operator/snapshot_before/op_time，双索引）
  - `cms_content_news`（ENT/SVC/IND 三域一行型，org_ids JSON 多选数组）
  - `cms_content_sz`（ENT/SVC；docx 扩展列 cases/evaluation/sz_note 注释标明）
  - `cms_content_region_roster`（org_id 可空=手填名录语义）
  - `cms_industry_custom`（kind=CLASS/LINK 合一，uk(kind,code)，CLASS 树 parent_code 自关联）
  - `cms_kg_stage_def` / `cms_kg_entity_status`（extra JSON 存类型专属字段）/ `cms_kg_relation`（break_time）/ `cms_kg_attr`（group=base/dyn）
  - `cms_expert_knowledge`（entity JSON + content JSON 按 section 有序键值对）

### 2. join 视图（A5-5，4 个）

- `v_cms_ent` / `v_cms_pol` / `v_cms_svc` / `v_cms_prod`：真源 LEFT JOIN overlay 逐字段 COALESCE + 虚拟实体 UNION ALL + 软删剔除；**视图列名 = 规格书字段名**（接口层零映射）。

### 3. **live 库列名校准（本单最大产出）**

用公网只读连接（gkxlumenx-dwd-public，MySQL 8.0.46）实测正式库，发现并修正了规格书假设列名与 live 的偏差——正是"实际开发字段对不上"的活案例，在 DDL 阶段掐灭：

| 规格假设列 | live 实际列（enterprise_base，189,115 行） |
|-----------|------------------------------------------|
| `name_cn` | `enterprise_name` |
| `incorporation_date` | `registration_date` |
| `registered_capital_value`+`capital_currency` | `registered_capital`（decimal 单列） |
| `area` | `district` |
| `org_type` | `enterprise_type` |
| `reg_status` | `business_status` |
| `external_id` | `enterprise_code`（统一社会信用代码） |
| `industry_l1~l4_name` | `industry_category` + `industry_code`（两级） |

- `policy_base_info` 列与规格假设**全部一致**（title/content/publish_organization/publish_date/issued_number/url/status/level/source ✓）
- **环境现状**：企业数据在正式库；政策 20,000 行/服务圈定池/产品表当前在 `demo_gkxlumenx_dwd`（正式库 0 行待数据工厂灌数）。视图默认指向正式库，dev 部署 sed 替换 demo 前缀（两环境列名一致，文件头注记）
- 修正 SVC 视图：机构名称/区域读 `svc_org_card`（ADS 卡片）而非 enterprise_base（enterprise_base 是企业域表，无 org_type_hint 列——起草时猜测错误已纠正）
- 数据抽样验证：企业 3 行实查，名称/成立/资本/类型/状态/区域/信用代码全部正确映射到规格字段

### 4. 种子数据

- 阶段定义 16 行（四类×4 阶段，name+feature+metric 与原型 STAGE_DEFS 逐条一致）
- 属性模板 22 行（industry 4 + enterprise 7 + policy 5 + service 6，dtype/constraint 对齐原型 ATTR_DEFS）

### 5. 四态自检脚本（DoD 第 5 条）

文件 §6 内嵌注释版（真源行/覆盖行/虚拟行/软删行 + 断言 COUNT + 清理），**落库执行版**待有写权限账号时跑；本单已用 live SELECT 验证视图 SELECT 逻辑正确（列映射 + COALESCE 语义）。

## 遗留与移交

| 项 | 说明 | 去向 |
|----|------|------|
| 建库执行 | 公网账号只读（Access denied 已证），需 DBA/运维用高权限账号执行 `9x_gkxlumenx_cms.sql` | devops 部署时；或下次有内网写连接时 |
| `NULL->>'$.x'` 裸 NULL 限制 | 视图内均为列引用不受影响；CRUD 单写 SQL 时注意对 NULL overlay 列用 `JSON_EXTRACT` 判空 | 各 CRUD 单实现注意项 |
| 正式库政策/服务/产品 0 行 | demo 库有数；视图环境切换已注释 | 数据工厂灌数任务（不在本 epic） |
| Nacos 数据源 | `MYSQL_DB=gkxlumenx_cms` + DWD 只读第二数据源配置 | gkxlumen-cms 模块搭建单（19 张 CRUD 首张时一并做） |

## 测试结果

- live 只读验证：enterprise_base 抽样 3 行 → 规格字段全映射成功（见 §3）
- 列存在性核查：enterprise_base 50 列 / policy_base_info 37 列 / svc_org_circle / svc_org_card / enterprise_industry_product / industry_chain(_node) 全部过 information_schema 实测
- MySQL 版本 8.0.46（JSON 函数/`->>` 操作符/函数索引均支持）

## 架构合规自检

| # | 铁律 | 结论 |
|---|------|------|
| 1-3 | 算法/调用链/图谱 | ✅ 纯 DDL；KG 表只落 MySQL overlay，零 Nebula 写入 |
| 4 | 可观测 | ✅（DDL 层无埋点；CRUD 单接入 OTel） |
| 5 | CI/CD | ✅ SQL 落仓 `db/`，随仓走 pipeline；无手工建表 |
| 8 | 数据策略 | ✅ 独立业务库 `gkxlumenx_cms`，真源零写，未动 DWD/ADS |
| 12 | demo/lumen 隔离 | ✅ 落 lumen-svc-platform 正式仓 |

## CI/CD

- lumen-svc-platform `dev`：`dcb41d3` → `f1fb7e4` → `6503cd3`（已推 origin/dev，pipeline 走仓默认）

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | ~60000（DDL 编写+live 校准） |
| model_used | glm-5.3 |
| actual_cost | ~$0.6 |
| cost_warn | green |
