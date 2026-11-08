# SITUATION-IM-C1-L01 · pilot 首叶：M6 深圳 carriers 端点打通

> **单号**：`SITUATION-IM-C1-L01`（WBS-05-19-03） · **日期**：2026-10-28 · **监管人**：`human:李伟`
> **契约**：`SITUATION-IM-API-CONTRACT-01.md` **v0.3**（§4.6 端点清单 / §4.7 数据真源规则）
> **状态**：`integration`（代码已完成并通过编译与等价 SQL 验证；**HTTP 端到端自测未做**，原因见 §4）

---

## 1. 交付物

### 1.1 innov 侧（**U13 授权新增的 `/internal/*`**）

| 文件 | 内容 |
|---|---|
| `gkxlumen-innov/src/main/java/com/topcomm/gkxlumen/innov/controller/ShenzhenController.java` | 新增 `POST /internal/innov/v1/shenzhen/carriers`，`@Inner(value = false)` 标注 |

能力：
- 按 `adminCode` 前缀过滤（默认 `440300` 深圳市本级）
- `period` 取最新一期（`YYYY-MM`）
- `keyword` 名称模糊、`carrierType` 精确、`pageNum/pageSize` 分页
- **JOIN 时显式 `COLLATE utf8mb4_general_ci`**（解决 `ERROR 1267`，见 §3）
- `LEFT JOIN dim_admin_division` 翻译行政码 → 中文名
- 返回 `total / list / period / adminCode / pageNum / pageSize / noSourceFields / emptyReason`

### 1.2 display 侧（BFF 聚合）

| 文件 | 内容 |
|---|---|
| `gkxlumen-display/.../controller/ShenzhenInnovationController.java` | 新增 `POST /v1/situation/shenzhen-innovation/carriers` |
| `gkxlumen-display/.../feign/RemoteInnovClient.java` | 新增 `shenzhenCarriers(...)`，`@NoToken` 与下游 `@Inner` **配对** |

装配对齐前端 `types/shenzhenInnovation.ts` 的 `SzInnovationCarrier`。
为便于本地自测，`RemoteInnovClient` 增加 `url = "${feign.innov.url:}"`（与 `RemoteElementClient` 同款惯例，留空即走服务发现）。

---

## 2. 字段有源 / 无源清单（诚实表）

| 前端字段 | 有源 | 来源 | 备注 |
|---|---|---|---|
| `id` | ✅ | `carrier_id` | |
| `name` | ✅ | `name` | |
| `type` | ✅ | `carrier_type` | **值域偏离**：含 `incubator`，不在 `SzCarrierType` 枚举内 → 保留原值 |
| `level` | ✅ | `carrier_level` | **值域偏离**：`national/provincial`，与前端五档语义不同 → 保留原值 |
| `location` | ✅ | `lng` / `lat` | 缺失时返回**空数组**，不落 `(0,0)`（避免点被画到几内亚湾） |
| `district` | ✅ | `admin_code` → `dim_admin_division.name` | 实测得到「深圳」 |
| `domain` | ✅ | `domain_id` | 指数侧固定 `ALL` |
| `value` | ✅ | `index_score` | 强转 double |
| `rank` | ✅ | `rank_total` | 强转 int（Long 会被 Jackson 序列化成字符串） |
| `street` | ❌ | 无源列 | 字典只到城市级 |
| `description` `patents` `papers` `projects` `talents` `rdInvestment` `domainDist` `domainCover` `孵化企业数` `合作机构数` | ❌ | 无源列 | `dim.carrier` 实测仅 9 列，无这些列 |
| `isSubscribed` | ❌ | 需登录态与写面 | 本次 deferred |

无源字段统一登记在返回值的 `noSourceFields` 中，由前端按 **D1 missing** 出红问号（`IconQuestionCircle`），**禁止伪造数值**。

---

## 3. 关键技术处置

### 3.1 `ERROR 1267` 排序规则冲突（本次最大坑）

```
ads.carrier_index.carrier_id : utf8mb4_0900_ai_ci
dim.carrier.carrier_id       : utf8mb4_general_ci
→ 直接 JOIN 抛 Illegal mix of collations
```

按 `human:李伟` 裁定采用**方案 A**：SQL 层显式
`i.carrier_id COLLATE utf8mb4_general_ci = c.carrier_id`。
代码内已写注释标明「不可删」。

⚠️ **残留风险**：现役 `CarrierController.rank / compare / detail`（`CarrierController.java:41,72,82`）存在**同款缺陷**，
此前不暴露是因为事实表为空。**超出本管线范围**，已建议另行开单给平台侧。

