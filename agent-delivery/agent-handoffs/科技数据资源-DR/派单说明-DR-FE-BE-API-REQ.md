# 派单说明 · 科技数据资源 · FE 后台需求 + 聚合调科学数据中心（两叶）

> 建单日：2026-11-11  
> 监管人：**human:淮政玮**（两叶统一）  
> Epic：`E-FE-DATA-RESOURCES`  
> 调用链：**前端 → 聚合服务（Java BFF）→ 科学数据中心（第三方接口）**；本模块**仅接口对接**，不做数据集成。  
> 过程夹索引：`工程过程/04-系统集成/05-展示系统集成/派单说明-DR-FE-BE-API-REQ.md`

---

## 总览

| 顺序 | task-id | 执行 | 状态 | 一句话 |
|---|---|---|---|---|
| 1 | `FE-DR-BE-API-REQ-L01` | frontend-agent | ready | 前端要**聚合服务**提供什么（四 GET Dataset） |
| 2 | `BE-DR-FE-API-ALIGN-L01` | api-agent | backlog | 聚合服务要调**科学数据中心**哪些接口（粗粒度需求表）+ 与 FE/契约差异 |

依赖：叶 2 依赖叶 1 草稿可用 + `BE-DR-CONTRACT-01` + `DR-RES-C4-L01`。  
铁律：前端不直连科学数据中心；不写 gapfill DDL；不改业务仓代码（默认）；对科学数据中心**不做数据集成**。

认领：`supervised_by=human:淮政玮`。任务只用 MCP；禁读 `task-registry.yaml`。

---

## 叶 1 · FE-DR-BE-API-REQ-L01

```text
/goal frontend-agent
身份：你是展示系统前端工程师。本单是定义任务：只整理「前端要聚合服务（Java BFF）提供什么 HTTP」，不写实现代码。
强度：ponytail off（definition）。
任务：FE-DR-BE-API-REQ-L01
标题：科技数据资源：依据现有前端整理后台接口需求草稿（四 GET Dataset）
监管人：human:淮政玮
执行：agent:frontend-agent
状态：ready。认领后 in_progress。勿自行 done（definition；done 仅 human:淮政玮）。
仓：gkx-orchestration（只改 agent-delivery 文档）。不改 lumen-ui-science-pc / lumen-svc-platform 代码。
协作：api-agent 只读对照。

目标：审定/补齐「前端 → 聚合服务」接口需求，供叶 2 推导「聚合 → 科学数据中心」上游接口需求。
已有草稿：agent-delivery/agent-handoffs/科技数据资源-DR/FE-DR-BE-API-REQ-DRAFT.md

必读：
- lumen-ui-science-pc/src/types/dataResources.ts
- lumen-ui-science-pc/src/api/dataResources.ts（real() 仍回种子、未接网关）
- lumen-ui-science-pc/src/mock/modules/dataResources.ts + dataResourcesSeed.ts
- lumen-ui-science-pc/src/views/data-resources/{overview,access,theme,application}/
- agent-delivery/agent-handoffs/科技数据资源-DR/BE-DR-CONTRACT-01.md
- agent-delivery/工程过程/04-系统集成/05-展示系统集成/方案-科技数据资源-后台接口.md §5

范围：
1. 仅四个无参 GET：/display/v1/data-ops/{overview|access|theme|application}/dataset
2. PigX 信封 code=0 → data；空库仍 0，数组 []、键保留
3. 按四 Dataset 列出前端必有根键 + 对应界面（总体/接入/主题/应用）
4. 写明前端不直连科学数据中心、不要 R-01～R-24 直出、不要筛导出/WS 等
5. 待对齐项交给叶 2

不做：不改接线；不写科学数据中心明细；不写 DDL；不替代契约冻结正文。

DoD：
1. 修订或确认 FE-DR-BE-API-REQ-DRAFT.md
2. 覆盖四视窗四 GET；写明未接网关事实
3. 列出待对齐项给 BE-DR-FE-API-ALIGN-L01
4. handoff：agent-handoffs/科技数据资源-DR/FE-DR-BE-API-REQ-L01.md；ponytail: off
5. 禁止自行 done

认领：task-claim id=FE-DR-BE-API-REQ-L01 claimed_by=agent:frontend-agent supervised_by=human:淮政玮
```

---

## 叶 2 · BE-DR-FE-API-ALIGN-L01

