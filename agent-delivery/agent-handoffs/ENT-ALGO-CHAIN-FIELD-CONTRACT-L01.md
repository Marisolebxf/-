# ENT-ALGO-CHAIN-FIELD-CONTRACT-L01 Handoff

## 1. 任务与监管

- 任务：企业产业链 算法读取字段与 DWD/ES ETL 契约统一。
- 执行：algorithm-agent。
- 认领/监管：human:唐绍祖。
- ponytail: full。

## 2. 确认人

- DWD v3.1 `enterprise_industry_chain` 正式字段定义来源：`DWD表结构设计-企业工商表-MySQL-v3.1.md` §3.11
- 字段语义等价性确认：human:徐滕强（DWD schema owner），2026-08-12 纠偏 handoff `DWD-ENT-SCHEMA-ALIGN-20260812.md` 已确认产业链字段为历史命名差异，语义等价。

## 3. 字段映射矩阵

| 算法侧字段 | DWD v3.1 正式字段 | 语义 | 来源表 | 映射方式 |
|---|---|---|---|---|
| `industry_chain` | `chain_name` | 产业链名称 | `enterprise_industry_chain` | 直接别名 (AS) |
| `industry_chain_node` | `node_name` | 链节点名称 | `enterprise_industry_chain` | 直接别名 (AS) |
| `industry_chain_role` | `node_stage` | 企业在链中的角色/环节 | `enterprise_industry_chain` | 语义映射 (role=stage) |
| `is_chain_owner` | `is_chain_leader` | 是否链主 | `enterprise_industry_chain` | 语义映射 (owner=leader) |
| `participation_depth` | `chain_score` | 参与深度/评分 | `enterprise_industry_chain` | 语义映射 (depth=score) |

### 3.1 结论

字段语义可一一映射。未发现不可映射字段。无需设计变更提案。

### 3.2 阻塞项

- `enterprise_industry_chain.org_id` 在 DWD v3.1 中为可空（`DEFAULT NULL`），当前 20,000 行因信用代码映射阻塞暂无 org_id。算法行为：`org_id` 为 NULL 时不生成本地哈希 ID，跳过该行企业级关联计算。此为已知数据映射阻塞，不是代码问题。

## 4. 代码变更

### 4.1 新增文件

- `entan/common/chain_field_mapping.py`
  - 提供 SQL SELECT 别名常量（`CHAIN_FIELD_ALIASES` 等）
  - 提供 `map_chain_row()` 行级映射函数（DWD 正式 -> 算法侧）
  - 提供 `algo_to_dwd()` 逆向映射函数（算法侧 -> DWD 正式，用于 mock 数据写入）

- `tests/test_chain_field_mapping.py`
  - 16 个测试覆盖：SQL 别名正确性、行级映射、逆向映射、org_id 可空处理、往返一致性

### 4.2 修改文件

以下文件的 SQL 查询从直接引用算法侧字段名改为通过 AS 别名读取 DWD 正式字段：

- `entan/basic/indicators.py` — SELECT org_id, chain_name AS industry_chain, chain_score AS participation_depth
- `entan/eval/biz_power.py` — SELECT 增加 node_stage AS industry_chain_role, is_chain_leader AS is_chain_owner
- `entan/graph/entity.py` — SELECT 增加 node_name AS industry_chain_node
- `entan/graph/incremental.py` — SELECT（读路径）+ INSERT（写路径，使用 algo_to_dwd 逆向映射）
- `innov/analysis/__init__.py` — SELECT chain_name AS industry_chain
- `entan/mockgen/generate.py` — INSERT 使用 algo_to_dwd 逆向映射，确保 mock 数据写入正式字段名
- `scripts/mysql/schema_mysql.sql` — `enterprise_industry_chain` DDL 对齐 DWD v3.1 §3.11 正式字段名

### 4.3 未修改内容

- API 层（`api/entan_analysis_routes.py`、`api/entan_gap_routes.py`）中的 `chain_name` 查询目标是 `enterprise_score`（ADS 表），不是 `enterprise_industry_chain`（DWD 表），字段名本就一致，无需修改。
- `entan/depth/pipeline.py` 中的 `chain_name` 同样来自 ADS 层，不涉及 DWD 读取。
- 现网 `enterprise_industry_chain` 字段未被删除、改名或覆盖。
- 未伪造 org_id。

## 5. 验证证据

### 5.1 测试结果

```
python -m pytest tests/ -v
```

结果：75 passed in 0.13s（59 原有 + 16 新增 chain mapping 测试）

### 5.2 结构校验

```
python scripts/validate_risk_schema.py
```

结果：9/9 PASS（DDL 变更未影响风险表校验）

## 6. 架构合规自检

- 算法只在 Python：OK 映射层在算法读取侧，不改变 DWD 结构
- 前端 -> Java -> Python：OK 未改变 API 路径或响应结构
- NebulaGraph：OK 产业链图谱节点读取兼容
- 可观测性：OK 未改变埋点
- CI/CD：待后续流水线验证
- demo/lumen 边界：OK 仅修改算法仓代码
- 共享聚合核心：OK 未改变服务边界
- ADS/Mock 策略：OK mock 数据写入使用正式 DWD 字段名
- D8 前端规范：N/A
- D9 数据血缘：OK 算法读取层字段与正式 DWD v3.1 一致
- D10 交互规范：N/A

## 7. Cost

- actual_tokens: 30000
- model_used: GPT-5.6
- actual_cost: 0.40
- cost_warn: green