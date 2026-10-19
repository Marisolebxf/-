# SCI-INT-A12 handoff：全球领域人才态势系统集成项

| 项 | 值 |
|---|---|
| task_id | SCI-INT-A12（spike） |
| 执行 | agent:product-agent（协作 architect-agent；coordinator_dispatch） |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新（旧路径沿用「九新」写法） |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：需规 `科技人才态势/全球领域人才态势.md`，excel_row 246–268（seq 243–265），共 23 个 SRS 叶。页面 DS-13-TALENT-GLOBAL。
- **实现**：按 `产物/_card-template.yaml` 输出 23 张页面级卡片（号段 INT-A-TAL-1100～1122），一叶一卡，差集 0。
- **输入**：`产物/_prep/A12-pack.yaml`、C-index、global-findings、B01 的 IP-01～IP-13。只读核对了 lumen 菜单 `src/router/menu.ts`（材料包 fe_files_hit）和 demo 是否存在本页。
- **指标**：材料包已给出 MCP 口径，未再调 metric-get。6 个已挂指标均为 third_party / D1=draft / D4=mock。

### 1.1 页面指标挂叶

| metric_id | 材料包挂到的 SRS 行 | 卡片额外消费 |
|---|---|---|
| M_TALENT_BASE_98_1 | 246、252、254 | 247、248、250、253（同一 SQL-98 聚合的筛选/定位/导出/机构人数） |
| M_TALENT_DEEP_157_1 | 249、255、259 | — |
| M_TALENT_DEEP_162_1 | 261、262 | — |
| M_TALENT_DEEP_164_1 | 266 | — |
| M_TALENT_GRAPH_110_1 | 260、263 | — |
| M_TALENT_GRAPH_111_1 | 264 | — |

### 1.2 本叶必须给的结论

1. **华人占比（row 251，INT-A-TAL-1105）：无源。** 三方库没有国籍/华人标记列（OI-C01-09）。久新 51 行没有华人占比。材料包本叶没有指标。不从姓名、地址或论文语种推断。模式 IP-10，空态 + ⚠️。华人定义和分母登记 DN-A12-01，不替甲方定口径。
2. **迁徙图（row 249 / 255，INT-A-TAL-1103 / 1109）：主源是久新，不是无源。** 久新 API-157（M_TALENT_DEEP_157_1，IP-08，C01 的 INT-C-TAL-044，行 SRS-157）。`dwd_scholar_work_experience`（INT-C-TAL-002）只是任职原料，不能直接差分成迁徙事件。事件定义未拍板（DN-A12-02），确认前按 IP-10 空态降级。
3. **与 A11 的重叠：** A11 整叶是科技发展规划。其中 excel_row 185「科技人才流动监控」与本页迁徙重叠，指标是 `M_INNOV_DS_09_COMPREHENSIVE_006`（材料包标 MODEL）。`SCI-INT-A11.yaml` 不存在，本页独立出卡，不引用尚未写出的 int_id（CF-A12-3）。
4. **H 指数：** 沿用 A10。算法在久新 DS-08-VIZ-001，已并入 API-162（INT-C-TAL-049）。`dwd_scholar.h_index` 只作降级源，谁为主待 OI-C01-15。本页 1115/1116 只读 162 快照，Java 不排序。
5. **人才主键：** 候选 `dwd_scholar.scholar_id`，卡在供应方 P0-1（INT-C-TAL-001）。本页不新造 ID。

### 1.3 需要久新提供的能力

已有行 6 条，全部待确认，本叶不新增久新行：SRS-98（基础指标 SQL）、SRS-110 / SRS-111（实体识别与关系抽取）、SRS-157（流动追踪）、SRS-162（学术力，含 H 指数）、SRS-164（招入推荐）。华人占比、动态气泡、动态热力、最新动态、奖项、出访不向久新虚构接口。

## 2. 偏离说明

- 分布图上的缩放、定位、导出、洞察（247、248、250、252、253、254）没有单独向久新再要，记 IP-09，仍挂 SRS-98，因为读的是同一份聚合。
- 无注册指标的统计数字写在 gaps，前缀 `metric_missing`。纯地图镜头（258）记 `n/a_ops`。
- 动态热力（257）与人数热力（246）拆成两个接口，避免用人数顶替「人才动态密度」。
- 详情页匹配度（266）只读 API-164。完整引进评估归 A15，A15 产物未出。

## 3. 产物清单

| 产物 | 路径 |
|---|---|
| 集成卡片 | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A12.yaml` |
| 自检脚本 | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A12-check.py` |
| 生成脚本 | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A12-build.py` |
| 本 handoff | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/SCI-INT-A12.md` |

未改业务仓、seed、矩阵或 task-registry.yaml，未执行 git commit/push。

## 4. 验收证据

自检命令为 `python 产物/_work/A12-check.py`。脚本先 `yaml.safe_load`，再核对 P00 中 leaf=A12 的 246–268、差集、号段 1100–1199、id 唯一且连续、IP 编号、页面归属、三要素四段调用链、调用链无 `demo-`、久新行在 P00 内、材料包指标行都被挂上、华人占比为 IP-10 无源、迁徙主源为 SRS-157。实际输出：

