# DEMO-SVC-ABORT-L01 · 范围 3 停机（revert + 清 Demo 切片 + 删 storage/SVC + 停 topic-svc）

> 日期：2026-08-18  
> Task：`DEMO-SVC-ABORT-L01`（chore）  
> 总控：[`DEMO-SVC-ABORT-停机总控.md`](./DEMO-SVC-ABORT-停机总控.md)  
> 路径表：[`DEMO-SVC-停机转交-侯佳伟.md`](./DEMO-SVC-停机转交-侯佳伟.md) §4  
> 本机会话：`human:侯佳伟` 电脑 · `claim_type=coordinator_dispatch` · lock 24h

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 混改 SHA 不整单 revert；只删/改 SVC 路径；CHAIN 页/Job/helm 发布门不动；未用 YAGNI 跳过 handoff / 调用链 / D12 / 可观测卸挂 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 跨仓 git revert + 清库，未挂 compress |

## 范围与实现

① 旧叶废作：coordinator 已完成（69 叶），本叶不改旧施工叶状态。  
② 按仓路径正向提交（revert / 拆文件），已 push `origin/dev`。  
③ TRUNCATE 仅 Demo DWD `service_org*` + ADS `svc_*`。  
④ 删除 `agent-delivery/data/data-design/storage/SVC/`。  
⑤ 代码/CI/Helm 已停 `topic-svc` 发版；**K8s 实停与 Nacos 清 `/svc` 路由待人工点 `helm:chart`**。

禁止项本叶均遵守：无 force / 无整仓 reset；未碰 `storage/CHAIN` · `gkxlumen-topic-chain` · `views/chain.py`；未 DROP `demo_gkxlumenx_ods` 33 表；未写正式 `gkxlumenx_*`；未派旧 C/D；未开新 A 总控。

## 偏离说明

| 项 | as-built |
|----|----------|
| 非 `git revert <sha>` 整单 | 混改 SHA（Java `8d846a5` 后叠 CHAIN helm/CI；UI 与 CHAIN 共改 router/perms/search）改为 **拆文件 + 正向删改**，效果等价 revert SVC 路径 |
| `lumen-topic-py` | 仓已 clone；`gkx_svc_service` 已在 `origin/dev`（`feat/svc-middle-boot` 已合入），本叶卸挂载 |
| Helm `topic-svc` 键 | `values.yaml` **保留** `topic-svc.enabled: false`（upgrade 才能从 release 卸已有 Deployment）；`values-lumen.yaml` 去掉 enable |
| ⑤ K8s | 本机 `kubectl` 无 context，`helm:deploy` 在 `origin/dev` 为 **manual** → 卡点，不改 chain helm |

## 产物清单（各仓 SHA）

| 仓 | SHA | 说明 |
|----|-----|------|
| `gkx-orchestration` | `9281a16` | 删 `storage/SVC/`；`storage/README.md` 去现行 SVC；服务机构 README 改历史对照 |
| `demo-algo-ent-analysis` | `45c5745` | 删 `entan/svcseed.py` · `api/svc_routes.py` · SVC 脚本/测试；保留 ENT / polan |
| `lumen-topic-py` | `2e182b9` | 整包删 `gkx_svc_service/` + `tests/test_gkx_svc_*.py`；search 卸挂；Dockerfile.search 去 COPY |
| `lumen-algo-py` | `6675192` | 删 `views/svcan.py` / `svcan/` / `test_svcan_boot.py`；`main.py` 去 include；**保留 `views/chain.py`** |
| `lumen-svc-platform` | `929411e` + `325bdce` | 整模块 `gkxlumen-topic-svc/`；父 POM；CI `backend:image:topic-svc` / `deploy:topic-svc`；gateway `/svc/**`；async 仅 SVC Job 白名单；`topic-svc.enabled=false` |
| `lumen-ui-topic` | `4f923e3` | 删 `service-portal/**` · `service-center/**`（含 `ServiceChainAnalysisPage`）· `api/svc/**` · SVC utils/mock；router 只去 SVC；产业链页保留 |

未 clone：无（`lumen-topic-py` 已在 `${GKX_ROOT}/repos/lumen-topic-py`）。

CHAIN 冲突处理：未整仓 reset；与 `LUMEN-CHAIN-E-CI-PLAYWRIGHT-L01` 同仓只动 SVC 路径。CHAIN 指标 `industryWorkspace.ts` 的 `service_org` / 产业中心页 **未动**。CHAIN 同事请 `git pull --rebase origin dev`。

## ③ 清库结果（仅 Demo）

连接：NAT 主机 `111.198.38.90:34306`（用户名见本机 `.env.local`，**密码不入库**）。未写正式 `gkxlumenx_*`。未 DROP ODS。

### `demo_gkxlumenx_dwd` · `service_org*`

| 表 | before | after |
|----|--------:|------:|
| `service_org` | 59 | 0 |
| `service_org_chain_rel` | 59 | 0 |
| `service_org_financing` | 0 | 0 |
| `service_org_financing_legacy_pre_svc` | 17 | 0 |
| `service_org_legacy_pre_svc` | 50 | 0 |
| `service_org_org_rel` | 9 | 0 |
| `service_org_type_tag` | 59 | 0 |

