# IA-SVCCHAIN-RECOMMEND｜机构招引培育 信息架构

> **版本**：v1.0-r3（移除 US-05 / F-SVC-REC-04 收藏，对齐 bid-reference）
> **registry**：TOPIC-SVCCHAIN-R2  
> **本轮决策（Q068 · P7）**：产业上下文 = 15 个产业集群。任务 `CHAIN-INDUSTRY-CLUSTER-SUPP-L01`。

## 1. 模块目标与边界

- 目标：招引/培育两套推荐模型可见可调 → 名单生成（评分/排名/理由或建议）→ 输出（导出/入篮）。
- 不做：链路/图谱/深圳对比（ECOSYSTEM）；机构集合技术力评估（R1，本叶子只"送入"）；任何真实模型推理（演示口径，Q-SVCCHAIN-05）；名单行内收藏/关注名单（招标未要求，v1.0-r3 废止原 F-SVC-REC-04）。

## 2. 对象模型

| 对象 | 关键字段 | 来源 |
| --- | --- | --- |
| 外部候选机构 `ExternalOrgCandidate` | id / name / city / 四指标分（industryFit(按产业) / techLead / growth / cooperation） | `serviceRecommendData.ts`（确定性 mock，独立于 R1 在库机构） |
| 本土候选机构 = R1 `ServiceOrg` | 复用 `serviceCenterData.ts` 深圳在库机构 + 培育四维度分扩展表 | `serviceRecommendData.ts` 扩展映射（org_id 对齐 R1） |
| 招引模型配置 `AttractConfig` | weights{4} | store 持久化 |
| 培育模型配置 `CultivateConfig` | weights{4} / orgTypes[] / stages[] | store 持久化 |

## 3. IA 结构与 Frame

```text
/service-center/recommend（F-SVC-REC-01 页面壳）
├── 上下文条：产业方向选择（招引/培育共享）+ 页签（attract | cultivate）
├── Tab attract（F-SVC-REC-02 招引）
│   ├── 模型配置区（四指标权重 + 归一 + 复位）
│   └── 名单结果区（排名表 + 推荐理由 + 导出）
├── Tab cultivate（F-SVC-REC-03 培育）
│   ├── 模型配置区（四维权重 + 类型/环节筛选）
│   └── 名单结果区（排名表 + 建议展开行 + 画像下钻 + 入篮 + 导出）
└── OrgProfileDrawer（F-SVC-05 复用 R1，CT-SVC-ORG-02）
```

## 4. URL 契约

| 参数 | 值 | 语义 |
| --- | --- | --- |
| `tab` | `attract` \| `cultivate` | 当前页签（缺省 attract，非法或遗留 `watchlist` 回落 attract） |
| `industry` | 产业方向 id | 分享恢复；非法回落默认并 Message |
| `org` | 本土机构 id | 打开画像抽屉（仅 cultivate 语境；非法清参数 + Message） |

权重/筛选不入 URL（本地持久化，`topic-svc-recommend`）。

## 5. Frame 职责

| Frame | 职责 | 主要组件 |
| --- | --- | --- |
| F-SVC-REC-01 | 页面壳、页签路由、产业方向上下文 | PageShell + Radio/Select |
| F-SVC-REC-02 | 招引模型 + 名单 | WeightEditor / RankTable / ReasonCell |
| F-SVC-REC-03 | 培育模型 + 名单 | WeightEditor / FilterGroup / RankTable(展开行) |
| F-SVC-05 | 机构画像（复用 R1 `OrgProfileDrawer`） | — |

> **废止**：原 F-SVC-REC-04（收藏管理）于 v1.0-r3 移除，对齐 bid-reference 7.6.2/7.7.2。

## 6. 数据与服务边界

- 演示态：全部数据来自 `src/app/pages/service-center/serviceRecommendData.ts` 确定性 mock + `serviceRecommendModel.ts` 纯函数计算（评分/排名/理由/建议）；无网络请求。
- 目标态：名单生成由 Java REST 聚合（gkxlumen-topic），推荐模型推理在 Python `/internal/*`（架构铁律 1/2）；前端仅消费。
- 综合分等指标 D1=draft（模型口径未拍板，Q-SVCCHAIN-05），D4=mock；徽章经 `SvcMetricBadges` 消费 `serviceReadinessSeed.ts` 新增条目。

## 7. 复用契约

| 契约 | 内容 |
| --- | --- |
| CT-SVC-ORG-02（既有） | 培育名单行下钻复用 R1 `OrgProfileDrawer`（props：orgId + onClose；数据自取） |
| CT-SVC-ORG-03（R2B 新增） | 培育名单行"加入对比篮"写系统篮 `service_org` 类型（复用 `CompareBasketProvider.addItem`），对比分析由 R1 页承接分发 |
| CT-SVC-ECO-02（既有） | 与 ECOSYSTEM 共享 `serviceCenterData.ts` 机构/环节基础数据，不复制 |

## 8. 指标登记（摘要，详见 TRACE）

`M_SVC_REC_ATTRACT_SCORE`、`M_SVC_REC_CULTIVATE_SCORE`、`M_SVC_REC_CANDIDATE_CNT` ×2 —— 全部 D1 draft / D4 mock，⚠️ Q-SVCCHAIN-05。
