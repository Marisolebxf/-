# 脚本重写试点 · 规约痛点与优化记录（工作稿）

> **状态**：已完成（三子任务收口 2026-10-14：SEARCH 重写重跑 → KEYENT 重写重跑 → 本文件 §4/§5 定稿）  
> **试点范围**：SEARCH（00438~00480 → 41 脚本）+ KEYENT（00379~00402 → 24 脚本），v2.0 用例 → 全新脚本，旧脚本与旧 runs 直接删除  
> **目的**：为后续 32 个功能批量铺开沉淀规约优化建议；本文件是试点核心产出之一  
> **记录人**：主对话（qa-agent）· 各子任务执行中发现的问题随时补录

## 0. 已确认决策（背景，子任务 1 执行前）

| # | 决策 | 来源 |
|---|------|------|
| D1 | 三次子任务 = SEARCH 全流程 → KEYENT 全流程 → 复盘收口（纵向切分） | 用户 2026-10-13 22:23 |
| D2 | 脚本编号：金样 P0-01~05 锁定语义，其余按用例册行序重新编号（不沿用旧脚本 id） | 用户 2026-10-13 22:23 |
| D3 | 旧脚本（gold.yaml / scripts.yaml / coverage.md / README）与旧 runs（20260826-search-gold / 20260826-search-full）直接删除，不归档 | 用户 2026-10-13 22:33（git 已恢复可用） |
| D4 | 旧 KEYENT 脚本不拆分不复用，24 用例 → 24 脚本全部从用例文本新写 | 用户 2026-10-13 30:33 修正：拆旧脚本无意义，用例已重写 |
| D5 | git 提交恢复正常流程，每阶段一笔提交 push origin/dev（迁移已结束） | 用户 2026-10-13 22:33 |
| D6 | 每脚本蓝本 = 对应 v2.0 用例行本身；locator 以现场实勘为准，不沿用旧脚本过期文案 | 主对话方案定稿 |
| D7 | 子任务 1、2、3 均由子 agent 隔离执行（主对话专注方案与验收） | 用户 2026-10-13 22:38 |

## 1. SEARCH 重写痛点记录（子任务 1，2026-10-14 01:00 执行完毕补录）

**R1 · 导出链断头无稳定下载入口**
- 现象：P1-11（批量导出）/ P1-22（单条导出）弹层「确认导出查询清单」确认后任务能创建并跑完（toast 100%），但「查看导出记录」仅 toast 瞬现，页面无持久下载按钮/入口，浏览器零下载事件，文件无法落盘。
- 规约条文：qa-test-case-spec §5.4.1 导出类用例要求「创建任务→等完成→下载文件→按附录 B 七字段核对（≥6/7）」；无文件 = Fail。
- 建议修订：①产品侧补「导出记录」持久入口（任务中心或工具区按钮）；②规约补一条「导出链断头（UI 无下载入口）」标准失败描述模板，归类 C1 固定话术，避免每条手写。

**R2 · 条件摘要显示内部枚举值而非中文标签**
- 现象：P1-07 / P0-06 高筛条件摘要出现「资质标签：little_giant」「资质标签：high_tech」，未映射为「专精特新小巨人」「高新技术企业」。
- 规约条文：用例册 as_built 备注「场景 chip 点击后摘要应出现场景对应条件」；未规定显示值必须是业务中文。
- 建议修订：用例册补明确「摘要 chip 显示值 = 业务标签中文名（不出现下划线枚举）」；转一条 UI 文案 bug（C1 范畴之外的产品缺陷，单独 defect 单跟踪）。

**R3 · 搜索提交按钮 locator 与用例文案不符**
- 现象：P0-07 查企业搜索实际提交按钮在 hero 搜索栏内（文案「搜索」），页面另有「查企业」按钮（tab 旁）点击不触发检索；用例步骤文案「点击查一下/查企业按钮」误导脚本定位。
- 规约条文：D4「locator 以 50892 现场实勘为准」；用例册步骤文案未更新。
- 建议修订：用例册 SEARCH 各条「测试步骤」列统一改为「点击 hero 搜索栏内『搜索』按钮」；_script.md 增补「步骤文案与现场 locator 不一致时以实勘为准并在 steps.md 标注」的显式条款。

**R4 · React 受控 tab 异步态导致同 tick 断言假红**
- 现象：P0-18 三模式互切，同一 eval 内 click tab + 立即读 aria-selected 读到旧值（React setState 异步），分步「点击 eval → 读态 eval」全部正确。
- 规约条文：_script.md action 枚举 click 与 assert 无等待语义说明。
- 建议修订：_script.md 增补「click 后断言必须跨 tick（或显式 wait）」时序规约；Playwright 工程化落地时用 expect(locator).to.be.selected 自动等待规避。

