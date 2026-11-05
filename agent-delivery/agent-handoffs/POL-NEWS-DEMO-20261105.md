# POL-NEWS-DEMO-20261105 · 现有表支撑政策新闻整页演示

日期：2026-11-05。用户明确要求通过 mock 写入已有库表，支持政策新闻展示所有模块的数据与图形展示。

## 任务与规范

- claimed_by：agent:frontend-agent / agent:algorithm-agent；本会话用户直接授权补演示数据。
- supervised_by：未提供团队实名，不推断代填。ID 为交付追踪标识，当前会话未挂载 task-registry MCP，未直接读写注册表。
- ponytail: full。遵守主仓路径、团队公约、并行保护与相关角色规则。无新依赖、无 DDL、无新表、无 ODS/DWD/ADS 写入。
- 范围：时间轴、主题、影响、扶持四页签，复用既有 Vue/Arco/ECharts、Java 聚合门面和 Python 数据查询。

## 落库与隔离

- 仅向现有 `gkxlumenx_gapfill.gapfill_policy_qry_stat` 新增 32 行：10 项扶持卡片、12 条省级演示排名、10 条城市演示排名。
- 批次：`mock_policy_news_page_20261105`；fill_method=mock；fill_model=synthetic-page-demo-v1；gap_item=policy_news_demo:card:{key} 或 policy_news_demo:rank:{province|city}。
- 值为明确授权的合成演示统计，非业务定义终值；按现有字段承载，不修改指标注册表。复用 metric_id 列的既有指标编码，演示 key/排名含义由独立 gap_item 和批次判定，不作为正式指标计算结果。
- 既有 `_gapfill_stat` 查询显式排除 policy_news_demo 行，防止演示卡片混入原总量/分布查询。
- 新 `demo_support` 块独立承载演示卡片与排名；正式 portal_gaps 和 intensity_rank 不改写。现有有效值（包括零）优先；只有缺项或无正式排名时使用标记为 mock 的数据库行。
- 前端补齐项与演示排名显示“演示数据”，不恢复此前把 mock 评分当正式评分的路径，不改评分公式。
- 脚本 `seed_policy_news_page.py` 默认 dry-run，--apply 只插入本批次缺失键，事务提交；第二次预演 missing_rows=0。

## 其他模块与详情

- 时间轴接通既有 Java viz.events 数据，复用 6 条现有重大事件；无前端写死的新事件。
- 词云、聚类、深度复用已有 gapfill 表：10 个词、3 个主题、市场/企业/人才 3 层。
- 修复显式 GF-POL- 演示文档 ID 在 DWD 无对应记录时无法打开：先读正式文档，确无记录才读现有 gapfill 文档；不覆盖正式原文。
- 六条聚类政策详情均已实库验证正文可读取。

## 验证

- 实库只读整页验证：support_cards=10，demo_fallback_cards=5；demo_province_ranks=12、demo_city_ranks=10；正式省级排名仍为0，未污染。
- 区域图31行、重大事件6条、词频10项、主题3簇、深度3层、可打开聚类文档6条。
- `python3 -m pytest tests/test_policy_news_demo.py tests/test_policy_portal_gaps.py tests/test_policy_search_filter.py -q`：34项通过。
- 前端 policyNewsDisplay.selfcheck、type-check、build-only 通过；构建有原有 bundle 大小提示。
- 两仓 diff-check 通过。未做浏览器截图验收，未宣称线上部署成功。
- Java 无需改代码：现有 Map 门面去掉 items 目录字段后保留 demo_support，events 仍走既有 DTO。

## 架构与交付

- D8/D10：沿用现有布局、图表、行业/区域筛选及详情抽屉；仅增加演示来源标签，不新增无需规依据的业务模式或计算规则。全量视觉/键盘验收未执行。
- D9：本批次保留 mock 来源与追溯，正式数据和演示补齐并存，不改就绪度或冒充真实统计。
- D12：前端 → Java → lumen-algo-py → 既有 gapfill；无前端直连 Python/数据库，无新 demo 服务回落。沿用 trace header。
- Python提交 `afaa26d` 已推送origin/dev；前端原实现提交 `51e0365`，从 origin/dev 的临时检出仅摘取该提交后为 `84fcf3c`，仅含4个政策文件。
- 并行会话修改CMS并自行完成远端合并后，自动审批拒绝推送共享 dev，因为包含该会话尚未授权发布的CMS提交。本次改为在 `/private/tmp/policy-news-demo-delivery` 独立检出 origin/dev，cherry-pick 本次政策提交，不发布CMS提交、不stash/reset原工作区。该限定差异提交为实际推送对象。
- CI pipeline、镜像tag、K8s rollout 尚未确认。cost 未获得可核实统计，不填虚假费用或注册表状态。
