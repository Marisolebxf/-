# ARCH-TS-L3-01 交接（科技发展态势 · L3 领域服务划分与数据接入架构）

- **task-id**：`ARCH-TS-L3-01`
- **状态**：`draft`（**待架构裁决**；本文为报批稿，非生效基线）
- **执行**：`agent:architect-agent`
- **裁决人**：`human:徐腾强 @qike366.com`（架构师，D15 落地人）
- **知会**：`human:李伟`（契约监管）、`孔东`（前端路径对齐）、`堂绍祖`（Python 门面）
- **仓**：`gkx-orchestration`（架构真源，不落业务代码）
- **上游**：`BE-TS-CONTRACT-01.md`（U1–U8）· `API-TS-M1.md` ~ `M9.md` · `TS-聚合方案-产业铺底.md` §1.3 · `TS-模块开发规划与任务拆分.md` §5
- **下游**：`BE-TS-IMPL-01`（Java 实现）、`FE-TS-S01`（前端路径对齐）、`DEVOPS-LUMEN-TOPIC-PY-SHOW-L01`（L4 门面）
- **关联基线条款**：D1 · D3 · D5 · D7 · D9 · D12 · D15 · §2.2 要素归属 · §4 依赖规则

> **本文用途**：科技发展态势（TS，M1–M9 共 9 页）在 Java 侧**尚无领域服务**。本文给出 L3 层服务划分、数据接入策略与久新供方的通道抽象，并列出 **6 项需架构裁决**的议题（§7）。**裁决前不动工**；其中不依赖裁决的部分已在 §8 标注，可先行。

---

## 1. 结论摘要

| 议题 | 结论 |
|---|---|
| **L3 服务数量** | **新建 1 个** `gkxlumen-element`，内部按「维度分包 + 供方通道分包」，不按维度拆 8 个服务 |
| **为什么是 1 个** | 展示系统的跨维度聚合是常态（如地图列表接口同时要「企业 + 科研机构」）。同进程聚合是本地方法调用；跨服务则退化为 Feign + 超时 + 降级 + 序列化，**慢一个数量级且降级逻辑要写 8 遍** |
| **数据读取** | 智树自建 4 维度 → **Java 直读 `gkxlumenx_ads`**；久新 3 维度 → **通道抽象，API / 库 / ADS 三种实现配置切换** |
| **久新接入** | 不做「整个供方二选一」，做**片段级混合编排**：一次查询内可部分走久新 API、部分走久新库、部分走我方 ADS，再拼装 |
| **现有资产** | 必复用 `gkxlumen-metrics`；过渡复用 `gkxlumen-innov`；**不复用** `gkxlumen-topic-*` 四服务（⚠️ 此项偏离基线 §4，需裁决，见 A1） |

---

## 2. 架构总览

### 2.1 调用链（对齐 D15 三层）

```
终端 → gkxlumen-gateway
     → gkxlumen-display        （L2 展示聚合 BFF，/display/v1/** 单入口）
       └─ Feign 并行 + 分区降级
          ├─ gkxlumen-element 【新建】科技发展态势域
          │    ├─ domain/*          → 维度聚合（编排）
          │    └─ channel/*         → 供方通道（local-ads / jiuxin-http / jiuxin-jdbc）
          ├─ gkxlumen-innov         创新监测、载体、事件（过渡复用）
          └─ gkxlumen-metrics       指标 ⓘ 八件套（必复用）
```

### 2.2 分层职责（本次涉及的 L2 / L3）

| 层 | 服务 | 职责 | 禁止 |
|---|---|---|---|
| **L2** | `gkxlumen-display` | 展示系统**唯一入口**；接口粒度 = **页面区块**（非整页）；接口内跨域并行聚合；Redis 缓存；**分区降级**；D9 就绪度注入 | **不直连 Python / DB**（D15 明文） |
| **L3** | `gkxlumen-element`【新建】 | 维度聚合；**只读 ADS**；供方通道封装；直调三方供方 | 算法、写 ADS、扫 ODS/DWD |