**R5 · 对比篮悬浮球遮挡坐标点击**
- 现象：P0-15/P0-16 批量对比时，336×698 对比篮浮层覆盖结果卡，坐标 click 被拦截，需 DOM .click() 绕过。
- 规约条文：schema.md locator 体系无遮挡处理指引。
- 建议修订：schema.md 补「结果区交互断言优先 DOM 事件或先收起对比篮」备注；产品侧评估浮层可折叠态。

**R6 · 保存方案弹层标题与用例措辞不一致**
- 现象：P0-12 弹层标题实为「保存筛选模板」，用例与页面上部按钮文案为「保存为查询方案」，三处措辞不统一（筛选模板/查询方案/我的方案区）。
- 规约条文：用例册 as_built 已录「保存为查询方案」按钮；未录弹层标题。
- 建议修订：产品统一术语（建议全链「查询方案」）；用例册 as_built 补弹层标题字段。

**R7 · 深链路由双轨易错**
- 现象：P1-14 正确深链为 /enterprise/enterprise-search?mode=advanced；/enterprise/search?mode=advanced 落入企业详情壳并 424，路由表无重定向。
- 规约条文：用例册 P1-14 步骤只写「携带 ?mode=advanced 访问」，未指定完整 path。
- 建议修订：用例册补完整 URL；产品侧给 /enterprise/search 加 301 到 enterprise-search 或兜底 404 页。

**R8 · 评审模式开关藏于 persona 菜单且默认开**
- 现象：P1-08/P1-26 内部评审模式 switch 在右上角人设菜单（persona-menu）内，aria-label=「内部评审模式」；早期会话中曾找不到 locator 误判 n/a。
- 规约条文：任务约束「业务态断言脚本前置关闭内部评审模式」但未给开关位置。
- 建议修订：_script.md 补全局前置片段（persona-menu → 内部评审模式 switch aria-checked 置 false 的标准步骤）；fixtures/testdata.yaml 记录该开关路径。

**R9 · allow_skip 与 Fail 边界在现场数据缺失时的裁量**
- 现象：P1-01/P1-02 推荐区未渲染（无推荐数据）→ allow_skip 记 N/A 合理；但 P1-15「无命中反馈」属功能缺失，不能用「数据不配合」豁免，必须 Fail。
- 规约条文：qa-test-case-spec §5.4.1「数据前提不足用 allow_skip 记 Pass-N/A 不判 Fail」——边界在「前提数据」vs「被测功能本身」。
- 建议修订：spec 补一句判别口径：被测功能自身的行为缺失（即使由数据触发）不适用 allow_skip；只有「功能无法被触发」才可 skip。

**R10 · CDP 求值 async 空对象陷阱**
- 现象：Runtime.evaluate + awaitPromise:true 对 async IIFE 常返回空对象，改同步函数或拆多次同步求值才稳定。
- 规约条文：无（工具层）。
- 建议修订：qa/as-built/README 或执行手册补「CDP 求值一律同步单目的」工程注意事项，Playwright 正式化后自然消除。

**R11 · 任务书 D2 编号母表与 v2.0 用例册语义错位**
- 现象：D2 母表按旧语义分配（如 P0-06=00441 查企业关键词、P0-08=00444 热门场景），但 v2.0 用例册重写后 00441 行语义=查企业关键词且其「自动化用例ID」列回填 P0-07、00444 行=热门场景回填 P0-06；首日 10 个脚本的 result.yaml func_id 按任务书字面填写导致与脚本工程 func_id 不一致（后已全量修正，41/41 对齐）。
- 规约条文：D2「编号母表严格执行 id 不可自创」与 D4「每一脚本唯一蓝本=用例册对应行」在用例册重写后可能互斥。
- 建议修订：派单任务书给编号母表时必须与用例册「自动化用例ID」回填列做过一致性预检（脚本侧以用例册回填列+脚本工程 func_id 为唯一基准）；母表只锁金样 id，其余行标注「以用例册回填为准」。

## 2. KEYENT 重写痛点记录（子任务 2，2026-10-14 执行完毕补录）

**R12 · 任务书母表槽位与脚本工程自建编号错位（同 SEARCH R11）**
- 现象：重写首版 scripts.yaml 沿用旧脚本槽位语义自建编号（如区域级联占用 P0-07、评审开关占用 P0-11、地图缩放占用 P1 前段），与任务书 D-KEYENT-1 母表（金样锁定 + P0/P1 按用例册优先级顺延）产生 14 处槽位偏差；run 落盘后才发现，需全量重排 scripts.yaml / coverage.md / full.md / runs 目录与三方一致性校验。
- 规约条文：D-KEYENT-1「编号母表 24 条 1:1，id 不可自创不可空缺」；脚本工程未做落盘前母表比对。
- 建议修订：①执行侧铁律「先抄母表、后写脚本」，scripts.yaml 落笔前逐行比对任务书母表；②落盘后增加「目录名 = result.yaml id = func_id 尾号 = steps.md 标题」四方一致性机检（本次以 Python 脚本收口）。

