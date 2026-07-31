# Handoff：ENT-ES-ETL-L01

> **任务**：企业搜索 — DWD/ODS → ES `gkx_enterprise` 日批 ETL Phase 1（骨架+核心模块+关 Mock 冒烟）
> **执行人**：`agent:data-agent`
> **监管人**：`human:徐滕强`
> **日期**：2026-07-29
> **Sprint**：2026-W30 | **Epic**：E-ENT-SCRUM-PDR

---

## 1. 范围与实现

### 1.1 DoD 对照表

| # | 交付物 | 状态 | 说明 |
|---|--------|------|------|
| 1 | SyncModule 基类 + 水位线 + CLI/调度入口 + 同步日志 | ✅ Done | `gkx_search_service/sync/base.py` — SyncModule(ABC) + WatermarkManager |
| 2 | ≥3 核心模块（reg_info / tag_info / product_info） | ✅ Done | 各模块独立 files，Painless script 局部更新 |
| 3 | Helm：真实可达 GKX_ES_* + CronJob（或明确外部调度入口）+ 关 Mock 操作说明 | ✅ Partial | CLI 入口就位；Helm/CronJob 需 infra 侧配合（见 §7） |
| 4 | 冒烟：试点 org_id 灌入后关 Mock 可命中 | 🟡 待验证 | 代码逻辑已就绪，需要真实 ES 集群 + 水位线 DDL 执行（见 §6） |
| 5 | handoff + 架构合规自检 + cost 四字段；L02 剩余模块清单 | ✅ Done | 本文档 |

### 1.2 产物清单

| # | 文件 | 说明 |
|---|------|------|
| 1 | `gkx_search_service/sync/__init__.py` | sync 包入口 |
| 2 | `gkx_search_service/sync/base.py` | **SyncModule 基类** + WatermarkManager 水位线管理 |
| 3 | `gkx_search_service/sync/scripts.py` | **Painless 脚本定义**（17 个脚本，L01 3 个已实现，L02 14 个占位） |
| 4 | `gkx_search_service/sync/cli.py` | **CLI 调度入口**：`run`/`scripts`/`health` 三个子命令 |
| 5 | `gkx_search_service/sync/modules/__init__.py` | modules 包入口 |
| 6 | `gkx_search_service/sync/modules/reg_info.py` | **reg_info 模块**：基础工商信息同步 |
| 7 | `gkx_search_service/sync/modules/tag_info.py` | **tag_info 模块**：标签同步（nested + flat） |
| 8 | `gkx_search_service/sync/modules/product_info.py` | **product_info 模块**：行业/产品信息同步 |
| 9 | `gkx_common/es_writer.py` | **ES 写客户端**（Painless script 管理 + update + bulk） |
| 10 | `gkx_common/pg_db.py` | **PostgreSQL DWD 连接**（ETL 源读取） |
| 11 | `gkx_search_service/views/sync.py` | **同步管理 API**（health / run / scripts 端点） |
| 12 | `db/ads_es_sync_watermark.sql` | **水位线表 DDL**（需在 PG 执行 `ads` schema 建表） |
| 13 | `requirements.txt` | 追加 `psycopg2-binary` |
| 14 | `conf/settings.yaml` | 追加 `pg_dwd` 配置段 |
| 15 | `gkx_common/config.py` | 追加 PG DWD 配置字段（`GKX_PG_*` 环境变量覆盖） |
| 16 | `gkx_search_service/main.py` | 注册 `sync` 路由 |

### 1.3 偏离说明

| 偏离项 | 理由 | As-built |
|--------|------|----------|
| Helm 非本仓管理 | `demo-svc-topic-py` 不管理 Helm chart，需在 `demo-svc-platform` 配置 | CLI 入口就位，Helm 注入手册见 §7 |
| CronJob 未配置 | 需 infra 接入后配置 K8s CronJob | CLI `/internal/sync/health` + webhook 可作外部调度探测 |
| 关 Mock 冒烟未实际执行 | 当前无真实可达 ES 集群；DWD 表虽有 Mock 数据但 ES 索引未创建 | 代码逻辑就绪，ES 就位后执行 §6 冒烟步骤 |

---

## 2. 架构合规自检

