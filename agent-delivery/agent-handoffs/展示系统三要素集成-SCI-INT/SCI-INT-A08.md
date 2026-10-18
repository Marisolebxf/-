# SCI-INT-A08 handoff：深圳创新监测系统集成项

| 项 | 值 |
|---|---|
| task_id | SCI-INT-A08（spike） |
| 执行 | agent:product-agent（coordinator_dispatch） |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新（旧路径沿用「九新」写法） |
| ponytail | N/A（分析叶） |
| 日期 | 2026-10-18 |

## 1. 范围与实现

- **范围**：需规 `bid-reference/srs/02-科技信息展示系统/科技发展态势/深圳创新监测.md`，excel_row 115–138（seq 112–135），共 24 个 SRS 叶。对应 4 个 DS 页面：DS-06-CARRIER（115–120）、DS-06-INDICATOR（121–126）、DS-06-DOMAIN（127–131）、DS-06-CITY（132–138）。
- **实现**：按 `产物/_card-template.yaml` 输出 33 张页面级卡片（号段 INT-A-*-701～733）。同一 SRS 行涉及多个三要素或多种对端能力时拆卡：row 115 拆成地理维和载体实体两张；row 122 按人才、技术、机构和其余六维拆成四张；row 127 另拆出领域分类映射卡；row 130、133、134 按人才和技术拆卡。
- **输入**：页面映射 `metrics/request/展示系统/pages/DS-06-*.yaml`（真源）、P00 基线、B01 集成模式、C01/C02/C03 主数据结论、A05 卡片风格，以及只读核对的 lumen-ui-science-pc、demo-ui-science、lumen-svc-platform（gkxlumen-innov）、lumen-algo-py、lumen-etl-es-py。
- **MCP**：所有卡片的 algorithm_type 和 d1_d4 都来自 `user-metric-registry`。涉及的指标有 M_INNOV_DS_06_CARRIER_003、M_INNOV_CARRIER_VALUE_RANK_SZ、M_INNOV_KPI_BOARD_SZ、M_INNOV_DOMAIN_KPI_SZ、M_INNOV_CITY_{COMPARE,RANK,INDEX,COMPETE,TREND,TALENT_INDEX}_SZ、M_SYNTH_186_1；为核对久新深圳叶，另查了 M_ORG_DEEP_151_1、M_TECH_DEEP_133_1、M_TALENT_DEEP_159_1。

### 1.1 派单关注点结论

1. **多级地理维表（市/区/街道/园区）**：市、区、街道三级可以用三方库的 `dwd_dim_admin_area` 一张维表承接（源头有 street_code，见 C03 INT-C-ORG-222），但我方 ETL 的 `RegionCodeResolver` 只解析到区级，Java 侧的 `dim_admin_division` 还在 demo 库。**产业园级和园区级全链路都没有数据源和编码**，需要新建园区维（structure_escalation，INT-A-X-701），名录和边界由谁提供待甲方定（DN-A08-02）。区/街道边界面的来源也未知，现在 demo 和 lumen 都只是硬编码的 20 个街道中心点。
2. **「载体=机构」**：DS-06 的「载体」至少有三种语义：机构或企业实体本身、企业持有的创新载体资质（lumen-etl-es-py 中 `innovation_carrier` 是企业的资质属性）、园区。它不等于 ORG 主数据。草案沿用 C03 的 🟡 默认值：载体榜按 org_category 联合机构和企业两侧，园区另建维表，载体统一 ID 通过 org_uid 和企业 org_id 桥接。待甲方拍板（DN-A08-01）。
3. **久新深圳类库叶与本页的关系**：通过 MCP 核对，151/152 只挂在 TOPIC-ORG-05，159 只挂在 TOPIC-TALENT-05，133 没有挂任何页面。DS-06 四个页面映射都明令禁止挂技术链 130–140、151/152 等。显示序号 130–135 与 05 技术链 seq 130–135 只是撞号。**本页不消费任何久新深圳叶，新增久新能力需求为 0。**
4. **C03 冲突**：架构级初稿 §1 的 DS-06 行写了「对端依赖 131/133/151/152（API）」，与页面映射冲突。按派单要求以页面映射为准，已写入 INT-A-ORG-704、INT-A-X-717、727、730 的 conflicts，并登记 DN-A08-15（owner architect，对应 OI-C03-11）。

### 1.2 需要久新提供的能力（全部待确认）

- **久新 API / 算法能力：0 项**（P00 的 51 行中没有 DS-06 行，jiuxin_row_id 全部为 null）。
- **三方库（北京久新供数）数据问题 6 项**：深圳街道级区划的覆盖、版本和更新频率；产业园和园区名录及边界；研发投入（区级和城市级）来源；会议、课题、项目、资金、政策、基础设施六维源表；高新技术企业认定数据；工作室类载体来源。

## 2. 偏离说明

