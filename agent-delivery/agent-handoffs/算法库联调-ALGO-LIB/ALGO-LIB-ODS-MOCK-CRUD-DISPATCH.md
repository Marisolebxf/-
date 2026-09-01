# 派单包：50100 各算法库 ODS 主表 Mock CRUD

- **状态**：2026-09-01 SPEC 已锁主表（`ALGO-LIB-ODS-MOCK-SPEC-L01`）；实现叶禁止猜表，COMP/INNOV = n/a 不得空转页面
- **派发角色**：coordinator-agent
- **承接**：`agent:algorithm-agent`（Python `/v1/{域}/mock/*` + 接线）；UI 落 `demo-ui-system-test`，`collaborators: frontend-agent`
- **监管人**：SPEC / POLICY / COMP / INNOV = `human:淮政玮`；ENT=`human:徐滕强`；CHAIN=`human:李伟`；SVC=`human:侯佳伟`
- **仓**：`demo-ui-system-test` + 对应 Python（政策/企业/服务默认 `demo-algo-ent-analysis`）；**禁止**改 `lumen-ui-*`（D12）
- **Epic**：`E-ALGO-LIB-DEMO`
- **Sprint**：`2026-W36`
- **强度**（coding 叶 `/goal` 必带）：`ponytail full`

---

## 0. 已拍板（勿再议）

| # | 决策 | 值 |
|---|------|-----|
| 1 | 现场 | **50100** `GKX 系统和算法`（`demo-ui-system-test` → `demo-platform-gateway` → Python） |
| 2 | 菜单形态 | 每个算法库侧栏底部一条 **`{维度} Mock`**，对标现网「政策 Mock」 |
| 3 | 数据面 | **只写当前面 Demo ODS 主表**；不入 DWD、不重算 ADS、不写正式 `gkxlumenx_*`；顶栏 live 禁止写 |
| 4 | 列表能力 | **关键字段搜索**（服务端过滤）+ **翻译**（列头中文 + 码值/枚举中文）。**不是** locale 切换，**不是** LLM 正文翻译 |
| 5 | 政策现状 | 已有 CRUD / LLM 填表 / 差集追加（`POLICY-MOCK-INCR-L01`）。本波政策叶 **只补搜索+翻译**，不重做攒货 |
| 6 | 本波不做 | `lumen-ui-algo-apiview`；维护管理；科技新闻四要素复核；ORG/TALENT/TECH 单独算法库菜单（50100 无此侧栏） |

覆盖侧栏（`src/layout/menuConfig.ts`）：

| 侧栏 | 菜单文案（暂定） | 实现叶 |
|------|------------------|--------|
| 政策分析算法库 | 政策 Mock（已有，增强） | `ALGO-LIB-ODS-MOCK-POLICY-L01` |
| 企业分析算法库 | 企业 Mock | `ALGO-LIB-ODS-MOCK-ENT-L01` |
| 产业链分析算法库 | 产业链 Mock | `ALGO-LIB-ODS-MOCK-CHAIN-L01` |
| 产业服务算法库 | 产业服务 Mock | `ALGO-LIB-ODS-MOCK-SVC-L01` |
| 产业综合分析算法库 | 综合 Mock | `ALGO-LIB-ODS-MOCK-COMP-L01` |
| 展示系统 → 创新监测 | 创新 Mock | `ALGO-LIB-ODS-MOCK-INNOV-L01` |

---

## 1. 背景

政策 Mock 能对 `demo_gkxlumenx_ods.dwd_policy_base` 做增删改查，但列表无搜索、列头多为英文字段。其余算法库没有对等的 ODS 主表工作台。空 ODS 时列表应诚实空态（见 trace `9728323964a5cb7efce47de2bf2c76c3`：接口 200、`ods_count=0`），不得 fixture 填数。

---

## 2. 产物落点

| 产物 | 路径 |
|------|------|
| 主表/搜索/列头契约 | 本包 SPEC 叶 handoff + 下表（SPEC 填绿，禁止实现叶自填） |
| UI | `demo-ui-system-test/src/views/{域}/` 菜单 + Mock 页 |
| API | 对应 Python `GET/POST/PUT/DELETE /v1/{域}/mock/...`，包络 `{code,msg,data}`，带 `X-Trace-Id` |

---

## 3. 叶拆

| ID | type | 做什么 | 依赖 | 初始状态 |
|----|------|--------|------|----------|
| `ALGO-LIB-ODS-MOCK-SPEC-L01` | definition | 锁每域 **一张** ODS 主表（库.表）+ 主键 + 列表列 + 搜索字段 + 列头中文 + 码值字典；定产业链与「要素库维护（Mock）」关系；综合无主表则标 n/a 不空转 | 无 | **ready** |
| `ALGO-LIB-ODS-MOCK-POLICY-L01` | feature | 现页补搜索 + 列头/码值翻译 | SPEC | backlog |
| `ALGO-LIB-ODS-MOCK-ENT-L01` | feature | 企业 Mock CRUD+搜索+翻译 | SPEC | backlog |
| `ALGO-LIB-ODS-MOCK-CHAIN-L01` | feature | 产业链 Mock（按 SPEC：升级 indana 或新页） | SPEC | backlog |
| `ALGO-LIB-ODS-MOCK-SVC-L01` | feature | 产业服务 Mock；**禁止**平行 `svc_org_base` | SPEC | backlog |
| `ALGO-LIB-ODS-MOCK-COMP-L01` | feature | 综合 Mock；SPEC=n/a 则本叶 `blocked` 不空转 | SPEC | backlog |
| `ALGO-LIB-ODS-MOCK-INNOV-L01` | feature | 创新监测 Mock | SPEC | backlog |

