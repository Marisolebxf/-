# TS-DS07-DEMO-ACCEPT-LOOP · 科技创新评估合规演示验收单

> 页：**DS-07 科技创新评估（P2）**｜编号：`TS-L2-DS07`｜模块：科技发展态势
> 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS07-合规演示用例.md`
> 计划：`.../编排计划/TS-L2-DS07-LOOP计划.md`（R0–R7）
> 补项：`.../合规演示用例/展示系统-第一批-DS07-补项派单-20261110.md`（DSP-DS07-SUP-01 / SUP-02）
> 状态：**✅ 已签收（2026-11-10 · human:李伟）**｜授权人：`human:李伟`｜起草：`agent:dev`

## 1. 验收结论

| 项 | 结果 |
|---|---|
| 需规覆盖 | 23 行 → **18 可演 / 5 部分可演 / 0 覆盖不到**（18+5=23 平） |
| 复跑轮次 | R0–R7 全部完成，末轮 R7（2026-11-10）生产实测 |
| 补项闭环 | SUP-02（150，R6）✅ / SUP-01（158，R7）✅ |
| 阻断项 | **无** |
| 建议 | 准予签收，附 §4 保留口径 |

## 2. 需规核对（SRS 科技创新评估 23 行，一条不漏）

| 序号 | 需规要点 | 实测证据（R7 生产） | 判定 |
|---|---|---|---|
| 136 | 科学影响力 | `sciImpact.score` = 36.6（非 null） | ✅ |
| 137 | 网络中心性 | 无独立端点（G8）；知识图谱页可演，网络中心性维空态呈现 | ⚠️ |
| 138 | 技术前沿性 | `frontier_ratio` 有值 | ✅ |
| 139 | 科学趋势预测 | `sciForecast.domains` 3 领域：series 2015–2023 真值 + forecast 2024/2025 + lo80/hi80；2024–2026 为 null 预测位 | ✅ |
| 140 | 技术创新力（分项） | `techPatent.composite` 200 个 IPC4，`patent_count` 真实（A61K = 226,626） | ✅ |
| 141 | 技术创新力（质量维） | FIX-01：`techPatent.quality` **5 维齐全**（家族/被引/技术宽度/授权率/权利要求数），`missing_dimensions` 空；A61K `avg_claims` = 15.24、`claims_covered_count` = 25（覆盖 0.68% 冻结上限如实披露）；quality_score 按 5 维重归一（A61K 72.86→64.75） | ✅ |
| 142 | 技术市场潜力 | `market_score` 恒 null（G2 整维缺测 + G8 码值缺失）→ 空态并明示「未测」 | ⚠️ |
| 143 | 技术维权重合成 | `weights` 默认 25/25/25/25（非 0）、`weightCoverage` 100；`composite` 41.4（技术 19.4/科学 36.6/产业 50.0/政策 59.4，分项贡献 4.9·9.2·12.5·14.9）；自定义 40/30/20/10 → 后端重算 36.4；110% 非法 → `weightsValidation.valid=false` 且不产出综合分 | ✅ |
| 144 | 空间分维 | `spatialRows` / `spatialRegions` 各 100 城计数真实；`spatialByDimension` 四维均 `[]` → 按维切换无数据 | ⚠️ |
| 145 | 技术趋势预测 | `forecast_top` series 2015–2026 真实申请量 + forecast 2027 起 + `cagr_3y_pct`（年度断档见 LOOP §4） | ✅ |
| 146 | 产业投入 | industry「产业投入」= 50.0（48 行业真实计量） | ✅ |
| 147 | 产品成熟度 | industry「产品成熟度」= 50.0 | ✅ |
| 148 | 产业产值 | industry「产业产值」= 50.0 | ✅ |
| 149 | 产业科学影响力 | `industrySciInfluence` = 74.9，15/15 集群齐全（top1 CL-SEI-01 新一代信息技术 612,431 篇 / 12,765,905 被引 / 篇均 20.84；合计 5,826,738 篇 / 114,379,101 被引） | ✅ |
| 150 | 产业技术影响力 | SUP-02 改走 entan-py `M_ENT_DS_07_INDUSTRY_POTENTIAL_005`：score 24.3，`axes` 2 轴（`sep` = `pending` → 置灰「未测」），`chains` 12（9 条有专利、3 条 0 件不参与加权），覆盖 citedRows 20,515 / linkedChainPatentN 190 / linkedChainCitedSum 415 | ⚠️ |
| 151 | 产业维权重合成 | 权重模型落地后参与合成，支持自定义权重重算；`industryRanking` 48 行（rank 1–48 连续、score 降序、无空无 0，top1 计算机通信电子 75.42 / 末位农业 27.8） | ✅ |
| 152 | 战略引导力 | policy「战略引导力」= 50.1 | ✅ |
| 153 | 政策扶持力度 | policy「政策扶持力度」= 64.3 | ✅ |
| 154 | 经费支持 | policy「经费支持」= 89.4 | ✅ |
| 155 | 政策项目支持 | `projectSupport` = 42.9（NSFC 代理口径：dwd_zh_project 58,453 项；approval_year 覆盖 1986–2021，2022 起缺失不按 0 摊入）；资助额 mean 43.27 万 / median 30 / max 920 | ✅ |
| 156 | 实施效果 | policy「实施效果」= 100.0，须保留「仅相关不构成因果」标注 | ✅ |
| 157 | 政策维权重合成 | 权重模型落地后参与合成，支持自定义权重重算 | ✅ |
| 158 | 政策建议与方法论 | SUP-01：`generate` → 轮询 `status`，**5 条建议**、`degraded=false`、每条带 evidence（metricId + value + caliber）；建议卡带「模型生成·非评估结论」角标，不参与计分/排名/覆盖率；`methodEvidence` 仍空态（德尔菲/仿真方法依据未提供，演示口径列「未提供」） | ✅ |

## 3. SUP-01 五条验收口径逐条核对

| # | 口径（补项派单 §） | 实测 | 结论 |
|---|---|---|---|
| 1 | 建议条数 ≥ 3 且结构完整（title/action/evidence） | 5 条，字段齐全 | 满足 |
| 2 | 每条建议带可追溯 evidence（metricId + value + caliber） | 5/5 带 metricId+value+caliber | 满足 |
| 3 | 不伪造：模型不可用时降级为空态并说明，不套模板 | `degraded=false`；异常路径回空态 + 说明文案，无模板套话 | 满足 |
| 4 | 异步单飞：同用户同条件只允许一条在跑；当天成功直接打开旧结果 | 二次 `status` 直接返回旧结果，不重复调模型 | 满足 |
| 5 | 建议不参与业务计分/排名/覆盖率 | 建议卡独立展示，`composite` 等计分字段不含建议输入 | 满足 |

## 4. 保留口径（签收须一并确认）

1. **137 / 138 / 142 / 144**：数仓/算法无源（网络中心性无独立端点、前沿主题缺测、市场活动数据缺失、空间分维无源），页面按空态呈现并明示「未测」，**不建补数单、不补 0、不沿用 demo 假数**（裁定单 §10）。
2. **150**：SEP 轴无源，`pending` 置灰「未测」，**不得由规则或模型填充**；覆盖量为台账口径（见 §2 第 150 行）。
3. **158**：建议为**模型生成内容，非评估结论**，不参与任何计分/排名/覆盖率；方法依据空态如实说明。
4. **141**：权利要求数维已由 FIX-01 落地（5 维齐全），但 claims 覆盖仅 0.68% 属**冻结上限**，演示时须如实披露覆盖比例，不得表述为全量覆盖。
5. **台账**：`指标入库详情.xlsx` 中 DS-07 相关指标行仍登记 `dwd_*` 旧口径，需由 **唐绍祖 / 王惠** 人工同步，**不阻塞演示与本次签收**。

## 5. 证据索引

- 生产实测：snapshot 200；`composite` 41.4；`industryRanking` 48 行；`industryTechInfluence` 24.3；`policySuggestions` 5 条 / `degraded=false`。
- 发布记录：R5 FIX-07（svc `a843b09` pipeline 4597 / `deploy:display` 34316 ✅ + FE `7dd8ada` pipeline 4596 ✅）；R6 SUP-02（svc `1d3a70e` + `dfb3a88`，pipeline 4607/4609，`backend:image:display` 34426 + `deploy:display` 34437 ✅）；R7 SUP-01（algo `display_policy_suggestion_routes.py` + svc `PolicySuggestionService` + FE `PolicySuggestionCard`）。
- 口径文档：`agent-delivery/metrics/gap-analysis/M_INNOV_POT_SCI_INFL.md` §六 v2（SUP-02 口径）；政策建议口径见补项派单 §SUP-01。
- 轮次记录：`TS-L2-DS07-LOOP计划.md` §1 状态行 R0–R7、§5 覆盖表（小计 18/5/0）。

## 6. 签收栏

| 项 | 内容 |
|---|---|
| 演示结果 | ☑ 通过　☐ 有条件通过　☐ 不通过 |
| 授权人签字 | `human:李伟` |
| 签字日期 | 2026-11-10 |
| 备注 | 按 §4 保留口径签收（137/138/142/144/150 维持部分可演，158 建议为模型生成非评估结论）；台账 `指标入库详情.xlsx` 由唐绍祖/王惠人工同步，不阻塞签收 |
