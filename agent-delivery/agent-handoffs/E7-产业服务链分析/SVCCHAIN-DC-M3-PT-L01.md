# Handoff — SVCCHAIN-DC-M3-PT-L01

- 日期：2026-11-07
- agent：doc-agent；监管人：human:徐滕强；强度：ponytail full
- 产物：
  - `agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-PT-合规演示用例.md`
  - `agent-delivery/工程过程/04-系统集成/03-专题系统集成/编排计划/SVC-PT-LOOP计划.md`
- 任务状态：M3d 产物完成，待 coordinator 推进（AV-0：handoff + evidence 就绪；状态留 in_progress 由 coordinator 按 AV 规则推进）
- 依赖消费：M1 `SVCCHAIN-需规条目矩阵.md` §2.4（11 行条目基准）+ M2 `SVC-数据调研-20261107.md`（库实值与缺口判据）+ as-built `qa/as-built/scripts/KJZTFWXT/service/{portal,portal-capability,portal-industry,portal-region,portal-shenzhen}/`（只读第二参照）+ `repos/demo-ui-topic/src/app/pages/service-portal/*`（只读，期望值真源）

## 1. 范围与实现（对照总控 §1/§4/§6）

- **覆盖表 11/11 行落齐**：97/98/99（33.1 全球概况三块）+ 100/101/102/103/104（33.5 深圳介绍五块）+ 33.2/33.3/33.4（3 无编号补充行，M1 矩阵 §3.1 既定口径）。8 列结构（需规位置/界面/输入或选择/触发/接口地址/按界面值填好的请求/期望输出/数据情况）对齐 POL-L2-DS10-QRY 金样。
- **查库节**：入口 `demo-gkxlumenx-ods`（M2 同款，认证受阻绕行先例沿用），跨库限定名查 `demo_gkxlumenx_ads`；实查门户统计面 5 张（`svc_metric_series` / `svc_metric_fact` / `svc_metric_dist` / `svc_global_dist` / `svc_region_dist`）+ 机构卡面 `svc_org_card`（city=深圳切片 × `service_type_candidate` / `org_size` 分布）+ `svc_chain_gap`。严格只读，零写操作，未探活。
- **期望值全部写具体值且可复算**：门户页面数字真源=前端编译期常量（`servicePortalData.ts`），故期望按页面常量值写；为避免「拍脑袋数」，用一次性离线脚本复刻前端缩放链路（`mockScopeShare`→`industryScaleRatio`/`szRatio`→`Math.round`；技术力=分析侧 `computeEvaluation` 固定五维等权复刻）逐值实算（`/tmp/svc-pt-calc.cjs`，一次性，未入任何仓）。库侧 ADS 实值（如类型全塌企业 43296/0/0、规模档 >500=19,030、深圳 fact=14,033、十区九区实值）在「数据情况」列如实对照，**两轨差异**（页面常量轨 vs 库 ADS 轨）逐行标注，LOOP 首轮核对项已入计划 §5。
- **主路径 6 步**：概况页（97/98/99）→ 产业分布（33.2）→ 区域分布切视图（33.3）→ 技术力榜（33.4）→ 深圳介绍（100–103）→ 重点机构抽屉（104）；只串可演行，条件不排列组合（统一 `industry=CL-SEI-01`，根集群 share=1）。
- **LOOP 计划全要素**（总控 §4）：常驻验收单建议 ID `SVC-PT-DEMO-ACCEPT-LOOP`（**只写不建**）、先决条件、token `~/.gkx/topic-loop-token` + `systemCode: topic`、一轮四步、缺口分类表（含本轮 7 条预判）、每轮≤3 张 `SVC-PT-DEMO-FIX-R{YYYYMMDD}-*`、同缺口两轮停、报告路径 `agent-handoffs/E7-产业服务链分析/SVC-PT-DEMO-ACCEPT-LOOP.md`（只追加）、状态行「覆盖已齐，未执行。等人说『按 LOOP 跑』」。

## 2. 11 行判定（含全球轴处置）

| 行 | 判定 | 要点 |
|---|---|---|
| 97 全球数量 | 可演 | KPI 10,310/621/10,310（ratio 0.115067 离线实算）；库侧 series 49 行未接线 |
| 98 全球类型 | 可演 | 三档环 6,731/2,152/1,427；库侧类型全塌企业（两轨差） |
| 99 全球规模 | 可演 | 四档 5,443/3,038/1,289/541；库侧已按 A 总则灌 5 档实值（两轨差） |
| 33.2 产业分布 | 可演 | 六环节卡 field-info 原值（研发 2,860 最厚）；领域×环节无源（Q-SVCCHAIN-08） |
| 33.3 区域分布 | 可演 | 全球 12 国 + 全国 12 省双视图常量值；库侧仅 5 国种子面板 + 3 省（两轨差，Q-SVCCHAIN-07） |
| 33.4 技术力 Top30 | 可演 | 在库 15 家诚实标注；榜首鹏城实验室 75.0（等权复用 CT-SVC-PT-03） |
| 100 深圳数量 | 可演 | szRatio 0.219885 → KPI 700/71；库侧深圳口径扎实（fact 14,033 + series 47 行） |
| 101 深圳类型 | 可演 | 三档 506/147/47；库侧同样全塌企业（两轨差） |
| 102 深圳领域×环节 | 可演 | 条形六档原值（share=1）；无库源计数表（Q-SVCCHAIN-08） |
| 103 深圳十区 | 可演 | 十区常量 ×szRatio；库侧九区实值排名序一致（大鹏 0 除外），旁证最强 |
| 104 重点机构 | 可演 | field-info 下 3 卡 75.0/73.6/66.2；抽屉四板块 `KEY_ORG_PROFILES` 演示档案；库侧 employees_number/operating_revenue 可对标未接线 |

