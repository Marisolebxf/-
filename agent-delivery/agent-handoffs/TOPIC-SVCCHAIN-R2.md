# TOPIC-SVCCHAIN-R2 / R2B · 产业服务链 R2（链路生态域 + 招引培育域）+ R2B（检索对齐企业模式 + 对比篮落地）Handoff

> **任务**：TOPIC-SVCCHAIN-R2（范围 A）+ TOPIC-SVCCHAIN-R2B（范围 B，与 R2 合并同批执行）
> **执行**：agent:frontend ｜ **监管**：human:淮政玮
> **日期**：2026-08-05
> **状态**：integration（两任务同推）

---

## 1. 范围与实现（对照 bid-reference）

### 1.1 R2 范围核对（§1.1.1.2.4.2.7.4–7.8）

按招标原文逐级清点，7.4–7.8 共 **10 个三级项**（任务描述称 11 项，实测原文为 7.4/7.5/7.6/7.7/7.8 各 2 项；E7 README 原"17 个三级项"总数亦已更正为 16）。TRACE 反向核对逐条闭合：

| # | 招标三级项 | 叶子 | 落点 | 结论 |
| --- | --- | --- | --- | --- |
| 7.4.1 | 全链路可视化呈现 | ECOSYSTEM | US-ECO-01：6 环节链路图（研发→中试→产业化全周期），环节卡机构数/平均深度，click/Enter 下钻环节详情，URL `segment` 直达 | ✅ |
| 7.4.2 | 瓶颈堵点智能识别 | ECOSYSTEM | US-ECO-02：空白/薄弱/瓶颈三类判定（演示规则），链路图高亮标注 + 识别面板依据行互指；算法未定 → D1 missing 红问号（Q-SVCCHAIN-03） | ✅（演示口径） |
| 7.5.1 | 关系网络构建 | ECOSYSTEM | US-ECO-03：ECharts force 图谱，投资/合作/竞争/人才流动四类关系 × 服务机构/企业/高校/资本四类主体，过滤持久化，确定性数据集 | ✅ |
| 7.5.2 | 图谱探索与统计 | ECOSYSTEM | US-ECO-04：机构节点下钻 R1 同一画像抽屉（同 org_id），聚焦 1 度邻域；网络密度 2E/(N(N-1))、度中心性 TOP5；影响力评分 D1 missing 诚实态 | ✅ |
| 7.6.1 | 招引模型与指标 | RECOMMEND | US-REC-01：产业匹配度/技术领先性/发展潜力/落地意愿四指标调权，归一校验，默认权重可复位（Q-SVCCHAIN-05 ⚠️） | ✅（演示口径） |
| 7.6.2 | 推荐名单生成 | RECOMMEND | US-REC-02：外部候选库加权排序名单（名次/城市/四指标分/综合分/推荐理由），确定性可复现，CSV 导出带演示声明，收藏闭环 | ✅ |
| 7.7.1 | 培育模型与筛选 | RECOMMEND | US-REC-03：本土机构四维度调权 + 机构类型/服务环节筛选持久化，全不选禁用有解释 | ✅（演示口径） |
| 7.7.2 | 培育名单与建议 | RECOMMEND | US-REC-04：深圳本土机构名单 + 短板建议标签/文本（🧪 引用行内数值），下钻画像、行内入对比篮、CSV 导出 | ✅ |
| 7.8.1 | 统一评价框架 | ECOSYSTEM | US-ECO-05：框架说明卡列全部对比指标 + 各自就绪度；"框架口径待甲方确认"声明（Q-SVCCHAIN-04）；服务链完整度 D1 missing 诚实排除 | ✅（演示口径） |
| 7.8.2 | 横向对比分析 | ECOSYSTEM | US-ECO-06：深圳 vs 全国平均/北京/上海/广州柱状图 + 梯队仪表盘 + 结论区，指标多选持久化 | ✅ |

范围外确认：与 R1 叶子（7.1–7.3）无重叠；E7 README 划分表已更新三叶子状态。

