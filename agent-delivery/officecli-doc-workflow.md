# officecli 文档工作流（格式参考 · 内容发挥）

> **原则**：`正式文件/` 提供 **版式与结构** 参考；报告 **正文内容** 按实际代码、K8s 测试、Pipeline 结果编写，可发挥，不必抄 V6 原文。
> 凡读/改 **.docx 格式**（样式、标题、表格），**必须使用 officecli**。

---

## 1. 格式参考什么、内容写什么

| 维度 | 参考正式文件 | Agent 自行发挥 |
|------|-------------|----------------|
| 章节编号 | V6 的 1→9 章、3.2.4.x 层级 | — |
| 标题样式 | 仿宋、14pt/16pt、heading 1–6（officecli get/query） | — |
| 报告结构 | 引言→范围→用例表→结论（见 templates） | — |
| 时序图格式 | Mermaid `sequenceDiagram` + autonumber 写法 | 参与者名可随实际服务名调整 |
| 测试用例表 | 表格列：序号/测试项/预期/实际/结果 | 用例描述、curl、截图、pipeline ID |
| 功能说明正文 | 仅作范围边界参考 | 按 lumen 实际实现写 |
| 接口字段 | innov-api 契约为技术准绳 | 实测 request/response 样例 |

---

## 2. 安装与调用

```powershell
& "$env:LOCALAPPDATA\OfficeCLI\officecli.exe" --version

$DOC = "e:\实施\2025\智谱-深圳国科信\5-实施和开发\详细设计\正式文件\03详细设计说明书-科技信息展示系统-Demo修正版-V6.docx"
$OC  = "$env:LOCALAPPDATA\OfficeCLI\officecli.exe"
```

**文件被 Word 占用时**：Copy-Item 到 `agent-delivery/_tmp/design-v6.docx` 再操作。

---

## 3. officecli：抽格式（优先这些命令）

| 目的 | 命令 |
|------|------|
| 章节目录层级 | `officecli view $DOC outline` |
| 样式分布 | `officecli view $DOC stats` |
| 某级标题样式 | `officecli query $DOC 'paragraph[style=heading 2]'` |
| 段落版式样例 | `officecli get $DOC '/body/p[@paraId=…]' --depth 1 --json` |
| 表格结构 | `officecli get $DOC '/body/tbl[N]' --depth 2` |
| 格式问题自检 | `officecli view $DOC issues --type format` |

**范围对照**（可选，不必摘录全文）：

```powershell
& $OC query $DOC 'paragraph:contains("3.2.4.3")'   # 确认章节存在即可
```

不确定属性：`officecli help docx paragraph`

---

## 4. Markdown 时序图：格式参考

读 `正式文件/科技信息展示系统-7模块34页面全量时序图.md`，复用：

- ` ```mermaid` + `sequenceDiagram` + `autonumber`
- `alt/else`、`opt`、`par` 结构
- 模块说明段落写法

**内容**：participant 名称、接口路径按 **gkx_lumen_backend / innov-api** 实际命名写。

---

## 5. 生成验收 .docx（克隆 V6 版式或模板）

**推荐**：新建 docx 时复制 V6 的 styles/节属性，再填入自写内容：

```powershell
# 从 V6 克隆样式骨架（不复制正文）
Copy-Item $DOC $out -Force
# 清空 body 示例段落后，用 officecli add 写入自写章节（heading 1/2 + Normal）
& $OC add $out /body --type paragraph --prop text="1.测试概述" --prop style=Heading1
& $OC add $out /body --type paragraph --prop text="本次对 dev 环境 …" --prop style=Normal
& $OC validate $out
```

或从 `templates/*.md` 写 Markdown 验收报告（更轻量，格式对齐 templates 即可）。

---

## 6. 各 Agent 分工

| Agent | 格式 | 内容 |
|-------|------|------|
| **doc-agent** | officecli 读 V6 outline/styles；套 templates | 汇总 handoff、Pipeline、测试数据 |
| **qa-agent** | 用例表列结构与 templates 一致 | 填实测 PASS/FAIL、curl、截图 |
| **api-agent** | 接口文档表格格式参考 V6 §5 | OpenAPI / 实测 JSON |
| **frontend-agent** | 时序图 Mermaid 格式参考 seq md | 实际路由、组件、API 调用 |

---

## 7. 禁止事项

- 禁止不套 **templates / V6 章节结构** 就交验收报告（格式乱）
- 禁止把 V6 **大段原文** 粘贴进验收文档冒充测试内容
- 禁止手改 V6 源 docx（仅只读或 copy 后当样式母版）
- 禁止不用 officecli 直接改 .docx XML

---

## 8. 索引

`formal-docs-registry.yaml` · `templates/`