**全球轴处置**：97/98/99 与 33.3 全球视图按 Q-SVCCHAIN-06/07 已拍口径判「可演」（演示态格子可显示 + UI ⚠ 提醒 + 不造国家真值）；期望值全部注明「演示口径」；库侧境外名录无源（`dwd_forg_base_info`=0）仅 150 行种子面板，在用例文末「全球轴处置声明」如实登记，未把种子面板值写成全球真实统计。

## 3. 偏离说明

1. **期望值口径选择**：任务书提示「直接把实查 COUNT/分布值写进期望」。实查后发现门户页面统计**不读库**（前端常量集），照抄库值会产出注定失败的期望。按金样精神（期望=页面真实会渲染的值）改为：期望=页面常量轨实算值 + 数据情况列并排库侧实查值，两轨差如实标注并入 LOOP 首轮核对项。此为体例级偏离，请监管人确认。
2. 产业筛选参数取根集群 `CL-SEI-01`（share=1，数值不被 `mockScopeShare` 权重比缩小），非任务书示例路径 INB1303；原因=根集群口径可整除复算、且与「无参数默认值」一致，便于 LOOP 精确核对。
3. as-built 历史实勘为诚实空 skip 波（2026-10-14/15），与现库已灌数状态不符；按铁律不改写历史文件，用例文头声明重判依据。
4. 104 行主路径产业从任务书暗示的 field-bio 改为统一的 field-info（CL-SEI-01）：11 行统一一条产业轴，主路径无切换；field-bio 六档全中的情形在 M1 矩阵已留痕，不丢失可演性。

## 4. 缺口引用清单（无新造编号）

Q-SVCCHAIN-01（技术力口径）、Q-SVCCHAIN-06（门户统计口径与数据源——97/98/99/100/101/103/104 主挂）、Q-SVCCHAIN-07（全球名录抽不出——33.3 主挂）、Q-SVCCHAIN-08（领域×环节无源——33.2/102 主挂）、Q-SVCCHAIN-09（产业筛选回落默认）、Q-SVC-004（十区直字段，已 🟢）、Q-SVC-010（深圳圈定准入）。未引用 GAP-SVC-*（该 5 枚均属分析侧 D1 missing 指标，PT 域不涉）。

## 5. 验收证据

- 覆盖表 11 行 × 8 列齐备；主路径 6 步全可演行；调度核对：可演 11 / 覆盖不到 0 / 设计无资源 0，与总控 §6「M3 完成定义」逐项满足（`可演` 行请求参数=界面输入真源值 + 实查数据引用；`覆盖不到` 0 行故无缺口编号缺失问题）。
- 库实值证据：查库节逐表行数 + 分布值（fact 43,296/14,033；dist 类型 3+3+5 行、scale 5 行；global_dist 5 行；region_dist province 6 行 + sz_district 18 行；chain_gap 6 行；org_card city=深圳 14,080 及类型/规模切片分布）。
- 前端真源证据：`servicePortalData.ts` / `servicePortalModel.ts` / 五个页面组件 / `resolveScope.ts` / `seed.ts` / `resolve.ts`（`mockScopeShare`）逐文件只读核对；期望值离线实算脚本输出存档于会话记录。
- 未建任何任务单（task-registry 零写入）；未跑 LOOP；未派修数单。

## 6. 架构合规自检

- D1/D9 指标口径：未改 registry seed；`M_SVC_PT_*` 只读消费；期望输出未引用未注册指标名 ✅
- D10 交互：本产物为文档，不涉交互实现；条件枚举均引 M1 矩阵锚点 ✅
- D12 demo/lumen 隔离：只在编排仓写文档；`demo-ui-topic` 只读，未改业务仓任何文件 ✅
- D14/D16/D18：未写任何库表；未建 gapfill；无 mock 接口直返表述（两轨差异按演示口径如实标注，未伪闭合） ✅
- 只读库：全部 SELECT / information_schema，零写、零探活 ✅
- 不造数：期望值=页面常量轨离线实算（可复算），库值=实查原值，无编造 ✅
- cicd: skip（纯编排仓文档） ✅

## 8. 评审修正记录

- **2026-11-07 Minor-2（深圳十区两处口径不一致）**：已核实并修复。根因（复查 `svc_region_dist` 实证）= sz_district 每区 2 行，`M_SVC_SZ_DISTRICT` 与 `M_SVC_PT_SZ_REGION_ORG` 两 metric_id 同值各登记一行；M2 §2.2 按整表 `SUM(org_count)` 求和把同值复用行加总（3,655×2=7,310 等），本用例按 `M_SVC_PT_SZ_REGION_ORG` 单行口径取值——属「单行 vs 含复用行求和」口径差，非批次不同、非去重口径差，不构成数据缺口。改动位置：`SVC-PT-合规演示用例.md` 查库节 `svc_region_dist` 条目补口径声明（含 LOOP 首轮禁止用跨 metric 求和值当期望）；103 行与其余行未动。未 commit/push。

## 7. cost

- estimated_tokens: ~90,000（含 15 次只读查库、前端 10 文件核对、离线实算与两文档产出；含 Minor-2 复查 1 次）
- model_used: glm-5.3-Flash
- actual_cost: ~$0.5（< $10 阈值，无需复盘）
- cost_warn: no

ponytail: full——复用 POL 金样体例与 M1/M2 既有产物、期望值离线一次算清不引入新抽象、as-built 历史零改动；唯一新增物为一次性核算脚本（不入仓，符合「一条可复算自检」要求）。
