# POL-L2-PC3-PC4-E01 · 金路径

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| 状态 | `in_progress`（本叶只写交接，不改 task-registry） |

QA 不改业务代码。

## 发布核对

上一轮只因已发布前端不是 `b7fea01`，四行都记了发布未绿，没有点「运行对比 / 查看报告 / 导出 / 侧栏」。

本轮点名提交：前端 `c712ae6fda2a173767c9933c0fd95d2c631b11b2`（过程壳 `14228e6d7e92` 已含在这之后），Java `700f0079fb5505011bfbee7a4ca229e0e1d84225`，算法 `9a784b42446960e1c398f3ba24f5754803b942cc`。

| 仓 | 点名提交的发布作业 | 此刻已发布 |
|----|--------------------|------------|
| lumen-ui-science-pc | 流水线 5703 `deploy:k8s` 成功，镜像 `gkx-lumen-pc:c712ae6f`，rollout 成功 | 是。dev 上没有更新的流水线。`http://10.50.69.111:30891/` 入口脚本为 `/assets/index-CvHY9g7P.js`，对比页块含过程壳四步和政策名槽 |
| lumen-svc-platform | 流水线 5700 `deploy:display` 成功，短 SHA `700f0079` | 仍是这次。dev 上更新的成功 `deploy:display` 没有出现 |
| lumen-algo-py | 流水线 5698 `deploy:api`、`deploy:worker` 成功，短 SHA `9a784b42` | 仍是这次。dev 上更新的成功 `deploy:api` 没有出现 |

发布门已绿。下面四行按已发布页实点。

## 金路径

实际打开过：`https://edu.itic-sci.com/tid/policy/policy-compare-upgrade`（NodePort `http://10.50.69.111:30891`）。地区选广东省，效力级别选市级，对比对象为珠海固态电池行动方案与深圳新型储能规划。刷新后槽里是这两份政策名，不是 `cn-zh-3840797` 与 `SYN2026111046a36ecf4c`。

| # | 结果 | 地址 |
|---|------|------|
| 1 运行对比 | 红。过程壳出现「读取所选政策、核对结构化与拆解、生成对比与研报、呈现结果」，随后页面写「这次对比没有写出来，可稍后重试」。没有四类识别、对比表、柱状图、雷达图、知识图谱、摘要、结论 | `https://edu.itic-sci.com/tid/policy/policy-compare-upgrade` |
| 2 查看报告 | 红。记录 `5ad8bcba9fae419e835ae2f3fed6a662` 为已完成。点「查看报告」后研报页动态块 `index-DIjhgILw.js` 返回 404，仍停在对比记录，没有深度四块、四类洞察、各章、双向溯源 | 同上 |
| 3 PDF / Word | 红。研报页没有打开，「导出 PDF」「导出 Word」点不到 | 同上 |
| 4 侧栏 | 红。侧栏没有「智能研报生成」，对比页高亮「多维政策对比」。研报页没有打开，没有停在研报页上的高亮 | 同上 |

## 架构合规

未改业务代码，未改 `task-registry.yaml`，未调 task-registry 写工具，未重发 Nacos。任务未改为 done。
