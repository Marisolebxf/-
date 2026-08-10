# FIX-TOPIC-SEARCH-PY-DWD-PREFIX-L01 Handoff

> 状态：DWD v3.0 设计、Python 兼容实现及真实库结构迁移完成；等待应用级联调与旧测试改造，暂不申请 done  
> 执行：agent:data-agent  
> 监管：human:徐滕强  
> 详细审计：`agent-handoffs/FIX-TOPIC-SEARCH-PY-DWD-PREFIX-L01-audit.md`

## 1. 范围与实现

本轮处理 `demo-svc-topic-py` 的 DWD 表名前缀、数据访问层、Mock 运行路径和结构漂移错误暴露。

已实现：

1. SQLAlchemy 2.x 数据访问基础
   - Engine + QueuePool（20 基础连接、10 overflow）
   - ORM Session 退出统一 rollback
   - 遗留 `%s` SQL 与 ORM 共享连接池
   - 只读 Repository 基类
2. DWD v3.0 Model
   - 本轮 12 张非风险目标表全部建立 SQLAlchemy Model
   - 专利、投资、区域/产业/趋势/统计字段已按 human 确认的 MySQL v3.0 目标结构更新
   - 风险汇总 Model 保持现有稳定契约
3. DWD 表名规范
   - Python 运行时 SQL 中企业/风险表统一移除历史 `dwd_` 前缀
   - `dwd_sz_city_benchmark` 经核实确由 Python 使用，已按 human 决策改为目标表 `sz_city_benchmark`
   - 真实库已完成重命名和 v3.0 结构切换；旧结构保留为 `__pre_v3` 回退表
4. Mock fail-closed
   - `GKX_MOCK_ENABLED=1` 直接拒绝启动
   - 5 类 Docker 镜像默认均为 0
   - Search/entan/science 上游失败直接抛错
   - 不再伪造算法任务 `running` 或同步评分结果
5. 结构漂移错误
   - MySQL 1054/1146 转换为明确的 503 统一响应
   - 成功 API 路径、请求、响应字段和层级未修改
6. 可重复结构审计
   - `scripts/audit_schema_contract.py`
   - 只读比较 ORM Model 与目标 MySQL 表
7. 正式 DWD 结构与 Python 兼容
   - 新增 36 张已复核表的 MySQL v3.0 正式候选设计和完整 DDL
   - 18 类风险 SQL 使用 DWD 物理列并 alias 回稳定 API 字段
   - 6 类 Party 表统一以 `case_id` JOIN，`is_history` 从 Party 返回
   - 约定不入 DWD 的字段显式 `NULL AS`，不删除 API 字段
   - `risk_limit_high`、`risk_equity_freeze` 将 `case_id` 映射回原 API ID
   - `enterprise_type_scale_stats.region_id` 和 `enterprise_distribution.stat_date` 查询已对齐
   - `enterprise_risk.py` 已删除 Mock 生成器、Mock 分支和 ES→Mock 静默兜底
8. 真实库迁移
   - 目标：公网 MySQL `gkxlumenx_dwd`
   - 先完成结构快照及 10 张有数据表的完整备份，再执行迁移
   - 9 张有数据差异表采用“目标暂存表 → 映射迁移 → 行数校验 → 原子切换”
   - 24 张空风险表按 v3.0 DDL 建立目标结构后原子切换
   - 新建 `shenzhen_enterprise_summary`、`enterprise_distribution`
   - `dwd_sz_city_benchmark` 已重命名为 `sz_city_benchmark`
   - 33 张旧表保留为 `__pre_v3`，未删除

## 2. Human 决策落实

human:徐滕强确认：

- Java 已接入的 API 契约不改。
- 数据库字段变化由 Python Model/Repository 兼容。
- 无法兼容时显式报错，不伪造。
- ES 更新脚本等 DWD 表结构稳定后再处理。
- DWD 表存在但无数据时接口应正常返回空结果；只有缺表、缺字段或数据源故障才显式报错。

## 3. 偏离与 As-built

### 3.1 不适配旧精简样例结构

原因：当前真实库精简字段来自/符合 Mock 灌数脚本；代码 SQL 与权威 DWD 设计整体更接近。若把代码全面适配到精简 Mock 结构，会固化错误规范。

As-built：