**L2 定位澄清**（易误解，特此写明）：

> display 不是「一个页面一个接口」，而是「前端所有请求都走它，一个页面拆成多个接口」。
> 判断粒度：**UI 上需要独立 loading / 空态 / 错误态的，就是独立接口**。
> 单个接口内部可横向聚合多个维度，但不得把多个区块合并成一个大响应——避免一个慢接口拖垮整页。

---

## 3. L3 服务划分方案

### 3.1 维度 × 供方 × 通道映射

| 维度 | 供方 | 数据来源 | 通道 |
|---|---|---|---|
| 企业 | 智树自建 | ADS（`enterprise_industry_summary` 等现成表） | `local-ads` |
| 产业链 | 智树自建 | ADS | `local-ads` |
| 服务机构 | 智树自建 | ADS（`svc_metric_dist` 等现成表） | `local-ads` |
| 政策 | 智树自建 | ADS | `local-ads` |
| 科研机构 | **久新** | 待定（API / 库） | `jiuxin-*` |
| 人才 | **久新** | 待定（API / 库） | `jiuxin-*` |
| 技术 | **久新** | 待定（API / 库） | `jiuxin-*` |
| 综合服务 | — | **横切查询**（跨上述维度） | 服务内编排 |

### 3.2 三条划分判据

| # | 判据 | 结论指向 |
|---|---|---|
| ① | **跨维度聚合的频率** | 聚合越频繁越该同进程 → 合并为 1 个服务 |
| ② | **供方对接的集中度** | 同一供方只应有一处对接（凭证/限流/重试/容错收敛）→ `channel/` 按供方分包 |
| ③ | **消费方数量** | 被 ≥2 个系统消费的能力才值得独立成服务 → 久新暂不独立出服务 |

### 3.3 目录结构

```
gkxlumen-element     （JDBC 主库 gkxlumenx_ads @Primary read-only；久新库 第二数据源 read-only）
│
├─ domain/                     【按业务维度 = 对外语义】
│    enterprise/  chain/  service/  policy/      → ElementDao 直读 ADS
│    institution/ talent/  tech/                 → XxxSource 接口（三实现配置切换）
│    general/                                    → 综合服务（横切编排）
│
├─ channel/                    【按供方 = 技术防腐层】
│    ChannelRegistry           能力表 + resolve(capabilityKey)
│    local-ads/                包 ElementDao（gkxlumenx_ads 全限定名）
│    jiuxin-http/              久新 API（超时/重试/熔断/限流）
│    jiuxin-jdbc/              久新库直查（readOnly，**唯一持有久新数据源**）
│    JiuxinMapper              键归一化 + 字段映射（供方结构变化不外溢）
│    yanda/ zhipu/ shenshi/    （阶段一内联，消费方 ≥2 再独立）
│
└─ support/
     ElementDao
     FragmentAssemblerSupport   并行 + 降级工具
```

### 3.4 与现有 L3 资产的关系

| 现有服务 | 处置 | 理由 |
|---|---|---|
| `gkxlumen-metrics` | ✅ **必复用** | `/metrics/v1/catalog`，两系统共用，无争议 |
| `gkxlumen-innov` | 🟡 **过渡复用** | 载体/事件/城市指数已实线；后续按要素迁入 element |
| `gkxlumen-topic-enterprise` / `chain` / `policy` / `svc` | ❌ **不复用** ⚠️**待裁决 A1** | 数据形态不同：专题侧要「检索/画像/对比篮」，展示侧要「要素 count/地图落点/热力/时间序列」；复用需改造对方并绑死发布节奏；且其下游是专题侧 Python 门面（:8080/:8081），与 D15「三重隔离」冲突 |

---

## 4. 数据读取策略

### 4.1 规约依据

