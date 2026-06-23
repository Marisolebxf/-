# 政策模块 · 灌数（数据初始化）流程说明

> 适用对象：算法 / 后端 / 前端 / 运维 / QA
> 关联仓：`demo-algo-ent-analysis`（polan 算法 + FastAPI）、`demo-ui-system-test`（政策展示页）
> 关联交付：`POLICY-delivery-summary.md`
> 最近更新：2026-06-23（run-pipeline 改异步触发 + 前端轮询）

---

## 1. 什么是「灌数」

政策模块的前端 demo 展示的是 **polan 算法跑出来的结果表**（`gkx_ads.*` 17 张）。
"灌数" = 在目标数据库里**从零跑通整条政策算法流水线**，把这些结果表写满，让前端各 Tab 能出数。

一次灌数会顺序完成：

```
建表(DDL) → 模型注册 → Mock 贴源明细 → 基础指标 → 图谱(NER/RE)
→ Nebula 灌入(可选) → 6 个深度模型 → 文本(解析/匹配/推演)
```

全程**幂等**（每步先 `TRUNCATE` 再写入），可反复重跑，不会产生重复数据。

---

## 2. 总体数据流

```
[前端 灌数据按钮]                      [展示查询]
 demo-ui-system-test                  各 Tab 组件
        │ POST                              │ GET
        ▼                                   ▼
 Spring Cloud Gateway  /api/policy/**  (sys_route_conf 路由 → entan-py)
        │                                   │
        ▼                                   ▼
 FastAPI (demo-platform-entan-py pod, dev 命名空间)
   /internal/policy/run-pipeline   /v1/policy/**
        │                                   │
        ▼                                   ▼
   polan 算法包  ──写──►  PostgreSQL (gkx_ads.* / dwd.* / gkx_cfg.*)
                          (与企业 entan 同一个 PG 实例)
```

- 前端只调 Java 网关，网关转发到 Python FastAPI（符合调用链铁律）。
- 写库与读库是**同一个 PG**；灌数写入后，`/v1/policy/**` 立即可查到。

---

## 3. 三种灌数触发方式

| 方式 | 触发点 | 适用场景 | 是否需要部署环境 |
|---|---|---|---|
| **A. 启动自举** | pod 启动时 `api/main.py::maybe_bootstrap_policy()` | 首次部署 / SQLite 空库自愈 | 是 |
| **B. HTTP 一键灌数** | 前端「灌数据」按钮 → `POST /internal/policy/run-pipeline` | 部署环境按需重灌 | 是 |
| **C. 命令行** | `python scripts/run_all_policy.py` | 本地开发 / 验证算法 | 否（本地 SQLite） |

### A. 启动自举（自动）

pod 启动时自动判断是否需要灌数，逻辑（`api/main.py`）：

- **SQLite 后端**：表为空 → 后台线程自动跑全流水线（pod 重启可自愈）。
- **PG 后端**：默认**不自动跑**（避免每次重启重复重跑慢任务）；仅当显式设置环境变量 `POLAN_RUN_ON_START=1` 时才跑。
- 自举在**后台线程**执行，不阻塞 `/healthz` 探活。

### B. HTTP 一键灌数（前端按钮）

- 前端政策页右上角 **「灌数据」** 按钮。
- 点击 → 确认弹窗 → `POST /api/policy/internal/policy/run-pipeline`。
- 后端**异步触发**：立即返回 `running:true`，全流水线在后台线程跑。
- 前端随后**轮询** `GET /api/policy/internal/policy/status`，直到 `running:false`，再整页刷新出数。

> ⚠️ 远程 PG 全量灌数耗时**数分钟**（见 §8），所以一定是「异步触发 + 轮询」，不能同步等待，否则前端/网关会超时。

### C. 命令行（本地）

