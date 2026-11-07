# SYSINT-04-01-DATA-OPEN-L01 · 专题一张图数据探查与指标口径冻结

## 任务状态

- 状态：`in_progress`，只读探查阶段；尚未会签、未解锁后续灌数实施单。
- 认领 / 监管：`human:徐滕强` / `human:徐滕强`，4 小时锁。
- 执行范围：需规 99–101 中智树负责的产业、企业和政策项 G1–G6。技术、人才、科研仍由久新负责。
- 数据边界：仅对正式 `gkxlumenx_dwd` 执行只读查询；不写库、不建表、不改表、不运行灌数脚本。任何 DDL 提案先向用户沟通。

## 实查证据

2026-11-07 通过 `lumen-topic-py` 现有配置建立只读会话；报告仅含表结构与聚合统计，不含凭据或企业明细。

| 项 | 正式库观察 | 对需求的影响 |
|---|---|---|
| 库选择 | 默认配置指向 `demo_gkxlumenx_dwd`；正式库 `gkxlumenx_dwd` 存在同名企业表。正式库 `enterprise_base` 查询为 269,511 行、269,511 个 `org_id`，其中 `city='深圳市'` 95,600 家；这与 demo 快照不可混用。 | 所有实现与验收必须显式区分 demo / 正式库。 |
| 全口径从业人数 G3 | 正式 `enterprise_base` 没有 `employees_number`，仅有 `rd_staff_count`；`enterprise_finance_history.rd_staff_count` 567,263 行全空。唯一正式 `employees_number` 在境外表 `enterprise_forg_finance_history`：51 行、12 个机构，2025/2026 年记录均无正值。 | 深圳国内企业全口径人数无可用字段；研发人数也没有正式数据。G3 保持空态，不能用 `research_staff_total`、研发岗或境外零值代替。现有填数脚本检测不到 `enterprise_base.employees_number` 时会跳过；不能把字段名当作实有来源。 |
| 企业人数分桶 G2 | 同 G3，无深圳企业人数明细可分桶。正式 `enterprise_industry_chain` 当前约 20 行；按城市 JOIN 后只匹配到 9 个 INB 码、18 个关联，无法代表完整产业企业池。 | G2 暂无可灌明细。需先解决人数来源和产业归属闭合；ES 仅作候选时也必须实查字段与覆盖率。 |
| 产业规模 G1 | 正式 `enterprise_finance_history` 有 2021–2025 年记录，但每年全深圳注册企业中仅约 544–625 家有正收入；金额单位为万元。2026 年有部分期数据。`enterprise_industry_product` 有产业名称 JSON 类标签，但不是已验证的 INB 映射；企业关联与财务记录也不等于全产业统计口径。 | 该表可列为候选“已披露企业营业收入”，不能直接称完整产业规模或深圳产业总产值/增加值。统计对象、覆盖率门槛、年度可比、INB 映射、单位转换及快照年份须先会签；缺年份不能插值。 |
| G5/G6 企业规模 | 正式 `enterprise_type_scale_stats` 为空。`enterprise_base.org_size` 可统计全市截面：大型 1,125、中型 9,092、小型 42,938、微型 41,437、未知 1,008；该字段没有产业维度。 | 可支持全深圳注册企业的候选分布，不能直接支撑页面的产业筛选结果；需冻结分类真源、时间口径和产业关联。现有 `M_ENT_TYPE_COUNT` 是多标签企业分类，不是互斥的大/中/小/微桶。 |
| G4 区级发展指数 | 正式库没有现成一张图区级指数表。`M_CHAIN_REGION_INDEX` 注册定义是产业链 × 城市的模型，D3=partial、D4=mock，缺学术生态维度；不是深圳九区模型。 | 不能原样复用为区级指数。需业务确定“区综合”还是“产业 × 区”，并由指标口径与算法负责人会签定义后，另立计算实施任务。 |
| 目标汇总表 | 正式 `enterprise_stat_summary` 存在但为零行，唯一键为 `(stat_type, dim_code, stat_year, stat_date)`，`stat_value BIGINT`；`enterprise_type_scale_stats` 亦为零行，唯一键不含产业维度。`enterprise_industry_summary` 有 9 行，均为 2026 年当前快照，人数汇总为 0。 | 当前数据值没有可直接点亮的正式记录。G1/G4 若保留小数，BIGINT 会丢精度；不得直接截断。现有 `stat_type` 新增也不能代替存储层与访问层架构评审。 |
| 指标目录 | metric-registry 查无 `M_ONE_MAP_INDUSTRY_SCALE`、`M_ONE_MAP_DISTRICT_DEV_INDEX`、`M_ENT_GAP_03`、`M_ENT_GAP_03B`、`M_ENT_GAP_09`、`M_ENT_GAP_10`。已找到 `M_ENT_SZ_COUNT`、`M_ENT_REGIONAL_COUNT_TOPIC`、`M_ENT_REGIONAL_COUNT`、`M_ENT_TYPE_COUNT`；后者定义或需求范围不自动等于一张图产业筛选口径。 | 不得把 Java 常量占位当正式注册；由指标负责人决定复用、纠正引用或按注册流程正式化，确认 8 件套与 D1–D4。 |
| 产业目录 | Q068 记录从“20+8 / 八大未来产业”转向 10+5 共用 15 集群的临时默认仍标 🟡 待甲方 + PM 确认；一张图需规写八大，接口枚举文档同时列多于 8 个 INB 码。 | 本轮不自行选 8 个、15 个或接口全部枚举；需产品/PM/业务确认页面目录及集群—INB 映射。 |

