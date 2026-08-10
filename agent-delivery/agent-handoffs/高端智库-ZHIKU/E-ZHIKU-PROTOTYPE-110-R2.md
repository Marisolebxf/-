# Handoff｜E-ZHIKU-PROTOTYPE-110-R2：ZHIKU-BASIC-RESEARCH 基础研究智能决策闭环重实现

> **批次**：R2（重跑，延续 R1 打样确认标准）
> **执行**：frontend-agent（监管人/认领：human:淮政玮）
> **日期**：2026-08-05
> **业务仓 commit**：`2d6dd9c`（demo-ui-gaoduanzhiku-view @ origin/dev）

## 1. 范围与实现（对照 bid-reference）

范围真源：`agent-delivery/bid-reference/高端智库/新型高端智库需求拆解.md` §四 模块三（序号 82-87，6 项）。

| 序号 | 需求 | 落地 |
| --- | --- | --- |
| 82 | 问题识别与清单研发 | F-BR-01：关键词/来源/状态筛选、订阅退订持久化、🧪 智能识别新问题真实入库（候选池+固定延时）、在线发布状态流转、未发布新识别可移除、我的订阅聚合区 |
| 83 | 问题发展趋势分析 | F-BR-02：来源回溯条、发展轨迹图（新识别问题 Empty 不伪造）、增长/热度/潜力得分卡、预警"标记已处理"持久化分组、智能推荐（相关问题跳转 / 文献摘要抽屉） |
| 84 | 国内外竞争格局报告 | F-BR-03：三层次 Tab 持久化、四统计卡、柱/雷达切换、趋势追踪、**生成报告→writing createTask 预填任务并跳转大纲确认（跨叶子闭环）** |
| 85 | 深圳市基础研究部署清单 | F-BR-04：三维筛选持久化、地图↔表格双向联动（TalentMapView 增量 selectedId 高亮+flyTo）、详情侧条、趋势分析、热点问题回链 issues 趋势下钻 |
| 86 | 基础研究组织实施分析 | F-BR-05：五维雷达/资源清单/需求预测（虚线演示态）、资源配置建议"纳入跟踪/移除跟踪"持久化 + 我的跟踪清单 |
| 87 | 基础研究成果评估 | F-BR-06：成果选择持久化、四维雷达、对比/趋势子视图切换持久化、**生成评估报告→writing 预填任务（跨叶子闭环）** |

## 2. 产物清单

**叶子五件套**（`agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/ZHIKU-BASIC-RESEARCH-基础研究智能决策/`）：

- `USM-ZHIKU-BASIC-RESEARCH.md`：7 故事（US-ZHIKU-BR-01…07），每故事属性表/As-Want-So that/编号主路径/异常恢复表/5-6 条 AC/不包含边界；4 条跨故事 walkthrough；反向核对 6/6。
- `IA-ZHIKU-BASIC-RESEARCH.md`、`Wireframe-ZHIKU-BASIC-RESEARCH.md`（6 Frame 草图+字段表，第 6 列 metric_id/序号）、`UX-SPEC-ZHIKU-BASIC-RESEARCH.md`（7 旅程/持久化契约/状态机/机器可读契约）、`TRACE-ZHIKU-BASIC-RESEARCH.yaml`（6 序号全路由、39 AC、指标 rename 登记、跨叶子契约）。

**业务仓代码**（commit `2d6dd9c`，11 files，+1028/−192）：

- `src/mock/basicResearch.ts`：领域 store 重构——reducer 化 action + localStorage 持久化（key 前缀 `zhiku-br-`，7 个 key）+ `resetToSeed`；识别候选池、推荐扩展（targetIssueId/文献摘要）、部署领域→问题领域回链映射。
- `src/views/basic-research/`：4 页 + 3 panel 全部重实现（issues 页 URL `tab/issue` 下钻上下文、无效 id 回退）。
- `src/components/map/TalentMapView.vue`：增量可选 prop `selectedId`（选中描边 + flyTo），不影响既有调用方。
- `src/mock/metricSeed.ts` / `readinessSeed.ts`：`ZHIKU-S5-*` → `ZHIKU-BR-*` 正名（6 指标 + 2 GAP 引用），全仓无双 id 残留（rg 校验 0 命中 ZHIKU-S5）。

