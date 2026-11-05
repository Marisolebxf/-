# SVC-VIZ-DEMAND-MATCH-FIX-20261105 · 产业服务需求与匹配修复记录

- 日期：2026-11-05。
- 来源：用户直接要求修复产业服务可视化的需求分布、供需匹配空态，并要求按主仓 Cursor 规范提交代码。
- 执行：agent:codex；用户身份未确认，不代填监管人姓名。
- 标识：本文为本会话交付追踪标识，不宣称已在 task-registry 注册；本会话未挂载 task-registry MCP，不直接读写注册表。
- ponytail: full；复用现有 Arco/ECharts 及 Java 聚合层，无新增依赖。

## 范围与实现

对照 `bid-reference/科技信息展示系统和科技专题服务系统.md` 服务需求与匹配可视化：需求分布图按服务类型展示，支持行业、企业规模筛选；供需匹配用热力图展示。

- 前端真实模式恢复行业、规模筛选，需求分布按需求服务类型汇总。
- 需求分布和供需匹配使用面向客户的空态，不直接展示后端 reason。
- Java 两块的异常仍记日志，返回业务空态。
- 保持前端 → Java REST → Python `/internal/*` 调用链；未改路由、依赖、可观测配置、数据库或指标就绪度。

## 提交与文件

- `lumen-ui-topic`：`f517ccd`，已推送 `origin/dev`。
  - `src/views/viz/service/ServiceVizPage.vue`
  - `src/views/viz/service/serviceViz.selfcheck.mjs`
- `lumen-svc-platform`：`3e75227`，`git push origin dev` 返回 Everything up-to-date，远端已包含。
  - `gkxlumen-topic-svc/gkxlumen-topic-svc-biz/src/main/java/com/topcomm/gkxlumen/topic/svc/service/impl/ServiceVizServiceImpl.java`
  - 对应 `ServiceVizServiceImplTest.java`
- 上述历史提交带 `[agent:codex]`，未带本文追踪标识；已发布提交不改写，本记录补充映射。

## 验证

- 前端 `serviceViz.selfcheck.mjs`：通过。
- 前端 `npm run type-check`：通过。
- 前端 `npm run build-only`：通过。
- 两仓 `git diff --check`：通过。
- Java 已增加异常空态测试；本机无 Maven 和 Maven Wrapper，测试未执行，不宣称通过。

## 排查证据与遗留问题

- 前端请求 `/svc/topic/v1/service-portal/viz`；Java 映射 Python `/internal/gkx-svc/portal/demand`、`/match`，代码中的请求路径一致。
- Python 路由已存在，查询 `gkxlumenx_gapfill.svc_demand_match`；工作区未发现该表的 DDL 或装数脚本。这只能证明仓库缺少交付资产，不能证明线上数据库一定缺表。
- 截图的两句“数据服务暂不可用”对应 Java catch 分支，说明调用或响应处理发生异常；确切异常仍须从线上日志确认。
- Python demand/match 当前只处理 data_year，未应用顶部 industry 参数；不能据此前端修复宣称产业筛选端到端已闭环。
- 仍需核对线上 Python 版本、表结构与数据、查询权限及日志；未写入演示数据，未执行线上数据修复。

## CI/CD 与验收状态

- 两个业务仓的 `origin/dev` 代码提交已确认。
- 使用 GitLab API 按提交 SHA 查询流水线，两个项目均返回 HTTP 404，未取得 Pipeline ID/URL 或成功证据。
- K8s rollout、线上页面与接口冒烟：未验证，不标记完成。
- 当前交付范围为代码修复与提交；线上数据出数及 CI/部署闭环仍待验证。

## 规范与偏离

已核对主仓 `.cursor/rules/00-path-resolution.mdc`、`00-team-constitution.mdc`、`multi-session-protection.mdc`、`frontend.mdc`、`api.mdc`、`ponytail.mdc`。

代码保持现有 Vue/Arco 组件、蓝色图表和前端只调 Java 的架构。未更改第三方工作产物，未使用 force push。未新增独立指标或修改指标定义，不伪造 D9 就绪状态。未完成截图走查、D9 全量扫描或线上验收，故不宣称全部工程 DoD 已通过。