### 1.2 R2B 范围核对（用户新口径）

| 要求 | 落点 | 结论 |
| --- | --- | --- |
| 服务机构检索对齐企业检索 | 新增 `/service-center/search` 检索页：复用同一 `SearchScaffold`/`ElementSearchWorkbench` 通用壳（零改动），智能/关键词/高级三模式，服务机构字段库 + 智能解析器为配置层新增；差异点在 R1 UX-SPEC §检索对齐差异表登记 | ✅ |
| 对比篮：任意上下文入篮/移除 | `ServiceOrgBasketButton` 五类触点：检索结果行、R1 集合/覆盖视图、机构画像抽屉、生态图谱环节详情、培育名单行；状态跨页即时一致（系统篮 store 单真源） | ✅ |
| 篮内列表页 + 导入对比分析 + 回跳 | 系统篮 `service_org` Tab 摘掉"开发中"占位，`ServiceOrgCompareBasketPanel` 对齐政策篮（列表/勾选/过滤/移除/清空/分发）；`serviceAnalysisRegistry` 分发"技术力横向对比"（2~5 家）→ R1 评估页 `source=compare-basket&org_ids[]` 自动预选；"返回对比篮"经 `open_compare_basket=1&compare_object_type=service_org` 重开浮层（浮层常驻挂载，关键词/勾选会话内保留） | ✅ |
| 篮内容持久化 | 走系统篮既有 `compareBasketStore` localStorage 机制，`service_org` 类型独立容量与去重 | ✅ |
| R1 自选对比收编，不留两套入口 | `CapabilityView` 对比候选改为**只读系统篮**（本地集合仅作分析工作台语义），篮空显示引导空态；R1 页无绕开篮的第二套对比对象控件 | ✅ |
| R1 五件套同步修订 | USM 增补 US-SVC-ORG-07（检索）/US-SVC-ORG-08（对比篮），US-06 增 AC-06-07/06-08；UX-SPEC 增检索对齐差异表与篮交互章节；TRACE 增 CT-SVC-ORG-03/04 引用 ENT-COMPARE | ✅ |
| 本批内闭环 | 培育名单 → 入篮 → 篮内勾选分发 → R1 技术力对比自动预选 → 返回对比篮，全链路可走通 | ✅ |

## 2. 产物清单

### 2.1 五件套（编排仓 `agent-delivery/agent-handoffs/产品整体定义/E7-产业服务链分析/`）

| 文件 | 说明 |
| --- | --- |
| `README.md`（更新） | 三叶子划分表 + R2B 修订标注 + Q-SVCCHAIN-01..05 索引 + CT-SVC-ORG-03/04 契约摘要；三级项总数更正 17→16 |
| `SVCCHAIN-ECOSYSTEM-服务链生态/`（新增 5 件） | USM（US-ECO-01~06，AC 28 条）/ IA / Wireframe（F-SVC-ECO-01~04）/ UX-SPEC / TRACE（6 项需求逐条正反向核对 + 指标注册） |
| `SVCCHAIN-RECOMMEND-机构招引培育/`（新增 5 件） | USM（US-REC-01~05，AC 21 条）/ IA / Wireframe / UX-SPEC / TRACE（4 项需求 + 指标注册） |
| `SVCCHAIN-ORG-ANALYSIS-服务机构分析/`（R2B 修订 3 件） | USM v1.1-r2b（+US-07/08，US-06 修订）/ UX-SPEC（检索对齐差异表 + 篮交互）/ TRACE（+CT-SVC-ORG-03/04，指标补注） |
| `客户决策清单跟踪表.md`（更新） | 新增 **Q-SVCCHAIN-03**（瓶颈识别算法/专家规则库）、**Q-SVCCHAIN-04**（深圳统一评价框架）、**Q-SVCCHAIN-05**（招引/培育模型口径），均 🟡 |

### 2.2 实现（业务仓 `demo-ui-topic`，origin/dev）

