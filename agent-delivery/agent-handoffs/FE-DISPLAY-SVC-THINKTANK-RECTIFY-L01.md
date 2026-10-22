# FE-DISPLAY-SVC-THINKTANK-RECTIFY-L01 · 展示系统-科技服务全景-智库服务 demo 页按需规 566-574 整改

> 本地未提交。页面在 `demo-ui-science`，监管人孔东看过后再决定是否提交。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 孔东派工并自领监管。MCP `task-claim` 未回传 `claim_type`，按本人认领记 `pull`。状态停在 `in_progress`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 沿用 demo 现有 Ant Design 页和详情抽屉，不新依赖。需规五类模块、筛选、详情、动态条和来源标注都保留。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶是 demo 页整改，未走 Headroom 代理。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本叶只改 demo 展示页，不改架构图、存储流图或接口契约图。 |
| 会签态 | 不适用 |
| 说明 | 展示侧五个对象的接口仍待后续单承接；本叶用样例数据把页面功能补齐。 |

## 格式参考（可选）

| 项 | 对齐来源 |
|----|---------|
| 章节结构 | templates/handoff-template.md |
| 范围边界 | 需规 `智库服务.md` 序号 566–574 |

## 问题清单

- 服务类型正式用词仍是运营临时目录（政策研究、战略咨询、评估评价、人才培训、学术交流），待甲方确认。
- 供方七种分析方法只在服务类型页说明，不进入服务类型目录。
- 活动地点、内容、媒体文件、供方专家详情页地址，样例中空位显示「待补齐」。
- 成果里有一条缺投资回报率和客户满意度，全部样例汇总这两项显示「待补齐」；筛掉该条后，当前筛选汇总能算出数。
- 问卷统计默认收起，展开后只保留位置，不填问答明细。

## 修改内容

- `ThinkTankService.jsx`：五个页签、动态条（重大事件 / 成果发布 / 政策建议）、服务类型·主题·时间·排序筛选、列表进详情。
- `mockData.js`：智库样例改为带来源的字段。重大事件含运营编目和采集补充。无摘要的报告由系统按标题和主题摘录。
- `thinkTankModel.js`：筛选、摘录、成果汇总。有空值的汇总项不算成完整指标。
- `style.css`：来源标、动态条、选中的服务类型卡。

## 测试结果

- `node src/pages/tech-service/thinkTankModel.js`：通过。
- `node src/pages/tech-service/innovationEcosystemModel.test.mjs`：通过（专家头像仍指向本地 jpg）。
- 浏览器 `http://127.0.0.1:4176/#/topic/智库服务`：五个页签可见；报告详情含摘要、目录、正文、图表位和媒体「待补齐」；近一月筛掉 5 月报告和缺回报率的成果，筛选汇总变为投资额 400、回报率 15.3、满意度 93.5；活动详情默认收起问卷统计，展开后标明不宜公开且不填明细；服务类型页标明待甲方确认，并列出七种分析能力不作为服务类型。

## 遗留风险

- 数字和正文是演示样例，不是 Z-01～Z-03 实接。
- 未提交、未推送。`lumen-ui-science-pc` 仍只有菜单，未复刻本页。
- 服务类型卡片上的关联数是全量档案计数，不随主题和时间筛选变化；列表本身随筛选变化。

## CI/CD（必填）

- 分支：`demo-ui-science` 本地工作区，未 commit
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：未部署
- dev 测试 URL / 命令与结果：本地 `npm run dev` → `http://127.0.0.1:4176/#/topic/智库服务`，见测试结果

## 可观测性（建议）

- OTEL_SERVICE_NAME：无（demo 静态页）
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `repos/demo-ui-science/src/pages/tech-service/ThinkTankService.jsx`
- `repos/demo-ui-science/src/pages/tech-service/mockData.js`
- `repos/demo-ui-science/src/pages/tech-service/thinkTankModel.js`
- `repos/demo-ui-science/src/pages/tech-service/style.css`
