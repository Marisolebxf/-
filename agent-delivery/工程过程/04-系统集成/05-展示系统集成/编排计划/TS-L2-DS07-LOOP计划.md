# TS-L2-DS07 科技创新评估 · 演示样本循环（LOOP）计划

> 依据：`产品实现规程.md` §6.5（含 §6.5.7）。用例真源：`../合规演示用例/TS-L2-DS07-合规演示用例.md`（23 行，2026-11-09 已回写 M4 裁定）。
> 验收单：`TS-DS07-DEMO-ACCEPT-LOOP`。监管人：human:李伟。
> **前置已解**：G1（算法库路由）2026-11-08 修复并发布，生产实测四维出分（pipeline 4305 / 4306）。

## 状态行（每轮回写）

| 轮次 | 日期 | 探测 | 对得上 | 缺口 | 子任务 | 结论 |
|---|---|---|---|---|---|---|
| R0 | 2026-11-09 | meta 200（9.4KB）/ snapshot 200（205KB，8.3s） | 四维出分 19.6 / 36.6 / 50.0 / 63.4；techPatent 三榜各 200 | 覆盖表 23 行仍按 G1 修复前填写，待重判 | — | **待 R1 复跑重填** |
| R1 | 2026-11-09 | meta 200（1.9s / 8.4KB）；snapshot 200（8.2s / 198.7KB） | **11 可演 / 7 部分可演 / 5 覆盖不到**（23 行逐行见 §5） | ①生产 payload 缺 `industrySciInfluence`、`projectSupport` 两块（源码 `InnovationEvaluationController.java` L296/L470/L537 已有）→ 疑似 display 未发布最新版；②四维 `weights` 全 0（无权重模型）；③`spatialByDimension` 四维全空；④137/138 仅有总分值、无图谱/主题明细 | DSP-M4-FIX-03（149/155 归属部署）、FIX-07（权重）已派 | **R1 完成·不申请签收（待确认部署版本后复测）** |
| R2 | 2026-11-09 | token 换新后复测：meta 200 / 1.8s / 9.9KB；snapshot 200 / **0.19s** / 31.8KB → **空态壳**：`dimensions[0]`、`techPatent` 三键空对象、`spatialByDimension` 四维全空、`weights` 四维全 0、`policySuggestions[0]`、`sciForecast.domains[0]`，`noSourceFields` 10 项挂空；仅 `spatialRows`/`spatialRegions` 各 100 行城市统计与 `dataSourceNote` 为真值。VPN 恢复后二测：meta 200 / 2.4s；snapshot 200 / 0.17s / **31.8KB 与首测字节级一致**；`updatedAt` 逐次变化 + `Cache-Control: no-store` 排除缓存；`techPatent` 三键 `ConvertTo-Json` 实证 `{}`。另内网网关 `10.50.69.111:30895` 本机不可达（curl exit 28）无法交叉验证 | 0/23 可复判（较 R1 四维出分 19.6/36.6/50.0/63.4 与 techPatent 三榜 200 **明显退化**） | **断链实锤、与用户 VPN 无关**（VPN 断/恢复两测字节级一致）：经算法库 innov-py 的块（dimensions / techPatent / spatialByDimension / sciForecast / policySuggestions / methodEvidence）全空，不经算法库的 Doris 直查块（spatialRows / spatialRegions 各 100 行）正常 → 生产 show-py → innov-py 通道断，快速失败 0.17s（R1 通道正常时 8.2s）；R1 缺口①②③④（缺 industrySciInfluence/projectSupport、weights 全 0、spatialByDimension 空、137/138 无明细）均无法核验 | **根因实锤（SQL 探针 + innov-value 探针）**：①SQL/数据层全通——本机直连久新 Doris（47.93.119.170:29030）：TCP 0.09s、握手 0.35s、`ads_patent_profile` 176.9 万件、有效 IPC 158.7 万、质量榜 SQL 7.08s 返回 200 行真值（A61K 22.7 万件）、趋势 SQL 5037 行；②innov-py 服务整体不可达——经 `POST /v1/situation/global-innovation/innov-value`（直透 algoScienceClient.compute，失败带 emptyReason）分别探 DS-04 `M_INNOV_POINT_VALUE` 与 DS-07 `M_TECH_DS_07_TECH_INNOV_002`，**双指标同报 `DOWNSTREAM_UNREACHABLE`** → display → `gkxlumen-platform-innov-py:8000` 连接失败，DS-04/DS-07 算法指标块共因全空（DS-04 昨日签收时为绿，今日环境退化）；③kubectl 本地代理 127.0.0.1:16443 未监听，无法直查 Pod 状态 | **集群侧查/重启 `gkxlumen-platform-innov-py` Pod**（疑似 CrashLoopBackOff 或副本为 0，Feign 头注曾记 2026-11-08 同症状：无实例 → 静默降级空） | **blocked（新一轮）· R1 判定 11/7/5 维持 · 不重判 23 行 · 不申请签收** |
| R3 | 2026-11-09 | innov-py Pod 恢复后复测：PIV 200 / 3.7s / 5.2KB（DS-04 复验 ✓ 真数据）；meta 200 / 1.3s / 9.9KB；snapshot 200 / **8.0s / 211.9KB**（恢复 R1 体量） | **12 可演 / 7 部分 / 4 覆盖不到**（155 解除，§5 同步） | ①`projectSupport` **已出真值**（NSFC 代理口径：dwd_zh_project 58,453 项 / score 42.9 / 资助额 mean 43.27 万·median 30·max 920 / 类别 面上 27,939·青年C 23,884·地区 2,634·专项 1,058·重点 962）→ 155 转 ✅；`industrySciInfluence` **仍缺**（data keys 无此 key）→ 149 维持 ❌，按约定建后端缺陷单；②四维 `weights` 仍全 0 → 143/151/157 维持 ⚠️（FIX-07 未落地）；③`spatialByDimension` 四维 0 行 + ④137/138 明细缺——`noSourceFields` 10 项已如实声明，确认为**设计空态非缺陷** | 149 建单（industrySciInfluence 缺块）；FIX-07 权重模型 | **R3 完成·不申请签收（12/7/4；残余均为后端项：149 缺块 + FIX-07 权重）** |
| R4 | 2026-11-09 | FIX-09 算法侧落地（vendor/innov-py v2，commit `84ff427`，pipeline 4552 / job 33813 构建、33819 部署成功）后复测：snapshot 200 / **214.8KB**（含 `industrySciInfluence` + `projectSupport` 两块）；meta 200 | **13 可演 / 7 部分 / 3 覆盖不到**（149 解除，§5 同步） | ①`industrySciInfluence` **已出真值**：15 集群、score 74.9、合计 5,826,738 篇 / 114,379,101 被引，top1 CL-SEI-01 612,431 篇 / 12,765,905 被引 → 149 转 ✅；`gaps` 错误归因（原「256MB 内存硬限」）已更正为「FE 30s 单查询硬限 + CRC32 无损分片」；②四维 `weights` 仍全 0 → 143/151/157 维持 ⚠️（FIX-07 未落地）；③④维持设计空态 | FIX-07 权重模型；口径文档待补 v2（已登记） | **R4 完成·不申请签收（13/7/3；残余仅 FIX-07 权重 + 口径文档，均非算法链路）** |
| R5 | 2026-11-10 | FIX-07 权重模型发布（svc `a843b09` pipeline 4597 / `deploy:display` 34316 ✅ + FE `7dd8ada` pipeline 4596 `deploy:k8s` ✅）后生产实测 snapshot 200 | **17 可演 / 4 部分 / 2 覆盖不到** | ①四维 `weights` 全 0 已解除 → **143/151/157 转 ✅**：默认 25/25/25/25 非 0、`weightCoverage` 100，`composite` = **41.4**（技术 19.4 / 科学 36.6 / 产业 50.0 / 政策 59.4，分项贡献 4.9·9.2·12.5·14.9）；改 40/30/20/10 → 后端重算 **36.4**；110% 非法 → `weightsValidation.valid=false` 且不产出综合分；②`industryRanking` **48 行**（rank 1–48 连续、score 降序、无空无 0，top1 计算机通信电子 75.42 / 末位农业 27.8）→ 143/151/157 解除；③残余 137/138/142/144 部分可演（图谱·前沿主题·市场诉讼·空间分维无源）+ 150/158 覆盖不到 | — | **R5 完成·不申请签收（17/4/2；残余仅 SUP-02 的 150 与 SUP-01 的 158）** |
| R6 | 2026-11-10 | SUP-02 发布（svc `1d3a70e` + `dfb3a88`，pipeline 4607/4609，`backend:image:display` 34426 + `deploy:display` 34437 ✅）：display 改走 entan-py `POST /v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_005/compute` | **17 可演 / 5 部分 / 1 覆盖不到**（150 由 ❌ 转 ⚠️） | ①根因：`M_ENT_*` precompute 只烘焙在 entan 镜像，原打 innov-py 必空；②`industryTechInfluence` 出真值 **score 24.3**、`axes` 2 轴（`sep` = `pending` → 置灰「未测」）、`chains` 12（9 条有专利、3 条 0 件不参与加权）、覆盖 citedRows **20,515** / linkedChainPatentN **190** / linkedChainCitedSum **415** → 150 转部分可演；③残余仅 158 | SUP-01 | **R6 完成·不申请签收（17/5/1；仅余 158）** |
| R7 | 2026-11-10 | SUP-01 三仓落地并发布（algo `display_policy_suggestion_routes.py` + svc `PolicySuggestionService` Redis 异步 + FE `PolicySuggestionCard` 中间态）：`generate` → 轮询 `status` | **18 可演 / 5 部分 / 0 覆盖不到** | ①`policySuggestions` **5 条**、`degraded=false`、每条带 evidence（metricId + value + caliber）→ **158 转 ✅**（建议卡带「模型生成·非评估结论」角标，不参与计分/排名/覆盖率）；②同用户同条件当天 `status` 二次调用直接返回旧结果（单飞 + 缓存直开，不重复调模型）；③首轮曾因事实校验过严（年份/序号/百分比误杀）+ 模型单对象输出判 `bad_schema` 降级，已修为「正文只校验小数 + evidence 值白名单校验 + 结构抽取容错」并复测通过；④`methodEvidence` 仍空态（德尔菲/仿真方法依据未提供，演示口径列「未提供」） | — | **R7 完成·已签收（18/5/0，2026-11-10 · human:李伟）** |

