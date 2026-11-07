# POL-L2-PC1-INDLIB-GAPFILL-L01 · 规划指标库缺项表灌数

- 任务：`POL-L2-PC1-INDLIB-GAPFILL-L01`
- 日期：2026-11-08
- 执行：`agent:data-agent` · 监管：`human:淮政玮`
- ponytail: full
- 上游：`sdd/l2/POL-L2-PC1-INDLIB-ARCH.md` / `INDLIB-DATA.md`

## 1. 范围与实现

| 项 | 内容 |
|---|---|
| 库 | `gkxlumenx_gapfill`（`10.50.11.76:3306`） |
| 表 | `gapfill_policy_indicator_lib` |
| 脚本 | `lumen-algo-py/scripts/seed_gapfill_policy_indicator_lib.py` |
| SQL | `lumen-algo-py/scripts/mysql/gapfill_policy_indicator_lib.sql` |

全部 mock：3 政策 × 四维闭集（扶持力度/适用范围/实施时效/申请条件）= **12 行**。政策 id 与 604 共用 ADS 真实 id，便于核增页同一选择器。不挂 `M_POLICY_*`，不抬升 `policy_support`。

## 2. 命令与证据

```text
python scripts/seed_gapfill_policy_indicator_lib.py --check
# → {"mode":"check","ok":true,"rows":{"total":12,"扶持力度":3,"适用范围":3,"实施时效":3,"申请条件":3}}

$env:LUMEN_ALGO_MYSQL_PASSWORD = "<secret>"
python scripts/seed_gapfill_policy_indicator_lib.py --apply
# → {"mode":"apply","connected":true,"rows":{"total":12,...四维各3}}
```

## 3. 架构合规

| 铁律 | 结果 |
|---|---|
| D16/D18 只写 gapfill | ✅ |
| 维度闭集四项、不新造 metric | ✅ |
| 全行 is_mock=1 | ✅ |

## 4. cost（占位）

完工总控回填。
