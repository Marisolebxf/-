# D12 lumen-topic-py · 长任务总控（无人值守）

> **日期**：2026-08-14  
> **授权**：`human:淮政玮`（本管线监管人；后续认领 **不必再问**）  
> **目标**：闭合 D12-DEBT-TOPIC-PY：新建 `lumen-topic-py`，Java 企业检索/AI 不再打 `demo-platform-search-py`  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)。三叶串行；执行 agent **按本文件已拍板项继续**，禁止把「等用户」当默认阻塞。

| 叶 | 仓 | 任务 | 门 |
|----|-----|------|----|
| 1 | `lumen-topic-py` | `DEVOPS-LUMEN-TOPIC-PY-L01` | D12 **done** 后 ready |
| 2 | `lumen-topic-py` | `PY-LUMEN-TOPIC-PY-PORT-L01` | L01 **ready_to_sign** 即可开工（同仓连续） |
| 3 | `lumen-svc-platform` | `API-LUMEN-TOPIC-PY-CUTOVER-L01` | L01+L02 代码已在 dev |

厚包：[派单条](./D12-LUMEN-TOPIC-PY-派单条.md) · 决策 `DECIDE-D12-LUMEN-CALLCHAIN`

---

## 1. 无人值守规则

1. **监管已授权**：`supervised_by=human:淮政玮`，`claim_type=pull`。升 ready 后直接认领开工。  
2. **已拍板不回问**：仓名=`lumen-topic-py`（禁止 `lumen-svc-topic-py`）；禁止只改 GitLab 名；禁止并进 `lumen-algo-py`；`demo-svc-topic-py` 保留。  
3. K8s：`gkxlumen-platform-search-py` / `ai-py` / `ai-worker`。镜像：`gkxlumen-search-service` / `gkxlumen-ai-service` / `gkxlumen-ai-worker`（禁止覆盖 demo 的 `gkx-search-service` tag）。  
4. OTel：`http://gkxlumen-platform-otel-collector:4318`。算法厨房：`http://lumen-platform-algo-py:8000`。  
5. 本管线不改 `demo-svc-topic-py`。  
6. git：lumen 仓只推 `origin/dev`。禁止 force。commit `[agent:<role>]`。  
7. 每单 handoff + `ponytail: full` + cost 四字段。签收 `ready_to_sign→done` 可积压。  
8. 卡住只允许：GitLab 无权限建仓、K8s/Harbor 不可达。本地仓与清单仍要交。

锁：长任务 `lock_hours=24`。

---

## 2. 开工顺序

1. 认领并做完 **DEVOPS**（复制树 + 改名 + CI/K8s + 尽量 push）。  
2. 认领 **PY-PORT**（settings / 内部 URL 切 lumen；冒烟测试）。  
3. 认领 **API-CUTOVER**（Java helm/Nacos 切 `gkxlumen-platform-search-py`）。

---

## 3. 执行记录（2026-08-14 无人值守）

| 叶 | 状态 | 证据 |
|----|------|------|
| DEVOPS | **done** | GitLab project **275**；commit `5d20411`；pipeline [5026](https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5026) 全绿（含 3 deploy） |
| PY-PORT | pending_test | 同 commit；本地 pytest 83 pass；handoff `PY-LUMEN-TOPIC-PY-PORT-L01.md` |
| CUTOVER | **integration** | Java `1ceb8e3`；pipeline [5027](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5027) helm/enterprise/async **success**；网关 filters **200** |

