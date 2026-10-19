# SCI-INT-A07 handoff：湾区创新监测系统集成项

| 项 | 值 |
|---|---|
| task_id | SCI-INT-A07（spike） |
| 执行 | agent:product-agent（协作 architect-agent；coordinator_dispatch） |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新（旧路径沿用「九新」写法） |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：需规 `科技发展态势/湾区创新监测.md`，excel_row 92–114（seq 89–111），共 23 个 SRS 叶。对应 4 个 DS 页面：DS-05-GBA-ACHIEVE（92–96）、DS-05-GBA-CAPACITY（97–100）、DS-05-GBA-ANALYSIS（101–107）、DS-05-GBA-INDICATOR（108–114）。
- **实现**：按 §2 schema 输出 35 张页面级卡片（号段 INT-A-*-601～636，606 空号）。同一行涉及多个三要素或多种数据源时拆卡：row 92 拆为地理维、成果落点、机构落点三张；row 96 拆为成果详情和关联机构；row 97 拆为总指数（MIXED Job）和资源、机构、机制、环境、人才五张输入卡；row 102 拆为技术、机构和无源环境因素三张；row 109 拆为指标目录、专利论文、统计年鉴类三张。
- **输入**：`产物/_prep/A07-pack.yaml`（SRS 原文 + MCP 口径指标，18 个未挂序号候选指标已逐个挂叶）、C-index（引用 INT-C-* 不重复造卡）、global-findings（引用已登记 DN/R）、B01 IP-01…IP-13、页面映射 `DS-05-GBA-*.yaml` 的 srs05_do_not_map；前端仅点查 `bayAreaInnovation.ts` / `bayAreaModel.ts` / `index.vue` / `menu.ts`。
- **构建方式**：卡片内容集中在 `产物/_work/A07-build.py`，生成 `产物/SCI-INT-A07.yaml`；自检 `产物/_work/A07-check.py`。

### 1.1 派单关注点结论

1. **SWOT 四象限**：是规则 + 统计识别（四子指数 12 分项相对排名得出优势/短板，政策/技术/合作外部信号得出机会/威胁），不是大模型。05 算法库没有对应叶，demo-algo-science 只有规格登记、没有计算代码。归属记 algo_owner_missing，建议我方在 lumen-algo-py 重写 `/internal/gba/swot`（IP-04 + 快照 IP-11）。机会和威胁的外部信号没有数据源，走 IP-10（空态 + ⚠️）。见 INT-A-X-619、623–626。
2. **报告生成**：现状全在前端——模板拼装，PDF 走浏览器打印，Word 是 .doc 包 HTML；lumen 没有大模型报告能力。是否需要大模型润色 + 人工审核由甲方定（DN-A07-07），服务端还是前端导出并入 DN-A08-13。见 INT-A-X-627。
3. **lumen 链路未通**：Java 侧湾区接口零命中；前端调用的 `/situation/v1/bay-area/innovation/dataset` 后端不存在；lumen-algo-py 没有湾区/SWOT 路由。草案拆为 `/innov/v1/gba/*` 资源接口（经 gateway），算法统一落 `/internal/gba/{hotspot,capacity,swot,alerts}`。
4. **湾区 11 市地理维表不存在**：只在前端 mock 和 Python 临时码表里，后者只有 8 个市码（缺肇庆、香港、澳门）。港澳在国标区划只有省级码。新建 `dim_gba_city`，structure_escalation 升 human:李伟（INT-A-X-601）。
5. **指标两套 id 并存**：M_SYNTH_186_1（MIXED）与 M_INNOV_GBA_CAPACITY_INDEX（MODEL）类型都不一致；M_INNOV_DS_05_GBA_ACHIEVE_004 / ANALYSIS_003–006 与 M_INNOV_GBA_HOTSPOT / SWOT_* 同义。页面主 id 待 Q133（DN-A07-02），已写入相关卡 conflicts。

### 1.2 需要久新提供的能力

- **久新 API / 算法能力：0 项**。P00 的 51 行中没有 DS-05、湾区或 186 行；pack 中 jiuxin_rows_page 和 b01_mapping 都为空；DS-05-GBA-* 页面映射禁挂技术前沿热点 134 和 SYNTH 182–191。所有卡片的 jiuxin_row_id 都为 null。
- **三方库（北京久新供数）数据问题 5 项**：港澳成果/机构地址覆盖与地理编码；城市级研发投入；政策类数据；统计年鉴类（高技术产业增加值、GDP、技术合同成交额）；dwd_org_tech_tag 高企值域。

## 2. 偏离说明

- 无范围偏离。号段 606 未使用（规划时合并到 605），不影响唯一性和号段约束。
- 前一轮超时中断；本轮直接采用前一轮已核实的 5 条结论，未重扫代码。