## 1. 探测（每轮第一笔，只读）

1. `POST {网关}/display/v1/situation/innovation-evaluation/meta`，body `{}`，头 `Authorization: Bearer <本机 token>` + `systemCode: display`；
2. `POST {网关}/display/v1/situation/innovation-evaluation/snapshot`，body 同 `{}`（空筛选即全量口径）。

- 生产网关 `https://edu.itic-sci.com/tid/api`（注意必须带 `/tid` 前缀，否则整站 500）；内网 `http://10.50.69.111:30895`。
- token 读本机凭据文件，不打印、不入库。
- **熔断**：401/424 → blocked 并通知监管人；404 → 「接口映射不存在」停止；200 才进对照。
- **性能红线**：snapshot 单次约 8.3s，超过 15s 记性能缺陷（不判数据缺口）。

## 2. 用例集（R1 全量重判 23 行）

覆盖表 23 行原按「G1 未修」全部标 ❌，R1 必须逐行按实测重判，判定以各行「期望输出」为准。要点：

| 序号 | 内容 | R1 判定要点 |
|---|---|---|
| 136 | 科学影响力 | 应出分（R0 实测 36.6）；非空即由 ❌ 升 ✅ |
| 137 | 网络中心性 | 无独立端点（G8）；知识图谱页可演、网络中心性维按空态讲 → 部分可演（不建补数单） |
| 138 | 技术前沿性 | `frontier_ratio` 有值即可演 |
| 139 | 科学趋势预测 | `forecast` 段有值（注意年度断档，见 §4） |
| 140–141 | 技术创新力 | 维分 19.6；141 于 FIX-01 后 **5 维齐全**（含权利要求数 `avg_claims`），`missing_dimensions` 空、claims 覆盖 0.68% 冻结上限如实披露 |
| 142 | 技术市场潜力 | `market_score=null`（G2 整维缺测 + G8 码值缺失），R5 复判 → 部分可演（空态讲「未测」） |
| 143 | 技术维权重合成 | R5 FIX-07 权重模型已落地：`weights` 默认 25/25/25/25、支持自定义重算 → 可演 |
| 144–148 | 产业发展潜力 | 维分 50.0；techPatent 三榜各 200 条 |
| 149 | 产业科学影响力 | 有值（15 集群口径）即可演 |
| 150 | 产业技术影响力 | R6 SUP-02 落地（entan 台账口径）→ 部分可演（SEP 轴无源，置灰「未测」） |
| 151 | 产业维权重合成 | R5 FIX-07 权重模型已落地 → 可演 |
| 152、154 | 政策与条件保障力 | 维分 63.4 |
| 155 | 政策项目支持 | G4 已落地（国自然代理三维），按「代理口径」讲 |
| 156 | 政策维度明细 | 有值即可演 |
| 157 | 政策维权重合成 | R5 FIX-07 权重模型已落地 → 可演 |
| 158 | 政策建议与方法论 | R7 SUP-01 落地（生成 → 异步轮询 → 当天缓存直开）→ 可演，带「模型生成·非评估结论」角标，禁模板套话 |

