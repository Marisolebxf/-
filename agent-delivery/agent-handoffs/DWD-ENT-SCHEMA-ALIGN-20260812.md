# DWD-ENT-SCHEMA-ALIGN-20260812 Handoff

## 1. 任务与授权

- 任务：企业 DWD 代码、数据库、设计文档结构纠偏。
- 授权人：human:徐滕强。
- 授权口径：有数据表优先保留数据；数据库变更需谨慎；不得修改算法代码。
- task-registry：用户直接发起的临时修复，未提供 registry task ID，本次未写 task-registry。
- ponytail：full。

## 2. 范围与实现

本次不改变招标功能点与接口范围，只修复企业 DWD 结构和数据迁移：

- 将 4 张 ODS 原始风险结构转换为 v3.0 正式风险结构：
  `risk_abnormal`、`risk_punishment`、`risk_illegal`、`risk_tax_punish`。
- 将 3 张有数据 `U+200B` 零宽字符表迁入规范表：
  `risk_judicial_case`、`risk_executed`、`risk_bankruptcy`。
- 将 ODS 结构 `risk_bankruptcy_party` 转换为规范 party 结构。
- 将全局 1 行宽表 `enterprise_risk_summary` 重建为
  `org_id + risk_type` 长表。
- 删除 0 行 `enterprise_base2` 和 0 行 `risk_dishonest[U+200B]`。
- `enterprise_industry_chain` 仅新增可空 `org_id` 和索引，不生成假 ID。
- `enterprise_financing` 经依赖扫描后保持现行字段，不执行改名。

执行脚本：

- `agent-delivery/data/ddl/gkxlumenx_dwd_enterprise_schema_align_20260812.sql`
- `agent-delivery/data/ddl/gkxlumenx_dwd_org_id_collation_align_20260812.sql`

## 3. 偏离与数据隔离

- `risk_bankruptcy_party` 原始 20,000 行中：
  - 7,705 行无法按 `case_no` 关联本批破产主表；
  - 已关联数据中有 129 条违反目标
    `case_id + org_id + party_role` 唯一键。
  - 规范表迁移 12,166 行；全部原始行保留于
    `risk_bankruptcy_party__pre_fix_20260812`，未静默丢弃。
- `enterprise_industry_chain` 20,000 行无法权威回填 `org_id`：
  `enterprise_base.enterprise_code` 当前全部为空，按名称仅匹配 3 行。
  经 human 确认，新增可空列但不回填、不设 `NOT NULL`。
- `risk_punishment.reason` 从候选设计的 `VARCHAR(500)` 改为 `TEXT`，
  避免 79 条超过 500 字符的源值被截断。
- 无历史状态源字段的有效风险记录暂计为当前记录；异常/严重违法按
  `remove_date`、破产按 `history_status` 判定。

## 4. 产物

- `agent-delivery/data/ddl/gkxlumenx_dwd_enterprise_schema_align_20260812.sql`
- `agent-delivery/data/ddl/gkxlumenx_dwd_org_id_collation_align_20260812.sql`
- `agent-delivery/data/data-design/企业/DWD表结构设计-企业模块-MySQL-v3.0.md`
- `agent-delivery/data/data-design/企业/DWD表结构设计-企业工商表-MySQL-v3.1.md`
- `agent-delivery/data/data-design/企业/DWD表结构设计-企业指标汇总表-MySQL-v3.1.md`
- 本 handoff。

未创建 commit，未修改任何算法代码。

## 5. 验收证据

### 5.1 数据库

- 9 张规范目标表均为 `id BIGINT AUTO_INCREMENT PRIMARY KEY`。
- 迁移目标必填键缺失：0。
- 迁移目标唯一键重复：0。
- 正式表名中的 `U+200B`：0。
- 暂存 `__v31fix` 表：0。
- `enterprise_base2`：已删除。
- `enterprise_industry_chain`：20,000 行全部保留；新增可空 `org_id`
  和 `idx_enterprise_industry_chain_org_id`。