```text
/goal api-agent
身份：你是展示系统聚合服务（Java BFF）侧接口工程师。本单重点：整理「聚合服务调用第三方科学数据中心」的接口需求；接口需求不要求过细。顺带对照 FE 草稿与 BE-DR-CONTRACT-01 / C1～C4 的差异（默认不改契约、不改前端、不扩对外四 GET）。
强度：ponytail off（definition）。
任务：BE-DR-FE-API-ALIGN-L01
标题：科技数据资源：聚合服务调科学数据中心接口需求 + FE/契约差异
监管人：human:淮政玮
执行：agent:api-agent
状态：backlog。须 FE-DR-BE-API-REQ-L01 草稿经监管人可用后再认领；依赖 BE-DR-CONTRACT-01、DR-RES-C4-L01。
仓：gkx-orchestration（文档/handoff）。可读 lumen-svc-platform data-ops，本叶不强制改码。
协作：frontend-agent。

目标（主）：
在聚合服务中调用第三方「科学数据中心」——输出一份接口需求表（粒度粗即可），每条至少含：
1. 哪个界面需要（总体视窗 / 接入视窗 / 主题视窗 / 应用视窗；可落到页面区块名）
2. 对应需规条目（seq，如 330–399 中相关号；可多对一）
3. 接口中文名称（可对齐 EXT-B3-RESOURCE R-xx 名称，或科学数据中心侧现名）
4. 接口输入参数：哪些必填、哪些选填（参数名 + 必填/选填即可，不必写完整 JSON Schema）
5. 接口期望的输出参数（响应里聚合服务要用的字段/对象，列名级即可，不必嵌套到叶子）

约束：本模块仅接口对接、不做数据集成；前端不直连科学数据中心；不把门户「科技资源服务」算进本轨。

目标（辅）：
对照 FE-DR-BE-API-REQ-DRAFT ↔ BE-DR-CONTRACT-01 / C1～C4：一致/多种子键/缺键/多余键；种子多出类型无的键建议禁止 HTTP 出站。

必读：
- agent-delivery/agent-handoffs/科技数据资源-DR/FE-DR-BE-API-REQ-DRAFT.md
- agent-delivery/agent-handoffs/科技数据资源-DR/BE-DR-CONTRACT-01.md
- agent-delivery/agent-handoffs/科技数据资源-DR/DR-RES-C1-L01.md ～ C4
- lumen-ui-science-pc/src/types/dataResources.ts
- agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/外部接口依赖/04-科技数据资源与服务全景-第三方API接口清单.md（R-01～R-24 名称参考）
- agent-delivery/工程过程/04-系统集成/05-展示系统集成/对接澄清-科技数据资源-字段级.md（字段线索，勿写成数据集成）
- agent-delivery/工程过程/04-系统集成/05-展示系统集成/能力对照-科技数据资源-科学数据中心.md

交付物：
- 主表：agent-delivery/agent-handoffs/科技数据资源-DR/BE-DR-SDC-UPSTREAM-API-REQ.md
  （科学数据中心上游接口需求；表格列=界面|需规seq|接口中文名|输入必填|输入选填|期望输出）
- 辅：同夹 BE-DR-FE-API-ALIGN-L01.md（FE↔契约/C 差异摘要，可短）
- handoff：同夹 BE-DR-FE-API-ALIGN-L01.md 内含 evidence 指针；ponytail: off

不做：
- 不写过细 OpenAPI/样例报文（除非监管人另要）
- 不写库表 DDL、不写数据集成 AH 清单
- 未经 human:淮政玮 批准不改契约正文、不改前端 types
- 不把本叶标 done（仅人签收）

DoD：
1. 上游接口需求表覆盖四视窗，列齐全（界面/需规/中文名/入参必填·选填/期望出参）
2. 写明调用方=聚合服务、提供方=科学数据中心
3. FE↔契约差异有结论（可附在同一 handoff）
4. 状态可至 ready_to_sign；done 仅 human:淮政玮

认领：task-claim id=BE-DR-FE-API-ALIGN-L01 claimed_by=agent:api-agent supervised_by=human:淮政玮
```

---

## 监管人检查清单（human:淮政玮）

- [ ] FE 叶只描述「前端→聚合」四 GET，未要求直连科学数据中心  
- [ ] api-agent 主交付是「聚合→科学数据中心」粗粒度接口表，且含：界面 / 需规 / 中文名 / 入参必填·选填 / 期望出参  
- [ ] 未写成数据集成或库表移交  
- [ ] 未伪称联调通过 / 未擅自改契约  

---

## 修订

| 日期 | 说明 |
|---|---|
| 2026-11-11 | 首版：两叶合册；监管人淮政玮 |
| 2026-11-11 | 叶 2 改主目标：聚合服务调用科学数据中心接口需求（界面/需规/中文名/入参/出参）；仅接口不数据集成 |
