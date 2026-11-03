# checklist · TS-INDDISC-01

> 复核时间 2026-11-02（含 2026-11-01 二次复核）。验证方式：源码核对 + 运行实例实测（display :7099 / innov :7090 / 前端 :3000）+ MySQL 直查。

## 后端（display BFF）

- [x] `RemoteInnovClient` 存在 `industryClusters()`，`@NoToken` + `GET /v1/meta/industry-clusters`（L119-L122）
- [x] `SituationController` 存在 `POST /v1/situation/industry-domains`，返回 `clusters[]`（含 `clusterId / name / group / mapStatus / l0[]`）（L651-L654）
- [x] `POST /v1/situation/industry-domains` 取不到数据时返回空数组 + `note`，不编造集群
- [x] `/fields` 的 javadoc 与空态 `note` 措辞改为「技术领域（D-*）」，不再自称「学科领域 / 产业领域字典」（L796）
- [x] `overview` 的企业领域分布调用带上 `statYear`（不再传 `null`）（L524 `enterpriseDomainDist(scope.endYear())`）
- [x] `overview` / `map` 的久新 KPI 传 `year`、年度序列传 `year_from/year_to`；论文/专利/人才补「（xx年）」标签（实测 2021 与 2016-2026 两组数字均不同）

## 后端（gkxlumen-innov 反查）

- [x] 存在只读端点 `GET /v1/meta/industry-clusters/industry-subfields?cluster_id=&industry_id=`（`lumen-svc-platform/gkxlumen-innov`，即页面实际调用的 `:7090`）
- [x] 该端点标 `@Inner(value=false)`（`IndustryClusterController.java` L45-L54）
- [x] 该端点只读已落库表，不在查询路径上触发 sync / link（`IndustryClusterService.subfieldsForIndustry` 只做 SELECT）
- [x] 无命中返回空数组 + `mapped=false`，不回落全量（6 个 `pending_vendor` 集群实测 `emptyReason` 如实返回）

## 后端（display 子学科）

- [x] `RemoteInnovClient.subfieldByIndustry(...)` 已添加且 `@NoToken`（L125-L128）
- [x] `SituationController` 存在 `POST /v1/situation/subfields`，返回 `subfieldIds / items / mapped / source`（L721-L735）
- [x] 无命中返回空 + `emptyReason`，不回落全量（实测 CL-SEI-01+INB1303 返回 7 条；pending 集群返回空 + 原因）

## 前端

- [x] `fetchSituationIndustryDomains` / `fetchSituationSubfields` 已添加，风格与 `fetchSituationFields` 一致
- [x] 筛选栏「学科领域」（D-*）不再出现；改为「产业领域」级联（集群 → 产业），选项来自 `/industry-domains`
- [x] 未映射集群（`mapStatus !== 'mapped'`）在选项上肉眼可辨（「（未映射产业）」）
- [x] 选中未映射集群时显示「该集群尚未映射产业，暂无关联子学科」，且不把该集群下发到要素请求（`effectiveIndustryFieldValues` 置空）
- [x] 「技术领域」块仅在科创事件 Tab（`showEventTypeFilter`）显示，取 `D-*` 选项，占位文案「请选择技术领域（仅作用于科创事件）」
- [x] 二级「学科领域（细化）」仅在已选产业且集群 `mapped` 时可用，来源 `/subfields`
- [x] 要素请求的 `selectedFieldValues` 用产业编码；事件请求的 `selectedFieldValues` 用 `D-*`
- [x] 两套编码不被同一个字段混用（`store.fieldValues`=产业，`store.techFieldValues`=技术）
- [x] 事件 0 条已区分「该技术领域无事件数据（数据现状）」/「该领域当期暂无事件记录」/「事件明细接口尚未上线」
- [x] 产业领域级联支持「点叶子文字即选中」（`IndustrySelect` `#option` 插槽转发到复选框；集群文字仍展开）
- [x] 已选产业/学科时显示一次性诚实提示：两套领域仅用于关联清单，久新要素与科创事件数据源无该维度，指标数字不随之变化；未选时零 DOM

## 数据侧边界（本轮不承诺，已实测记录）