| 来源 | 原文 | 含义 |
|---|---|---|
| `data/data-design/storage/README.md:40` | 「调用链前端→Java→Python；**Java 只读 ADS**；Python 写 ADS/Nebula/ES；三方经数据工厂 `ODS → DWD → ADS`」 | ADS 的读者就是 Java |
| `storage/README.md:89` | 「MySQL ADS \| **契约面** \| Python/工厂写出 \| **Java 只读**」 | 同上 |
| `storage/README.md:87` | 「MySQL ODS（供应库视角）\| 贴源 \| … \| **ETL**（正式 GDF）」 | ⚠️ ODS 的读者是 ETL，**不是 Java** |
| 基线 D3 | 「Java 业务 API **仅读 `*_ads`**（+ `app_user` 读写）；**禁扫 ODS/DWD**」 | 直连三方库属违规 |
| 基线 D7 | 「三方源…经数据工厂转换接入，**不传导到契约面**、上层零改动」 | 三方库应经 ETL 落 ADS |

### 4.2 已有实现证据

| 模式 | 实例 | 证据 |
|---|---|---|
| **纯查询/聚合 → Java 直读 ADS** | `gkxlumen-innov` JDBC 默认库 `gkxlumenx_ads`，`hikari.read-only: true` | `gkxlumen-innov/src/main/resources/application.yml:19-27` |
| **需算法加工 → Feign 调 Python** | innov 科技新闻抽取 → `gkxlumen-platform-innov-py:8000` | 同上 `:29-35` |
| **直连外部只读库（双数据源）** | `gkxlumen-cms` 业务库 `@Primary` + 真源只读库 `@Qualifier` | `gkxlumen-cms/.../overlay/SourceDataSourceConfig.java:29-75` |

### 4.3 结论

| 维度 | 走法 | 判据 |
|---|---|---|
| 企业 / 产业链 / 服务机构 / 政策 | **Java 直读 `gkxlumenx_ads`** | 数据在 ADS 现成（`TS-聚合方案 §1.3`「复用现成表，不新建」）；展示要 count/落点/统计 = 纯聚合，无算法加工 |
| 科研机构 / 人才 / 技术 | **分阶段**：阶段一直连久新（API 或库），阶段二切 `ts_*` 表 | D15 §2.2「领域服务直接调久新 API」是当前态；D7 数据工厂是目标态 |

> **注**：D15 建议智树自建 6 要素走 `gkx_show_service`（:8082）。但该项目目前仅 `/healthz`，`data_source: none`。
> 本文建议**先直读 ADS**（D3 允许、innov 有成熟先例），待门面填实后经 `channel/local-ads` 内部切换，**domain 层零改动**。⚠️ 见裁决 A4。

---

## 5. 久新接入：片段级通道抽象

### 5.1 粒度纠正

```
❌ 供方级：久新 ──► 全部 HTTP   或   全部库
❌ 要素级：institution ──► jdbc（整个要素一个通道）
✅ 片段级：一次「科研机构详情」查询
     ├─ 基础信息片段 → 久新库（自查询）
     ├─ 指标片段     → 久新 API（其已提供能力）
     └─ 关联关系片段 → 我方 ADS
     然后拼装为一个结果
```

同一要素，在不同查询（列表 / 详情 / 统计）中用到的片段组合也不同。

### 5.2 三层抽象

| 概念 | 职责 |
|---|---|
| **Fragment** | 数据片段，最小来源单元，带 `emptyReason` |
| **Channel** | 通道，统一 `fetch(capabilityKey, params)`；实现有 `jiuxin-http` / `jiuxin-jdbc` / `local-ads` |
| **Assembler** | 装配器，**手写 Java** 声明本次查询要哪些片段、有无依赖、如何拼装 |

```java
public record Fragment(String key, Map<String, Object> data, String emptyReason) {
    public boolean present() { return data != null && !data.isEmpty(); }
}

public interface Channel {
    String name();
    Fragment fetch(String capabilityKey, Map<String, Object> params);
}

@Component
public class ChannelRegistry {
    public Channel resolve(String capabilityKey) { /* 能力表 → 通道名 → bean */ }
}
```

装配器（编排是代码，不是配置）：

