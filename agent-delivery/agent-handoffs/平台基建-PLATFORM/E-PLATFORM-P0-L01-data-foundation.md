# Data handoff · E-PLATFORM-P0-L01 数据底座 L1

| 项 | 值 |
|---|---|
| 任务 | E-PLATFORM-P0-L01 |
| Epic | E-PLATFORM-P0 |
| 角色 | data-agent |
| 分支 | `feat/E-PLATFORM-P0-L01`（demo-algo-science） |
| 性质 | 设计类 `cicd: skip` |
| 日期 | 2026-06-20 |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 产物 |
|--------|------|------|
| 冻结 ADS + gkx_dim/gkx_cfg DDL（§2–§4） | ✅ | `demo-algo-science/scripts/sql/gkx/*.sql` |
| ADS 预留 ext JSON | ✅ | 全部 ADS 表含 `ext JSON NULL` |
| 稳定业务主键定稿（§8） | ✅ | `agent-delivery/data/gkx-platform-business-keys.md` |
| Mock 生成器（固定种子、mock_ 前缀） | ✅ | `mock/ads_generator.py` + `scripts/mock_ads_generator.py` |
| data-source-mapping-registry 骨架 | ✅ | `agent-delivery/data-source-mapping-registry.yaml` v1.1 |
| 质量规则与血缘 Markdown | ✅ | `agent-delivery/data/gkx-platform-quality-lineage.md` |
| ODS/DWD 仅命名占位 | ✅ | `00_schemas.sql` 注释 + README |

## 产物清单

### Python 仓（demo-algo-science）

| 路径 | 说明 |
|------|------|
| `scripts/sql/gkx/00_schemas.sql` | CREATE DATABASE gkx_dim/gkx_cfg/gkx_ads |
| `scripts/sql/gkx/gkx_dim.sql` | dim_region / dim_industry_chain / dim_element / dim_org_master |
| `scripts/sql/gkx/gkx_cfg.sql` | cfg_metric / cfg_metric_lineage / cfg_model_registry / cfg_degrade_switch |
| `scripts/sql/gkx/gkx_ads_platform.sql` | ads_metric_timeseries / ads_policy_focus / graph_* |
| `scripts/sql/gkx/gkx_ads_ent.sql` | ads_ent_* 13 张 + ads_enterprise_score |
| `scripts/sql/gkx/README.md` | 执行顺序与 Convoy 说明 |
| `mock/gkx_db.py` | DDL 初始化连接 |
| `mock/ads_generator.py` | Mock 写入逻辑（seed=20260620） |
| `scripts/mock_ads_generator.py` | CLI 入口 |

### 编排仓（agent-delivery）

| 路径 | 说明 |
|------|------|
| `data/gkx-platform-business-keys.md` | §8 业务主键定稿 |
| `data/gkx-platform-quality-lineage.md` | DQ-P01~P15 + 血缘说明 |
| `data-source-mapping-registry.yaml` | 扩充平台+ENT ADS 骨架（source pending_source） |

## 与 L02 Convoy 文件隔离

| 区域 | L02（E-INNOV-M1-L02） | L01（本任务） | 隔离策略 |
|------|----------------------|---------------|----------|
| Pipeline | `scripts/run_all.py`、innov P1–P4 | **未修改** | Convoy 铁律 |
| innov DDL | `scripts/schema_mysql.sql` | **未修改** | 分目录 |
| 平台 DDL | — | `scripts/sql/gkx/` | 新目录 |
| Mock | `innov/mockgen/*`（ODS→innov 流水线） | `mock/ads_generator.py` | 独立模块 |
| 分支 | `feat/E-INNOV-M1-L02` | `feat/E-PLATFORM-P0-L01` | worktree 并行，禁止互 merge 至完成 |

**合并策略**：coordinator 在 L02 done 后协调 rebase；L01 文件集与 L02 无路径重叠（除共享 `requirements.txt`/`README` 未改）。

## Mock 运行说明

```bash
cd demo-algo-science
# 可选：GKX_MYSQL_* 或复用 INNOV_MYSQL_*
python scripts/mock_ads_generator.py --init-schema --generate
```

- 固定种子：`GKX_MOCK_SEED=20260620`（默认）
- 批次 ID：`mock_20260620_platform`
- 样例规模：政策 20 条、企业 50 家、时序 24 点、能力评估 30 条等

## 偏离说明

| 项 | 说明 |
|----|------|
| `gkx_dwd` 9 表 DDL | 已在 `企业域数据库设计(v1).md`，本任务仅 ADS/dim/cfg 冻结入仓；DWD 随 P1 或 ENT Wave1 落地 |
| `cfg_metric` 数据 | 49 条 ENT 种子仍在 YAML；物理 INSERT 由 P0-L02 / 后续脚本加载 |
| CI/deploy | 按任务标注 skip，未 push/未跑 Pipeline |

## 架构合规自检（§2 十条）

| # | 项 | 结果 |
|---|-----|------|
| 1 | 算法只在 Python | ✅ Mock 写入在 Python |
| 2 | 调用链不越层 | ✅ Java 只读 ADS（契约在 DDL 注释） |
| 3 | 图谱 NebulaGraph | ✅ graph_* PG 镜像预留，禁 Neo4j |
| 7 | 共享聚合核心 | ✅ gkx_ads 为契约面 |
| 8 | D7 数据契约 + Mock | ✅ ADS 冻结 + Python Mock |
| 10 | D9 血缘 | ✅ mapping registry + quality-lineage 文档 |
| 其余 | 前端/Java/CI | N/A（本任务不涉及） |

## 接力清单

| 下游 | 动作 |
|------|------|
| **api-agent P0-L02** | 基于 `gkx_cfg.cfg_metric` 实现 GET `/metrics/v1/catalog` |
| **algorithm-agent P0-L03/L04** | graph_* 灌 Nebula；cfg_model_registry 样例 |
| **data-agent P1-L01** | 三方源就绪后 ODS/DWD + mapping status→verified |
| **coordinator** | L02 完成后协调 demo-algo-science 双分支合并 |

## cost 回填

| 字段 | 值 |
|------|-----|
| estimated_tokens | 400_000 |
| actual_tokens | 185_000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.37 |
| cost_warn | green |

## git

- 分支：`feat/E-PLATFORM-P0-L01`
- commit message 建议：`[agent:data-agent] E-PLATFORM-P0-L01 gkx platform DDL + Mock ADS generator`
- **未 push**（设计类 skip CI；由人类/coordinator 择机提交）

---

*handoff · data-agent · E-PLATFORM-P0-L01*