- [x] element 侧**未**按 `subfieldIds` 过滤：`gkxlumen-element` 无领域/子学科列，`企业→产业` JOIN 在现网数据不通（`enterprise_industry_chain.node_id` 空 378,290/388,824；`INB1303`↔`INB170101` 两套码）→ 按 D5 走「诚实提示」而非伪造筛选
- [x] 未新增任何伪造的 D-* ↔ CL/INB/subfield 映射

## 工程门

- [x] `npx vue-tsc --build` 通过（exit 0）
- [x] `npm run build` 通过（exit 0）
- [x] 浏览器实测：级联 15 个集群可见、未映射集群可辨；选 CL-SEI-01/INB1303 能拿到 7 条子学科并发出 `/subfields`
- [x] 改动全部停本地，未 commit / 未 push

---

## v3 清单（2026-11-02 用户裁定：学科挂载产业、前端单下拉、后台分流）

> 上方 v2 清单中「学科领域（细化）下拉」「产业/学科仅用于关联清单的诚实提示」两条已被 v3 推翻作废，以本节为准。

### 后端 · python gkx_show_service（T20-T22）

- [x] `geo_indicator.factor_metrics` 增 `subfield_ids`：四要素改查 `ads_geo_yearly_discipline_metrics`；topic 经 `ads_research_problem_discipline`（OpenAlex 码桥接）、result 经 `outcome_discipline→ads_discipline_topic`；不传参行为不变
- [x] `monitor_indicator.overview_kpi`：paper 经 `primary_topic_id→ads_discipline_topic`、talent 走 discipline_metrics COUNTRY 级 SUM；专利/项目经费返 null+note「无学科维度，不参与产业过滤」
- [x] `monitor_indicator.yearly_trend`：有 `subfield_ids` 改查 discipline_metrics JOIN ads_location；caveat 补过滤说明
- [x] curl 实测过滤生效：2024 深圳 paper 17596→178 / talent 4922→128 / project 13501→147 / topic 11→2（均 >0）；KPI paper 858620→7924、talent 159546→8303；trend 17 年过滤序列与 factor-metrics 对齐；institution/result null 经库内直查佐证为数据真空；不传参三端点回归一致

### 后端 · element / display（T23-T25）

- [x] `EnterpriseController.appendScope` 增 `industryIds`：`chain_code` 精确 + `LIKE 前缀%`（每码 OR 组、args 两次、片段尾空格保留）；七端点透传；入参清洗（去重/上限 50/超 32 字符丢弃）
- [x] `RemoteElementClient` 7 方法签名同步加 `industryId`；`mvn install` 通过（JDK17）
- [x] display `Scope` 增 `industryIds`/`clusterId`/`industryNote`；`resolveSubfieldIds` 单请求一次反查 + 降级标注；三处久新 body 条件加 `subfield_ids`；element 调用点全传 industryId；`scopeLabelOf` 生效文案
- [x] 链路行为实测：`/map`+`/overview` 选 INB1303 时 scopeLabel/notes 如实标注、错误码不误过滤、不选产业回归一致、整集群分支标注「目录不可用」
- [ ] ⚠️ 数值对比**待环境恢复后复测**：MySQL `10.50.11.76:3306` 不可达（element 全空）+ `subfield_topic_map` 经 innov 反查全空（久新未过滤）——两项均为环境数据问题与代码无关，走查时断言「企业数显著变小、论文/人才变小且非 0、专利 null+note」

### 前端（T26）

- [x] 筛选栏只留「产业领域」级联；「学科领域（细化）」下拉从模板移除（内部 props/emit/watch 保留，便于回滚）；DOM 无「学科领域」label
- [x] alert 改为生效说明：「产业领域已生效：企业按产业链匹配；论文/人才/项目/机构/课题/成果按关联子学科过滤；专利与项目经费无学科维度不参与」
- [x] 修复 `industryOptions` 空数组阻塞 IndustrySelect 内置 CLUSTER_SEED 兜底的根因（传 `undefined`）；`vue-tsc` + `build` 双绿；浏览器实测三 PASS

### 工程门（v3）

- [x] python `py_compile` 通过；`mvn -o -pl gkxlumen-element,gkxlumen-display -am install -DskipTests` 通过；`npx vue-tsc --build` + `npm run build` 双绿
- [x] 全部改动停本地，未 commit / 未 push，等 human:李伟 走查
