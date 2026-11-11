# POL-L2-DS12-SIM-242-COVER-FDE · E 波次 · 用例 / 冒烟

- 总单：`POL-L2-DS12-SIM-242-COVER-FDE-L01`
- 日期：2026-11-12
- 身份：qa-agent / doc-agent
- 依据：D FE live（本地 `21844ac`，待推）+ CMP 217 COVER-FDE 形态写法
- 未改 FE

## 用例改了哪些句

| 文件 | 位置 | 改动 |
|---|---|---|
| `合规演示用例/POL-L2-DS12-SIM-合规演示用例.md` | 文头日期 | 增补「2026-11-12 242 COVER-FDE 废止「没有下载」、补章节自定义+真 Word/PDF」 |
| 同上 | 覆盖表 242 · 触发 | 「只看正文」→「有正文后勾选章节，再点导出 Word/PDF」；接口列补 `situation/report/generate` |
| 同上 | 覆盖表 242 · 期望输出 | **废止**句末「没有下载」；保留四段字段期望；**补形态期望（COVER-FDE）**：章节自定义勾选 → `POST /display/v1/situation/report/generate`（`reportType=policy-interpret-report`）→ OpenHTMLtoPDF；PDF 真 `.pdf`；Word 同源 html→`.doc`；内容=勾选段 `body_text`；禁 text/plain、禁打印另存；无行/无勾选不产文件 |
| 同上 | 主路径第 6 步 | 同步废止「没有下载」；补章节勾选 + 导出冒烟句（对标 CMP 217 主路径写法） |

## 与 D 对齐

| D 落点 | E 用例是否钉住 |
|---|---|
| `reportType=policy-interpret-report` + OpenHTMLtoPDF | ✅ 形态期望句已写 |
| Word=`format=html`→`.doc`；PDF 真字节 | ✅ |
| 内容=当次勾选段 `bodyText` / `body_text` | ✅ |
| 无行 / 无勾选不产文件 | ✅ |
| 空态「没有解读报告段落」 | 产品空态，本波用例未另钉（正文四段仍为可演期望） |
| FE 本地 `21844ac` 待推 | 记入总单 note；冒烟须 FE 已部署或本机带该 commit |

对标：`POL-L2-DS10-CMP-合规演示用例.md` 217 行「形态期望（COVER-FDE）」同构（report/generate + 真 PDF / 同源 Word + 禁 text/plain）。

## 建议冒烟（§6.5）

1. 展示 PC 进「政策效果推演 · 科技政策推演」，政策编号 `18363390`，生成解读报告。
2. 核对四段正文与覆盖表一致。
3. 见「章节自定义」勾选；至少勾一段，点「导出 Word」与「导出 PDF」各一次。
4. Network：须有 `POST /display/v1/situation/report/generate`，body 含 `reportType=policy-interpret-report`。
5. 下载文件：PDF 打开为真 PDF（非 text/plain）；Word 为 `.doc` 且可见勾选段落正文。
6. 取消全部勾选或无行时，导出按钮不可用 / 不发请求、不产文件。

前置：FE `21844ac` 已合入运行面（本机或推送后 CI）。

## 总单下一状态

| 项 | 结论 |
|---|---|
| E 用例 | ✅ 已改；「没有下载」已废止 |
| AV-0 → `integration` | **暂不改状态**：尚无总单 handoff（`agent-handoffs/POL-L2-DS12-SIM-242-COVER-FDE-L01.md`）+ cost；evidence 已可指本 E 简报 |
| 建议 | 保持 `in_progress`；note 标「可 AV 或待冒烟」。冒烟绿 + 总 handoff/cost 回填后走 AV-0→`integration`，再视联调关键词进 `pending_test`。**勿**改 `done`（需淮政玮） |
