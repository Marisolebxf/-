---
name: gkx-yuansuku-live-snapshot
description: >-
  Runs the full 20-要素库 Excel vs live MySQL gkx row-count and schema-diff
  snapshot (gen_schema_diff_report.py), writes a dated summary against the
  last in-repo report, and updates 加工/README.md. Use when the user says
  执行一次快照, 跑行数报告, 要素库对照, gen_schema_diff_report, or
  数据源表及行数报告. Not for enterprise Wave A 40-table probes
  (LIVE-DWD-ENTERPRISE) or TOPIC-METRIC coverage.
---

# 全要素库 live 快照

执行真源在 `agent-delivery/data/third-party-source/gkx-mysql-raw/加工/`（脚本 + `要素库xlsx/`）。本 Skill 只规定怎么跑、怎么环比、怎么对人说。不要把脚本复制进本目录。

Codex 同文入口：`.codex/skills/gkx-yuansuku-live-snapshot/`（短指针；改流程先改本文件）。

## 何时开工 / 何时不要用

**开工**：用户说「执行一次快照」/「跑行数报告」/「要素库对照 live」，或点名 `gen_schema_diff_report.py`。

**不要用本 Skill**：

- 只要企业 Wave A 40 表齐套 → `_probe_live_dwd_enterprise.py` / `LIVE-DWD-ENTERPRISE-READINESS-*.md`
- 专题指标覆盖 → `TOPIC-METRIC-SOURCE-COVERAGE-*`
- 用户只要解读已有报告、不连库

## 标准顺序

```
- [ ] 1. 确认 Excel 与 .env.local
- [ ] 2. 短连库烟测
- [ ] 3. python gen_schema_diff_report.py
- [ ] 4. 相对仓内上一份行数报告写摘要
- [ ] 5. 更新 加工/README.md 最新指针
- [ ] 6. 对人汇报；未点名不 commit
```

### 1. 确认输入

工作目录（PowerShell `working_directory` 必须指到这里）：

`agent-delivery/data/third-party-source/gkx-mysql-raw/加工`

| 依赖 | 路径 |
|------|------|
| Excel | `要素库xlsx/*.xlsx`（可用 `GKX_YUANSUKU_XLSX_DIR` 覆盖） |
| 密码 | 上一级 `.env.local`（gitignore；**禁止打印密码**） |
| 推荐脚本 | `gen_schema_diff_report.py`（行数 + Excel↔库字段差） |

缺 xlsx 或 `.env.local`：停止并报告缺口，不要猜连接串。

### 2. 烟测

`$env:PYTHONUNBUFFERED = "1"`。先短连：

```powershell
python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('.').resolve())); from update_row_counts import load_env, ENV_PATH, connect; env=load_env(ENV_PATH); conn=connect(env); cur=conn.cursor(); cur.execute('SELECT VERSION(), DATABASE(), CURRENT_USER()'); print('OK', cur.fetchone()); conn.close()"
```

`WinError 10060` / OperationalError 2003：等几十秒再试一次。端口探活 `TcpTestSucceeded` 只能作旁证，以 pymysql 为准。不要为此改脚本加功能。

### 3. 全量快照

`block_until_ms` 按全表 `COUNT(*)` 给足（建议 ≥ 900000）。

```powershell
python gen_schema_diff_report.py
```

成功时 stdout 末尾有 `==== SUMMARY ====` 和 `updated: ...GKX数据源表及行数报告-YYYYMMDD-HHMM.MD`。新报告必须落在 `加工/`（`_yuansuku_paths.report_dir`），不是 D 盘离线目录。

只抽 Excel、不连库：`gen_gkx_report.py`。只要行数不要结构差：`update_row_counts.py`。日常默认前者不跑。

### 4. 环比与摘要（易错）

脚本内 `find_previous_report` 会扫 `加工/` **以及**本机 `D:\...\数据库表-20260812` 等离线目录，可能把同日另一次未入仓跑数当成「上次」，造成假「无行数变化」。

**对人摘要的对比基准**：仓内上一份 `加工/GKX数据源表及行数报告-*.MD`（按文件名时间戳，排除刚写出的本次文件）。不要用 D 盘文件当有意义环比。

写 `加工/GKX数据源表差异分析摘要-YYYYMMDD.md`，至少含：

- 生成时刻、完整报告文件名、仓内对比基准文件名
- 库内 BASE TABLE 数、匹配计数、有数据表数、库中无此表数（相对仓内上一份）
- 分要素库：有数据 / 0 行 / 库中无此表
- 回灌 vs 抽空（行数变化绝对值大的表）
- 仍成片缺失：海洋 `hycy_*`、量子 `company_*`/`ods_quantum_*`、外文论文、行业分析无前缀文档维（以当次 missing 清单为准）

可用 `update_row_counts.parse_report_inventory` 解析两份报告再写摘要；写完删一次性辅助脚本。

### 5. README

更新 `加工/README.md`「数据源表分析」表：最新摘要、最新全量报告、上一仓内快照。日期写死到文件名，不要写「昨日」这类会过期的词。

### 6. 对人怎么说

先给文件路径，再给相对仓内上一份的数字表，再列回灌/抽空/仍缺。默认 `is_deleted=0` 为业务行；括号「全表 N」表示物理行在、业务行被删除标记滤掉。

**禁止**：打印密码；把 `ods_*` 当正式入站工作面；把 TOPIC-METRIC / `_tmp_*` / 企业齐套探测混进这次交付；用户未说 `commit`/`push` 就提交。

## 铁律

- 入站正式工作面 = 供应方 `dwd_*`；缺表登记待核验，勿自行认定下线。
- 路径用 `agent-delivery/...` 相对主仓，禁止把盘符工作根写进 Skill。
- Shell 按 `.cursor/rules/00-shell-powershell.mdc`：不用 `&&`，中文路径加引号。
