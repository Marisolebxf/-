---
name: gkx-bug-record
description: >
  登记或修订 GKX 三系统缺陷（科技专题服务系统 KJZTFWXT、科技信息展示系统 KJXXZSXT、
  深度挖掘算法 SDWJSF-KJZTFWSFK）。Use when the user says 提交bug、记bug、登记缺陷、
  修订bug、补截图、bug编号冲突, or invokes gkx-bug-record. 文字写入台账并推 origin/dev；同一条的编号和文字列写入飞书，截图只上传飞书、不进 git。
---

# GKX 缺陷登记

正文约定：`agent-delivery/qa/bugs/README.md`。字段与冲突顺延：本目录 `reference.md`。

不改业务仓代码，不建 task-registry 任务，不读 `task-registry.yaml`。

## 系统目录

| 用户说法 | 系统码 | 正文 |
|----------|--------|------|
| 专题系统、科技专题服务系统 | `KJZTFWXT` | `agent-delivery/qa/bugs/KJZTFWXT/items/` |
| 展示系统、科技信息展示系统 | `KJXXZSXT` | `agent-delivery/qa/bugs/KJXXZSXT/items/` |
| 深度挖掘算法、算法库 | `SDWJSF-KJZTFWSFK` | `agent-delivery/qa/bugs/SDWJSF-KJZTFWSFK/items/` |

板块固定 `ZNFWJQ`。编号 `BUG-{板块}-{系统码}-{YYYYMMDD}-{3位}`，序号按**系统+日期**递增，不跳号、不复用。

## 先确认，再占号

信息齐了才写文件。缺了就先给判断，停下来等用户确认。

| 项 | 齐 | 不齐 |
|----|----|------|
| 系统 | 用户点了上表中的系统或系统码 | 只凭页面猜。给出系统码，等确认 |
| 模块 | 用户点了模块名，照抄，格式 `一级 / 二级` | 自己判断后等确认。不占号 |
| 现象 | 用户写了实际看到的文字、接口状态或操作结果 | 只有截图。根据图里文字起草标题和实际，连同系统、模块一起等确认 |

同一原因并成一条，用例号放进范围。用户说「另外」或原因不同，才另开一条。脚本 blocked / fail 本身不登记。

取号前在 `qa/bug-registry.yaml` 里对一下模块和标题。像是已有缺陷，问要不要补在旧编号上，不直接开新号。

## 落盘

1. 在 `gkx-orchestration` 执行 `git fetch origin dev`。
2. 该系统当天序号 = `max(本地 registry, origin/dev registry)` 已有序号 + 1。本地 registry 缺远端已有条目时，先把那些条目补进来，不要整文件覆盖。
3. 正文：`qa/bugs/{系统码}/items/{编号}.md`，按 `qa/bugs/_template.md`。
4. 台账：`qa/bug-registry.yaml` 追加一条，并在 `note` 末尾加一句这个编号是什么。`updated` 改为当天。
5. 截图不进仓库。有图时正文「截图」写 `飞书附件`，没有写 `无`。不要把对话附件 `cp` 到 `assets/`，不要在 Markdown 里写图片路径或 base64。
6. 登记：本 skill 提交写 `人工`。用户给出脚本编号或试跑目录时写 `轮次`，并填关联脚本。不要把已有 `人工` 改成 `轮次`。
7. 结论只写一种：`产品缺陷`、`数据缺口`、`环境不可用`、`用例与现网不一致`。判别见 `reference.md`。
8. 预期抄用例原文。找不到用例就写用户认为应该怎样，关联用例写「无」，不编用例号。实际用用户原话。环境用用户正在看的地址；没说就写「未说明」。
9. 登记人只写用户自己报出的姓名。没报就写「未具名」。
10. 不要往历史轮次文件追加。`KJZTFWXT/R1-20261023-脚本修订.md` 保持不动。
11. 文字落盘后立刻把这一条写入飞书「GKX 当日进展 / 缺陷」，不能只传截图。在编排仓根执行 `node scripts/sync-feishu-bug.mjs --id {编号}`。这条命令从刚写的台账和正文写入这些列：BUG编号、标题、结论、模块、入口、环境、预期、实际、状态、关联用例、发现日期。有图时对每个对话附件原路径再加一个 `--image`，多张就重复该参数；没图不要加。用附件的原始路径，不先拷进仓库。登记人、登记方式只留在正文，飞书没有这两列。命令没跑成，或飞书行里缺 BUG编号，登记不算完成。失败只说「飞书未推」，不回滚文字，不挡住后面的 git push。全量补投影不带 `--id`，覆盖上述文字列，不清除已有附件。

## 提交并推送

占号并写完文件后立刻提交、推送，不必再问。

- 只 `git add` 本次的 registry 和 `items/{编号}.md`。不要加入图片。工作区里其它改动不要带上。
- 分支只推 `origin/dev`。禁止 force，禁止推 `main`。
- 提交说明含 `[agent:qa-agent]`。Windows PowerShell 5 不用 heredoc，用重复的 `-m`。
- `git push origin dev` 被拒：`git pull --no-rebase --no-autostash origin dev`，然后只再推一次。
- pull 会覆盖无关未提交文件时，不要 stash、不要 reset。告诉用户推送被挡住，本次提交留在本地。
- pull 成功后若本次编号与远端另一条不同缺陷撞号，按 `reference.md` 顺延，再提交并推一次。第二次仍被拒就停，报出两个编号。

## 修订已有缺陷

用户给出编号时，改 `items/{编号}.md`；没有再查历史轮次文件。不新占号。补图不落盘，用 `--image` 追加到该编号的飞书附件列，正文「截图」写 `飞书附件`。

状态仍用 `open` / `fixed` / `verified` / `closed` / `deferred`。只有用户明确说修复已验证，才写成 `verified`。复测仍失败保持 `open`。改完同样只提交相关文件并推 `origin/dev`，并再跑一次 `node scripts/sync-feishu-bug.mjs --id {编号}`，把 BUG编号和其余文字列按正文覆写到飞书。补图时另加 `--image`。

## 不要做

- 占号前不写文件
- 不把截图拷进 `qa/bugs/**/assets/`，不把图片路径或 base64 写进 Markdown
- 不提交 `.env`、密钥，以及不是本次缺陷的文件
- 不把 `git reset --hard`、rebase、force push 用于撞号
- 不顺延已经推送过的旧编号
