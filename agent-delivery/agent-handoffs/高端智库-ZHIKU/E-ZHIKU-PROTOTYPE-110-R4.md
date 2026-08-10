# Handoff｜E-ZHIKU-PROTOTYPE-110-R4：ZHIKU-RESEARCH-NEED / ZHIKU-TECH-SYSTEM / ZHIKU-TECH-TREND 战略研究三叶子闭环重实现

> **批次**：R4（重跑，延续 R1 打样确认 + R2/R3 同一标准）
> **执行**：frontend-agent（监管人/认领：human:淮政玮）
> **日期**：2026-08-05
> **业务仓 commit**：`a3173a1`（主实现）+ `405a8e3` / `13bf8ee`（AC 补漏），demo-ui-gaoduanzhiku-view @ origin/dev

## 1. 范围与实现（对照 bid-reference）

范围真源：`agent-delivery/bid-reference/高端智库/新型高端智库需求拆解.md` §模块一"战略咨询智能支持"。三叶子切分（战略研究序号 1-45）：

- **ZHIKU-RESEARCH-NEED 研究需求分析**：序号 1-7（科技实体检索/画像下钻/颠覆性与前沿技术/趋势速览/媒体舆情联动）
- **ZHIKU-TECH-SYSTEM 技术体系分析**：序号 8-28（体系管理/在线编辑/互动交流/论文分析/专利分析/科研项目/社会网络）
- **ZHIKU-TECH-TREND 技术趋势分析**：序号 29-45（聚类分析/三级筛选/共性网络/技术热点/合作与发展趋势/预警跟踪订阅检测）

| 序号段 | 需求 | 落地 |
| --- | --- | --- |
| 1-3 | 科技实体检索与画像 | F-RN-01/02：四维筛选+双视图持久化、批量导入幂等（🧪）、`?entity=` URL 分享恢复、相似推荐切换、非法 id 回落 |
| 4-5 | 颠覆性/前沿技术 | F-RN-03：六要素卡、下钻联动、关注集持久化、热度趋势图、🧪 挖掘演示态标注 |
| 6 | 趋势数据卡片 | F-RN-04：标签过滤持久化、摘要抽屉+去 TECH-TREND 深挖跨叶子入口 |
| 7 | 媒体舆情联动 | F-RN-05：六层次过滤+可视化联动、预警处理持久化、实体回链（US-02 复用）、**生成舆情研判报告 → writing createTask 预填（CT-RN-01）** |
| 8-10 | 体系管理与编辑 | F-TS-01/02：体系建/删/筛选闭环、树节点增删改+TRL/重要性编辑、`?system=` URL 恢复、展开态持久化 |
| 8-10 | 互动交流 | F-TS-03：双维筛选、回复追加持久化、确认状态联动、单用户代演声明 |
| 11-14 | 论文分析 | F-TS-04：词云/排行/趋势三视图、交叉矩阵下钻样本明细、任务模拟推进/合并/重解析 |
| 15-20 | 专利分析 | F-TS-05：四视图、任务暂停/恢复/删除、深度矩阵 CSV 真实导出、**生成专利分析报告（CT-TS-01）**、算法层 🧪 目标态声明 |
| 21-23 | 科研项目 | F-TS-06：组合检索持久化、仪表盘联动、任务新建/合并 |
| 24-28 | 社会网络 | F-TS-07：图↔列表双向联动、上传建任务、维护区增删改实时反映、重新分析+节点/边 CSV 导出 |
| 29-32 | 聚类分析 | F-TT-01/02：任务建/删/重跑流转、簇卡↔散点联动选中（持久化）、三级权重零和校验、重算按加权得分真实重排、清单重命名+CSV |
| 33-37 | 共性网络 | F-TT-03：任务流转、矩阵单元格三值下钻、规则启停联动过滤语义主题、主题五要素卡、**高产作者→人才库画像（CT-TT-01）**（未收录明确提示） |
| 38-41 | 热点/合作/趋势 | F-TT-04/05：热点搜索/下钻持久化+走势图+**相关实体回链 RN 清单**、交叉阈值过滤、合作网络图↔四列列表双向联动（选中持久化）、时间窗/对象持久化+对比表格、预测区间 D1 missing 诚实态 |
| 42-45 | 预警跟踪订阅检测 | F-TT-06：预警详情抽屉（影响评估+关联技术）、处理态持久化、**生成预警研判报告（CT-TT-02）**、订阅增删去重、检测出趋势序列+三类建议分组 |