- **不演行**：无（158 已于 R7 由 SUP-01 转可演，演示须带「模型生成·非评估结论」角标，且不参与计分/排名）；**维持部分可演**：137、138、142、144（无源）、150（SEP 轴无源）；**维持覆盖不到**：0 项（R7 状态）。
- 演示口径：12 项 `noSourceFields` 全部空态呈现，不补 0、不沿用 demo 假数。

## 3. 判定与退出

同 DS-03 计划 §3：全过 → 状态行回写 → **需规核对（对照 SRS 科技创新评估 23 行一条不漏）** → 等监管人「签收」；有缺口 → DATA/QUERY/ALGO 分类建子任务到 ready，等「可以派了」；只读不签发；同页同条件单飞。

**本页额外强制**：R1 必须同步产出「覆盖表 23 行重填结果」（可演 / 部分可演 / 覆盖不到 + 依据），未重填不得申请签收。

## 4. 已知记录（演示红线）

- **产业维三项同为 50.0 不是占位值**：百分位得分在 48 个行业上的均值必然趋 50，话术按「行业均值百分位」讲，禁说「恰好都 50」。
- **趋势预测 trend=down、CAGR −81.51%**：因 2023–2026 专利申请量断崖（2026 仅 127 件为年中数据），属真实数据形状，**禁解释为「技术衰退」**。
- **POT_COMPOSITE 实为 3 维综合**：`coverage.science_dim_available=false`、`technology_influence.usable=false`，禁止宣称四维齐备。
- **评估对象范围**：SRS 未给「评估对象」枚举，P2 页复刻无法排期，需产品补；不影响本页签收。
- **性能**：snapshot 8.3s，页面首屏需骨架屏或预取，禁在演示中现场等待。

