# agent-delivery/data — 数据资产目录

> 整理日期：2026-07-22（PM：归集垂向设计 / 清理历史 Excel·SQL / Mapping 分垂向 / 源表与加工分离）

## 目录结构

```text
data/
├── README.md                          ← 本说明
├── DS-25-data-availability-matrix.md  ← 试点可用性矩阵（保留）
├── gkx-platform-*.md                  ← 平台级业务键 / 质量血缘（保留）
├── data-design/                       ← 自建库 / 垂向数据库设计（当前在用）
│   ├── 企业/
│   ├── 产业链/
│   ├── 政策/
│   ├── 服务机构/
│   └── _公共/                         ← 跨垂向参考清单
├── GDF/
│   └── Mapping/                       ← 数据工厂字段映射（按垂向）
│       ├── 企业/
│       ├── 产业链/
│       ├── 政策/
│       └── 服务机构/
└── third-party-source/                ← 外部数据源结构
    └── gkx-mysql-raw/                 ← 根目录=已确认源表；加工/ = 映射约束与全量对照
```

## 放哪里

| 内容类型 | 目录 |
|----------|------|
| 垂向数据库设计 MD / ES 设计等 | `data-design/{企业\|产业链\|政策\|服务机构}/` |
| ODS→DWD 映射分析报告 | `GDF/Mapping/{垂向}/` |
| 三方/外部**源表结构** | `third-party-source/`（入站细节见 `gkx-mysql-raw/SOURCE-TABLES.md`） |
| 历史 Excel / 旧要素库 SQL | **已删除**；有最新文件再更新 |

## 注意

- 供应方 `dwd_*` ≠ 项目自建 DWD；勿混名。
- 改任务状态/看板请走 `scripts/update-task-status.ps1`，与本目录整理无关。