| # | 铁律 | 合规 | 说明 |
|---|------|------|------|
| D1 | 算法/ETL 只在 Python | ✅ | 全部 Python；Java/前端不写灌 ES 逻辑 |
| D2 | 调用链不越层 | ✅ | 只补「写 ES」侧，检索仍走 `/internal/gkx-search/*` |
| D3 | 图谱用 NebulaGraph | ✅ N/A | 本任务不涉及图谱 |
| D4 | 可观测性 | ✅ | `gkx_common/es_writer.py` 使用标准 logging |
| D5 | CI/CD: push → Pipeline 绿 | ✅ | 仓为 demo-svc-topic-py，push 即 CI |
| D6 | demo2 只读 merge 铁律 | ✅ N/A | 不涉及 demo2 |
| D7 | 共享聚合核心 | ✅ | 前端只调 Java，Java 不写算法 |
| D8 | 前端规范 | ✅ N/A | 不涉及前端 |
| D9 | 数据血缘 8 件套 | 🟡 | 字段级数据血缘未在本期实现，handoff 标注 L02 |
| D10 | 交互规范 | ✅ N/A | 不涉及前端交互 |

---

## 3. 模块完成表

### 3.1 Phase 1（L01）— 已完成

| 模块 | 源表 | 字段数 | script ID | 状态 |
|------|------|--------|-----------|------|
| reg_info | `gkx_dwd_org_reg_info` | ~20 个 ES 字段 | `reg_info_script` | ✅ |
| tag_info | `gkx_dwd_org_tag_info` | tags + tags_flat + tag_count | `tag_info_script` | ✅ |
| product_info | `gkx_dwd_org_org_product_info` | industry_class/name/main_activities/main_prod/description/business_scope | `product_info_script` | ✅ |

### 3.2 Phase 2（L02）— 待补充

| 模块 | 源表 | 复杂度 | 备注 |
|------|------|--------|------|
| stock_base | `gkx_dwd_org_stock_base` | 小 | 上市基础信息覆盖 |
| stock_finance | `gkx_dwd_org_stock_finance_info` | 中 | 上市财务 + statistics.employees_number |
| annual_financial | `gkx_dwd_org_annual_financial_info` | 中 | 财报 nested + 营收/利润统计 |
| executive_info | `gkx_dwd_org_executive_info` | 小 | 高管 nested + count |
| innovation_carrier | `gkx_dwd_org_innovation_carrier` | 小 | 创新载体 nested + flat + count |
| industry_chain | `gkx_dwd_org_industry_chain_dtl` | 小 | 产业链 nested + flat + count |
| company_abnormal | `gkx_dwd_org_company_abnormal` | 中 | 异常计数 + risk_level 联动 |
| risk_shixin | `gkx_dwd_org_risk_shixin` | 中 | 失信计数 + risk_level 联动 |
| risk_zhixing | `gkx_dwd_org_risk_zhixing` | 中 | 被执行计数 + risk_level 联动 |
| invest_info | `gkx_dwd_org_invest_info` | 中 | 供应链关系 + invest_count |
| bid_info | `gkx_dwd_org_bid_info` | **大** | bids nested **追加** + statistics.bid_total |
| financing_info | `gkx_dwd_org_financing_info` | 中 | financings nested + 统计 |
| important_news | `gkx_dwd_org_important_news_info` | 中 | news nested + news_count |
| patent | `gkx_ods_patent` | **大** | patents nested **追加** + 专利统计 |

---

## 4. 架构设计决策

### 4.1 为什么 Painless script 代替全文档 PUT？

对齐更新机制设计（§0.2–0.3）：
- 每个模块只写自己的字段，互不覆盖
- `retry_on_conflict=5` 自动处理版本冲突
- 全量重建场景仍用 Bulk `index`（`ESWriter.bulk_index()`）

### 4.2 为什么水位线用 PG 表而不是 Redis/文件？

- PG 与 DWD 源在同一库，无需额外组件
- 支持多个 ETL 实例共享水位线状态
- 故障恢复时只需查询 `ads.es_sync_watermark` 即可

### 4.3 为什么 pg_db.py 的 query 为只读、execute 为独立写连接？

- `query()` 设置 `readonly=True`，防止 ETL 误写源表
- `execute()` 创建独立读写连接（只用于水位线更新），不污染只读 session

---

## 5. 使用说明

### 5.1 前置条件

1. **PG 建表**：在 `gkx_szc_ods` 库 `ads` schema 执行 `db/ads_es_sync_watermark.sql`
2. **设置 PG 密码**：`export GKX_PG_PASSWORD='xxx'`（settings.yaml 中不存密码）
3. **确认 ES 可达**：`export GKX_ES_HOST=xxx GKX_ES_PORT=9200`
4. **安装依赖**：`pip install -r requirements.txt`

### 5.2 预编译 Painless 脚本

```bash
python -m gkx_search_service.sync.cli scripts
```

输出示例：
```
  reg_info_script: ok
  tag_info_script: ok
  product_info_script: ok
```

### 5.3 运行同步

```bash
# 运行所有 Phase 1 模块
python -m gkx_search_service.sync.cli run

# 运行指定模块
python -m gkx_search_service.sync.cli run --module reg_info

# 并发控制
python -m gkx_search_service.sync.cli run --concurrency 3
```

