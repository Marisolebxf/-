# SITUATION-ENT-A0-L01 · 数据/环境体检报告

> **任务**：科技全域态势·企业维度跑通 A0 叶（只读体检，无业务代码、无库写入）  
> **角色**：`agent:data-agent`（执行）· 监管人：`human:李伟`（长任务总控授权人）  
> **状态**：`in_progress → ready_to_sign`（spike，AV-0 目标态）  
> **上位**：[SITUATION-ENT-长任务总控](./SITUATION-ENT-长任务总控.md) · 挂接 WBS-05-18-01（`工程过程/04-系统集成/05-展示系统集成/WBS.md` §4.3）  
> **日期**：2026-10-27

---

## 一、环境核验结论

| 项 | 结果 | 证据 |
|----|------|------|
| 开发库 `10.50.11.76:3306` | ✅ **可达**（TCP 通，mysql 客户端实测查询成功） | Test-NetConnection + mysql 查询（§二） |
| K8s 网关 | ✅ 真源 `http://10.50.69.111:30895`，`/display/actuator/health` **200 UP** | 见下方 2026-10-27 补验 |
| 本机 kubeconfig | ❌ 指向 `127.0.0.1:16443`（本地集群未起），无法看 K8s dev | kubectl 报 connection refused |
| 本地 `gkxlumen-element`（:7082，local profile，直连开发库） | ✅ 运行中；**发现旧实例僵死（TCP 接受连接后零字节关闭）**，已停掉并用当前代码重建重启（PID 55840，26s 启动完成），六端点全通 | netstat / 日志 `target/element-local.out.log` |
| 本地 `gkxlumen-display`（:7099，local profile） | ✅ 运行中（昨夜 21:49 起的实例，健康）；`/v1/situation/**` 在 local profile 放行（`ignore-urls`），**curl 自测无需 token**，仅需内部头 `from: Y` | `application-local.yml` L50-56 |
| 真实网关 token 获取 | ⚠️ 无 token 调 `/display/v1/situation/map` 返回 **401**。local profile 已放行聚合端点、`@Inner` 用 `from: Y` 头；PigX 登录 token 留 D1 前置 | 见下方补验 |

> **2026-10-27 补验（授权人提供真实网关地址 `http://10.50.69.111:30895`）**：① `/display/actuator/health` → **200 UP**（Redis 7.4.0 UP、Nacos 发现 13 服务）；② 无 token POST `/display/v1/situation/map` → **401「访问令牌不存在」**（真实 token 需 PigX 登录获取，组合验证留 D1 前置）；③ ⚠️ **注册中心服务列表不含 `gkxlumen-element`**（display 视角 Nacos 13 服务无 element）——K8s 路径 display→element Feign 依赖服务发现，**element 未注册/未部署到 K8s dev 是缺口**（本地 local profile 不受影响；K8s 全链路验证前需部署 element 或确认其 Nacos 注册策略，记录为 C2/D1 前置风险）。网关真源是 `10.50.69.111:30895`。

**环境根因记录**：昨夜启动的 element 旧实例处于「连接即零字节关闭」的僵死态（对 curl/原始 TCP 均如此；期间 display 经 Feign 仍能取到真实数据）。处置：`Stop-Process 53576` → `mvn -pl gkxlumen-element -am install -DskipTests`（JDK 17）→ 重启 local profile → 六端点全绿。**教训（沉淀给 C 段）：本地联调前先 `curl /actuator/health` 探活，勿信任「进程在=服务可用」。**

## 二、库体检（`10.50.11.76:3306`，demo 库，只读）

### 2.1 行数

| 表 | 行数 |
|----|------|
| `demo_gkxlumenx_dwd.enterprise_base` | **189,115** |
| `demo_gkxlumenx_ads.enterprise_score` | **189,115**（与 base 一一对应） |
| `demo_gkxlumenx_ads.enterprise_domain_dist` | 30 |
| `demo_gkxlumenx_ads.enterprise_type_dist` | 35 |

### 2.2 脏值体检（enterprise_base）

| 检查项 | 行数 | 占比 | 结论 |
|--------|------|------|------|
| 经纬度 NULL（lng 或 lat） | 1,132 | 0.6% | **C1 点位端点必须剔除**（契约 §3 已写明） |
| city 空或 NULL | 1 | ~0 | 可忽略 |
| registration_date NULL 或年份越界（<1900 / >2026） | 353 | 0.19% | trend 聚合时 YEAR() 为 NULL 的行自然落不进任何年份桶 |
| 坐标越界（|lng|>180 或 |lat|>90） | 0 | — | 干净 |
| enterprise_score.score_total NULL / 越界（<0 / >100） | 0 | — | 干净 |

### 2.3 enterprise_score 口径事实（C3 influence 端点输入）

