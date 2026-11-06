# TS-L2-M10-LAYER-SIGNOFF-ARCH · 维护管理 · 图层与数据源 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-06
- 对象：`TS-L2-M10-LAYER-ARCH` / `TS-L2-M10-LAYER-API` / `TS-L2-M10-LAYER-METRIC` / `TS-L2-M10-LAYER-DATA`（四张定义稿，2026-11-06 落盘，均已按监管人裁定改写为「写库全归 Python」版本）
- 对照：`architecture-baseline.md` D3 / D7 / D12 / D15 / D18、§2.2 要素归属、§4 机器可读依赖规则
- 监管：`human:刘剑锋`（2026-11-06 裁定：写数据库全归 Python，保持原有规矩 D7/D15；原「gkxlumen-display 直写业务库」裁定作废，稿已按退路转正改写）
- 范围：只读核对，不改被审四张稿，不动 task-registry / WBS，不 git commit/push。格式对齐 `POL-L2-DS10-SENT-SIGNOFF-ARCH`（2026-11-03）先例

## 结论

**有条件同意会签**。改写后链路与 D7/D15/D18 自洽、D18 三要素齐备、范围边界与上游一致、种子数字经独立验证成立。以下 4 条条件不要求改被审稿正文，均为会签确认项的附带边界与后续单动作；条件闭合前四张稿不标 done：

| # | 条件 | 责任落点 | 时点 |
|---|---|---|---|
| C1 | 库名撞名处置：`gkxlumenx_config` 与既有 `gkxlumenx_cfg`（baseline §3.1 D12 数据面 as-built，innov catalog，`InnovSql` / `innov-py` 在用）仅三字母之差。保留建议名须在灌数单与基线登记处写明两库边界一句话备注，或更名（如 `gkxlumenx_maintain_cfg`）；不允许无注记的裸并存 | data-agent 灌数单起草时定，报监管人 | 灌数单起草前 |
| C2 | 基线显式化写授权：baseline §4 `python_show_facade.may_read: [mysql_ads]` 未含任何写授权。本稿 show_service 写 `gkxlumenx_config` 不触 must_not（`write_ads` 限于 ADS），但字面超出 may_read 授权，校验 agent 按 yaml 字面会误判。须由架构角色对 §4 补 `may_write: [gkxlumenx_config（cfg_* 四表）]` 并走 §8 变更记录一行；同条变更顺带回写 ③ 的 D3 侧库只读口径（见下） | `agent:arch-agent`（基线增量，非本会签页动作） | 实现单 `TS-L2-M10-BE-IMPL` 开工前 |
| C3 | SEQ 图 probe 边修正：`TS-L2-M10-LAYER-ARCH-SEQ` 中 `dom -->|probe …| fe` 是领域服务直连前端的画法。按图即契约（图文冲突以图为准）会被误实现为领域服务直连前端，违反调用链铁律。改为探测结果沿 `dom → bff → gw → fe` 原响应链回流（或边改 `dom → bff` 加注）。§4.2 DATA 图省略 gw 节点属数据流视角省略，可接受，实现单版补 gw 或加图注声明 | 接线/实现单引用该图前，由 ARCH 稿维护方修图（draft 图一处边，不动正文） | 实现单起草前 |
| C4 | probe SSRF 防护必列实现单：领域服务对用户登记的任意 `endpoint` 发 HTTP 探测，须限协议 http/https（已有）、禁私网/环回/链路本地/云元数据地址段、重定向 ≤3（已有）、不读响应体（已有）、5s 超时（已有）；地址段黑名单是新增性质，缺它则 ⑤ 的出网裁定不成立 | `TS-L2-M10-BE-IMPL` 实现单 DoD 必列 | 实现单起草时 |

## 逐关注点核对（ARCH §7 ①–⑦）