```bash
cd demo-algo-ent-analysis
# 本地默认 SQLite，零依赖即可真实跑通
python scripts/run_all_policy.py

# 切 PG：
set POLAN_DB_BACKEND=pg          # Windows
export POLAN_DB_BACKEND=pg       # Linux/mac
# 启用 Nebula 图谱灌入（默认跳过，用 PG/SQLite 镜像兜底）：
set POLAN_NEBULA_ENABLED=1
```

---

## 4. 流水线 15 步详解

来源：`scripts/run_all_policy.py::STEPS`（HTTP/自举与命令行**共用同一份步骤**）。

| # | 步骤 | 实现 | 产出表 / 动作 |
|---|---|---|---|
| 1 | Schema 初始化 | `polan.common.db.init_schema` | 建 `dwd` / `gkx_ads` / `gkx_cfg` 全部表 |
| 2 | 政策模型注册 seed | `polan.models.registry.seed_registry` | `gkx_cfg.cfg_model_registry`（element=POLICY） |
| 3 | Mock 贴源明细 | `polan.mockgen.generate.run` | `dwd.policy_base_info`（约 600 条政策明细） |
| 4 | A 基础指标 | `polan.basic.indicators.run` | `ads_policy_level_dist` / `type_dist` / `timeseries` / `national_dist` / `sz_dist` |
| 5 | B 实体识别 NER + 关系抽取 RE | `polan.graph.entity.run` | `ads_policy_entity` + `policy_graph_node` + `policy_graph_edge` |
| 6 | B+ Nebula 灌入 | `load_nebula_safe` | 灌入 NebulaGraph `gkx_policy`；**未启用/失败安全跳过**（API 回退 PG 镜像） |
| 7 | C1 政策焦点识别 | `polan.eval.focus.run` | `ads_policy_focus` |
| 8 | C2 政策力度评估 | `polan.eval.intensity.run` | `ads_policy_intensity` |
| 9 | C3 政策效果评估 | `polan.eval.effect.run` | `ads_policy_effect`（`scope_type='region_effect'`）+ `ads_policy_metric_timeseries` |
| 10 | C4 政策短板识别 | `polan.eval.gap.run` | `ads_policy_effect`（`scope_type='region_gap'`，复用同表区分类型） |
| 11 | C5 政策机遇识别 | `polan.eval.opportunity.run` | `ads_policy_focus`（region 粒度行，`policy_id IS NULL`，`opportunity_cnt`） |
| 12 | C6 政策布局推荐 | `polan.eval.layout.run` | `ads_policy_effect`（`scope_type='region_layout'`） |

> 注：短板/机遇/布局**没有独立表**——短板与布局复用 `ads_policy_effect`（靠 `scope_type` 区分），机遇写入 `ads_policy_focus` 的区域行。前端按 `scope_type` / 行类型分别读取。
| 13 | D1 政策文本解析 | `polan.text.parse.run` | `ads_policy_text_parse` |
| 14 | D2 政策匹配推送 | `polan.text.match.run` | `ads_policy_match` |
| 15 | D3 政策效果推演仿真 | `polan.text.simulate.run` | `ads_policy_simulate` |

> 每步先打印 `[policy-pipeline] <步骤名> ...`，可用 pod 日志判断进度（见 §9）。

---

## 5. 数据库后端选择逻辑

实现：`polan/common/db.py`。优先级如下：

```
1) 显式 POLAN_DB_BACKEND（pg / sqlite）       —— 最高优先
2) 容器内检测到 ENTAN_PG_HOST                  —— 自动用 PG（与企业同库）
3) settings 配置 backend（默认 sqlite）        —— 本地兜底
```

**PG 连接信息复用规则**（同库部署，与 entan 共存不冲突）：

```
连接参数：POLAN_PG_*  优先 → 否则复用 entan 的 ENTAN_PG_*  → 否则 settings
schema 名：政策自己的 gkx_ads / dwd / gkx_cfg（与 entan 的 ads/enterprise 表互不干扰）
占位符：PG 用 %s；SQLite 用 ?（本层自动改写）
```

