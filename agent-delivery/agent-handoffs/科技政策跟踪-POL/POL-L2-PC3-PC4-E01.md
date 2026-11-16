# POL-L2-PC3-PC4-E01 · 金路径

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| 状态 | `in_progress`（本叶只写交接，不改 task-registry） |

QA 不改业务代码。

## 发布核对

点名提交：前端 `b7fea01fe25c037edace2b6c087d5f57c61fa6e3`，Java `700f0079fb5505011bfbee7a4ca229e0e1d84225`，算法 `9a784b42446960e1c398f3ba24f5754803b942cc`。

| 仓 | 点名提交的发布作业 | 此刻已发布 |
|----|--------------------|------------|
| lumen-ui-science-pc | 流水线 5701 `deploy:k8s` 成功，镜像 `gkx-lumen-pc:b7fea01f`，当时 rollout 成功 | **不是**。其后流水线 5702（`14228e6d7e92`）`deploy:k8s` 已成功。`http://10.50.69.111:30891/` 的入口脚本已从 `/assets/index-Bl21T2qg.js` 换成 `/assets/index-CqE_R8Bp.js`。流水线 5703 仍在构建，尚未 deploy |
| lumen-svc-platform | 流水线 5700 `deploy:display` 成功，`gkxlumen-platform-display` rollout 成功，短 SHA `700f0079` | 仍是这次。dev 上更新的成功 `deploy:display` 没有出现 |
| lumen-algo-py | 流水线 5698 `deploy:api`、`deploy:worker` 成功，短 SHA `9a784b42` | 仍是这次。dev 上更新的成功 `deploy:api` 没有出现 |

**发布未绿。** 展示 dev 已发布前端不是 `b7fea01`。下面四行不把已打开页面算通过。

## 金路径

实际打开过：`https://edu.itic-sci.com/tid/policy/policy-compare-upgrade`（NodePort 文档地址 `http://10.50.69.111:30891`，gitlab-ci `environment.url` 与 `k8s/lumen-pc.yaml` NodePort 30891）。发布门未绿，四行都记红。

| # | 结果 | 地址 |
|---|------|------|
| 1 运行对比 | 红。发布未绿 | `https://edu.itic-sci.com/tid/policy/policy-compare-upgrade` |
| 2 查看报告 | 红。发布未绿 | 同上 |
| 3 PDF / Word | 红。发布未绿 | 同上 |
| 4 侧栏 | 红。发布未绿 | 同上 |

## 架构合规

未改业务代码，未改 `task-registry.yaml`，未调 task-registry 写工具，未重发 Nacos。