## 5. R1 覆盖表 23 行重填结果（2026-11-09 实测，强制产出）

判定口径：以各行「期望输出」为准。**仅当期望输出要求的明细结构在 payload 内确有对应字段才记 ✅**；只有汇总分值、明细字段缺失的记 ⚠️；整维无字段/恒 null 记 ❌。

| 序号 | 判定 | 实测依据 |
|---|---|---|
| 136 | ✅ | science「论文数量」=68.5（dwd_zh_paper 100,900 篇） |
| 137 | ⚠️ | science「网络中心性」=57.5 有分；payload 无中心性排名表/合作网络图谱字段（期望输出要求图谱+排名） |
| 138 | ⚠️ | science「研究前沿」=68.9 有分；payload 无前沿主题清单/时间演变字段 |
| 139 | ✅ | `sciForecast.domains` 3 领域：series 2015–2023 真值（2024–2026 为 null 预测位）+ forecast 2024/2025 + lo80/hi80 |
| 140 | ✅ | `techPatent.composite` 200 IPC4，patent_count 真实（A61K=226,626） |
| 141 | ✅ | FIX-01 落地：`techPatent.quality` **5 维齐全**（家族/被引/技术宽度/授权率/权利要求数），`missing_dimensions` 空；A61K `avg_claims`=15.24、`claims_covered_count`=25（覆盖 0.68% 冻结上限如实披露）；quality_score 按 5 维重归一，A61K 72.86→64.75 |
| 142 | ⚠️ | `market_score` 仍恒 null（G2 整维缺测：专利转让/许可/诉讼市场活动数据无源）→ **R5 复判由 ❌ 归入部分可演**：页面按空态呈现并明示「未测」，与 137/138/144 同列，不计可演 |
| 143 | ✅ | **R5 2026-11-10 解除**：FIX-07 权重模型落地——四维 `weights` 默认 25/25/25/25 非 0、`weightCoverage` 100，`composite` 41.4（技术 19.4/科学 36.6/产业 50.0/政策 59.4，分项贡献 4.9·9.2·12.5·14.9）；自定义改 40/30/20/10 → 后端重算 36.4；110% 非法 → `weightsValidation.valid=false` 且不产出综合分 |
| 144 | ⚠️ | `spatialRows`/`spatialRegions` 各 100 城计数真实；`spatialByDimension` 四维均 `[]` → 按维切换无数据 |
| 145 | ✅ | `forecast_top` series 2015–2026 真实申请量 + forecast 2027 起 + cagr_3y_pct（年度断档见 §4） |
| 146 | ✅ | industry「产业投入」=50.0（48 行业真实计量） |
| 147 | ✅ | industry「产品成熟度」=50.0 |
| 148 | ✅ | industry「产业产值」=50.0 |
| 149 | ✅ | **R4 2026-11-09 解除**：FIX-09 v2 部署后 `industrySciInfluence` 出真值——久新 15 集群口径，score 74.9，15/15 集群齐全（top1 CL-SEI-01 新一代信息技术 612,431 篇 / 12,765,905 被引 / 篇均 20.84 / D1 100.0；合计 5,826,738 篇 / 114,379,101 被引），industry「科学影响力」=74.9（非 null） |
| 150 | ⚠️ | **R6 2026-11-10 转部分可演**：SUP-02 改走 entan-py `M_ENT_DS_07_INDUSTRY_POTENTIAL_005`（`M_ENT_*` precompute 只烘焙在 entan 镜像），score 24.3；`axes` 2 轴（`sep` = `pending` → 置灰「未测」）、`chains` 12（9 条有专利、3 条 0 件不参与加权）、覆盖 citedRows 20,515 / linkedChainPatentN 190 / linkedChainCitedSum 415；SEP 轴无源，**不得由规则或模型填充** |
| 151 | ✅ | **R5 2026-11-10 解除**：同 143——权重模型落地后 industry「综合评估」参与合成、支持自定义权重重算；`industryRanking` 48 行（rank 1–48 连续、score 降序、无空无 0，top1 计算机通信电子 75.42 / 末位农业 27.8） |
| 152 | ✅ | policy「战略引导力」=50.1 |
| 153 | ✅ | policy「政策扶持力度」=64.3 |
| 154 | ✅ | policy「经费支持」=89.4 |
| 155 | ✅ | **R3 2026-11-09 解除**：`projectSupport` 出真值——NSFC 代理口径（dwd_zh_project 58,453 项；approval_year 覆盖 1986–2021，2022 起缺失不按 0 摊入）score 42.9；资助额 mean 43.27 万 / median 30 / max 920；类别 面上 27,939 / 青年C 23,884 / 地区 2,634 / 专项 1,058 / 重点 962 |
| 156 | ✅ | policy「实施效果」=100.0（须保留「仅相关不构成因果」标注） |
| 157 | ✅ | **R5 2026-11-10 解除**：同 143——policy「综合评估」参与合成、支持自定义权重重算 |
| 158 | ✅ | **R7 2026-11-10 转可演**：SUP-01 落地——`generate` → 轮询 `status`，5 条建议 / `degraded=false` / 每条带 evidence（metricId + value + caliber）；同条件当天 `status` 直开旧结果（单飞 + 缓存）；建议卡带「模型生成·非评估结论」角标、**不参与计分/排名/覆盖率**；方法依据 `methodEvidence` 仍空态（德尔菲/仿真未提供，演示口径列「未提供」） |