含义：部署环境只要注入了企业的 `ENTAN_PG_*`，polan **自动用同一个 PostgreSQL**，无需为 polan 单独配 Helm。

---

## 6. 接口契约

### 6.1 触发灌数（异步）

```
POST /api/policy/internal/policy/run-pipeline
```

立即返回（不等待完成）：

```json
{ "code": 0, "msg": "政策流水线已启动（后台运行，请轮询 status 查看进度）",
  "data": { "running": true, "last_run": null, "last_error": null, "last_cost_s": null } }
```

并发保护：已有流水线在跑时返回 `code:1, msg:"政策流水线正在运行"`，不会重复触发。

### 6.2 查询数据状态

```
GET /api/policy/internal/policy/status
```

```json
{ "code": 0, "data": {
    "backend": "pg",
    "running": false,
    "last_run": "2026-06-23 15:46:49",
    "last_error": null,
    "last_cost_s": 412.0,
    "tables": {
      "ads_policy_level_dist": 6, "ads_policy_type_dist": 5, "ads_policy_timeseries": 9,
      "ads_policy_national_dist": 31, "ads_policy_sz_dist": 9,
      "ads_policy_focus": 631, "ads_policy_intensity": 631, "ads_policy_effect": 93,
      "ads_policy_text_parse": 600, "ads_policy_match": 144, "ads_policy_simulate": 36,
      "policy_graph_node": 806, "policy_graph_edge": 3726 }
} }
```

- `running` —— 是否正在灌数（前端轮询此字段判断完成）。
- `last_error` —— 上次失败原因（成功为 `null`）。
- `last_cost_s` —— 上次耗时（秒）。
- `tables` —— 各结果表当前行数（判断是否已就绪）。

---

## 7. 前端「灌数据」按钮交互

实现：`demo-ui-system-test/src/views/policy/index.vue` + `src/api/policy/index.ts`。

```
点击「灌数据」
  → 确认弹窗
  → POST run-pipeline（20s 超时，仅触发，立即返回）
  → 提示「已启动，后台运行中」
  → 每 3s 轮询 status，最多 ~10 分钟
       ├─ running=true  → 继续等
       └─ running=false → last_error? 报错 : 提示完成耗时 → 刷新页面出数
```

要点：
- 触发请求超时设为 20s（只是触发，不等待全程）。
- 用轮询而非同步等待，规避前端/网关超时误报。
- 期间可关闭弹窗，后台照常跑。

---

## 8. 性能与超时说明（重要）

| 后端 | 单次全量灌数耗时（实测） | 原因 |
|---|---|---|
| 本地 SQLite | 数秒 ~ 十几秒 | 本地文件，无网络往返 |
| 远程 PostgreSQL | **约 412s（≈7 分钟）** | pg8000 的 `executemany` 实为**逐行执行**，全量约 **1.2 万+ 次单行 INSERT**，每次都有网络往返 |

结论与对策：
- **必须异步触发 + 轮询**（已落地），否则前端按钮 120s 必超时。
- 客户端断开**不会中止**服务端 uvicorn worker，后台会继续跑完。
- 数据落 PG 后**持久化**，pod 重启 / 重新部署**不丢**，无需反复灌数。

> 后续可优化方向（未实施）：把逐行 `executemany` 改为多行 `INSERT ... VALUES (...),(...)` 批量，远程 PG 可显著提速。

---

## 9. 故障排查 FAQ

### Q1. 点了「灌数据」前端报超时？
属正常现象（旧同步版本），新版已改异步。确认 status 接口 `running:true` 即代表后台在跑，等几分钟后 `running:false` 即完成。

### Q2. 怎么看灌数进度 / 是否卡死？

查状态接口（最快）：
```bash
curl "http://<网关>/api/policy/internal/policy/status"
# 看 running 与 tables 各表行数是否在增长
```

