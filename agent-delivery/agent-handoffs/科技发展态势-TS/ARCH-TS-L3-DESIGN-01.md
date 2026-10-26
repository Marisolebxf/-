# 科技发展态势（TS）L3 领域服务 技术架构设计说明书

| 项 | 内容 |
|---|---|
| **文档 ID** | `ARCH-TS-L3-DESIGN-01` |
| **版本** | v0.1（设计稿，待架构裁决） |
| **状态** | `draft` |
| **范围** | 科技发展态势模块（TS，M1–M9 共 9 页）Java 侧 L3 领域服务 |
| **起草** | `agent:architect-agent` |
| **裁决人** | `human:徐腾强 @qike366.com`（架构师，D15 落地人） |
| **知会** | `李伟`（契约监管）· `孔东`（前端路径）· `堂绍祖`（Python 门面） |
| **仓** | `gkx-orchestration`（架构真源，不落业务代码） |
| **配套文档** | `ARCH-TS-L3-01.md`（决策摘要单，一页签字用）· `API-TS-M1.md`~`M9.md`（接口契约）· `TS-聚合方案-产业铺底.md`（数据方案）· `BE-TS-CONTRACT-01.md`（契约交接） |

**修订记录**

| 版本 | 日期 | 变更 | 作者 |
|---|---|---|---|
| v0.1 | 2026-10-25 | 初稿：L3 服务划分、数据接入策略、供方通道抽象 | `agent:architect-agent` |

---

## 1. 概述

### 1.1 背景

科技发展态势（TS）是科技信息展示系统 7 大模块之一，含 9 个页面（M1 科技全域态势 / M2 技术全景 / M3 发展跟踪 / M4 全球 / M5 湾区 / M6 深圳 / M7 科技创新评估 / M8 科技指数 / M9 发展规划）。

前端 9 页已复刻完成（mock 态点测全通），接口契约 `API-TS-M1.md`~`M9.md` 已出草案，但 **Java 侧尚无对应的领域服务**——L3 层没有 `gkxlumen-element` 模块、没有 `/element/**` 或 `/display/v1/trend/**` 路由、网关未配、ADS 表未建。本文即为此缺口给出可落地的架构设计。

### 1.2 范围

**本文覆盖**：

- TS 在 L3 层的服务划分与服务边界
- 服务内部模块/包结构与核心类型设计
- 数据架构（数据源、数据模型、DDL、数据流）
- 供方接入的通道抽象（久新 API / 久新库 / 我方 ADS 混合编排）
- 对外接口设计与降级规范
- 与 L2 `gkxlumen-display` 的协作契约
- 部署配置、演进路线、测试策略

**本文不覆盖**：

- 前端实现（见 `FE-TS-*` 系列交接单）
- Python 算法与 ETL 内部实现（见 `lumen-algo-py` / `gkx_show_service` 各自文档）
- 具体 SQL 调优与索引设计的最终定稿（DDL 给出初版，随数据量演进）

### 1.3 目标与非目标

| 目标 | 说明 |
|---|---|
| **G1 边界清晰** | TS 的领域逻辑收敛到单一服务，不与 `gkxlumen-innov`（创新监测）互相渗透 |
| **G2 供方无关** | 久新提供 API 还是库、未来是否切换，都不改动业务代码 |
| **G3 合规** | 满足 D3（Java 只读 ADS）、D12（不调 demo）、D15（三重隔离） |
| **G4 可演进** | 现在不拆服务，但拆分路径与触发条件预先定义 |
| **G5 快** | 跨维度聚合在同进程完成，避免 Feign 往返放大延迟 |

| 非目标 | 说明 |
|---|---|
| 不做通用查询引擎 | 不实现 DSL、规则引擎、联邦 SQL |
| 不承接算法职责 | 指标计算、影响力评估归 Python（D2/D15） |
| 不写 ADS | Java 侧对 ADS 只读（D3） |

### 1.4 术语表

| 术语 | 含义 |
|---|---|
| **TS** | 科技发展态势模块（Technology Situation），M1–M9 共 9 页 |
| **维度** | 业务视角的分类：企业 / 产业链 / 服务机构 / 政策 / 科研机构 / 人才 / 技术 / 综合服务 |
| **要素** | `API-TS-M1.md` §2 定义的 11 类对象类型，比维度更细 |
| **供方** | 数据提供方：智树自建 / 久新 / 燕大 / 智谱 / 深势 |
| **通道（Channel）** | 数据获取途径的实现：HTTP API / 直连库 / 本地 ADS |
| **片段（Fragment）** | 一次查询中的最小数据来源单元 |
| **装配器（Assembler）** | 声明一次查询需要哪些片段、如何拼装的组件 |
| **能力键（capabilityKey）** | 片段的唯一标识，用于路由到具体通道 |
| **分区降级** | 聚合接口中某个下游失败时，仅该分区置空并给出原因，不影响其他分区 |

---

## 2. 现状与约束

### 2.1 系统现状盘点

| 层 | 服务/组件 | 端口 | 现状 |
|---|---|---|---|
| L0 | `lumen-ui-science-pc` | — | TS 9 页完成，mock 态 |
| L1 | `gkxlumen-gateway` | 9999 | 已建；`/display/**` 路由**未配** |
| L2 | `gkxlumen-display` | 7099 | 骨架已建（`DomainHealthAggregator` + 3 个 Feign），业务端点未填 |
| L3 | `gkxlumen-innov` | 7090 | 实线，7 个 Controller；⚠️ `InnovSql` 指向 demo 库 |
| L3 | `gkxlumen-metrics` | 7091 | `/metrics/v1/catalog` 可用 |
| L3 | `gkxlumen-topic-*` | 7080/7081 等 | 专题侧，实线 |
| L3 | **TS 域** | **7082（拟）** | ❌ **不存在** |
| L4 | `gkx_show_service` | 8082 | 骨架，仅 `/healthz`，`data_source: none` |
| L5 | `lumen-algo-py` | 8000/8001 | 已建；❌ TS 专用算法为 0 |
| L6 | MySQL ADS | 3306 | ❌ `ts_*` 表未建 |

**端口分配结论**：`7082` 当前空闲（已占用为 7080/7081/7090~7099），建议 `gkxlumen-element` 使用 **7082**。

### 2.2 架构基线约束（逐条 + 对本设计的影响）

