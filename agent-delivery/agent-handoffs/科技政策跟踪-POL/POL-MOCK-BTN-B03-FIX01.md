# POL-MOCK-BTN-B03-FIX01 · 评价按钮与种子批双源冲突根治（报障单）

> 2026-11-11 · 报障人 `agent:frontend-agent` · 类型 数据/灌数冲突 · 强度 2 点（data + algorithm 各 1）
> 状态 `proposed`（待监管人认领派单；本单只登记问题与方案，不改代码）

## 一、报障

### 现象（2026-11-11 01:47 用户截图报障「重复了」）

政策分析评价 · 推荐方案页「选择推荐方案」出现两张「人才引育优先方案」、两张「研发投入加力方案」；互动意见同翻倍。

### 根因（已实查库与代码，证据齐全）

`gkxlumenx_gapfill` 的评价缺项表存在**两个灌数入口写同一张表**，批次互不相删：

| 入口 | 批次 `gapfill_batch_id` | 写入行为 |
|---|---|---|
| 种子 SQL（`lumen-algo-py/scripts/mysql/gapfill_policy_eval_scheme.sql` 等） | `POL-L2-DS11-PLAN-GAPFILL-L01` / `POL-L2-DS11-READ-GAPFILL-L01` | 手工执行，只 INSERT 不 DELETE（「不整表删除」约束） |
| 评价按钮（`vendor/entan-py/polan/mockgen/evaluation.py`，经 `/policy/v1/policy/mock/page` `{"page":"evaluation"}` 触发） | `BTN-evaluation` | 每次运行先 `DELETE ... WHERE gapfill_batch_id='BTN-evaluation'` 再**整批重插** 5 张表 |

冲突表（其余 trend/partition/template 三表仅按钮一个来源，无冲突）：
- `gapfill_policy_eval_scheme`：227 方案对照 / 228 参数模拟 / 229 路径与风险 / 230 互动意见（DS11 五叶正源）
- `gapfill_policy_eval_shell`：224 解读条目 / 225 多媒体（DS11 READ 正源）

2026-11-09 22:50 有人点击评价按钮 → 两表全部翻倍（scheme 19+19、shell 7+7）。

### 已做处置（2026-11-11 凌晨，不重复计入本单工作量）

1. **数据修复**：按 `gapfill_batch_id='BTN-evaluation'` 精确删除 scheme 19 行 + shell 7 行（事务内核对行数后提交）；API 复核 227=2 行、228=3 档、230=3 条。
2. **入口熔断**：`demo-ui-system-test` `4fa76c7` 隐藏 PolicyMockPage 的「评价」按钮（配置保留，`HIDDEN_PAGE_JOBS` 登记原因）。**后端 `/v1/policy/mock/page` 接口未封**，直接 curl 仍可复灌。

## 二、根治方案（本单验收内容）

按「种子 SQL 是唯一正源」裁决（DS11 五叶的 gapfill 单 `POL-L2-DS11-PLAN-GAPFILL-L01`、READ 的 `POL-L2-DS11-READ-GAPFILL-L01` 是建表灌数的正源单）：

1. **按钮跳过冲突表**（algorithm，`vendor/entan-py/polan/mockgen/evaluation.py`）：
   - `write_evaluation()` 对 `_TABLES` 中的 `gapfill_policy_eval_scheme`、`gapfill_policy_eval_shell` 改为**只 DELETE 自己批次、不重插**（或直接从 `_TABLES` 移除这两张，同步改 `build_rows`/回执 `227/228/229/230/224/225` 计数语义为「登记 0 行，来源见种子单」）；
   - `self_check_writer()` 断言同步更新（scheme/shell 写入为 0、DELETE 仍只打 BTN 批次）；
   - trend/partition/template 三表行为不变（仍是 219/220/222 唯一来源）。
2. **按钮重新可见**（frontend，`demo-ui-system-test/src/views/policy/pages/PolicyMockPage.vue`）：方案 1 合入并部署后，移除 `HIDDEN_PAGE_JOBS` 里的 `btn:evaluation`，确认文案与回执如实标注。
3. **DoD**：
   - 点「评价」按钮后 `gapfill_policy_eval_scheme/shell` 行数不变（无 `BTN-evaluation` 新行）；
   - 219/220/222 三表照常重灌、回执如实；
   - `python -m pytest tests/`（entan-py 自检）与 `self_check_writer()` 全绿；
   - 演示页 227–231、224/225 数据仍为种子批，行数不翻倍。

## 三、影响面与风险

- 若裁决反转为「按钮批是正源、种子 SQL 废弃」：需同步作废 `POL-L2-DS11-PLAN-GAPFILL-L01`/`POL-L2-DS11-READ-GAPFILL-L01` 两单的灌数物，并把按钮生成文案（`_scheme_rows` 等，与种子内容有措辞差异）提为冻结种子——影响面更大，不推荐；本单按推荐方案执行。
- `POL-MOCK-BTN-B03` 的 DoD「评价页五表全套重灌」由本单修订；B03 本体不回滚。

## 四、关联

- 报障源头走查：`POL-L2-DS11-PLAN-WIRING-L01`（用户截图）、本轮对话记录（2026-11-10 22:00 – 11-11 02:30）
- 熔断提交：`demo-ui-system-test 4fa76c7`；数据修复脚本（临时，未入库）：按 batch 删 scheme/shell 的 BTN 批
- 同表 reader：`gkxlumen-element` PolicyEvaluationReadController（jobs/shells 五叶）
