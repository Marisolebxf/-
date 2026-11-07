ponytail: full

# TS-DS03-CASE-FILL-L01 · 技术发展跟踪（DS-03）合规演示用例填实 handoff

> **日期**：2026-11-07 ｜ **任务**：TS-DS03-CASE-FILL-L01 ｜ **对象**：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS03-合规演示用例.md`
> **口径**：网关 `http://10.50.69.111:30895`（StripPrefix=1，无 token 即 200）；curl.exe、`--max-time 40`、**只读探测**（未建评估任务、未写模板/报告）。前端注记「后端无 tracking 控制器」等旧记录一律作废，以本日实测为准（与对齐表 §6.1 DS-03 行一致）。

---

## 1. 探测记录（13 次请求全部 200，零受阻）

| # | 端点 | 方法/参数 | 状态 | 关键返回 |
|---|---|---|---|---|
| 1 | `/display/v1/situation/tracking/meta` | POST `{}` | 200（4.2s） | timeline 2000–2025（26 年，currentYear=2025）；geoDrillLevels=全球/国家/区域；mapTechnologyTypes=6 类；mapRegionCascadeOptions=100 城市；bubbleAxisOptions=12 维；historyMatrix=3 期×3 方法；parameterTemplates=9；noSourceFields=[timeline.events, capabilities, methods, knowledgeBase] |
| 2 | `/display/v1/situation/industry-domains` | POST `{}` | 200（1.1s） | 15 集群全集（10 战略性新兴 CL-SEI-01~10 + 5 未来产业 CL-FUT-01~05）；mapped=9，pending_vendor=6（新能源/新材料/高端装备/绿色环保/海洋产业/未来能源） |
| 3 | `/display/v1/situation/tracking/dataset` | POST `{}` | 200（11.6s，416KB） | isEmpty=false；records/hotTopics/heatMatrix/bubbles 各 20；relations=18；mapRegions=100；years=26；heatMatrixYears=11（2015–2025）；metrics=4（论文 858,620 / 专利 71,043 / 项目经费 null / 人才 159,546）；noSourceFields=[workflow, summary, sliceSummary] |
| 4 | 同 dataset | `timeRange 2020–2025` | 200 | years=6（2020–2025），时间窗生效 |
| 5 | 同 dataset | `fieldValues=["CL-SEI-01"]` | 200 | scopeEffectNote「已生效（反查 420 Topic / 12 子学科，年度趋势按 topic_ids 过滤）」；trend 序列与默认不同 |
| 6 | 同 dataset | `fieldValues=["CL-SEI-02"]` | 200 | trend 序列与 CL-SEI-01 不同，领域过滤真实生效（仅趋势/热力图列） |
| 7 | 同 dataset | `regionKeys=[深圳 loc_E167…]` | 200 | scopeEffectNote「区域范围：已生效（年度趋势按所选城市 location_id 过滤）」 |
| 8 | 同 dataset | `keyword="基因"` | 200 | mapRegions=0、图例清空——keyword 过滤的是**城市名**，不过滤话题记录 |
| 9 | 同 dataset | `selectedMapTechnologyTypeKeys=[机器学习加速硬件架构]` | 200 | mapRegions 100→57，图例过滤生效 |
| 10 | 同 dataset | `mapDrillLevel=country / region` | 200 | 返回层级标注；`activeGeoParentKey` 未被后端消费（drill 仅标注） |
| 11 | `/display/v1/situation/tracking/parameter-templates` | GET | 200 | items=9（自定义 4 落库 evaluation_template + 系统内置 5）；note 明示落库口径 |
| 12 | `/display/v1/situation/tracking/reports?limit=5` 与 `/display/v1/situation/report/list?reportType=tracking` | GET | 200 | **items=0（均无已生成报告）** |
| 13 | `/display/v1/situation/tracking/evaluation/{历史taskId}/progress` 与 `/result` | GET | 200 | progress 返回 code=1「任务不存在或已过期」；result records=0——**任务进度/结果为内存态，历史不可回放** |

**探测受阻**：无（首次 2 次 400 为本机 PowerShell 引号转义问题，改 JSON 文件提交后全通，非接口故障）。

---

## 2. 逐行判定（8 行零缺格：可演 7 / 部分可演 1 / 覆盖不到 0 / 待开发 0）