看 pod 日志（确认当前步骤）：
```bash
kubectl -n dev get pods | grep entan
kubectl -n dev logs <demo-platform-entan-py-pod> --tail=60 | grep policy-pipeline
# 出现某步骤行但迟迟无下一步 → 该步在慢/卡；有 Traceback → 看 last_error
```

### Q3. 前端某 Tab 报 500 / "no such table"？
说明该后端表还没灌数（如 SQLite 空库或 PG 未跑）。点「灌数据」或确认 `POLAN_RUN_ON_START` / 后端配置。

### Q4. 图谱 Tab 没数据？
B+ Nebula 默认跳过，图谱用 `policy_graph_node/edge` 的 **PG/SQLite 镜像**兜底；只要第 5 步跑过即有数据。要真正灌 Nebula 需设 `POLAN_NEBULA_ENABLED=1`。

### Q5. 重复灌数会不会数据翻倍？
不会。每步先 `TRUNCATE` 再写，幂等可重跑。

---

## 10. 关键环境变量速查

| 变量 | 作用 | 默认 |
|---|---|---|
| `POLAN_DB_BACKEND` | `pg` / `sqlite` 后端选择 | 容器内检测到 `ENTAN_PG_HOST` 则 pg，否则 sqlite |
| `POLAN_RUN_ON_START` | `=1` 时 PG 后端也在 pod 启动时自举灌数 | 不设（PG 不自动跑） |
| `POLAN_NEBULA_ENABLED` | `=1` 启用 Nebula 图谱灌入 | 不设（跳过，用 PG/SQLite 镜像） |
| `POLAN_PG_*` | 政策 PG 连接参数（host/port/user/password/database） | 复用 `ENTAN_PG_*` |
| `ENTAN_PG_*` | 企业 PG 连接参数（polan 复用同库） | Helm 注入 |

---

## 11. 产出结果表清单（灌数完成后）

| 表 | 内容 | 样例行数 |
|---|---|---|
| `dwd.policy_base_info` | Mock 政策贴源明细（37 字段） | ~600 |
| `gkx_ads.ads_policy_level_dist` | 级别分布 | 6 |
| `gkx_ads.ads_policy_type_dist` | 类型分布 | 5 |
| `gkx_ads.ads_policy_timeseries` | 时序趋势 | 9 |
| `gkx_ads.ads_policy_national_dist` | 全国分布 | 31 |
| `gkx_ads.ads_policy_sz_dist` | 深圳区县分布 | 9 |
| `gkx_ads.ads_policy_entity` | NER 实体 | ~7517 |
| `gkx_ads.policy_graph_node` | 图谱节点 | 806 |
| `gkx_ads.policy_graph_edge` | 图谱边 | 3726 |
| `gkx_ads.ads_policy_focus` | 焦点识别 + 机遇(C5，region 行) | 631 |
| `gkx_ads.ads_policy_intensity` | 力度评估 | 631 |
| `gkx_ads.ads_policy_effect` | 效果(C3)/短板(C4)/布局(C6)，按 `scope_type` 区分 | 93 |
| `gkx_ads.ads_policy_metric_timeseries` | 效果指标时序（C3 附产） | — |
| `gkx_ads.ads_policy_text_parse` | 文本解析 | 600 |
| `gkx_ads.ads_policy_match` | 匹配推送 | 144 |
| `gkx_ads.ads_policy_simulate` | 效果推演 | 36 |

> 行数随 Mock 随机种子与算法阈值略有浮动，以 status 接口实际为准。

---

## 12. 一句话总结

> 灌数 = 在目标库（部署环境为与企业同一个 PostgreSQL）从零跑通 polan 政策算法 15 步流水线，幂等写满 17 张结果表；
> 部署环境用前端「灌数据」按钮**异步触发**、轮询 status 等待完成（远程 PG 约 7 分钟），数据持久化、重启不丢。
