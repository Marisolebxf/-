> 第一轮试跑审稿（2026-11-10）。监管人要求按定稿规程重新试跑，本记录不再续写。§3、§4 是打断前的回应草稿，不是现行结论；重跑只可引用已核实的事实。

# 602 波次 B · 读法方案对抗审稿记录

- 被审稿：`POL-L2-PC1-CLEAN-FDE-B-读法方案.md`（arch-agent 起草，推荐方案 D）
- 规程：`产品实现规程.md` §4.2.4 多身份会签；清单 `.cursor/skills/gkx-fde-design-change/审稿硬清单.md`
- 审稿身份：data-agent（18 条，D-xx）、api-agent（22 条，P-xx），各自独立会话，只读
- 回应：arch-agent 逐条写在 §3

## 1. data-agent（结论：有条件支持 D）

| 编号 | 问题 | 依据 | 建议 |
|---|---|---|---|
| D-01 | 批次「失败」状态无数据来源；`script_state` 已移出，又无作业运行表 | 方案 §6-5；说明书 602-8 | 复用 `script_state` 加 `job=clean602` 行，或新建作业运行表 |
| D-02 | 规则目录（编码、名称、作用范围、阈值版本）放哪没写 | 说明书「六条都列出」 | 定为代码常量或配置表；事实表加 `rule_version` |
| D-03 | 「脱敏」对象未定义 | 602-7；方案 §6-7 | 样例只截命中字段前 N 字，正则遮手机号、邮箱 |
| D-04 | 正式贴源两表无行数证据：10-26 建成为 0 行，Wave A 未回签，`OPEN-POLICY-FLOW-01` 未关 | `SYSINT-06-03-DDL-L01`、`GDF-POLICY-WORKPACK-v2/05` | 方案 F3 补「行数未知」；有权限人做一次只读分组 COUNT |
| D-05 | lumen 运行时实际连 `demo_gkxlumenx_*`，与说明书写的 `gkxlumenx_ods` 冲突 | `LUMEN-POLICY-ABCDE-长任务总控.md` 37/73 行；element `application.yml` 33/55–56；`lumen-algo-py` `db.py` 81–83/98–99 | 人类裁定：demo 平面（说明书改 `{ods}` 占位）或正式平面 |
| D-06 | demo 海外源几乎空（DWD global 1 行） | `POL-L2-DS10-TREND-INGEST-FIX01` 21 行 | 用例写明海外可能空态，或先补海外贴源样本；禁 fixture |
| D-07 | 贴源为空与 ID 不存在分不开 | 说明书状态清单 | 检索接口另回各表行数或「源不可用」标记 |
| D-08 | 新 ADS 表直读 ODS、跳过 DWD，是流图新边 | `storage/POLICY/01-data-flow.md` | 数据稿在流图加边并写例外理由；数据平台 Owner 签 |
| D-09 | `assert_demo_mysql_targets()` 拒写非 `demo_` 库；走正式平面要改闸门 | `db.py` 74–90 | 写明写入平面；正式平面只放行 `policy_source_clean_*`，人类批准 |
| D-10 | 「去重合并」「格式标准化」易被理解为改源行 | `pipeline-source-to-ods.md` 禁止项；D16 | 硬约束：只读 ODS，只写事实表；产出「应合并 / 待标准化」标记；界面文案改判定口径 |
| D-11 | 表名库名写死 `gkxlumenx_ads`，与运行时不一致 | 同 D-05 | 库写 `{ads}` 占位并标本期平面；不进 gapfill（同意方案） |
| D-12 | 主键 `(source_plane,id,rule_code)`：未命中是否写行；重跑覆盖；接口须带 `source_plane` | `dwd.md` 79；`ods-to-dwd-mapping.md` 57 | 每行每规则写一行 `hit=0/1`；复查范围定为最近一次；接口传 `source_plane:id` |
| D-13 | 准确性 mock 行与真算行同表不合 D18 字面，且有伪闭合风险 | `architecture-baseline.md` 145；`gapfill.md` 83 | 另建 D18 表 `policy_source_clean_accuracy_mock`，或准确性显示空；批次状态排除 mock。人类架构师裁定 |
| D-14 | 采集范围未过滤 `is_deleted` / `is_history`，历史版本会被判重复 | `04-技术字段与过滤规则.md` 20；`dwd.md` 27 | 统一取 `is_deleted=0 AND IFNULL(is_history,0)=0`；非当前版本单独提示 |
| D-15 | 去重：海外无 `rank`，跨表键不成立；文号体系不同 | `ods-ddl.md` 66–103 | 同源内按规范化标题+文号(+级别)；跨源只按标题，标「跨源疑似重复」 |
| D-16 | 标准化：`publish_date` 是 DATE 无「非法」；PDF 判定条件偏；文号模式只适用国内 | `ods-ddl.md` 26–31/44–49 | 改为空、哨兵、年份不一致；看 `link` 是否 .pdf 且 content 空；海外标不适用 |
| D-17 | 噪声：附件字段多值格式未核实；乱码无 OCR 标记，只能启发式 | `ods-ddl.md` 48–49/84–85 | 波次 C 前抽 demo ODS 200 行核格式；乱码规则标「启发式」并记阈值版本 |
| D-18 | 一致性：区划维表 `OPEN-POLICY-DIM-01` 未定，部委词表无源；`rank` 出现「园区级」；海外无 `rank` | `01-data-flow.md` 230/241；`SZ3D-DATA-DEMO-L01` 62 | 改为 `rank` 与 `province/city/district` 填写对比；闭集外为「未知级别」；海外「不适用」 |

