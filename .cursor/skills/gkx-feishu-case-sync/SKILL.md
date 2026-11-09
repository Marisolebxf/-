# gkx-feishu-case-sync · 合规演示用例 → 飞书表格同步

把「合规演示用例」覆盖表的【输入或选择】同步到飞书在线表格**新增列**（只加列，绝不改动原有列与内容）。截图贴图（自动化测试截图 → 表内嵌图/浮动图）为规划中的二期。

## 何时用

- 用户要求把 `${GKX_ROOT}/gkx-orchestration/agent-delivery/工程过程/04-*/0*-系统集成/合规演示用例/*.md` 的用例内容同步到飞书表格（如展示系统「需规核验」页）
- 用户提到「合规用例同步」「用例贴到飞书表」「需规条目对齐填输入」

## 前置条件

1. 飞书自建应用（`GKX周报WBS`，APP_ID/APP_SECRET）已存在；机器人已被添加为目标文档**协作者（可编辑）**
2. 环境变量：`LARK_APP_ID` / `LARK_APP_SECRET`（PowerShell：`$env:LARK_APP_ID='...'`，不进 git）
3. 目标表格 token 与 sheet_id 从 URL 提取：`https://xxx.feishu.cn/sheets/<spreadsheet_token>?sheet=<sheet_id>`
4. wiki 节点（`/wiki/<token>`）先用 MCP `wiki_v2_space_getNode` 换 `obj_token`

## 用法

```powershell
$env:LARK_APP_ID='...'; $env:LARK_APP_SECRET='...'
# ① 试跑（只出报告，不写任何单元格）
python "$GKX_ROOT/gkx-orchestration/.cursor/skills/gkx-feishu-case-sync/scripts/sync_cases_to_sheet.py" `
  --md-dir "agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例" `
  --spreadsheet <token> --sheet-id <sheet_id>
# ② 确认报告后正式写入（L=输入与条件，M=来源；可用 --cols 换列）
python ... --apply
```

## 安全保证（铁律）

- **写入前强制校验目标列必须为空**，非空直接中止（防止覆盖人工内容）
- 只写指定的两列（默认 L/M），原有列零改动；写入范围永远是显式 range
- 匹配三级策略，逐级收紧：标题词唯一命中 → 标题+序号偏移 → 文件级偏移学习（同一文件 ≥2 个确定性命中共享同一偏移才外推）；**无匹配/歧义/冲突一律不写**，只进报告人工核对
- 报告落盘在用例目录（`*-用例同步报告-<日期>.md`），含未匹配清单、歧义、冲突、完整映射附录

## 已知坑（2026-11-10 实测）

1. Sheets **v2 读接口**范围分隔符必须用 `!`（`d7d70e!A1:F10`）；用 `.` 报 `90215 not found sheetId`
2. Sheets **v2 写接口**body 必须包 `valueRange`；单格 range 写 `J53:J53` 形式
3. 混合文件里内嵌的多维表格（`?table=tbl...`）用外层 sheet token 调 bitable API 报 `91402 NOTEXIST`，块级 token 获取方式待查（未解决）
4. 贴图链路已验证到「上传素材」：`POST /drive/v1/medias/upload_all`（`parent_type=sheet_image`，`parent_node=spreadsheet_token`）返回 `file_token`；下一步用 `sheets.v3.spreadsheetSheetFloatImage.create`（range 单格、宽高≥20px）或写单元格 `{"type":"embed-image","fileToken":...}` 结构
5. 单元格文本上限：脚本截断在 4500 字符（CELL_CAP）
