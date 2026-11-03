# POL-L2-DS10-SENT-QA-L01 · 科创政策全景 · 政策舆情评估 · 合规验收测试报告

- 任务：`POL-L2-DS10-SENT-QA-L01`
- 日期：2026-11-04（00:50–01:15 执行）
- 监管：`human:淮政玮`
- 认领：`agent:qa-agent`（claim_type=coordinator_dispatch）
- 强度：ponytail full
- 测试对象：`POL-L2-DS10-SENT-FE-L01` 四卡接线（前端 `73cc1e8`+`e29090c`）+ `POL-L2-DS10-SENT-JOBQ-L01`（jobs 查询 `387502a`）+ `POL-L2-DS10-SENT-IMPL-JAVA`（读面 `6e7f7f4`）
- 环境：K8s dev 真连，`https://edu.itic-sci.com/tid/policy/tech-policy-panorama?tab=sentiment`（USE_MOCK=false），内置浏览器 CDP 驱动，UC 统一登录（机构=某某大学）
- 截图目录：`agent-handoffs/科技政策跟踪-POL/screenshots/SENT-QA-*.png`（8 张）

## 0. 执行环境与已知缺口（先读）

| 项 | 状态 | 说明 |
|---|---|---|
| 登录态 | ⚠️ 半登录 | UC SSO 登录成功（右上角「领导驾驶舱用户」）；但 localStorage 令牌经网关 `sso check-token failed`（401 访问令牌不存在）——组件 axios 请求带全部头仍 200（见 §3 各条），手工 fetch 直发被 401。**jobs 业务层在该态下返回「未获取到当前用户」**，与 FE handoff §2.4「匿名时后端拒，前端原样展示不伪造用户」的预期路径一致 |
| **element 缺库凭证（环境缺陷，父会话已确认）** | ❌ | K8s 里 `gkxlumen-element` 连 `gkxlumenx_gapfill` 库被拒：`Access denied for user 'gkxlumenx'@10.50.179.112' (using NO)`——**接口 200 + 空列表的根因是缺库凭证，不是表空**。Loki 持续打「gapfill 读表失败，返回空列表」。trace 证据：`3079b126`（assessment-report）/ `9c4a5ca8`（feedback），Tempo lumen 平面 00:39:11 display→element 全 200 但 JDBC span STATUS_CODE_ERROR |
| 数据准备核对 | ❌ 未达预期 | 按 DoD 预期：反馈 6 行三渠道、报告 2 行。当前 dev 环境两接口均返回空列表（根因=上述缺库凭证）。**灌数侧（MOCK-210/211）已验证写入成功**（handoff 记录 SELECT 6 行/2 行），数据在库里，是 K8s 读不到 |

**合规判定口径（父会话指示）**：F1/R1 写双维度——「接口诚实返回空、未造数（PASS 维度）；数据链路断（FAIL 维度，根因=element 缺库凭证）」。该缺陷已登记由父会话派单修复，本报告记入缺口章节。

## 1. 用例执行结果总览

| 组 | 用例 | 覆盖 DoD | 结论 |
|---|---|---|---|
| F1 | 受众反馈 · 三渠道空态 | 210 同步读 + 空态不造数 | ✅ PASS（诚实维度）/ ❌ FAIL（数据维度，环境） |
| R1 | 评估报告 · 空态 | 211 同步读 + 空态不造数 | ✅ PASS（诚实维度）/ ❌ FAIL（数据维度，环境） |
| S1 | 关键词检索 | 207 search | ✅ PASS |
| S2 | 空结果不回退种子 | DoD-2 核心 | ✅ PASS |
| S3 | 详情抽屉 | 207 detail | ✅ PASS |
| J1 | 效果任务受理+失败不清同步块 | 209 jobs + I2-12 | ✅ PASS（诚实失败路径） |
| J2 | 匹配任务受理+如实提示 | 212 jobs + 匿名 | ✅ PASS（诚实失败路径） |
| J3 | 切条件不自动起任务 | I2-12 | ✅ PASS |
| G1 | 裸别名拒绝（effect/match/policy:effect） | jobs 白名单 | ✅ PASS |
| G2 | 老 sub_type 不泄漏（policy_focus） | 白名单回归 | ✅ PASS |
| G3 | 越层路径不出现 | D12 | ✅ PASS |
| I2-12 附验 | 单飞按钮禁用 / 复用键不写 | I2-12 | ✅ PASS |

**未执行项（如实记录）**：
- J 组「任务成功终态渲染 + 当天复用 + force 重跑」——当前环境用户身份不生效（sso check-token failed），任务到不了成功态。留给 element 凭证与 SSO 会话修复后复验。
- F1 详情弹窗真实行字段（渠道/反馈人/评分）——空列表下无行可点，同上留复验。

## 2. F 组 + R 组 · 同步读面（210/211）

### F1 政策受众反馈收集