- `acf7f42` chore(build)：pnpm v11 配置迁移（见 §6 风险项）
- `284b681` feat(service)：**29 文件 +4023/−2269**

| 文件 | 职责 |
| --- | --- |
| `serviceEcosystemData.ts` / `serviceEcosystemModel.ts` / `serviceEcosystemStore.ts` | 链路环节/关系边/城市基准确定性 mock；环节统计、瓶颈判定、图谱构建、密度/中心性、深圳对比与梯队计算；tab/field/图谱过滤/深圳指标持久化（`topic-svc-eco`） |
| `ChainLinkView.tsx` / `StageDetailDrawer.tsx` | 7.4 链路图 + 环节下钻（环节机构可入篮） |
| `EcosystemGraphView.tsx` | 7.5 力导图谱：关系/主体过滤、聚焦邻域、统计面板、机构节点下钻 R1 画像 |
| `ShenzhenCompareView.tsx` | 7.8 框架卡 + 指标多选柱状图 + 梯队仪表盘，完整度诚实排除 |
| `ServiceChainEcosystemPage.tsx` | 生态页壳（URL `field`/`tab`/`segment`/`org` 同步） |
| `serviceRecommendData.ts` / `serviceRecommendModel.ts` / `serviceRecommendStore.ts` | 7.6/7.7 候选库与四指标/四维度、加权计算纯函数、CSV 构造、权重/筛选/收藏持久化（`topic-svc-recommend`） |
| `ServiceRecommendPage.tsx` | 招引/培育/已收藏三 Tab 闭环（生成→收藏/导出） |
| `serviceOrgSearchData.ts` / `serviceOrgSmartParser.ts` / `ServiceOrgSearchPage.tsx` | R2B 检索页（企业检索同构，配置层新增） |
| `ServiceOrgBasketButton.tsx` / `ServiceOrgCompareBasketPanel.tsx` / `serviceAnalysisRegistry.ts` | R2B 入篮触点 / 篮内面板 / 分析分发注册表 |
| `EnterpriseCompareBasketPage.tsx`（修订） | `service_org` Tab 摘"开发中"，挂服务机构面板 |
| `CapabilityView.tsx` / `ServiceOrgAnalysisPage.tsx` / `OrgProfileDrawer.tsx` / `serviceCenterStore.ts`（修订） | 对比候选收编系统篮 + 分发消费（`source=compare-basket`）+ 画像入篮 + `eval/setCompareOrgs` |
| `serviceReviewData.ts` / `serviceReadinessSeed.ts`（修订） | 新增 12 指标 8 件套 + 四维就绪度（R2）+ R2 需求 TRACE 记录 + Q-03/04/05 登记 |
| `routes.tsx` / `Layout.tsx`（修订） | `/service/chain-analysis`、`/service/institution-decision` 换新页；新增"服务机构查询"导航 |
| `service/ServiceChainAnalysis.tsx`、`service/ServiceInstitutionDecision.tsx` | **删除**（旧粗糙实现） |

## 3. AC-US 自走查

### 3.1 SVCCHAIN-ECOSYSTEM（28/28 通过）

- US-ECO-01（5 条）✅：6 环节顺序/机构数与详情列表一致；`segment` URL 直达；领域切换全重算并持久化；机构数 ⓘ `M_SVC_CHAIN_SEGMENT_ORG_COUNT`+🧪。
- US-ECO-02（5 条）✅：三类判定与链路图标注一一对应，依据行引用当前数值；瓶颈判定红问号（`M_SVC_CHAIN_BOTTLENECK` D1 missing，评审模式只显 Q-SVCCHAIN-03 引用）；click 判定行环节卡高亮入视口；业务态无 metric_id 泄漏。
- US-ECO-03（4 条）✅：四关系×四主体图例独立过滤即时生效并持久化；重置恢复全选；聚焦 1 度邻域可清除；确定性数据集（布局种子稳定）。
- US-ECO-04（5 条）✅：节点下钻与 R1 同一抽屉同一 org_id，URL `org` 直达；密度按 2E/(N(N-1)) 与可见子网一致；度中心性 TOP5 可下钻；影响力红问号不出伪评分；过滤变化统计同步重算并注明范围。
- US-ECO-05（3 条）✅：框架卡指标集与图表一致并带就绪度标注；完整度红问号 + 不参与图渲染；"待甲方确认"声明双模式覆盖。
- US-ECO-06（5 条）✅：五城市固定列，hover 与柱值一致；指标多选即时反映并持久化；对比值 ⓘ（`M_SVC_SZ_COMPARE_METRIC` draft ⚠️ Q-04）+🧪；仪表盘 🧪+⚠️，结论区数值不越图编造；完整度诚实排除。

