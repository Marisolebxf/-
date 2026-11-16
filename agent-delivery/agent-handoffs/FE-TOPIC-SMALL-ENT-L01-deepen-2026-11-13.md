# FE-TOPIC-SMALL-ENT-L01 · 专题小屏企业维 — 深耕批 A-D（2026-11-13）

> 认领：human:孔东（认领 + 监管，2026-11-13 23:34 起，锁 24h）
> 范围来源：2026-11-13 会话差距清单（lumen-ui-topic vs lumen-ui-topic-mobile 企业分析模块对照）
> ponytail: full

## 范围与实现

对照 PC 仓 `lumen-ui-topic` 企业模块逐项盘点后按 Design-mobile §10 红线与规划 v2 裁剪，落地 4 批：

### 批 A · 企业详情明细 Tab（11 端点）
- 新建 `src/api/enterprise/profileDetail.ts`：news / finance / finance-latest / finance-trend / patent / patent-history / tags / competitiveness / bids / qualifications / shareholders（对照 PC 同名文件，经 gateway 同链路）
- `types/profile.ts` 补明细响应类型；`EntProfileRequest` 补 page/size
- `EnterpriseDetailView.vue` 3 Tab → 4 Tab（概况/专利/财务/产业链）：专利趋势折线 + van-list 分页专利列表、财务趋势图（panorama.financials 兜底）、股东信息、企业资讯、资质认定
- mock：`mocks/profileDetail.ts`（ENTERPRISE_LIST 样本派生）

### 批 B · 评估模板 CRUD（4 端点）
- `evaluation.ts` 补 create / update / archive / set-default（网关仅 GET/POST，update 走 POST 子路径——与 PC 一致）
- `EnterpriseEvaluationView.vue` 模板步骤加「存为我的模板 / 更新当前模板 / 管理」；底部弹层两枚（保存 + 管理列表：设默认/删除）
- mock：`evaluationTemplates.ts` 内存态 CRUD

### 批 C · 任务资产下载（修 424 + 补入口）
- 发现存量 `analysisTask.ts` 已有 #106 下载实现（FE-TOPIC-SMALL-CHAIN-GAP-L01）但 **fetch 不带鉴权头 → 真网关 424 token expired**
- 补 `assetRequestHeaders()`（systemCode/trace/Bearer，Mock 登录态不带 token——与 request.ts 同语义）
- `useMobileAsyncAnalysis` 暴露 `downloadAsset`；评估/招引/风险三视图结果态加「下载结果」（`v-if="!USE_MOCK"`，Mock 态禁直调——PC 同款约束）

### 批 D · 总览页统计缺口（2 端点）
- `stats.ts` 补 industry-distribution / district-heat；总览「概况」Tab 加产业分布 Top8 + 各区企业热力条
- `main.css` 补 `.heat-row` 全局样式

## 明确不做（红线/另排，均有出处）

| 项 | 依据 |
|---|---|
| 对比篮 14 API + store + 悬浮层 | Design-mobile §10 红线：对比篮仅 PC |
| 列表导出 | §10 红线：导出仅 PC |
| 风险 19 明细端点 | 小屏 panorama 聚合裁剪口径 |
| CMS / VIZ | 规划 v2 批 5（FE-TOPIC-SMALL-CMS-VIZ-L01）已排期 |
| SSE 流式进度 | 轮询可用；无产品要求 |
| 筛选模板/示例场景/搜索 meta 9 项 | 移动端简化交互，待产品要 |

## 防漏自检（新增断言）

`scripts/enterprise-remediation.test.mjs` 追加「深耕批 A-D 防漏自检」：13 端点 paths 断言、11 API id、11 mock 注册、5 处视图消费、批 B 4 API + 2 弹层、批 C 鉴权头 + 3 视图下载入口、批 D 2 端点 + 2 mock。

## 验收证据

- `pnpm type-check` exit 0
- `pnpm test` 49/49 pass（含新增防漏断言）
- `pnpm build` exit 0（20.55s）
- `pnpm lint` 6 errors —— **全部为存量**（干净工作区对照验证：`git stash` 后同样报错；涉及 request.ts / ent-tag-dict-cache.test.mjs / mocks.ts 未使用变量，均不在本次改动面）

## 架构合规自检

- ✅ 调用链：全部经 `gkxlumen-platform-gateway`（/api → enterprise/topic/v1），无越层、无直连 demo-*
- ✅ Mock 开关：新端点全走 defineApi + registerApiMock；USE_MOCK=false 零 fixture 渲染（防漏断言覆盖）
- ✅ D9：新增统计块均挂 StatCard/rank-row（后续 metric-id 按指标注册表补标）
- ✅ 设计：沿 `--sci-*` token、Vant + Arco 壳、触控热区 ≥44px；无新增依赖
- ✅ 多会话保护：未 commit 未 push（本机孔东规约：改动停工作区，待本人确认）

## 偏离说明

- registry 认领 commit（主仓 `9f5a0c7e5`）push 因 GitLab 403（凭证/权限）暂挂本地，待网络/凭证恢复补推；MCP 侧状态已生效（integration）
- 批 C 初版重复插入旧版下载块导致 TS 重复声明，已修复为「保留旧签名 + 补鉴权头」方案（调用方 ChainReportSheet 零改动）

## 开放项

1. lint 6 存量错误建议另开 chore 单清理
2. 详情页 metric-id 标注随 D9 指标注册表补齐（与 PC 对齐节奏）