**SPEC 强度**：definition，**禁止** ponytail 行。其余 coding：`ponytail full`。

### 3.1 SPEC 已锁主表（实现叶不得猜；真源 `ALGO-LIB-ODS-MOCK-SPEC-L01.md`）

| 域 | 库.表 | 主键 | 列表展示列 | 搜索字段（服务端） | 列头中文映射 | 码值字典 | Python 仓 | 与现有页关系 |
|----|--------|------|------------|-------------------|--------------|----------|-----------|--------------|
| 政策 | `demo_gkxlumenx_ods.dwd_policy_base` | `id`（API=`policy_id`） | policy_id, title, ministry, publish_date, source, rank, type；派生 ingest_status | title, ministry, publish_code, rank, type | 政策ID/标题/发布机构/发布日期/来源标记/层级/类型/状态 | rank 国家级\|省级\|市级\|区县级；status 有效\|失效；ingest_status 待追加\|已入库；type 原文 | `demo-algo-ent-analysis` | **升级** `/policy/mock`（只补搜索+翻译） |
| 企业 | `demo_gkxlumenx_ods.dwd_org_base_info` | `org_id` | org_id, name_cn, city, area, industry, org_type, reg_status, org_size | name_cn, org_id, external_id, city, industry | 机构ID/企业名称/城市/区县/行业/机构类型/登记状态/规模 | org_size 微型\|小型\|中型\|大型\|未知；reg_status 原文；org_type 原文 | `demo-algo-ent-analysis` | **新页** `/entan/mock`；llm_ods≠表 |
| 产业链 | `demo_gkxlumenx_ods.dwd_industry_chain_info` | 物理 `pk_id`；业务 `industry_link_code` | industry_code, industry_name, industry_link_code, industry_link_name, level, parent_name, node_company_count | industry_name, industry_link_name, industry_code, industry_link_code | 产业链编码/名称/节点代码/节点名称/节点层级/父级节点/节点企业数 | level → 第N级 | `demo-algo-ent-analysis`（CRUD） | **新页** `/chain/mock`；**不升级** `/chain/indana`（行业分析六表保持原页）。可选页签 tags/product，资讯表禁用 |
| 产业服务 | `demo_gkxlumenx_ods.dwd_org_base_info`（与企业共用；只露圈定列） | `org_id` | org_id, name_cn, city, area, industry, industry_l1_name | name_cn, org_id, city, industry, industry_l1_name | 机构ID/机构名称/城市/区县/行业/行业门类 | **无**服务类型 ODS 码值；禁 org_type 冒充六类；禁 `svc_org_base`；禁遗留 `dwd_service_org` 当主表 | `demo-algo-ent-analysis` | **新页** `/industry-service/mock` |
| 综合 | **n/a** | — | — | — | — | — | — | COMP 叶 **blocked**，不空转页面 |
| 创新 | **n/a** | — | — | — | — | — | — | INNOV 叶 **blocked**（无算法认领的已建事件/载体 ODS 主表），不空转页面 |

---

## 4. 实现铁律（coding `/goal` 必抄）

1. 调用链：前端 → Java 网关 `/policy|/entan|/chain|...` → Python `/v1/.../mock`；禁止前端直连 Python、禁止 lumen 调 demo。
2. `USE_MOCK=false` / live 面：禁止 fixture 填列表。
3. 搜索走查询参数，在 ODS 过滤；禁止只对已拉 200 条做前端 filter 冒充搜索。
4. 翻译：列头中文映射 + 码值字典（如政策 `level` 1→国家级）；原始码可保留在详情。
5. 空表：`list=[]` + 诚实空态（对标政策「待追加 0」），HTTP 200。
6. 可观测：现有 `observability.ts` / `X-Trace-Id`；新路由不要漏。
7. D8：本页是 50100 Element Plus 联调台，**不**按 Arco Design.md 重做视觉；交互对齐现网政策 Mock。
8. 同仓同时只一张 coding 单（`demo-ui-system-test` / `demo-algo-ent-analysis`）。

---

## 5. `/goal` 摘要（SPEC 完成后填主表名再派）

```
/goal ALGO-LIB-ODS-MOCK-{域}-L01
监管人：human:{上表}
仓：demo-ui-system-test + {python repo}
强度：ponytail full
图：本叶不改存储流图拓扑；写库方仍=Demo ODS（见 SPEC 主表）
范围：侧栏「{维度} Mock」；主表见本包 §3.1 已锁库.表；CRUD；列表关键字段搜索；列头+码值中文。
禁止：写 DWD/ADS/正式库；lumen-ui-*；fixture 冒充 ODS；COMP/INNOV 空转页面。
DoD：见 registry。
```
