# Pipeline / 本地构建验收暂缓 · PM 决策（2026-06-20）

## 决策（v2 修订）

**略过** GitLab Pipeline、K8s rollout、dev URL 冒烟、**以及本地 `mvn package` / `npm run build`**。

Wave 0 快路径 **仅要求：代码完成 + git push + handoff**。

| 项 | 值 |
|---|---|
| 决策人 | PM（用户确认） |
| 日期 | 2026-06-20 |
| v2 修订 | 本地 mvn/npm build 一并 defer |
| 范围 | `gitlab_pipeline_*`、`k8s_rollout`、`:30891/:30892`、`mvn package`、`npm run build`、`py:smoke` 本地跑 |
| **仍必做** | 功能代码移植、commit 含 `[agent:*]` + task-id、**git push**、handoff 文件 |
| 补验 owner | qa-agent + devops-agent（E-PLATFORM-P0-L06 / E-INNOV-M1-L10 / E-PLATFORM-P0-L08） |
| 关联事件 | `INCIDENT-2026-06-18-k8s-dev-nfs-storage.md` |

## 适用任务

| 类型 | defer | 放行条件 |
|------|-------|----------|
| Java backend（L03/P0-L02/P0-L05…） | mvn package、backend:build | push 到 feature 分支 |
| Python algo | py:smoke 本地、deploy:innov-py | push |
| 前端 | npm build、deploy:k8s | push |
| 里程碑签收 L10/P0-L08 | — | **不可 waive**，必须补全矩阵 |

## coordinator 派单话术追加

> PM pipeline waiver v2：**禁止**为等 mvn/npm/CI 而阻塞；完成移植 → handoff → push 即视为 leaf 可签收（`pipeline_deferred: true`）。
