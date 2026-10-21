# 维护管理（服务机构占位壳） 脚本→用例 覆盖表（2026-10-14 BATCH32 建仓 · svc-maintenance；2026-10-15 P0-06 补齐 + coverage 建档；同日 P0-07 / P0-08 / P0-09 / P0-10 / P0-11 补齐）

蓝本 = `qa/test-cases/KJZTFWXT/service-产业服务链分析/SVCMAINT-维护管理/FUNC-维护管理-服务机构-用例.md` v2.0（01351~01361，11 条）。
闸门 = `fixtures/scout/env-gate.json`（overall=**pass**，无头 `_env-gate-probe.mjs`；g2~g5 N/A=pass——占位壳无异步任务/预检/生物黑名单/历史结果依赖）。
方法论 = `as-built/retro/20261014-batch32-method-patch.md`。
USM 口径 = E7 README as-built（「维护管理 L4；复用 ENT-OPS 三组 15 项壳，字段服务机构域；门户『专题服务』内容工作台可演示，其余占位」）——目标态说明，现场为占位壳，差异记 observed 不判 Fail。

| 汇总 | 值 |
|------|-----|
| A 档金样 | **5**：`P0-01~P0-05` · **零 allow_skip**（闸门建议升 01355 入金样已采纳；01356 仍 B→A 候补；01361 已独立 B 档） |
| B 档机检 | **6**（P0-06、P0-07、P0-08、P0-09、P0-10、P0-11）· skip 0 |
| 机检合计 | **11** · skip 占比 **0/11 = 0% ≤25%** |
| 本轮不自动化 | **0**（01351~01361 全脚本化） |
| catalog | **未改**（子 agent 禁改；父 agent 挂） |

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 档(A/B) | 页面区块/状态 | P（用例优先级） | skip ticket | 可见动作 |
|---------|----------|---------|---------------|---|-------------|---------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01351 | A | 入口·路由/页头 | P0 | — | goto /service/maintenance；断言 URL+title+H1 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01352 | A | 构成·页头+占位说明+业务占位壳 | P0 | — | goto；断言区块构成+无 ENT-OPS/CHAINMAINT 实壳 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01353 | A | 占位说明·文案全文 | P0 | — | goto；断言文案=闸门/附录 B 全文 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01354 | A | 诚实态·无伪造无假列表 | P0 | — | goto；断言诚实空文案+无演示列表/不可用控件 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01355 | A | 刷新稳定·路由/标题/文案保持 | P0 | — | goto→reload；断言三态保持 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01356 | B | 备选-占位说明·文案语义两要素 | P1 | — | goto；断言当前态+交付来源两要素关键词、主区无「开发中」、非空白页 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01357 | B | 备选-系统级入口·对比篮浮层可达 | P2 | — | goto；点悬浮球开浮层→关闭；断言开合正常、壳不变（路由/H1/占位文案）、对比篮零写请求 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01358 | B | 备选-跨目录兄弟模块隔离 | P2 | — | goto；动态枚举页面内可点入口逐一点击；断言每点后 URL 保持 /service/maintenance、不出现 industry-center/chain-maintenance 等兄弟路由、终态 H1 保持 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01359 | B | 权限-评审模式零泄漏 | P1 | — | goto；P3 关评审（锁态踢门户 observed）→再开评审深链回页；断言附录 A 零泄漏 + 占位文案/页标题与基线一致 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01360 | B | 异常-远端异常·网络异常反馈 | P1 | — | goto；setOffline+reload；断言 chrome-error/ERR 明确反馈 + 非静默占位；P8 恢复在线（零 allow_skip） |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01361 | B | 异常-刷新后路由保持 | P1 | — | goto→reload；只断言 URL 仍 /service/maintenance（不叠 title/占位，归 01355） |

## 本轮不自动化（声明 + ticket）

| 用例编号 | 原因 | ticket / 去处 |
|----------|------|--------|
| — | （空）01351~01361 均已脚本化 | — |

## 补齐纪要（2026-10-15 P0-06 波）

- **本波新建**：`cases/P0-06.yaml`（01356 备选-占位说明文案语义，tier B）+ 本 coverage.md 建档（入口此前缺）。
- **写前探针**：`fixtures/scout/_probe-p006.mjs` → `probe-p006.json` + `probe-p006.png`——两要素在文（`stateOk=true`「入口已对齐 demo 路由」+ `sourceOk=true`「业务区块由后续 US-SVC-* 叶交付」）、主区无「开发中」（浮层 tab「区域 · 开发中」在对比篮浮层内非主区，关浮层后扫 main）、非空白页（H1+占位区块+业务占位面板）、无 ENT-OPS 实壳词（`entOpsShellWordsInMain=false`）。
- **实跑**：`runs/20261015-50892-svc-maintenance-p0-06-r1/`（--only P0-06，headless）→ **pass，4 项机检断言通过**；`check-run-consistency.py` 四方一致性 ✓。
- **--check**：6 条脚本（含 P0-06）assert 编译错误 0。
- **observed（E7 README 口径）**：「复用 ENT-OPS 三组 15 项壳，字段服务机构域」为 USM 目标态交付说明，非现场页面文案；现场为占位壳（无 15 分类实壳词）。后续 US-SVC-* 叶交付业务区块后：01356 复测占位文案移除、01352/01354 同步改写（复测钩子见用例册备注）。
- **前作映射核实**：P0-01~05 ↔ 01351~01355 与用例册「自动化用例ID」列一致（回填时逐行核对）。
- **缩进门检**：P0-01~05 存量 steps/expect 列表均为 2 空格缩进（python yaml 机检全部解析出真实 steps 3 / expect 2~3），无 portal 波列 0 假绿隐患；r3-runner 波（2026-10-14 16:14）steps.md 非空、真断言 2 项、截图齐——非假绿波。

