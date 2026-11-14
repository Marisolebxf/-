# POL-L2-DS10-SENT-211 · 政策效果评估报告共用版式

角色：ui-agent。只定查看弹窗与下载文稿的同一套段落。不改列表卡片，不改按钮文案。

## 版式意图

这是一份正式评估报告，读起来应是标题、范围、时间和连续正文，而不是后台表单配几段灰字。查看弹窗、列表下载、弹窗导出 Word、弹窗导出 PDF 共用下面固定顺序，只允许字距松紧不同。弹窗约 800 宽，可稍紧凑；下载是打印/导出用的 A4 白纸，顶部一条主色细线，各段有小标题。主色 `#165DFF`，页面底 `#D8E7FC`，正文 14px，圆角与描边按 `agent-delivery/Design.md` §4–§6。

段落顺序固定，不得调换、合并或插入其他块：

1. 标题：政策效果评估报告
2. 评估范围（`scope_text`，可能是一句很长的政策名称，必须全文换行，禁止省略号截断）
3. 生成时间（`generated_at`）
4. 达成度（`achievement_text`，一段文字）
5. 社会影响（`social_impact`，一段文字）
6. 存在问题（`problem_text`，按 `；`、`;` 或换行拆条）
7. 改进建议（`suggestion_text`，按 `；`、`;` 或换行拆条）
8. 报告正文（`report_body`，一段或多段，段间按换行切开）

报告面上禁止出现：综合评分、维度得分、进度条、评估机构、图表、库表名、mock、缺项演示。字段名只留在实现注释里，不写给读者。

空段保留标题和位置，正文写「暂无」（`#86909C`）。问题、建议拆完没有非空条目时，不渲染空列表，同样写「暂无」。

## 弹窗结构

遮罩后的页面底仍是 `#D8E7FC`。弹窗本体白底 `#FFFFFF`，外宽 800px，圆角 8px，描边 `1px solid #E5E6EB`，阴影 `0 4px 10px rgba(0, 0, 0, 0.10)`。内容区内边距 24px 24px 16px。字体 `PingFang SC`，英文数字可辅 `Inter`。字距 0。

| 块 | 字号 / 行高 / 字重 | 颜色 | 间距 |
| --- | --- | --- | --- |
| 标题 | 18px / 24px / 600 | `#1D2129` | 下 12px |
| 元信息标签（评估范围、生成时间） | 14px / 22px / 400 | `#4E5969` | 标签列宽 72px，行距 8px，块下 8px |
| 元信息值 | 14px / 22px / 400 | `#1D2129` | 评估范围允许多行 |
| 小节标题（达成度、社会影响、存在问题、改进建议、报告正文） | 16px / 24px / 600 | `#1D2129` | 上 16px，下 8px，底边 `1px solid #E5E6EB`，底边下再留 8px |
| 小节正文 | 14px / 22px / 400 | `#1D2129` | 段间距 8px |
| 空段「暂无」 | 14px / 22px / 400 | `#86909C` | 与正文同一位置 |
| 问题 / 建议有序列表 | 14px / 22px / 400 | 正文 `#1D2129`，序号 `#165DFF` | 左缩进 22px，条间距 4px |

拆条：先按换行切开，再按 `；` 与 `;` 切开，去掉首尾空白，丢掉空条。报告正文只按换行分段，不按分号拆条。

底部操作条与正文之间用 `1px solid #E5E6EB` 分隔，上内边距 12px，按钮右对齐，间距 8px。按钮不进入下载文稿。

- 导出 Word、导出 PDF：主按钮。高 32px，圆角 4px，底 `#165DFF`，字 `#FFFFFF` 14px。
- 关闭：次按钮。高 32px，圆角 4px，白底，描边 `1px solid #E5E6EB`，字 `#1D2129` 14px。

列表卡片的字段、按钮和密度保持现状，下载时改用本节同一套段落，不另写一套摘要。

## 导出 HTML 草稿

下面这份 HTML 是 Word / PDF / 列表下载的纸面稿。OpenHTMLtoPDF 只吃块级和表格，不用 flex、grid、固定定位。弹窗按上一节把同一顺序排紧，不另起段落。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>政策效果评估报告</title>
  <style>
    @page { size: A4; margin: 18mm 16mm 18mm 16mm; }
    html, body { margin: 0; padding: 0; background: #FFFFFF; }
    body {
      color: #1D2129;
      font-family: "PingFang SC", "Microsoft YaHei", SimSun, sans-serif;
      font-size: 14px;
      line-height: 22px;
      font-weight: 400;
    }
    .top-rule { height: 2px; background: #165DFF; margin: 0 0 16px 0; }
    h1 {
      margin: 0 0 16px 0;
      font-size: 18px;
      line-height: 24px;
      font-weight: 600;
      color: #1D2129;
    }
    table.meta { width: 100%; border-collapse: collapse; margin: 0 0 8px 0; }
    table.meta td { vertical-align: top; padding: 0 0 8px 0; font-size: 14px; line-height: 22px; }
    table.meta td.k { width: 72px; color: #4E5969; white-space: nowrap; }
    table.meta td.v { color: #1D2129; }
    h2 {
      margin: 20px 0 8px 0;
      padding: 0 0 8px 0;
      border-bottom: 1px solid #E5E6EB;
      font-size: 16px;
      line-height: 24px;
      font-weight: 600;
      color: #1D2129;
    }
    p { margin: 0 0 8px 0; }
    p.empty { color: #86909C; }
    ol { margin: 0 0 8px 0; padding: 0 0 0 22px; }
    li { margin: 0 0 4px 0; color: #1D2129; }
  </style>
</head>
<body>
  <div class="top-rule"></div>
  <h1>政策效果评估报告</h1>
  <table class="meta">
    <tr>
      <td class="k">评估范围</td>
      <td class="v"><!-- scope_text：全文，可很长；空则输出「暂无」并加 class="empty" --></td>
    </tr>
    <tr>
      <td class="k">生成时间</td>
      <td class="v"><!-- generated_at；空则「暂无」 --></td>
    </tr>
  </table>

  <h2>达成度</h2>
  <!-- achievement_text：一整段，不写分数。空则 <p class="empty">暂无</p> -->
  <p><!-- 达成度正文 --></p>

  <h2>社会影响</h2>
  <!-- social_impact：一整段。空则 <p class="empty">暂无</p> -->
  <p><!-- 社会影响正文 --></p>

  <h2>存在问题</h2>
  <!-- problem_text：按换行、；、; 拆条。有条目用 ol；无条目改为 <p class="empty">暂无</p> -->
  <ol>
    <li><!-- 问题 1 --></li>
    <li><!-- 问题 2 --></li>
  </ol>

  <h2>改进建议</h2>
  <!-- suggestion_text：拆条规则同存在问题 -->
  <ol>
    <li><!-- 建议 1 --></li>
    <li><!-- 建议 2 --></li>
  </ol>

  <h2>报告正文</h2>
  <!-- report_body：按换行拆成多个 p；整段为空则一个 <p class="empty">暂无</p> -->
  <p><!-- 正文第 1 段 --></p>
  <p><!-- 正文第 2 段 --></p>
</body>
</html>
```
