# repro/ —— 指标复现脚本与实测产物（20261021 改源工程批）

> **是什么**：565 份指标信息 MD（`../calc-logic/{域}/M_*.md`）配套的 gkx 只读复现脚本与当日实测产物。
> 2026-10-24 依淮政玮反馈从本地 `local-workspace/…/20261021_指标整体开发进度调研/code/` 入仓——
> **本目录是 GitLab 上唯一可见的复现副本**；本地 `code/` 仍是工作底稿（含 `_snapshots21/` 等大缓存，不入仓）。

## 目录结构

```
repro/
├── README.md          ← 本文件
├── _gkxdb.py          ← gkx 库（183.240.141.251:3318 只读）统一连接入口，全部脚本共用
├── M_{指标ID}.py       ← 每指标一份复现脚本（560 份；连库只读、零写操作）
└── out/
    └── M_{指标ID}_out.json ← 对应当日实测产物（565 份 MD 的数字真源）
```

## 复现方式

```bash
cd agent-delivery/metrics/repro
python3 M_{指标ID}.py        # 约几秒：全表拉取后本地聚合，产出 out/{ID}_out.json
```

- 脚本从环境变量或 `local-workspace/config/database_env.yaml` 读 gkx 凭据（只读账号）；
- 产物 `out/` 是**当日快照**：重跑会因源库数据增长产生合理漂移，与 MD 数值对照时以 MD 记录的实测日期为准；
- `18 份早期批次件（CHAIN/ENT）`无本批脚本（口径早在库、无 gkx 复现步），其 calc-logic MD 本就自包含。

## 与 calc-logic MD 的对应关系

每份 `../calc-logic/{域}/{ID}.md` 的「溯源与复现」表登记本目录路径：
`复现脚本 = metrics/repro/{ID}.py`、`复现产物 = metrics/repro/out/{ID}_out.json`。
MD 内不再出现 `local-workspace/` 路径（2026-10-24 已全量清除，避免验收方找不到路径）。