**小计（R7 2026-11-10 更新）**：✅ **18** / ⚠️ **5**（137、138、142、144、150）/ ❌ **0** = 23。转档轨迹：155（R3）→ 149（R4）→ 143/151/157（R5）→ 150（R6，→⚠️）→ 158（R7）；141 于 FIX-01 后 5 维齐全，142 于 R5 复判由 ❌ 归入 ⚠️（空态讲，不计可演）。与用例文档原「19 ✅ / 1 ⚠️ / 3 ❌」的差异，全部源于「仅汇总分无明细」与「缺块/无模型」，已在用例文档同步更正。

**部署确认结果（R3）**：display 新版已发布——`projectSupport` 已出真值（155 解除）；`industrySciInfluence` 仍缺（data keys 无此 key）→ 按「发布后仍缺」约定**建后端缺陷单**。权重模型（FIX-07）未落地，143/151/157 维持 ⚠️；`noSourceFields` 10 项（spatialByDimension / methodEvidence / policySuggestions / evidence 等）确认为**设计空态（诚实性声明）非缺陷**。

### 149 修复单（DSP-M4-FIX-09，算法侧，2026-11-09 立单）

**根因（已实锤，非同步漏）**：Java 期望契约 `M_INNOV_POT_SCI_INFL` 返回 `cluster_level.ranked`（[InnovationEvaluationController.java L443-449](../../../repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/InnovationEvaluationController.java)，15 集群被引排名结构 rank/cluster_code/cluster_name/papers/cited/cited_per_paper/score_d1，产品裁定 2026-11-08），但**算法侧从未实现**——vendor/innov-py 与 demo-algo-science 的 `spec_specs.py` 该指标均为论文粒度旧代理口径（gkx `dwd_zh_paper_citation` 被引 SUM + `dwd_zh_author` 论文计数），不产出 `cluster_level`；demo precompute JSON 亦无此结构（Grep 实证零命中）。Java 门控 `ranked` 空 → 块不组装 → 149 恒 ❌。

