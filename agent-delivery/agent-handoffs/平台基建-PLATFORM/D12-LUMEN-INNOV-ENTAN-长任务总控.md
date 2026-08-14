# D12 lumen-algo-py innov/entan · 长任务总控（无人值守）

> **日期**：2026-08-14  
> **授权**：`human:淮政玮`（本管线监管人；后续认领 **不必再问**）  
> **目标**：闭合 **D12-DEBT-INNOV-PY** 与 **D12-DEBT-ENTAN-PY**：lumen 的 innov-py / entan-py 不再由 demo 仓 CI 热更新、不再使用 demo Harbor 制品名  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)。三叶串行；执行 agent **按本文件已拍板项继续**，禁止把「等用户」当默认阻塞。

| 叶 | 仓 | 任务 | 门 |
|----|-----|------|----|
| 1 | `lumen-algo-py` | `PY-LUMEN-INNOV-PORT-L01` | D12 **done** 后 ready |
| 2 | `lumen-algo-py` | `PY-LUMEN-ENTAN-PORT-L01` | L01 达联调闸门即可（同仓连续） |
| 3 | `lumen-svc-platform` + 两 demo 仓 CI | `API-LUMEN-INNOV-ENTAN-CUTOVER-L01` | L01+L02 镜像已推 Harbor |

厚包：[派单条](./D12-LUMEN-INNOV-ENTAN-派单条.md) · 决策 `DECIDE-D12-LUMEN-CALLCHAIN`

---

## 1. 无人值守规则

1. **监管已授权**：`supervised_by=human:淮政玮`，`claim_type=pull`。升 ready 后直接认领开工。  
2. **已拍板不回问**：
   - 代码进 **`lumen-algo-py`**（`vendor/innov-py` / `vendor/entan-py`），**不**新建 `lumen-innov-py` / `lumen-svc-*`。
   - 禁止 git merge demo→lumen；对照复制后改镜像名。
   - `demo-algo-science` / `demo-algo-ent-analysis` **保留**，只收窄 CI 前缀为 `demo-platform`。
   - K8s 名保持现网：`gkxlumen-platform-innov-py` / `gkxlumen-platform-entan-py` / `gkxlumen-platform-entan-py-worker`（Java 已钉 innov DNS）。
   - 镜像：**`gkxlumen-innov-py`** / **`gkxlumen-entan-py-api`** / **`gkxlumen-entan-py-worker`**（禁止覆盖 `gkx-innov-py` / `gkx-entan-py-*`）。
   - 现有 `lumen_algo_service` / `py:test` compileall **不**把 vendor 整包塞进去。
   - 产业链厨房仍只在本仓正式包；禁止把 chain 从 `lumen-algo-py` 拆走。
3. OTel：helm `commonOtelEnv` → `gkxlumen-platform-otel-collector:4318`。  
4. 切服务 ≠ 切库：MySQL `innov` / `gkxlumenx_*` 本管线不迁（余项见 `API-LUMEN-INNOV-DB-ALIGN-L01`）。  
5. git：lumen 只推 `origin/dev`；demo 仓 CI 收窄推 `origin/main`。禁止 force。commit `[agent:<role>]`。  
6. 每单 handoff + `ponytail: full` + cost 四字段。签收可积压。  
7. 卡住只允许：Harbor/K8s 不可达、GitLab 无权限。本地仓与清单仍要交。

锁：长任务 `lock_hours=24`。

---

## 2. 开工顺序

1. **INNOV-PORT**：对照复制 `demo-algo-science` → `vendor/innov-py`；独立 Dockerfile + CI `image:innov` / `deploy:innov`（只 `set image`，不 apply 对抗 helm 的清单）。本叶不改 helm 镜像名、不改 demo CI。  
2. **ENTAN-PORT**：对照复制 `demo-algo-ent-analysis` → `vendor/entan-py`；`image:entan-api` / `entan-worker` + 对应 deploy。  
3. **CUTOVER**：helm `values.yaml` / `values-lumen.yaml` 镜像改 `gkxlumen-*`；删「可回落 demo-platform-innov-py」；`INNOV_CHAIN_ALGO_BASE_URL` 钉 `lumen-platform-algo-py:8000`；两 demo 仓 `PLATFORM_K8S_PREFIXES` 仅 `demo-platform`；触发 lumen-algo-py deploy + platform helm。

---

## 3. 执行记录（2026-08-14 无人值守）

| 叶 | 状态 | 证据 |
|----|------|------|
| INNOV-PORT | pending_test | `179fe8d` / pipeline 5029 `image:innov` 绿；handoff `PY-LUMEN-INNOV-PORT-L01.md` |
| ENTAN-PORT | pending_test | `ef54caa` / pipeline 5030 `image:entan-*` 绿；handoff `PY-LUMEN-ENTAN-PORT-L01.md` |
| CUTOVER | pending_test | helm `474e98a` job 21627；Python deploy 21647/21648/21649 healthz ok；demo CI 已收窄 |
| DB-ALIGN | ready_to_sign | `API-LUMEN-INNOV-DB-ALIGN-L01` helm `e62230d` python `9a1889a`；lumen 现网 rev 19 已绿 |
| V1-CLOSE | ready_to_sign | `API-LUMEN-ENTAN-V1-CLOSE-L01` python `9a1889a` helm `e62230d` |
| ADS-ISOLATE | ready_to_sign | `API-DEMO-INNOV-ADS-ISOLATE-L01` demo `6f73df7`；jar/JDBC 已上，helm 21724 红在 Nacos hook |
| NACOS-HOOK | ready_to_sign | `DEVOPS-DEMO-NACOS-HOOK-N3-L01` demo `08f6ca9`；待再点 helm:deploy |
