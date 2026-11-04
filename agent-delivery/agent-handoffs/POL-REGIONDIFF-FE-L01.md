# Handoff — POL-REGIONDIFF-FE-L01

> 需求：区域政策差异性分析（FE-POL-01B · Bid §4.2.1.3.2）前端接线：开始分析 + Job 轮询 + 真实矩阵渲染
> 强度：ponytail full
> 认领：`agent:frontend-agent` / 监管：`human:淮政玮` / `claim_type: pull`
> ⚠️ **人工验收闸门（AGENTS.md 2026-10-20 裁定）：改动停在本地工作区，等监管人走查通过后再推，本 handoff 先行提交**

## 范围与实现

| 文件 | 改动 |
|---|---|
| `src/views/policy/panorama/components/RegionalDifferencePanel.vue` | I2-12/附录 E 接线（详见下） |
| `src/views/policy/panorama/sentimentLive.ts` | `PanoramaJobSubType` 联合类型扩 `policy_region_diff`；新增 `regionDiffJobBodyOf`（regions 进 `params`，display 白名单只转发 params/draft）与 `mapRegionDiff`（rows/points 双块映射）；复用键类型同步 |
| `src/views/policy/panorama/FE-POL-SENT-LIVE.test.mjs` | 补面板锚点 + `mapRegionDiff`/`regionDiffJobBodyOf` 纯函数断言 |

### 面板行为（对照 `ImplementationTracker.vue` 既有范式，同款状态机）

- **USE_MOCK=false**：「开始分析」→ POST `/display/v1/policy/panorama/jobs` `{sub_type:'policy_region_diff', params:{regions}}` → 单飞（busy 禁重复提交）→ 轮询（首查 1.2s / 间隔 3s / 封顶 2 分钟）→ 终态渲染；「重新分析」force 重跑；同区域集合当天已成功 → `onMounted` GET 回读直接打开（`readReuse`/`writeReuse`，键=排序区域名逗号串）
- **切地区选择器不自动起任务**（无 watch，只改本地过滤集与下次任务条件）——I2-12 铁律
- **失败不清已返回结果**：矩阵与差异点原样保留，仅卡内红条（提交失败/任务失败/超时三分文案）
- **空态诚实**：无行显 `a-empty`，不造数据；`support` 缺失但 `support_index` 有值时显示力度指数
- **USE_MOCK=true**：现状不变（policySeed 静态种子 + MockBadge），demo 语义等价

## 验证证据（交付三绿 + 自检）

| 检查 | 结果 |
|---|---|
| `pnpm type-check`（vue-tsc --build） | ✅ exit 0 |
| `pnpm build` | ✅ built in 1m22s |
| `FE-POL-SENT-LIVE.test.mjs`（含新增断言） | ✅ 全绿 |
| panorama 域全部 5 个 `.test.mjs` | ✅ 全 PASS |
| `pnpm lint:eslint` | 🟡 未跑（本仓改动文件无新增 console/类型豁免；如走查要求补跑） |

## 附录 D 防漏扫描摘要

- D.1 页面差集：本叶只动 `panorama/components/RegionalDifferencePanel.vue` 单组件；无新页、无路由变化
- D.2 本地 KPI 接线：本面板无统计数字（矩阵文本表），不涉及 metric ⓘ；MockBadge 保留
- D.3 镜像 vs 矩阵：区域差异指标无独立 metric_id（结果板口径 `region_diff_v1`，Python 侧已标注 QPOL-02）
- D.4 错挂/正名：不涉及
- D.5 契约防漏：`regionDiffJobBodyOf` 断言锁死 `{sub_type, params:{regions}}` 形状；`mapRegionDiff` 空/坏载荷断言诚实空
- P0/P1 遗漏：无

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 FE→Java REST→Python | ✅ 只打 `/display/v1/policy/panorama/jobs`（测试红线断言禁 `/topicAsync` `/internal` `/policy/topic`） |
| D9 | ✅ 行级 `is_mock` 透传 + MockBadge 不撤（底座是 mock 种子，D4 仍 mock，不伪闭合） |
| D10/I2-12 | ✅ 显式「开始分析」、单飞、当天复用、force 重跑、失败保留旧结果 |
| D12 | ✅ 无 demo 服务依赖 |

## 开放项

- 待监管人本地走查（use_mock 双态切换目检）；走查修正同样停本地等确认
- Java 叶（POL-REGIONDIFF-API-L01）CI `backend:build` 绿后，真实链路端到端联调才可用

## cost

- `actual_tokens`: ~150k
- `model_used`: glm-5.3-flash
- `actual_cost`: ~$0.15
- `cost_warn`: false
