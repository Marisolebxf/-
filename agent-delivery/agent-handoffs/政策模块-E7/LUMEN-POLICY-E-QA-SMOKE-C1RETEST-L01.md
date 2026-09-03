# LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01 · 政策专题 E1 — C1 发布后金路径复测

> 格式参考 `templates/handoff-template.md`。对 K8s 已发布 `lumen-ui-topic` 手跑。本单 **不改业务代码**。  
> 总控：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md) §4  
> 缺陷包：[`LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01-defect-pack.md`](./LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01-defect-pack.md)  
> 首轮 FAIL：[`LUMEN-POLICY-E-QA-SMOKE-L01.md`](./LUMEN-POLICY-E-QA-SMOKE-L01.md)（镜像 `97963375`，**本叶未沿用其指纹结论**）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。tech_task。FAIL → integration + 缺陷包。不要自行 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 删验收条。五条均在已发布 30892 手跑；镜像门先核 `006d186d`；Job 未 succeeded 不改判 PASS；未拿 `e2e:chain-gold` 26205 当政策结论。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 已发布冒烟，未挂载 compress。 |

## 结论（给 coordinator）

**FAIL**（1 PASS / 4 FAIL）。**不要**写「联调通过」。请按缺陷包先派 **C5 api/data**（`industry_cluster_map` / demo 前缀），clusters 有可挂图 L0 后再复测 #2～#5。

- 证据源：http://192.168.88.50:30892 （deploy **`gkx-lumen-topic:006d186d`**，已换掉 `97963375`）
- Playwright：Chromium / `@playwright/test` 1.51，headless，只点已发布前端
- CI：`e2e:policy-gold` 未绿，本叶手跑。**未**把 `e2e:chain-gold` [26205](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26205) 当本叶结论
- 健康体：`GET http://192.168.88.50:30899/policy/topic/v1/policy/health` **200**，`degraded=false`，`python.pathPrefix=/internal/policy`。Trace `374a933df17559351f2bc9ccf535c56d`
- D12：本会话 `/api/*` 均打 `192.168.88.50:30892` / `30899`；无 demo-* host
- 缺陷包：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01-defect-pack.md`

## 五条金路径

| # | 故事 | 路由 | 判定 | 实际现象 | HTTP / 页面态 | X-Trace-Id |
|---|------|------|------|----------|---------------|------------|
| 1 | `US-E7-POL-01c` | `/policy/search` | **PASS** | 搜「半导体」出卡 6 张（total 47051）；结果区无「加入对比篮」「深度分析」 | GET search **200** | `1f319c98e38090efc675d90a448cf8df` |
| 2 | `US-E7-POL-01`+`05` | `/policy/overview` 页内集群→L0 | **FAIL C5** | 产业下拉「无相关产业数据」；开始分析 disabled。clusters API **500** | GET clusters **500** | **`071b34f54c36d31761617fc884567f03`** |
| 3 | `US-E7-POL-02`+`06` | `/policy/overview` | **FAIL C5/C1** | VID `chain:INB170101` 可见；三维全开；开始分析仍 disabled（无集群）。**未进过程页**，Create 未发 | 无 Create | 见 #2 clusters；本步无 Create |
| 4 | `US-E7-POL-03` | `/policy/analysis` | **FAIL C5/C1** | 同上，未出矩阵/雷达；未 succeeded | 无 Create | 同 #2 |
| 5 | `US-E7-POL-04` | `/policy/recommendation` | **FAIL C5/C1** | 一级权重 100% 绿条可见；指标 Java 实包空；开始分析仍 disabled。任务未跑通 | 无 Create | 同 #2 |

Tempo（clusters 500）：http://192.168.88.50:30201/api/traces/071b34f54c36d31761617fc884567f03  
error span：`gkxlumen-innov` `Table 'gkxlumenx_dim.industry_cluster_map' doesn't exist`

### 1. US-E7-POL-01c

- 打开 `/policy/search`，智能检索「半导体」。
- GET search 200，`items=6` `total=47051`，非 5xx。
- 卡片可见；正文无「加入对比篮」「深度分析」。

### 2. US-E7-POL-01 / 05（页内集群→L0，不强制篮）

- 空配置：「开始分析」disabled，「尚未选择分析对象」；无「去产业查询」主按钮；空点不 POST Create。
- 时序三维默认全开（发布时间 / 效力层级 / 支持力度）。
- 集群目录：`GET /topic/v1/meta/industry-clusters?include_l0=true` **500**。页上产业 placeholder =「无相关产业数据」。catalog 降级短码全部过不了图上 VID 规则。
- **不是**篮路径；本条按总控现行 §4 只验页内直选。

### 3–4. 时序 / 区域 wait_view

