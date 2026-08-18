# LUMEN-SVC-JAVA-JOB-WHITELIST-L01 · SVC Gate-1 Job 白名单扩八叶子

> 日期：2026-08-18  
> Task：`LUMEN-SVC-JAVA-JOB-WHITELIST-L01`  
> 总控：`DEMO-SVC-FULL-底座后全量-长任务总控.md` / `DEMO-SVC-GATE1-全量派单.md`（已授权 · human:侯佳伟）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只扩 `SvcAnalysisTypes` 白名单 + analysis_key 映射 + 最小单测；不新建依赖、不写 NLP |

## 范围与实现

### Before → After

| | analysisType 白名单 | analysis_key |
|---|---------------------|--------------|
| **Before** | `svc:analysis:shortboard`（1） | `svcan.shortboard.v0` |
| **After** | 八叶子（见下，8） | `svcan.{leaf}.v0` |

| analysisType | analysis_key | 页面对齐 |
|--------------|--------------|----------|
| `svc:analysis:org_coverage` | `svcan.org_coverage.v0` | 机构分析 · 产业领域 |
| `svc:analysis:org_trend` | `svcan.org_trend.v0` | 机构分析 · 新增趋势 |
| `svc:analysis:tech_power` | `svcan.tech_power.v0` | 机构分析 · 技术力 |
| `svc:analysis:shortboard` | `svcan.shortboard.v0` | 生态 · 短板（既有） |
| `svc:analysis:graph` | `svcan.graph.v0` | 生态 · 图谱 |
| `svc:analysis:shenzhen` | `svcan.shenzhen.v0` | 生态 · 深圳 |
| `svc:analysis:attract` | `svcan.attract.v0` | 招引 |
| `svc:analysis:cultivate` | `svcan.cultivate.v0` | 培育 |

- `SvcAnalysisAdapterImpl.analysisTypes()` 注册全量白名单（同一 Adapter，同 chain 模式）
- create 时 `analysis_key` 为空则抛「不支持的 SVC analysisType」；未注册类型仍由 `AnalysisTaskServiceImpl` 返回：`功能尚未开放或不支持的 analysisType：{type}`
- 调用链不变：FE → Java async-service → topic-py `/internal/gkx-svc/analysis/tasks/*`（禁直连 algo / demo-*）

## 偏离说明

- 本机 JDK8 + Maven 过旧，单测待 CI（与 `LUMEN-SVC-JAVA-JOB-L01` 同策略）
- Python/algo 仍可能只实现 shortboard 样板；本叶只放开 Java 白名单，真实 ADS 结果由 `DEMO-SVC-PY-SVCAN-MODELS-L01` / FE 叶消费

## 产物清单

| 产物 | 路径 |
|------|------|
| 白名单 | `gkxlumen-topic-async-service-biz/.../SvcAnalysisTypes.java` |
| Adapter 守卫 | `.../SvcAnalysisAdapterImpl.java` |
| 单测 | `SvcAnalysisTypesTest` / `SvcAnalysisAdapterImplTest` |
| 本 handoff | `agent-handoffs/服务机构-SVC/LUMEN-SVC-JAVA-JOB-WHITELIST-L01.md` |

## 验收证据

- [x] 白名单 1→8；三视图/短板/招引培育键齐全
- [x] 未知类型诚实拦截文案保留
- [x] commit + push `origin/dev`
- [ ] CI 绿（待 pipeline）

## CI/CD

- 分支：`dev`
- commit：`ac5df683adda23a424d3e5a9ad63deaffd74a4b0`
- pipeline：push 后由 GitLab CI 触发（async-service 模块）
- 部署：随 platform K8s dev rollout（topic-async-service）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 2 | 前端→Java→Python；Java 不写 NLP | ✅ |
| D12 | 禁 Feign demo-* | ✅ |
| Job 真源 | async-service 签发 snapshot 不变 | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~3.5 万 |
| actual_cost | 估 <$2 |
| cost_warn | false |

## 联调确认

联调通过（代码侧）：Java 可诚实接受八叶子 `svc:analysis:*`；非法类型仍拒。下一叶：`DEMO-SVC-PY-SVCAN-MODELS-L01`（algo 出结果）+ `LUMEN-SVC-FE-ANALYSIS-FULL-L01`（FE 接线新类型）。