## 2. 产物清单

**叶子五件套 ×3**（`agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/`）：

- `ZHIKU-RESEARCH-NEED-研究需求分析/`：USM（5 故事 US-ZHIKU-RN-01…05，25 AC）/ IA / Wireframe / UX-SPEC / TRACE.yaml（序号 1-7 反向核对闭合、`ZHIKU-S2-*` rename 登记）。
- `ZHIKU-TECH-SYSTEM-技术体系分析/`：USM（7 故事 US-ZHIKU-TS-01…07，35 AC）/ IA / Wireframe / UX-SPEC / TRACE.yaml（序号 8-28 闭合、`ZHIKU-S3-*` rename 登记）。
- `ZHIKU-TECH-TREND-技术趋势分析/`：USM（6 故事 US-ZHIKU-TT-01…06，28 AC）/ IA / Wireframe / UX-SPEC / TRACE.yaml（序号 29-45 闭合、`ZHIKU-TT-TREND-FORECAST` D1 missing GAP 登记）。

**业务仓代码**（3 commits，31+5+7 files，约 +3307/−577）：

- `src/mock/`：`persist.ts` 复用；`researchNeed.ts`（前缀 `zhiku-rn-`）、`techSystem.ts` / `paperAnalysis.ts` / `patentAnalysis.ts` / `researchProject.ts` / `socialNetwork.ts`（前缀 `zhiku-ts-`）、`clusterAnalysis.ts` / `commonNetwork.ts` / `techHotspot.ts` / `techAlert.ts`（前缀 `zhiku-tt-`）：reducer 化 action + localStorage 持久化（筛选/导入/树展开/回复/任务/权重快照/选中态/订阅/检测等 25+ key）。
- `src/views/research-need/` `tech-system/` `tech-trend/`：3 Home + 13 Panel 全部重实现或重构（URL tab/entity/system 契约、EmptyState 全覆盖、异常态按 USM 异常表）。
- `src/components/`：`CrossHeatTable.vue` 增 clickable 下钻；`GraphView.vue` 增 `selectedId` 选中高亮（列表↔图双向联动）；`SocialNetworkGraph.vue` props 化。
- `src/mock/metricSeed.ts` / `readinessSeed.ts`：`ZHIKU-S2-*` → `ZHIKU-RN-*`、`ZHIKU-S3-*` → `ZHIKU-TS-*`/`ZHIKU-TT-*` 正名（rename 登记 TRACE，无双 id 残留）；`ZHIKU-TT-TREND-FORECAST` D1 missing + GAP 引用。

## 3. AC-US 自走查表（RN 25 + TS 35 + TT 28 = 88 条）

### ZHIKU-RESEARCH-NEED（25 条）

