# tasks · TS-INDDISC-01（v2，按算法中台实查修订）

> 依赖 `spec.md` 的 D1–D4 批准。P0 → P1 → P2 串行；未过门不开工。

## 门禁

- [x] **G0 决策批准**：D1 产业领域=CL/INB（放弃 D-*）、D2 双下拉并存、D3 要素范围、D4 是否改后端、D5 路径 A、D6 点文字即选中、D7 时间范围实测（2026-11-01 用户已裁定）。
- [x] **G1 数据复核**：只读确认 ① `demo_gkxlumenx_dim.subfield_topic_map` = **390 行**（registry 390/130 一致）② 逐集群覆盖度见 spec §1.5.1 ③ 人才表 `subfield_ids` 存在但未接入查询路径（本轮不做）。

## P0 · 产业领域换成中台目录

- [x] **T0b** 时间范围联动补漏：`overview` 的 `enterpriseDomainDist(null)` 改传 `scope.endYear()`（领域分布随区间变化）。
- [x] **T1** `RemoteInnovClient` 新增 `industryClusters()`（`GET /v1/meta/industry-clusters?include_l0=true`）。
- [x] **T2** `SituationController` 新增 `POST /v1/situation/industry-domains`，透传集群+产业；`/fields` javadoc 与措辞改「技术领域（D-*）」。
- [x] **T3** 前端 `fetchSituationIndustryDomains`（`defineApi` 双轨）。
- [x] **T4** `SituationFilterBar.vue`：原「学科领域」块换「产业领域」级联（复用 `IndustrySelect`）；新增「技术领域」块仅事件 Tab 显示。
- [x] **T5** `index.vue` + `stores/situation.ts`：拆 `fieldValues`（产业 CL/INB）/ `techFieldValues`（技术 D-*）两组状态，禁止同一字段双关两套编码。
- [x] **T6** 未映射集群（`mapStatus !== 'mapped'`）不发下游请求，显示「该集群尚未映射产业，暂无关联子学科」。
- [x] **T7** 验证：`npx vue-tsc --build` 通过 + `npm run build` 通过；页面实测级联 15 个集群、未映射集群带「（未映射产业）」标识。

## P1 · 子学科反查 + 要素过滤

- [x] **T8** gkxlumen-innov（`lumen-svc-platform`）新增只读 `GET /v1/meta/industry-clusters/industry-subfields?cluster_id=&industry_id=`（读已落库表，不在查询路径上同步/关联）。
- [x] **T9** display 新增 `POST /v1/situation/subfields`（`@NoToken` + 下游 `@Inner` 配对）；无命中返回空 + `emptyReason`。
- [x] **T10** 前端 `fetchSituationSubfields` + 二级「学科领域（细化）」下拉，仅产业领域已选且 `mapped` 时可用。
- [ ] **T11**（D3/D4 批准）element 侧按 `subfieldIds` 过滤带子学科的要素；其余要素标 `field_filter_supported=false` 并置灰。
  - ⛔ **2026-11-01 复核后判定阻塞**：element 无领域/子学科列，且 `产业→node→企业` JOIN 在现网数据不通（`node_id` 98% 空、`INB1303`↔`INB170101` 两套码）。本任务仅在用户确认「路径 B」且数据侧补齐干道后开工；否则本轮降级为「UI 明示未生效」（T18）。

## P2 · 事件侧正名与诚实提示

- [x] **T12** 事件下拉文案「技术领域」，标注「产业/学科领域暂不适用于事件」（`SituationFilterBar` 标签「技术领域」+ 占位「请选择技术领域（仅作用于科创事件）」）。
- [x] **T13** 事件 0 条区分三种情况：技术领域真实条数为 0 →「该技术领域无事件数据（数据现状，不是筛选失效）」；条数 > 0 但当期无记录 →「该技术领域在当前时间范围内暂无事件记录」；`/events` 未上线（404/405/501）→ 追加「事件明细接口尚未上线」。实测 `/events` 本机为 200 + 11 条真实事件，故按运行时判别，不写死「未上线」。

## P3 · 二次复核后新增（2026-11-01）

- [x] **T17** 产业领域级联可用性修复：`IndustrySelect.vue` 增 `#option` 插槽，叶子文字点击转发给同行复选框（集群文字仍展开）；type-check 通过 + 浏览器实测「点集成电路文字→出标签→发 /subfields→再点取消」通过。
- [x] **T18** 诚实提示（路径 A）：`index.vue` 增 `industryScopeHintVisible` + `a-alert`，未选时零 DOM，选中后文案说明「产业/学科无下游消费方，指标数字不变」；实测出现/消失/零泄漏均通过。
- [x] **T19** 校验时间范围（T0b）：定位为「后端收到区间但没用（b 类）」——久新 KPI/年度序列此前不带年份。已修 `map`/`overview` 传 `year` 与 `year_from/year_to`，并给论文/专利/人才补统计年标签。实测 2021 区间 vs 2016-2026：企业 13,300↔102,167、论文 306,284↔858,620、专利 131,483↔71,043、人才 110,178↔159,546、项目 505,124↔392,032、机构 38,433↔48,444，标签带「（2021年）/（2025年）」。