| 项 | 内容 |
|---|---|
| 前置 | 登录页签，USE_MOCK=false |
| 步骤 | 挂载舆情评估页签 → 组件自动 GET feedback → 依次切「问卷调查/在线评价/意见征集」三渠道 |
| 实际网络 | `GET /tid/api/display/v1/policy/panorama/feedback` → **HTTP 200**，`records: []` 空列表 |
| 页面表现 | 三渠道均空态：问卷「0 问卷份数 / — 平均评分（本渠道暂无评分）/ 0 五星占比 / 暂无问卷反馈」；在线评价「暂无在线评价」；意见征集「暂无征集意见」。**平均评分显「—」不造 0，意见聚类块不出现（真实态不造演示聚类）** |
| 合规判定 | **PASS 维度**：接口 200 诚实返回空列表，前端 a-empty 空态 + 不造 0 不造聚类，无 501。**FAIL 维度**：预期 6 行三渠道未读到——根因=element 缺库凭证（§0），非前端/接口逻辑缺陷 |
| trace 证据 | 父会话 Tempo：`9c4a5ca8`（display→element 200 但 JDBC Access denied using NO） |
| 截图 | `SENT-QA-F1-反馈三渠道空态-接口200空列表.png`、`SENT-QA-F1-反馈面板特写-问卷空态.png`、`SENT-QA-F1-意见征集渠道空态.png` |

### R1 政策效果评估报告

| 项 | 内容 |
|---|---|
| 步骤 | 同页签挂载 → 组件自动 GET assessment-report |
| 实际网络 | `GET /tid/api/display/v1/policy/panorama/assessment-report` → **HTTP 200**，`records: []` 空报告 |
| 页面表现 | 「暂无可用报告」a-empty；无写死报告、无 501 |
| 合规判定 | **PASS 维度**：同 F1。**FAIL 维度**：预期 2 行报告未读到——同根因（element 缺库凭证） |
| trace 证据 | 父会话 Tempo：`3079b126` |
| 截图 | `SENT-QA-F1-反馈三渠道空态-接口200空列表.png`（报告卡同框） |

## 3. S 组 · 检索（207 三条链路，复用检索页签）

### S1 关键词检索走真实门面

- 操作：关键词搜索 Tab 输入「人工智能」→ 点搜索
- 网络：`GET /display/v1/policy/panorama/search?keyword=人工智能&q=人工智能` → 200；随后自动 `POST /display/v1/policy/panorama/favorites/history` → 200（历史保存，无 user_id 泄漏由 FE 自检覆盖）
- 页面：「共找到 20 项政策」「主检索命中 20 项 · 二次筛选后 20 项 · 已按 1 个类别分组」；首条「关于组织开展人工智能医疗器械创新任务揭榜申报工作的通知 · 苏州市工业和信息化局 · 2021-11-24」——真实库数据非种子
- 截图：`SENT-QA-S1-关键词检索命中20项.png`

### S2 空结果不回退种子（DoD-2 核心）

- 操作：输入 `zzqqxx无此政策` → 搜索
- 网络：search 200，命中 0
- 页面：「共找到 0 项政策」+「无检索结果，不可排序 / 二次筛选 / 按类别分组 / 分享」空态；**结果列表无任何种子政策回退**（「专精特新」仅出现在搜索框示例按钮的静态文案，不在结果列表）
- 截图：`SENT-QA-S2-空结果不回退种子.png`

### S3 详情抽屉

- 操作：S1 结果首条点「查看」
- 网络：`GET /display/v1/policy/panorama/18323509/detail` → 200
- 页面：右侧抽屉（Teleport `.arco-drawer`）展开：政策ID 18323509 / 发布机关 苏州市工业和信息化局 / 发布时间 2021-11-24 / 概览·政策原文·条款结构化页签；空字段显「—」，无种子全文
- 截图：`SENT-QA-S3-详情抽屉真实行数据.png`

## 4. J 组 · jobs（209/212）

### J1 政策实施效果跟踪（policy_effect）

- 操作：点「开始分析」（提交前后按钮 disabled 单飞生效）
- 网络：`POST /display/v1/policy/panorama/jobs {sub_type:"policy_effect"}` → HTTP 200，业务响应 `{"code":1,"msg":"未获取到当前用户"}`
- 页面：红警条「效果分析任务失败：未获取到当前用户（**已返回的反馈与报告保持原样**）」——失败后反馈卡、报告卡内容原样保留（DoD「失败不清空同步块」直接验证），按钮恢复可点
- 合规判定：**PASS**（诚实失败路径完整：后端拒 → 前端原样展示 msg → 同步块保留 → 无伪造区域表）。trace `1761fcb71d7b4513e5042848d04ff922`（规范名对照用例）
- 截图：`SENT-QA-J1-效果任务失败不清同步块.png`
- 遗留：成功终态渲染（区域效果表）待环境修复后复验

### J2 政策匹配与推送（policy_match）

- 操作：主体编号 E0001（默认）→ 点「开始匹配」
- 网络：`POST jobs {sub_type:"policy_match", params:{subject_id:"E0001"}}` → 200，`未获取到当前用户`
- 页面：「匹配任务失败：未获取到当前用户」；**无伪造匹配列表、无演示分**
- 合规判定：**PASS**（匿名拒绝如实提示，不伪造用户与结果）
- 截图：`SENT-QA-J2-匹配任务失败如实提示.png`

