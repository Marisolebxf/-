# DS10-QRY-FDE · 波次 A · product-agent 任务单

总单：`POL-L2-DS10-QRY-FDE-L01`。监管人 `human:淮政玮` 于 2026-11-10 确认执行计划后开工。  
本单只做波次 A 的产品设计。你是 product-agent，独立会话。不定档、不选读法、不改业务仓代码、不改 Storage、不改注册表、不 commit。

## 先读

- `agent-delivery/产品实现规程.md` §4.2（含 §4.2.0 / §4.2.3）
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` 中多维检索相关节（序号 **197 / 198 / 200**；总表与正文）
- 专题真源（只读对照，不改专题仓）：
  - `repos/lumen-ui-topic/src/views/policy/policySearchModel.ts`（`POLICY_QUERY_EXAMPLES` / `POLICY_KEYWORD_EXAMPLES` / 模式文案）
  - `repos/demo-ui-topic/src/app/pages/policy/PolicyTopicSearchPage.tsx`（示例分套、最近检索按 mode、热门进高级）
- 展示现状（只读）：`repos/lumen-ui-science-pc/src/views/policy/panorama/search/DisplayPolicySearchHub.vue`、`displayPolicySearchConfig.ts`

路径相对 `gkx-orchestration/`；业务仓在 `${GKX_ROOT}/repos/`。

## 监管人已锁定的意图（不要改、不要扩）

- 改哪一叶：展示系统 · 科创政策全景 · 多维检索蓝色检索中枢（197 一带；展示页 `policy/panorama` 检索 Tab）
- 改成什么样：
  1. Tab 文案**跟招标**：保持「智能检索 / 关键词搜索 / 高级检索功能」（不改成专题「查政策 / 高级筛选」）
  2. 示例查询文案**直接搬专题**两套：`POLICY_QUERY_EXAMPLES` → 智能；`POLICY_KEYWORD_EXAMPLES` → 关键词；高级不挂第三套文案示例（进字段库态）
  3. 点示例**跟专题**：只填入输入框，不自动搜索
  4. 最近检索位置跟专题：挪到蓝色检索区下方；按当前 Tab（mode）分桶；**收藏仍留结果区**
  5. 热门 filter 类落地跟专题：进高级预填、待应用（不偷偷改成关键词检索）
- 为什么：展示与专题检索中枢交互一致，避免演示两套说法；招标 Tab 名保留

## 要改的范围

改说明书多维检索相关节（197/198/200 能挂上的功能点），满足规程 §4.2.3：

- 功能点编号建议挂在 197 下拆分（如 `197-hub-1`…）或与现有 197/198/200 分句对齐；每点写「界面上必须看见什么」，能被截图验证
- 状态清单至少覆盖：未输入、点示例后未点搜索、智能解析未命中、最近检索空、高级模式（蓝色快捷区收起/让位）、热门进高级未点应用
- 影响清单：哪份二级四单（至少 `POL-L2-DS10-QRY-ARCH`）、合规演示用例、前端 leaf（`POL-L2-DS10-QRY-FE-DISP-L01` / 本 FDE 实现段）还是旧口径；旧处标「已被说明书 2026-11-10 取代」
- 文末变更记录追加一行白话
- 另写一页短线框或区块说明（可放 `sdd/l2/会签/DS10-QRY-FDE-蓝色区-线框.md`）：蓝色区三 Tab、示例行、热门行、最近检索行的相对位置；不画架构时序、不写接口字段、不写建表

## 回复（压成 8 行以内）

改了说明书哪一节；功能点几个；示例/最近检索/点示例/热门各怎么写的；影响清单几条；待裁定是否为零。