| 条款 | 原文摘要 | 对本设计的约束 |
|---|---|---|
| **D1** | 统一 `gkxlumen-topic` 提供 `/topic/v1/{element}/*`，两前端共享；展示页面级拼装走薄 BFF `gkxlumen-display`；M1 阶段 innov 仍直接服务展示 | 展示系统的页面拼装在 display；但 `/topic` 实际为空壳 |
| **D2** | 算法库统一出口 | Java 不承接算法 |
| **D3** | **Java 业务 API 仅读 `*_ads`**（+ `app_user` 读写）；**禁扫 ODS/DWD**；禁 Java 写 ADS | ① 主体读 ADS 合规；② **直连久新库属违规，需豁免** |
| **D4** | 收藏/标签带写面，落服务端 | 需建收藏/标签表 |
| **D5** | 网关路由划分：`/display/**`（展示 BFF）· `/topic/**` · `/innov/**` · `/metrics/**` | 路径前缀须为 `/display/v1/**` |
| **D7** | 三方源经数据工厂 `ODS→DWD→ADS` 接入，**不传导到契约面**、上层零改动 | 久新直连须可切回 ADS 且不改上层 |
| **D9** | 算法输出带 `metric_id` 映射，指标注册于 `/metrics/v1/catalog` | 指标元数据复用 metrics 服务 |
| **D12** | **lumen 不调 demo** | 不得复刻 `InnovSql` 的 `demo_gkxlumenx_ads` 映射 |
| **D15** | 展示 BFF `gkxlumen-display`（`/display/v1/**` 单入口）→ Feign 并行 → 领域服务 → Feign `/internal` → 算法层；**展示 BFF 不直连 Python / DB**；领域服务 Feign 调 Python 是合规路径 | ① display 不碰 DB；② element 作为领域服务可直读 ADS / 直调供方 |

**`gkxlumen-display/application.yml` 注释（第 20–26 行）已明确本设计的边界**：

```
# 前端 /api/display/v1/** -> 网关 /display/** StripPrefix=1 -> 本服务 /v1/**
# 职责：页面级 Feign 并行聚合 innov/topic/metrics 域服务 + 读缓存 + 分区降级 + D9 就绪度注入。
# 职责边界：只读。不直连业务库、不写算法、不做指标计算。
# 三方维度（久新 / 燕大 KG / 智谱 / 深势）由 innov/topic 域服务直调，不经过本服务二次转发。
```

最后一行直接支撑了本设计的判断：**久新等三方供方由 L3 领域服务直调，display 不转发。**

### 2.3 现状缺口

| # | 缺口 | 影响 |
|---|---|---|
| 1 | 无 TS 领域服务模块 | 全部需新建 |
| 2 | `ts_*` 表未建（全仓 0 命中，无 `db/9x_gkxlumenx_element.sql`） | 无数据面 |
| 3 | 网关 `/display/**` 路由未配 | 前端无法访问 |
| 4 | `gkx_show_service` 仅 `/healthz` | 自建维度门面不可用 |
| 5 | 久新责任人未落（`TS-聚合方案 §2` 中 10 行均为「久新-？」） | **最大外部阻塞** |
| 6 | `metric_id` 清单未登记（U6） | D9 ⓘ 角标无法对接 |
| 7 | `lumen-algo-py` 零 TS 算法 | 依赖算法的接口只能占位 |
| 8 | `InnovSql` 指向 demo 库（违反 D12） | 新域不得复制；另需整改单 |

---

## 3. 架构总览