## 收尾

- [x] **T14** 三绿复跑：`npx vue-tsc --build` exit 0、`npm run build` exit 0、浏览器实测（级联/子学科/诚实提示/事件空态文案）通过。
- [x] **T15** 交接结论已写入 `spec.md` §8（不另建文件）。
- [x] **T16** 改动停本地：`lumen-ui-science-pc` 与 `lumen-svc-platform` 均未 commit / 未 push，等 `human:李伟` 走查。

## P4 · v3 单下拉 + 后台分流（2026-11-02 用户裁定，实施见 spec §9）

> 门禁：G2 待批准（D2/D5 推翻重裁、D3/D4 更新、D8 新增）。**T11 作废**——v3 企业侧不走 subfieldIds/JOIN，改走 `chain_code` 产业码过滤（spec §9.2）。

- [x] **T20** python `geo_indicator.factor_metrics` 增 `subfield_ids`：四要素改查 `ads_geo_yearly_discipline_metrics`；topic/result 分别经 `ads_research_problem_discipline` / `ads_research_outcome_discipline→ads_discipline_topic`；不传参行为不变。
- [x] **T21** python `monitor_indicator.overview_kpi` + `yearly_trend` 增 `subfield_ids`：paper 经 `primary_topic_id→ads_discipline_topic`；talent/project/institution 走 discipline_metrics COUNTRY 级 SUM；专利/项目经费返 null+note；不传参行为不变。
- [x] **T22** 重启 `:8082` 并 curl 三端点：过滤生效（2024 深圳 paper 17596→178 / talent 4922→128 / project 13501→147 / topic 11→2，均 >0；KPI paper 858620→7924、talent 159546→8303；专利/项目经费 null+note；trend 17 年过滤序列与 factor-metrics 数值对齐）；institution/result 的 null 经库内直查佐证为数据真空；不传参三端点回归一致。验证用 sub_* 取久新直采有数样本（中台 subfield_topic_map 当前反查全空，见 §风险）。
- [x] **T23** element `EnterpriseController.appendScope` 增 `industryIds`（`chain_code` 精确 + `LIKE 前缀%` 子查询）；overview/regions/districts/points/trend/influence/cluster 七端点透传；display `RemoteElementClient` 同步。
- [x] **T24** display `SituationController`：Scope 增 `industryIds`/`clusterId`；新增 `resolveSubfieldIds`；`kpiBodyOf`/`yearlyTrendBodyOf`/geoFactorMetrics body 加 `subfield_ids`；element 调用点全传 `industryId`；仅选集群时展开 mapped L0 产业，pending_vendor 集群返空+标注；`scopeLabelOf` 补生效文案。
- [x] **T25** `mvn -o -pl gkxlumen-element,gkxlumen-display -am install -DskipTests` 通过（JDK17）；重启 `:7082/:7099`；curl `/v1/situation/map`+`/overview`（`selectedFieldValues:["CL-SEI-01","INB1303"]`）对比不选产业。⚠️ 验收结论分两半：**链路行为全部正确**——scopeLabel/notes 如实标注「子学科无映射…产业筛选未作用于久新要素」、不选产业时 notes 干净、整集群分支标注「产业集群目录不可用」、错误码 INB9999ZZZ 不触发错误过滤；**数值对比未能实测**——MySQL `10.50.11.76:3306` 当前不可达（element 全空）且 subfield_topic_map 反查全空（久新未过滤），两项环境数据问题与代码无关，待环境恢复后由 human:李伟 走查时复测数值断言。
- [x] **T26** 前端：`SituationFilterBar.vue` 隐藏「学科领域（细化）」下拉（industryPendingHint 挪到产业块）；`index.vue` watch 保留、alert 改生效说明文案；顺带修根因 `industryOptions.length ? industryOptions : undefined`（空数组曾阻塞 IndustrySelect 内置 CLUSTER_SEED 兜底致下拉「暂无数据」）；`npx vue-tsc --build` + `npm run build` 双绿；浏览器 `:3000` 实测三项 PASS（级联 15 集群可见可勾、勾选后提示条出现、DOM 无「学科领域」label）；数字变化受环境阻（MySQL 10.50.11.76 不可达 + subfield_topic_map 反查全空），待走查复测。
- [x] **T27** spec §2/§3 已同步 v3；checklist.md 补 v3 清单；全部改动停本地等 `human:李伟` 走查。
