# SVC · Demo / 约定 ODS 全链路（模拟 GDF）

> **口径**：对齐 ENT / CHAIN `pipeline-demo-mock.md`；SVC S1 锁定真源、库名与 **不复制机构主表**。  
> **建表 Owner**：`human:侯佳伟`（`DATA-SVC-STORAGE-S2-L01`，依赖本流图人签）  
> 流图：[`../01-data-flow.md`](../01-data-flow.md) §7

```yaml
---
doc_id: SVC-ETL-DEMO-MOCK
element: SVC
role: etl
status: draft
version: "2026-08-14"
updated: "2026-08-14"
engine: multi
---
```

## 1. 意图

Demo 灌数基于 **ETL 调度模拟 GDF**。ODS 结构以 **`third-party-source/doc/`** 为准（优先 `md-extract/` **国内机构要素库**），不以现网 as-built / L01 实查为准。落 `demo_*`。

## 2. 主路径

```text
约定文档(md-extract 国内机构要素库)
  → 复用/核对 demo_gkxlumenx_ods（与 ENT 同实例）
  → ETL 模拟 GDF → ENT 机构 DWD
  → SVC 圈定（Demo 临时规则 · 待核验）
  → demo_* SVC DWD / ADS / ES / Nebula / MinIO
```

## 3. 命名表

| 角色 | 开发默认 | 禁止作 Demo 默认 |
|---|---|---|
| MySQL ODS | `demo_gkxlumenx_ods` | `gkxlumenx_ods` |
| MySQL DWD | `demo_gkxlumenx_dwd` | `gkxlumenx_dwd` |
| MySQL ADS | `demo_gkxlumenx_ads` | `gkxlumenx_ads` |
| MinIO | `demo_**` 桶 | 正式桶当 Demo 默认 |
| Nebula | `demo_**` space | 正式 space 当 Demo 默认 |

## 4. S2 待回填

| 项 | 说明 |
|---|---|
| 入口脚本 | 优先复用 ENT `entan/llm_ods` / 同构 CHAIN `run_chain_ods.py` 模式；**禁止**平行第二套机构主表 DDL |
| 对列 | 按 md-extract 核对 `industry*` 等文档列（Q-SVC-009） |
| 圈定样例 | seeds 必须标待核验（Q-SVC-010） |

## 5. 禁止

- 以现网三方 as-built、L01 `SHOW CREATE`、或未对齐 `doc/` 的草稿当 Demo ODS 真源  
- 复制 `dwd_org_base_info` 到 SVC 名下  
- 写正式 `gkxlumenx_*`  
- 第二套表结构 / 直写 ADS 冒充全链路  
- 把 Demo 临时准入口径写成正式契约  