### 3.2 数据来源性质

`city_index.indicator_values.source = benchmark_manual_pack` —— 由 `innovPy` P1–P9 批处理灌入的演示基准包，
**非真实数仓实算**。已写入返回的 `dataSourceNote`，评审层须按 **D4=mock** 标注。

### 3.3 地域筛选能力边界

深圳载体的 `admin_code` **全是 `440300`（市本级）**，`dim_admin_division` 无区级数据。
因此「按行政区筛选」在当前数据下必然查不到 → 返回空列表 + `emptyReason`，**不谎称支持**。
`scopeOf` 仅能识别「深圳 / 440300」，其余中文区名原值下传并自然落空态。

---

## 4. 验证证据

| 项 | 方式 | 结果 |
|---|---|---|
| 编译 | `mvn -pl gkxlumen-innov,gkxlumen-display -am compile`（**JAVA_HOME 须为 JDK 17**，本机默认 JAVA_HOME 是 JDK 8，会报「无效的目标发行版: 17」） | ✅ 通过，产物确认存在：`ShenzhenController.class`、`ShenzhenInnovationController.class` |
| lint | IDE diagnostics | ✅ 0 error |
| **端点逻辑** | 用与端点完全等价的 SQL 直连 demo 库执行 | ✅ 成功返回深圳 3 条（含真实经纬度与指数），`COLLATE` 修复确认生效 |

等价 SQL 实测返回：

```
深圳科技大学         university  national    114.127932,22.527368  深圳  51.88  rank 10
深圳科创孵化器       incubator   provincial  114.061245,22.425458  深圳  50.23  rank 12
中科院深圳先进技术研究院 research    national    113.962082,22.651624  深圳  46.58  rank 14
```

### ⚠️ 未完成：HTTP 端到端自测

**原因**：本机无法启动 `gkxlumen-innov`
1. 缺 Nacos 注册/配置中心 → `Client not connected, current status:STARTING`
2. 即便加 `--spring.cloud.nacos.discovery.enabled=false` 绕过，仍会
   因 `FeignClientsRegistrar` 解析 `${server.servlet.context-path}`（该占位符由 Nacos 供给）失败而中断
3. jar 已构建成功（`gkxlumen-innov.jar` 118.6MB），缺的是运行环境的配置中心

→ **innov 无法脱离 Nacos 独立运行**，属环境既有约束。按 DoD 第 7 条，此处如实记为「未动态验证」，
并在 registry evidence 中同源说明。解决条件：提供可达的 Nacos 或补全本地配置。

---

## 5. 遗留 / 建议

1. **既有 `CarrierController` 的 `ERROR 1267` 缺陷**：建议单独开单（不在本管线范围，勿自行改动）。
2. **缺 resolutions**：`talents` / `rdInvestment` 等字段需新增源列或对接真实数据源 → 属「新增列」，
   按总控 §0.1 第 4 条须 `human:李伟` 单独批准，本叶未做。
3. **`city_code` 归一**未在本叶实装（本叶不涉及 `city_index`），由后续 C4 `city-benchmark` 按契约 §4.7 第 2 条落实。
4. **后续 pilot 叶顺序**（按 A0 §9）：C1 ✅ → C4 `city-benchmark` → C5 `operation-timeline` → C3 `field-distribution` → C2 `indicator-systems`。

---

## 6. ponytail

- **本单变更**：新增 3 个文件 / 改 1 个文件，全部在 `lumen-svc-platform`；**未改任何 UI 仓文件**。
- **本单变更范围严格限于上述 4 个后端文件**；未完成 HTTP 自测前请勿向外部声称「已联调通过」。
- **待回填**：契约 §7 实装对照表（本叶一行）——见 §7。

## 7. 契约 §7 回填（本叶）

| 端点 | 服务 | 状态 | 备注 |
|---|---|---|---|
| `POST /v1/situation/shenzhen-innovation/carriers` | `gkxlumen-display` | ✅ 已实装 | 编译通过，逻辑经等价 SQL 验证，HTTP 自测待 Nacos |
| `POST /internal/innov/v1/shenzhen/carriers` | `gkxlumen-innov` | ✅ 已实装（U13 新增） | 同上 |

## 8. cost 四字段

| 字段 | 值 |
|---|---|
| `cost_warn` | `green` |
| `actual_cost` | 3.6 |
| `model_used` | `auto` |
| `actual_tokens` | 620000 |
