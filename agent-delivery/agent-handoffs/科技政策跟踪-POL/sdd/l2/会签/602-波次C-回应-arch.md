# 602 · 波次 C · 架构回应

身份：arch-agent。只改了 `sdd/l2/POL-L2-PC1-CLEAN-ARCH.md`。未改 API、数据、指标、说明书、Storage。

## 采纳

- ARCH-C1：采纳。第 2 节调用链、时序图，并改了文首、第 5、8、9 节里仍写成 display 直转 Python 或表名另定的句子。浏览器仍只打 display。display 只调 element，不直连 Python，不直连库。候选和五条由 element Feign 新建的只读内部路由。不复用 `RemotePolicySyncClient`，不打 demo 服务。准确性仍由 element 只读 `policy_accuracy_demo`。
- ALG-1：采纳。第 7 节。页眉库内政策数的 `metric_id` 仍是 `M_POLICY_TOTAL_COUNT`，D4 保持 mock。`results` 里的计数不得写成已经接入，也不得替代本批条数。
- ALG-3：采纳。第 7 节。清洗页从 `results` 只取页眉这个数。`qualityAgg` 不进 602 的批次明细，不再挂 `M_POLICY_VALIDITY_RATE`。
- 本批状态：采纳。第 4 节。能判定的都过了、没有失败样例 = 成功。既有过的也有失败样例，或者有的能判定、有的仍无加工事实 = 部分。能判定的都带失败样例 = 失败。读取失败和无加工事实不占用这三句。只写进流程，不展开成算法。

## 见数据回应

- ARCH-C2：见数据回应。
- ARCH-C3：见数据回应。
- ARCH-C4：见数据回应。
- ARCH-C5：见数据回应。
