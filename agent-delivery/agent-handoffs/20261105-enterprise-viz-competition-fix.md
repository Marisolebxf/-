# 企业发展可视化竞争力空白排查

范围：截图企业深圳市红阳电池有限公司（29961637）的 SWOT 与同行对比。

ponytail: full；沿用现有接口、ES 字段与 ECharts，无新增依赖。

交付标识：20261105-enterprise-viz-competition-fix。当前会话未提供 task-registry MCP，未虚构登记 ID 或成本数据。

## 原因与实现

- Python 原 SWOT 与规则 SWOT 同路径，先注册的 LLM 路由遮蔽规则路由。规则路由独立为 `/internal/enterprise/viz/swot`，Java 可视化调用同步修改，原 LLM 接口保留。
- ES statistics 为 nested 列表，按字典读取导致异常；修复为取最新统计记录，并修复专利字段名称与源字段投影。
- Java SWOT DTO 兼容 title 字段，有事实支持的象限直接展示，不因未生成四象限而整块隐藏。前端使用真实 snake_case expert_comment，显示规则生成说明。
- Java peers 原来固定空块，现对接已有 Python peers 接口。
- Python peers 的顶层 ids 过滤将查询收缩为自身，现按行业取同行后补入自身；保留零利润、零研发值，规范缺失维度处理。
- 前端指标改为 key/name/max、企业值改为 values/self，接入条形图（少于三维）与雷达图。

## 数据验证

只读远端现有 ES。红阳电池已有 2021–2025 财务、竞争力 72.5、有效专利 12、成立日期及企业规模，无新增 mock、无写库。

修复后的 Python 直接查询返回两个有事实支持的 SWOT 象限，22 家（含自身）专利对比。抽查发现部分同行 financials 只有年份、无金额，因此本次可比维度为专利；未为显示更多维度伪造数据。

## 验证与限制

- Python：11 项回归测试通过，覆盖旧 SWOT 契约、新路由、nested 统计、同行过滤、零值和缺维。
- 前端：type-check 与生产构建通过。
- Java：修改源码使用已有依赖 javac 编译通过；标准 Maven 因离线缺少插件依赖失败，改用已有本地依赖运行 JUnit，8 项全部通过（临时使用 subclass mock maker，不修改仓库测试配置）。
- 代码提交：lumen-algo-py `1ef82bd`，lumen-svc-platform `1fe2aa2`，lumen-ui-topic `2560850`。按主仓规范推送 origin/dev；CI 与线上页面验收尚待确认。
- 工作区另有产业全景修改，与本次企业模块无关，未覆盖或提交。

## 架构与数据血缘

沿用前端 → Java → Python → 现有 ES；无新增表、无前端硬编码业务值、无写入 ODS/DWD/ADS。规则生成说明与可用指标数据一致。