成本：本会话没有可核验的 token/费用计量，未虚填 actual_tokens / actual_cost；模型为 gpt-6.1-sol（本轮提交与规范核对）。

## 用户走查修正：筛选控件按需展示

用户指出无数据时新增两个空下拉框增加页面负担。重新核对需规：需求分布明确支持按行业、规模筛选，但未要求始终展示控件。

本次只调整显示条件：行业、规模分别在有效选项数量大于 1 时展示；两个维度都没有可筛选项时不渲染工具栏。无数据时保留需求分布、供需匹配两块业务空态，避免用户展开空下拉框。未增加接口、字段、依赖或新业务流程。

本次复验：前端自检、type-check、build-only、diff --check 均通过。

## 用户明确口径：一级 NIC 行业 + 统一企业规模

用户要求复用 `code_nic` 一级行业，规模按需规严格支持。本节取代上节“有多个选项才显示”的临时处理。

- 行业：前端复用 Java 现有 `/enterprise/topic/v1/search/meta/industries`，请求 `{parent_code:"0", mode:"children"}`，仅显示一级门类；名称用于显示、code 用于筛选，不从需求结果反推选项。
- 规模：复用 `/enterprise/topic/v1/search/meta/enterprise-scales` 的统一大型、中型、小型、微型四档，不使用既有 store 中的旧三档兜底。
- 两项可独立选择、组合选择、清空恢复全部；需求为空时仍提供完整字典选项。
- 现有 `/svc/topic/v1/service-portal/viz` 新增可选请求字段 `nic_code`、`enterprise_scale`，Java 既有 Map 请求原样透传，无需改 Java。
- Python `/internal/gkx-svc/portal/demand` 使用参数化 SQL 过滤：一级 NIC 通过同版本 `code_nic` 获取该门类及子级的 code/scode/name，匹配需求行 `industry`；企业规模匹配四档及带“企业”后缀的名称。未匹配的行业不猜测归类；无效码或规模返回非零业务码。
- 行业、规模作用于需规指定的需求分布，不新增供需匹配算法或重新定义匹配分值。顶部产业筛选的历史限制仍见上文。
- 前端加请求版本校验，快速切条件时旧响应不覆盖新条件结果。

验证：前端 selfcheck、type-check、build-only、diff --check 通过。Python 新增需求组合过滤测试，含 SQLite 内存执行真实过滤 SQL，覆盖一级/下级码及名称、规模后缀、清空、无结果、非法参数；与行业字典相关回归合计 `9 passed, 4 deselected`。

首次同时运行完整 `test_meta_dimension_endpoints.py` 时，两个未改动的旧产业链 fallback 用例失败（期待 LOW_ALTITUDE/NEW_ENERGY，现实现返回 INB 新码）；未为通过测试改动该历史逻辑。仅排除 meta_chains 后运行本次相关回归，结果见上。

未验证线上字典、需求数据源及部署；不宣称空数据问题已由筛选改动解决。未执行数据库写入或装数。

本节代码提交已推送 `origin/dev`：前端 `96b5e7b`，Python `aa6589a`。

## 发布复核：筛选控件消失截图

用户再次反馈筛选消失。首次直接读取 `http://10.50.69.111:30892` 的静态资源：入口 `index-j6Jhg88K.js`，页面 `ServiceVizPage-BxkD72bY.js`，仍含 `length>1` 隐藏条件且无 `nic_code`，说明截图对应旧实现。

主仓 GitLab 客户端使用配置令牌并通过项目搜索解析数字 ID 后可正常查询 CI；此前按远端 URL 携带的凭据及编码路径查询 404 不代表 CI 不可用。

前端项目 ID 17，Pipeline 3878（96b5e7b）成功，deploy:k8s job 25698 成功。日志确认镜像 `gkx-lumen-topic:96b5e7b3` rollout 成功，完成于 2026-11-05 17:24:59（北京时间）。链接：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-topic/-/pipelines/3878

