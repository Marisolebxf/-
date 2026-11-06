# POLICY-CMS-UX-20261106 · 政策 CMS 列表与编辑体验修复

日期：2026-11-06。用户确认提交并推送政策新闻内容管理相关本地修复，包含地理默认值、更新时间、倒序、Top10 提示和名次列。

## 规则与范围

- claimed_by：agent:frontend-agent / agent:api-agent，按仓职责标记。用户本会话明确授权 push。
- supervised_by：未提供团队实名，不推断代填。
- ponytail: full。复用现有 RegionSelect、Arco Table、CMS 错误处理、schema/list 机制，无新增依赖。
- 遵循主仓路径真源、团队公约、并行保护、前端/API 规则及完工即推要求。
- 用户提供的访问令牌未写入源码、日志、handoff 或提交。

## 需规依据

- 需规 335(2)：用户“可为政策手动标注”适用或发布区域，因此区域条目可选；有行时区域和关联说明必填。
- 需规 336(2)：政策力度榜单为“政策力度Top10”，包括上榜政策名称、评估依据、专家评述及推荐理由；名次是结构化字段，外层列表展示为本次按用户要求补充。

## 修复内容

1. 地理默认值：RegionSelect 空 model 时只显示“全国”占位，未回写表单值。现在地理行挂载且值为空时写入真实“全国”，默认值可直接通过校验；用户仍可继续选择省市区。
2. 草稿更新时间：原列表 `updatedAt` 只读 `publish_time`，草稿必然为空。Java envelope 现在对业务字段未占用 `updated_at` 的类型输出数据库审计更新时间；前端政策 CMS 优先读取 `updated_at`，缺失时回退 `publish_time`。
3. 列表顺序：政策 CMS 按更新时间倒序；无可用时间时按内容序列 ID 倒序，新建项优先。
4. 名次约束：政策力度榜 `rank_no` 限制 1–10（企业/服务榜分别 1–30）；正整数字段支持可选 max，提交前拦截超限值。
5. 业务错误提示：前端优先读取后端 `msg`，不再直接显示 Axios `Request failed with status code 400`；未知 400 显示“提交内容不符合要求，请检查后重试”。后端政策榜越界返回“政策力度榜名次须在 1–10 之间（榜单仅保留前10名）”。
6. 外层列表名次列：CmsTypeSchema 增加 `listColumns`，通用 CMS 表格支持动态业务列；政策力度榜在标题后展示“名次”，标题继续展示政策名称。
7. 政策统计区域：`regions` 移出新建必填集合，未传时落空数组，显式 `[]` 合法；有行时仍逐行校验区域路径和关联说明。

## 测试与验证

- 前端 `policyCmsGapFix.selfcheck.mjs`：通过，覆盖默认全国、Top10 max、名次列、错误提示优先级、列表倒序。
- 前端 `cmsOpsMap.selfcheck.mjs`：通过，覆盖 `updated_at` 优先、业务字段隔离和 `regions` 契约。
- 前端 `npm run type-check`：通过。
- 前端 `npm run build-only`：通过；仅保留既有 bundle 体积提示。
- Java 定向 `OpsContentServiceTest`：44 项通过。
- Java 完整 CMS 模块测试此前 109 项通过；本次后端改动在新基线隔离工作区重新编译并通过 44 项定向测试。
- 后端全量 `backend:build`：成功。

## 提交与流水线

- 前端提交：`42ab85daef83789398716ed474eb89168f5ada97`，消息 `[agent:frontend-agent] fix(POLICY-CMS-UX-20261106): ...`。
- 前端流水线：[4043](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-topic/-/pipelines/4043)，frontend:build/image、trivy、deploy:k8s 均成功。
- 后端提交：`cfe092ec20d453e388164a430e486b2ad81d73d7`，消息 `[agent:api-agent] fix(POLICY-CMS-UPDATED-AT-20261106): ...`。
- 后端流水线：[4050](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/4050)，基于包含本次提交的最新 dev `ba2f3feb`。
- 后端 pipeline 4050：backend:build 成功；backend:image:cms 成功；deploy:cms 成功（61.61s）；其他同批服务也完成部署。
- 后端自动流水线 4045 曾出现零 job；查明为当前远端 CI 中 `deploy:topic` needs 在普通 dev 规则下不存在 `backend:image:topic`。本次通过仓库已支持的 `TOPIC_RELEASE=true` 创建合法 pipeline 4050。该 CI 配置问题不由本次 CMS 提交引入。
- 总流水线状态保留 manual 是因为 `helm:chart`、诊断等人工 job，不代表 CMS 未部署。

## 架构与边界

- D8/D10：沿用 Arco、现有抽屉/表格和交互；未新增页面或组件体系。
- D9：未改指标口径、血缘或 mock 就绪度；`updated_at` 仅作为运营审计时间，不冒充业务统计。
- D12：保持前端 → lumen Java；无 demo 服务回落。
- 可观测：沿用现有 trace；未新增持久缓存。
- 未使用用户令牌执行现网写请求，未把敏感信息写入仓库。
- cost：环境未提供可核实 token/费用统计，未臆造注册表字段。
