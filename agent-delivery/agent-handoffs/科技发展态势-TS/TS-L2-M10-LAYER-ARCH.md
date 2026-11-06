# TS-L2-M10-LAYER-ARCH · handoff

- 任务：`TS-L2-M10-LAYER-ARCH`（definition · 图层与数据源后台实现架构）
- 日期：2026-11-06 · 监管：`human:刘剑锋` · 认领：`agent:arch-agent`
- 状态：架构稿已落盘，**待四角色会签**，不自签 done

## 范围与实现

架构稿（真源）：[`sdd/l2/TS-L2-M10-LAYER-ARCH.md`](./sdd/l2/TS-L2-M10-LAYER-ARCH.md)

- 需规：M1《科技全域态势》序 5–9（图层配置 5/6/7/8 + 科创要素 9 的配置面）
- 核心裁定（**2026-11-06 终版 v3**，当日三次演变见稿 §3 表：v1 Java 直写→v2 写库归 Python→**v3 开发团队核实「Java 可建业务表写数据」**）：M10 分区1 演示态正式化为**业务库四张 `cfg_*` 配置表**；DDL+种子（26 行）+运行时 CRUD 全归 Java 领域服务（display 经 Feign，D15 合规）；**Python 不参与、无灌数单**；M1 地图经同一链路只读配置
- 序 6 读侧、序 9 浏览/收藏归 M1（WBS-05-18），本二级不做；序 34–40 报价划掉；41–47 归 ENT 二级
- metric_id 全 N/A（已过 METRIC 会签复核）
- probe：API 型真探测（领域服务出网 + SSRF 黑名单）；DB 表型 501

## 偏离说明

无。范围与存量调研（对照文档 A 段）一致。

## 产物清单

- 新增：`agent-handoffs/科技发展态势-TS/sdd/l2/TS-L2-M10-LAYER-ARCH.md`（含调用链 + 数据流两张 Mermaid，图 ID `TS-L2-M10-LAYER-ARCH-SEQ` / `-DATA`）
- WBS：`工程过程/04-系统集成/05-展示系统集成/WBS.md` §4.1e 行状态更新

## 架构合规自检

| 铁律 | 状态 |
|---|---|
| 调用链 前端→display→Feign→领域服务→业务库 | ✅ v3 终版链路，两图已改 |
| D3 契约面=ADS | ✅ 业务配置表非契约面，Java 读写属 PigX 业务常规（开发团队 2026-11-06 口径，稿 §7 ③ 备案） |
| D7 写数归 Python（数仓灌数） | ✅ 不适用：cfg_* 是业务配置表非数据域写；种子为真配置非 mock，不走 Python 灌数 |
| D12 无 demo 依赖 | ✅ |
| D15 display 不直连 Python/DB | ✅ display 经 Feign 调领域服务，领域服务持表 |
| D18 可实现（表名/灌数方/读接口齐备，接口不返回 mock） | ✅ §2 逐叶三要素（灌数方=Java 实现单 SQL 变更） |
| 指标不新造 | ✅ 全 N/A 已过 METRIC 会签 |

## cost

- actual_tokens: ~60k（会话累计，含调研）
- model_used: glm-5.3（ZCode agent）
- actual_cost: <$1
- cost_warn: green
