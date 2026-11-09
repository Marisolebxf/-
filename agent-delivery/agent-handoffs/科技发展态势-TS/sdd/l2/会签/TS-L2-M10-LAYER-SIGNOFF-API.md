# TS-L2-M10-LAYER-SIGNOFF-API · 维护管理 · 图层与数据源 · 接口会签

- 角色：`agent:api-agent`
- 日期：2026-11-06
- 对象：`sdd/l2/TS-L2-M10-LAYER-API.md`（主审，2026-11-06 监管人裁定后改写版）；交叉核对 `TS-L2-M10-LAYER-ARCH.md`（§2/§3/§5/§7）、`TS-L2-M10-LAYER-DATA.md`（列定义与 DTO 对齐）、`FE-TS-10A.md`（as-built）
- 监管：`human:刘剑锋`
- 范围：只读核对。不改被审文件，不动 task-registry / WBS，不 git commit / push。API 分册是对外契约（URL/方法/DTO/错误码）的裁决对象；内部链路（Feign/Python）以 ARCH 分册为准，本页只核 API 分册对链路的表述与契约面不自相矛盾

## 结论

**有条件同意**。条件 1 条（错误码一致性，一行级修订）；备注 4 条（不阻塞，落实现单/接线单处理）。条件清掉后，本分册可作为 Java 实现单 `TS-L2-M10-BE-IMPL` 的唯一契约源。

## 条件（会签生效前需修订 API 分册）

1. **400 错误码双轨不一致**：§4.1 填报型 probe 响应体写 `400 { code: 'INVALID_SOURCE_TYPE' }`（API 分册 L97），而 §6 错误码汇总只有 `400 PARAM_INVALID` 且场景列明「填报型 probe」（L121）。同一场景两处两个 code，实现单无法判定该返回哪个。二选一：§4.1 改用 `PARAM_INVALID`（本页倾向，§6 保持四码封闭），或 §6 补登 `INVALID_SOURCE_TYPE`。其余三个码（404 NOT_FOUND / 409 GROUP_IN_USE / 501 NOT_IMPLEMENTED）§4.1 与 §6 一致，无需动。

## 核对一：4 组资源 + probe 完备自洽（能否当唯一契约源）

| 资源 | 方法/路径/请求/响应/空态 | 判定 |
|---|---|---|
| layers（§2） | GET/PUT 齐全；固定 9 枚举集不可增删、只收 `layerCode`+`enabled`、其余字段忽略不报错、出枚举 400、PUT 回全量。图层为枚举集故无 POST/DELETE/{id}，成立 | 完备 |
| layer-groups（§3） | GET/POST/PUT/DELETE 四动作齐全；`groupCode` 服务端生成、`groupName` 不唯一（写明理由）、color 格式 400、删除约束（409 + 先改挂/置空）自洽 | 完备 |
| datasources（§4） | 四动作 + `groupId` 可空/传 null 置空/传不存在 404；`endpoint` 语义随型；无级联删除写明 | 完备 |
| probe（§4.1） | 三型分派：API 型 200 实时结果（`result`/`latencyMs`/`message?`，失败也是 200 带结果——探测失败是数据不是 HTTP 错误，语义清晰）；DB 型 501；填报型 400。路径 id 不存在 → 404 沿 §6 通则 | 完备 |
| factor-display（§5） | GET/PUT 齐全；11 行固定不可增删、只收显示名/颜色、`sortOrder` 冻结、出枚举 400 | 完备 |
| 横切 | 全量不分页（9/11/十行级，成立）；最后写胜无乐观锁（运营配置单管理员，成立）；空态=空数组+200 写死；鉴权沿 `/display` 网关、traceId 沿既有链 | 完备 |

判定：**可作唯一契约源**（条件 1 清除后）。两处留白建议实现单拍板而非补进分册：PUT /layers 单次请求内重复 `layerCode` 的处理（建议后者胜或 400，二选一写死）；PUT 类「部分提交」语义（只传变更行，从请求形状读是自然解，可在实现单注一句）。

## 核对二：枚举三套与种子逐一对得上

| 枚举 | API §7 | 事实源 | 判定 |
|---|---|---|---|
| SourceType 3 中文值 | `API 接口`/`数据库表`/`用户填报` | `layerSourceState.js` L1 逐字一致；lumen `maintainModel.ts` L68 一致；DATA §4 `source_type` 三值一致；种子三型各一（src-1/2/3）与 demo L13-44 一致 | 一致 |
| LayerCode 9 | paper/journal/patent/scholar/meeting/institution/topic/project/result + 中文名 | demo `LAYER_OPTIONS`（L2，中文 9 值）与 API §7 中文名列一一对应；DATA §2 `layer_code` 9 值同序冻结 | 一致 |
| FactorKey 11 | scholar/meeting/institution/enterprise/service/topic/project/paper/journal/patent/result | `situation.ts` `factorItems` L92-104 的 key 逐一、同序一致；中文 gloss 与 factorItems label 逐字一致；DATA §5 同 | 一致 |
| LayerCode ⊂ FactorKey | 差集 `enterprise`/`service` | factorItems 确含 enterprise/service 且不在 LAYER_OPTIONS | 成立 |
| 种子行（DATA 交叉） | 分册头声明 3源/3组/9层/11要素=26 行 | demo `layerSourceState.js` L10-53：src-1/2/3（enabled 1/1/0、endpoint、挂组 grp-ip/lit/org）、grp 三组（名/色）逐一与 DATA §3/§4 种子列一致；DATA §5 颜色=M1 `entityColorByKey`（situation.ts L62-74，11 键齐） | 一致（API 分册头已采 DATA §0 修正后的正确数字，未沿用 ARCH 原稿的 8/9 误记） |

