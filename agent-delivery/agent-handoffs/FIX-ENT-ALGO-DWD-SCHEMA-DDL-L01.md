# FIX-ENT-ALGO-DWD-SCHEMA-DDL-L01 Handoff

## 1. 任务与监管

- 任务：企业算法仓 `scripts/mysql/schema_mysql.sql` 风险表 DDL 与 DWD v3.0/v3.1 契约对齐。
- 执行：algorithm-agent。
- 认领/监管：human:唐绍祖。
- ponytail: full。

## 2. 范围与实现

### 2.1 修改文件

- `repos/demo-algo-ent-analysis/scripts/mysql/schema_mysql.sql`
  - 替换第 549-588 行（旧简化风险 DDL）为 DWD v3.0/v3.1 正式结构。
  - 涉及 1 张汇总表 + 18 张风险主表 + 6 张 party 表 = 25 张表。

- `repos/demo-algo-ent-analysis/scripts/validate_risk_schema.py`（新增）
  - 可重复执行的结构校验脚本，验证 schema_mysql.sql 中风险表与正式设计一致。

### 2.2 逐表差异摘要

| 表名 | 旧结构问题 | v3.0/v3.1 目标 |
|---|---|---|
| `enterprise_risk_summary` | org_id 无 collation；缺索引 | org_id 加 utf8mb4_general_ci；加 idx_risk_summary_type + idx_risk_summary_org |
| `risk_judicial_case` | 无 case_id/is_history；无唯一键 | 加 case_id + is_history + uk_risk_judicial_case_id |
| `risk_dishonest` | 无 dishonest_id/is_history | 加 dishonest_id + is_history + uk_risk_dishonest_id |
| `risk_executed` | 无 case_id/is_history/exec_person_id | 加 exec_person_id + is_history + uk_risk_executed(org_id,case_no,exec_person_id) |
| `risk_limit_high` | 无 case_id/is_history | 加 case_id + is_history + uk_risk_limit_high_case |
| `risk_equity_freeze` | 无 case_id/is_history | 加 case_id + is_history + uk_risk_equity_freeze_case |
| `risk_equity_pledge` | 无 case_id/is_history/reg_no | 加 case_id + is_history + uk_risk_equity_pledge_case |
| `risk_zhongben` | 无 is_history；org_id 无 collation | 加 is_history + uk_risk_zhongben(org_id,case_no) |
| `risk_chattel_mortgage` | 无 is_history；reg_no 类型宽 | 加 is_history + guarantee_scope TEXT + uk_risk_chattel_mortgage(org_id,reg_no) |
| `risk_abnormal` | 无 case_id/is_history | 加 case_id + is_history + uk_risk_abnormal_case |
| `risk_punishment` | reason VARCHAR(500)；无 case_id/is_history | reason TEXT + case_id + is_history + uk_risk_punishment(case_id,org_id) |
| `risk_illegal` | 无 case_id/is_history | 加 case_id + is_history + uk_risk_illegal_case |
| `risk_tax_punish` | 无 case_id/is_history/tax_vio_type | 加 case_id + is_history + tax_vio_type + uk_risk_tax_punish_case |
| `risk_lawsuit` | 缺 judgment_date/publish_date/case_cause | 补全字段 + uk_risk_lawsuit_case(case_id) |
| `risk_lawsuit_party` | 无 is_history；无唯一键；org_id 无 collation | 加 is_history + uk_risk_lawsuit_party(case_id,org_id,party_role) + idx_risk_lawsuit_party_org |
| `risk_court_filed` | 缺 case_status/closing_date/hearing_date | 补全字段 + uk_risk_court_filed_case |
| `risk_court_filed_party` | 无 is_history/update_time；无唯一键 | 加 is_history + update_time + uk + idx_org |
| `risk_court_notice` | 缺 context TEXT/case_cause/hearing_date | 补全字段 + uk_risk_court_notice_case |
| `risk_court_notice_party` | 无 is_history/update_time；无唯一键 | 加 is_history + update_time + uk + idx_org |
| `risk_court_announcement` | 缺 context TEXT/notice_type/notice_date | 补全字段 + uk_risk_court_announcement_case |
| `risk_court_announcement_party` | 无 is_history/update_time；无唯一键 | 加 is_history + update_time + uk + idx_org |
| `risk_judicial_sale` | 缺 notice_name/notice_time/asset_disposal_unit | 补全字段 + uk_risk_judicial_sale_case |
| `risk_judicial_sale_party` | 无 is_history/update_time；无唯一键 | 加 is_history + update_time + uk + idx_org |
| `risk_bankruptcy` | 缺 case_type/public_date | 补全字段 + uk_risk_bankruptcy_case |
| `risk_bankruptcy_party` | 无 is_history/update_time；无唯一键 | 加 is_history + update_time + uk + idx_org |

### 2.3 关键变更总结

1. 所有含 org_id 的风险表及 `enterprise_risk_summary.org_id` 显式使用 `CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci`（19 处）。
2. `risk_punishment.reason` 从 `VARCHAR(500)` 改为 `TEXT`，避免超 500 字符源值截断。
3. 12 张直接关联企业的风险主表增加 `is_history TINYINT NOT NULL DEFAULT 0`。
4. 6 张 party 表增加 `is_history` + `uk_*_party(case_id, org_id, party_role)` 唯一键 + `idx_*_party_org(org_id, is_history)` 索引。
5. `risk_lawsuit_party` 按 v3.0 §5.5 仅有 `create_time`（无 `update_time`），其余 5 张 party 表均有 `create_time` + `update_time`。
6. 所有表使用 `COLLATE=utf8mb4_0900_ai_ci`，与正式设计一致。
7. 无 U+200B 零宽字符。

### 2.4 未修改内容

- 非风险表（enterprise_base、enterprise_industry_chain 等 12 张）
- ADS 表、CFG 表
- 运行时算法计算逻辑、接口契约
- 现网数据库（本工单只修正算法仓自带建表脚本）

## 3. 验证证据

### 3.1 结构校验脚本

```
python scripts/validate_risk_schema.py
```

结果（9/9 PASS）：
- [PASS] No U+200B zero-width spaces
- [PASS] All 25 target tables found
- [PASS] All org_id fields use utf8mb4_general_ci
- [PASS] risk_punishment.reason uses TEXT
- [PASS] is_history found 26 times (>=24 expected)
- [PASS] All case_id tables have case_id field
- [PASS] All party tables have correct unique keys and org indexes
- [PASS] risk_lawsuit_party has only create_time (no update_time)
- [PASS] enterprise_risk_summary has both indexes

### 3.2 仓内测试

```
python -m pytest tests/ -v
```

结果：59 passed in 0.18s

## 4. 架构合规自检

- 算法只在 Python：N/A（本工单修改 SQL DDL 脚本，不涉及算法逻辑）
- 前端 -> Java -> Python：OK 未改变调用链
- NebulaGraph：OK 未涉及图数据库
- 可观测性：OK 未移除或改变埋点
- CI/CD：待后续流水线验证
- demo/lumen 边界：OK 仅修改算法仓自带建表脚本
- 共享聚合核心：OK 未改变服务边界
- ADS/Mock 策略：OK 未修改数据和 Mock
- D8 前端规范：N/A
- D9 数据血缘：OK DDL 与正式 DWD v3.0/v3.1 设计一致
- D10 交互规范：N/A

## 5. Cost

- actual_tokens: 35000
- model_used: GPT-5.6
- actual_cost: 0.45
- cost_warn: green