**R13 · 指标说明卡 Arco TriggerPopup 无法通过 Esc / body click 关闭**
- 现象：P1-06（00399）点击 ⓘ 打开指标说明卡（arco-trigger-popup）后，Esc 键与 body 点击均不关闭，弹层常驻；只能以 style.display='none' 优雅收场，否则污染后续断言。
- 规约条文：UX-UE 通用交互组件规范（D10）要求弹层类交互具备键盘可达关闭路径；qa 脚本无标准收场手段。
- 建议修订：①转 UI 缺陷单跟踪（Esc 关闭缺失）；②_script.md 补「弹层无关闭路径时以 DOM display none 收场并在 steps.md 标注」工程兜底条款。

**R14 · 抽屉关闭拦截与 transparent mask 残留**
- 现象：P0-12（00391）企业清单抽屉点击关闭按钮后 DOM 仍残留 `.arco-drawer-mask`（透明态）与 `.arco-drawer` 容器；P0-05 首次关闭亦有 mask 残留。对「抽屉已关闭」断言需以可视性（display/popup 容器隐藏）为准，不能以节点存在性为准。
- 规约条文：schema.md 断言体系未区分「DOM 存在」与「可视」。
- 建议修订：schema.md 补「抽屉/弹层关闭断言 = 可视性断言（非节点存在性）」条款；产品侧评估 mask 残留是否为 Arco 关闭动画未清理。

**R15 · 级联下拉分组标题 pointer-events none 导致点击穿透**
- 现象：P0-11（00389）区域级联展开后，分组标题节点（如「全国热门科创城市」）pointer-events 为 none，真实点击目标为父级分组容器；直接 click 文本节点无效，需按容器选择器点击。
- 规约条文：D10 交互规范与 schema.md locator 体系未覆盖 Arco Cascader 分组节点点击语义。
- 建议修订：fixtures/testdata.yaml 记录级联分组容器的可点击 selector 口径；_script.md 补「分组标题节点不可点时回退父容器点击」的 locator 回退策略。

**R16 · 天地图 WMTS 瓦片矩阵作为 zoom 证据的间接核验**
- 现象：P0-13（00394）地图缩放后无法从 DOM 直接读取 zoom 值（Leaflet 实例不暴露在 window）；以 WMTS 请求 `TILEMATRIX` 参数变化（9→10→9）作为视野变化的代理证据。
- 规约条文：schema.md 无地图类断言的替代证据规约。
- 建议修订：schema.md 补「地图 zoom/视野断言可用瓦片请求参数（TILEMATRIX / z 参数）作代理证据，observed 记录请求序列」；产品侧评估暴露 `window.__leaflet_map` 调试句柄的可行性。

## 3. 复盘指标（子任务 3 汇总）

| 指标 | SEARCH | KEYENT |
|------|--------|--------|
| 用例数 / 脚本数 / 1:1 达成率 | 43 / 41+2 未脚本化 / 100%（41 脚本逐条映射用例号） | 24 / 24 / 100%（24 脚本逐条映射 00379~00402，母表四方机检通过） |
| expect 断言密度（均值） | ≈3.1 条/脚本（steps 断言全数译自用例预期列） | ≈2.8 条/脚本（结构性检查 00380 五点 / 00381 四点按备注允许，未额外加点） |
| 重跑通过率（Pass / Fail / N-A / Blocked） | 35 / 3 / 3 / 0（P0 18:18 全过） | 24 / 0 / 0 / 0（P0 14:14、P1 9:9、P2 1:1 全过；零匹配空态 2 条实跑通过未走 N/A） |
| locator 实勘修正数 | 9 处（R1~R8 涉及搜索按钮/弹层/深链/persona 开关/级联/摘要值等） | 6 处（R12~R16 涉及母表槽位/指标卡弹层/抽屉 mask/级联分组点击/WMTS zoom 代理证据等） |

## 4. 规约优化建议清单（子任务 3 收口，2026-10-14）

> 分组按规约真源分五类：spec（qa-test-case-spec.md）/ _script.md / _result.md+schema.md / 用例册协作 / 派单流程。
> 同源痛点已合并（R11+R12）；产品缺陷类不入规约建议，单列 §4.6。每条含：来源 R / 问题 / 建议修订 / 影响文件。

### 4.1 spec（qa-test-case-spec.md，现行 v1.2）

| # | 来源 | 问题 | 建议修订 | 影响文件 |
|---|------|------|----------|----------|
| S1 | R9 | allow_skip 与 Fail 的边界在「数据前提缺失」vs「被测功能自身行为缺失」处无判别口径，靠执行者现场裁量（SEARCH P1-15 无命中反馈被一度想按数据不配合豁免） | §5.4.1 或 §8 增补一句判别口径：**被测功能自身的行为缺失（即使由数据触发）不适用 allow_skip；只有「功能无法被触发」（前置数据不存在）才可 skip**；skip 时 observed 必须记录「为何无法触发」 | `qa-test-case-spec.md` |
| S2 | R4 | spec 只管用例层断言，未约束执行层「同 tick 断言」时序——React 受控组件 setState 异步，同一次 eval 内 click+读态会读到旧值造成假红 | §8（测试记录）补执行时序提示：**交互后断言须跨 tick 或显式 wait**；属执行工程注意，Playwright 正式化后由 expect 自动等待兜底 | `qa-test-case-spec.md` §8（一句提示即可，避免与 _script.md 重复） |