**实现要点**：
1. vendor/innov-py `spec_specs.py` v2：M_INNOV_POT_SCI_INFL 改集群粒度——论文经 `ads_sz_gkx_industry_cluster_topic`（gkx 库集群→topic 桥，3098 行/15 集群）⋈ 论文级 topic 归属表聚合被引，按 cluster_code 分组输出 `cluster_level.ranked`（含 papers/cited/cited_per_paper/score_d1）；国际合作维久新无国别字段，整维缺测不参与合成（产品裁定 2026-11-08）。
2. 输出结构需 compute 框架支持自定义 result 块（cluster_level 非框架标准 entity 结构）——按 `projectSupport` 同款改造路径。
3. `catalog.py` v2 同步：口径/源表/版本更新；xlsx 台账（指标入库详情.xlsx · 科技专题算法库 sheet）源表字段与备注同步（当前登记仍是 dwd_* 旧口径 + 「部分支持→完全转换支持(条件)」，创建人唐绍祖/王惠，未归久新）。
4. 重打 innov-py 镜像发布 → Java 块自动组装（`ranked` 非空即进）→ 149 解除，R4 复测。

**验收**：`POST /internal/innov/metric/M_INNOV_POT_SCI_INFL/compute` 返回非空 `cluster_level.ranked`（15 集群、含被引真值）；生产 snapshot `data.industrySciInfluence` 块出现且 industry「科学影响力」score 非 null。

