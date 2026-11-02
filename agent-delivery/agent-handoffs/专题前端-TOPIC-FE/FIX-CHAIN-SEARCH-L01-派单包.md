# FIX-CHAIN-SEARCH-L01 派单包 — 产业链高级筛选 400 修复（后端兼容数组 value）

> **状态**：待认领（registry 已入库 `backlog`）
> **建单背景**：2026-11-02 用户线上报障，产业链「高级筛选」查询报「产业查询不可用，请保留当前条件稍后再试」。trace 排查定位为 Java DTO 反序列化失败。用户裁定：**后端兼容**。

## 1. 任务基本信息

| 字段 | 值 |
|---|---|
| Task ID | `FIX-CHAIN-SEARCH-L01` |
| task_type | `bugfix`（P0） |
| 执行 Agent | `agent:api-agent` |
| 默认监管人 | `human:侯佳伟`（dispatch-rules#agent_supervisors；开工时可由实际开 Cursor 会话的真人认领，`supervised_by` 填该真人） |
| 认领类型 | `pull`（侯佳伟认领）或 `coordinator_dispatch`（如他人代派） |
| repo | `lumen-svc-platform`（**origin/dev 直推，禁 main**；commit 必带 `[agent:api-agent]`） |
| 模块 | `gkxlumen-topic-chain`（topic-chain-biz 服务） |
| delivery_phase | implementation |
| 强度 | **ponytail full**（最小 diff 修根因；不新增依赖；不做前端改动） |
| 预估 | effort_points=1 / difficulty=S / estimated_tokens=40000 |

## 2. 故障现象

- 页面：专题系统 → 产业链分析 → 产业查询（`/industry-center/search?mode=advanced`）高级筛选
- 操作：选「产业节点」条件（`industry_link in [CL-SEI-01|INB1303|INB130301]`）后查询
- 结果：红色提示「**产业查询不可用，请保留当前条件稍后再试**」；同页简单筛选、我的方案均正常

## 3. 线上证据（2026-11-02 14:58:27 CST）

**traceID**：`cbf0f78478b907d37598cba1f86ebaf1`（lumen 平面，Tempo :30202 / Loki :30311）

**Span 断点**：
- `gkxlumen-gateway` POST `gkxlumen-topic-chain-biz` → 400（11ms）
- `gkxlumen-topic-chain-biz` POST `/topic/v1/industry/search` → **400**（7.9ms），随后 `OnCommittedResponseWrapper.sendError`
- 无任何 DB / 下游 Python span —— 请求未进业务逻辑

**Loki 日志**（`service_name="gkxlumen-topic-chain-biz"`，时间窗内仅 3 行，全为同一错误）：

```
Resolved [org.springframework.http.converter.HttpMessageNotReadableException: JSON parse error: Cannot deserialize value of type `java.lang.String` from Array value (token `JsonToken.START_ARRAY`)]
```

**复现请求**（前端原始抓包）：

```bash
curl --url 'http://10.50.69.111:30892/api/chain/topic/v1/industry/search' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'systemCode: topic' \
  -H 'X-Trace-Id: cbf0f78478b907d37598cba1f86ebaf1' \
  --data-raw '{"mode":"advanced","keyword":"","logic":"all","conditions":[{"id":"f14","field":"industry_link","operator":"in","value":["CL-SEI-01|INB1303|INB130301"]}]}' \
  --insecure
```

## 4. 根因

`/topic/v1/industry/search` 请求体中 `conditions[].value` 的 **DTO 字段定义为 `String`**：
- 简单筛选：`value` 传标量字符串 → 正常；
- 高级筛选 `operator=in`：前端传 **字符串数组** → Jackson 遇 `START_ARRAY` 反序列化失败 → `HttpMessageNotReadableException` → 400。

`in` 语义下数组是前端合理契约，修后端，不改前端。

## 5. 修复要求

1. **根因修一处**：条件 DTO 的 `value` 兼容数组和字符串（如 `List<String>` + 自定义反序列化/`@JsonSetter` 容错，或 `Object` + 收敛归一化——按仓内既有模式选最小实现，不要两套都做）
2. **向后兼容**：`value` 传标量字符串时行为完全不变（按单值处理）；`logic=all/any` 语义不受影响
3. **入参校验**：`value=null` / 空数组 / 非法类型返回明确业务校验信息（400 + 可读 message），不再抛 Jackson 原始栈
4. **自检**：按 ponytail 规约留一个最小可跑检查（curl 回归脚本或单测，覆盖数组 / 字符串 / null 三种入参）
5. **可观测**：不改动既有埋点；如有统一异常处理，保持 trace / X-Trace-Id 透传不变

## 6. DoD 对照（registry 已写）

1. 后端接受 `conditions[].value` 为字符串数组（`operator=in`），返回结构与非空筛选结果与简单筛选一致
2. 向后兼容：`value` 传标量字符串时行为不变
3. 异常入参返回明确 400 校验信息而非 Jackson 原始报错
4. 原报错场景回归验证：`mode=advanced + industry_link in ["CL-SEI-01|INB1303|INB130301"]` 查询成功（handoff 附 curl 证据）
5. touch `gkxlumen-topic-chain`；commit 带 `[agent:api-agent]`

## 7. 发布与验收闸门

- ⚠️ **人工验收闸门（2026-10-20 用户裁定）**：改动完成后**默认停本地工作区**，等监管人走查确认后再 push `origin/dev`。本次为 P0 线上故障，如需「完工即推」，须由监管人 `human:侯佳伟` 在 /goal 或本包签署处**明确授权**（授权后走 CI → K8s dev rollout，再按 §6.4 回归验证）。
- DoD 第 5 条的「推 origin/dev，CI 绿」仅在获上述授权时执行；未授权时执行为「本地自检通过 + 监管人验收」，push 后补 CI 链接进 handoff。
- CI 绿后验证 K8s dev（`http://10.50.69.111:30892`）高级筛选恢复可用；前端无需改动，回归走原 curl。

## 8. Handoff 要求

- 交付后写 `agent-handoffs/FIX-CHAIN-SEARCH-L01.md`（模板按 `templates/handoff-template.md`）：
  - 根因 / 修法 / diff 摘要 / 三种入参自检结果 / 回归 curl 证据
  - `ponytail: full` 行
  - 架构合规自检（调用链未变、无算法逻辑进 Java、可观测未动）
  - cost 四字段回填（actual_tokens / model_used / actual_cost / cost_warn）
- 状态机：`bugfix` → in_progress → pending_test → testing → ready_to_sign → done

## 9. 排查材料归档

- 本包：`agent-delivery/agent-handoffs/专题前端-TOPIC-FE/FIX-CHAIN-SEARCH-L01-派单包.md`
- 故障截图：会话附件（用户 2026-11-02 15:00 提供高级筛选报错页截图）

---
派单包生成：`agent:coordinator` 会话（2026-11-02，用户口头确认「后端兼容，派单修复」）