- 分数域：`score_total` min **11.34** / max **70.28** / avg **37.78**
- 等级分布：**D 125,261 · C 63,701 · B 153 · A 0**（无 A 级）
- Top5：京泉华 70.28（深圳）· 宝鹰建设 69.70（深圳）· 东莞捷荣 68.04（东莞）· 科达利 67.89（深圳）· 中铁隧道局 67.12（广州）
- ⚠️ **口径差异警示**：demo mock 榜单是华为 96.8 等演示值；真实分数域上限 70.28，且 Top 企业不是「华为/大疆」。走查清单第 4 条的「期望」应按本报告真实值核对，D1 切换后数字变化属预期。
- `score_detail` 为 JSON（含 metric_ids，可对接 D9）；`org_id` 与 base 关联存在 **collation 不一致**（`utf8mb4_0900_ai_ci` vs `utf8mb4_general_ci`）——C1/C3 写 join SQL 时必须显式 `COLLATE`（已在 A0 探查中实测踩到）。

## 三、element 六端点 curl 基线（本地 :7082，`from: Y`，2026-10-27 15:3x）

| # | 端点 | HTTP | 关键数据 |
|---|------|------|---------|
| 1 | `GET /v1/element/enterprise/overview` | 200 | total 189,115 · highTech 27,936 · littleGiant 14,903 · gazelle 588 · unicorn 167 · sme 25,725 · listed 0 |
| 2 | `GET /v1/element/enterprise/regions?limit=3` | 200 | 深圳 95,525(114.0088,22.6404) · 广州 48,779 · 东莞 33,574 |
| 3 | `GET /v1/element/enterprise/districts?city=深圳市` | 200 | 9 区：宝安 25,189 · 龙岗 17,443 · 南山 16,002 · 龙华 13,879 · 福田 8,802 · 光明 6,878 · 罗湖 3,627 · 坪山 3,027 · 盐田 678 |
| 4 | `GET /v1/element/enterprise/trend?startYear=2020&endYear=2026` | 200 | 13,030/13,423/8,940/7,884/5,349/3,061/122（2020→2026） |
| 5 | `GET /v1/element/enterprise/domain-dist` | 200 | 30 行（2021–2025 × 6 域）；⚠️ 人工智能占比 98.7%+（161,343→186,842）——**分布近乎单域，为口径事实，非 bug**；growthRate null（首年）与 `0E-10` 序列化现象记录在案 |
| 6 | `GET /v1/element/enterprise/type-dist` | 200 | 35 行（2021–2025 × 7 类型）；high_tech 27,677→27,936 · sme 25,231→25,725 · little_giant 14,815→14,903 · gazelle 588 · unicorn 165→167 · **foreign 0 · listed 0** |

## 四、display 聚合端点基线（本地 :7099，`from: Y`）

- `POST /v1/situation/overview`（`{}`）→ 200：stats 五值（企业总数 189,115 等真实值）、trendSeries 2015–2026、factorCards、domainRows（人工智能 186,842 等）。**数值型字段以字符串序列化（`"value":"189115"`）**，与前端 `displayValue` 消费方式对齐。
- `POST /v1/situation/map`（`{}`）→ 200：factorItems（enterprise=189,115，其余 10 要素 count=0——**与走查清单第 1 条期望一致**）、regions 30 城市、regionCascadeOptions 含深圳 9 区/广州 11 区级联、legend 完整；**`objectPoints: []` + `objectPointsEmptyReason: "企业对象级点位接口未开放，暂不返回（不以城市点冒充对象点）"`** —— C1/C2 改造前现状基线。完整响应存档：[SITUATION-ENT-A0-L01-map-baseline.json](./SITUATION-ENT-A0-L01-map-baseline.json)。

## 五、对 C 段/D 段的输入结论

1. **C1 可开工**：数据齐（enterprise_score+base 坐标可用；1,132 行脏坐标剔除；join 需显式 COLLATE）。
2. **C2 对照基线已存档**（本报告 §四 + map-baseline.json）。
3. **C3 数据域确认**：真实分数域 11.34–70.28、无 A 级；`score_level` 可作 rankScope 语义参考。
4. **D1 注意**：mock 值（92,000/华为 96.8）与真值差异巨大，走查期望以本报告为准。
5. **网关**：真源是 `http://10.50.69.111:30895`（health 200）。经网关的全链路仍差 PigX 登录 token，不阻塞本地 C/D 段。
6. ⚠️ **domain-dist 口径风险**：人工智能占比 98.7%，页面饼图将近乎全幅单域——如需产品口径复核，属口径侧问题，本管线不擅改（记录，不阻塞）。

## 六、本叶操作留痕（全部只读/环境操作）

- 建 registry：`SITUATION-ENT-A0-L01`（MCP `task-create`）→ `task-claim`（supervised_by=human:李伟, lock 24h）→ `in_progress` → 本报告后转 `ready_to_sign`。
- 环境操作：停掉僵死 element 旧进程（PID 53576）→ 重建 jar（`-DskipTests`）→ 重启 local profile（新 PID 55840）。**未改任何业务代码、未写任何库。**
- 查询 SQL 均为 SELECT / SHOW（见 §二 §三）；`map-baseline.json` 为响应存档副本。

## 七、Cost 四字段

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈ 150k（估，含两条并行调研子代理） |
| model_used | auto（CodeBuddy） |
| actual_cost | ≈ $1.0（估） |
| cost_warn | green（<$10） |

ponytail: full（体检完整性优先：环境根因定位 + 脏值 + 口径事实 + 基线存档，未为省 token 砍核验项）