### 3.2 SVCCHAIN-RECOMMEND（21/21 通过）

- US-REC-01（4 条）✅：四指标名称与 7.6.1 一致；≠100% 禁用显差值 + 一键归一；权重持久化可复位；演示口径声明 + ⚠️ Q-SVCCHAIN-05。
- US-REC-02（6 条）✅：名单列完整，综合分 = Σ(指标×权重)；ⓘ `M_SVC_REC_ATTRACT_SCORE`（draft ⚠️）+🧪；推荐理由引用行内数值；同配置确定性复现 + 配置变更提示（fingerprint）；CSV 行数/表头/声明/文件名合规；收藏即时同步 US-05。
- US-REC-03（3 条）✅：四维度语义与 7.7.1 一致，校验/归一同招引；类型/环节筛选持久化，全不选禁用有解释；声明同标准。
- US-REC-04（5 条）✅：仅深圳本土在库机构；ⓘ `M_SVC_REC_CULTIVATE_SCORE`+🧪，建议标签引用行内数值；下钻 R1 同一画像 + URL `org`；行内入篮与系统篮即时同步；CSV 含建议列。
- US-REC-05（3 条）✅：收藏 localStorage 跨刷新，两组独立；单移除即时、清空二次确认；收藏为快照，机构失效显"已失效"可移除。

### 3.3 R2B（R1 叶子修订部分，13/13 通过）

- US-ORG-06 修订（AC-06-07/06-08）✅：对比候选=系统篮唯一入口，无第二套控件，篮空引导空态；`source=compare-basket&org_ids[]` 自动预选并切到评估页签，无效 id 以 Message 报数量不静默丢弃。
- US-ORG-07（5 条）✅：三模式同 `SearchScaffold` 壳，差异仅配置层并登记 UX-SPEC；技术力分 ⓘ（draft ⚠️）+🧪，统计字段带状态角标；行级入篮/加入分析集合即时同步持久化；下钻同一画像；智能解析失败降级提示。
- US-ORG-08（6 条）✅：五类上下文触点状态跨页一致；`service_org` Tab 对齐政策篮全功能；2~5 家门禁 + 自动预选结果与手选一致（同一计算路径）；返回对比篮浮层常驻挂载、关键词/勾选会话内保留（`saveCompareBasketReturnContext` 快照同步落 sessionStorage 备用）；篮内容持久化、清空二次确认、容量与企业篮同机制；R1 无绕篮入口（与 06-07 互证）。

## 4. 架构合规自检（十条）

1. 算法只在 Python：✅ 纯前端确定性 mock；瓶颈/框架/推荐模型均演示态并登记 Q-03/04/05。
2. 调用链：✅ 无后端调用；正式接入按各叶子 IA 数据边界走 Java REST。
3. 图谱：✅ 前端 ECharts 演示图谱；正式关系数据接 NebulaGraph 时经 Java REST（IA 已注明），未引入 Neo4j。
4. 可观测性：✅ 沿用本仓既有接入，无变更。
5. CI/CD：✅ push origin/dev 触发（本地 build 绿；远端见 §5）。
6. demo2 只读 merge：✅ 未触碰 lumen 仓。
7. 共享聚合核心：✅ 不涉及 Java 变更。
8. 数据策略：✅ 全 mock + 🧪 标识。
9. 前端规范（D8）：✅ Arco React + ECharts，Arco Icon 表状态，无 emoji 状态位。
10. 数据血缘（D9）：✅ 新增 12 指标注册（`M_SVC_CHAIN_*`/`M_SVC_GRAPH_*`/`M_SVC_SZ_*`/`M_SVC_REC_*`），ⓘ+四维就绪度角标走评审层；BOTTLENECK/INFLUENCE/CHAIN_COMPLETENESS 三项 D1 missing 红问号，禁止伪闭合。