| AC | 结论 | 说明 |
| --- | --- | --- |
| RN-01-01 四类筛选叠加+清空 | ✅ | filters reducer 实时联动 |
| RN-01-02 双视图切换+刷新保留 | ✅ | `zhiku-rn-` 前缀持久化 |
| RN-01-03 批量导入真实入清单+幂等 | ✅ | 导入 🧪 标记，重复跳过摘要列明 |
| RN-01-04 筛选/视图/导入刷新保持 | ✅ | localStorage 全量 |
| RN-01-05 实体总数卡 ⓘ+🧪 | ✅ | `ZHIKU-RN-ENTITY-TOTAL` 8 件套+就绪度四行 |
| RN-01-06 无结果 Empty+清空筛选 | ✅ | EmptyState 引导 |
| RN-02-01 详情抽屉三区块 | ✅ | 基础信息/热度趋势/相似推荐 |
| RN-02-02 相似推荐切换+选中同步 | ✅ | 抽屉内切换联动清单 |
| RN-02-03 `?entity=` URL 分享恢复+非法回落 | ✅ | restoreFromUrl + 警告回落 |
| RN-02-04 演示推荐诚实标注 | ✅ | 🧪 同领域规则声明 |
| RN-02-05 关闭抽屉 URL 清除 | ✅ | query 双向同步 |
| RN-03-01 颠覆性卡六要素 | ✅ | 名称/指标/TRL/热度/参与方/场景 |
| RN-03-02 下钻前沿详情真实联动 | ✅ | 滚动定位+抽屉打开 |
| RN-03-03 关注/取关+重点关注区+刷新保持 | ✅ | 幂等 toggle |
| RN-03-04 前沿详情热度趋势图 | ✅ | 近 6 期折线 |
| RN-03-05 AI 挖掘 🧪 演示标注 | ✅ | 预置清单声明 |
| RN-04-01 趋势卡标签过滤+持久化 | ✅ | 标签点选/取消 |
| RN-04-02 趋势总数卡 ⓘ+🧪 | ✅ | `ZHIKU-RN-TREND-TECH-TOTAL` |
| RN-04-03 摘要抽屉+跨叶子深挖入口 | ✅ | 跳 `/strategy/tech-trend?tab=hotspot` |
| RN-04-04 标签无结果 Empty | ✅ | 清空标签按钮 |
| RN-05-01 六层次过滤+可视化联动 | ✅ | 分布图高亮同步 |
| RN-05-02 预警处理+统计卡联动+持久化 | ✅ | `ZHIKU-RN-MEDIA-WARNING-PENDING` |
| RN-05-03 关联实体回链详情抽屉 | ✅ | US-02 同组件，未收录有提示 |
| RN-05-04 生成舆情研判报告（CT-RN-01） | ✅ | createTask 预填统计数值+跳大纲 |
| RN-05-05 图谱联动 🧪+GAP | ✅ | GAP-ZHIKU-RN-KG-LINK 登记 |

### ZHIKU-TECH-SYSTEM（35 条）

| AC | 结论 | 说明 |
| --- | --- | --- |
| TS-01-01 新建体系入库+校验 | ✅ | 空名/重名拦截 |
| TS-01-02 关键词筛选+Empty | ✅ | 清空筛选按钮 |
| TS-01-03 删除二次确认+联动 | ✅ | 统计卡同步 |
| TS-01-04 体系总数卡 ⓘ+🧪 | ✅ | `ZHIKU-TS-SYSTEM-TOTAL` |
| TS-01-05 在线编辑直达+URL | ✅ | `?system=` 同步 |
| TS-02-01 节点属性修改即时反映 | ✅ | 名称/TRL/重要性 |
| TS-02-02 增删节点+级联确认 | ✅ | 级联数量文案 |
| TS-02-03 `?system=` 分享恢复+非法回落 | ✅ | 提示回落 |
| TS-02-04 树展开态/选中持久化 | ✅ | `zhiku-ts-` 前缀 |
| TS-02-05 编辑联动更新时间 | ✅ | US-01 卡片同步 |
| TS-03-01 双维筛选+Empty | ✅ | 体系+分支 |
| TS-03-02 回复追加+空回复拦截 | ✅ | 持久化 |
| TS-03-03 确认状态+计数联动 | ✅ | 刷新保持 |
| TS-03-04 单用户代演说明 | ✅ | 不伪装多账号 |
| TS-04-01 论文总览三视图 | ✅ | 词云/排行/趋势 |
| TS-04-02 交叉矩阵下钻样本明细 | ✅ | CrossHeatTable clickable+🧪 |
| TS-04-03 任务入列+模拟推进+持久化 | ✅ | queued→analyzing→done |
| TS-04-04 合并/重新解析 | ✅ | 原任务归档标记 |
| TS-04-05 论文统计卡 ⓘ+🧪 | ✅ | `ZHIKU-TS-PAPER-TOTAL` |
| TS-05-01 专利总览四视图 | ✅ | 词云/排行/国别/IPC |
| TS-05-02 任务暂停/恢复/删除持久化 | ✅ | 刷新保持 |
| TS-05-03 案例库详情抽屉 | ✅ | 卡片下钻 |
| TS-05-04 深度矩阵维度切换+CSV | ✅ | 真实文件下载 |
| TS-05-05 生成专利报告（CT-TS-01） | ✅ | createTask 预填+跳大纲 |
| TS-05-06 算法层 🧪 目标态声明 | ✅ | GAP-ZHIKU-TS-ALGO-LAYER |
| TS-06-01 组合检索+持久化 | ✅ | 关键词+多筛选 |
| TS-06-02 仪表盘三视图联动 | ✅ | 领域筛选驱动 |
| TS-06-03 任务新建/合并+三列 | ✅ | 状态/进度/优先级 |
| TS-06-04 项目统计卡 ⓘ+🧪 | ✅ | `ZHIKU-TS-PROJECT-TOTAL` |
| TS-07-01 网络图↔列表双向联动 | ✅ | 节点选中同步 |
| TS-07-02 统计/关键节点/社区三块 | ✅ | 结果区齐备 |
| TS-07-03 上传流程真实产任务 | ✅ | 模板→上传→任务推进 |
| TS-07-04 维护增删改实时反映+级联提示 | ✅ | 图与统计同步 |
| TS-07-05 重新分析+节点/边 CSV | ✅ | 真实下载 |
| TS-07-06 节点统计卡 ⓘ+🧪 | ✅ | `ZHIKU-TS-NETWORK-NODE-TOTAL` |