```java
public InstitutionDetail assemble(InstitutionQuery q) {
    Map<String, Object> p = q.toParams();

    // 无依赖片段：并行
    var base = supply(() -> channels.resolve("jiuxin.institution.base").fetch("jiuxin.institution.base", p));
    var rel  = supply(() -> channels.resolve("jiuxin.institution.relation").fetch("jiuxin.institution.relation", p));

    // 有依赖片段：需 base 的 orgKey 作入参
    Fragment baseFrag = base.join();
    p.put("orgKey", baseFrag.data().get("org_key"));
    var metric = supply(() -> channels.resolve("jiuxin.institution.metrics").fetch("jiuxin.institution.metrics", p));

    return InstitutionDetail.builder()
            .base(baseFrag)                                  // 久新库
            .metric(joinOrEmpty(metric, "指标服务不可用"))      // 久新 API，失败降级
            .relation(joinOrEmpty(rel, "暂无关联数据"))        // 我方 ADS
            .build();
}
```

配置仅描述**片段默认通道**，不描述编排：

```yaml
gkxlumen:
  element:
    channels:
      default: local-ads
      mapping:
        jiuxin.institution.base:     jiuxin-jdbc    # 自查询
        jiuxin.institution.metrics:  jiuxin-http    # 久新已提供 API
        jiuxin.institution.relation: local-ads      # 我方 ADS
```

久新改提供形式（API↔库）或数据工厂就绪，**改配置即可，Assembler 不动**——这正是 D7「不传导到契约面、上层零改动」的落地方式。

### 5.3 执行语义

| 场景 | 处理 |
|---|---|
| 片段间无依赖 | `CompletableFuture` 并行，总耗时 ≈ 最慢片段 |
| 片段间有依赖 | 先 `join()` 前驱，结果入 `params` 再查后继 |
| 单片段失败/超时 | 降级为 `emptyReason`，**其余片段照常返回**（沿用 `DomainHealthAggregator` 分区降级范式） |
| 超时配置 | 通道级独立：HTTP 用 connect/read timeout，JDBC 用 `queryTimeout` |

### 5.4 复杂度边界（明确不做）

| 做 | 不做 |
|---|---|
| 片段 = 一次方法调用 | ❌ DSL / 规则引擎 |
| 编排 = 手写 Java，一个 Assembler 一个方法 | ❌ 配置驱动的通用编排 |
| 仅「片段 → 通道」映射可配置 | ❌ 通用联邦 SQL 引擎 |

理由：展示系统查询形态有限（统计 / 落点 / 检索 / 详情 / 导出），手写编排的可读性与可测性远优于通用引擎。

---

## 6. 关键设计约束（硬性，落地时不得违反）

| # | 约束 | 原因 / 证据 |
|---|---|---|
| **C1** | **久新数据源只能由 `channel/jiuxin-jdbc/` 持有**，其余 `domain/` 包禁止直接注入久新 `JdbcTemplate`，只能走 `Channel` 接口 | 多数据源是服务拆分的最大障碍。收敛后将来拆 `gkxlumen-supplier-jiuxin` 只需搬一个包 |
| **C2** | **主体键归一化**：所有片段对外统一为我方 `org_id`（对齐 `TS-聚合方案 §1.3` 主体统一键），久新原始键不得外溢到 `domain/` 与前端契约 | 混合拼装最大风险：API 与库主键若不同套，拼装产出错数据**且不报错** |
| **C3** | **SQL 直接写 `gkxlumenx_ads.xxx` 全限定名，不复刻 `InnovSql.qualify()` 的 demo 映射** | `InnovSql.java` 将表名映射到 `demo_gkxlumenx_ads`，而 `gkxlumen-innov/application.yml:19` 注释要求「正式 2B 改写到 `gkxlumenx_`」——属未闭合整改债，违反 D12。新域不得复制 |
| **C4** | **双数据源装配两条坑**：业务库必须显式建 bean 并标 `@Primary`；注入处 `@Qualifier` **必须显式** | CMS 注释原文：「`@Primary` 业务库在候选解析中优先于参数名匹配，否则真源池会**静默连错库**」。自定义 DataSource 会让自动配置整体 back off |
| **C5** | **库名/凭证走 Nacos，不硬编码、不进 git** | CMS 注释：「正式化：`CMS_SOURCE_MYSQL_DB` 改 `gkxlumenx_dwd`（nacos 一处）」；D14 凭证放 K8s Secret |

