# POL-L2-PC3-PC4 · 总派单

必读：`POL-L2-PC3-PC4-长任务总控.md`、说明书 #### 610。  
监管人：`human:淮政玮`。分支：`origin/dev`。强度：`ponytail full`。  
会签签收且总控写上「后续认领不必再问」之前，下面五段都不认领。

## 铁律

浏览器只打 `/display/v1/policy/compare/runs`。Python 写 `gkxlumenx_ads.ads_policy_compare_report`，Java 只读。材料用政策库检索、603 结构化、604 溯源，以及拆解 606–609。不新模型，不标 501，不建 gapfill，不把智能研报生成加回侧栏。样本两份：珠海市固态电池产业发展行动方案（2025-2030年）、深圳市新型储能产业发展规划（2026—2030年），地区广东省，效力市级。

## ADS-L01

仓 `lumen-algo-py`。建表。一行装下政策编号与标题、维度、权重、阈值、时间窗、状态、分数、四类识别、图用点边、摘要、结论、深度四块、洞察四类、章节、双向溯源、失败原因、写入时间。字符集 `utf8mb4_general_ci`。

## WRITE-L01

仓 `lumen-algo-py`。排在 ADS 之后。对样本两份：没有结构化先走已有抽取，没有拆解先提交 `policy_parse_semantic` / `policy_parse_clause` / `policy_parse_metric` / `policy_parse_entity`，再写完成行。条款进对比的条款维，指标和力度进核心指标与扶持力度，语义进适用范围与实施路径，实体进知识图谱。溯源用「原文 → 条款 → 结论」。正文不出现「演示」「mock」。当天同一指纹已完成则直接返回该行。

## API-L01

仓 `lumen-svc-platform`。`POST /display/v1/policy/compare/runs` 委托 Python。`GET` 列表给分析对比记录，`GET` 单行给对比和研报。不拼种子句。没有行就空。

## FE-L01

仓 `lumen-ui-science-pc`。完工即推。运行对比画出该行的表、四类、三张图、摘要和结论。查看报告打开完整研报。PDF 与 Word 带正文和三张图。关 mock 时失败不得留下种子。

## E01

QA 不改代码。打已发布展示 dev。总控 §4 四行，期望未发生必红。
