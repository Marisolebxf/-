# QA handoff：QA-PERF-SPEC-L01 · 性能测试统一规约升格

- 时间：2026-10-14
- 监管人：human:黄敬洲（用户指派）
- 执行：agent:qa-agent
- 任务：升格 `qa/perf-baseline.md` 为三系统性能测试统一规约

## 范围与实现

| 项 | 说明 |
|---|---|
| 产物 | `agent-delivery/qa/perf-baseline.md` v1.0（草案，待会签转正式） |
| 同步 | `agent-delivery/qa/README.md` 目录索引行更新（基线表 → 性能测试规约） |

### v0.1.1 → v1.0 变更

1. **升格为统一规约**（单文件承载，不另建平行文件）：
   - 新增 §5 工具与脚本规约：jmx 归档命名（多轮不覆盖）、施压参数基线表（OP-3 关联）、AI 场景首 Token 取样口径
   - 新增 §6 接口盘点：真源分层表（API 现状主源=Controller 扫描 / 契约=OpenAPI 对照 / 页面入口=as-built catalog / 业务覆盖=acceptance-catalog / 故事级=TRACE）+ §6.2 清单就地回填表——**明确不建 perf-api-inventory.md**（用户决策 2026-10-14）
   - 新增 §7 执行与证据规约：前置检查、证据四件套（JMeter 指标/设置 + Grafana 资源 + 小结）、场景小结模板、失败处置（BUG 号 + 三联查缺陷包，qa 不改业务代码）
   - 新增 §8 交付映射：PERF 用例 sheet / 记录 sheet / 性能报告 docx 的内容来源对照
2. **修正 v0.1.1 两处引用错误**：
   - `acceptance-catalog` **存在**（v0.1.1 误报不存在，系 Glob 未穿透目录）——恢复为业务覆盖层真源（221 条功能点）；TRACE 降为故事级补充层
   - 删除 v0.1.1 中"另建 `qa/perf-api-inventory.md`"提法（OP-4 建议列同步改）
3. 保留并继承：§1 SLA 摘录（标书真源）、§2 判定口径、§3 17 场景基线、§4 环境（正式压测环境留位；B 线/INTEG 仅脚本开发用不作交付证据）、§9 开放项 OP-1~OP-8（状态如实，未替任何决策）

## 偏离说明

- 无。两处引用错误按"失败可逆"原则在维护记录中原样留痕（v0.1/v0.1.1 记录未删），便于审计。

## 产物清单

- `agent-delivery/qa/perf-baseline.md`（v1.0，约 260 行）
- `agent-delivery/qa/README.md`（索引行）

## 验收证据

- 本 handoff
- 文档内维护记录 v1.0 条目
- 开放项 OP-4（接口盘点）在本规约 §6 有了明确方法与载体，待执行

## 架构合规自检

| 铁律 | 结论 |
|---|---|
| 压测层级（前端→Java REST→Python /internal） | ✅ §2 规则 3 明确只压 Java 收口接口 |
| 算法只在 Python / D12 | ✅ 不涉及业务代码 |
| 不改业务仓 | ✅ 仅编排仓文档 |
| 决策不外包 | ✅ OP-1/2/3/6/7/8 均留人类 Owner，未替决策 |
| 用例编号对齐总集 | ✅ 引 spec §3，不重复定义 |

## cost

- ponytail: full（规约文档，未过度工程；单文件承载符合用户要求）
- actual_tokens: ~0.09M（对话累计口径，本轮约 25k）
- model_used: glm-5.3
- actual_cost: ~$1.5
- cost_warn: false

## 后续（不阻塞本单）

- OP-4 接口盘点执行（qa-agent，规约 §6 方法已定）
- OP-1/2/6 待 PM/架构师决策后回填规约