---

## 7. 待裁决清单（请徐腾强逐项签署）

> 每项给出**建议答案**；如认可，仅在「裁决」栏填「同意」即可；如不认可，请填替代方案。

| # | 议题 | 选项 | **建议** | 依据 | 不裁决的后果 |
|---|---|---|---|---|---|
| **A1** | TS 的 L3 归属：新建 `gkxlumen-element`，还是复用 `gkxlumen-topic-*`？ | (a) 新建 `gkxlumen-element`<br>(b) 复用 `topic-enterprise/chain/svc/policy`<br>(c) 落 `gkxlumen-innov` | **(a)**。展示侧数据形态（要素 count/落点/热力/时间序列）与专题侧（检索/画像/对比篮）不同，复用需改造对方并绑死发布节奏；且 topic-* 下游是专题侧 Python 门面（:8080/:8081），与 D15 三重隔离冲突 | 本文 §3.4；⚠️ 偏离基线 §4 `display_aggregation.prefer_reuse: [/topic/v1]` | 决定代码写哪个模块；选错则整体返工 |
| **A2** | **直连久新库**是否准予过渡态豁免？ | (a) 准予，登记豁免与切换条件<br>(b) 不准，必须先经数据工厂落 ADS | **(a)**，并登记：切回条件 = 数据工厂 `ts_*` 表就绪；隔离措施 = 只读 + 收敛于 `channel/jiuxin-jdbc` + 配置可切 | D3（Java 仅读 `*_ads`）、D7（三方经数据工厂）、`storage/README.md:87`（ODS 读者为 ETL）；先例 `gkxlumen-cms` | 架构违规风险；闷头做会在验收时被拦 |
| **A3** | 路径前缀：`/display/v1/trend/**` 还是 `/situation/v1/**`？ | (a) `/display/v1/trend/**`<br>(b) 新增 `/situation/**` 网关路由 | **(a)**。D15 规定展示单入口为 `/display/v1/**`。前端 `src/api/situation/*.ts` 目前写死 `/situation/v1/**`，但注释已预留「契约出稿后仅改本层 real 路径，页面零改动」，改造成本极低 | D15；`repos/lumen-ui-science-pc/src/api/situation/index.ts` | 决定 `@RequestMapping` 与网关路由；前端定不了路径 |
| **A4** | 智树自建 4 维度读法：Java 直读 ADS 还是 Feign → `gkx_show_service`？ | (a) 先直读 ADS，门面就绪后内部切换<br>(b) 必须走 show-service | **(a)**。D3 允许 Java 读 ADS；innov 有成熟先例；`gkx_show_service` 当前仅 `/healthz`、`data_source: none`。切换点收敛在 `channel/local-ads`，domain 零改动 | D3、D15；`gkxlumen-innov/application.yml:19-27`；`lumen-topic-py/gkx_show_service/main.py` | 若选 (b) 则需先排 Python 门面工期，Java 阻塞 |
| **A5** | 久新**主体键是否对齐**（API 机构 ID 与库主键是否同一套）由谁向久新确认、何时答复？ | 指定责任人 + 答复时限 | 建议与久新接口清单一并催办；**在答复前 `channel/jiuxin-*` 只出桩实现（返回空 + `empty_reason`）** | 本文 §6 C2；`TS-聚合方案 §2` 中 10 行「久新-？」责任人至今未落 | 拼装正确性无法保证；是最大技术风险 |
| **A6** | 「综合服务」维度定义 | 需产品/需求给出：聚合哪几个维度、产出什么结构 | 暂缓 `domain/general/`，待定义明确后再开工 | 本文 §3.1 标注为「横切查询」 | 该包返工 |

**另需知会（非裁决，但影响排期）**：

