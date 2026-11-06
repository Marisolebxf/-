# SYNTH-CHAINFIX-FE-L01 Handoff — 跨层链路修复第③站（FE 段）

- **任务**：SYNTH-CHAINFIX-FE-L01（跨层链路修复③：FE 段，最后一站；消费①PY/②JAVA 冻结契约）
- **执行**：agent:frontend（claimed_by=agent:frontend-agent，supervised_by=human:徐滕强）
- **仓**：`lumen-ui-topic`（origin/dev，**已 commit 未 push**：`9c4694d` + 补丁 `4397e0c`，等 coordinator 统一推）
- **强度**：ponytail: full（最短 diff；零新依赖；复用既有 defineApi/Arco/结果源样板）
- **契约输入**：`SYNTH-CHAINFIX-JAVA-L01.md` §2 FE 对齐清单（②站）+ `SYNTH-CHAINFIX-PY-L01.md` §2 契约签名清单（①站）
- **日期**：2026-11-06

## 1. 范围与实现（逐项修法）

### F1（P1-1）weight_profile 贯通 FE 段 ✅
| 改动点 | 文件 | 修法 |
|---|---|---|
| 查询类型 | `src/api/topic/synthBatch.ts` | 新增 `WeightProfile`（INDEX_MAIN/WEIGHT_MAIN/EQUAL 三枚举）+ `SynthVitalityBatchQuery`（`weight_profile?`，仅活力）；`VitalityBatchSnapshotResp` 外壳补 `weight_profile`/`cache_key`/`calc_batch_id` 回显（PY §2.3） |
| 四段指纹 | `src/composables/useSynthCtx.ts` | `SynthContext.weightProfile?` + 默认 `INDEX_MAIN` + URL/storage/query 全链（`weight_profile` query 键）+ 新 `synthVitalityFingerprint()`（三段+档；缺省档不占段，对齐 Java 归一口径）；三段 `synthCtxFingerprint` 原样保留供要素/协同叶 |
| 任务桥透传 | `src/composables/useSynthTaskBridge.ts` | `startOrResumeSynthAnalysis` 活力叶：指纹用四段、create `params/draft` 带 `weight_profile`；`ctxQuery` 活力路径带 `weight_profile`（结果/报告页回跳同档）；`resolveSynthWorkbenchRestore` 同指纹口径 |
| 工作台 UI | `RegionalInnovationVitality.vue` | 条件栏 actions 增权重档 a-select 三档（缺省 INDEX_MAIN；切换走 `patchCtx` = 切条件清任务态进 config，与既有切条件语义一致）；快照标识行含回显档（`快照档 {profile} · 批次 · cache_key`，cache_key 第四段=档）；404/400/502 空态分文案（F4） |
| 回显禁自标 | `vitalityResultSource.ts` + 工作台 | `resolveVitalityInstantResult` 返回 `{result, echo, errorText}`；echo.weightProfile = **响应外壳 `weight_profile` || result 内 `weight_profile`**（PY 行内回读为权威，禁前端自标）；`displayedProfile` instant 沿用 echo、task 沿用结果内档 |
| 报告页 | `VitalityReportPage.vue` | subject 段补「权重档：{响应内档}（回显=实际计算档）」 |

### F2（P1-5）全景 snapshotId 透传 ✅
| 改动点 | 文件 | 修法 |
|---|---|---|
| props+重拉 | `ElementPanoramaPanel.vue` | props 增 `snapshotId?`；`pullFiltered` 带 `snapshotId: props.snapshotId \|\| undefined`（筛选锁定当前快照，显式批可回溯）；watch 源 `[props.ctx, props.snapshotId]`——**快照切换重置 remotePanorama/remoteReason**（防 A/B 批筛选残留） |
| 挂点 | `ElementsWorkbenchView.vue` | `:snapshot-id="result.snapshotId"`（result 源已有字段） |

### F3（P1-6）DTO 可空化 + 诚实渲染 ✅
| 改动点 | 文件 | 修法 |
|---|---|---|
| 类型可空 | `vitalityMock.ts` | `vitalityIndex/deltaVsCompare/yoy → number\|null`；`DimScore.score/weight → number\|null`（键在值可空）；`trend[].index/strengths/weaknesses score → number\|null`；`weight_profile?` 回显字段 |
| normalize 内层 | `vitalityResultSource.ts` | dimScores 元素校验 `'dim' in dim && 'score' in dim && 'weight' in dim`（允许 null 但键必须在；键缺失=伪数据整包拒收） |
| 渲染容忍 | `RegionalInnovationVitality.vue` | 三指定点全部 null→「—」：L393 区域 deltaVsCompare/yoy 缺行不硬拼 `+` 号；L247 维分文案 `score ?? '—'`/`weight!=null?xx%:'—'`；L419 指标权重列同款；weight 环图 filter null（缺行不进 chart data，同要素页既有做法） |
| 报告门控+判空 | `VitalityReportPage.vue` | instant 快照源 = **`USE_MOCK && hasSnapshot ? DEFAULT_BATCH_RESULT : null`**（real 无快照=空态引导，禁演示值出 PDF）；报告全量 toFixed/百分号前置判空（`fmt1/fmtPct` → null「—」）；deltaVsCompare/yoy 判空不出现「高 —3.2」 |
| mock 兜底闸 | `vitalityMock.ts` | `getVitalityBatchSnapshot` 头部 `if (!USE_MOCK) return null`（real 面 DEFAULT_BATCH_RESULT 只在 Mock 面出 PDF） |

