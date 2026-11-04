# Handoff — POL-REGIONDIFF-API-L01

> 需求：区域政策差异性分析（FE-POL-01B）打通后台分析链路 · Java display 门面叶
> 强度：ponytail full
> 认领：`agent:api-agent` / 监管：`human:淮政玮` / `claim_type: pull`

## 范围与实现

| 文件 | 改动 |
|---|---|
| `PolicyPanoramaService.java` | `JOB_SUB_TYPES` 白名单加 `policy_region_diff`；`jobs()` 拒绝文案、`toAsyncCreateBody` javadoc 同步 |
| `PolicyPanoramaServiceTest.java` | 补断言：`policy_region_diff` 合法转发（`analysisType` + `params.regions` 透传）；裸名 `region_diff` / 未注册 `policy_shard` 仍拒 |

- 不新增接口、不动 evaluation 资源、无 ADS 读面改动；纯白名单放行，转发链（`/topic/v1/analysis/tasks`）零改动。
- 上游：`POL-REGIONDIFF-PY-L01`（lumen-algo-py `6ec91f2`）已在 `polan/job.py` 注册同名 sub_type，`params.regions` 白名单校验在 Python 侧。

## 验证证据

- push：`lumen-svc-platform` origin/dev `df497dc`
- 单测：断言已补进 `jobsOnlyAcceptEffectAndMatch`；**本机无 mvn/JDK（仓惯例，见 `PIPELINE-WAIVER-2026-06-20.md`），随 GitLab CI `backend:build` verify**
- CI：流水线由 df497dc 触发，签收前以 `backend:build` 绿为凭

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| Java 不做算法 | ✅ 纯白名单转发，无计算逻辑 |
| 调用链 FE→Java→Python | ✅ 复用既有 asyncClient.create 链路 |
| D12 | ✅ 无 demo 依赖 |

## cost

- `actual_tokens`: ~40k
- `model_used`: glm-5.3-flash
- `actual_cost`: ~$0.04
- `cost_warn`: false