## 架构与治理门禁

- `enterprise_stat_summary` 在现有存储文档中属于 DWD 通用汇总，不是 ADS 契约面；Java 只读 ADS、不得扫 DWD。当前 one-map 草案通过 Python internal summary 读取该表，需架构负责人确认这是已批准的访问例外，或先确定合规读面。此处只记录风险，不预设建表。
- D18 仅定义无法真实计算时的 mock ADS 兜底；不能把“加一个 `stat_type`”自动视为 D18 合规。真实来源、数据缺项表与演示 mock 应分别按 D16、D18 和标准 ADS 契约判断。
- `stat_date` 查询当前按每个 `stat_type` 的全局最大日期取批次。正式批量更新需保证同类完整快照一起发布；否则逐产业新批次会遮蔽其余产业的旧值。API-GAP 单已登记为后续依赖任务。
- 真实源营业收入用 `万元`，拟展示单位为 `亿元`；转换、汇总和可能的小数值必须在精度方案签收后处理。

## 尚待会签 / 阻塞

1. 需规 99 的页面产业集合、Q068 15 集群临时默认与 INB 编码映射。
2. G2/G3 深圳企业全口径员工人数的可信源、统计时点、缺失率处理和产业关系覆盖。
3. G1 “产业规模”正式语义（营业收入、产值或增加值）、允许覆盖率、深圳地域和年度可比口径。
4. G4 维度主键、指数公式、城市模型复用边界、原子指标与数据覆盖。
5. 缺失的一张图 metric_id 是否登记、已有指标是否可复用及其 readiness。
6. `enterprise_stat_summary` DWD 读取路径的架构裁定；如果方案涉及新表或改列，先提交具体 DDL / 影响 / 迁移与回滚方案并与用户沟通，未确认前不执行。

## 下一步建议

- 由产品 / PM 整理页面产业目录口径会签；由指标负责人确认 metric_id 和口径流程；架构负责人裁定 DWD / ADS 访问契约。
- G2/G3 暂不放行实施单，除非提供国内企业人数真实来源或书面改变需求口径。
- G1 先按 `enterprise_finance_history` 的年度来源和 INB 映射做候选完整性分析，不向外宣称全量产业规模。
- G4 另行会签指数定义；不得复用现有 `M_CHAIN_REGION_INDEX` 直接填九区。

## 验证与成本

- 验证：正式库 `information_schema` 结构核验 + 只读聚合统计；metric-registry MCP 指标核验；无写库动作。
- CI/CD：`cicd: skip`，本 handoff 是阶段性定义证据，尚无代码发布。
- 成本：本阶段执行模型 token / 实际费用由 registry handoff 流程回填；无数据库写入成本。
- 架构自检：Java 不写库 ✅；无 DDL / 灌数 ✅；凭据未记录 ✅；未改变 D4 ✅；待架构/产品/指标会签，暂不宣称签收。