### F4（P1-7）synthBatch 真语义 HTTP 分支 ✅
| 改动点 | 文件 | 修法 |
|---|---|---|
| 状态码读取 | `synthBatch.ts` | 新 `synthHttpErrorStatus()`（读 `err.status \|\| err.response?.status`——**AxiosError 本身带 status，按仓内 request 实际抛错形态适配；request.ts 未动**）+ `synthHttpErrorMsg()`（`err.response?.data?.msg`） |
| vitality | 同上 | **400 不再吞**（原 404-only 分支保留——400/502 原样上抛由结果源分类）；404 → `IntelBatchSnapshotNotFound`（进 no_batch 引导开始分析） |
| elements/collab batch | 同上 | 404/400 → no_batch（维持既有契约）；**502 不再吞**——原样上抛（协同 instant 侧 catch null、活力侧分类文案），不误报「无快照」 |
| graph | 同上 | 注释更新：空图=合法 200（reason 区分非错误）；400/404 → `graph_request_rejected` 空图（维持） |
| 分类文案 | `vitalityResultSource.ts` | 新 `vitalityHttpErrorText()`：502 →「快照服务暂不可用，请稍后重试」；400 按 errorCode 分文案（WEIGHT_PROFILE_INVALID/WINDOW_INVALID/REGION_*/Python 原文透传）；404 无文案走 no_batch |

### F5（P1-3）queue_full 误报修正 ✅
- `useSynthTaskBridge.ts`：`SynthStartDecision.queue_full` 增 `reason`；create catch 读 `err.response?.data?.msg`/`err.message`，`/not[_ ]?support|unsupported|不支持|ANALYSIS_TYPE/i` → `unsupported`（「该分析类型暂未支持」），否则 `queue_full`（「当前分析队列已满，请稍后重试」）；`applySynthStartDecision` 按分支出文案。

### F6（P1-4）industry 下拉传 code ✅
- `CollabWorkbenchView.vue`：`industryOptions` 改 `{label, value:code}` 结构（code=`row.industry ?? row.industry_label`——PY §2.1 industry 键=industry_code 值；label=`industryLabel ?? industry_label ?? code`，**节点无 code 时回退 label** 并注释）；a-option `:value="opt.value"` 显示 label；行业筛选值即 code 服务端精确匹配。`synthBatch.ts` graph 注释更新「后端已支持（PY §2.1），UI 本期不暴露」（entity_types/relation_types/limit 签名保留可用）。

### F7（P2-c）collab 门面接通 + isLatest ✅
- `synthBatch.ts`：`CollabBatchSnapshotResp` 外壳补九列回显类型（`isLatest?/region?/compare?/window?/batchMetaReason?`）；`SynthBatchQuery` 增可选 `snapshotId`（门面透传）。
- `CollabWorkbenchView.vue`：real instant 改直调 `fetchCollabBatchSnapshot`（+`snapshotId: task:{id}` 透传）；`latestFlag` ref 存 `resp.isLatest`（0/1/null）；快照标识行尾追加「 · 最新批 / · 历史批」（null 不显示）。

## 2. 自检结果（三绿）

| 自检 | 结果 |
|---|---|
| `pnpm type-check`（vue-tsc --build） | ✅ 0 error |
| element.selfcheck / collab.selfcheck / intelVit.selfcheck（含新契约断言） | ✅ 全绿 |
| intel.selfcheck / intelL1c.selfcheck / useSynthCtx.selfcheck（回归） | ✅ 全绿 |
| `pnpm build` | ✅ built in 31.29s（仅 chunk 体积 warning，与基线一致） |
| intelL1b.selfcheck | 🔴 存量红：`/view=\$\{processView\}&task_id=\$\{taskId\}/` 断言不匹配 `analysisTaskRoutes.ts` 现状——**git stash 干净基线复验同红**（该文件演进早于本单），按派单边界不算回归、未修 |
| 新契约断言（本单补齐） | vit：weight_profile 透传/三档枚举/回显禁自标/normalize 内层校验/400 分文案/502/报告 USE_MOCK 门控/toFixed 判空；element：F2 snapshotId 透传+切快照重置；collab：isLatest 透传/九列外壳/industry code 双值 |

