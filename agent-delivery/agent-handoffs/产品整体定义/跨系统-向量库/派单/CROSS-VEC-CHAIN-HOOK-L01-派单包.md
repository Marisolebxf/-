# 派单包 · CROSS-VEC-CHAIN-HOOK-L01

```yaml
task_id: CROSS-VEC-CHAIN-HOOK-L01
dispatcher: agent:coordinator-agent
suggested_supervised_by: human:唐绍祖
collaborators: data-agent
claim_type: coordinator_dispatch
date: 2026-09-10
status: backlog
ponytail: full
```

## 1. 范围 / 不做

**做**：产业链灌数管线在 **DWD 链表 + 上图 VID 稳定之后** 调用一次 `embed/rebuild`。失败/未稳则跳过。

**不做**：逐行 embed；政策/企业 reload 调 rebuild；改 `amcpdp-*`；Job A enrich（另叶）。

用语：灌链 / 刷链 / 链上图。不要叫「政策重灌」。

夜班位置：本叶 rebuild **最早**（VID 稳定后）；再重灌 → Job A → Hang。

## 2. /goal

```text
/goal algorithm-agent
身份：资深 Python 算法工程师。
强度：ponytail full。
图：必含 02 §1.1 建库切面（挂钩只能出现在灌链末段）。
任务：CROSS-VEC-CHAIN-HOOK-L01
仓库：${GKX_ROOT}/repos/lumen-algo-py
依赖：CROSS-VEC-PY-INDEX-L01
目标：灌链成功且 VID 稳定 → 一次 rebuild；否则 skip 并打日志。
验收：handoff 附 industry_index_version；grep 政策 reload 路径无 embed/rebuild。
commit：[agent:algorithm-agent]；push origin/dev。
```