- `enterprise_financing`：11,230 行及现行字段保持不变。
- `enterprise_risk_summary` 与全部含 `org_id` 的规范风险表已统一为
  `utf8mb4_general_ci`；`enterprise_industry_chain.org_id` 原本已是同一规则。
- 与 `enterprise_base.org_id` 的直接 JOIN 已验证通过，不再报 MySQL 1267。
- `enterprise_risk_summary`：
  28,758 行、28,183 个 `org_id`、累计 87,396 条风险；
  `total_count != current_count + history_count` 异常数为 0。
- `risk_bankruptcy_party`：目标孤儿 0、目标重复键 0。
- 所有有数据原始表已保留为
  `__pre_fix_20260812` / `__raw_u200b_20260812`。

### 5.2 测试

- `lumen-algo-py`: `python -m pytest tests/test_real_data.py`
  → 7 passed。
- `demo-svc-topic-py`:
  `.venv/bin/python -m pytest tests/test_dwd_v3_compatibility.py tests/test_sqlalchemy_data_layer.py`
  → 37 passed。
- 现网 MySQL smoke：
  风险汇总、司法、执行、破产 party JOIN、异常、处罚、严重违法、税收违法均成功返回。

## 6. 后续责任

### 6.1 算法团队

本次不需要修改 `lumen-algo-py`：最新代码已兼容现行融资字段，并已通过测试。

仍需算法团队单独处理：

1. `demo-algo-ent-analysis/scripts/mysql/schema_mysql.sql` 中风险明细 DDL
   仍是简化旧结构，应更新为 v3.0 ORM 实际字段；本次遵照“不得修改算法代码”未改。
2. `demo-algo-ent-analysis` 的产业链分析使用
   `industry_chain / industry_chain_node / industry_chain_role /
   is_chain_owner / participation_depth`，而现行 ES ETL 使用
   `chain_name / node_name / node_stage / is_chain_leader / chain_score`。
   需由算法与数据团队统一契约后调整读取映射，禁止直接删改现网字段。

### 6.2 数据团队

1. 修复 `enterprise_base.enterprise_code` 全空问题，建立权威
   `enterprise_code → org_id` 映射后回填
   `enterprise_industry_chain.org_id`，验收 100% 映射率后再设非空/唯一键。
2. 提供同批次 `dwd_org_bankruptcy_public_cases` 与
   `_list`，处理隔离的 7,705 条孤儿和 129 条重复。
3. 修复外部 ODS→DWD 装载流程，禁止再次把 ODS 原始表结构直接覆盖 DWD
   正式表或生成带不可见字符的表名。
4. 观察期结束后，由 human 确认是否删除
   `__pre_fix_20260812` / `__raw_u200b_20260812`。

## 7. 架构合规自检

- D1 算法只在 Python：✅ 未在 Java 增加算法。
- D2 前端 → Java → Python：✅ 未改变调用链。
- D3 NebulaGraph：✅ 未引入其他图库。
- D4 可观测性：✅ 未改变运行服务；现有埋点未移除。
- D5 CI/CD：✅ 本次为数据库与设计文档纠偏；代码仓未 push。
- D6 demo 只读 merge：✅ 未向 lumen merge。
- D7 共享聚合核心：✅ 未改变服务边界。
- D8 ADS/Mock 数据策略：✅ 未伪造业务数据；异常源行保留隔离。
- D9 前端 Design：N/A，无前端改动。
- D10 数据血缘：✅ 汇总来源、口径、异常与回退表已记录。
- D11 交互规范：N/A，无交互改动。

## 8. Cost

- actual_tokens：Cursor 会话未提供可核算值。
- model_used：GPT-5.6 Sol。
- actual_cost：Cursor 会话未提供可核算值。
- cost_warn：无法计算；未写 task-registry。