| # | 关注点 | 架构表态 |
|---|---|---|
| ① | 改写后与 D7/D15/D18 自洽 | **成立，附 C2**。D7：写全归 Python（灌数单 + `gkx_show_service` 运行时写），Java/前端零造假、零写库，符合「Python 写」分工；本二级是真配置 CRUD 非 mock 场景，D7 的「Python 写 Mock 至 ADS」条款不适用。D15：display 只做门面（鉴权/枚举校验/聚合），`display → Feign → 领域服务 → Feign /internal/gkx-show/maintain/config/** → gkx_show_service → 写库` 正是 D15 明文合规路径（「领域服务 Feign 调 Python 算法层（含 show-service）是合规路径」）；display 不直连 Python/DB ✓；唯一残留是 §4 yaml `python_show_facade` 未含写授权（C2）。D18：三要素齐备（见下表）、接口读表不返回内存 mock、无行返回空数组非 501 ✓；本二级是**真实现**（配置 CRUD 本身可实现），不触发 D18 替代条款（新建 ADS 表灌 mock 仅适用于真算/真查/真模型做不到的场景）；配置表不进 ADS 反而正确——运营即时写不适合数仓分层与 D7 数据工厂链路，且混 ADS 语义 |
| ② | 库名 `gkxlumenx_config` + `cfg_` 前缀不挂 `gapfill_` | **方向接受，附 C1**。独立于 ODS/DWD/ADS/gapfill 的 Python 管理配置库、`cfg_` 表前缀表「配置真源」、不混 D16 缺项语义——均成立。撞名 `gkxlumenx_cfg` 须处置（C1），方向本身不因撞名推翻 |
| ③ | D3 字面「Java 仅读 `*_ads`」 vs 政策 gapfill 只读先例 | **口径裁决：接受，沿 D16 / POL 先例。** D3 立法意图是契约面收口：禁 Java 扫 ODS/DWD、禁 Java 写数仓、「算法写、API 读」钉在 ADS。D16（2026-10-28 项目负责人决策）已开第一条结构化豁口：Python 管理侧库 `gkxlumenx_gapfill` + Java 只读，并经 `POL-L2-DS10-SENT` 会签（2026-11-03）落地（领域服务直读 `gapfill_policy_audience_feedback` / `gapfill_policy_assessment_report`）。`gkxlumenx_config` 是同构第二条豁口。**口径一句话：D3 字面约束在「Python 管理的侧库 + Java 零写只读 + 不进 ODS/DWD/ADS 分层」三条件同时满足时按 D16 先例放宽；Java 侧红线不变——不写任何库、不扫 ODS/DWD、不读供应方库。** 建议随 C2 回写 baseline，此后同构场景不再逐单重议。监管人裁定与铁律无冲突（D15 must_not 为 write_ads / 算法职责，写配置库两者皆不触），无需上报冲突 |
| ④ | 领域服务承载（候选 gkxlumen-topic 侧 element 模块）由实现单定 | **接受。** 本叶只锁链路形态（display → 领域服务 → /internal 或直读），承载服务是实现选择。与 §2.2 要素归属不冲突：maintain 配置不属任一要素路由，候选挂 topic 侧 element 模块与政策 gapfill 同链路，实现单定即可 |
| ⑤ | probe 出网位置：领域服务出网（BFF 不出网） | **接受，附 C4。** 与 §2.2 领域服务直接调久新/智谱/深势外 API 同构（领域服务本就承载出网调用，BFF 不出网是 D15 职责边界推导）。前提是 C4 的 SSRF 地址段黑名单落地；探测结果不落库不留存 ✓。若 C4 被否决，接受 API 分册预案：probe 整体降级全型 501，URL 不变 |
| ⑥ | `meta` 端点废弃 | **接受。** BE 从未实现（ARCH §1 grep 0 命中），无兼容负担；拆 4 组资源与 D5 网关路由划分一致 |
| ⑦ | METRIC 全 N/A | **复核成立。** 配置页无统计数字（开关/色值/元数据行/显示名均非统计量），probe 时延是即时探测结果不构成指标口径，D9 角标不渲染于配置页，种子行不设 `is_mock`/`metric_id` 列。同意 METRIC 分册「确认不存在」的结论 |

## D18 三要素核查（ARCH §2 逐叶）