### 3.1 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│ L0  前端 lumen-ui-science-pc（34 页，TS 9 页）                 │
│     唯一出口：/api/display/v1/**                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ L1  网关 gkxlumen-gateway :9999                              │
│     /display/** → StripPrefix=1 → lb://gkxlumen-display      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ L2  展示聚合 BFF  gkxlumen-display :7099   /v1/**            │
│     页面区块级接口 · Feign 并行 · Redis 缓存 · 分区降级        │
│     · D9 就绪度注入                                           │
│     ⛔ 不直连 Python / DB                                     │
└─────────────────────────────────────────────────────────────┘
        ↓ Feign 并行          ↓                    ↓
┌───────────────────┐ ┌──────────────┐ ┌──────────────────┐
│ L3 gkxlumen-      │ │ gkxlumen-    │ │ gkxlumen-        │
│    element   :7082│ │ innov :7090  │ │ metrics :7091    │
│    【新建】        │ │ （过渡复用）  │ │ （必复用）        │
│  ┌─────────────┐  │ └──────────────┘ └──────────────────┘
│  │ domain/*    │  │
│  │ 维度聚合     │  │
│  ├─────────────┤  │
│  │ channel/*   │  │
│  │ 供方通道     │  │
│  └─────────────┘  │
└───────────────────┘
        ↓                    ↓                    ↓
┌──────────────┐  ┌────────────────┐  ┌──────────────────┐
│ gkxlumenx_ads│  │ 久新 API / 库   │  │ 燕大KG/智谱/深势  │
│ （只读）      │  │ （只读，需豁免） │  │                  │
└──────────────┘  └────────────────┘  └──────────────────┘
```

### 3.2 调用链（以 M1 地图列表接口为例）

```
前提：筛选项选中「企业」+「科研机构」

前端  GET /api/display/v1/trend/regions?factor_keys=enterprise,institution
  ↓
网关  /display/**  StripPrefix=1
  ↓
display  GET /v1/trend/regions
  ├─ Feign 并行 ─► element  GET /element/v1/regions/objects?factor_keys=enterprise
  │                    └─► domain/enterprise ─► channel/local-ads ─► gkxlumenx_ads
  └─ Feign 并行 ─► element  GET /element/v1/regions/objects?factor_keys=institution
                       └─► domain/institution ─► channel/jiuxin-* ─► 久新 API 或库
  ↓
display 内聚合：object_points[] + heat_points[] + heat_legend
        企业域超时 → 该要素 empty_reason，科研机构点照常返回
  ↓
前端  ← 一个响应（R<Map<String,Object>>）
```

### 3.3 服务职责边界矩阵

| 服务 | 层 | 路由 | 职责 | 禁止 |
|---|---|---|---|---|
| `gkxlumen-display` | L2 | `/display/v1/**` 对外，`/v1/**` 服务内 | 区块级接口；Feign 并行聚合；Redis 缓存；分区降级；D9 注入；导出任务编排 | **不直连 Python/DB**；不写 ADS；不重复造算法调用 |
| **`gkxlumen-element`** | L3 | `/element/v1/**`（`@Inner`，仅内网 Feign） | 维度聚合；**只读 ADS**；供方通道封装；直调三方供方；片段编排 | 算法；写 ADS；扫 ODS/DWD；对外暴露 |
| `gkxlumen-metrics` | L3 | `/metrics/v1/catalog` | 指标元数据（八件套） | — |
| `gkxlumen-innov` | L3 | `/innov/v1/**` | 创新监测、载体、事件、城市指数（过渡） | — |

### 3.4 部署视图

| 组件 | 服务名（Nacos） | 端口 | 副本 | 对外 |
|---|---|---|---|---|
| `gkxlumen-element` | `gkxlumen-element-biz` | 7082 | 2 | ❌ 仅内网 |
| `gkxlumen-display` | `gkxlumen-display-biz` | 7099 | 2 | ✅ 经网关 |

> **注**：`gkxlumen-element` **不配置网关路由**——它只被 `gkxlumen-display` 通过 Feign 内网调用，不对外暴露。这与 D15「展示单入口 `/display/v1/**`」一致。

---

## 4. L3 服务设计：`gkxlumen-element`

### 4.1 服务定义

| 项 | 值 |
|---|---|
| 模块目录 | `lumen-svc-platform/gkxlumen-element` |
| artifactId | `gkxlumen-element-biz`（参照 `gkxlumen-topic-chain-biz` 惯例，**以 pom 实际值为准**） |
| 端口 | 7082 |
| 服务内路由前缀 | `/element/v1/**` |
| 可见性 | `@Inner`，仅注册中心内网可见 |
| 主数据源 | `gkxlumenx_ads`（`@Primary`，`read-only: true`） |
| 第二数据源 | 久新库（`@Qualifier`，`read-only: true`） |
| 写库 | `app_user` 家族（收藏/标签/导出任务）——按 D4 |

### 4.2 职责边界

| 做 | 不做 |
|---|---|
| 维度聚合与片段编排 | 算法计算（影响力、聚类、指数） |
| 只读 `gkxlumenx_ads` 的 `ts_*` 表 | 写 ADS（D3） |
| 封装供方通道（久新/燕大/智谱/深势） | 扫 ODS/DWD |
| 主体键归一化 | 将供方原始键外溢到契约面 |
| 读写 `app_user` 家族（收藏/标签/导出） | 承接 ETL |

### 4.3 模块与包结构

```
gkxlumen-element/
├── pom.xml
├── src/main/java/com/topcomm/gkxlumen/element/
│   ├── GkxlumenElementApplication.java
│   │
│   ├── controller/                      【对外：仅 @Inner，供 display Feign】
│   │   ├── FactorLayerController        /element/v1/layers
│   │   ├── RegionController             /element/v1/regions
│   │   ├── ObjectSearchController       /element/v1/objects/search
│   │   ├── ObjectDetailController       /element/v1/objects/{id}/detail
│   │   ├── EventController              /element/v1/events
│   │   ├── RealtimeController           /element/v1/realtime
│   │   ├── GeneralController            /element/v1/general      （综合服务，横切）
│   │   └── dict/DictController          /element/v1/dict
│   │
│   ├── domain/                          【按业务维度 = 对外语义】
│   │   ├── enterprise/                  企业      ─┐
│   │   ├── chain/                       产业链     │ 智树自建
│   │   ├── service/                     服务机构   │ → local-ads
│   │   ├── policy/                      政策      ─┘
│   │   ├── institution/                 科研机构  ─┐
│   │   ├── talent/                      人才      ├─ 久新 → jiuxin-*
│   │   ├── tech/                        技术      ─┘
│   │   ├── general/                     综合服务（横切编排）
│   │   └── shared/                      跨维度公共（降级、分页、empty_reason）
│   │
│   ├── channel/                         【按供方 = 技术防腐层】
│   │   ├── Fragment                     数据片段（record）
│   │   ├── Channel                      通道接口
│   │   ├── ChannelRegistry              能力表 + resolve()
│   │   ├── ChannelProperties            通道路由配置
│   │   ├── local-ads/                   我方 ADS 通道（包 ElementDao）
│   │   ├── jiuxin-http/                 久新 API 通道
│   │   ├── jiuxin-jdbc/                 久新库通道（**唯一持有久新数据源**）
│   │   ├── JiuxinMapper                 键归一化 + 字段映射
│   │   └── yanda/ zhipu/ shenshi/       （阶段一内联）
│   │
│   ├── support/
│   │   ├── ElementDao                 JdbcTemplate，gkxlumenx_ads 全限定名
│   │   ├── FragmentAssemblerSupport     并行编排 + 降级工具
│   │   └── config/
│   │       ├── PrimaryDataSourceConfig  主库（ADS，@Primary，read-only）
│   │       └── JiuxinDataSourceConfig   久新库（@Qualifier，read-only）
│   │
│   └── api/  dto/  enums/               契约对象
│
├── src/main/resources/
│   ├── application.yml
│   └── bootstrap.yml
└── src/test/java/...                    单测（每个 Assembler 可 mock Channel）
```

### 4.4 包依赖规则（可用 ArchUnit 校验）

| 规则 | 说明 |
|---|---|
| **R1** | `domain/*` 只能依赖 `Channel` 接口与 `domain/shared`，**不得直接注入任何 JdbcTemplate 或 HttpClient** |
| **R2** | 久新数据源**只能**被 `channel/jiuxin-jdbc/` 引用，其他包禁止（C1） |
| **R3** | `channel/*` 不得反向依赖 `domain/*` |
| **R4** | `controller/*` 不得直接调用 `channel/*`，须经 `domain/*` |
| **R5** | 供方原始字段类型不得出现在 `api/` 与 `dto/`，须经 `JiuxinMapper` 归一化 |

R2 是服务可拆分性的保障：将来拆 `gkxlumen-supplier-jiuxin` 时只需搬 `channel/jiuxin-*` 两个包。

### 4.5 核心类型设计

**片段**

```java
public record Fragment(String key, Map<String, Object> data, String emptyReason) {
    public static Fragment of(String key, Map<String, Object> data) {
        return new Fragment(key, data, null);
    }
    public static Fragment empty(String key, String reason) {
        return new Fragment(key, Map.of(), reason);
    }
    public boolean present() { return data != null && !data.isEmpty(); }
}
```

**通道**

```java
public interface Channel {
    String name();
    Fragment fetch(String capabilityKey, Map<String, Object> params);
}
```

**能力注册表**

```java
@Component
public class ChannelRegistry {
    private final Map<String, Channel> channels;   // name → bean
    private final ChannelProperties props;          // capabilityKey → name

    public Channel resolve(String capabilityKey) {
        String name = props.mapping().getOrDefault(capabilityKey, props.defaultChannel());
        Channel c = channels.get(name);
        if (c == null) throw new ChannelMissingException(capabilityKey, name);
        return c;
    }
}
```

**装配器支撑（并行 + 降级）**

```java
@Component
public class FragmentAssemblerSupport {

    public CompletableFuture<Fragment> supply(String capabilityKey,
                                              Map<String, Object> params,
                                              ChannelRegistry registry) {
        return CompletableFuture.supplyAsync(() ->
                registry.resolve(capabilityKey).fetch(capabilityKey, params));
    }

    /** 超时或异常 → 降级为空片段，不向上抛 */
    public Fragment joinOrEmpty(CompletableFuture<Fragment> f, String capabilityKey, String reason) {
        try {
            return f.get(...timeout..., TimeUnit.MILLISECONDS);
        } catch (Exception e) {
            log.warn("fragment degraded: key={}, reason={}", capabilityKey, e.toString());
            return Fragment.empty(capabilityKey, reason);
        }
    }
}
```

> 编排线程池须**独立配置**（不复用 Feign 的默认线程池），避免慢片段耗尽公共线程。

---

## 5. 数据架构

### 5.1 数据源清单

| # | 数据源 | 用途 | 读写 | 装配 |
|---|---|---|---|---|
| 1 | `gkxlumenx_ads` | 主体数据（`ts_*`） | **只读** | `@Primary`，`read-only: true` |
| 2 | 久新库 | 科研机构/人才/技术（阶段一） | **只读** | `@Qualifier("jiuxinDataSource")`，`read-only: true` |
| 3 | `app_user` 家族 | 收藏/标签/导出任务 | 读写 | 独立数据源（如与现有实现共用则延用） |

### 5.2 数据模型

**命名**：全部前缀 `ts_`（Trend/Situation）。SQL 一律写 `gkxlumenx_ads.ts_xxx` 全限定名。

#### 5.2.1 `ts_factor_stat` — 要素统计（按地域 × 时间）

支撑 `API-TS-M1.md` §3.1 要素图层、§3.6 实时监控。

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | bigint PK | |
| `factor_key` | varchar(32) | 要素编码（对齐 §2 枚举） |
| `region_code` | varchar(32) | 地域编码 |
| `stat_date` | date | 统计日期 |
| `granularity` | varchar(16) | 时间粒度（day/month/quarter/year） |
| `object_count` | bigint | 对象数量 |
| `metric_value` | decimal(20,4) | 主指标值 |
| `yoy_growth` | decimal(10,4) | 同比增长 |
| `metric_id` | varchar(64) | 关联指标中心（D9） |
| `updated_at` | datetime | |

索引：`(factor_key, region_code, stat_date)`、`(metric_id)`

#### 5.2.2 `ts_object` — 对象主表（跨要素统一）

支撑 §3.2 地域落点、§3.3 要素检索、§3.4 详情基础信息。

| 字段 | 类型 | 说明 |
|---|---|---|
| `object_id` | varchar(64) PK | **主体统一键**（归一化后，非供方原始键） |
| `object_type` | varchar(32) | 对象类型（11 要素之一） |
| `source` | varchar(32) | 供方：`ztree` / `jiuxin` / … |
| `source_key` | varchar(128) | 供方原始主键（仅用于追溯，不外溢） |
| `name` | varchar(256) | |
| `region_code` | varchar(32) | |
| `lon` / `lat` | decimal(10,6) | 地图落点 |
| `status` | varchar(16) | |
| `updated_at` | datetime | |

索引：`(object_type, region_code)`、`(region_code)`、`(source, source_key)`

#### 5.2.3 `ts_object_metric` — 对象指标

支撑 §3.4 详情的指标区与趋势。

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | bigint PK | |
| `object_id` | varchar(64) | |
| `metric_id` | varchar(64) | 关联 `/metrics/v1/catalog` |
| `stat_date` | date | |
| `value` | decimal(20,4) | |
| `unit` | varchar(32) | |

索引：`(object_id, metric_id, stat_date)`

#### 5.2.4 `ts_event` — 科创事件

支撑 §3.5 事件时间轴。

| 字段 | 类型 | 说明 |
|---|---|---|
| `event_id` | varchar(64) PK | |
| `title` | varchar(512) | |
| `event_type` | varchar(32) | 对齐 §2 事件类型枚举 |
| `importance` | tinyint | 重要性分级（算法产出，阶段一可空） |
| `occur_date` | date | |
| `region_code` | varchar(32) | |
| `summary` | text | |
| `updated_at` | datetime | |

#### 5.2.5 `ts_opinion` — 舆情

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | bigint PK | |
| `event_id` | varchar(64) | 可空（独立舆情） |
| `source` | varchar(64) | ⚠️ 三方源未定（U4） |
| `sentiment` | varchar(16) | |
| `publish_time` | datetime | |
| `content` | text | |

#### 5.2.6 带写面（`app_user` 家族，D4）

| 表 | 用途 |
|---|---|
| `ts_favorite` | 收藏（`user_id`, `object_id`, `object_type`, `created_at`） |
| `ts_tag` | 标签定义（`tag_id`, `user_id`, `name`） |
| `ts_object_tag` | 对象-标签关联 |
| `ts_export_task` | 导出任务（`task_id`, `user_id`, `status`, `file_url`, 审计字段） |

> 导出任务中心的五接口（配置/建任务/状态/取消/下载）见 `API-TS-M1.md` §3.8，对应前端 `ExportFlowPanel` 8 相位。

### 5.3 数据流

```
【写】Python（lumen-algo-py / ETL / 数据工厂）
        ↓ 写
   gkxlumenx_ads.ts_*