**闭环记录（R4 2026-11-09，已验收）**：
- 代码：lumen-algo-py `84ff427`（rebase 自 `71c5ea3`，含 v2 实现 + gaps 归因更正 + CRC32 无损分片）
- 构建/部署：pipeline 4552 / `image:innov` job 33813 ✅、`deploy:innov` job 33819 ✅
- compute 自检：`precompute` 路径 0.46s，`ranked` 15 行，top5 逐位一致
- 生产实测：snapshot 214.8KB，`industrySciInfluence` score=74.9、clusters=15、top1 CL-SEI-01 612,431/12,765,905、合计 5,826,738/114,379,101；`gaps` 已无「256MB」表述
- 结论：**149 解除，覆盖表 12→13 可演**（残余仅 FIX-07 权重与口径文档待补 v2）

### 遗留登记（口径文档待补 v2，不阻塞演示，2026-11-09）

| 项 | 内容 |
|---|---|
| 事项 | `agent-delivery/metrics/calc-logic/INNOV/M_INNOV_POT_SCI_INFL.md` 待补 v2 章节 |
| 责任人 | **口径主（唐绍祖 / 王惠）**——该文档文头登记「维护者：唐绍祖、口径调研人：wanghui 标记 true」 |
| 现状 | 文档为 20261027 批旧口径（gkx `dwd_zh_paper_citation` 论文级，判「部分支持 / 产业级排名做不出来 / ranked=[]」），与本次 v2 实现（久新 15 集群完整排名、`support_judgment=完全转换支持(条件)`）**直接矛盾** |
| 处置裁定 | **本次不修**（人力：李伟，2026-11-09）：`calc_logic_ref` 为纯字符串元数据（`catalog.py` 104 处定义、全仓零处消费），不影响算法运行、接口返回、页面展示与 149 演示验收；仅影响口径符合性审计 |
| 残余风险 | ①若甲方/质量审计以该文档为「唯一真源」核对实现，会判「实现超出口径授权」；②后续维护者按该文档改代码，可能把实现回退到论文粒度 |
| 触发条件 | **口径评审 / 甲方符合性核查前必须补齐**（追加 §六 v2 章节 + 修正判档行，不重写原 586 行调研历史） |
| 关联事项 | `agent-delivery/metrics/指标入库详情.xlsx`（科技专题算法库 sheet）该指标行仍登记 gkx `dwd_*` 旧口径；**2026-11-09 裁定由唐绍祖 / 王惠走人工台账同步**（agent 不代改），须与 calc-logic 文档 v2 一并更新为久新集群口径 |
| **闭环（2026-11-10）** | **v2 已补**：`calc-logic/INNOV/M_INNOV_POT_SCI_INFL.md` 追加 **§六 v2 口径**（6.1 变更结论 / 6.2 公式与缺测处理 / 6.3 生产基线 5,826,738 篇·114,379,101 次·15 集群·综合 74.9 / 6.4 实现发布对应 `84ff427`+pipeline 4552 / 6.5 条件与话术约束 / 6.6 台账人工同步），并修正抬头与基础信息判档行「部分支持 → **完全转换支持（条件）**」、口径定义/源表/判档理由各增 v2 段（v1 全文保留作历史对照，§〇–§五 与附录未改写）。**残余仅 xlsx 台账人工同步（唐绍祖 / 王惠）**，不影响演示与审计引用 |
