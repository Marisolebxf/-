# ALGO-LIB-ODS-MOCK-SPEC-L01 · 50100 各算法库 Demo ODS 主表 / 列表契约

> 定义·文档叶。锁定每域 **一张** Demo ODS 主表 + 列表/搜索/列头/码值契约，供后续 Mock CRUD 实现叶使用。实现叶 **禁止猜表**。未写业务仓代码、未改 seed/矩阵 YAML、未 commit。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 用户授权连跑；本会话独自完成 SPEC，不问人。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A（定义·文档类）` |
| 说明 | definition 不压文档完整性；未用 YAGNI 跳过架构铁律。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只改编排仓文档，未走 Headroom。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（本叶不改存储流图拓扑） |
| 图 diff | 无。写库方仍 = Demo ODS（`demo_gkxlumenx_ods`）；禁止写 DWD/ADS/正式 `gkxlumenx_*`。 |
| 会签态 | 本叶定义契约；流图会签态仍抄源文件（ENT/CHAIN/SVC/POLICY `01-data-flow.md` 已 `approved`）。 |

## 范围与实现

对照派单包 `ALGO-LIB-ODS-MOCK-CRUD-DISPATCH.md`：

1. 覆盖 50100 侧栏：政策 / 企业(entan) / 产业链 / 产业服务 / 产业综合 / 创新监测。
2. 不做：`lumen-ui-*`、维护管理、科技新闻、ORG/TALENT/TECH 单独菜单。
3. 翻译 = 列头中文 + 码值中文。**不是** locale，**不是** LLM 正文翻译。
4. 搜索 = 服务端过滤字段名单（查询参数）。**禁止**只对已拉列表做前端 filter。
5. 空表：`list=[]` + HTTP 200 诚实空态（政策现网 `dwd_policy_base` 行数 = 0 即此态）。

核对来源（2026-09-01）：

- 现网政策 Mock：`PolicyMockPage.vue` + `polan/mockgen/incr.py` + `GET /v1/policy/mock/policies`
- 现网产业链 indana：`IndanaCrudPage.vue`（行业分析六表，**不是**产业链四表）
- 存储清单：`storage/{POLICY,ENT,CHAIN,SVC}/sources/inventory*.md`
- 现网 `demo_gkxlumenx_ods`：经 10.50.69.111 `demo-platform-entan-py` 只读 `SHOW TABLES` / `SHOW COLUMNS` / 行数（**未写**正式 `gkxlumenx_ods`）

## 已锁主表总表（每域一行 · 实现叶只认此表）

| 域 | 库.表 | 主键 | 列表展示列 | 搜索字段（服务端） | 列头中文映射 | 码值字典 | Python 仓 | 与现有页关系 |
|----|--------|------|------------|-------------------|--------------|----------|-----------|--------------|
| 政策 | `demo_gkxlumenx_ods.dwd_policy_base` | 业务键 `id`（API 暴露 `policy_id`）；物理 PRI=`id` | `id`/`policy_id`, `title`, `ministry`, `publish_date`, `source`, `rank`, `type`；派生 `ingest_status` | `title`, `ministry`, `publish_code`, `rank`, `type` | 见 §政策 | `rank`/`status`/`type`；派生 `ingest_status` | `demo-algo-ent-analysis` | **升级现页** `/policy/mock`「政策 Mock」：只补搜索+列头/码值翻译，不重做攒货 |
| 企业 | `demo_gkxlumenx_ods.dwd_org_base_info` | 业务/物理 PRI=`org_id` | `org_id`, `name_cn`, `city`, `area`, `industry`, `org_type`, `reg_status`, `org_size` | `name_cn`, `org_id`, `external_id`, `city`, `industry` | 见 §企业 | `org_size`/`reg_status`；`org_type` 原文 | `demo-algo-ent-analysis` | **新页** `/entan/mock`「企业 Mock」。`entan/llm_ods` 是灌数生成器，**不是**表名 |
| 产业链 | `demo_gkxlumenx_ods.dwd_industry_chain_info` | 物理 PRI=`pk_id`；业务键 `industry_link_code` | `industry_code`, `industry_name`, `industry_link_code`, `industry_link_name`, `level`, `parent_name`, `node_company_count` | `industry_name`, `industry_link_name`, `industry_code`, `industry_link_code` | 见 §产业链 | `level`→第 N 级节点 | `demo-algo-ent-analysis`（CRUD）；灌数流水线仍在 `demo-algo-science` `--chain` | **新页** `/chain/mock`「产业链 Mock」。**不升级** `/chain/indana` |
| 产业服务 | `demo_gkxlumenx_ods.dwd_org_base_info` | 同企业 `org_id` | **圈定列**：`org_id`, `name_cn`, `city`, `area`, `industry`, `industry_l1_name` | `name_cn`, `org_id`, `city`, `industry`, `industry_l1_name` | 见 §产业服务 | **无**服务类型 ODS 码值；禁止 `org_type` 冒充六类 | `demo-algo-ent-analysis` | **新页** `/industry-service/mock`「产业服务 Mock」。与企业 **共用** 主表，列表只露圈定列 |
| 产业综合 | **n/a** | — | — | — | — | — | — | **不空转页面**。`ALGO-LIB-ODS-MOCK-COMP-L01` → `blocked` |
| 创新监测 | **n/a** | — | — | — | — | — | — | **不空转页面**。`ALGO-LIB-ODS-MOCK-INNOV-L01` → `blocked` |

现网抽检行数（只读，2026-09-01）：政策 `dwd_policy_base`=**0**；企业 `dwd_org_base_info`=**50000**；产业链 `dwd_industry_chain_info`=**1273**；行业分析文档 `dwd_industry_analysis_documents`=**1000**（indana 页，非本波主表）。

---

## 政策（核对现网，已锁）

| 项 | 值 |
|----|-----|
| 库.表 | `demo_gkxlumenx_ods.dwd_policy_base` |
| 主键 | `id` VARCHAR(100)。列表/API 字段名继续用 `policy_id`（`incr.list_policies` 已映射） |
| DDL 真源 | `storage/POLICY/sources/ods-ddl.md`；现网列与 DDL 一致（无 `_demo_id`） |
| 现网 API | `GET/POST/PUT/DELETE /v1/policy/mock/policies`；列表目前仅 `limit` + `pending_only`，**无搜索** |
| 实现叶 | `ALGO-LIB-ODS-MOCK-POLICY-L01`：现页补搜索 + 列头/码值翻译 |

**列表展示列**（列头中文）：

| 字段 | 列头 |
|------|------|
| `policy_id`（←`id`） | 政策ID |
| `title` | 标题 |
| `ministry` | 发布机构 |
| `publish_date` | 发布日期 |
| `source` | 来源标记 |
| `rank` | 层级 |
| `type` | 类型 |
| `ingest_status`（派生，非列） | 状态 |

现页「发布机构」已中文；`policy_id` 列头仍是英文字段名，本波改中文。

**搜索字段**（2–5，服务端 `LIKE`/`=`，AND）：`title`, `ministry`, `publish_code`, `rank`, `type`。查询参数建议 `q_title` / `q_ministry` / `q_publish_code` / `q_rank` / `q_type`（可空）。禁止只滤前端已拉的 200 条。

**码值字典**：

| 字段 | 码 → 中文 |
|------|-----------|
| `rank` | `国家级` / `省级` / `市级` / `区县级`（与 `LEVEL_NAME` 1–4 及表单一致；库内也可存中文原文） |
| `status` | `有效` / `失效`（DDL 注释；详情保留原文） |
| `type` | 政策类型，**自由文本**（如产业政策）；列表展示原文，不做封闭枚举 |
| `ingest_status` | `pending`→待追加；`ingested`→已入库（ODS−DWD 差集派生，不落 ODS 列） |

详情仍可保留 `publish_code` 文号、`province`/`city`/`district`、正文等。本波不改攒货 / LLM 填表。

---

## 企业（已锁一张主表）

候选淘汰：`entan/llm_ods` 是脚本包（写 `dwd_org_*`），不是表。禁止另锁股东/高管/资讯从表当主表。

| 项 | 值 |
|----|-----|
| 库.表 | `demo_gkxlumenx_ods.dwd_org_base_info` |
| 主键 | `org_id` |
| 信用代码列 | `external_id`（现网样本为 18 位统一社会信用代码；**不要**猜 `credit_code` 列——本表无此列名） |
| 实现叶 | 新菜单「企业 Mock」+ `/v1/entan/mock/...` |

**列表展示列**：

| 字段 | 列头 |
|------|------|
| `org_id` | 机构ID |
| `name_cn` | 企业名称 |
| `city` | 城市 |
| `area` | 区县 |
| `industry` | 行业 |
| `org_type` | 机构类型 |
| `reg_status` | 登记状态 |
| `org_size` | 规模 |

**搜索字段**：`name_cn`, `org_id`, `external_id`, `city`, `industry`。

**码值字典**：

| 字段 | 码 → 中文 |
|------|-----------|
| `org_size` | `微型` / `小型` / `中型` / `大型` / `未知`（现网五值） |
| `reg_status` | 现网主值 `存续（在营、开业、在册）`、`在营（开业）企业`；**原文展示**，不做 shrinkage |
| `org_type` | 工商类型自由文本（如「有限责任公司(法人独资)」）；**不封闭枚举** |
| `listing_status` | **不进码值字典**（现网大量空值，非空多为证券代码脏值） |

禁止：写 `enterprise_*` DWD；把 llm_ods 当表名。

---

## 产业链（已锁默认主表 + 与 indana 关系）

### 与 `/chain/indana`「要素库维护（Mock）」关系（拍板）

**新开「产业链 Mock」页**（`/chain/mock`），**不升级** indana 同页。

| 现网页 | 要素库 | ODS 表族 | 本波 |
|--------|--------|----------|------|
| `/chain/indana` 要素库维护（Mock） | 行业分析六表 | `dwd_industry_analysis_*`，主表 `dwd_industry_analysis_documents` | **保持原页**；本波不改其 CRUD 契约 |
| 新 `/chain/mock` 产业链 Mock | 产业链四表 | 默认主表 `dwd_industry_chain_info` | **本波实现叶** |

理由：两套 sheet/表族在 `storage/CHAIN` 已并列切片（`inventory.md` vs `inventory-industry-analysis.md`）。indana 页写的是文档+五从表，不是产业链节点树。糊进同一页会让实现叶猜表。

可选页签（仍指定默认主表 = 图谱表）：

| 页签 | 表 | 本波 |
|------|-----|------|
| 默认「产业链节点」 | `dwd_industry_chain_info` | **主表，必做 CRUD+搜索+翻译** |
| 「关联企业」 | `dwd_org_industry_tags` | 可选只读/后补；**不得**替代主表 |
| 「关联产品」 | `dwd_org_industry_product_tags` | 同上 |
| 「产业资讯」 | `dwd_industry_chain_news_info` | **禁止**（清单已标不可用） |

| 项 | 值 |
|----|-----|
| 库.表（默认主表） | `demo_gkxlumenx_ods.dwd_industry_chain_info` |
| 主键 | 列表/编辑键优先 `pk_id`；业务键 `industry_link_code`（UNIQUE 语义，现网 MUL） |
| Python | CRUD 落 `demo-algo-ent-analysis`（与 chain ODS DDL / 现网 entan API 同仓）。`demo-algo-science` 的 `--chain` 灌数入口 **不改仓** |

**列表展示列**：

| 字段 | 列头 |
|------|------|
| `industry_code` | 产业链编码 |
| `industry_name` | 产业链名称 |
| `industry_link_code` | 节点代码 |
| `industry_link_name` | 节点名称 |
| `level` | 节点层级 |
| `parent_name` | 父级节点 |
| `node_company_count` | 节点企业数 |

**搜索字段**：`industry_name`, `industry_link_name`, `industry_code`, `industry_link_code`。

**码值字典**：

| 字段 | 码 → 中文 |
|------|-----------|
| `level` | 现网 0–7 整数。展示 **`第{n}级`**（文档无国家级那种封闭中文档；禁止编造「领域/链/环节」专名除非另有会签） |

---

## 产业服务（已锁 · 禁止平行表）

| 项 | 值 |
|----|-----|
| 库.表 | `demo_gkxlumenx_ods.dwd_org_base_info`（与企业 **共用**；本域 **无独有 ODS 主表**） |
| 主键 | `org_id` |
| 列表列 | **只圈定列**，禁止把机构主表全列当本页主路径 |

**禁止（实现叶抄）**：

- 新建 / 启用平行主体表 `svc_org_base`
- 把现网遗留 `demo_gkxlumenx_ods.dwd_service_org`（`_demo_id` + `demo-svc-*`，50 行）当本波 Mock 主表
- 复制 `dwd_org_base_info` 全列到另一张 SVC 表
- 用 `org_type` 当服务机构六类（`svc_rule_demo_kw_v1` 已禁）

**列表展示列**（圈定列）：

| 字段 | 列头 |
|------|------|
| `org_id` | 机构ID |
| `name_cn` | 机构名称 |
| `city` | 城市 |
| `area` | 区县 |
| `industry` | 行业 |
| `industry_l1_name` | 行业门类 |

**搜索字段**：`name_cn`, `org_id`, `city`, `industry`, `industry_l1_name`。

可选：列表可用 `svc_rule_demo_kw_v1.1` 做 **服务端** 圈定过滤（查询参数 `circled_only=true`）；命中过少则诚实少行，禁止 fixture 补齐。规则命中是过滤，不是第二张主表。

**码值字典**：本表 **无** 服务类型码值列。六类候选只存在 DWD `svc_org_circle.service_type_candidate`，本波 Mock **不写 DWD**。页面不展示伪「科技金融/知识产权/…」下拉（那是 `dwd_service_org.org_type` 遗留值，禁止搬到主路径）。

与企业 Mock 关系：两页可同时改同一张 ODS；产业服务页不得提供企业页已有的全列编辑（资本、法人、经纬度等）。实现叶若做编辑，只允许改圈定列 + 技术列（`table_data_source`/`operator_remarks` 等），禁止借本页改工商全档。

---

## 产业综合 = n/a

`storage/` 仅 ENT / CHAIN / POLICY / SVC，**无 COMP ODS 清单**。50100「产业综合分析算法库」十模型读的是 **上游 ADS/依赖**，不是本域贴源主表。

现网 `demo_gkxlumenx_ods` 无 `*comp*` / `*synth*` 综合主表（`SHOW TABLES LIKE '%comp%'` 命中的是公司/构成类表，属企业或行业分析）。

**决议**：本域 **n/a**。禁止为凑菜单造一张综合 ODS。`ALGO-LIB-ODS-MOCK-COMP-L01` 开工前应变 `blocked`（blocked_by=本 SPEC：无独立 Demo ODS 主表），**不空转「综合 Mock」页**。

---

## 创新监测 = n/a

核对后 **没有** 可锁的一张「事件/载体」三方约定 ODS 主表：

| 候选 | 结论 |
|------|------|
| `innov` mockgen `ods.news` / `ods.org_reg_info` 等 | 映射到 `demo_gkxlumenx_ods.news` 等；**现网库中不存在**这些表 |
| `demo_gkxlumenx_ods.dwd_event` | 存在（20 行），但是医药论坛/展会标题；**未进入** `innov_table_map.yaml`，算法读 ADS `innovation_event` ← DWD `event_std` ← 仓内 mock `ods_*`，**禁止猜绑** |
| 载体 | ODS 无 `*carrier*`；载体在 DIM `dim.carrier`，不是 Demo ODS 主表 |

**决议**：本域 **n/a**。`ALGO-LIB-ODS-MOCK-INNOV-L01` → `blocked`（无已建且算法认领的 Demo ODS 事件/载体主表），**不空转「创新 Mock」页**。若后续单独建 `dwd_*` 科创事件约定表，另开 SPEC 修订，禁止实现叶自填。

科技新闻四要素复核不在本波（派单已排除）。

---

## 翻译 / 搜索铁律（各 coding `/goal` 必抄）

1. 列头用上表中文；禁止列表只显示英文字段名（政策 `policy_id` 列头现状即反例）。
2. 码值：列表/筛选项显示中文；详情可保留原始码。
3. 搜索必须进 Python SQL（`WHERE` 参数化）；禁止前端 `rows.filter`。
4. `USE_MOCK=false` / 顶栏 live：**禁止写**；禁止 fixture 填列表。空表返回 200 + `list=[]`。
5. 调用链：50100 → `demo-platform-gateway` → Python `/v1/{域}/mock`；禁止前端直连 Python、禁止 lumen 调 demo。
6. 不写 DWD/ADS/正式库。本 SPEC 不改流图。

## 实现叶派单提示（SPEC 完成后）

| 叶 | 主表 | 菜单 | 监管人（派单包） |
|----|------|------|------------------|
| POLICY-L01 | `dwd_policy_base` | 现页增强 | `human:淮政玮` |
| ENT-L01 | `dwd_org_base_info` | 新「企业 Mock」 | `human:徐滕强` |
| CHAIN-L01 | `dwd_industry_chain_info` | 新「产业链 Mock」；indana 不动 | `human:李伟` |
| SVC-L01 | `dwd_org_base_info` 圈定列 | 新「产业服务 Mock」 | `human:侯佳伟` |
| COMP-L01 | n/a | 不建页 | `human:淮政玮` → **blocked** |
| INNOV-L01 | n/a | 不建页 | `human:淮政玮` → **blocked** |

同仓同时只一张 coding 单（`demo-ui-system-test` / `demo-algo-ent-analysis`）。

## 偏离说明

无范围偏离。COMP/INNOV 按派单允许标 n/a，而不是空转页面。

## 产物清单

| 产物 | 路径 |
|------|------|
| 本 handoff | `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-ODS-MOCK-SPEC-L01.md` |
| 派单包 §3.1 已锁总表 | `…/ALGO-LIB-ODS-MOCK-CRUD-DISPATCH.md` |

## 测试结果

- 定义叶：以现网 DDL/行数/代码对照锁表；未跑 UI/CI。
- SSH 只读 `demo_gkxlumenx_ods` 成功；**零写入**正式 `gkxlumenx_ods`。

## 遗留风险

- 企业与产业服务共用 `dwd_org_base_info`：两页并发编辑同一 `org_id` 可能互相覆盖圈定列；实现叶须按域限制可写列。
- 政策 ODS 现为空：搜索/翻译可在空态验收；有数后再回归。
- COMP/INNOV blocked：若甲方坚持要页，须先补约定 ODS 表并修订本 SPEC。

## CI/CD（必填）

- 分支：未 commit（用户未要求）
- commit：N/A
- pipeline URL / ID：N/A（definition / cicd skip）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL：N/A（无代码）

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A（文档）
- 实现叶新路由须带现有 `X-Trace-Id` / `observability.ts`

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 契约指向 Python Mock CRUD；Java 不写 ODS |
| 2 | 调用链 前端→Java→Python | ✅ 50100 → gateway → `/v1/{域}/mock` |
| 3 | 图谱 NebulaGraph | ✅ N/A（本叶不写图） |
| 4 | 可观测性 | ✅ 实现叶沿用；本叶无新路由 |
| 5 | CI/CD | ✅ skip（definition） |
| 6 | demo 不污染 lumen | ✅ 只改 orchestration 文档 |
| 7 | 方案 A | ✅ Java 不直连 ODS |
| 8 | 数据走 ADS | ✅ Mock 只写 Demo ODS；不写 DWD/ADS |
| 9 | D8 | ✅ N/A（无 UI；实现叶 50100 Element Plus） |
| 10 | D9/D10 | ✅ N/A（联调台 Mock 工作台，非指标卡页） |
| 12 | D12 lumen 不调 demo | ✅ 禁止改 lumen-ui-* |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 72000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.85 |
| cost_warn | green |

## 明确未做

- 未开始 POLICY/ENT/CHAIN/SVC coding 叶
- 未改 `demo-ui-system-test` / Python 仓
- 未 git commit / push
- 未把 COMP/INNOV 叶改为 blocked（registry 状态由 coordinator 随后改；本 SPEC 已给出 blocked 理由）
