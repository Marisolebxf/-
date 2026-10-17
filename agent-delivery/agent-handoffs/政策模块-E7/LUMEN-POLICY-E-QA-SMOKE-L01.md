# LUMEN-POLICY-E-QA-SMOKE-L01 · 政策专题 E1 — 已发布金路径冒烟

> 格式参考 `templates/handoff-template.md`；内容按 2026-09-02 对 K8s 已发布 `lumen-ui-topic` 实测。本单 **不改业务代码**。  
> 总控：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md) §4  
> 缺陷包：[`LUMEN-POLICY-E-QA-SMOKE-L01-defect-pack.md`](./LUMEN-POLICY-E-QA-SMOKE-L01-defect-pack.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。tech_task。不要自行 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 删验收条。五条金路径均在已发布页手跑；Job 未 succeeded 不改判 PASS；未拿 `e2e:chain-gold` job 26183 当本叶结论。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 已发布冒烟，未挂载 compress。 |

## 结论（给 coordinator）

**FAIL**（1 PASS / 4 FAIL）。**不要**写「联调通过」。请按缺陷包派 **C1 frontend**（先修 `analysis_fp` SHA-256 + 篮 VID）。

- 证据源：http://192.168.88.50:30892 （deploy `gkx-lumen-topic:97963375`，**不是** demo / localhost）
- Playwright：已用（Chromium / `@playwright/test` 1.51，headless，点已发布前端）
- CI：`e2e:policy-gold` 未绿，本叶手跑。**未**把 `e2e:chain-gold` [26183](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26183)（CHAIN #4 wait_view）当政策结论
- 健康体（辅助）：`GET http://192.168.88.50:30899/policy/topic/v1/policy/health` **200**，`java.status=up` `gkxlumen-topic-policy-biz`，`python.pathPrefix=/internal/policy`，`baseUrl=http://gkxlumen-platform-entan-py:8000`，`degraded=false`。Trace `3a4516e481c696b1ee1a9178a944538f`
- D12：本会话 `/api/*` 均打 `192.168.88.50:30892` → gateway；无 demo-* host
- 缺陷包：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-L01-defect-pack.md`

## 五条金路径

| # | 故事 | 路由 | 判定 | 实际现象 | HTTP / 页面态 | X-Trace-Id |
|---|------|------|------|----------|---------------|------------|
| 1 | `US-E7-POL-01c` | `/policy/search` | **PASS** | 搜「半导体」出政策卡 12 张（total 507）；结果区无「加入对比篮」「深度分析」 | GET search **200** | `c8aec115d7b1f433fcee944cb534b79c` |
| 2 | `US-E7-POL-01`+`05` | 对比篮产业 Tab → `/policy/overview` | **FAIL C1** | 篮分发成功，角标「来自对比篮 · 产业」可见；**开始分析 disabled**（VID 未形成 `chain:INB…`）。空配置页禁止空跑已见 | 无 Create | 见缺陷包（本步无 Create） |
| 3 | `US-E7-POL-02`+`06` | `/policy/overview` | **FAIL C1** | 锚点 `chain:INB170101` 可配；点开始分析后 **未进过程页** | POST tasks **200** `code=1` `analysis_fp 必须是 64 位小写 SHA-256` | `6d2565eb49b41650e411f061c8220465`（#4 同源闸门；#3 同契约） |
| 4 | `US-E7-POL-03` | `/policy/analysis` | **FAIL C1** | 同上，未出区域矩阵/雷达；未 succeeded | POST tasks **200** 同上 msg | **`6d2565eb49b41650e411f061c8220465`** |
| 5 | `US-E7-POL-04` | `/policy/recommendation` | **FAIL C1** | VID 与「一级权重 100%」文案可见；开始分析仍 disabled（指标未入模）。即使提交也会撞同一 `analysis_fp` 闸 | 无有效 Create | 同 #4 闸门 |

Tempo：http://192.168.88.50:30201/api/traces/6d2565eb49b41650e411f061c8220465  
Grafana Explore：http://192.168.88.34:3000（**旧环境已废弃**；现网 Grafana：$newGf） 数据源 Tempo，粘贴上表 id。

### 1. US-E7-POL-01c

- 打开 `/policy/search`，智能检索「半导体」。
- GET `/api/policy/topic/v1/policy/search?keyword=半导体` 200，`items=12` `total=507`，非 5xx。
- 卡片 `article.policy-search-result` +「查看详情」；正文无「加入对比篮」「深度分析」。

### 2. US-E7-POL-01 / 05

- 空配置：无 VID 时「开始分析」disabled，禁止空跑文案存在。
- 产业查询加入对比篮 → dock 打开 → 产业 Tab → 勾选 →「发起分析」→ 模态选「政策时序分析」→「下一步：前往政策分析配置」。
- 落地 `/policy/overview?source=compare-basket…`，**来自对比篮 · 产业**可见。
- **开始分析仍 disabled**：入篮产业 id 未变成 `chain:INB…`。不是「篮空引导」空态。

### 3–4. 时序 / 区域 wait_view

- 直达配置 `object_ids[]=INB170101` 时图上 VID 文案出现（#3/#4 可点开始；#5 另受指标闸）。
- I2-12 切条件：**未**自动 POST Create（点「开始分析」才发）。
- Create 被 Java 拒：`analysis_fp` 须 64 位小写 SHA-256。FE `policyAnalysisFingerprint` 为 `'\|'` 拼接明文。已有 `createAnalysisFingerprint` 未接。
- URL **无** `view=processing`。Job 未 succeeded → 按总控 **红**，不以过程页失败改判 PASS（本叶连过程页都没进）。

### 5. US-E7-POL-04

- 三维一级权重合计 100% 文案出现；QPOL-02 PendingBadge 在评审块（可带角标）。
- 开始分析 disabled（入模指标）。与 #3/#4 同一 Create 契约，修指纹后须再跑通 Job。

## I2-12

| 条 | 结果 |
|----|------|
| 切条件不自动起任务 | **观察到**：改条件未自动 POST（#3 脚本计数 0） |
| 条件栏「开始分析」 | **有** `data-testid=policy-start-analysis`；「重新分析」`policy-rerun-analysis` |
| 同用户同条件一条在跑 | **未验到**（Create 被拒） |
| 当天已成功直接打开结果 | **未验到** |
| 「重新分析」force | **未验到** |

## 问题清单

- 主 C1：`analysis_fp` 明文 vs Java SHA-256 闸。
- 次 C1：对比篮产业短码无法形成图上 VID，开始分析 disabled。
- #5 指标未默认入模（修指纹后复测）。
- 残差：已发布登录仍 mockLogin（与 CHAIN E1 相同，不挡本金路径检索）。`e2e:chain-gold` 26183 红 **不是**本叶。

## 修改内容

- 无业务仓代码变更。仅本 handoff + 缺陷包 + evidence 手跑脚本。

## 测试结果

- Playwright 对 http://192.168.88.50:30892：**#1 PASS，#2–#5 FAIL**。
- 健康体 30899 policy health 200。
- 手跑记录：`evidence/LUMEN-POLICY-E-QA-SMOKE-L01/run-notes.json` · `policy-gold.spec.ts`

## 遗留风险

1. 修指纹后 Job 仍可能 freeze failed → 仍红（总控：未 succeeded ≠ 空态）。
2. 产业查询入篮对象与图上链码不一致时，篮分发会再次 disabled。
3. `e2e:policy-gold` CI 仍未绿；复测继续手跑 30892 或补 CI。

## CI/CD（必填）

- 分支：未改业务仓
- commit：orchestration 本叶 handoff（见 git）
- pipeline：未触发业务仓 CI（QA 不改代码）
- 部署 namespace：`dev`；镜像 `gkx-lumen-topic:97963375` · `gkxlumen-topic-policy:7d12b8dd` · `gkxlumen-topic-async-service:7d12b8dd` · `gkxlumen-entan-py-api:ea3acc39`（E0 已核）
- K8s rollout：E0 已绿，本单未再滚
- dev 测试 URL：http://192.168.88.50:30892 ；网关 http://192.168.88.50:30899

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-topic-policy-biz` / `gkxlumen-topic-async-service-biz` / gateway
- traceId：search `c8aec115d7b1f433fcee944cb534b79c`；Create 拒 `6d2565eb49b41650e411f061c8220465`；health `3a4516e481c696b1ee1a9178a944538f`
- Tempo / Loki：Tempo API 200 有 batches（Create 抽样）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | 通过。QA 未改 Java 算法 |
| 2 调用链 前端→Java REST→Python `/internal/*` | 通过。health python `/internal/policy`；Create 打 Java async（被指纹闸拦住，未到 Python Job） |
| 3 图谱 Nebula | 通过。VID 规则要求 `chain:INB…`，未直连 nGQL |
| 4 可观测 | 通过。`X-Trace-Id` / Tempo |
| 5 CI/CD | N/A（本单不改业务仓） |
| 6 demo2 merge | N/A |
| 7 共享聚合核心 | N/A |
| 8 数据策略 ADS | 通过。search 经 Java 有实包 |
| 9 D8 Design | N/A（不改 UI） |
| 10 D9 血缘 | N/A 本叶未改 ⓘ；#5 QPOL-02 角标在评审块 |
| 11 D10 交互 | 部分：wait_view 因 Create 拒未跑到 |
| 12 D12 demo/lumen 隔离 | 通过。只认 30892 / 30899，无 demo-* 服务 |

## cost 四字段（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 320000 |
| model_used | grok-4.6 |
| actual_cost | 1.73 |
| cost_warn | green |

口径：`budget-estimate.md` §8.2，B 档 in $3/M out $15/M，qa 默认 in/out=80/20。`source: estimate`。未超 $5。

## 涉及文件

- `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-L01.md`（本文件）
- `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-L01-defect-pack.md`
- `agent-delivery/agent-handoffs/政策模块-E7/evidence/LUMEN-POLICY-E-QA-SMOKE-L01/`（手跑 spec + run-notes）