- `gkxlumen-innov/support/InnovSql.java` 指向 `demo_gkxlumenx_ads`，与 D12 冲突 —— 建议单开整改单，新域不复制（§6 C3）。
- `lumen-algo-py` **零 TS 算法**（影响力/聚类/事件分级），M1 部分接口依赖；建议并行排期。
- `metric_id` 清单（U6）未登记，D9 ⓘ 角标暂无法对接。

---

## 8. 落地路线（最小验证闭环）

**不依赖裁决即可先行**（§7 中 A1/A2/A3 不影响以下结构搭建，但**联调前必须闭合**）：

| Step | 内容 | 验证点 |
|---|---|---|
| **1** | `gkxlumen-element` 模块骨架（pom + 启动类 + 双数据源） + `ts_*` 五表 DDL | 服务可启动、数据源装配正确（C4/C5） |
| **2** | `domain/enterprise` 一条完整链路（纯 ADS 直读，零外部依赖） | 直读 ADS 全链路（C3） |
| **3** | `display` 侧 `ElementLayerController`（跨域并行 + 分区降级） | 并行聚合与降级范式 |
| **4** | 前端 `USE_MOCK=false`，打通 FE → gateway → display → element → ADS → 回显 | **一次性验证五项架构决策**：路径前缀、包结构、双数据源、分区降级、D9 注入 |

**Step 4 联调成功即是最好的决策依据**，建议以此作为 M0 评审的演示材料。

验收后再按维度铺开，并填 `channel/jiuxin-*` 实现（待 A5 答复）。

---

## 9. 附录：证据索引

| # | 文件 | 关键位置 |
|---|---|---|
| 1 | `gkx-orchestration/agent-delivery/architecture-baseline.md` | D3 / D7 / D12 / D15 / §2.2 要素归属 / §4 依赖规则 |
| 2 | `gkx-orchestration/agent-delivery/data/data-design/storage/README.md` | `:40` Java 只读 ADS；`:87` ODS 读者为 ETL；`:89` ADS 契约面 Java 只读 |
| 3 | `repos/lumen-svc-platform/gkxlumen-innov/src/main/resources/application.yml` | `:19-27` JDBC `gkxlumenx_ads` + `read-only: true`；`:29-35` 算法走 Feign |
| 4 | `repos/lumen-svc-platform/gkxlumen-innov/src/main/java/.../support/InnovSql.java` | demo 库映射债（违反 D12） |
| 5 | `repos/lumen-svc-platform/gkxlumen-cms/src/main/java/.../overlay/SourceDataSourceConfig.java` | `:16-25` 双数据源说明与正式化注记；`:29-49` `@Primary` 业务库；`:51-75` 只读真源 + `@Qualifier` 显式 |
| 6 | `repos/lumen-svc-platform/gkxlumen-display/src/main/java/.../service/DomainHealthAggregator.java` | Feign 并行 + 分区降级范式 |
| 7 | `repos/lumen-svc-platform/gkxlumen-display/src/main/java/.../feign/RemoteInnovClient.java` | `:12-14` D15 调用路由说明 |
| 8 | `repos/lumen-topic-py/gkx_show_service/main.py` | 当前仅 `/healthz`，`data_source: none` |
| 9 | `agent-handoffs/科技发展态势-TS/TS-聚合方案-产业铺底.md` | §1.3 现成表清单 / §2 久新要素与责任人（「久新-？」未落） |
| 10 | `agent-handoffs/科技发展态势-TS/API-TS-M1.md` | §1.1 U1–U8 未决项；§3.1–§3.8 八类接口 |
| 11 | `repos/lumen-ui-science-pc/src/api/situation/index.ts` | 当前写死 `/situation/v1/**` |

---

**签署栏**

| 角色 | 姓名 | 裁决（A1–A6） | 日期 |
|---|---|---|---|
| 架构师 | 徐腾强 @qike366.com | | |
| 契约监管 | 李伟 | | |
| 前端 | 孔东（A3 路径对齐） | | |
| Python 门面 | 堂绍祖（A4 门面工期） | | |