### 4.2 _script.md（脚本编写提示词）

| # | 来源 | 问题 | 建议修订 | 影响文件 |
|---|------|------|----------|----------|
| P1 | R3 | 用例步骤文案与现场 locator 不一致（「查一下/查企业」按钮实为 hero 搜索栏「搜索」按钮）时无处理条款 | 增补条款：**步骤文案与现场 locator 不一致时以实勘为准，steps.md 与 as_built_note 标注差异**（D6 已有事实标准，落成文字） | `as-built/prompts/_script.md` |
| P2 | R4 | action 枚举 click 与 assert 无等待语义说明，同 tick 断言假红 | 增补：**click 后断言必须跨 tick（分步 eval 或显式 wait）**；Playwright 工程化后用 expect(locator).to.be.selected 类自动等待规避 | `as-built/prompts/_script.md` |
| P3 | R8 | 「业务态断言前置关闭内部评审模式」无开关位置指引，早期会话找 locator 失败误判 | 增补**全局前置片段**：persona-menu →「内部评审模式」switch aria-checked 置 false 的标准步骤；`fixtures/testdata.yaml` 记录开关路径 | `as-built/prompts/_script.md` + `as-built/scripts/KJZTFWXT/enterprise/{search,key-type}/fixtures/testdata.yaml` |
| P4 | R13 | 弹层无 Esc/body-click 关闭路径（Arco TriggerPopup 常驻）时无标准收场手段，污染后续断言 | 增补兜底条款：**弹层无关闭路径时以 DOM display:none 收场并在 steps.md 标注**（不判 Fail——关闭缺失归缺陷单） | `as-built/prompts/_script.md` |
| P5 | R15 | Arco Cascader 分组标题节点 pointer-events:none 点击穿透，无 locator 回退策略 | 增补：**分组标题节点不可点时回退父容器点击**的通用 locator 回退策略；fixtures 记录级联分组容器 selector 口径 | `as-built/prompts/_script.md` + 两功能 fixtures/testdata.yaml |
| P6 | R10 | CDP Runtime.evaluate + awaitPromise 对 async IIFE 常返回空对象，工具层陷阱无文档 | 在「过程」节补工程注意：**CDP 求值一律同步单目的**（async 拆多次同步求值）；Playwright 正式化后自然消除 | `as-built/prompts/_script.md` |

### 4.3 _result.md + schema.md（执行与断言体系）