## 3. 产物清单

- `产物/SCI-INT-A07.yaml`（35 卡 + 久新/SWOT/报告/地理维/链路 5 个 verdict + summary + 11 个 DN + 7 个风险）
- `产物/_work/A07-build.py`（卡片构建脚本）
- `产物/_work/A07-check.py`（自检脚本）
- 本 handoff `SCI-INT-A07.md`

## 4. 验收证据

`python -X utf8 产物/_work/A07-check.py` 输出：

```
scope_count=23 covered_rows=23 diff=[]
cards: 35 {'X': 22, 'TECH': 8, 'ORG': 4, 'TAL': 1}
jiuxin_rows: []
metric_missing: 4 ['INT-A-ORG-603', 'INT-A-TAL-615', 'INT-A-TECH-602', 'INT-A-X-618']
algo_owner_missing: 8
structure_escalation: 7
patterns: {'IP-01': 15, 'IP-04': 6, 'IP-10': 6, 'IP-11': 2, 'IP-12': 3, 'IP-13': 3}
OK
```

### 4.1 统计

| 项 | 值 |
|---|---|
| 范围 / 覆盖 / 差集 | 23 / 23 / 0 |
| 卡片 | 35（TAL 1 / TECH 8 / ORG 4 / X 22） |
| 久新依赖 | 0（新增需求 0） |
| metric_missing | 4 张卡 |
| algo_owner_missing | 8 张卡（热点 1、能力指数/贡献度 2、SWOT 5） |
| structure_escalation（→ human:李伟） | INT-A-X-601、INT-A-TECH-602、INT-A-TECH-607、INT-A-X-610、INT-A-X-618、INT-A-X-619、INT-A-X-631 |
| 新结构候选 | dim_gba_city、ads_gba_achievement_geo、ads_gba_city_flow、ads_gba_hotspot_snapshot、ads_gba_city_input_yearly、ads_gba_capacity_snapshot、app_gba_alert_rule/event、ads_gba_swot_snapshot、ads_gba_city_stat_yearly |

### 4.2 最大 3 个开放项

1. **湾区算法无主**（热点、创新能力指数、SWOT、预警评估）：05 库和久新都不交付，建议我方 lumen-algo-py 自建，需指派 algorithm owner，并由 data-agent 把 registry 算法位置从 demo-algo-science 改正（R-A07-3）。
2. **湾区 11 市地理维 + 港澳口径**：dim_gba_city 建表升李伟（DN-A07-01）；港澳统计口径、币种、地址解析待甲方（DN-A07-09）。
3. **指标口径与数据源**：双 id 主身份（DN-A07-02 / Q133）、四子指数权重（DN-A07-04）、统计年鉴类 4 指标无源（DN-A07-08 / Q132 / Q135 / Q136）。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 调用链 FE → Java → Python /internal | ✅ 草案全部经 `/innov/v1/gba/*`（gateway）；算法在 `/internal/gba/*`。❌ 现状：前端在 bayAreaModel.ts 做热点识别、阈值预警、贡献度计算（R-A07-2），已标为整改项 |
| 算法只在 Python / Java 不做算法、不写 nGQL、只读 ADS | ✅ 草案 Java 只读快照/ADS |
| Nebula TRSGraph | ✅ 本页不涉图谱读写（飞线由 ETL 预聚合 ADS） |
| 可观测 | ✅ 草案沿用 Java Agent + Python instrument + 前端 observability.ts；无新增链路例外 |
| D8 Design | ✅ 不涉视觉改动；卡片只定契约 |
| D9 metric_id + ⓘ + D1–D4 | ✅ 有注册的都挂 metric_id；无注册的 4 张卡记 metric_missing；数据来源/计算方式说明走 catalog（IP-12），扩展字段记 DN-A07-11 |
| D10 交互 | ✅ 测试点含键盘可切换效果、空态 + ⚠️ |
| D12 lumen 禁调 demo-* | ✅ 草案调用链无 demo-*（check 脚本断言）。❌ 现状风险：registry 算法位置指向 demo-algo-science（R-A07-3）；复用 gkxlumen-innov 会读 demo_gkxlumenx_*（R-A07-7）；前端运行时 import @/mock 违反 IP-13（R-A07-1） |
| 不改业务仓 / seed / matrix / task-registry.yaml；不 commit | ✅ 只写编排仓本目录产物，未 commit |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | 400000（估算：前一轮超时约 200k + 本轮约 200k） |
| model_used | claude-opus-5.5 |
| actual_cost | 9.5（USD，估算，含前一轮） |
| cost_warn | yellow |
