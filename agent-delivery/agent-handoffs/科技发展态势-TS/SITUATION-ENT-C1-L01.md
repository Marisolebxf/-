# SITUATION-ENT-C1-L01 · element 对象级企业点位端点

> **任务**：科技全域态势·企业维度跑通 C1 叶（U3 点位）——`gkxlumen-element` 新增对象级企业点位端点
> **角色**：`agent:api-agent` · 监管人：`human:李伟`（长任务授权，**授权句已生效**）
> **状态**：`backlog → claimed → in_progress → integration`（AV-1 自验后，待人工签收）
> **上位**：[SITUATION-ENT-长任务总控](./SITUATION-ENT-长任务总控.md) · 契约：[SITUATION-ENT-API-CONTRACT-01.md](./SITUATION-ENT-API-CONTRACT-01.md) §3
> **前沿倚**：A0 体检叶 [SITUATION-ENT-A0-L01.md](./SITUATION-ENT-A0-L01.md)（`ready_to_sign`）
> **挂接**：`工程过程/04-系统集成/05-展示系统集成/WBS.md` §4.3（WBS-05-18-02） · 日期 2026-10-27

---

## 一、交付内容

**新端点**：`GET /v1/element/enterprise/points`（`@Inner`，内部头 `from: Y`）

| 参数 | 默认 | 说明 |
|------|------|------|
| `limit` | 100 | **硬顶 500**（`Math.min(max(limit,1),500)`），防 18.9w 全量点位打爆前端地图 |
| `city` | — | 可选，限定城市（`b.city = ?`） |
| `district` | — | 可选，限定区县（`b.district = ?`） |

**SQL 口径**（`ElementDao` 占位 `{dwd}/{ads}` → `demo_gkxlumenx_dwd/ads`）：

```sql
SELECT s.org_id, b.enterprise_name, b.city, b.district, s.score_total, s.score_level,
       ROUND(b.headquarters_lng,6) AS lng, ROUND(b.headquarters_lat,6) AS lat,
       b.industry_category, b.is_high_tech, b.is_little_giant, b.is_gazelle, b.is_unicorn,
       b.patent_grant_count AS patent_count          -- ⚠️ 不是 patent_valid_count，见 §三
FROM {ads}.enterprise_score s
JOIN {dwd}.enterprise_base b
  ON s.org_id = b.org_id COLLATE utf8mb4_0900_ai_ci -- A0 实测两表 collation 不一致（1267）
WHERE s.score_total IS NOT NULL
  AND b.headquarters_lng IS NOT NULL AND b.headquarters_lat IS NOT NULL
  AND ABS(b.headquarters_lng) <= 180 AND ABS(b.headquarters_lat) <= 90
ORDER BY s.score_total DESC, s.org_id   -- org_id 兜底稳定排序
LIMIT ?
```

**响应**（`records[]` 已按契约 v1.1 §3 的 `MapRegion` 形状装配，C2 可直接透传）：

```
records[]: { key, parentRegionKey, label, objectTypeKey='enterprise', value, level,
             layerKeys, coordinates:[lng,lat], localDetail=true,
             detail:{ description, properties{region,industry,source}, relatedElements{patents} } }
total: <int>            // 实际出点数
emptyReason: "企业维度暂无数据"（仅空集时出现）
```

- `key` = `object-{org_id}`；`parentRegionKey` = district ?: city（中文名作 key，与 `/regions` 的城市级 key 同源）
- `value` = `影响力 {score，1 位小数}`（对齐 demo 种子语义如「影响力 96.8」，**数值真实**）
- `level`：`score≥55 → high` / `≥35 → medium` / 否则 `low`（阈值按 A0 实测分数域 11.34–70.28、均值 37.78、B 级仅 153 行校准）
- `layerKeys`：`enterprise`；`patents>0` 时追加 `patent`
- **序列化铁律**：`coordinates` 出 `double`（BigDecimal 直出有尾零/科学计数风险）、`patents` 出 `Integer`（平台 Jackson 把 `Long` 序列化成字符串 → 前端画不出图；见 `numify` 同源坑）

## 二、自测证据（本地 element :7082，`from: Y`，2026-10-27 16:2x）

| 用例 | HTTP | records | 耗时 | 首条 |
|---|---|---|---|---|
| 默认 `limit` | 200 | **100** | 959ms / 818ms（稳态；首次冷启动 6.6s） | 深圳市京泉华科技股份有限公司 · 影响力 70.3 · 龙华区 · patents=198 |
| `limit=2` | 200 | 2 | 729ms | 同上 |
| `limit=9999`（越界） | 200 | **500**（硬顶生效） | 1282ms | 同上 |
| `city=广州市&limit=2` | 200 | 2 | 504ms | 中铁隧道局集团有限公司 · 影响力 67.1 · 南沙区 · patents=103 |

- Top-N 与 A0 分数基线**完全一致**（京泉华 70.28 / 宝鹰建设 69.70 / 东莞捷荣 68.04 / 科达利 67.89 / 中铁隧道局 67.12）。
- 候选点位池核对：`187,983` 行 = 189,115 − 1,132（A0 实测脏坐标行数），**脏坐标剔除口径验证通过**。
- 单测 `EnterprisePointsAssemblerTest` **7/7 绿**（打包阶段执行，非跳过——见 §三）。