| 叶 | 表名 | 灌数方/写者 | 读取接口 | 判定 |
|---|---|---|---|---|
| 序 5 | `cfg_tech_layer` | 种子 data-agent 灌数单；运行时写 display→领域服务→Python internal | `GET/PUT /display/v1/situation/maintain/layers` | 齐备 |
| 序 7 | `cfg_tech_layer_group` | 同上 | `…/layer-groups`（GET/POST/PUT/DELETE） | 齐备 |
| 序 8 | `cfg_tech_datasource` | 同上 | `…/datasources`（GET/POST/PUT/DELETE） | 齐备 |
| 序 8 probe | —（明示不落表、不持久化） | —（明示无灌数） | `POST …/datasources/{id}/probe` | 语义明示，齐备 |
| 序 9 | `cfg_factor_display` | 同上 | `…/factor-display`（GET/PUT） | 齐备 |
| 序 6 | —（明示不实现，读侧归 M1 WBS-05-18） | — | — | 边界明示 |

四表归属 `gkxlumenx_config` 四稿一致（ARCH §2/§3、API §1、DATA §1）；种子 26 行（3 源/3 组/9 图层/11 要素）经独立核对成立（`repos/demo-ui-science/src/pages/tech-situation-maintain/layerSourceState.js` 与 `repos/lumen-ui-science-pc/src/views/situation/maintain/maintainModel.ts` 一致：src-1/2/3、grp-ip/lit/org、LAYER_OPTIONS 9 值；`situation.ts factorItems` 11 值）。ARCH 原稿「8 源/9 组」误记已被 DATA §0 纠正并采信，无遗留事实错误。

## 链路与铁律核对

| 项 | 判定 |
|---|---|
| 调用链：前端 → gw → display（门面）→ Feign → 领域服务 → Feign `/internal/gkx-show/maintain/config/**` → `gkx_show_service` 写 `gkxlumenx_config` | 与 D15 三层链路一致；display 不直连 Python/DB ✓；对外 URL 全在 `/display/v1/situation/maintain/**`（D5）✓ |
| 读链：领域服务直读 `gkxlumenx_config` → display Feign 聚合；M1 只读 layers / factor-display 同链路 | 按 ③ 口径成立 ✓ |
| D12：不调任何 `demo-*` 服务 | 四稿均写明；种子取自 demo 源码冻结清单属「读代码后重写」合法路径，非运行时依赖 ✓ |
| D13/D14/D17：无消息总线、无对象存储、不触算法闭包 | ✓ |
| D9/D4：无 metric 挂接、不挂 MockBadge、不新造 `metric_id` | ✓（METRIC 分册） |
| 范围边界：序 6/9 读侧归 M1（WBS-05-18）、34–40 不做（报价划掉）、41–47 归 ENT | 四稿一致，与 ARCH §0 上游引用一致 ✓ |
| 图文一致：SEQ 图读写边/四表节点/26 行种子/pyseed 与 §2/§3 一致；DATA 图写终于 Python、读回流与 §3 一致 | 成立，除 C3 的 probe 边方向；DATA 图省略 gw 属视角省略（可接受，建议实现单版补） |

## 备注（非错误，不阻塞）

1. `institution` 图层/要素显示名「组织机构」（demo 冻结）与 baseline §2.2 要素路由表 `institution`=科研机构 是两个语境（图层显示名 vs 要素路由编码）。实现单不得据 §2.2 改显示名。
2. 种子 `src-1` endpoint `https://mock.api/patents` 为 demo 冻结占位 URL，M10 首启 probe 该源将显示「失败」，属预期运营态，不构成 mock 违规（DATA 已标注冻结清单一致）。

## 签收边界

- 本页是架构角色会签，不把四张稿、不把任何任务标 done；签收仍由监管人 `human:刘剑锋` 做。
- 留实现单（`TS-L2-M10-BE-IMPL` 及接线单）：C4 SSRF 地址段黑名单、领域服务承载服务选型（④）、`meta` 端点废弃的 api 层重写、localStorage 降级策略、409 文案接线。
- 留灌数单（data-agent）：DDL + 26 行种子、C1 库名边界注记。
- 留基线增量（`agent:arch-agent`，走 §8 变更记录）：C2 的 `python_show_facade.may_write` 补注 + ③ D3 侧库只读口径回写。
- 条件 C1–C4 不要求改被审四张稿正文；C3 是 draft 图一处边的修正，由 ARCH 稿维护方在实现单引用前完成。