## 3. 架构合规自检（铁律逐条）

| 铁律 | 合规 |
|---|---|
| ②调用链 前端→Java REST→Python | ✅ 全部经 `/topic/v1/synth/*` 门面；无越层直连 |
| ⑧数据策略 | ✅ USE_MOCK=false 零 fixture（报告页门控+mock 函数双闸） |
| ⑩D9 血缘 | ✅ 缺行 null 不补 0；ⓘ/角标 IntelMetricMount 全保留；回显档=实际计算档（禁伪闭合） |
| D8 前端规范 | ✅ Arco a-select 控件高沿用条件栏既有 token；无新色/字号 |
| D10 交互 | ✅ 下拉 aria-label、缺行「—」诚实态、切档=改条件进 config 需重新分析 |
| ⑫demo/lumen 隔离 | ✅ 未触碰任何 demo-* 引用 |
| 多会话保护 | ✅ commit 仅暂存本单 13 文件；工作区另有他会话 WIP（cms/*、policy/* 共 9 文件）未触碰 |
| 前端推送闸门 | ✅ commit 即止未 push（派单：coordinator 统一推） |

## 4. 偏离说明

1. **回显档展示挂 instant 快照标识行 + 报告页**，不再另设档切换徽标：工作台切档=改条件（进 config），无「档内切换」态可标；回应「结果渲染沿用响应内 weight_profile（禁自标）」以 `displayedProfile` 实现（instant=echo、task=result.weight_profile）。
2. **vitality 400/502 语义发生在 instant 路径**（默认三元组专属），错误文案经 `resultState.errorText` 在结果空态区展示；task 路径 #104/#105 失败维持既有诚实降级（超边界未扩）。
3. **三自检新增断言升级了两条旧正则**（element I5 watch 源含 snapshotId），属派单明示的「补新契约断言」范围。
4. **未修清单：无**（派单 F1–F7 七项全落地）。
5. 范围外移交：`intelL1b.selfcheck` 断言与 `analysisTaskRoutes.ts` 现状脱节（存量红，基线复验过），建议 coordinator 另派 chore 修断言；本仓 dev 有他会话 WIP 未入本 commit，push 前需注意隔离。

## 5. 产物清单

| 类型 | 产物 |
|---|---|
| commit | `9c4694d`（13 文件 +392/−91）+ `4397e0c`（label 样式补丁 +8；**均未 push**，等 coordinator 统一推） |
| 改文件（13） | `api/topic/synthBatch.ts`、`composables/useSynthCtx.ts`、`composables/useSynthTaskBridge.ts`、`mock/intel/vitalityMock.ts`、`views/intelligence/{RegionalInnovationVitality,VitalityReportPage,vitalityResultSource.ts}`、`views/intelligence/collaboration/{CollabWorkbenchView.vue,collab.selfcheck.mjs}`、`views/intelligence/elements/{ElementPanoramaPanel.vue,ElementsWorkbenchView.vue,element.selfcheck.mjs}`、`views/intelligence/intelVit.selfcheck.mjs` |

## 6. 验收证据

- §2 自检输出（type-check 0 error；六 selfcheck 全绿；build 31.29s 成功）。
- intelL1b 存量红 stash 基线复验（干净 dev 基线同红，排除本单引入）。
- CI：未 push，push 后由 GitLab CI 验证；K8s dev 行为变化 = 活力三档秒开/任务链四段指纹/全景筛选锁快照/协同门面 isLatest 展示（依赖②站 Java 已 commit 的 `f4b2ccb` 先行部署）。

## 7. cost（待 task-update-fields 回填）

| 字段 | 值 |
|---|---|
| actual_tokens | ≈150k（含读两站契约/现状代码/自检迭代） |
| model_used | glm-5.3-Flash |
| actual_cost | ≈$0.7（< $10 阈值，不触发复盘） |
| cost_warn | false |

## 8. 移交 coordinator 注意事项

1. **push 顺序**：①PY `4828c06` → ②JAVA `f4b2ccb` → ③FE `9c4694d`（FE 错误分支依赖 Java 新 HTTP 码上线；Java 未上时 FE 400/502 分支表现为既有 catch 兜底，不炸页）。
2. **本仓 dev 当前有他会话 WIP**（`cms/*` 8 文件 + `policy/*` 2 文件，未入本单 commit）——push 本单时严禁连带；建议由 WIP 所属会话自行收口。
3. 活力页切档/切条件均清任务态进 config（「开始分析」入口），附录 E E.3 禁自动 create 语义不变。
4. 协同任务链（②站 §2.5）任务中心标签「区域创新协同分析」已由 INTEL_ANALYSIS_LABEL 覆盖，FE 无需再改。
