# agent-delivery/data — 数据资产目录

> 最近整理：2026-07-22（PM：归集垂向库设计 / 清理历史 Excel·SQL / Mapping 可执行 / 源表与加工分离）  
> **解耦决策补记：2026-07-28（项目负责人）**：供应库 `dwd_*` = 本项目 **ODS**；项目自研 DWD 由架构师按需求设计，**不与 ODS 一一对应**；8/20 ODS 稳定后由 **GDF** 做映射。详见 `data-lineage-policy.md` §2.2。

## 目录结构

```text
data/
├── README.md                          ← 本说明
├── DS-25-data-availability-matrix.md  ← 试点数据可用性矩阵（保留）
├── gkx-platform-*.md                  ← 平台级业务键 / 质量血缘等说明
├── data-design/                       ← 项目自研 DWD / 垂向库设计（对接层）
│   ├── _templates/                    ← DWD 表设计契约模板（含 ods_mapping_expectation）
│   ├── 企业/
│   ├── 产业链/
│   ├── 政策/
│   ├── 服务机构/
│   └── _公共/                         ← 跨要素参考清单
├── GDF/
│   └── Mapping/                       ← 数据工厂字段映射（Phase 2 主战场）
│       ├── 企业/
│       ├── 产业链/
│       ├── 政策/
│       └── 服务机构/
└── third-party-source/                ← 外部贴源结构（= 本项目 ODS）
    └── gkx-mysql-raw/                 ← 入站真源；加工/ = 映射约束与全量清单
```

## 怎么找

| 你在找什么 | 目录 |
|------------|------|
| **项目自研 DWD 设计契约**（Phase 1） | `data-design/_templates/dwd-table-contract-template.md` → 复制到各要素目录 |
| 垂向库设计 MD / ES 索引等 | `data-design/{企业\|产业链\|政策\|服务机构}/` |
| ODS→项目 DWD 映射（Phase 2） | `GDF/Mapping/{要素}/` |
| 甲方/外部**源表结构**（实质 ODS） | `third-party-source/`（站内细节见 `gkx-mysql-raw/SOURCE-TABLES.md`） |
| ODS 连接元数据（只读） | `third-party-source/gkx-mysql-raw/CONNECTION.md`（**密码不进仓**） |
| 历史 Excel / 要素库旧 SQL | **已删除**；有备份文件再恢复 |

## 两阶段工作约定（2026-07-28）

| 阶段 | 时间 | 做什么 | 不做什么 |
|------|------|--------|----------|
| **Phase 1** | 现在 ~ 2026-08-20 | 架构师按需求设计**项目自研 DWD**；metric `source_tables` 指向项目 DWD；`mapping_status: ⏳ pending_ods` | **不做** ODS→DWD 一一映射；不把供应库表当项目 DWD |
| **Phase 2** | 2026-08-20 后 | GDF 产出映射；lineage 验证；升级 `mapping_status`；补 ETL | — |

## 注意

- **供应商 `dwd_*` ≠ 项目对接 DWD（解耦）**。供应库里的 `dwd_*` 是本项目的 **ODS 源表**；项目 DWD 表名/字段由架构师自研。
- 密码与密钥只放本地 `.env.local`（已 gitignore），禁止写入本目录 Markdown。
- 任务状态/看板请走 `scripts/update-task-status.ps1`，与本目录资产无关。
