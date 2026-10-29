# 当日进展

飞书八列表改挂本目录，停止在格子里手填。skill `gkx-dev-process` 的「今日快照」覆盖写入 `YYYY-MM-DD.md`，并另写 `WBS汇总-YYYY-MM-DD.xlsx`。

**新企业投影**（Z.ai · 只出站，不回写 git）：
- 多维表格：<https://zhipu-ai.feishu.cn/base/P0DdbN6Iia3BxXsSusycQCyunIh>
- 配置：`agent-delivery/feishu/feishu-daily-snapshot-board.yaml`
- 同步：`node scripts/sync-feishu-daily-snapshot.mjs [--date YYYY-MM-DD] [--dry-run]`
- 凭据：本机 `.env` 的 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`（应用 `cli_aa698af4efb9dc09`，须已加为表格可编辑协作者）

旧电子表格（智谱租户，已停手填，仅存档）：<https://zhipu-ai.feishu.cn/sheets/YiwIsN4HjhGs6it3IW8Cvfnn5Tf?sheet=GviW3p>

PM 没说「今日快照」之前，本目录没有当天文件。没有文件就表示还没跑快照，不表示工作停了。

八列：负责人、任务内容、完成时间、完成状态、当日任务、当日进展、测试情况、其他备注。完成百分比按规约 §7.1，不用口令里的百分数。