```
scope_count=23 covered_rows=23 diff=[]
cards: 23 {'TAL': 23}
jiuxin_rows: ['SRS-110', 'SRS-111', 'SRS-157', 'SRS-162', 'SRS-164', 'SRS-98']
metric_missing: 10 ['INT-A-TAL-1105', 'INT-A-TAL-1107', 'INT-A-TAL-1108', 'INT-A-TAL-1110', 'INT-A-TAL-1111', 'INT-A-TAL-1113', 'INT-A-TAL-1116', 'INT-A-TAL-1119', 'INT-A-TAL-1121', 'INT-A-TAL-1122']
structure_escalation: 3 ['INT-A-TAL-1100', 'INT-A-TAL-1103', 'INT-A-TAL-1114']
patterns: {'IP-06': 1, 'IP-07': 3, 'IP-08': 4, 'IP-09': 9, 'IP-10': 6}
OK
```

**范围 23 / 已出卡 SRS 行数 23 / 差集 0**

### 4.1 统计

- **卡片**：23 张，TAL 23、TECH 0、ORG 0、X 0。
- **久新依赖**：6 条（见上），新增 0 条。
- **metric_missing（10 张）**：华人占比（1105）、机构排名分与论文量（1107）、产研比例（1108）、动态气泡（1110）、动态热力（1111）、学术发布/项目启动动态（1113）、学科贡献度（1116）、最新动态（1119）、荣誉奖项（1121）、出访记录（1122）。
- **structure_escalation（3 张，升级 human:李伟）**：
  - INT-A-TAL-1100：区域人数聚合表候选 `ads_talent_geo_agg`（SQL-98 落 ADS，Java 不现场扫三方库）。
  - INT-A-TAL-1103：人才流动边表，沿用 C01 候选 INT-C-TAL-071，名未定。
  - INT-A-TAL-1114：人才主档与人员 ID 映射，沿用 INT-C-TAL-070 / 072。主键未定前详情不可开。
- **lumen 页面**：无。菜单 `talent/global-talent-situation` 落到 `DevelopingView.vue`。
- **demo 页面**：有。`src/pages/talent-preview/TalentPreviewPage.tsx`（页键 global）及 `src/pages/talent-trend/`。只作对照。
- **decision_needed**：DN-A12-01～10；另引用 OI-C01-01/03/07/08/09/11/14/15、OI-C02-02、DN-01、DN-07、DN-09。

### 4.2 关键冲突

- **CF-A12-1**：材料包 algorithm_type=third_party，久新行侧常标 MODEL/Python（同 B01 C2）。卡片以材料包为准。
- **CF-A12-2**：需规要华人占比，数据侧无字段、无指标、无久新行。
- **CF-A12-3**：本页 DEEP_157 与 A11 row 185 的 INNOV 流动监控指标不是同一个注册项。
- **CF-A12-4**：产研对比要机构类型，人才主数据没有稳定 org_uid。
- **CF-A12-5**：需规写实时动态，没有事件流；供应方更新频率也未书面给出。

### 4.3 最大 3 个开放项

1. **华人定义与分母**（DN-A12-01）：无源。确认前 1105 不出数。
2. **迁徙事件定义，以及是否与 A11 row 185 同一口径**（DN-A12-02 / CF-A12-3）：久新 API-157 是候选主源，确认前迁徙图空态。
3. **人才主键 P0-1**（OI-C01-01）：scholar_id 不稳定时，分布、详情、迁徙都无法落键。动态事件、奖项、出访则是另一类无源（DN-A12-04 / 05）。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ SQL-98 进 GDF；110/111 并入 lumen-algo-py；157/162/164 走 Python 适配层。Java 只读 ADS，不算 H 指数、不差分迁徙 |
| 2 调用链：前端 → Java → Python /internal | ✅ 前端不直连久新。IP-06/09/10 的在线链路不经 Python，离线才进 ETL/Job |
| 3 只用 NebulaGraph | ✅ 合作网络（1118）写 TRSGraph，Java 不写 nGQL，在线读 ADS 投影 |
| 4 可观测 | ⚠️ 本页 lumen 尚无实现。契约要求 Java Agent + Python 外呼 span；实现叶补齐 |
| 5 CI/CD | N/A（分析叶，cicd skip） |
| 6 demo 只读 | ✅ demo 只记「有原型」，不把原型数据接进调用链 |
| 7 共享聚合核心 | ✅ Java 门面归属引用 DN-07。`/situation/v1` 现网没有 |
| 8 ADS 先行 + Mock | ✅ 无源走 IP-10。USE_MOCK=false 禁止用 demo 原型填数 |
| 9 D8 | N/A（不改 UI） |
| 10 D9 | ✅ 6 个已挂指标都写入卡片。无注册统计记 metric_missing（10 张）。catalog 现仅 ENT（B01 R3），ⓘ 会空，记 R-A12-5 |
| 11 D10 | N/A（不改 UI） |
| 12 D12 | ✅ 调用链无 demo-*（脚本断言）。lumen 本页无代码，当前没有把 demo 服务接进正式链。正式开发时禁止复用 demo 原型的数据接口 |
| 禁读 registry YAML | ✅ 任务走 MCP。指标口径用材料包，未读 metrics/registry |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | 220000（估算，无 Console 分项） |
| model_used | grok-4.7 |
| actual_cost | 1.19（USD，估算） |
| cost_warn | green |

预算表没有 Grok 单价。成本按 B 档（输入 $3/M、输出 $15/M）和约 80/20 的输入输出比估算：`220000×0.8×3/1e6 + 220000×0.2×15/1e6 = 1.19`。即便按 C 档旗舰价粗算也约 $6，低于 $10 暂停线，不暂停。
