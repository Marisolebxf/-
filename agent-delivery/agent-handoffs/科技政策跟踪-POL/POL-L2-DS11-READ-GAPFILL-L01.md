# POL-L2-DS11-READ-GAPFILL-L01 · 结果解读缺项表灌数

- 任务：`POL-L2-DS11-READ-GAPFILL-L01`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 执行：`agent:data-agent`
- 强度：ponytail full
- 状态：in_progress（本单不改任务状态）
- 对照分册：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-READ-DATA.md`（已签收，第 5 节列定义、第 7 节灌数单职责）
- 参考：commit `40d84e2`（CMP 灌数脚本做法；实际位于 `scripts/`，非 `vendor/entan-py`）

## 库表

| 项 | 值 |
|---|---|
| 库 | `gkxlumenx_gapfill`（10.50.11.76:3306） |
| 表 | `gapfill_policy_eval_shell`（本单唯一新建表） |
| 列 | 按分册第 5 节：`id`、`entry_kind`、`subject_name`、`conclusion_text`、`suggestion_text`、`title`、`caption_text`、`is_mock`、`metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`；`idx_kind_item(entry_kind, gap_item)` |
| 拣行键 | `entry_kind` 与 `gap_item` 成对：`解读`+`224 分主题分指标互动解读`、`多媒体`+`225 多媒体辅助解读` |
| 行约束 | 解读行 `subject_name`/`conclusion_text`/`suggestion_text` 必填且 `title`/`caption_text` 必空；多媒体行反之。`is_mock=1`，`metric_id` 全留空，`fill_method=manual`，`gapfill_batch_id=POL-L2-DS11-READ-GAPFILL-L01` |

## 灌数行数

| entry_kind | gap_item | 行数 |
|---|---|---|
| 解读 | 224 分主题分指标互动解读 | 4 |
| 多媒体 | 225 多媒体辅助解读 | 3 |
| 合计 | — | 7 |

解读 4 条（研发费用加计扣除、科技型中小企业培育、高新技术企业认定、科技创新成果科普传播，各一句结论+一句应用建议），多媒体 3 条（政策图解、宣讲实录、认定要点速览，各标题+一句说明），中文内容贴合科技政策。

## 灌数命令

```powershell
# 不连库自检并覆写 SQL（幂等）
python scripts/seed_gapfill_policy_eval_shell.py --check

# 连库建表灌数（幂等：先 DROP 再按分册列建再插）
$env:LUMEN_ALGO_MYSQL_PASSWORD = "<secret>"
python scripts/seed_gapfill_policy_eval_shell.py --apply
```

- 脚本：`lumen-algo-py/scripts/seed_gapfill_policy_eval_shell.py`
- SQL 镜像：`lumen-algo-py/scripts/mysql/gapfill_policy_eval_shell.sql`
- 密码经环境变量 `LUMEN_ALGO_MYSQL_PASSWORD` 注入，不进 git

## 验收证据

独立 SELECT（apply 后重跑一次验证幂等，行数不变）：

```
('多媒体', '225 多媒体辅助解读', 3)
('解读', '224 分主题分指标互动解读', 4)
total: 7
```

查询口径：`SELECT entry_kind, gap_item, COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_eval_shell WHERE is_mock=1 AND metric_id IS NULL GROUP BY entry_kind, gap_item`。

## Git 提交

| commit | 内容 |
|---|---|
| `ef33dce` | 并行会话第一版（旧列名 `topic_or_metric`/`caption`，已被本单修正） |
| `8c0a59c` | fix(policy): 解读壳表列名对齐分册 subject_name/caption_text [agent:data-agent]，已推 `origin/dev`（`a527c42..8c0a59c`） |

仓库内事件说明：本会话首轮暂存的新版被并行会话的 merge 动作覆盖（工作区回退到 `ef33dce` 旧版），且 commit 期间遭遇 `index.lock` 争用。已按分册口径重写脚本、重跑 --check/--apply 并单独提交推送；并行会话的 2 笔提交（评价方案、评价可视化）随远端基线正常在链上，未改动。

## 架构合规自检

- ✅ 只建 `gkxlumenx_gapfill.gapfill_policy_eval_shell` 一张表；未建 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`
- ✅ 未写 ODS、DWD、ADS、供应方库；未插入短板/焦点/摘要数据（它们读已有 ads 表）
- ✅ `is_mock=1`，`metric_id` 全留空，未新造 metric_id，未改 D4
- ✅ 未灌模板选用、视频、动画、图形文件、PDF（BANNED 断言强制）
- ✅ 脚本幂等（DROP+CREATE+INSERT；ponytail 注释标明天花板：本表灌数方唯一，若出现第二写入方改为按批次删除）
- ✅ 未执行 `gap.run`/`focus.run`/`parse.run`，未改 jobs/execute
- ✅ 无 force push、无 reset --hard；PowerShell 全程未用 `&&`/heredoc

## 明确不做（与分册第 9 节一致）

不改 D4、不改架构稿/会签页/说明书/WBS/ads.md/注册表、不把本单标 done、不灌 222 模板选用、不从 shell 反查 223 焦点或 226 摘要。