### J3 切条件不自动起任务（I2-12）

- 操作：改主体编号 E0001 → U0001，等 2s
- 结果：jobs 请求数 2→2 不变（**不自动 POST**）；sessionStorage 复用键 `pol-sent-job:*` 为空（任务未成功不写复用条目）
- 合规判定：**PASS**

## 5. G 组 · 反向验证（越层与白名单）

经组件同款 xhr（带登录令牌 + systemCode 头）直打 jobs 入口：

| 用例 | 请求 | 响应 | trace | 结论 |
|---|---|---|---|---|
| G1-a | `{sub_type:"effect"}`（裸名） | `code:1 sub_type 只能是 policy_effect、policy_match 或 policy_intensity` | `8617ed35af6d9ad0939fc87c42827521` | ✅ 拒绝 |
| G1-b | `{sub_type:"match"}`（裸名） | 同上拒绝 | `3c58537bb194d0be6d5740d24c4b7850` | ✅ 拒绝 |
| G1-c | `{sub_type:"policy:effect"}`（冒号别名） | 同上拒绝 | `8e604049f5ba1d953e768af3f38ac952` | ✅ Python 别名未透到浏览器入口 |
| G1-d 对照 | `{sub_type:"policy_effect"}`（规范名） | 通过白名单进入业务层（报「未获取到当前用户」身份错，非白名单拒绝） | `1761fcb71d7b4513e5042848d04ff922` | ✅ 闭包白名单非一刀切 |
| G2 | `{sub_type:"policy_focus"}`（老 sub_type） | 同 G1 拒绝文案 | `2f3c30d0d74b6154d1399293be94d537` | ✅ display 白名单未混入老键，老校验未泄漏 |
| G3 | 页面全部请求扫描 | performance 列表所有请求仅落 `/display/v1/policy/panorama/**`，无 `/topicAsync`、`/policy/topic`、`/internal`、任何 `demo-*` | 见 §3/§4 各条 URL | ✅ D12 调用链干净 |

注：裸 fetch（无令牌）下 G1/G2 全部 401「访问令牌不存在 / sso check-token failed」——鉴权层先于白名单，行为正确。

## 6. I2-12 行为附验

| 断言 | 证据 | 结论 |
|---|---|---|
| 切条件不自动起任务 | J3（jobs 数不变） | ✅ |
| 单飞（提交中禁用） | J1/J2 点击后按钮即 disabled | ✅ |
| 失败不清同步块 | J1 红警条文案 + 反馈/报告卡内容保留 | ✅ |
| 空态不造 0 | F1 平均评分「—」；J1/J2 无伪造结果 | ✅ |
| 不 501 充当功能 | 全程无 501（空=200+空列表） | ✅ |

## 7. 缺口登记（转父会话派单）

1. **[环境/配置] element 缺库凭证（P0，阻断 F/R 数据链路）**：K8s `gkxlumen-element` 连 `gkxlumenx_gapfill` 被拒 `Access denied for user 'gkxlumenx'@10.50.179.112' (using NO)`；`using NO` 指向未走密码认证，疑似 K8s env `ELEMENT_MYSQL_PASSWORD` 未配/配错。trace `3079b126` / `9c4a5ca8`；Loki 持续「gapfill 读表失败，返回空列表」。修复后 F1 预期 6 行三渠道、R1 预期 2 行。**父会话已接管派单，本条仅留档。**
2. **[环境] SSO 会话与网关令牌校验不一致**：UC 登录成功但 localStorage 令牌过网关 `sso check-token failed`；组件请求（多带头）200、裸 fetch 401——差异头待定位（可能 systemCode / cookie 会话）。影响 jobs 成功路径复验。不阻断当前验收结论（诚实失败路径已全验）。
3. **[复验项] J 组成功终态**：区域效果表 / 匹配卡列表渲染、当天复用、force 重跑——待 1/2 修复后跑（数据已在 demo ADS：效果 2 行、时序 2 行、匹配 111 行 18 主体，见 MOCK-ADS handoff）。

## 8. 架构合规自检（QA 侧）

- ✅ 只测不修：未改任何业务仓代码；截图与报告为仅有的写产物
- ✅ 未造数、未把 mock 写成上线；D4 口径表述未动
- ✅ 期望未发生必红：G1/G2 非法 sub_type 被拒（若被受理即红）、S2 空结果无种子回退（若出现即红）均验证为绿
- ✅ 证据链：每组附 trace / 截图 / performance URL；截图 8 张归档 `screenshots/SENT-QA-*.png`
- ✅ 任务不标 done；状态流转交 registry 流程

## 9. 产物清单

- 本报告：`agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-SENT-QA-L01.md`
- 截图 8 张：`agent-handoffs/科技政策跟踪-POL/screenshots/SENT-QA-{F1,J1,J2,S1,S2,S3}-*.png`

ponytail: full —— QA 只测不修；空态/匿名/白名单全部按「诚实失败」口径判定，环境缺口如实分离不冒充用例失败。