## 补齐纪要（2026-10-15 P0-07 波）

- **本波新建**：`cases/P0-07.yaml`（01357 备选-系统级入口·对比篮浮层可达，tier B；用例优先级 P2 与脚本 id 前缀独立勿混读）——原「不自动化」清单 01357 行移出（本册只顺带验可达与开合无副作用，深交互仍归 COMPARE 集不展开）。
- **写前探针**：`fixtures/scout/_probe-p007.mjs` → `probe-p007.json` + `probe-p007-open.png` / `probe-p007-reclosed.png`——入口=右下悬浮球 `button[aria-label^="打开对比篮"]`（40×40 在屏可点，aria「打开对比篮，共 12 项」）；面板 `div[aria-label="对比篮"].system-compare-panel` DOM 常驻、关→点开 visible、再关回 hidden（X2 可视性语义）；头部「对比篮 · 共 12 项」；类型 Tab 4 项=企业 7/50 · 产业 0/50 · 服务机构 5/50 · 区域·开发中；开合全程路由/H1/占位文案逐字不变；窗口内 compare-basket 全 GET（零写入）。
- **observed（用例备注「篮内条目清单与生产一致性」）**：「共 8 项」为原勘察时点总数；条目数随 guest 共享会话漂移（10-14 scout 16 项=7+4+5 → 10-15 探针 12 项=7+0+5，他端会话增删所致非本页写入）；类型清单稳定 4 类，与生产一致性属人工比对项随 run observed 落盘不判 Fail。
- **实跑**：`runs/20261015-50892-svc-maintenance-p0-07-r1/`（--only P0-07，headless）→ **pass，4 项机检断言通过**（窗口内 POST×0、compare-basket 零非 GET、壳逐字不变）；`check-run-consistency.py` 四方一致性 ✓。
- **--check**：7 条脚本（含 P0-07）assert 编译错误 0；python yaml 门检 P0-07 steps=6 / expect=4 真实解析（2 空格缩进无截断）。
- **run 截图形态**：交互自含 expect 脚本的 steps 阶段截图均为初始态（与已验收 P0-06 r1 / sz P0-20 r2 同形态）；浮层开/合视觉证据由探针 PNG 承载。

## 补齐纪要（2026-10-15 P0-08 波）

- **本波新建**：`cases/P0-08.yaml`（01358 备选-跨目录兄弟模块隔离，tier B；用例优先级 P2 与脚本 id 前缀独立勿混读）——原「不自动化」清单 01358 行移出（操作面经动态枚举收窄为可机检：探针实证页面内可点入口仅 1 个）。
- **写前探针**：`fixtures/scout/_probe-p008.mjs` → `probe-p008.json` + `probe-p008-final.png`——页面全部可点元素共 3 个：全局导航 2（header 内人设菜单「专 创新工作台 INNO 未付费」+ 折叠按钮，`closest('aside, header, nav, [class*=sidebar], [class*=menu]')` 命中）+ 页面内唯一入口=对比篮悬浮球 `button[aria-label^="打开对比篮"]`（40×40 在屏，aria「打开对比篮，共 12 项」）；点击后 `stayedOnPage=true`、终态 `routeKept=true`、`h1Kept=true`；URL 全程 `http://10.50.69.111:30892/service/maintenance` 无漂移。
- **分层口径（任务书 §3 落地）**：「页面内可点元素」= 主区动态枚举（排除全局导航容器）纳入断言逐一点击；「全局导航」（人设菜单/折叠按钮/侧栏菜单）跳别页属预期行为不算缺陷，记 observed 不纳入断言范围；侧栏菜单项为自定义 div 结构不落入 a/button/menuitem/tab 标准选择器集，且属全局导航，不点击。对比篮浮层开合不算路由漂移（P0-07 已验开合壳逐字不变，本探针复验）；浮层内深交互（清空/移除/发起分析）归 COMPARE 用例集，DANGER 词表排除且枚举前先回收浮层防混入点击面。
- **动态枚举设计**：脚本运行时实时枚举（与探针同逻辑同选择器集），后续 US-SVC-* 叶交付业务区块新增按钮自动纳入点击面，无需改脚本；href 型真跳转入口若指向非 `/service/maintenance` 前缀即 fail（承载用例预期②）。
- **实跑**：`runs/20261015-50892-svc-maintenance-p0-08-r1/`（--only P0-08，headless）→ **pass，4 项机检断言通过**（observed：页面内入口=对比篮悬浮球 1 个、已点=1、URL 保持、H1 保持）；`check-run-consistency.py` 四方一致性 ✓（1 条）。
- **--check**：index.yaml `all` 追加 P0-08 前首跑（7 条，assert 编译错误 0）为时序产物；**回填后复检为准**：全量 **8 条脚本，assert 编译错误 0 处**；python yaml 门检 P0-08 steps=4 / expect=4 真实解析（2 空格缩进无截断）。