【读】display → Feign → element
        ├─ channel/local-ads  → JdbcTemplate → gkxlumenx_ads.ts_*   （只读）
        ├─ channel/jiuxin-http → HTTP → 久新 API                    （只读）
        └─ channel/jiuxin-jdbc → JdbcTemplate → 久新库              （只读，需豁免）

【写】element → app_user 家族（收藏/标签/导出任务，D4）
```

**久新的两阶段演进**

| 阶段 | 通路 | 依据 |
|---|---|---|
| 阶段一（现在） | `domain/*` → `channel/jiuxin-http` 或 `jiuxin-jdbc` → 久新 | D15 §2.2「领域服务直接调久新 API」 |
| 阶段二（数据工厂就绪） | `domain/*` → `channel/local-ads` → `gkxlumenx_ads.ts_*` | D7 + `storage/README.md:87`（ODS 读者为 ETL） |

切换方式：**改 `ChannelProperties.mapping` 配置，domain 与 Assembler 零改动**。

### 5.4 只读约束与事务边界

| 约束 | 实现 |
|---|---|
| ADS 只读 | Hikari `read-only: true`（参照 `gkxlumen-innov/application.yml:27`） |
| 久新库只读 | Hikari `setReadOnly(true)`，`poolName` 显式（参照 `gkxlumen-cms/.../SourceDataSourceConfig.java:66-67`） |
| 事务 | `DataSourceTransactionManagerAutoConfiguration` 按 single-candidate 绑 `@Primary`；**写操作仅针对 `app_user` 数据源**，ADS/久新库不得参与事务 |
| 多数据源装配 | 业务库必须显式建 bean 并标 `@Primary`；注入处 `@Qualifier` **必须显式**（CMS 血泪坑，见 §6.7 C4） |

---

## 6. 供方通道抽象（核心设计）

### 6.1 设计动机

久新侧的供给形态存在三重不确定性：

1. 部分能力提供 **HTTP API**，部分只有 **数据库**；
2. 同一查询可能**既要调 API 又要查库**再拼装；
3. 未来数据工厂就绪后要切回**我方 ADS**。

若按「整个供方二选一」或「整个要素一个通道」建模，任一变化都会穿透到业务代码。因此把路由粒度下沉到**数据片段**。

### 6.2 粒度纠正

```
❌ 供方级：久新 ──► 全部 HTTP   或   全部库
❌ 要素级：institution ──► jdbc（整个要素固定一个通道）
✅ 片段级：一次「科研机构详情」查询
     ├─ jiuxin.institution.base      → jiuxin-jdbc  （久新库，自查询）
     ├─ jiuxin.institution.metrics   → jiuxin-http  （久新已提供 API）
     └─ jiuxin.institution.relation  → local-ads    （我方 ADS）
     三个片段并行/串行获取后在 Assembler 内拼装
```

同一要素在不同查询（列表 / 详情 / 统计）中，片段组合可以不同。

### 6.3 能力键规范

```
格式：<supplier>.<domain>.<fragment>
示例：jiuxin.institution.base
      jiuxin.institution.metrics
      ztree.enterprise.points
      local.ads.object.relation
```

- 全小写、点分三段
- `<supplier>` ∈ {`jiuxin`, `ztree`, `yanda`, `zhipu`, `shenshi`, `local`}
- 能力键须在 `ChannelProperties.mapping` 中登记，未登记走 `default`

### 6.4 编排执行模型

| 场景 | 处理 |
|---|---|
| 片段间无依赖 | `CompletableFuture` 并行，总耗时 ≈ 最慢片段 |
| 片段间有依赖 | 先 `join()` 前驱，把结果写入 `params` 再查后继 |
| 单片段失败/超时 | 降级为 `Fragment.empty(key, reason)`，**其余片段照常返回** |
| 全部片段失败 | 返回空结果 + `empty_reason`，**不得抛 5xx**（延续 `DomainHealthAggregator` 范式） |
| 超时 | 通道级独立配置：HTTP 用 connect/read timeout，JDBC 用 `queryTimeout` |

### 6.5 装配器示例（完整）

```java
@Component
public class InstitutionDetailAssembler {

    private final ChannelRegistry channels;
    private final FragmentAssemblerSupport support;

    public InstitutionDetail assemble(InstitutionQuery q) {
        Map<String, Object> p = q.toParams();

        // 1) 无依赖片段：并行
        CompletableFuture<Fragment> base =
                support.supply("jiuxin.institution.base", p, channels);
        CompletableFuture<Fragment> rel =
                support.supply("jiuxin.institution.relation", p, channels);

        // 2) 有依赖片段：需 base 的归一化主体键作入参
        Fragment baseFrag = support.joinOrEmpty(base, "jiuxin.institution.base", "基础信息服务不可用");
        p.put("objectId", baseFrag.data().get("object_id"));   // ← 已归一化
        CompletableFuture<Fragment> metric =
                support.supply("jiuxin.institution.metrics", p, channels);

        // 3) 拼装（各片段独立降级）
        return InstitutionDetail.builder()
                .base(baseFrag)
                .metric(support.joinOrEmpty(metric, "jiuxin.institution.metrics", "指标服务不可用"))
                .relation(support.joinOrEmpty(rel, "jiuxin.institution.relation", "暂无关联数据"))
                .build();
    }
}
```

**说明**：`p.put("objectId", ...)` 取的是**归一化后的 `object_id`**，不是久新原始键——这是混合拼装正确性的关键（见 §6.7）。

### 6.6 配置规范

```yaml
# nacos: gkxlumen-element-dev.yml
gkxlumen:
  element:
    channels:
      default: local-ads
      mapping:
        # 久新：能力就绪一项登记一项，未定项保持注释
        jiuxin.institution.base:      jiuxin-jdbc
        jiuxin.institution.metrics:   jiuxin-http
        jiuxin.institution.relation:  local-ads
        # jiuxin.talent.profile:      <待久新答复>
        # jiuxin.tech.paper_stats:    <待久新答复>
      timeout-ms:
        jiuxin-http: 3000
        jiuxin-jdbc: 2000
        local-ads:   1500
    jiuxin:
      http:
        base-url: ${JIUXIN_API_BASE_URL:}
        connect-timeout-ms: 3000
        read-timeout-ms: 10000
      jdbc:
        host: ${JIUXIN_MYSQL_HOST:}
        port: ${JIUXIN_MYSQL_PORT:3306}
        db:   ${JIUXIN_MYSQL_DB:}
        username: ${JIUXIN_MYSQL_USER:}
        password: ${JIUXIN_MYSQL_PASSWORD:}   # 走 K8s Secret，不进 git
```

久新改供给形式、或数据工厂就绪：**只改 `mapping`，Java 不动**。

### 6.7 关键设计约束（硬性）

| # | 约束 | 原因 / 证据 |
|---|---|---|
| **C1** | **久新数据源只能由 `channel/jiuxin-jdbc/` 持有**，其余包禁止直接注入 | 多数据源是服务拆分的最大障碍；收敛后可平滑拆出 |
| **C2** | **主体键归一化**：所有片段对外统一为 `object_id`（对齐 §5.2.2），久新原始键仅存 `source_key` 用于追溯，**不得外溢** | 混合拼装最大风险：API 与库主键若不同套，拼装产出错数据**且不报错** |
| **C3** | **SQL 直写 `gkxlumenx_ads.ts_xxx` 全限定名，不复刻 `InnovSql.qualify()`** | `InnovSql.java` 映射到 `demo_gkxlumenx_ads`，而 `gkxlumen-innov/application.yml:19` 要求「正式 2B 改写到 `gkxlumenx_`」——未闭合整改债，违反 D12 |
| **C4** | **双数据源两条坑**：① 业务库必须显式建 bean 并标 `@Primary`（自定义 DataSource 会让自动配置整体 back off）；② 注入处 `@Qualifier` **必须显式** | `gkxlumen-cms/.../SourceDataSourceConfig.java:73` 原文：「`@Primary` 业务库在候选解析中优先于参数名匹配，否则真源池会**静默连到**业务库」 |
| **C5** | **库名/凭证走 Nacos，不硬编码、不进 git** | CMS 注释「正式化：改库名（nacos 一处）」；D14 凭证放 K8s Secret |

### 6.8 复杂度边界（明确不做）

| 做 | 不做 |
|---|---|
| 片段 = 一次方法调用 | ❌ DSL / 规则引擎 |
| 编排 = 手写 Java，一个 Assembler 一个方法 | ❌ 配置驱动的通用编排 |
| 仅「片段 → 通道」映射可配置 | ❌ 通用联邦 SQL 引擎 |
| 每个 Assembler 可单测（mock Channel） | ❌ 追求一次抽象吃下所有场景 |

理由：展示系统查询形态有限（统计 / 落点 / 检索 / 详情 / 导出），手写编排的可读性与可测性远优于通用引擎。

---

## 7. 接口设计

### 7.1 接口总览（`@Inner`，供 display Feign 调用）

| # | 接口 | 对应契约 | 维度 |
|---|---|---|---|
| 1 | `GET /element/v1/layers` | §3.1 要素图层 | 多要素并行 |
| 2 | `GET /element/v1/regions` | §3.2 地域与对象落点 | 多要素并行 |
| 3 | `GET /element/v1/objects/search` | §3.3 要素检索 | 按 `object_type` 路由 |
| 4 | `GET /element/v1/objects/{id}/detail` | §3.4 详情（四 kind） | 片段编排 |
| 5 | `GET /element/v1/events` | §3.5 事件 | 事件 + 舆情 |
| 6 | `GET /element/v1/realtime` | §3.6 实时监控 | 数量/占比/增长 |
| 7 | `GET/POST /element/v1/general` | 综合服务（横切） | 跨维度编排 |
| 8 | `POST/DELETE /element/v1/favorites` · `/tags` | §3.7 收藏/标签（**写**） | `app_user` |
| 9 | `/element/v1/export/*` | §3.8 导出任务中心（**写**） | `app_user` |

### 7.2 通用规范

| 项 | 规范 |
|---|---|
| 注解 | `@RestController` + `@RequestMapping("/element/v1")` + `@Inner(value = false)` + `@Tag` + `@Operation`（参照 `gkxlumen-topic-chain` 的 `IndustryFacadeController`） |
| 包络 | `R<T>`：`R.ok(data)` / `R.failed(msg)`（`common-core/util/R.java`） |
| 分页 | 统一 `page` / `size`，返回 `{items, total, page, size}` |
| 异常 | 交由 `GlobalBizExceptionHandler`（已处理 `Exception` / `SQLException` / `FeignException`） |
| 空结果 | **不抛异常**，返回空集合 + `empty_reason` |

### 7.3 关键接口契约（示意，最终以 `API-TS-M1.md` 为准）

`GET /element/v1/regions`

```jsonc
// 请求
{ "factor_keys": ["enterprise","institution"], "region_scope": "shenzhen" }

// 响应
{
  "object_points": [
    { "object_id":"...", "object_type":"enterprise", "name":"...", "lon":114.05, "lat":22.54 }
  ],
  "degraded": [
    { "factor_key":"institution", "empty_reason":"科研机构服务不可用" }
  ]
}
```

### 7.4 降级与 `empty_reason` 规范

| 场景 | `empty_reason` |
|---|---|
| 通道超时 | `"XX 服务响应超时"` |
| 通道抛异常 | `"XX 服务不可用"` |
| 数据未就绪（阶段一） | `"XX 数据接入中"` |
| 查询无结果 | `"暂无数据"` |

**原则**：**任一分区失败不放大为 5xx**——这是 `DomainHealthAggregator` 已固化的范式，本服务须沿用。

### 7.5 错误码

沿用 `common-core` 既有错误码体系，不新增私有码；业务异常用 `R.failed(msg)` 表述。

---

## 8. 与 L2 `gkxlumen-display` 的协作

### 8.1 display 定位（易误解，特此明确）

> display 不是「一个页面一个接口」，而是**前端请求的唯一入口，一个页面拆成多个接口**。

**粒度判据**：UI 上需要独立 loading / 空态 / 错误态的，就是独立接口。
**理由**：避免单个慢接口拖垮整页。
**接口内**：可跨多个域服务并行聚合（横向），但不得把多个区块合并成一个大响应（纵向）。

### 8.2 区块级接口清单（M1 示例）

| 接口 | 区块 | 跨域聚合 |
|---|---|---|
| `/v1/trend/layers` | 11 要素 chips + 统计 | 各要素 count 并行 |
| `/v1/trend/regions` | 地图 + 落点 + 热力 | **多要素并行**（§3.2 示例） |
| `/v1/trend/objects/search` | 检索列表 | 多要素合并 + 统一分页排序 |
| `/v1/trend/objects/{id}/detail` | 详情抽屉 | 四 kind 统一契约 |
| `/v1/trend/events` | 事件时间轴 | 事件 + 舆情 |
| `/v1/trend/realtime` | 实时监控 KPI | 30s 轮询，天然独立 |

### 8.3 并行聚合与分区降级

沿用 `DomainHealthAggregator`：`CompletableFuture` + `orTimeout` + `exceptionally`，单下游失败仅该分区置空。

### 8.4 超时预算

| 层 | 建议 | 说明 |
|---|---|---|
| display → element | 按接口类型可配：地图类 3s / KPI 类 1s / 导出类单独 | 建议纳入 Nacos，替代现有 `TIMEOUT_MS = 2000` 固定值 |
| element → channel | 见 §6.6 `timeout-ms` | 通道级独立 |
| 网关 | `response-timeout: 30000`（沿用现网路由配置） | |

---

## 9. 关键机制设计

### 9.1 并行编排

- 使用**独立线程池**（`element-assembler`），不复用 Feign 默认池
- 队列容量与拒绝策略显式配置，拒绝时降级为 `empty_reason` 而非抛异常

### 9.2 分区降级

- 每个片段独立 `joinOrEmpty`
- 结果中携带 `degraded[]` 数组，前端可据 `empty_reason` 展示差异化空态

### 9.3 缓存策略

| 层 | 策略 |
|---|---|
| display | Redis 缓存（D15 指定职责） |
| element | 阶段一不引入缓存（数据在 ADS，查询快）；阶段二若久新通道延迟高，在 `channel/jiuxin-*` 内做**通道级短 TTL 缓存**，对 domain 透明 |

### 9.4 D9 就绪度注入

- `metric_id` 由 `/metrics/v1/catalog` 提供（复用 `gkxlumen-metrics`）
- element 只返回 `metric_id`，**就绪度判定与 ⓘ 注入在 display 完成**（D15 指定）
- ⚠️ 阻塞：`metric_id` 清单（U6）未登记

### 9.5 导出任务中心（带写面）

- 五接口（配置/建任务/状态/取消/下载），见 `API-TS-M1.md` §3.8
- 写 `app_user` 家族；审计字段落服务端
- 文件产出走对象存储（D14：桶 `gkx-lumen`，用途为目录），**禁止前端直连对象存储**

---

## 10. 非功能设计

### 10.1 性能

| 项 | 设计 |
|---|---|
| 地图落点数据量 | ⚠️ **需早期验证**：若单地域对象点达数万级，须在 SQL 层聚合或按视野分页，不可全量透传 |
| N+1 | 禁止：对象列表与指标须批量查询（`ts_object_metric` 按 `object_id IN (...)`） |
| 慢查询 | 所有 ADS 查询设 `queryTimeout` |

### 10.2 可观测

| 项 | 设计 |
|---|---|
| 日志 | 片段降级必须 `warn` 并带 `capabilityKey` 与耗时 |
| 链路 | JavaAgent 全 OTLP（沿用仓内既有做法） |
| 埋点 | 前端 `observability.ts` 已建，后端补充片段级耗时 |

### 10.3 安全与凭证

| 项 | 设计 |
|---|---|
| 凭证 | 久新账号/库口令走 K8s Secret 或 Nacos，**不进 git**（D14） |
| 只读 | 所有外部数据源 `readOnly = true` |
| 接口可见性 | element 全部 `@Inner`，不对外暴露 |

### 10.4 容量

| 项 | 评估 |
|---|---|
| `ts_object` | 按 11 要素 × 各要素对象量估算，需数据侧给出量级后定索引与分区 |
| 副本 | 2（无状态，可水平扩） |

---

## 11. 部署与配置

### 11.1 服务注册与端口

| 服务名 | 端口 | 注册 |
|---|---|---|
| `gkxlumen-element-biz` | 7082 | Nacos（内网） |

### 11.2 数据源配置

```yaml
spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://${SITUATION_MYSQL_HOST:10.50.11.76}:${SITUATION_MYSQL_PORT:3306}/${SITUATION_MYSQL_DB:gkxlumenx_ads}?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true
    username: ${SITUATION_MYSQL_USER:gkxlumenx}
    password: ${SITUATION_MYSQL_PASSWORD}
    hikari:
      maximum-pool-size: 10
      read-only: true          # D3：Java 对 ADS 只读
```

久新库第二数据源按 §5.4 与 C4/C5 装配（`readOnly=true`、`poolName` 显式、`@Qualifier` 显式）。

### 11.3 Nacos 配置清单

| 配置 | 内容 |
|---|---|
| `gkxlumen-element-dev.yml` | 数据源、通道映射、超时、供方凭证引用 |
| Helm 种子 | `helm/gkxlumen-platform/configs/gkxlumen-element-dev.yml`（参照 display 既有文件） |

### 11.4 网关路由

**`gkxlumen-element` 不配网关路由**（仅内网 Feign）。需新增的是 **`/display/**`** 路由（当前未配）：

```sql
-- db/9x_gkxlumenx_sys_route_conf_display.sql
-- /display/** → lb://gkxlumen-display-biz
-- ⚠️ GlobalFilter 已剥第一段，禁止再配 StripPrefix（对齐 topic_chain 路由约定）
INSERT INTO `sys_route_conf` (...)
SELECT ...
  'gkxlumen-display-biz',
  CAST('[{"args": {"_genkey_0": "/display/**"}, "name": "Path"}]' AS JSON),
  CAST('[{"args": {"key-resolver": "#{@remoteAddrKeyResolver}", "redis-rate-limiter.burstCapacity": "100000", "redis-rate-limiter.replenishRate": "10000"}, "name": "RequestRateLimiter"}]' AS JSON),
  'lb://gkxlumen-display-biz',
  0,
  CAST('{"cors": {...}, "response-timeout": 30000}' AS JSON),
  'agent:api-agent', '0'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM `sys_route_conf` WHERE `route_id` = 'gkxlumen-display-biz' AND `del_flag` = '0');
```

### 11.5 DDL 文件

新建 `db/9x_gkxlumenx_element.sql`（命名惯例对齐 `9x_gkxlumenx_cms.sql` / `9x_gkxlumenx_topic_enterprise.sql`），含 §5.2 全部表。

---

## 12. 演进路线

### 12.1 阶段划分

| 阶段 | 内容 |
|---|---|
| **W1** | 模块骨架 + 双数据源 + `ts_*` DDL + `domain/enterprise` 全链路 + display 聚合端点 → 跑通 FE→gateway→display→element→ADS 闭环 |
| **W2** | 铺开 `chain` / `service` / `policy`（纯 ADS，无外部依赖） |
| **W3** | `channel/jiuxin-*` 填实现（依赖久新答复） |
| **W4** | `domain/general` 综合服务（依赖需求定义） |
| **W5** | 收藏/标签 + 导出任务中心（带写面） |

### 12.2 服务拆分触发条件

| 触发 | 动作 |
|---|---|
| 专题系统也要调久新 | `channel/jiuxin-*` 拆为 `gkxlumen-supplier-jiuxin`（判据③：消费方 ≥2） |
| 某 domain 包膨胀 / 需独立发布 | 该包拆为独立模块 → 服务（R1–R5 已预留边界） |
| 燕大/智谱/深势 被 ≥2 服务调用 | 对应通道独立成服务 |

### 12.3 与 `gkxlumen-topic-*` 的关系

- **当前**：不复用（数据形态不同 + D15 三重隔离）
- **未来**：若 `/topic/v1` 演进为两系统真正共享的要素聚合核心（D1 原意、但当前为空壳），可评估将 `domain/enterprise` 等下沉复用
- **本文立场**：现在不复用，但**不排斥未来复用**，接口设计保持与 `/topic` 语义对齐以降低未来切换成本

---

## 13. 测试策略

| 层 | 策略 |
|---|---|
| Assembler 单测 | mock `Channel`，验证：并行、依赖顺序、单片段降级、全片段降级 |
| Channel 单测 | `jiuxin-http` 用 WireMock；`jiuxin-jdbc` 用 H2 或 Testcontainers |
| Controller 单测 | 参照 `gkxlumen-topic-chain` 既有单测写法 |
| 契约测试 | 与 `API-TS-M1.md` 字段逐项比对 |
| 联调 | 前端 `USE_MOCK=false` 打通 M1 全链路 |

---

## 14. 风险与开放问题

| # | 风险 | 影响 | 缓解 |
|---|---|---|---|
| **R1** | **久新主体键与库主键不同套** | 混合拼装产出错数据**且不报错** | C2 归一化；**答复前不出实现，只出桩** |
| **R2** | 久新责任人未落 | 通道清单无法确定 | 同步催办（§15 A5） |
| **R3** | 单服务承载 8 维度 + 3 数据源 | 膨胀后难拆 | C1 + R1–R5 包依赖规则 |
| **R4** | 地图落点数据量未知 | 传输与渲染性能 | 早期压测（§10.1） |
| **R5** | `metric_id` 未登记 | D9 ⓘ 无法对接 | 随 W1 一并登记 |
| **R6** | 直连久新库违反 D3/D7 | 验收被拦 | §15 A2 必须登记豁免 |

---

## 15. 待裁决项（请徐腾强签署）

| # | 议题 | 选项 | **建议** | 依据 | 不裁决后果 |
|---|---|---|---|---|---|
| **A1** | TS 的 L3 归属 | (a) 新建 `gkxlumen-element`<br>(b) 复用 `gkxlumen-topic-*`<br>(c) 落 `gkxlumen-innov` | **(a)** | §3.4；⚠️ 偏离基线 §4 `prefer_reuse: [/topic/v1]` | 决定代码落哪个模块，选错整体返工 |
| **A2** | 直连久新库是否准予 D3/D7 过渡豁免 | (a) 准予并登记<br>(b) 不准，须先经数据工厂 | **(a)** + 登记切换条件 | D3 / D7 / `storage/README.md:87`；先例 `gkxlumen-cms` | 违规风险，验收被拦 |
| **A3** | 路径前缀 | (a) `/display/v1/trend/**`<br>(b) 新增 `/element/**` | **(a)** | D5 / D15；前端 `src/api/situation/*.ts` 改一层即可 | 决定 `@RequestMapping` 与网关路由 |
| **A4** | 智树 4 维度读法 | (a) 先直读 ADS，门面就绪后内部切换<br>(b) 必须走 `gkx_show_service` | **(a)** | D3；`gkxlumen-innov/application.yml:19-27`；门面当前仅 `/healthz` | 选 (b) 则 Java 阻塞于 Python 工期 |
| **A5** | 久新主体键对齐——**谁去问、何时答复** | 指定责任人 + 时限 | 与久新接口清单一并催办；答复前只出桩 | §14 R1；`TS-聚合方案 §2`「久新-？」未落人 | 拼装正确性无保证 |
| **A6** | 「综合服务」维度定义 | 产品/需求给出聚合范围与结构 | 暂缓 `domain/general/` | §3.1 | 该包返工 |

**知会事项（非裁决，影响排期）**

- `InnovSql` 指向 demo 库（违反 D12）→ 建议单开整改单，新域不复制（C3）
- `lumen-algo-py` 零 TS 算法 → 并行排期
- `metric_id` 清单（U6）未登记 → D9 暂无法对接

---

## 16. 附录：证据索引

| # | 文件 | 关键位置 |
|---|---|---|
| 1 | `architecture-baseline.md` | D1 / D2 / D3 / D4 / D5 / D7 / D9 / D12 / D15 / §2.2 / §4 |
| 2 | `data/data-design/storage/README.md` | `:40` Java 只读 ADS；`:87` ODS 读者为 ETL；`:89` ADS 契约面 Java 只读 |
| 3 | `repos/lumen-svc-platform/gkxlumen-display/src/main/resources/application.yml` | `:20-26` 职责边界与调用链铁律；`:2` 端口 7099 |
| 4 | `repos/lumen-svc-platform/gkxlumen-display/.../service/DomainHealthAggregator.java` | Feign 并行 + 分区降级范式 |
| 5 | `repos/lumen-svc-platform/gkxlumen-innov/src/main/resources/application.yml` | `:19-27` JDBC `gkxlumenx_ads` + `read-only`；`:29-35` 算法走 Feign |
| 6 | `repos/lumen-svc-platform/gkxlumen-innov/.../support/InnovSql.java` | demo 库映射债（违反 D12） |
| 7 | `repos/lumen-svc-platform/gkxlumen-cms/.../overlay/SourceDataSourceConfig.java` | `:16-25` 双数据源说明；`:29-49` `@Primary`；`:51-75` 只读真源 + `@Qualifier` |
| 8 | `repos/lumen-svc-platform/db/9x_gkxlumenx_sys_route_conf_topic_chain.sql` | 路由 SQL 格式；**禁止再配 StripPrefix** |
| 9 | `repos/lumen-svc-platform/db/` | DDL 命名惯例 `9x_gkxlumenx_<x>.sql` |
| 10 | `repos/lumen-svc-platform/helm/gkxlumen-platform/values.yaml` | 端口占用清单（7080/7081/7090-7099，**7082 空闲**） |
| 11 | `repos/lumen-topic-py/gkx_show_service/main.py` | 当前仅 `/healthz`，`data_source: none` |
| 12 | `agent-handoffs/科技发展态势-TS/TS-聚合方案-产业铺底.md` | §1.3 现成表；§2 久新要素与责任人 |
| 13 | `agent-handoffs/科技发展态势-TS/API-TS-M1.md` | §1.1 U1–U8；§3.1–§3.8 八类接口 |
| 14 | `repos/lumen-ui-science-pc/src/api/situation/index.ts` | 前端当前写死 `/situation/v1/**`，待改为 `/display/v1/trend/**`（A3/A4） |

---

**签署栏**

| 角色 | 姓名 | 裁决（A1–A6） | 日期 |
|---|---|---|---|
| 架构师 | 徐腾强 @qike366.com | | |
| 契约监管 | 李伟 | | |
| 前端 | 孔东（A3） | | |
| Python 门面 | 堂绍祖（A4） | | |