## 3. AC-US 自走查表（39 条）

| AC | 结论 | 说明 |
| --- | --- | --- |
| BR-01-01 关键词/来源/状态叠加筛选+清空 | ✅ | store.filteredIssues 三条件叠加；清空按钮条件显示 |
| BR-01-02 订阅退订双处同步 | ✅ | 行内链接 + 我的订阅卡片区同 getter |
| BR-01-03 订阅刷新保留 | ✅ | `zhiku-br-subscriptions` 持久化 |
| BR-01-04 筛选空态+清空恢复 | ✅ | EmptyState + 清空按钮 |
| BR-01-05 总数卡 ⓘ+🧪+就绪度 | ✅ | `ZHIKU-BR-ISSUE-TOTAL`（draft/mock） |
| BR-01-06 订阅不改清单本体 | ✅ | 订阅仅写 subscribedIssueIds |
| BR-02-01 识别 loading+真实入库+标记 | ✅ | runIdentify 900ms + 置顶插入 + 新识别🧪 Tag |
| BR-02-02 发布流转+总数+1 | ✅ | publishIssue；总数卡口径=published |
| BR-02-03 刷新保留 | ✅ | `zhiku-br-issues`/`identify-cursor` 持久化 |
| BR-02-04 池尽空态 | ✅ | identifyPoolExhausted → info 提示，不入库 |
| BR-02-05 未发布新识别可移除 | ✅ | removeIssue 守卫 isNew && identifying，Modal 确认 |
| BR-02-06 识别诚实性标注 | ✅ | 按钮🧪 + Message + 页脚标注 |
| BR-03-01 下钻 URL 上下文可恢复 | ✅ | `?tab=trend&issue=`；onMounted+watch 同步 |
| BR-03-02 回溯+轨迹+三得分卡 | ✅ | 得分卡 ⓘ `ZHIKU-BR-ISSUE-HEAT-SCORE` |
| BR-03-03 预警标记已处理持久化 | ✅ | `zhiku-br-alerts-handled`，已处理灰色分组 |
| BR-03-04 推荐跳转/文献抽屉 | ✅ | targetIssueId 切换 + a-drawer 摘要 |
| BR-03-05 新识别问题趋势 Empty | ✅ | 轨迹 Empty + 得分卡"—"，不伪造 |
| BR-03-06 演示态标注 | ✅ | 页脚诚实性标注 |
| BR-04-01 层次切换联动+持久化 | ✅ | ui.activeTier 持久化 |
| BR-04-02 柱/雷达切换不丢层次 | ✅ | chartType 独立于 tier |
| BR-04-03 指数 D1 missing 红问号+GAP | ✅ | readinessSeed def missing + pending_ref |
| BR-04-04 生成报告真实建任务+思路含数值 | ✅ | createTask 预填 5 章，思路注入 4 项统计值 |
| BR-04-05 跳转大纲确认 | ✅ | `/writing/create?step=outline&task=` |
| BR-04-06 取消无副作用 | ✅ | Modal onOk 才创建 |
| BR-05-01 三维筛选+表图同步+持久化 | ✅ | `zhiku-br-deploy-filters` |
| BR-05-02 表↔图双向选中同一 id | ✅ | selectedDeployId + selectedId prop + select-point |
| BR-05-03 筛选空态双侧+清空 | ✅ | 表格/地图各自 Empty |
| BR-05-04 总数卡 ⓘ+🧪+诚实标注 | ✅ | `ZHIKU-BR-DEPLOY-TOTAL` |
| BR-05-05 热点回链 issues 下钻 | ✅ | goHotspot → tab=trend&issue=，缺失时 warning |
| BR-06-01 四分析区块对应需求 | ✅ | 雷达/清单/预测/建议 |
| BR-06-02 建议跟踪幂等+计数 | ✅ | toggleSuggestion + 标题计数 |
| BR-06-03 跟踪刷新保留 | ✅ | `zhiku-br-suggestions` |
| BR-06-04 综合得分卡 ⓘ 演示态 | ✅ | `ZHIKU-BR-ORG-CAPABILITY-SCORE` |
| BR-06-05 预测/建议诚实标注 | ✅ | 两处标注保留 |
| BR-07-01 成果切换三处联动+持久化 | ✅ | ui.activeEvalId |
| BR-07-02 子视图切换持久化 | ✅ | ui.evalView（compare/trend） |
| BR-07-03 得分 D1 missing+告警条 | ✅ | `ZHIKU-BR-EVAL-SCORE` missing + a-alert |
| BR-07-04 生成评估报告预填+跳转 | ✅ | createTask 4 章，思路含四维得分 |
| BR-07-05 取消无副作用 / 07-06 无伪装正式算法 | ✅ | Modal 确认制；页面无"正式算法"表述 |