| # | 来源 | 问题 | 建议修订 | 影响文件 |
|---|------|------|----------|----------|
| X1 | R1 | 导出链断头（任务完成但 UI 无持久下载入口）时无标准失败描述，每条手写 | _result.md 失败描述模板增补 **C1「导出链断头（UI 无下载入口）」固定话术**（现象 + file:null + 建议缺陷单）；仅规约侧，产品修复见 §4.6 D1 | `as-built/prompts/_result.md` |
| X2 | R14 | 抽屉/弹层关闭后 DOM 残留透明 mask 与容器，「节点存在」≠「可视」，断言易假红/假绿 | schema.md §4 断言体系补条款：**抽屉/弹层关闭断言 = 可视性断言（display/popup 容器隐藏），非节点存在性** | `as-built/schema.md` |
| X3 | R16 | 地图 zoom/视野无法从 DOM 直读（Leaflet 实例不暴露 window），无替代证据规约 | schema.md 补：**地图 zoom/视野断言可用瓦片请求参数（TILEMATRIX / z）作代理证据，observed 记录请求序列** | `as-built/schema.md` |
| X4 | R5 | 对比篮悬浮球遮挡结果卡坐标点击，locator 体系无遮挡处理指引 | schema.md locator 体系补备注：**结果区交互优先 DOM 事件（.click()）或先收起对比篮**；两功能 full.md 已有易错点条目，升格为 schema 通用条款 | `as-built/schema.md` |
| X5 | R12 | 槽位错位在 run 落盘后才发现，缺少机检闸门 | _result.md 落盘检查补一条：**run 落盘后执行「目录名 = result.yaml case_id = func_id 尾号 = steps.md 标题」四方一致性机检**（本次以 Python 脚本收口，建议固化为 tools/ 常驻脚本） | `as-built/prompts/_result.md`（+ 可选 tools/ 校验脚本沉淀） |
| X6 | 用户走查 2026-10-14（问题 1；13:33 修订） | 现行规约仅失败条强制截图（schema L73「screenshots/ 可选」、L78「截图可无」），成功条无终态画面，交付证据链不完整（本次 SEARCH 仅 2 张、KEYENT 0 张，较旧 run 每条有图为退步） | schema.md §4 改为：**每个操作步骤后必须截图**，文件名 = `步骤序号-简要说明.png`（如 `01-进入搜索页.png`、`05-点击搜索按钮.png`），存 `scripts/{id}/screenshots/`；序号与 steps.md 逐步记录一一对应；终态画面 = 最后一步截图（final.png 表述废止）；删除「截图可无」表述，screenshots 由「可选」升为**必选**（observed/steps 仍不可代替） | `as-built/schema.md` §4 + `_result.md` |
| X7 | 用户走查 2026-10-14（问题 1/5 延伸） | 执行中发现与用例预期不符的现场事实（如枚举值泄漏）仅文字记入 observed/actual、verdict 仍 pass，无截图无编号，缺陷立案证据链断裂（D2 五处出现仅存文字） | _result.md 增补：**verdict=pass 但 actual/observed 出现异常现场事实时，必须当场补截图 `screenshots/anomaly.png` + result.yaml 增 `anomaly_note` 字段**；§4.6 缺陷候选清单每条必钉**脚本编号 + 证据文件路径** | `as-built/prompts/_result.md` + 本 retro §4.6 表（后续缺陷清单模板） |
| X8 | 用户走查 2026-10-14（问题 2） | 无统一分辨率口径：MCP 默认视口不定，macOS Retina 下截图实为 2x（3840×2160），各 run 之间纵向不可比 | 统一功能测试分辨率：**1920×1080 + device_scale_factor=1**。fixtures/testdata.yaml 增 `viewport: {width: 1920, height: 1080, device_scale_factor: 1}` 标准字段；run 的 meta.yaml 记录实际 viewport；MCP 执行开场 `browser_resize` 1920×1080 一次 | `as-built/schema.md`（meta/ fixtures 字段）+ 两功能 fixtures + full.md 开场步骤 |
| X9 | 用户走查 2026-10-14（原生 runner 讨论） | MCP 逐步执行含 LLM-in-loop（每步看快照→思考→下一步），65 条跑 3~4h；regression 应确定性回放。expect 现为中文 prose，机器不能直判 | 落地**原生 Playwright runner（tools/ 跑批器）**：消费 scripts.yaml（locators/steps ~95% 直译）；expect 双层化 `{assert: 机检断言, note: 中文说明}`（格式定稿见下方块），存量由 AI 辅助一次性转换；执行形态 headless（new headless 与有头同引擎，本项目栈无已知阻塞；导出链 context 开 accept_downloads）；上 CI 时容器装 Noto CJK 字体。铺开前先做**校准跑**：runner 无头重放 KEYENT 24 条与 MCP 有头结果比对 verdict 一致 | `tools/` 新增 runner + schema.md expect 双层字段 + 后续脚本模板 |
| X10 | 用户走查 2026-10-14（问题 1 延伸 · 补录决策） | `_result.md` 铁律要求每 run 落盘 `prompts-used.md`（摘录实际喂给执行 agent 的任务书），本次两个 r2 run 均遗漏（任务书原文仅存会话记录，run 自证链断裂）；历史不追溯补录（用户裁定 2026-10-14） | `_result.md`「每条完成检查」前置 **run 级自检**：`meta.yaml` / `SUMMARY.md` / `prompts-used.md` 三文件存在性核对，缺一不宣称 run 完成；后续 runner 化后由跑批器自动落盘任务书参数 | `as-built/prompts/_result.md`（run 级自检清单） |

> **X9 · expect 双层格式定稿**（用户拍板 2026-10-14：双语「人话+机器」+ 注释，格式 qa 定）
>
> ```yaml
> expect:
>   - note: 结果标题出现「智能搜索结果 · 命中 N 家企业」                 # 必填：人话，译自用例预期列（人读/评审/追溯）
>     assert: "await expect(page.getByText('智能搜索结果')).toBeVisible()"  # 尽填：Playwright 原生断言表达式（runner 直判）
>     manual: true                                                        # 仅写不出机检断言时出现（主观文案/视觉类）；runner 跳过并标待人工
> ```
>
> 规则：① `note` 必填，保持与用例册预期列对齐——MCP 人工执行照 note 判定，assert 作操作提示；② `assert` 用 Playwright 原生表达式字符串（不发明 DSL，runner 零翻译成本），在 runner 的 page/expect 上下文中求值；③ 存量 65 条由 AI 辅助一次性转换，转换前 runner 遇裸字符串条目按 note 处理并告警；转换完成后 schema.md 禁止 expect 出现裸字符串。

### 4.4 用例册协作