另：完整性成立，但海外两列 NOT NULL，命中大概率为 0；界面须分清「0」与「空」。

## 2. api-agent（结论：有条件支持 D）

| 编号 | 问题 | 依据 | 建议 |
|---|---|---|---|
| P-01 | `policyId` 是 DWD 键且 603 用它出摘要，不能装贴源 id | element `PolicyGovernanceController` 56–62/124–127 | 602 新增 `sourceIds`、`enabledRules` 多值；`policyId` 只留 603 |
| P-02 | 国内、海外 id 可能撞号 | 方案 F1、§7 | `sourceIds=dom:123`，或拆 `domesticIds` / `globalIds` |
| P-03 | 多值 GET 长度无上限 | 网关 / Tomcat 限制 | 上限（建议 50），超限 400；值由产品定 |
| P-04 | `status` 参数（`script_state` 六值）作废未处理 | display / element Controller | 契约标废弃或挂到 603 |
| P-05 | 结果接口给不出「ID 不在贴源」 | element 只读 ADS | 未命中只由候选检索按 id 精确查回 `notFound` |
| P-06 | 分不清「没校验」与「校验未命中」；`listOrEmpty` 吞错 | `ElementDao` 72–80 | 每 id 每规则写行；回命中数、已校验数、未校验数 |
| P-07 | 「失败」无来源 | 方案 §6-5 | 作业运行记录（ADS）回 `jobStatus` / `jobFinishedAt`，否则删「失败」并升级产品 |
| P-08 | 批次名、已选条数无服务端来源 | 方案 §4 | 前端生成批次名；接口回显 `selectedCount` / `resolvedCount` |
| P-09 | 规则行字段：样例条数、作用范围来源未定 | 说明书 602 功能点表 | 规则编码、作用范围（固定枚举）、启用、命中、已校验、isMock、样例≤N |
| P-10 | D18 mock 行要逐行 `isMock` | 铁律 10/16 | `isMock` 放规则行；混 mock 不得算「成功」 |
| P-11 | 页眉库内政策数读失败造 0 | element `countOrZero`；display `emptyResults()` 72–78 | 读失败回 null + 错误标记，本叶一并修 |
| P-12 | 前端 `policy.ts` 读不存在的 `policyOptions`；`status ?? 'success'` | `policy.ts` 93–96/162 | 前端实现叶点名删除 |
| P-13 | 读失败被吞成空，显示「无加工事实」 | display `call()`；element `listOrEmpty` | 响应按区块带 error；事实表读失败与 0 行区分 |
| P-14 | 空态统一 | 硬清单 3 | 未选不查库；无事实命中数用 null；检索空沿用 honesty 结构 |
| P-15 | 漏了公开接口；`PolicyGovernanceService` 注释写「不调 Python」 | display 类注释 | 新开 `GET /display/v1/policy/governance/source-candidates`，独立服务调 Python |
| P-16 | 意图拆解输出维度按 DWD 定，贴源无行业列 | `query-intent` 链路 | 复用现有 query-intent；Python 把筛选映射到贴源列，映射不上进 `honesty.ignored_fields`；algorithm-agent 确认 |
| P-17 | 规则启停是会话态还是持久化，说明书有歧义 | 说明书 245/250/284/296 行；全仓无启停落库 | 602 按会话态 `enabledRules`；作业照跑六条 |
| P-18 | 若持久化，写接口不能放展示系统 | display / element 纯读面 | 持久化归后台，另单；需人类裁定 |
| P-19 | 挂在 `RemotePolicySyncClient` 会继承 50 秒读超时 | `PolicyAlgoFeignTimeout` | 贴源检索独立 Feign，读超时约 5 秒；前端防抖 + 最小关键词长度 |
| P-20 | 候选分页未定；标题模糊 COUNT 全表扫 | `policy_routes.py` 358 | 每次只查一源，各自分页，回 `hasMore` 不回 total；id 查走主键 |
| P-21 | 降级三种情况要分 | `policy_routes.py` 1216–1254 | 意图失败退关键词并标降级；Python 不可用回 `error=true`；绝不回退查 DWD |
| P-22 | 正式贴源可能无行，候选线上恒空 | 方案 F3 | 诚实空态；演示是等贴源还是改连 demo（碰 D12）需人类裁定 |

