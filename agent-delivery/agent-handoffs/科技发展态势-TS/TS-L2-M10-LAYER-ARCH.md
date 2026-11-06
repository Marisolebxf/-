# TS-L2-M10-LAYER-ARCH · handoff

- 任务：`TS-L2-M10-LAYER-ARCH`（definition · 图层与数据源后台实现架构）
- 日期：2026-11-06 · 监管：`human:刘剑锋` · 认领：`agent:arch-agent`
- 状态：架构稿已落盘，**待四角色会签**，不自签 done

## 范围与实现

架构稿（真源）：[`sdd/l2/TS-L2-M10-LAYER-ARCH.md`](./sdd/l2/TS-L2-M10-LAYER-ARCH.md)

- 需规：M1《科技全域态势》序 5–9（图层配置 5/6/7/8 + 科创要素 9 的配置面）
- 核心裁定（**2026-11-06 监管人裁定后修订**：写库全归 Python，原「Java 直写业务库」作废）：M10 分区1 演示态（页面内存 + localStorage）正式化为 **`gkxlumenx_show_config` 库（Python 侧）四张 `cfg_*` 配置表**；DDL+种子（26 行）归 data-agent 灌数单；运行时写经 `display 门面 → 领域服务 → gkx_show_service /internal/gkx-show/maintain/config/**`；读沿政策 gapfill 只读先例由领域服务直读；M1 地图经同一链路只读配置
- 序 6 读侧、序 9 浏览/收藏归 M1（WBS-05-18），本二级不做；序 34–40 报价划掉；41–47 归 ENT 二级
- metric_id 全 N/A（配置写侧无统计数字），待 `TS-L2-M10-LAYER-METRIC` 复核
- probe：API 型真探测；DB 表型 501

## 偏离说明

无。范围与存量调研（对照文档 A 段）一致。

## 产物清单

- 新增：`agent-handoffs/科技发展态势-TS/sdd/l2/TS-L2-M10-LAYER-ARCH.md`（含调用链 + 数据流两张 Mermaid，图 ID `TS-L2-M10-LAYER-ARCH-SEQ` / `-DATA`）
- WBS：`工程过程/04-系统集成/05-展示系统集成/WBS.md` §4.1e 行状态更新

## 架构合规自检

| 铁律 | 状态 |
|---|---|
| 调用链 前端→display→领域服务→Python `/internal/*`（写） | ✅ §3 裁定后合规链路，两图已改 |
| D3 Java 仅读 ADS（字面） | ⚠️ 配置表非 ADS，沿政策 gapfill 只读先例由领域服务直读——会签点 §7 ③ 确认口径 |
| D7 写数归 Python | ✅ **写库全归 Python**（DDL+种子归灌数单，运行时写经 internal），监管人 2026-11-06 裁定 |
| D12 无 demo 依赖 | ✅ |
| D15 display 不直连 Python/DB | ✅ 裁定改写后合规（原稿 bff→db 直连违规，已改 Feign 链路） |
| D18 可实现（表名/灌数方/读接口齐备，接口不返回 mock） | ✅ §2 逐叶三要素 |
| 指标不新造 | ✅ 全 N/A 待 METRIC 复核 |

## cost

- actual_tokens: ~60k（会话累计，含调研）
- model_used: glm-5.3（ZCode agent）
- actual_cost: <$1
- cost_warn: green