## 三、过程中发现并修正的两个数据/工程问题

1. **`patent_valid_count` 整列为 NULL**（我最初取它，导致 `patents: 0` 是**把「未知」写成「0」的伪事实**）。
   实测各列非空行数：`apply 189,115 / grant 189,115 / valid **0** / invention 189,115 / citation 189,115`。
   → 改用 **`patent_grant_count`（授权专利，0–325，均值 40.58）**；并改为 `relatedElements` **仅在数据源给出时现身**，NULL 时整个字段不出现（保留「未知」而非断言 0）。新增单测 `unknownPatentCountIsOmittedNotZero` 钉住此语义。
2. **element 模块单测此前是「假通过」**：低版本 surefire（2.12.4）不认 JUnit5，`Tests run: 0` 却 BUILD SUCCESS——本次之前所有测试都被静默跳过。按仓内既有做法（同 `gkxlumen-cms`、`gkxlumen-topic-svc-biz`）在 `gkxlumen-element/pom.xml` 显式声明 `maven-surefire-plugin:3.2.5`。**此结论建议沉淀为通用教训：新增测试模块先确认 surefire 版本，否则「绿」是假的。**

## 四、给 C2 / D1 的输入

1. **C2（display `/map` objectPoints 接线）**：直接 Feign 取本端点 `records` 透传为 `objectPoints`；Feign 方法需 `@NoToken`（下游 `@Inner` 配对，否则静默降级为「拿不到数据」，极易误判下游挂）。降级路径仍保留：element 不可达 → `objectPoints: []` + `objectPointsEmptyReason=UNREACHABLE`。
2. **默认 N 的取舍**：默认 100（硬顶 500）是本叶定的**工程口径**（不是业务口径）；前端若需「只显示 Top50」应在 any 层切片，不作为契约。
3. **`parentRegionKey` 口径**：目前填的是**行政区划中文名**（如「龙华区」），而 demo 种子用的是拼音 slug（`longgang`）。C2/D1 若发现 cascader 过滤对不上（点无法靠 expect 层级联动），是**口径差异**不是 bug——要么统一改用中位名、要么由 C2 建一层映射（建议在 C2 定，不擅改本叶输出）。
4. **`relatedElements` 只有 `patents`**：DWD 无论文 / 项目 / 成果列，按诚实性不补全 demo 的四个维度；UI 侧若有缺项依赖（如期望必有 papers/projects），需 D1 在 `types/situation.ts` 的可选字段语义内消化（字段名可选，不新增）。
5. **口径占位诚实性**：本端点分数来自 `enterprise_score`，**不等价**正式指标 `M_INNOV_ENTERPRISE_INFLUENCE`（算法未上线、D4=mock 不翻转）；`properties.source` 已写明「企业评分模型 enterprise_score（占位）」，C2/D1 不要把它改写成正式指标名。

## 五、环境事实更新（对 A0 报告的增补）

- **真实网关地址 = `http://10.50.69.111:30895`**（用户 10-27 提供；A0 记的 `192.168.88.50:9999` 作废）。`/display/actuator/health` → **200 UP**（Redis 7.4.0 UP）。
- **网关鉴权**：无 token POST `/display/v1/situation/map` → **401「访问令牌不存在」**（真实 token 需 PigX 登录获取；C 段本地 local profile 不受影响，D1 前置需解决）。
- ⚠️ **Nacos 服务列表（display 视角 13 个服务）不含 `gkxlumen-element`**：K8s 路径 display→element 走服务发现，**element 未注册/未部署到 K8s dev 是硬缺口**（走 K8s 全链路前需部署或确认注册策略）。本地 local profile 联调不受影响。

## 六、本叶改动清单（git）

| 文件 | 类型 | 说明 |
|---|---|---|
| `gkxlumen-element/src/main/java/.../controller/EnterpriseController.java` | 改 | 新增 `/points` 端点 + `toPointItems()` 纯函数装配 + 阈值/类型工具方法；口径写在 javadoc |
| `gkxlumen-element/src/test/java/.../EnterprisePointsAssemblerTest.java` | 新增 | 7 个单测（契约字段、Integer 类型、层级、阈值边界、缺失剔除、NULL 未知语义） |
| `gkxlumen-element/pom.xml` | 改 | 声明 surefire 3.2.5（修复 JUnit5 静默跳过，见 §三.2） |

> ⚠️ **未赛合冲突提醒**：工作区中另有前序任务的未提交改动（`gkxlumen-display/**`、`element/application*.yml`、`db/*.sql`、`scripts/local-seed-enterprise.sql` 等），**不属本叶范围**，本叶未动它们。监管人走查时请按上表三文件为准；**本叶按人工验收闸门停在本地工作区，未 commit、未 push**。

## 七、Cost 四字段

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈ 120k（估，含两次失败重构建的额外上下文） |
| model_used | auto（CodeBuddy） |
| actual_cost | ≈ $0.9（估） |
| cost_warn | green（<$10） |

ponytail: full（未为省 token 砍自测组数；两次构建失败都追到根因（varargs 泛型 / surefire 静默跳过），未绕过）
