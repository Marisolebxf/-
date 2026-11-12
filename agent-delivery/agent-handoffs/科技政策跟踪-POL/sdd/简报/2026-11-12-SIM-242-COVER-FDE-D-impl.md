# POL-L2-DS12-SIM-242-COVER-FDE · D 波次 · FE live 实现

- 总单：`POL-L2-DS12-SIM-242-COVER-FDE-L01`
- 日期：2026-11-12
- 身份：frontend-agent
- 输入：A product / B arch / C 会签；卡1=**B**
- 仓：`lumen-ui-science-pc`（本地 `dev`，**待人工确认推送**）

## 1. 改动要点

| 项 | 落点 |
|---|---|
| live 格式选择 | `InterpretWorkbench.vue` 报告子页 live 轨补 Word/PDF（`LIVE_REPORT_FORMAT_OPTIONS`，不暴露 markdown/plain） |
| 下载按钮 | 「下载推演解读报告」；无行 / 无勾选 → `disabled`，不调 `exportInterpretReport` |
| 共用下载 | `downloadMock` → `downloadReport`；live/mock 同入口；live 内容 = 勾选段 `sectionName` + `bodyText` |
| 导出链路 | 复用已有 `exportInterpretReport` → `situation/report`（`reportType=policy-interpret-report`）；Word=html→`.doc`；PDF 真字节（对标 217） |
| 空态 | 已点生成但无行 →「没有解读报告段落」；未点 →「尚未点击「生成解读报告」」（`liveReportRequested`） |
| 关评审 | 业务文案无新增「演示 / gapfill / fixture / Bid」；Bid 横幅仍仅 `reviewMode` |

**未改**：`interpretExport.ts`（已接 situation/report，本波复用）；Java / jobs / gapfill。

## 2. 自检

| 项 | 结果 |
|---|---|
| `pnpm type-check`（`vue-tsc --build`） | ✅ 绿（exit 0） |
| Lint（改动文件） | ✅ 无新增诊断 |

## 3. Git / 推送

| 仓 | 动作 | 说明 |
|---|---|---|
| `lumen-ui-science-pc` | **已本地 commit，未 push** | message 含 `[agent:frontend-agent]`；**待人工确认推送**（说「推」后再 `git push origin dev`） |
| `gkx-orchestration` | 本简报可 commit+push | 仅本 D 简报；不夹带其它 WIP |

FE commit：`21844ac`（本地 `dev`，ahead of origin，**未 push**）。

## 4. 下一跳 E

**E**：合规用例 242 —— 废止「没有下载」；补形态：须见章节自定义；点导出 Word/PDF；PDF=真字节；内容来自当次勾选段。不改 FE（除非验出缺口）。