## 3. arch-agent 回应

回应人：`agent:arch-agent`，2026-11-10。已回查 `polan/common/db.py`（ODS/DWD/ADS 默认 `demo_*`，`assert_demo_mysql_targets` 拒写非 `demo_`）、element `application.yml`、display `PolicyGovernanceService`（`emptyResults()` 回 0）、`PolicyAlgoFeignTimeout`（读超时 50 秒）、前端 `policy.ts` 93–96 / 162，异议所述属实。方案已按下表改写（见读法方案文末变更记录）。

统计：采纳 32，部分采纳 8（D-01、D-02、D-13、P-03、P-11、P-16、P-18、P-20），驳回 0。P-20 的依据行号不准，但风险成立，故不驳回。

| 编号 | 结论 | 理由或改法 |
|---|---|---|
| D-01 | 部分采纳 | 「失败」须有来源，采纳；不复用 `script_state`（DWD 表、键是 DWD `policy_id`，element 读它即触 D3），改为新建 ADS 作业运行表 `policy_source_clean_run`，并入裁定点 H3/H5 |
| D-02 | 部分采纳 | 规则编码、名称、作用范围定为 API 稿的闭集契约枚举（6 个），由 element 常量返回；阈值留 Python 常量，事实表加 `rule_version`；不建规则配置表 |
| D-03 | 采纳 | 样例只取命中字段、截前 40 字，遮手机号 / 邮箱 / 身份证号；规则写进方案 §5.4，细则归数据稿 |
| D-04 | 采纳 | F3 补「正式两表 10-26 建成 0 行，Wave A 未回签，行数未知」；有权限人做一次只读分组 COUNT，列入数据稿前置 |
| D-05 | 采纳 | 运行时确连 `demo_gkxlumenx_*`，与说明书 `gkxlumenx_ods` 冲突；方案改用 `{ods}` / `{ads}` 占位，平面选择并入 H1 |
| D-06 | 采纳 | 用例与空态写明「海外源可能空」，禁 fixture；补海外贴源样本归数据稿，不在本方案造数 |
| D-07 | 采纳 | 候选检索按源回 `sourceAvailable` 与该源当前行数，区分「贴源为空 / 不可用」与「ID 不存在」 |
| D-08 | 采纳 | ODS→ADS（跳过 DWD）是流图新边，方案标明例外理由（只读校验、不改主数据）；数据稿加边，数据平台 Owner 签，并入 H3 |
| D-09 | 采纳 | 写入平面写明；若走正式平面，闸门只放行 `policy_source_clean_*` 三张表，须人类批准，并入 H1 |
| D-10 | 采纳 | 硬约束：只读 ODS、只写事实表；规则输出改为判定标记（「疑似重复 / 待标准化 / 疑似噪声」），界面文案同步改为判定口径，交 product-agent |
| D-11 | 采纳 | 表名一律写 `{ads}.policy_source_clean_*`，不写死库名；不进 gapfill |
| D-12 | 采纳 | 每行每规则一行，`result ∈ hit / pass / na`；重跑覆盖，只保留最近一次并记 `run_id`；接口用 `dom:` / `gbl:` 前缀传源 |
| D-13 | 部分采纳 | 同意同表混 mock 不合 D18 字面，删去原「同表 `is_mock`」推荐；改为两个选项（另建 D18 表 / 显示空）交 H4，批次状态一律排除 mock |
| D-14 | 采纳 | 校验与候选统一过滤 `is_deleted=0 AND IFNULL(is_history,0)=0`；历史版本不参与判重 |
| D-15 | 采纳 | 同源内按规范化标题 + 文号（国内再加 `rank`）；跨源只按规范化标题，标「跨源疑似重复」 |
| D-16 | 采纳 | 日期改判空、哨兵（1970-01-01 / 1900-01-01）、`publish_year` 与日期年份不一致；PDF 看 `link` / `appendix_link` 为 .pdf 且 `content` 空；文号模式海外记 `na` |
| D-17 | 采纳 | 波次 C 前抽 200 行核附件多值格式；乱码规则标「启发式」，阈值进 `rule_version` |
| D-18 | 采纳 | 一致性改为 `rank` 与省 / 市 / 区填写层级对比；闭集外级别记 `na`（未知级别，不计命中）；海外整条 `na`；不依赖未定的区划维表与部委词表 |
| P-01 | 采纳 | 602 新增 `sourceIds`、`enabledRules` 多值参数；`policyId` 只留给 603 摘要 |
| P-02 | 采纳 | 单参数带前缀 `sourceIds=dom:{id}` / `gbl:{id}`，比拆两参数少一个字段 |
| P-03 | 部分采纳 | 加上限、超限 400，采纳；建议值 50，最终数由产品定，并入 H8 |
| P-04 | 采纳 | `status` 对 602 标废弃，随 `script_state` 一起归 603 稿 |
| P-05 | 采纳 | 「不在贴源」只由候选检索按 id 主键精确查回 `notFound`，结果接口不承担 |
| P-06 | 采纳 | 每 id 每规则写行；规则行回 `hitCount / checkedCount / uncheckedCount / naCount`；事实表读失败不走 `listOrEmpty` 吞错 |
| P-07 | 采纳 | 同 D-01：作业运行表回 `jobStatus / jobFinishedAt`；若不建运行表则删「失败」并升级产品（H5 选项二） |
| P-08 | 采纳 | 批次名前端生成（选择时间 + 条数）；接口回显 `selectedCount / resolvedCount` |
| P-09 | 采纳 | 规则行字段定为：`ruleCode / ruleName / scope / enabled / hitCount / checkedCount / uncheckedCount / naCount / isMock / samples(≤N)`；N 默认 3，产品可改 |
| P-10 | 采纳 | `isMock` 放规则行；含 mock 的规则不参与「成功」判定 |
| P-11 | 部分采纳 | 缺陷属实（`countOrZero` 与 `emptyResults()` 都回 0），同一资源同页，列入实现叶需同步；不在架构方案里写代码 |
| P-12 | 采纳 | 列入前端实现叶需同步：删 `policyOptions` 回退与 `status ?? 'success'` |
| P-13 | 采纳 | 响应按区块带 `error` 标记；display `call()` 失败不再整体回空壳，事实表读失败与 0 行区分 |
| P-14 | 采纳 | 未选不查库、区块为 `null`；无事实命中数为 `null` 不为 0；检索空沿用 `honesty` 结构 |
| P-15 | 采纳 | 新开 `GET /display/v1/policy/governance/source-candidates`，由独立 display 服务 + 独立 Feign 调 Python；`PolicyGovernanceService`「不调 Python」保持不破 |
| P-16 | 部分采纳 | 复用 `query-intent`，贴源无行业列时进 `honesty.ignored_fields`；映射表由 algorithm-agent 在波次 C 确认，不在本方案定 |
| P-17 | 采纳 | 602 规则启停按会话态 `enabledRules`；校验作业始终跑六条 |
| P-18 | 部分采纳 | 同意「若持久化，写接口不进展示系统」；是否持久化属产品口径，并入 H6，本方案按会话态写 |
| P-19 | 采纳 | 贴源检索独立 Feign，连接 3 秒、读 5 秒；前端防抖 300ms、关键词至少 2 字 |
| P-20 | 部分采纳 | 方案采纳：每次只查一源、各自分页、回 `hasMore` 不回 total、id 走主键；所引 `policy_routes.py` 358 行是缺项目录检索的分页钳制，并非 COUNT 全表扫，依据行号不准，但风险本身成立 |
| P-21 | 采纳 | 三种降级分开：意图失败退关键词并标 `degraded`；Python 不可用回 `error=true`；任何情况不回退查 DWD |
| P-22 | 采纳 | 正式贴源无行时诚实空态；演示连哪个平面并入 H1，由人类裁定 |

