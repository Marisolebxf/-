ponytail: full

# TS-DS01-DEMO-ACCEPT-LOOP · DS-01 演示样本循环验收记录

> **验收单**：TS-DS01-DEMO-ACCEPT-LOOP（tech_task / qa-agent）　|　**监管人**：human:李伟
> **依据**：`产品实现规程.md` §6.5；计划 `agent-delivery/工程过程/04-系统集成/05-展示系统集成/编排计划/TS-L2-DS01-LOOP计划.md`；用例真源 `agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS01-合规演示用例.md`
> **性质**：只读验收（GET/POST 查询体），零代码改动、零 commit/push；token 不落盘、不进本文档。

## 运行 2026-11-07 R1

- **执行**：qa-agent　|　**轮次**：R1（第一轮）
- **探测（第一笔）**：`POST http://10.50.69.111:30895/display/v1/situation/overview`，头 `Authorization: Bearer <本机 token>`（读 `%USERPROFILE%\.gkx\display-loop-token`，len=32，内容不记录）+ `systemCode: display`，body `{}`，curl.exe `--max-time 40`。
  - 返回 **HTTP 401**：`{"code":401,"msg":"访问令牌不存在","data":"sso check-token failed","ok":false}`
  - 命中计划 §1 熔断（401/令牌失效文案）→ **停止，不进逐行对照、不建子任务**；验收单 `blocked`，note「token 失效，已通知 human:李伟」。
- **逐行对照表（11 行可演）**：因探测熔断，11 行全部未发起请求，无接口证据，不判「对得上/对不上」，登记如下。

| 行 | 内容 | 端点 | 条件 | HTTP | 关键返回 | 判定 |
|---|---|---|---|---|---|---|
| 1/2/3 | 总览统计/领域分布/图层切换 | situation/overview、situation/map | — | 未发起 | 熔断（探测 401） | 未执行 |
| 5 | 地区切换（9 市+区级） | situation/map 带 region | — | 未发起 | 熔断（探测 401） | 未执行 |
| 6（部分） | 对象点位 | situation/map | — | 未发起 | 熔断（探测 401） | 未执行 |
| 10 | 事件流 | situation/events | — | 未发起 | 熔断（探测 401） | 未执行 |
| 11/12（部分） | 时间趋势/年份切换 | situation/timeline | — | 未发起 | 熔断（探测 401） | 未执行 |
| 13 | 要素对比 | situation/compare 带比较参数 | — | 未发起 | 熔断（探测 401） | 未执行 |
| 14（部分） | 影响力卡片 | situation/influence | — | 未发起 | 熔断（探测 401） | 未执行 |
| 15 | 主路径端到端 | 上述串行 | — | 未发起 | 熔断（探测 401） | 未执行 |

- **结论**：**blocked** —— 本机 `display-loop-token` 已被 SSO 判定不存在（令牌失效）。对得上 **0/11**（熔断未对照，**非样本缺口**，不做 DATA/QUERY/ALGO 分类、不建补数单）。
- **下一步建议**：监管人 human:李伟 换发新 token 写入 `%USERPROFILE%\.gkx\display-loop-token` 后触发 R2；R2 仍为只读全量 11 行对照，计划与用例不变。
- **参考线索（供排查，非结论）**：同日早些时候 M2/M3 回填探测（`TS-DS01-CASE-FILL-L01.md`）口径为「无 token」即可 200；本轮 401 说明网关鉴权已切换为强制令牌且本机令牌失效，换发后须以新探测为准。

## 运行 2026-11-07 R2

- **执行**：qa-agent　|　**轮次**：R2（token 已由 human:李伟 换发并验证 situation/overview 200）
- **探测（11 笔全 200）**：网关 `http://10.50.69.111:30895`，头 `Authorization: Bearer <本机 token>`（读 `%USERPROFILE%\.gkx\display-loop-token`，内容不记录）+ `systemCode: display`，body 一律写 `$env:TEMP` 文件用 `-d "@file"`（避免 PowerShell 内联引号 400），curl.exe `--max-time 40`，全部只读 POST。

| # | 端点 + 参数 | HTTP | 关键返回 |
|---|---|---|---|
| P1 | `/overview {}` | 200 | stats=9、factorCards=9、domainRows=6、trendSeries 2015—2025 共 12 年、**currentYear=空（基线 2026）**、isEmpty=false |
| P2 | `/map {"enabledFactorKeys":["paper"]}` | 200 | **回归**：scholar/institution/enterprise/service/project/patent 仍 active=true 且计数同全量；meeting/topic/journal/result 置 false（topic/result 计数为空）；objectPoints=0（基线 CASE-FILL P5：其余 10 要素 active=false） |
| P3 | `/influence {}` | 200 | cards=5（基线 5）；**totalCount=225,647（基线 50,631，漂移）** |
| P4 | `/map {}` | 200 | factorItems=11、regions=9、objectPoints=99、scopeLabel=全量样本 |
| P5 | `/map {"regionPaths":[["深圳市"]]}` | 200 | scopeLabel=城市：深圳市、regions=1、objectPoints=100 |
| P6 | `/map {"regionPaths":[["深圳市","南山区"]]}` | 200 | scopeLabel 区县级正确、regions=1，区级级联可取 |
| P7 | `/events {}` | 200 | events=34（基线 34） |
| P8 | `/events {"importanceFilter":"high"}` | 200 | events=1（2026-05-04 invest 战略投资，importanceScore=67.16）→ 重要性筛选生效 |
| P9 | `/timeline {"timeRange":{2025,2026}}` | 200 | years=[2025,2026]、rangeLabel=2025-2026、events=34 |
| P10 | `/timeline {"timeRange":{2026,2026}}` | 200 | events=11（收窄生效）；**但 years/rangeLabel 恒回 2025-2026（标签未随动）** |
| P11 | `/compare {"selectedFactorKeys":["enterprise","paper","scholar","project","institution"]}` | 200 | availableFactorKeys=5、series=5、years=2015—2025，返回有差值 |