- ORM Model 已切换为 human 确认的 DWD v3.0 目标结构。
- API 字段契约保持不变。
- 缺字段/缺表时明确返回 503。
- 风险 DWD→API 兼容映射已在 SQL/Repository 边界实现。

### 3.2 旧 Mock 测试与其他不可达 helper

运行时 Mock 已不可启用，静默回退已切断；本轮风险模块的 Mock helper/branch 已删除。其他模块仍有不可达 Mock helper，旧全量测试仍依赖 Mock 数据集。

后续需单独清理：

- 删除不可达 Mock helper/branch
- 将旧 Mock 接口测试改为仅测试进程可用的依赖注入 fake/contract test

## 4. 产物清单

业务仓 `demo-svc-topic-py`：

- `gkx_common/db.py`
- `gkx_common/orm_models.py`
- `gkx_common/repositories/base.py`
- `gkx_common/config.py`
- `gkx_ai_service/{search_client,entan_client,science_client}.py`
- `gkx_search_service/views/*.py`（仅 SQL 表名前缀）
- `docker/Dockerfile.*`
- `scripts/audit_schema_contract.py`
- `tests/test_sqlalchemy_data_layer.py`
- `tests/test_no_mock_runtime.py`
- `tests/test_real_data_mode.py`
- `tests/test_dwd_v3_compatibility.py`

编排仓：

- `agent-handoffs/FIX-TOPIC-SEARCH-PY-DWD-PREFIX-L01-audit.md`
- `agent-handoffs/FIX-TOPIC-SEARCH-PY-DWD-SCHEMA-REVIEW.md`
- `data/data-design/企业/DWD表结构设计-企业模块-MySQL-v3.0.md`
- 本 handoff

## 5. 验收证据

通过：

- `pytest tests/test_dwd_v3_compatibility.py tests/test_no_mock_runtime.py tests/test_real_data_mode.py tests/test_sqlalchemy_data_layer.py`
  - 47 passed
- `python -m compileall`
  - 通过
- IDE lints
  - 0 error
- `git diff --check`
  - 通过
- 公网 MySQL SQLAlchemy 实测
  - QueuePool size=20
  - ORM 与遗留 SQL 共池读取成功
- DDL 结构检查
  - 36 个 `CREATE TABLE`
  - 0 重复表名、0 重复字段
- 真实库迁移检查
  - 36/36 张目标表存在，`__v3` 暂存表为 0，`dwd_sz_city_benchmark` 为 0
  - 33 张旧结构表保留为 `__pre_v3`
  - 9 张有数据差异表迁移前后行数逐表一致
  - `sz_city_benchmark` 保留 8 行
  - 风险稳定字段 alias、party `case_id` JOIN、非风险 v3 查询均完成 SQL smoke test

未通过：

- 全量旧测试：138 passed / 216 failed
  - 失败集主要为明确标注“Mock 模式”的接口测试
  - 不能通过恢复生产 Mock 来修复

## 6. 剩余事项

1. 风险明细表与 party 表当前为空；目标结构查询已验证，应用接口应返回 200 空列表，不视为故障。
2. 需在部署环境完成 Python → MySQL 的应用级接口回归；本轮已完成数据库 SQL smoke test，未声称 K8s 联调完成。
3. 33 张 `__pre_v3` 回退表需经过观察窗口和 human 确认后再清理，本轮不擅自删除。
4. ES 当前样例数据质量需后续单独治理；按 human 决策，本轮不处理 ES 更新脚本。
5. 旧全量 Mock 测试仍需改为依赖注入 fake/contract test。
6. `task-registry` MCP 当前不可用，未擅自直接修改 registry 状态/成本字段。

## 7. 架构合规自检

1. 算法只在 Python：✅
2. 前端 → Java → Python 链路：✅，未修改
3. 图谱使用 NebulaGraph：✅，未修改
4. 可观测性：✅，错误保留日志并向上暴露
5. CI/CD：⚠️ 尚未 commit/push，未触发 Pipeline
6. demo2 只读 merge：✅，不涉及
7. Java 不写算法/不直连图谱：✅，不涉及 Java
8. ADS/DWD + Mock 策略：✅ Python 已 fail-closed；DWD 空表按正常空结果处理
9. 前端 Design：✅，不涉及 UI
10. 数据血缘/交互规范：✅，未修改前端指标展示

## 8. Cost

`actual_tokens/model_used/actual_cost/cost_warn` 待 task-registry MCP 恢复后按运行记录回填；当前不编造成本值。