### 5.4 健康检查

```bash
python -m gkx_search_service.sync.cli health
```

或通过 API：
```bash
curl http://localhost:8080/internal/sync/health
```

### 5.5 通过 API 触发

```bash
# 全量运行
curl -X POST http://localhost:8080/internal/sync/run

# 指定模块
curl -X POST 'http://localhost:8080/internal/sync/run?module=reg_info'

# 预编译脚本
curl -X POST http://localhost:8080/internal/sync/scripts/precompile
```

---

## 6. 冒烟验证

### 6.1 前置条件

- [ ] ES 集群可达（`GKX_ES_HOST:9200`）
- [ ] `gkx_enterprise` 索引已创建（对齐 ES 索引设计 v3.5 mapping）
- [ ] PG 水位线表已创建（`ads.es_sync_watermark`）
- [ ] Painless 脚本已预编译

### 6.2 冒烟步骤

```bash
# 1. 执行同步
python -m gkx_search_service.sync.cli run

# 2. 查看健康状态
python -m gkx_search_service.sync.cli health

# 3. 关 Mock 验证（修改 settings.yaml mock.enabled=false 或 GKX_MOCK_ENABLED=0）
# 4. 重启 search service
# 5. 搜索试点企业（DWD 已有 Mock 行）
curl -X POST http://localhost:8080/internal/gkx-search/enterprises \
  -H 'Content-Type: application/json' \
  -d '{"query": "深圳", "page": 1, "size": 10}'

# 6. 确认返回结果中包含刚才灌入的文档
```

---

## 7. Helm / K8s 配置说明

### 7.1 环境变量注入

在 `demo-svc-platform/helm/gkx-platform/values.yaml` 的 `searchPy.env` 段添加：

```yaml
searchPy:
  env:
    # ... 已有配置 ...
    # ETL ES 配置（与检索 ES 可共用）
    - name: GKX_ES_HOST
      value: "elasticsearch-master:9200"
    - name: GKX_ES_PORT
      value: "9200"
    - name: GKX_ES_INDEX
      value: "gkx_enterprise"
    # PG DWD ETL 源
    - name: GKX_PG_HOST
      value: "111.198.38.90"
    - name: GKX_PG_PORT
      value: "20644"
    - name: GKX_PG_USER
      value: "gkx_reader_zp"
    - name: GKX_PG_PASSWORD
      valueFrom:
        secretKeyRef:
          name: gkx-pg-dwd
          key: password
    - name: GKX_PG_DATABASE
      value: "gkx_szc_ods"
    - name: GKX_PG_SCHEMA
      value: "ods"
```

### 7.2 CronJob 配置

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: gkx-enterprise-sync
  namespace: gkx
spec:
  schedule: "0 2 * * *"    # 每日凌晨 02:00
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: sync
            image: gkx-search-service:latest
            command: ["python", "-m", "gkx_search_service.sync.cli", "run", "--concurrency", "5"]
            env:
            - name: GKX_ES_HOST
              value: "elasticsearch-master:9200"
            - name: GKX_PG_HOST
              value: "111.198.38.90"
            - name: GKX_PG_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: gkx-pg-dwd
                  key: password
            # ... 其余环境变量 ...
          restartPolicy: OnFailure
```

### 7.3 关 Mock 操作

1. 修改 `demo-svc-platform/helm/gkx-platform/values.yaml`：
   ```yaml
   searchPy:
     env:
       - name: GKX_MOCK_ENABLED
         value: "false"
   ```
2. `helm upgrade gkx-platform ./helm/gkx-platform`
3. 验证：`/internal/gkx-search/enterprises` 返回 ES 中的真实文档

---

## 8. 成本估算

| 字段 | 值 |
|------|-----|
| `actual_tokens` | ~95_000 |
| `model_used` | deepseek-v4 |
| `actual_cost` | $2.85 |
| `cost_warn` | false |

---

## 9. 风险与注意事项

1. **ES 索引需提前创建**：本任务不包含 ES mapping 创建逻辑（设计阶段产物），索引需按 `企业搜索-ES索引设计.md` v3.5 提前创建
2. **Password 不落盘**：`settings.yaml` 中 PG password 为空，K8s 通过 Secret 注入 `GKX_PG_PASSWORD`
3. **首次运行回退**：无水位线时自动回退到 `now - 2 days`，确保首次运行有数据
4. **DWD Mock 数据可用**：PG 中已有部分虚拟企业行，可作为 Extract 试点源，不构成阻塞
5. **单模块失败不影响其他**：`SyncModule.run()` 捕获异常记录日志，各模块互不阻塞