| # | 来源 | 问题 | 建议修订 | 影响文件 |
|---|------|------|----------|----------|
| C1 | R2 | 条件摘要显示内部枚举值（little_giant/high_tech）未映射中文，用例册未规定显示值必须业务中文 | 用例册 as_built 口径补明确：**摘要 chip 显示值 = 业务标签中文名（不出现下划线枚举）**；枚举值映射缺失转缺陷单 §4.6 D2 | SEARCH/KEYENT 用例册（下次修订时并入） |
| C2 | R3 | 用例步骤文案「点击查一下/查企业按钮」与现场实际按钮（hero 搜索栏「搜索」）不符 | SEARCH 用例册「测试步骤」列统一改为**「点击 hero 搜索栏内『搜索』按钮」** | `FUNC-企业查询-用例.md` v2.0 下次修订 |
| C3 | R6 | 保存方案弹层标题「保存筛选模板」与用例措辞「保存为查询方案」不一致，三处术语混用 | 用例册 as_built 补弹层标题字段记录差异；产品术语统一归 §4.6 D3 | SEARCH 用例册 as_built |
| C4 | R7 | 深链用例只写「携带 ?mode=advanced 访问」未指定完整 path，双轨路由易踩 424 | 用例册补完整 URL：`/enterprise/enterprise-search?mode=advanced`；路由重定向缺失归 §4.6 D4 | SEARCH 用例册 P1-14 行 |

### 4.5 派单流程

| # | 来源 | 问题 | 建议修订 | 影响文件 |
|---|------|------|----------|----------|
| D1 | R11+R12（同源合并） | 任务书编号母表与 v2.0 用例册「自动化用例ID」回填列语义错位（SEARCH 41 条 func_id 全量修正、KEYENT 14 槽位全量重排），「母表严格执行」与「用例册为唯一蓝本」在用例重写后互斥 | 派单任务书规则增补两条：① **母表只锁金样 id；其余行标注「以用例册回填列为准」**；② 任务书下发前必须与用例册回填列做一致性预检（脚本侧以用例册回填列 + 脚本工程 func_id 为唯一基准） | **QA 侧落点**：`as-built/prompts/_script.md` 增补「收到含母表的任务书先与用例册回填列逐行比对，不一致以用例册为准并回告派单方」闸门条款（用户裁定 2026-10-14：QA 不改派单手册）；**对 coordinator 的诉求走建议渠道**（本 retro + PM 转达）：QA 任务书母表只锁金样，是否入《智能体编排与派单手册》由 coordinator/PM 拍板 |
| D2 | R12 | 「先抄母表后写脚本」未成铁律，首版自建编号造成全量重排返工 | 执行侧铁律写入派单话术：**scripts.yaml 落笔前逐行比对任务书母表**；落盘后四方机检（见 X5）双闸门 | `as-built/prompts/_script.md`（执行侧闸门；同 D1 不碰派单手册） |

### 4.6 建议转缺陷单（产品缺陷，不入规约）

| # | 来源 | 现象 | 建议处置 |
|---|------|------|----------|
| D1 | R1 | 批量/单条导出任务完成（toast 100%）但无持久下载入口，「查看导出记录」仅 toast 瞬现，文件无法落盘（SEARCH **P1-11=00478 / P1-22=00479** 已判 C1 Fail） | 转 BUG 单：产品侧补「导出记录」持久入口（任务中心或工具区按钮）。证据：`runs/20261013-50892-search-r2/scripts/P1-11/`（no-download-entry.png + FILE-MISSING.md）、`…/P1-22/`（同构） |
| D2 | R2 | 高筛条件摘要显示内部枚举值（little_giant / high_tech）而非中文标签（专精特新小巨人 / 高新技术企业）；出现于 5 处 pass 条，仅文字记录无截图（X7 立案证据链教训） | 转 BUG 单：枚举→中文标签映射补齐。证据（文字）：`runs/20261013-50892-search-r2/scripts/{P0-06=00444, P0-10=00446, P0-12=00448, P1-07=00471, P1-18=00466}/observed.yaml`；**复现截图待补**（铺开前按 X7 补拍或随缺陷单现场复现） |
| D3 | R6 | 保存方案链路三处术语混用（查询方案 / 筛选模板 / 我的方案） | 转 BUG 单（低优）：产品统一术语，建议全链「查询方案」。证据：`runs/20261013-50892-search-r2/scripts/P1-17=00464/`（result 备注区） |
| D4 | R7 | /enterprise/search?mode=advanced 落入企业详情壳 424，路由表无重定向 | 转 BUG 单：加 301 到 enterprise-search 或兜底 404 页。证据：`runs/20261013-50892-search-r2/scripts/P1-12=00460/`（result actual） |
| D5 | R13 | 指标说明卡（Arco TriggerPopup）Esc 与 body click 均不关闭，弹层常驻 | 转 BUG 单：违反 D10 键盘可达要求，补关闭路径。证据：`runs/20261014-50892-keytype-r2/scripts/P1-06=00399/`（result actual；截图待补，同 X7） |
| D6 | R14 | 抽屉关闭后透明 mask（.arco-drawer-mask）残留 DOM | 转 BUG 单（低优）：评估是否 Arco 关闭动画未清理。证据：`runs/20261014-50892-keytype-r2/scripts/P0-12=00391/`（observed mask 残留记录；截图待补，同 X7） |

### 4.7 试点结论