## 4. 分歧与人工裁定点

以下各点 agent 不代选。推荐项放第一位，标「（推荐）」。

### H1 库平面：602 读写连 demo 库还是正式库（D-04、D-05、D-06、D-09、D-11、P-22）

问题：lumen 运行时实际连 `demo_gkxlumenx_*`，正式 `gkxlumenx_ods` 两表 10-26 建成 0 行且 Wave A 未回签；602 的候选与校验写哪个平面。

| 选项 | 做法 | 影响层 | 代价 | 风险 |
|---|---|---|---|---|
| 1（推荐） | 代码只写 `{ods}` / `{ads}` 占位；本期部署连 demo 平面，登记为 element 既有临时豁免的延续；切换条件写死：正式两表只读 COUNT>0 且 Wave A 回签后，只改环境变量切正式 | Python 配置、element 配置、说明书改占位 | 豁免多挂一项，须写切换条件 | 豁免拖成常态；演示数是 demo 贴源，不是正式贴源 |
| 2 | 直接走正式平面：Python 闸门只放行 `policy_source_clean_*` 写正式 `gkxlumenx_ads` | Python 闸门、DBA 授权 | 改闸门、开写权限 | 贴源未到位前候选线上恒空，602 演示用例跑不过 |
| 3 | 等正式贴源回签后再实现 602 | 排期 | 602 推迟 | 挂在 `OPEN-POLICY-FLOW-01` 上，无确定日期 |