### `demo_gkxlumenx_ads` · `svc_*`

| 表 | before | after |
|----|--------:|------:|
| `svc_chain_gap_score` | 3 | 0 |
| `svc_global_dist` | 5 | 0 |
| `svc_industry_layout` | 6 | 0 |
| `svc_invest_stat` | 2 | 0 |
| `svc_metric_dist` | 7 | 0 |
| `svc_metric_fact` | 2 | 0 |
| `svc_metric_series` | 8 | 0 |
| `svc_new_org_stat` | 12 | 0 |
| `svc_org_profile_card` | 59 | 0 |
| `svc_rec_ranking` | 56 | 0 |
| `svc_region_dist` | 13 | 0 |
| `svc_sz_dist` | 3 | 0 |
| `svc_sz_scale` | 1 | 0 |
| `svc_tech_power_score` | 35 | 0 |

`demo_gkxlumenx_ods`：**SKIPPED**（33 张约定表未 DROP、未 TRUNCATE）。

## ④ storage/SVC

已删整个 `agent-delivery/data/data-design/storage/SVC/`（S1–S4 一并）。`storage/ENT` · `storage/CHAIN` 未动。产品定义 E7 未动。停机总控 / 废作 registry 未回滚。

## ⑤ 停 topic-svc（卡点）

**代码侧已停发：** CI 去掉 `backend:image:topic-svc` / `deploy:topic-svc`；`helm:deploy` needs 不再依赖该 job；`values-lumen` 不再 enable；网关删除 `Path=/svc/**`；Nacos 种子 `gkxlumen-topic-svc-biz-dev.yml` 已从 chart 删除。

**集群侧未在本机验证：** `kubectl` `current-context is not set`。`helm:deploy` 在 `origin/dev` 为 manual。请 `human:侯佳伟` **微信升级 `human:淮政玮`**：

1. GitLab `lumen-svc-platform` 当前 pipeline 点 **`helm:chart`**
2. 变量 **`FORCE_NACOS_REPUBLISH=true`**（否则 Nacos 仍留 `/svc/**`；upgrade 默认不重灌）
3. 核：`kubectl -n dev get deploy,svc | findstr topic-svc` 应空；**不要**改 `topic-chain` helm / CHAIN 发布门

## 验收证据

- 各仓 `origin/dev` 已含上表 SHA（orchestration 以 push 后 SHA 为准）
- 清库 COUNT after=0（上表）
- `storage/SVC/` 工作区与 git 中不存在
- 本 handoff

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 卸 `svcan` / `gkx_svc_service`；未把算法迁入 Java |
| 2 | 调用链 前端→Java→Python `/internal/*` | ✅ 删除越层 SVC 门面与 `/svc/**`；CHAIN `/chain/**` 保留 |
| 3 | 图谱 Nebula，禁止 Neo4j | ✅ 未引入 Neo4j |
| 4 | 可观测 | ✅ 卸 `gkxlumen-topic-svc-biz` OTEL 服务；CHAIN/async OTEL 保留 |
| 5 | CI/CD push → Pipeline；禁 force | ✅ 只 `git push origin dev`；Java 停 `topic-svc` 发版 job |
| 6 | demo 不污染正式 | ✅ 清库仅 `demo_gkxlumenx_dwd/ads` |
| D12 | lumen 不调 demo-* 服务 | ✅ 卸 SVC 后无 lumen→demo-svc 回落；CHAIN 路径未改 |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | `claude-sonnet-4.5`（会话为 Cursor Grok 4.6，按 B 档公式回填） |
| actual_tokens | 180000 |
| actual_cost | 0.97 |
| cost_warn | green |

## CI/CD

- 分支：各仓 `dev` → `origin/dev`
- Java pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines
- UI pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines
- K8s rollout：⏳ 待 `helm:chart`（见 §⑤）
- namespace：`dev`（未本机核）

## 可观测性

- 已卸 `OTEL_SERVICE_NAME=gkxlumen-topic-svc-biz`
- CHAIN / async-service / algo-py chain 埋点未改
- Tempo 抽样：N/A（模块已下线）

## 遗留风险

- Nacos 旧 `Path=/svc/**` 在 `FORCE_NACOS_REPUBLISH` 前仍可能 404/502 而非「无路由」
- Nacos 残留 DataId `gkxlumen-topic-svc-biz-dev.yml` 无害（无消费进程）
- `search-workspace.css` 已去掉 `.svc-org-search-page` 选择器；对比篮 `service_org` 类型字面量仍在 picker（CHAIN/对比篮共用，未删）
- 旧 `DEMO-SVC-*` / `LUMEN-SVC-*` 施工叶保持废作，**不要标 done**

## 联调确认

联调通过：SVC 路径已从六仓 `origin/dev` 卸除；Demo DWD/ADS SVC 切片已空；`storage/SVC` 已删；CHAIN 模块与发布门未改。**ABORT 代码+清库完成。** 新 A 总控须等本叶 ≥ `integration` **且** helm:chart 卸掉 `topic-svc` 后再开。