1. **重写+重跑模式可行**：两功能 65 条脚本（41+24）全部从 v2.0 用例文本重写，重跑通过率 59/65（SEARCH 35 Pass/3 Fail/3 N-A；KEYENT 24 全 Pass），3 个 Fail 均为真实产品缺陷（导出断头×2、无命中反馈缺失）而非脚本问题——「删旧重写」比「修补旧脚本」成本低、判定干净，验证了 D3/D4 决策。
2. **规约不需要大改**：16 条痛点全部消化为 24 条规约建议（含 R11+R12 同源合并、用户走查新增 X6~X10）+ 6 项缺陷单；其中 5 条（R1/R2/R7/R13/R14）同时产生规约侧条款与缺陷侧跟踪。所有建议均为现有规约文件的一句话级增补，无一需要重构编号体系或字段结构；最大修改是派单流程 D1（母表锁金样+预检），属流程条款而非结构变更——且按用户裁定落 QA 侧闸门（`_script.md`），不改派单手册。
3. **用例册是唯一蓝本已在事实上成立**，但需要派单侧配合：母表与回填列的一致性预检（D1）+ 落盘后四方机检（X5）双闸门后，两功能 65/65 四方一致，该模式可作为铺开的标配。
4. **下一步铺开建议**：32 个功能按「SEARCH 模式」铺开（纵向切分：单功能全流程 → 复盘补录 retro）；每 5~8 个功能收口一次 retro 增量（不必每功能一条）；§4 建议清单经 PM/架构师评审后择机并入各规约文件（建议随 v1.3 spec 修订一并落地）；§4.6 六项缺陷单在铺开前先录入 bug-registry，避免后续功能重复踩坑误判 C1。
5. **成本数据**：SEARCH 约 4h（含 41 脚本 + 重跑 + 9 处实勘修正）、KEYENT 约 2h（24 脚本 + 重跑），铺开均值预估 3~5 min/脚本（含执行落盘），供后续排期参考。

## 4.8 原生 runner 校准（X9 落地实录，2026-10-14 补录）

> 背景：X9 决策后落地 `tools/run-scripts.mjs`（原生 Playwright 跑批器），KEYENT 24 条 + SEARCH 41 条做校准跑。本节记录 runner 层新挖出的系统性教训（区别于 §1/§2 MCP 时代痛点）。

**轮次与结果**（SEARCH 全程 41 条，KEYENT 24 条一次校准通过）：

| 轮 | 变更 | pass | 备注 |
|---|---|---|---|
| r2 | MCP 有头基线（对照锚点） | 35/41 | — |
| r3 | 首跑 runner | 5 | 大面积词表/词名缺失 |
| r4→r5 | 一次实勘（四状态 DOM 快照→fixtures/selectors.yaml）+ 批量修 + 前置自足（P8） | 15→19 | — |
| r6→r7 | 我误判"词表覆盖不足"再补词表 | 19→19 | **r7 是浪费的一轮**：未先审计就跑 |
| r8 | 视口外浮动条改文本级断言 | 21 | — |
| r9 | 修 `第[一二]张卡复选框` 正则同映射 `.first()` bug | 见 runs | 真根因：两次点击同一行=勾选→取消 |

**runner 层新教训（编号续 §1/§2）**：

| # | 痛点 | 规约/工具修订 |
|---|---|---|
| R17 · **词表覆盖率审计先于重跑**：r7/r8 空跑源于"跑一轮发现一批漏词"的被动模式；先做全量 target→tryHeuristic 正则扫描（71/71 覆盖）再跑，一轮收敛 | tools/ 固化 `词表覆盖审计` 脚本（本次为内联 Python），铺开各功能前必跑 |
| R18 · **正则字符族掩盖多目标**：`第[一二]张卡复选框` 一条正则同时匹配两个语义目标却 return 同一 `.first()`——click 无异常但行为=勾选→取消，所有"操作成功断言失败"类假红先查此模式 | 词表规约：一个 target 词一个映射；字符族 `[一二]` 禁用于含序数语义的目标 |
| R19 · **视口外元素 toBeVisible 必假**：底部浮动条（已选 N 家企业）文本在 DOM 但视口外，`toBeVisible` 判 false；目视截图"没勾上"实为点击自取消（R18）与视口外（R19）两个独立陷阱叠加 | runner 增 `floattext` kind（innerText 文本级断言）；schema.md 补条款：**视口外/底部浮动条断言 = 文本级（innerText），非可视性** |
| R20 · **select_option 只适用原生 `<select>`**：Arco Select/Dropdown 非原生元素，`selectOption` 必报错；应展开→click 选项两步 | _script.md 补：**Arco 下拉族一律 click 展开 + click 选项，禁用 select_option** |
| R21 · **登录流时序**：Enter 提交偶发不生效（焦点/时机），需 Enter→等 URL→回退点按钮三段式；fixtures 凭据独立文件化已验证 | runner ensureLogin 三段式已固化，无需规约变更（记录备查） |
| R22 · **同 tick 断言（R4 的 runner 版）**：runner 步骤化执行天然跨 tick，MCP 时代 R4 痛点在 runner 下自然消失——佐证 X9 决策 | 无修订；retro 记录工具选型收益 |

