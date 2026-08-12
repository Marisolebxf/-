# Handoff — GDF-ENT-LIVE-PROBE-WEEKLY

> **任务**：企业维三方源 `dwd_*` 承诺表 live 齐套周期复核  
> **责任人 / 监管**：`human:郭万迎`  
> **协助 Agent**：`data-agent`（可选，跑只读探测脚本）  
> **登记日**：2026-08-01  
> **标记**：`[agent:data-agent]`（派单登记）

## 1. 范围

- **周期**：每周至少 1 次（`cadence: weekly`；`next_due` 见 `task-registry.yaml`）  
- **对象**：Wave A 承诺 40 表（`GDF-ENT-WORKPACK-v1/02-WaveA-贴源表清单.yaml`）  
- **库**：MySQL `gkx` 只读（见 `gkx-mysql-raw/CONNECTION.md` + 本地 `.env.local`）  
- **禁止**：写源库；仅用 Navicat「行」/ `TABLE_ROWS` 下结论  

## 2. 标准作业

1. 运行 `gkx-mysql-raw/加工/_probe_live_dwd_enterprise.py`（或等价 `COUNT(*)`）  
2. 落盘 `加工/LIVE-DWD-ENTERPRISE-READINESS-YYYY-MM-DD.md`  
3. 更新 `third-party-source/SUPPLIER-LOAD-PROGRESS.md` 当周摘要  
4. 异常（主表骤降 / 新增缺表 / 与口头进度严重偏离）当日飞书知会数据 Lead / GDF  

## 3. 已有基线

### 2026-08-01
- 报告：`加工/LIVE-DWD-ENTERPRISE-READINESS-2026-08-01.md`  
- 要点：`dwd_org_base_info`=20,000；承诺 36/40 存在、13/40 有行；P0 有行 9/17；**未齐备但可烟测**

### 2026-08-04
- 报告：`加工/LIVE-DWD-ENTERPRISE-READINESS-2026-08-04.md`  
- 要点：有数据 **30/40**；P0 有行 **14/17**；主表仍 20,000；昨清零路径多数回灌；**未齐备，烟测路径可加宽**

### 2026-08-07 ⚠️
- 报告：`加工/LIVE-DWD-ENTERPRISE-READINESS-2026-08-07.md`  
- 要点：有数据 **30/40**；P0 有行 **15/17**；双标签回灌；但 **2×P0 表 MISSING**（经营/要闻）、失信清零

### 2026-08-10 ⚠️
- 报告：`加工/LIVE-DWD-ENTERPRISE-READINESS-2026-08-10.md`  
- 要点：存在 **39/40**；有数据 **27/40**；P0 全在且经营/要闻恢复；高校/澳门等多表清零；样例继续轮换

### 2026-08-12（最近一次）✅
- 报告：`加工/LIVE-DWD-ENTERPRISE-READINESS-2026-08-12.md`  
- 要点：有数据 **35/40**；**P0 首次全有数 17/17**；无新清零；主表仍 20,000；仍缺 college、失信等空  
- `next_due`：`2026-08-19`

## 4. 关单说明

本任务为**常驻周期项**，单次复核完成**不**改为 `done`；保持 `ready`，滚动更新 `next_due` 与 evidence。