## 4. 验收证据

- `vue-tsc --build --force`：**0 错**（exit 0）。
- `vite build`：**通过**（exit 0，仅 chunk 体积告警，与 R1 一致）。
- 业务仓 push：`988bfcb..2d6dd9c dev -> dev`，GitLab CI 自动触发（K8s dev rollout）。
- 走查路径：W1 订阅识别发布刷新验证 → W2 竞争格局生成报告跨叶子 → W3 部署地图双向联动+热点回链 → W4 建议跟踪+评估切换（对应 USM §5）。

## 5. 架构合规自检（公约 §2 十条）

1. 算法只在 Python：✅ 无 Java/前端真实算法，识别/得分均 🧪 演示态并登记 GAP。
2. 调用链：✅ demo 全 mock，无越层调用；正式态服务面已在 IA §7 声明（Java REST → Python internal）。
3. 图谱：✅ 未涉及（无图谱功能，未引入 Neo4j）。
4. 可观测性：✅ 沿用仓内 `observability.ts` 接线，未破坏。
5. CI/CD：✅ push dev 触发 Pipeline（deploy 见 §4）。
6. demo2 只读 merge：✅ 不涉及。
7. 共享聚合核心：✅ 前端只消费 mock/未来 Java REST。
8. 数据策略：✅ 标准表口径写入指标 8 件套 source_tables，Mock 填充。
9. 前端规范（D8）：✅ Arco Design Vue + ECharts + Leaflet + dayjs 栈内组件；主色/token 未改。
10. 数据血缘（D9）：✅ 6 指标 ⓘ+metric_id+就绪度角标；2 项 def=missing 红问号 GAP 引用；🧪 MockBadge 全量；rename 无双 id。

## 6. 偏离说明

- "定向查询与订阅"的推送通道：demo 只维护订阅关系与界面聚合（TRACE deviations 已登记）。
- "纳入跟踪"建议工作集为闭环增强（需求 86 未显式要求），USM/TRACE 已标注。
- 竞争格局"综合对比指数"数值沿用研究热度口径展示（指数算法未定义，D1 missing 诚实态），待 Q-ZHIKU-04 拍板后替换。

## 7. cost 回填（budget-estimate 口径）

- `actual_tokens`：≈ 300,000（本批次会话累计，含五件套撰写与实现）
- `model_used`：claude-fable-5
- `actual_cost`：≈ $4.5（估算）
- `cost_warn`：false（< $10）

## 8. 遗留风险

- CI 流水线结果需在 GitLab 确认绿（push 后自动触发，本 handoff 提交时处于运行中）。
- 两枚 missing 指标依赖算法定义卡（Q-ZHIKU-04），上线前必须补齐或按业务态置灰。
- localStorage 状态与 R1 写作域（`zhiku-wr:`）相互独立，若演示前需要干净环境，用页内"恢复演示数据"入口。
