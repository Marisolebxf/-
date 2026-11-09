# TS-L2-DS06 深圳创新监测 · 演示样本循环（LOOP）计划

> 依据：`产品实现规程.md` §6.5（含 §6.5.7）。用例真源：`../合规演示用例/TS-L2-DS06-合规演示用例.md`（24 行零缺格，2026-11-07 M2/M3 已填、human:李伟 审核通过）。
> 验收单：`TS-DS06-DEMO-ACCEPT-LOOP`。监管人：human:李伟。

## 状态行（每轮回写）

| 轮次 | 日期 | 探测 | 对得上 | 缺口 | 子任务 | 结论 |
|---|---|---|---|---|---|---|
| R1 | 2026-11-08 | indicator-systems 200（periods=27） | 17/18 对得上；134 跨城对比 R1 返回 count=0（align 11-07 23:57 有 18 点，下游持续无数据） | 0（无缺口；134 签收复核仍 0，深圳本地 27 期趋势可演，非演示阻塞） | — | **已闭环（R1 17/18+签收复核 3 行，已签收 done）** |

## 1. 探测（每轮第一笔，只读）

- `POST {网关}/display/v1/situation/shenzhen-innovation/indicator-systems`，body `{"cityCode":"CN-4403"}`，头 `Authorization: Bearer <本机 token>` + `systemCode: display`。
- 网关 `http://10.50.69.111:30895`。token 读 `%USERPROFILE%\.gkx\display-loop-token`，不打印。
- **熔断**：401/424 → 验收单 blocked、通知 human:李伟、停止；404 → 「接口映射不存在」停止。200 才进对照。

## 2. 用例集（R1 全量对照，18 行可演+部分可演）

覆盖表中「数据情况」为可演/部分可演的 18 行逐行对照，判定以各行「期望输出」为准。要点：

| 行 | 内容 | 判定要点 |
|---|---|---|
| 112 | 创新载体·多层级地理展示（部分可演） | district 8 区分布真实（南山 17/福田 11/龙岗 11/光明 3/罗湖 3/宝安 2/盐田 2/坪山 1），level/street 空按「暂无下级载体」 |
| 113 | 创新载体·载体详情查看（可演） | 深圳大学 papers=21,482/cited=491,794/talent=3,318；funding 明示混合口径 |
| 114 | 创新价值排名（部分可演） | technologyPowerRank 真实：深圳大学 35/南科大 58；innovValue 无源 |
| 116 | 载体筛选与搜索（部分可演） | type 8 类真实；keyword 走 name；domain/value 无源 |
| 117 | 载体对比分析（可演） | ≥2 勾选，paperCount/citedByCount/talentCount/projectCount/technologyPowerScore 真实 |
| 118 | 指标体系展示（部分可演） | 5 baseIndicators + 27 期 2000–2026；三级树/calcMethod 无源 |
| 119 | 多维度指标（部分可演） | 仅 5 维有数；期刊/专利/专家学者/会议/课题/资金/政策/基础设施 8 维按「暂无数据」 |
| 120 | 指标可视化（可演） | 4 类图切换数据点数=27 期不变 |
| 121 | 指标时间趋势（可演） | 深圳大学 2020–2025 papers 1487→5481；patentCoverageLastYear=2022 滞后口径；projectCountAvailable=false |
| 122 | 指标对比分析（可演） | 5 指标 ≥2 勾选；论文/被引/人才 3 序列齐 |
| 123 | 指标详情（部分可演） | 27 期趋势真实；calcMethod/unit/yoy 显示「—」，暂无解读 |
| 124 | 领域热力图（部分可演） | 15 集群 paperCount 真实；clusterPoints 无源→热力图不可演，只演集群柱/饼 |
| 125 | 领域筛选（可演） | 15 集群 id/name/groupName 真实，切换联动 |
| 127 | 领域详细指标（部分可演） | topicCount/paperCount/citedByCount/percent 有源；enterprises/patents/rdInvestment/talents 4 项「无数据」 |
| 129 | 城市选择（可演） | 20 国内城市真实；国际城市覆盖不到 |
| 130 | 科技指标对比（部分可演） | 5 项真实计数（北京 papers=119,285）；研发投入/专利数量/高新企业数 无源显示「—」 |
| 134 | 趋势分析（可演·历史段） | 3 城×6 年=18 点 5 指标齐；无预测端点→不画延伸虚线 |
| 135 | 报告生成（部分可演） | 端点在线 200，但当前条件「报告内容为空」业务失败→按此口径讲，不演示成功下载 |

- **覆盖不到 6 行（115 订阅/126 空间分析/128 分析建议/131 排名/132 竞争力/133 建议）**：不判、不建补数单（需求未排期，非缺陷），登记待开发。
- 演示口径：数据源为久新 Doris `gkx_technology_analysis_dev`，经 gkx_show_service 只读通道；经费混合口径真实覆盖率仅 1.3%–3.2% 必须明示。

## 3. 判定与退出

同 DS-03 计划 §3：全过 → 状态行回写 → **需规核对（签收前必做，对照 SRS 深圳创新监测 24 行一条不漏）** → 等监管人「签收」（再校验一次通过 → 验收单 done）；有缺口 → DATA/QUERY/ALGO 分类建子任务到 ready，等「可以派了」；只读不签发；同页同条件单飞。

## 4. 已知记录

- **经费混合口径**：fundingRealCoverageRate 仅 1.3%–3.2%（2026-11-07 实测），演示台词须明示。
- **专利数据滞后**：`patentCoverageLastYear=2022`，2023 起 patent_count 恒为 0 是覆盖滞后非产出归零，禁止讲成「深圳专利归零」。
- **项目数无源**：`projectCountAvailable=false`，年度表无项目数，按「—」讲。
- **operation-timeline 诚实空态**：benchmark_manual_pack 假数据已停用，total=0 是设计行为，不判缺口。
- **分析/建议/订阅/竞争力/排名 6 行覆盖不到**：后端无端点，需求未排期，不建子任务，登记待开发；连续两轮仍在 → 交监管人（§6.5.7 步 9）。
