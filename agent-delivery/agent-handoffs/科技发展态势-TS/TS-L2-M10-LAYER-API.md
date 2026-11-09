# TS-L2-M10-LAYER-API · handoff

- 任务：`TS-L2-M10-LAYER-API`（definition · 图层与数据源后台接口设计）
- 日期：2026-11-06 · 监管：`human:刘剑锋` · 认领：`agent:api-agent`
- 状态：接口分册已落盘，**待四角色会签**，不自签 done

## 范围与实现

接口分册（真源）：[`sdd/l2/TS-L2-M10-LAYER-API.md`](./sdd/l2/TS-L2-M10-LAYER-API.md)

- 契约面：`/display/v1/situation/maintain/` 下 4 组资源（layers GET/PUT · layer-groups CRUD · datasources CRUD + probe · factor-display GET/PUT），全同步、全量返回不分页
- 内部委托（**2026-11-06 开发核实后终版 v3**，对齐 ARCH §3）：配置表归 Java 业务库、Python 不参与——display 只做门面校验（400 类不出网关层），读经 Feign→领域服务直读业务库，写经 Feign→领域服务直写业务库；probe 出网归领域服务（display 不出网，SSRF 黑名单在册）。**对外 URL/方法/DTO/错误码全部不变**
- 本分册是 **M10 唯一契约源**：`BE-TS-CONTRACT-02` 范围 M2–M9 不回填；DTO 概要、枚举（SourceType 3 值中文 / LayerCode 9 值英文 / FactorKey 11 值英文）、错误码（400/404/409 GROUP_IN_USE/501 仅 DB 型 probe）全部冻结在册
- as-built 差异表（§0）：`meta` 端点废弃；`targetLayer` 中文改 `targetLayerCode` 英文 code；`lastSync`/`testStatus` 不落契约（无同步动作、探测不持久化）；删组 409 约束
- probe 分型：API 型 Java HEAD/GET 真探测（5s 超时、≤3 重定向、不读体、不落库）；DB 型 501；用户填报型 400（前端禁用按钮）

## 偏离说明

- 无 DoD 级偏离。一处细化：ARCH §5 差异表未提的「targetLayer 中文→英文 code」由本分册裁定（枚举值冻结在 §7，与 demo `LAYER_OPTIONS` 一一对应）
- `TS-L2-M10-LAYER-DATA` 同日落盘并修正 ARCH 种子数（8/9→3/3/9，事实纠错），本分册枚举与修正后种子一致

## 产物清单

- 新增：`agent-handoffs/科技发展态势-TS/sdd/l2/TS-L2-M10-LAYER-API.md`
- 本 handoff

## 架构合规自检

| 铁律 | 状态 |
|---|---|
| 调用链 前端→display→Feign→领域服务→业务库 | ✅ §1 内部委托（v3 终版） |
| D12 无 demo 依赖 | ✅ 枚举/种子值仅作冻结事实源引用 |
| D15 display 不直连 Python/DB | ✅ 读写均经 Feign 调领域服务、probe 归领域服务 |
| D18 接口不返回 mock，读表 | ✅ 全资源读写 cfg_* 表 |
| 指标不新造 | ✅ probe 时延等不注册（METRIC 分册确认） |
| 501 只当未排期用，不当空态用 | ✅ 仅 DB 型 probe；空数据=200 空数组 |

## cost

- actual_tokens: ~25k
- model_used: glm-5.3（ZCode agent）
- actual_cost: <$0.5
- cost_warn: green