- **xlsx 行 59「深圳重点人才指数」**：没有对应的 SRS excel_row。本包把它挂在 row 134「城市排名展示」，单独出一张卡（INT-A-TAL-728），属于草案归属。
- **对端写法**：INT-A-TAL-728 的 counterpart 按模板写成 `other:新型高端智库 / 科技人才智慧服务`，因为对端系统未知。
- **freshness 取值**：除模板的四个枚举值外，INT-A-X-712 和 INT-A-TAL-728 用了 `unknown`，因为源表或对端未知，不推测时效。自检脚本也放行了这个值。
- **ORG 卡的 dimension**：沿用 A05 自检约定，ORG 卡只写 `[ORG]`。企业、工作室、园区这些非 ORG 载体由 carrier_vs_org_verdict 和 INT-A-X-701 承接。

## 3. 产物清单

| 产物 | 路径 |
|---|---|
| 集成卡片 | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A08.yaml` |
| 自检脚本 | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A08-check.py` |
| 本 handoff | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/SCI-INT-A08.md` |

未改业务仓、seed 或矩阵，未执行 git commit/push。

## 4. 验收证据

自检命令为 `python 产物/_work/A08-check.py`。脚本先用 yaml.safe_load 解析，再核对 P00 中 leaf=A08 的范围、差集、号段 7xx、IP 编号、页面归属、三要素卡的四段调用链和 summary 一致性。实际输出：

```
scope_count=24 covered_rows=24 diff=[]
cards: 33 {'X': 20, 'ORG': 6, 'TAL': 4, 'TECH': 3}
jiuxin_rows: []
metric_missing: 4 ['INT-A-ORG-703', 'INT-A-ORG-707', 'INT-A-X-701', 'INT-A-X-719']
algo_owner_missing: 2
structure_escalation: 9
patterns: {'IP-01': 15, 'IP-02': 5, 'IP-08': 1, 'IP-09': 6, 'IP-10': 4, 'IP-12': 2}
OK
```

**范围 24 / 已出卡 SRS 行数 24 / 差集 0**

### 4.1 统计

- **卡片**：共 33 张，其中 TAL 4、TECH 3、ORG 6、X 20。
- **metric_missing（4 张）**：区划载体数量、载体详情计数、载体对比计数、街道聚集计数。
- **algo_owner_missing（2 张）**：
  - 创新价值排名：页面映射判 missing，registry 却登记为 MODEL，算法位置指向 demo-algo-science。
  - 城市趋势预测：SZCITY-B04 未冻。
- **structure_escalation（9 张，升级 human:李伟）**：园区维 / 街道维、载体统一维、ads_carrier_index、订阅表、深圳指标看板宽表、领域×区划表、领域映射表、ads_city_index、智库人才指数适配。
- **decision_needed**：DN-A08-01～15。
- **risks**：R-A08-1～8，其中 high 级 3 项。

### 4.2 最大 3 个开放项

1. **园区级地理维无源**（DN-A08-02/03）：地图下钻五级中，园区和产业园两级没有任何数据，街道级还需要扩 ETL 并补边界面。
2. **「载体=机构」口径和载体统一 ID**（DN-A08-01）：这决定载体地图、排名、筛选、对比四张卡的实体集合。
3. **CITY 页指标双身份和算法归属**（DN-A08-14/04/12）：页面映射挂 M_SYNTH_186_1，registry 另有 M_INNOV_CITY_*_SZ，且算法位置都指向 demo-algo-science。创新价值模型的交付方也待定。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 创新价值、区域创新活力（186）、竞争力和趋势预测都放在 lumen-algo-py 离线 Job（/internal 草案）；Java 只读 ADS |
| 2 调用链：前端 → Java → Python /internal | ✅ 所有卡片都按这个顺序写。智库人才指数走 Python 适配层（IP-08），前端不直连久新或智库 |
| 3 只用 NebulaGraph | ✅ 本页不需要图谱；筛选卡明确不走 05 seq 116 图谱 API |
| 4 可观测 | ⚠️ 前端已有 createTraceId 和 `ts-sz-innovation-track` 事件，但后端端点 `/situation/v1/shenzhen-innovation/dataset` 不存在，链路无法贯通；后续实现叶需要补 |
| 5 CI/CD | N/A（分析叶，cicd skip） |
| 6 demo 只读 | ✅ demo-ui-science 和 demo-algo-science 只作读取对照 |
| 7 共享聚合核心 | ✅ 订阅服务与 A05/A06 是否合并已登记（DN-A08-05） |
| 8 ADS 先行 + Mock | ✅ 无源或无交付方的项目走 IP-10，显示空态加 ⚠️，不伪造数值；已指出四个 tab 直接 import `@/mock` 违反 IP-13 |
| 9 D8 | N/A（不改 UI） |
| 10 D9 | ✅ 统计数字都挂了 metric_id，或登记了 metric_missing / algo_owner_missing；已指出前端自造的 `TS-M6-*` metricId 查不到 8 件套 |
| 11 D10 | N/A |
| 12 D12 | ⚠️ 发现两处风险，已写入 risks：① gkxlumen-innov 的复用候选接口经 InnovSql 读 `demo_gkxlumenx_*`（R-A08-1）；② 创新价值和城市类指标的 algo_server_location 指向 demo-algo-science（R-A08-2）。本方案不调用任何 demo-* 服务 |
| 禁读 registry YAML | ✅ task 和 metric 都只通过 MCP 查询；页面映射和 P00 不属于禁读范围 |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | 380000（估算） |
| model_used | claude-opus-5.5 |
| actual_cost | 9.0（USD，估算） |
| cost_warn | yellow |
