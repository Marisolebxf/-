# DEMO-ENT-LLM-ODS-L01 · LLM→约定 ODS（关 OPEN-ENT-FLOW-06）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最小脚本：md-extract CSV→建表/插数；offline 默认；可选 LLM；`--sql-out` 绕过无建库权限 |

## 修改内容

### demo-algo-ent-analysis

- `entan/llm_ods/`：schema / generate / load / self_check / README  
- `scripts/run_llm_ods.py`  
- `.gitignore` 加 `out/`

### gkx-orchestration

- `pipeline-demo-mock.md` / seeds / 流图 OPEN-06 → **已关闭**  
- CHANGELOG / etl README

## 测试结果

- `py -3 scripts/run_llm_ods.py --self-check` → OK（5 张 P0 表）  
- `--offline --sql-out out/demo_gkxlumenx_ods.sql` → OK  
- `--offline` 直写库：`1044 Access denied` 创建 `demo_gkxlumenx_ods`（**需 DBA 授权**；已登记，不阻塞脚本落仓）

## 遗留

| 项 | 说明 |
|---|---|
| DBA | `CREATE DATABASE demo_gkxlumenx_ods` + 授权 `gkxlumenx` |
| 扩表 | 招投标/产业链/风险 CSV 要素库尚未纳入 REQUIRED |
| ETL 模拟 GDF | ODS→DWD 仍走既有管道；本单只关灌 ODS 入口 |

## 架构合规

| 项 | 结果 |
|---|---|
| ODS 真源 = doc/md-extract | ✅ |
| 不以 gkx-mysql-raw | ✅ |
| 算法在 Python | ✅ |
| mockgen 仍标旁路 | ✅ |

## CI/CD

- 仓：`demo-algo-ent-analysis` main · `gkx-orchestration` dev  
- 纯脚本 + 文档

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~100k（估） |
| model_used | Cursor Grok 4.5 |
| actual_cost | <$3 |
| cost_warn | false |

## 联调确认

OPEN-ENT-FLOW-06 **关闭**（脚本+自检+sql-out）；直写库待 DBA。会签通过（文档口径已回写）。