## 核对三：错误码与空态语义

- 四码覆盖判定：枚举外/缺必填/格式/超长→400；路径 id 与请求 groupId→404；删被引用组→409；DB probe→501。边界够用，无遗漏场景被发现（probe 打不存在 id、PUT 不存在 id 走 404 通则；改名重名 200 放行且已写明理由）。
- 空数组 vs 404 vs 501：§6 明文「无行=空数组+200，不是 501、不是 404」，501 全分册仅 DB 型 probe 一处。三分语义清晰，可作为实现单断言用例。
- 唯一缺陷即条件 1（400 双 code）。

## 核对四：内部委托改写后自洽（可实施性）

| 项 | 核对 | 判定 |
|---|---|---|
| 链路与 D15 | display 门面（鉴权/枚举/参数校验/聚合）→ Feign → 领域服务 → Feign `/internal/gkx-show/maintain/config/**` → `gkx_show_service` 写库；读经领域服务直读。`architecture-baseline.md` L142（D15）：display「不直连 Python/DB」、领域服务 Feign 调 show-service 是合规路径、路由前缀 `/internal/gkx-show/**` 与分册写法匹配 | 合规 |
| 400 不出网关层 | 枚举/格式类校验 display 本地可判（三套枚举在本分册冻结，门面持有静态枚举表即可），不依赖 DB。成立 | 可实施 |
| 404/409 回传映射 | 引用完整性（groupId 存在性、组下是否挂源）依赖库，display 无库可查，归 Python 写侧回传映射——与「写库全归 Python」职责划分自洽，且码语义与 §6 对齐。POST/PUT datasource 报 404 多一跳往返，十行级配置可接受，不要求 display 预读校验 | 可实施 |
| 对外契约不变 | §1 明文 URL/方法/DTO/错误码不受内部链路影响；分册 §2–§7 通篇无内部路径漏进对外契约 | 成立 |
| probe 出网 | §4.1 出网归领域服务、display 不出网，与 ARCH §3.5 一致；已标注 ARCH §7 ⑤ 会签点及否决退路（全型 501、URL 不变） | 一致（见备注 3 的引用措辞） |

## 核对五：§0 as-built 差异五项，前端接线可行

| 项 | 证据 | 判定 |
|---|---|---|
| meta 废弃 | real 分支唯一端点确认：`lumen-ui-science-pc/src/api/situation/maintain.ts` L13-23 仅 `fetchMaintainMeta` 打 `/situation/v1/maintain/meta`；BE 无实现（ARCH §1 grep 0 命中），无兼容负担。api 层重写为 4 组资源拼装可行（页面 store 本就按分区组织） | 可行 |
| targetLayer 中→英 | `types/maintain.ts` L17-26 `LayerOptionKey` 确为中文字面量；`LAYER_OPTIONS` 中文序与 §7 code 表 1:1，对照索引取 code 可行 | 可行 |
| lastSync 不设 | demo 行上 `lastSync`（`types/maintain.ts` L35）与 DATA §4「不设 last_sync」互证。备注：demo `getDisplayLayerSources` 的 `latestSync` 聚合随列同灭，接线单动作只写了「列」，聚合函数需一并处理（见备注 4） | 可行 |
| testStatus 不落契约 | demo 行上 `testStatus`（L36）三态演示值不迁移；probe 实时返回、按钮即时态可行 | 可行 |
| 删组 409 | demo `removeLayerGroup`（L166-180）确无引用约束直接删（且自动改挂）；正式契约 409 + 先改挂再删，前端接 409 文案可行。备注：demo 另有「至少保留一个图层组」约束，正式契约未保留亦未声明放弃（见备注 2） | 可行 |

## 事实错误清单

未发现硬性事实错误。分册头种子数（3/3/9/11）、real 分支唯一端点、D15 表述、WBS-05-24「无权限是降级不是白屏」（`工程过程/04-系统集成/05-展示系统集成/WBS.md` L80/L148 原文相符）、枚举三套、FE-TS-10A §M1 联动语义引用，逐项核过均与源码/事实源一致。

## 备注（不阻塞，落实现单/接线单）

