# KG-GRAPH-COVER-01 执行证据（验收入口）

- 执行：human:白鑫凤，2026-11-17 21:20–22:25；对应[对账总表](../KG-GRAPH-COVER-01-覆盖补齐对账.md) §二 批次台账
- 本目录文件均由执行脚本当日产出，原样拷贝（哈希见 [MANIFEST.sha256.md](./MANIFEST.sha256.md)）；凭据不入任何文件

## 文件说明

| 文件 | 内容 |
|---|---|
| `trial_result.json` / `trial_pairs.json` | 第 0 步 1 万条试写：结果（含首试 SemanticError 报错原样留证）与试写端点对清单 |
| `s1_checkpoint.json` / `s1_batch_log.csv` | s1 建 17,227 个机构点：断点状态与 35 小批逐批日志 |
| `s2_checkpoint.json` / `s2_batch_log.csv` | s2 机构边 12 批：逐批时间/条数/探活/抽验/增量 + 中段 MIDCOUNT 行 + 终值 FINAL 行（末行 DRY 为修复后幂等复跑验证：新写 0、终值=期望） |
| `s2_apply_console.log` | s2 正式跑完整控制台输出（12 批全绿 + 中段/终段两次全量 count 对账） |
| `s3_checkpoint.json` / `s3_batch_log.csv` / `s3_diff_pairs.json` | s3 tech_rel 差分：日志与**实际写入的 45,824 对清单** |
| `s4_checkpoint.json` / `s4_batch_log.csv` | s4 community_id 回填日志与校验（19,430 ✅） |
| `missing_institutions_fields.csv` | s1 输入：17,227 个缺失机构点的源侧字段（name_zh 仅 184 家有值） |
| `legacy_pairs_not_in_source.json` | **图内遗留 2,110 对的逐对清单与定性**（全部 is_company=1 企业行，源表均在） |
| `signoff_counts.json` | SIGNOFF-06 回签 24 行 + 4 项未映射存量的当日实测计数（与 T07 逐行一致） |
| `path_sample_10.json` | 路径步确认单的 10 条路径抽样明细（step1 previous 全 NULL） |

## 不入仓的大文件

12 个分批端点对文件（`batch_kg100-cover-01-ins-01…12.json`，各 ~16MB，共 ~192MB）留在执行机
`~/qiliantupu/kg100-work/`，完整 sha256 见 MANIFEST.sha256.md 第二节，可按哈希核对。