### 11 行逐行对照（计划 §2）

| 行 | 条件 | 端点 | HTTP | 关键返回 | 判定 |
|---|---|---|---|---|---|
| 1/2/3 | overview {} + map {paper} | overview、map | 200 | stats=9 ✓、domainRows=6 ✓、factorItems=11 ✓；图层切换：enabledFactorKeys=["paper"] 时其余 6 要素未置 false（见 P2），与基线「其余 10 要素 active=false」矛盾 | **对不上**（图层过滤回归） |
| 5 | map 深圳市 / 南山区 | map 带 regionPaths | 200 | regions 9→1、scopeLabel 正确、区级级联可取 | 对得上 |
| 6（部分） | map {} | map | 200 | objectPoints=99（全量）/100（深圳市） | 对得上 |
| 10 | events {} / high | events | 200 | events=34；high→1 且类型/重要性值域齐 | 对得上 |
| 11/12（部分） | timeline 2025-2026 / 2026-2026 | timeline | 200 | years 含 2025/2026 ✓、切换有数（2026-2026→11 条）✓ | 对得上（带观察 O2） |
| 13 | compare 5 要素 | compare | 200 | 5 比较要素可切、series=5、返回有差值 | 对得上 |
| 14（部分） | influence {} | influence | 200 | cards=5（基线 5）✓ | 对得上（带观察 O3） |
| 15 | 主路径端到端（开页→切图层→切地区→看趋势→看事件） | 上述串行 | 全 200 | 全链有数，但「切图层」环节行为与用例期望不符（见 P2） | **对不上**（含图层切换环节缺陷） |

- **对得上 9/11**；**对不上 2/11**：行 3（图层切换）+ 行 15（主路径含该环节，同根因）。

### 缺口分类（只建议，不建单——等监管人）

- **G-R2-1【QUERY】**：`/map` 对 `enabledFactorKeys` 过滤未完整生效——仅 paper 时其余 6 要素（scholar/institution/enterprise/service/project/patent）仍 active=true 且计数同全量；meeting/topic/journal/result 置 false 但 topic/result 计数为空字符串（基线 11/232）。疑似 legend 构建丢失 enabledFactorKeys 过滤或部分要素查询未应用条件。建议 QUERY 类排查；注意与同日 CASE-FILL P5 基线矛盾，疑为 R1→R2 之间服务端变更引入。
- **DATA 确认建议（非判定缺口）**：influence `totalCount` 50,631 → 225,647（cards=5 不变），建议 DATA 侧确认口径是否变更（如从评分企业数和改为全库计数）。

### 观察项（不判对不上）

- O1：overview `currentYear` 返回空（基线 2026），前端默认年份展示可能受影响。
- O2：timeline 请求 2026-2026 时 events 收窄为 11（过滤生效），但 `years`/`rangeLabel` 恒回 2025-2026（标签未随动）。
- O3：见 G-R2-1 附带的 topic/result 计数空字符串，与过滤回归同源记录。

### 覆盖不到 5 行（4/7/8/9/16）

检索降级（search-py DOWN）、M10 未建表、要素/事件详情契约未冻结——属开发/契约缺口，本轮不判不建 DATA/QUERY/ALGO 单，登记「待开发完成」清单；若连续两轮仍在，交监管人裁定（§6.5.7 步 9）。

- **结论**：**有缺口待分类**（QUERY×1 建议 + DATA 确认建议 1 项）。验收单 **保持 blocked 不动**，等监管人 human:李伟 核对后统一处理。token 不落盘、不进本文档；本轮零代码改动、零 commit/push。

## 运行 2026-11-07 R3（修复部署后复测）

背景：Q01（TS-DS01-LOOP-R2-Q01）修复已推 origin/dev（commit 04da6ad）并经 CI 自动部署至 zhipu-tts。

- R3-P1 单选 `enabledFactorKeys=[paper]` → 200，paper active=true count=858620，**其余 10 要素全部 active=false（10/10 灭）**
- R3-P2 多选 `[paper,patent]` → 200，paper/patent 双亮（858620/71043），其余全灭
- 行 3（图层切换）：**对得上**（排他语义成立）；行 15（主路径含图层切换）：**对得上**
- 结论：R2 的 9/11 + R3 补验 2 行 = **11/11 样本满足**，待监管人「签收」后再校验一次即收口