1. **DTO↔表列两处命名映射需实现单写死归属**：Datasource DTO `groupId`（bigint，引 `LayerGroup.id`）↔ DATA `cfg_tech_datasource.group_code`（varchar，逻辑引用组 code）；FactorDisplay DTO `factorName` ↔ `cfg_factor_display.display_name`。两键各自唯一、映射无损，但 id↔code 翻译发生在哪层（Python 写侧或领域服务）未写——实现单定一处即可，不构成两分册冲突。
2. **§0 差异表可补第 6 行**：demo 删组还有「至少保留一个图层组」约束（`layerSourceState.js` L167），正式契约允许删到 0 组（无引用即成功）。属合理简化，但 §0 自称差异清单，建议补一行「显式放弃」避免接线单误移植。
3. **§4.1 括注「（display 不出网，D15）」引用略松**：D15 原文是 display「不直连 Python/DB」，未明文禁对外出站；「display 不出网」的真依据是 ARCH §3.5 裁定 + §7 ⑤ 会签点。分册已正确标注会签点与退路，改个引用源即可，非事实错误。
4. **latestSync 聚合**：见核对五第 3 行，接线单处理 `getDisplayLayerSources` 时一并写明。

## 签收边界

- 本页是接口角色会签意见，不把任何任务标 done；签收归监管 `human:刘剑锋`。
- 条件 1 的修订由 API 分册认领人落笔，本角色不代改被审文件。
- probe 出网位置（ARCH §7 ⑤）与读侧 D3 口径（§7 ③）属架构角色会签范围，本页仅确认 API 分册对二者「引用一致、退路成立」。

## v3 快审（2026-11-06）

- 对象：`TS-L2-M10-LAYER-API.md` v3 终版（内部委托改回 Java 领域服务直读直写业务库，display 经 Feign，Python 退出；对外契约不变）。只读核对，不改被审稿。
- 前置确认：v2 条件 C1（400 双码统一）已回填——§4.1 填报型 probe 改 `400 PARAM_INVALID`（带 API-C1 溯源括注），与 §6 四码封闭一致。**条件清空**。

### 结论

**通过**。v3 只动内部链路归属（写侧 Python → Java 领域服务直写业务库），对外 URL/方法/DTO/错误码未变；「门面 400 本地可判 / 404/409 写侧回传映射」的职责划分在 v3 表述下仍自洽；v2 残留已清净；备注 4 条无一被 v3 推翻（备注 2 已被分册回填闭合）。本分册可作 `TS-L2-M10-BE-IMPL` 唯一契约源。

### 核对清单

| # | 项 | 核对结果 |
|---|---|---|
| 1 | §1 内部委托 + §4.1 + §6 职责划分自洽 | 成立。写体校验（枚举/格式/长度）输入是请求体非库，§7 三套枚举冻结，门面静态表可判，与写侧语言无关；404/409（groupId 存在性、路径 id、组下引用）依赖库，库在领域服务手中，回传映射且码语义与 §6 一致；「400 不出网关层」限定于写体校验语境，probe 链路（无请求体、按库中 sourceType 分派）的 400/404/501 均由领域服务侧回传——§4.1 主语「领域服务发起」写法正确，与 §1 不矛盾（v2 同构，非 v3 新引入）。§1 明文对外契约不受内部链路影响，§2–§7 无内部路径漏进对外契约 |
| 2 | v2 残留 grep | 干净。`gkxlumenx_show_config` / `/internal/gkx-show` / `gkx_show_service` / `灌数单` 正文断言 0 命中；`/internal` 词根、撞名变体 `gkxlumenx_config` 亦 0 命中。`Python` 唯一出现于 §1 v3 声明句（「Python 不参与」+ D15 规则原文引用），属正确表述；`INVALID_SOURCE_TYPE` 仅存于 §4.1 C1 回填溯源括注（变更记录，非断言）；分册头种子事实源引用指向 demo 仓，按口径不算 |
| 3 | v2 备注 4 条在 v3 下 | 均仍成立/已闭合。① groupId↔group_code 翻译层：仍需实现单写死，v3 后候选收敛为 display 门面或领域服务之一（更简）；② 至少留一组：**已回填**——§0 差异表第 6 行显式声明放弃，接线单不再移植；③ D15 引用精度：措辞问题原样（v3 下 D15 的「Python」半边更无关），§4.1 末行已正确引 ARCH §7 ⑤，仍不阻塞；④ latestSync 聚合：与写侧归属无关，接线单一并处理，不变 |
| 4 | SSRF 黑名单 × 领域服务直写链路 | 兼容。探测发起方仍是领域服务（v3 只改其实现归属），黑名单条款（环回/私网/链路本地/云元数据/内网主机名、命中 400 不发请求、DNS 重绑定解析后按 IP 复核）作用于 probe 出网行为本身，与实现语言无关，Java 可落地；写侧直写业务库不产生出网行为，无新攻击面引入。ARCH §3 第 5 条 / §7 ⑤ 确认「probe 归领域服务出网 + SSRF 黑名单成果保留」，分册引用一致 |

- v3 新增轻备注（不阻塞，接 ①）：§1「写侧错误（404/409）由领域服务回传映射」的列举未含 probe 链路回传的 400/501——§4.1 逐格已写死响应码、§6 封闭，无实现歧义，实现单照 §4.1 执行即可。
- 签收边界不变：不标 done，签收归监管 `human:刘剑锋`；领域服务承载侧（候选 gkxlumen-topic）归 ARCH/实现单，本页只确认 API 分册对其引用一致。