## 5. 验收证据

- 业务仓 commit：`acf7f42` + `284b681`（`13436da..284b681`，origin/dev），feat 29 文件 +4023/−2269，均 `[agent:frontend]`。
- 本地验证：`vite build` 通过（exit 0）；全部改动文件 lint 0 错。本仓无独立 tsc/lint 脚本，门禁同 R1 = build + lint。
- `pnpm run design:check` 失败为**存量问题**（脚本扫描 `src/app/pages/industry`，该目录在本批之前的 commit `8c04b30` 已更名 `industry-center`），与本批无关，登记遗留。
- 远端 CI：push 已触发；令牌无 GitLab API 读权限，流水线绿灯请监管人页面确认（同 R1 惯例）。
- 决策登记：`客户决策清单跟踪表.md` Q-SVCCHAIN-03/04/05。

## 6. 遗留风险与开放项

| 项 | 说明 | 去向 |
| --- | --- | --- |
| Q-SVCCHAIN-03/04/05 | 瓶颈识别、深圳评价框架、招引/培育模型均无算法定义卡，现为演示规则 | 待算法 Lead + 甲方；对应指标保持 D1 missing/draft 诚实态 |
| 三级项计数差 | 任务描述"11 个三级项"，招标原文 7.4–7.8 实为 10 项（§1.1 已逐条对照）；E7 README 总数 17→16 已更正 | 请 PM 复核确认无漏项 |
| pnpm v11 配置迁移 | 本机 pnpm 升至 11.20.0 后 `package.json#pnpm.overrides` 失读且构建脚本默认禁跑，已按官方迁移路径新增 `pnpm-workspace.yaml` 的 `overrides` + `allowBuilds`（`acf7f42`，语义与原配置等价，`package.json` 未动）；CI 若用 pnpm ≤10 不受影响（旧字段仍在） | 触碰构建配置文件，按公约 §4.3 登记请监管人知悉 |
| design:check 存量失败 | 脚本引用已更名目录 `industry`（`8c04b30` 更名为 `industry-center` 时未同步脚本） | 建议下批 chore 修脚本路径 |
| CI 绿灯确认 | 令牌无 API 权限 | 监管人 GitLab 页面确认 |
| return_context_id 预留 | 篮分发已按 ENT-COMPARE 同构写入回跳快照；当前回跳恢复实际依赖浮层常驻挂载（会话内即满足 AC-08-04），快照消费端预留给后续跨会话恢复 | 无功能缺口，登记备查 |
| **2026-08-07 as-built 补丁** | R2 初版组件引用了 `svc-eco-chain` / `svc-eco-stage-card` / `svc-eco-problem-row` 等 class，但未写入 `serviceCenter.css`，链路卡被挤窄后中文逐字折行叠字（外观似乱码）。已在同文件补全 `svc-eco-*` 样式（含图谱过滤/对比栅格/环节机构行）；`ChainLinkView` 项容器改为 `svc-eco-chain__item` | 已修；非产品范围变更 |

## 7. Cost（已回填 registry）

| 字段 | TOPIC-SVCCHAIN-R2 | TOPIC-SVCCHAIN-R2B |
| --- | --- | --- |
| actual_tokens | ~2,900,000 | ~1,300,000 |
| model_used | claude-fable-5 | claude-fable-5 |
| actual_cost | ~$8.7 | ~$3.9 |
| cost_warn | false | false |