- URL `object_ids[]=INB170101` 时图上 VID 文案出现（C1-FP 的 `toPolicyGraphVid` 已在 006d186d 生效）。
- I2-12：切条件 **未**自动 POST（空配置 force 点击计数 0）。
- `canGenerate` 仍假：`scopeReady` 要 `clusterId`，clusters 500 / 无映射 → hint「尚未选择分析对象」。
- Create 未发 → **不能**用首轮明文指纹当本叶复现。Job 未 succeeded → 按总控 **红**。

### 5. US-E7-POL-04

- 「一级权重 100%，可开始分析。」绿条出现；QPOL-02 角标可带。
- 三维「该维核心指标 Java 实包为空」。开始分析仍 disabled（同无集群）。任务未跑通。

## I2-12

| 条 | 结果 |
|----|------|
| 切条件不自动起任务 | **观察到**：空配置 force 点击未 POST |
| 条件栏「开始分析」 | **有** `data-testid=policy-start-analysis`；本轮 disabled |
| 同用户同条件一条在跑 | **未验到**（Create 未发） |
| 当天已成功直接打开结果 | **未验到** |
| 「重新分析」force | **未验到** |

## 问题清单

- 主 C5：`gkxlumen-innov` 读 `gkxlumenx_dim.industry_cluster_map` 表不存在 → clusters 500 → 页内无可用 L0。
- 连带 C1 FE：VID 已形成仍要求 clusterId，开始分析 disabled。
- SHA-256 Create 闸 **本轮未跑到**（006d186d 含 C1-FP 修，但无 POST 证据）。
- 残差：登录仍 mockLogin。`e2e:chain-gold` 26205 **不是**本叶。

## 修改内容

- 无业务仓代码变更。仅本 handoff + 缺陷包 + evidence 手跑脚本。

## 测试结果

- Playwright 对 http://192.168.88.50:30892：**#1 PASS，#2–#5 FAIL**。
- 健康体 30899 policy health 200。
- 手跑记录：`evidence/LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01/run-notes.json` · `policy-gold.spec.ts`

## 遗留风险

1. clusters 修好后 Job 仍可能 freeze failed → 仍红。
2. catalog 短码（`INB1303`）永远过不了图上 VID；L0 必须是 `INB`≥6 或 `chain:INB…`。
3. `e2e:policy-gold` CI 仍未绿；复测继续手跑 30892。

## CI/CD（必填）

- 分支：未改业务仓
- commit：orchestration 本叶 handoff（见 git）
- pipeline：未触发业务仓 CI（QA 不改代码）
- 部署 namespace：`dev`；镜像 `gkx-lumen-topic:006d186d` · `gkxlumen-topic-policy:7d12b8dd` · `gkxlumen-topic-async-service:7d12b8dd` · `gkxlumen-entan-py-api:ea3acc39`
- K8s rollout：E0 C1ROLL 已把前端滚到 006d186d；本单未再滚
- dev 测试 URL：http://192.168.88.50:30892 ；网关 http://192.168.88.50:30899

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-innov` / `gkxlumen-gateway` / `gkxlumen-topic-policy-biz`
- traceId：search `1f319c98e38090efc675d90a448cf8df`；health `374a933df17559351f2bc9ccf535c56d`；clusters 500 **`071b34f54c36d31761617fc884567f03`**
- Tempo / Loki：Tempo API 200，batches=6，error 如上

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | 通过。QA 未改算法 |
| 2 调用链 前端→Java REST→Python `/internal/*` | 通过。health python `/internal/policy`；本叶 Create 未发，未到 Python Job |
| 3 图谱 Nebula | 通过。VID 规则仍要 `chain:INB…`，未直连 nGQL |
| 4 可观测 | 通过。`X-Trace-Id` / Tempo |
| 5 CI/CD | N/A（本单不改业务仓） |
| 6 demo2 merge | N/A |
| 7 共享聚合核心 | N/A |
| 8 数据策略 ADS | 部分：search 经 Java 有实包；clusters 打正式 `gkxlumenx_dim` 缺表 |
| 9 D8 Design | N/A（不改 UI） |
| 10 D9 血缘 | N/A；#5 QPOL-02 角标在评审块 |
| 11 D10 交互 | 部分：wait_view 因未 Create 未跑到 |
| 12 D12 demo/lumen 隔离 | 通过。只认 30892 / 30899，无 demo-* 服务 |

## cost 四字段（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 360000 |
| model_used | grok-4.6 |
| actual_cost | 1.94 |
| cost_warn | green |

口径：`budget-estimate.md` §8.2，B 档 in $3/M out $15/M，qa 默认 in/out=80/20。`source: estimate`。未超 $5。

## 涉及文件

- `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01.md`（本文件）
- `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01-defect-pack.md`
- `agent-delivery/agent-handoffs/政策模块-E7/evidence/LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01/`（spec + run-notes）