推荐理由：代码零改动即可切换，演示不被贴源排期卡住，豁免有明确退出条件。
裁定：**人类架构师**（D3 / D12 豁免），**数据平台 Owner**（平面与写权限）。

### H2 读法选型：A / B / C / D（原方案 §6-1）

问题：两位审稿身份均「有条件支持 D」，条件已在 §3 采纳；仍须人类架构师确认选型。

| 选项 | 做法 | 影响层 | 代价 | 风险 |
|---|---|---|---|---|
| D（推荐） | 候选走 Python 读贴源；校验离线写 ADS；element 只读 ADS | algo-py、display、element、数据 | 新建 2 张表（另见 H4） | 一页两条读链，契约须写清 |
| A | ADS 贴源目录 + 事实表，Java 只读 ADS | 数据新同步、element | 多一条同步链、工作量最大 | 目录延迟，像第二张政策主表 |
| B | Python 实时检索 + 实时算命中 | algo-py、display | 不建表 | 请求内全表扫；命中不落库不可复查 |
| C | 书面豁免 D3，element 直读 ODS | element 配置、Nacos | 仍需事实表 | 开 Java 读贴源先例 |

推荐理由：唯一同时不破 D3、候选实时、命中可复查的方案。
裁定：**人类架构师**。

### H3 新建正式表与流图新边（D-01、D-08、P-07）

问题：方案 D 需新建 `{ads}.policy_source_clean_hit`（规则事实）与 `{ads}.policy_source_clean_run`（作业运行），并在流图加一条 ODS→ADS、跳过 DWD 的边。

| 选项 | 做法 | 影响层 | 代价 | 风险 |
|---|---|---|---|---|
| 1（推荐） | 两表都建；流图加边，注明「只读校验，不改主数据」例外 | 数据、Storage、流图 | 2 张表 DDL + 调度登记 | 例外边被他域援引，须写明适用条件 |
| 2 | 只建事实表，不建运行表；批次状态不出「失败」 | 数据 | 1 张表 | 说明书 602-8「失败」无法呈现，须产品改口径 |
| 3 | 复用 DWD `script_state` 加 `job=clean602` 行 | 数据、element | 不建运行表 | element 读 DWD 触 D3；键是 DWD `policy_id`，贴源行装不进 |

推荐理由：运行表很小，是「失败」与「更新时间」的唯一诚实来源。
裁定：**数据平台 Owner**（建表、新边），监管人确认。

### H4 准确性校验没有原文比对能力（D-13、P-10）

问题：准确性需原文比对，现在做不到；602-7 要求三行各有命中与失败样例。

