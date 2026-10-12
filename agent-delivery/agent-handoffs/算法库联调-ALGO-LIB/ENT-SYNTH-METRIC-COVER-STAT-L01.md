# ENT-SYNTH-METRIC-COVER-STAT-L01 · 137 Wave1 STAT/COMPUTE 口径跟表

> 格式参考 `templates/handoff-template.md`。定义叶；**不写业务仓代码**。范围 = ENT STAT 47 + ENT COMPUTE 2 + SYNTH STAT 6 = **55**。  
> 口径一条一过已落 seed / 细稿 / 矩阵 D1。**公式会签（唐绍祖）未做**，本单不能自称 `done`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:徐滕强` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 企业模块架构师 lead 监管；一条一过口径由本机会话落盘 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义·注册表口径；不以缩 YAML 为目标。D9 8 件套 + 四维按 COVER-STAT 尺子写，不跳过 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 定义叶；不压缩会签原文 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 未改调用链 / 存储流图 |
| 会签态 | `draft`（待 `human:唐绍祖` 签公式） |
| 说明 | 无 Mermaid 契约图 |

---

## 范围与实现

对照 `metrics/request/专题系统/ENT-COVER-STAT-定义分流-20260904.md`（A14 / B29 / C12）+ live ABC 尺子（LANDING-DECIDE 锁定）：

- **A 14**：D1 本已 `aligned`，本波不重裁 ABC；只保持 formula 与 `source_tables` 一致。
- **B 29**：团队默认写入 seed；`M_ENT_RECOMMEND_COUNT` 阈值本波钉 **70**（招引/培育同一条，Q015 仍 🟡）。
- **C 12**：算法 2026-09 默认已落盘（权重 / 协同 / 密度分母 / 链完整度 / 创新型四码 / 核心供应商投资 TOP5 / 短板同链 / SCORE=INDEX 别名）。
- 分析源口径写项目 DWD `<- ods:`；二次 STAT/COMPUTE 右端 `metric:`。
- **D3 不升 `full`，D4 不升 `live`**。`is_mock: true`。甲方 Q 不升 🟢。
- 未另开 L01 公式叶。未改 MODEL/GRAPH 叶公式。

## 偏离说明

- 原 DoD「约 ENT 17 + COMPUTE 2 + SYNTH 6」被分流清单扩成 **55**（含 L01 已过 STAT 的 formula 跟表）。不另拆叶。
- C 桶「都留 SCORE」落地为 **INDEX 别名**，不另算第二套三维。
- `RECOMMEND_COUNT` 矩阵原先缺行，本波补在 `CULTIVATION_INDEX` 后。
- 协同事件三种里，项目/人才流动 **无对等项目 DWD**：标缺口，只通联合专利一路。不是「无法执行」抹口径。
- 唐绍祖公式会签 **未发生**。监管人未口头「会签通过」。

## 本波 ID 清单

### 复用（A · 不重裁 ABC，14）

`M_ENT_TOTAL_COUNT` · `NEW_COUNT_Y` · `SZ_COUNT` · `SZ_CHAIN_POSITION` · `DOMAIN_COVERAGE_COUNT` · `AVG_RD_INVESTMENT` · `DEV_HISTORY` · `PATENT_TOTAL` · `PATENT_GRANT_COUNT` · `REVENUE_LATEST` · `REVENUE_GROWTH_RATE` · `PROFIT_MARGIN` · `MARKET_SHARE` · `TYPE_RATIO`

### 团队默认写入（B · 29）

高企/六类/匹配/重点类型分布/`KEY_TOTAL`/`KEYPANO_*`×7 / 覆盖广度 / 领域分布 / 未来产业覆盖 / 区域家数与专题占比 / 深圳清单 / 资讯月统计 / 科研人数 / 明星 / 供应商 / 研发占比 / 技术力与竞争力排名 / `VIT_RANK` / `ELEM_RANK` / `CITY_AVG_TECH_POWER` / **`RECOMMEND_COUNT`（≥70）**

### 算法默认写入（C · 12）

| ID | 本波默认 |
|----|----------|
| `M_SYNTH_VIT_WEIGHT` | 0.25×4；不展示权重 |
| `M_SYNTH_ELEM_WEIGHT` | 1/3×3 |
| `M_SYNTH_COLLAB_COMPLETENESS` | n/N×100；N=企∪院∪人含无边 |
| `M_SYNTH_COLLAB_RELATION_INPUT` | 专利申请号≥2 主体；项目/流动无表=缺口 |
| `M_ENT_CITY_DENSITY` / `REGIONAL_DENSITY` | 分母 `code_region.area`；全国/国外不算 |
| `M_ENT_CHAIN_COMPLETENESS` | k/K×100；K=INB 叶子；全目录；不加权 |
| `M_ENT_INNOVATIVE_COUNT` | 四码并集；曾获算 |
| `M_ENT_CORE_SUPPLIER_COUNT` | 一级供应商 ∩ 投资 TOP5 |
| `M_ENT_SHORTBOARD_COUNT` | 同链同年；空值不判 |
| `M_ENT_ATTRACT_SCORE` | = `M_ENT_ATTRACTION_INDEX` |
| `M_ENT_CULTIVATE_SCORE` | = `M_ENT_CULTIVATION_INDEX` |

公式是否改：A 少数跟表；B/C **改了** definition / formula / `source_tables` / 细稿；矩阵 **只动 D1 + `d3_gap` 文案**，D3/D4 枚举未升。

## 测试结果

- 注册表 lib：ENT STAT+COMPUTE **49/49 D1=`aligned`**；SYNTH 本单 6 条 D1=`aligned`。
- 55 条均有 `formula` + `calc_logic_ref`。
- `node scripts/metric-mcp-selfcheck.mjs`：本叶收口时以 catalog join 为准；进度 xlsx **未**当本单产物提交。
- 未跑业务 CI（编排仓定义叶）。

## 遗留风险

- **唐绍祖未签公式** → 不能 AV-1 / `ready_to_sign`。
- Q010/Q011/Q012/Q015/Q016/Q017/Q038 等仍 🟡。
- INDEX / SCORE / 竞争力 MODEL 本波无出数；二次 COUNT 能写不能现算。
- 无独立目标 ADS 表多条（细稿已标缺口）；本波不改 GDF DDL。
- 父单 `ENT-SYNTH-METRIC-COVER-P01` 仍 `backlog`（MODEL/GRAPH Wave 未拆执行）。

## 产物清单

| 产物 | 路径 |
|------|------|
| 定义分流 | `metrics/request/专题系统/ENT-COVER-STAT-定义分流-20260904.md` |
| ENT / SYNTH seed | `metrics/registry/cfg_metric-ENT-seed.yaml` · `cfg_metric-SYNTH-seed.yaml` |
| ENT / SYNTH 矩阵 | `metrics/registry/metric-readiness-matrix-ENT.yaml` · `metric-readiness-matrix-SYNTH.yaml` |
| 细稿 | `metrics/calc-logic/ENT/*.md` · `metrics/calc-logic/SYNTH/{VIT,ELEM}_{WEIGHT,RANK}.md` · `M_SYNTH_COLLAB_*.md` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/ENT-SYNTH-METRIC-COVER-STAT-L01.md` |

## 验收证据

- 分流 A14+B29+C12 = 55；C 桶与 `RECOMMEND_COUNT=70` 经监管人点头后落盘。
- D4 仍 `mock` / 部分 SYNTH RANK `n/a`；无 D3 `full` 因本波新裁而升。
- 待：`human:唐绍祖` 会签公式 → 看板 `integration` 注「会签通过」→ coordinator AV-1 → `human:淮政玮` 签收。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java NLP/图谱算法 |
| 调用链 | ✅ 未改前端→Java→Python `/internal/*` |
| 图谱 Nebula | ✅ 未引入 Neo4j；未写正式 `gkx_chain` |
| 可观测 | ✅ N/A（定义叶） |
| CI/CD | ✅ `cicd: skip`（编排仓注册表） |
| D12 demo/lumen | ✅ 未改业务仓、禁止数 demo `svc_*` |
| 方案 A / ADS | ✅ Java 仍只读 ADS；本波不建目标表 DDL |
| D8/D10 | ✅ N/A（无前端页） |
| D9 8 件套 / 四维 | ✅ formula 与 `source_tables` 同批；D1 aligned ≠ 伪 D4 live；缺口进 8 件套 |

## CI/CD（必填）

- 分支：`dev` → `origin/dev`
- commit：见 git（本 handoff 同批）
- pipeline URL / ID：`cicd: skip`
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL：N/A（定义叶）

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- traceId：N/A
- Tempo / Loki：无

## Cost（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 900000 |
| model_used | grok-4.6（收口）+ 前期多会话一条一过 |
| actual_cost | 9.20 |
| cost_warn | green |

多会话累计估；未超 $10 硬暂停线。

## 下一步

- 状态目标：`in_progress` → **`integration`（会签中）**。`ready_to_sign` 等唐绍祖会签关键词进 `note`。`done` 只等 `human:淮政玮`。
- 企业 STAT/COMPUTE 定义执行面齐。产业链 / 服务链 STAT+COMPUTE 另开分流，不挤进本叶。