| 序号 | 界面 | 判定 | 依据 |
|---|---|---|---|
| 48 | 话题热力图 | **可演** | heatMatrix 20×11 真实；时间窗/领域实测生效；run 有 3 条落库运行记录佐证；⚠️ 进度条须现场新起任务（历史 taskId 已过期） |
| 49 | 地理分布图 | **可演** | mapRegions=100 城市（经纬度/评估值/证据来源）；图例勾选 100→57 生效；⚠️ 全球城市点位口径，非行政区着色 |
| 50 | 动态气泡图 | **可演（带口径警示）** | bubbles=20 八项评分；⚠️ 被引数/人才数/项目数三轴 max=0 无数据；investment 全为 RULE_SIMULATED 规则模拟 |
| 51 | 弦线图 | **可演** | relations=18，类型全集=知识依赖/专利趋同 |
| 52 | 评估流程概览 | **可演** | 纯前端静态；dataset.workflow=[] + noSourceFields 明示无后端源 |
| 53 | 评估方法详解 | **可演** | 前端静态 4 法（expert/economic/operations/comprehensive）；⚠️「按技术类型自动推荐」未提供（knowledgeBase 空） |
| 54 | 评估参数配置 | **可演** | GET 200：9 模板（5 系统 + 4 自定义落库）；保存/删除端点代码存在（TrackingController.java:1452），只读口径未实测写 |
| 55 | 评估结果追踪 | **部分可演** | 可演：historyMatrix 3 期×3 方法落库矩阵，并排 ≤3 期恰好；覆盖不到：报告产物 items=0（生成须现场触发写操作）；历史 taskId 结果过期 |

---

## 3. 条件全集枚举结果（全部有实测出处）

- **评估范围·区域**：regionCascadeOptions / mapRegionCascadeOptions = **100 全球城市**（北京市/上海/南京市/广州市/武汉/杭州市/西安/成都市/深圳/天津市/London/长沙/合肥市/济南市/Hong Kong/青岛市/重庆市/哈尔滨市/Paris/New York/Cambridge/郑州市/长春/Boston 等）。⚠️ 与用例旧稿「大湾区 11 城/深圳各区县」冲突，已按实测改写。
- **评估范围·时间**：2000–2025 共 26 年任意区间（currentYear=2025；实测 2020–2025 生效）。
- **评估范围·领域**：产业领域级联 15 集群（CL-SEI-01~10 + CL-FUT-01~05），其中 6 个「未映射产业（pending_vendor）」选中不参与取数。
- **地图层级**：global / country / region 三级。
- **技术类型图例**：6 类全集（机器学习加速硬件架构 264 / 基因组数据分析计算工具 173 / 生物序列比较计算方法 142 / 生物图像分析开源软件 103 / 生物通路数据库与网络分析 94 / 原子材料结构的计算建模 74）。
- **气泡轴维度**：12 维全集（潜力综合分/热度指数/科学增长/科学影响/科学规模/产业参与/项目证据/专利转化/论文数/被引数/人才数/项目数；后三者 max=0 无数据）。
- **弦线关系类型**：知识依赖 / 专利趋同（18 条实测枚举）。
- **评估方法**：expert 专家评估法 / economic 经济分析法 / operations 运筹学评价法 / comprehensive 综合评价法（历史矩阵已出现 3/4，economic 暂无历史期）。
- **参数维度**：maturity 技术成熟度 / potential 产业化能力 / activity 创新活跃度 / trend 发展趋势 / policy 政策关联度（权重合计 100、阈值 0–100 服务端校验）。
- **参数模板**：9 个全集（系统内置 5 + 自定义 4，key 已列用例）。
- **历史期数**：3 期（11-04 22:03、11-07 15:12 ×2），并排上限 3 期恰好覆盖。

---

## 4. 对用例文件的其他改动说明（非数据情况列）

1. 文件头状态行 →「M2/M3 已填·2026-11-07」，新增证据口径引用块（与 DS-01 同格式）。
2. 序号 48「输入或选择」列：旧稿「区域（大湾区 11 城 / 深圳市及各区县）」与实测（100 全球城市）冲突，按实测改写——**属旧记录错误，非笔误，已在此声明**。
3. 备注与风险 4 条旧记录按实测订正：范围三要素生效边界（仅趋势+热力图列，榜单不随领域变化）、49–51 落地确认、52–53 静态确认（自动推荐未提供）、任务进度内存态。其余列（触发/接口/请求/期望输出）与需规序号未动。

## 5. 遗留问题（需人工/开发确认）

1. **主路径与实测口径张力**：主路径写「区域=深圳市」，深圳在 100 城市级联内可选且生效于趋势；但榜单/六维为全局模型产出，甲方若问「选深圳后榜单为何不变」，须按 scopeEffectNote 口径答（全局模型产出，趋势按城市过滤）。**建议演示脚本把「开始分析」后的看点落在趋势/热力图列变化上**。
2. **evaluation/run 未实测**（写操作建任务，超出只读口径）：端点有 3 条落库记录佐证链路真实，但现场首次点击的耗时/进度表现未验证，建议正式演示前空跑一次。
3. **报告链路零产物**：tracking/reports 与 report/list 均 items=0；序号 55「生成报告」只能现场触发，且同条件复用（reused=true）。
4. **3 个气泡轴无数据**（被引数/人才数/项目数 max=0）与**项目经费 metric=null**：演示选轴须避开或按「该维度无源」明示。
5. **6 个未映射产业集群**（新能源/新材料/高端装备/绿色环保/海洋产业/未来能源）选中不取数，演示勿选。