再次读取同一线上地址：入口更新为 `index-CUIacGWu.js`，页面 `ServiceVizPage-BTXDs16X.js`，包含 `nic_code`、“全部行业”“全部企业规模”，且无 `length>1` 隐藏条件。确认最新筛选控件代码已随部署生效；本次未执行登录后的浏览器交互，不宣称字典与业务数据端到端已验收。

Python Pipeline 3877 的 deploy:search-py job 25691 已成功（需求接口所在进程）；查询时 show-py 镜像任务仍在运行，未将整条 Python Pipeline 宣称为成功。

## 数据展示闭环：用户授权补 Mock，修复实际部署入口

用户明确要求补 Mock 数据，使需求分布、供需匹配可展示。本次直连项目数据库只读核对，确认 `gkxlumenx_gapfill.svc_demand_match` 真实存在且已有 10 条 `data_source=mock` 的演示行；早前仓库未发现 DDL 不能用于推断线上缺表。

根因已确认：`gkx_svc_service.main` 虽挂载 service_viz，但线上 Docker 实际运行 `gkx_search_service.main`，后者缺少 service_viz 路由。Java 因此收不到结果并降级空块。本次在实际部署入口补挂同一 APIRouter，并新增 TestClient 回归覆盖部署入口上的 demand/match 两端点。

### 数据与查询

- 用户授权范围内复用既有演示表，不新增表、不写 ODS/DWD/供应方库、不覆盖原有 10 条。
- Python 脚本：`lumen-topic-py/scripts/seed_service_viz_mock.py`，默认只读预览，`--apply` 才写入；连接复用配置且不输出凭据。
- 读取真实 `code_nic` 一级门类 20 项，生成 20 行业 × 4 规模 × 6 深圳地区 × 6 服务类型 = **2,880 行**，2026 年，`data_source=mock_svc_viz_20261105`。事务写入，同批命名锁、按业务维度 NOT EXISTS 防重复。全部为规则生成的演示计数与预置匹配分值，不是源业务实测。
- 匹配接口以 `region,demand_type` 分组，需求数加权汇总已有匹配分值，输出唯一格子，避免各行业规模重复格子叠加。空分值与零需求不参与。
- 复用既有 MockBadge 标识两块数据库演示来源；未把 D4 改成 live、未启用前端 Mock 开关或返回硬编码 fixture。
- 既有 `svc_demand_match` 位于 gapfill 库且不满足当前 D16 `gapfill_` 命名/元数据，属于此前实现的遗留；本次只补该现有表，未冒称它是正式真实业务源。后续按正式数据源治理迁移，不能将本批演示行当作真实需求事实。

### 验证和发布结果

- Python：路由挂载、行业/规模过滤、热力格子聚合 **6 passed**；聚合验证执行 SQLite SQL，非仅字符串断言。
- 前端：selfcheck、type-check、build-only、diff --check 通过；ECharts 已注册 HeatmapChart 和 VisualMapComponent。
- 本地修正入口连接真实数据库：需求 2,890 行；制造业 C＋小型 36 行，信息服务业 I＋大型 36 行；匹配 43 格。
- Python commit `c07c5fa`，Pipeline **3881** 所有 build/package/deploy job 成功，deploy:search-py **25720** 成功。
- 前端 commit `0a87fef`，Pipeline **3882** 所有 job 成功，deploy:k8s **25727** 成功。
- 线上实际 Java 聚合接口 `POST http://10.50.69.111:30892/svc/topic/v1/service-portal/viz`：HTTP 200、code=0，`demand.empty=false`、rows=2,890；`match.empty=false`、cells=43。
- 同接口 `{nic_code:"C",enterprise_scale:"小型"}`：HTTP 200，需求缩为 36 行；匹配保持 43 格（筛选控件按需规仅约束需求分布）。
- 浏览器验证到统一 SSO 登录页，未执行登录后的截图验收。当前闭环证据为 CI rollout 成功、已发布静态资源与页面实际调用的 Java 聚合接口出数；不虚报登录后视觉走查。

CI：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-topic-py/-/pipelines/3881

CI：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-topic/-/pipelines/3882