### ZHIKU-TECH-TREND（28 条）

| AC | 结论 | 说明 |
| --- | --- | --- |
| TT-01-01 任务入列+模拟推进 | ✅ | created→running→done |
| TT-01-02 簇卡↔散点双向联动 | ✅ | 选中高亮+降透明，持久化（13bf8ee 批补齐） |
| TT-01-03 簇总数卡 ⓘ+🧪 | ✅ | `ZHIKU-TT-CLUSTER-TOTAL` |
| TT-01-04 聚类 🧪 诚实标注 | ✅ | GAP-ZHIKU-TT-CLUSTER |
| TT-01-05 删除/重跑真实生效 | ✅ | rerunTask 演示流转 |
| TT-02-01 权重零和校验+禁用提示 | ✅ | 差值提示 |
| TT-02-02 重算后排序真实变化 | ✅ | appliedWeights 快照加权重排 🧪 |
| TT-02-03 重命名/CSV/恢复默认 | ✅ | 真实下载 |
| TT-02-04 权重/清单刷新保持 | ✅ | `zhiku-tt-` 前缀 |
| TT-03-01 任务推进+矩阵三值下钻 | ✅ | 共现/相似度/综合强度 |
| TT-03-02 规则启停联动过滤语义主题 | ✅ | visibleSemanticNodes getter |
| TT-03-03 语义主题五要素卡 | ✅ | 置信度/中心性/文献量/关键词/作者 |
| TT-03-04 高产作者→人才库画像（CT-TT-01） | ✅ | sch-001/002 建档，未收录明确提示 |
| TT-03-05 语义网络 🧪 标注 | ✅ | 预置关系声明 |
| TT-04-01 热点搜索/排名/下钻+持久化 | ✅ | 搜索态保存 |
| TT-04-02 交叉明细三值+联动 | ✅ | 阈值过滤+单元格 title |
| TT-04-03 热点统计卡 ⓘ+🧪 | ✅ | `ZHIKU-TT-HOTSPOT-TOTAL` |
| TT-04-04 热点详情走势图+相关实体回链 | ✅ | 回链 `/strategy/research-need?tab=entity` |
| TT-05-01 合作图↔列表双向联动+四列 | ✅ | 强度/领域/时长/评分，选中持久化 |
| TT-05-02 趋势折线+对比表格+勾选保持 | ✅ | 窗口起止值与增幅 |
| TT-05-03 预测 D1 missing 红问号+GAP | ✅ | `ZHIKU-TT-TREND-FORECAST` 不伪闭合 |
| TT-05-04 预测虚线 ⚠ 行内标注 | ✅ | 非算法产出声明 |
| TT-06-01 预警详情抽屉+统计卡联动 | ✅ | 影响评估+关联技术，`ZHIKU-TT-ALERT-PENDING` |
| TT-06-02 双栏跟踪切换 | ✅ | 对象选中持久化 |
| TT-06-03 订阅全链路+幂等拦截 | ✅ | 关键词+频率去重 |
| TT-06-04 检测出趋势序列+三类建议分组 | ✅ | 跟踪/布局/风险三组，历史持久化 |
| TT-06-05 生成预警研判报告（CT-TT-02） | ✅ | createTask 注入级别+影响评估+跳大纲 |
| TT-06-06 检测/订阅 🧪 标注 | ✅ | 预置动态池声明 |