## 补齐纪要（2026-10-15 P0-09 波）

- **本波新建**：`cases/P0-09.yaml`（01359 权限-评审模式零泄漏，tier B；用例优先级 P1 与脚本 id 前缀独立勿混读）——原「不自动化」清单 01359 行移出。
- **写前探针**：`fixtures/scout/_probe-p009.mjs`（+ b/c/d 补探）→ `probe-p009.json` / `probe-p009b.json` / `probe-p009c.json` / `probe-p009d.json` + `probe-p009-review-on.png` / `probe-p009-review-off.png`——人设面板可达；默认评审=开；开态本页无页面级 trace/metric（壳层共享 2 枚 inMain=false）；精确 mouse 点关「内部评审模式」后路由立即踢至 `/service-portal/overview`（锁态入口 as-built）；关评态深链本页亦重定向；再开评审+深链回页后占位文案与 title 与基线逐字恢复。
- **D1 跟现场**：用例步骤「关闭后读本页」现场不可达；机检改为「关评踢页 observed + 再开评审深链回页后附录 A 零泄漏 + 文案/标题=基线」。D2 建议回开用例补锁态踢页分支。零 allow_skip。
- **自检**（不算正式验收）：`runs/20261015-50892-svc-maintenance-p0-09-self-r1/`（--only P0-09）→ pass，3 项机检断言通过；`--check` 全量 9 条 assert 编译错误 0；python yaml 门检 steps=6 / expect=3。

## 补齐纪要（2026-10-15 P0-10 波）

- **本波新建**：`cases/P0-10.yaml`（01360 异常-远端异常·网络异常反馈，tier B；用例优先级 P1 与脚本 id 前缀独立勿混读）——原「不自动化」清单 01360 行移出（coverage 曾声明「网络中断模拟条件执行期常不可用」；本条实勘后可构造）。
- **写前探针**：`fixtures/scout/_probe-p010.mjs` → `probe-p010.json` + `probe-p010-baseline.png` / `probe-p010-offline.png` / `probe-p010-restored.png`——`context.setOffline(true)`+reload → `net::ERR_INTERNET_DISCONNECTED` + URL=`chrome-error://chromewebdata/`（非静默占位）；body 对 Playwright 常空、无 `.arco-alert`（占位壳无业务 API 失败态）；`setOffline(false)`+深链回页后壳恢复。
- **D1 跟现场**：用例「明确异常反馈」现场承载=浏览器 chrome-error / 导航 ERR（与兄弟册 CHAINMAINT P1-09 setOffline 同源；本环境已采到 ERR+chrome-error → **零 allow_skip**，禁止用正常占位假绿）。不进 gold。
- **自检**（不算正式验收）：`runs/20261015-50892-svc-maintenance-p0-10-self-r1/`（--only P0-10）→ **pass**，3 项机检断言通过；`--check` assert 编译错误 0；python yaml 门检 steps=6 / expect=3。

## 补齐纪要（2026-10-15 P0-11 波）

- **本波新建**：`cases/P0-11.yaml`（01361 异常-刷新后路由保持，tier B；用例优先级 P1 与脚本 id 前缀独立勿混读）——原「不自动化」清单 01361 行移出（曾声明「01355 已含路由断言」；本波严格一用例一脚本独立承载，判定面只钉 URL）。
- **闸门证据**：`env-gate.json` `g_refresh_stable.pass=true`（url 仍 `/service/maintenance`）；本条未另写探针（fixtures 非必需）。
- **与 01355 分工**：P0-05=刷新后路由+title+占位三保持；P0-11=只答路由不漂移；禁止叠页面态断言假绿。
- **自检**（不算正式验收）：`runs/20261015-50892-svc-maintenance-p0-11-self-r1/`（--only P0-11）→ pass，2 项机检断言通过（before/after URL 均 maintenance，routeKept=true）；`--check` assert 编译错误 0；python yaml 门检 steps=4 / expect=2；零 allow_skip；不进 gold。

## 父验收金样 ids

```
P0-01,P0-02,P0-03,P0-04,P0-05
```