| 选项 | 做法 | 影响层 | 代价 | 风险 |
|---|---|---|---|---|
| 1（推荐） | 另建 D18 表 `{ads}.policy_source_clean_accuracy_mock`，Python 写 mock 行，element 读表，规则行 `isMock=true` 挂 MockBadge，不计入批次状态 | 数据、algo-py、element | 再多 1 张表与 1 个灌数入口 | 演示时 mock 被当真数；须评审层门控 |
| 2 | 准确性行显示空（未校验），不写 mock | 无 | 零 | 602-7 覆盖不足，§6.4 用例该行不过，须产品认可 |
| 3 | 与真算行同表，用 `is_mock` 区分 | 数据 | 不加表 | 不合 D18「新建 ADS 表」字面，伪闭合风险（审稿已否） |

推荐理由：合 D18 字面，又让 602-7 有可呈现的行。
裁定：**人类架构师**（D18 解释），**产品**（是否接受空）。

### H5 批次状态与「失败」口径（D-01、P-07、原方案 §6-5）

问题：成功 / 部分 / 失败 / 空 怎么判。

| 选项 | 做法 | 影响层 | 代价 | 风险 |
|---|---|---|---|---|
| 1（推荐） | 未选 → 空；已选 id 在启用真算规则下全无事实 → 空；最近一趟作业失败且有 id 未覆盖 → 失败；有 id 未校验 → 部分；全部已校验 → 成功；mock 规则不参与 | element 聚合 | 依赖 H3 运行表 | 「部分」可能常见（新进贴源未校验），须产品认 |
| 2 | 只有 成功 / 部分 / 空，删去「失败」 | 说明书 | 不建运行表 | 偏离 602-8 原文 |

推荐理由：每个状态都有落库来源，不造成功。
裁定：**产品**（监管人可拍，涉甲方口径转客户决策清单）。

### H6 规则启停是会话态还是持久化（P-17、P-18）

| 选项 | 做法 | 影响层 | 代价 | 风险 |
|---|---|---|---|---|
| 1（推荐） | 会话态：`enabledRules` 只是读条件，刷新回默认全启用；作业照跑六条 | 前端、element | 零写接口 | 用户以为停用被保存 |
| 2 | 持久化：后台管理系统另开写接口与配置表，展示系统只读 | 后台、数据、element | 新写接口、新表、新单 | 扩范围，须 PM 核 ±10% |

推荐理由：说明书只说「可启用、停用」，未说保存；读面不应长出写接口。
裁定：**产品**；选 2 时转 **PM**（范围）。

### H7 说明书前提修正（原方案 §6-4、D-10）

问题：说明书 602 写「对照第 6 项已落库的清洗事实」「不新建清洗管道」「element 只读两张 ODS」，均与方案 D 冲突；规则名「去重合并」「格式标准化」易被理解为改源。

| 选项 | 做法 | 影响层 | 代价 | 风险 |
|---|---|---|---|---|
| 1（推荐） | product-agent 改写三处前提；「不新建清洗管道」改为「新增只读校验作业，不改贴源与主数据」；规则行文案改为判定口径（疑似重复 / 待标准化 / 疑似噪声） | 说明书、高保真文案 | 中档内一次回写 | 需体验 Owner 复核文案 |
| 2 | 保留规则名，只在作用范围列加「仅判定，不改源」 | 说明书 | 改动少 | 误解仍在 |

裁定：**监管人**（产品口径）。

### H8 产品参数：多选上限、样例条数、脱敏（P-03、P-09、D-03）

| 选项 | 做法 | 影响层 | 代价 | 风险 |
|---|---|---|---|---|
| 1（推荐） | 上限 50、每规则样例 3 条、样例截 40 字并遮手机号 / 邮箱 / 身份证 | API、前端、数据稿 | 零 | 50 对演示够用，批量场景不够 |
| 2 | 上限 200，改 POST 查询 | API、网关 | 读面改 POST，偏离现有 GET 习惯 | URL 外的查询难以缓存与复现 |

裁定：**产品**。

### H9 element 既有 D3 / D12 临时豁免（原方案 §6-6）

| 选项 | 做法 | 影响层 | 代价 | 风险 |
|---|---|---|---|---|
| 1（推荐） | 另开技术债单；602 不新增对 DWD 的读取，并移出 `script_state` | 注册表、element | 一张新单 | 豁免继续存在 |
| 2 | 本叶顺带消除（页眉件数也改读 ADS） | element、数据 | 需 ADS 件数表或镜像 | 扩大本叶范围 |

裁定：**人类架构师**。