## 4. 验收证据

- `vue-tsc --build`：**0 错**（exit 0，三轮验证，末轮含 AC 补漏后全量）。
- `vite build`：**通过**（exit 0，仅 chunk 体积告警，与 R1-R3 一致）。
- 业务仓 push：`2d6dd9c..a3173a1..405a8e3..13bf8ee dev -> dev`，GitLab CI 自动触发（K8s dev rollout）。
- 走查路径：W1 实体检索→画像 URL 分享→媒体舆情→生成报告跨叶子 → W2 体系建/编辑树/URL 恢复→论文/专利任务闭环→专利报告跨叶子 → W3 聚类任务/权重重算重排→规则联动语义主题→作者跳人才库 → W4 热点下钻回链 RN→合作双向联动→趋势对比+预测诚实态 → W5 预警详情→研判报告跨叶子→订阅/检测闭环（对应三份 USM §5）。

## 5. 架构合规自检（公约 §2 十条）

1. 算法只在 Python：✅ 聚类/语义网络/相似度/预测/检测全部 🧪 演示态并登记 GAP，无前端真实算法冒充。
2. 调用链：✅ demo 全 mock；正式态服务面已在三份 IA §7 声明（Java REST → Python internal）。
3. 图谱：✅ 语义/合作/社会网络均为前端 G6 演示，未引入 Neo4j。
4. 可观测性：✅ 沿用仓内 `observability.ts` 接线，未破坏。
5. CI/CD：✅ push dev 触发 Pipeline。
6. demo2 只读 merge：✅ 不涉及。
7. 共享聚合核心：✅ 前端只消费 mock/未来 Java REST。
8. 数据策略：✅ 指标 8 件套 source_tables 写 ADS 目标口径，Mock 填充。
9. 前端规范（D8）：✅ Arco Design Vue + ECharts + G6 栈内；主色/token 未改。
10. 数据血缘（D9）：✅ 全部统计卡 ⓘ+metric_id+就绪度角标；`ZHIKU-TT-TREND-FORECAST` D1 missing 红问号 GAP 引用；🧪 MockBadge 全量；S2/S3 rename 无双 id 残留（rg 校验 0 命中）。

## 6. 偏离说明

- 聚类/语义网络/共性分析（序号 29-37）：算法结果为预置演示（🧪），真实图算法与聚类归 Python `/internal/*`，挂 GAP-ZHIKU-TT-CLUSTER（Q-ZHIKU-04），上线前须补算法定义卡。
- 趋势预测（序号 41）：预测区间为前端演示虚线，`ZHIKU-TT-TREND-FORECAST` 保持 D1 missing 诚实态，禁止对外决策展示。
- 预警/检测（序号 42-45）：触发与检测结果为预置动态池演示，非实时监测；真实检测依赖三方源接入与算法卡。
- 「生成趋势报告」（热点页）为 USM 基线外扩展出口，语义与 CT-RN-01/CT-TT-02 同模式，未单列契约编号。
- 批量导入（序号 1）：demo 用预置候选池模拟，无真实文件解析。

## 7. cost 回填（budget-estimate 口径）

- `actual_tokens`：≈ 420,000（本批次会话累计，含三套五件套撰写与 13 Panel 实现及两轮 AC 补漏）
- `model_used`：claude-fable-5
- `actual_cost`：≈ $6.5（估算）
- `cost_warn`：false（< $10）

## 8. 遗留风险

- CI 流水线结果需在 GitLab 确认绿（`13bf8ee` push 后自动触发，本 handoff 提交时处于运行中）。
- 聚类/语义/预测/检测四类算法能力依赖算法定义卡（Q-ZHIKU-04），上线前必须补齐或业务态置灰。
- 高产作者→人才库画像映射（CT-TT-01）为演示建档（sch-001/002），正式态须以真实人才库主数据对齐。
- localStorage 状态与 R1（`zhiku-wr:`）/R2（`zhiku-br-`）/R3（`zhiku-tp-`/`zhiku-tm-`）域相互独立；演示前如需干净环境，清除 `zhiku-rn-` / `zhiku-ts-` / `zhiku-tt-` 前缀 key（早期快照字段缺失已做 hydrate 兼容）。