**校准结论**：runner 化收益实证——KEYENT 一次通过、SEARCH 七轮收敛暴露的全部是 runner 工具 bug 与词表工程问题（R17~R21），非脚本语义问题；MCP 时代痛点 R4/R10 自然消除。铺开顺序建议：**先词表审计（R17）→ 再校准跑 → 差异归因三分类（工具 bug / 脚本问题 / 产品行为）**。

## 5. 指针一致性核验（子任务 3，2026-10-14）

> 核验范围：catalog ↔ 脚本工程 ↔ 用例册 ↔ runs ↔ README/prompts 五方互指。方法：路径存在性检查 + Python yaml 机检（scripts/coverage/run/用例册回填四方一致性）+ grep 旧目录名残留扫描。**发现的失效引用已就地修复，明细见 Fix 行。**

### 5.1 catalog ↔ 脚本工程 ↔ runs 路径存在性

| 功能 | 检查项 | 结果 | 说明 |
|------|--------|------|------|
| ent-search | `scripts` / `gold` / `full_scripts` 三路径 | ✅ Pass | 三文件均存在于 `scripts/KJZTFWXT/enterprise/search/` |
| ent-key-type | `scripts` / `gold` / `full_scripts` 三路径 | ✅ Pass | 三文件均存在于 `scripts/KJZTFWXT/enterprise/key-type/` |
| ent-search | catalog `inventory_run` 指向已删旧 run 的 `inventory/` | 🔧 **Fix** | 路径失效。已置 `inventory_run: null`（v2.0 r2 run 无 inventory/ 子目录，不指向不存在路径；`source` 字段仍有效）。后续需重爬侧栏时再回填新 run 路径 |
| 全局 | `catalog/index.yaml` systems 路径 | ✅ Pass | 三系统 catalog 文件均存在 |

### 5.2 四方一致性机检（脚本工程 ↔ coverage.md ↔ runs result.yaml ↔ 用例册回填列）

| 功能 | scripts+gold | coverage.md | run result.yaml | 用例册回填 | 结果 |
|------|-------------|-------------|-----------------|------------|------|
| SEARCH | 41 | 41 | 41 | 43（00473/00480 空回填=声明内未脚本化） | ✅ Pass：yaml=coverage=run 逐条 id↔func_id 全一致；回填列 41/41 对应（2 空为声明内） |
| KEYENT | 24 | 24 | 24 | 24 | ✅ Pass：四方逐条全一致（脚本 id ↔ func_id ↔ 用例册「自动化用例ID」） |

### 5.3 数量一致性（coverage.md 行数 ↔ 脚本数 ↔ SUMMARY 计数）

| 功能 | coverage 主表行数 | gold+scripts yaml 脚本数 | run result.yaml 数 | SUMMARY 判定 | 结果 |
|------|------------------|------------------------|--------------------|--------------|------|
| SEARCH | 41（+1 补充行非独立脚本） | 5+36=41 | 41 | 35 Pass/3 Fail/3 N-A（grep verdict 复核一致） | ✅ Pass |
| KEYENT | 24 | 5+19=24 | 24 | 24 Pass（grep verdict 复核一致） | ✅ Pass |

### 5.4 旧 run 目录名残留扫描（验收红线）

| 扫描范围 | 模式 | 结果 |
|----------|------|------|
| `as-built/README.md`、`qa/README.md`、`as-built/catalog/`、`as-built/prompts/` | `20260826-50892-search` / `20260828-50892-key-type` | 🔧 **Fix 后清零**：README.md 3 处 + catalog 1 处已改指 r2 新 run；修复前 grep 命中见下表 |
| `as-built/runs/*/meta.yaml`、`SUMMARY.md` | 同上 | ✅ 免扫（历史记录文件，meta.yaml 明确记载「旧 runs 已删除」属正常历史叙述） |
| `as-built/tools/*.mjs`（2 个旧辅助脚本） | 同上 | ⚪ Out-of-scope：`run-ent-search-full.mjs` / `emit-search-full-case-artifacts.mjs` 为一次性工具脚本，指向已删旧 run 属历史产物，不参与指针链，本试点不清理（建议后续随 tools/ 清理任务处置） |

**修复明细**：修复前 grep 命中 `as-built/README.md` 3 处（L45/L46/L66）+ `catalog/KJZTFWXT.yaml` 1 处（L11 inventory_run）；修复后目标文件 grep 为 0。`qa/README.md` 本无旧引用，零改动（保留他人未提交的 perf-baseline 行不动）。

### 5.5 用例册与 scripts.yaml 的 func_id 互指抽样

抽样 5 条（SEARCH P0-05→00456、P0-07→00441、P1-11→00478；KEYENT P0-11→00389、P1-06→00399）与用例册「自动化用例ID」回填列交叉核对——全部一致（机检覆盖 65/65，抽样仅示意）。
