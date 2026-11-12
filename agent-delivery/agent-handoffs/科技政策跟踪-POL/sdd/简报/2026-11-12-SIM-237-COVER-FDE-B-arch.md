# POL-L2-DS12-SIM-237-COVER-FDE · B 波次 · arch

- 总单：`POL-L2-DS12-SIM-237-COVER-FDE-L01`
- 日期：2026-11-12
- 身份：arch（本会话代写）
- 输入：A 波 product；监管人裁定样例=`18318861`，批准 UPDATE ADS

## 1. 定档

**中档**：不退定义规程；不新建 gapfill；不改 jobs URL；不进 async 白名单（真算属 `POL-L2-DS12-SIM-237-ASYNC-L01`）。

## 2. 要动的层

| 层 | 动作 | 不动 |
|---|---|---|
| ADS `gkxlumenx_ads.policy_text_parse` | **UPDATE** `policy_id=18318861`：`summary`、`auto_tags`、`structured_elements` 写入五要素 | 禁止 `polan.text.parse.run`；不加列；不灌 gapfill |
| element / display | 读列保持 `title,summary,auto_tags,structured_elements`；仍剥 clauses | 一般不改 SQL |
| FE parse live | 固定五标签；关键词用 `auto_tags` | mock 轨可保持原样 |
| 说明书 / SIM-ARCH | 回写界面必见 + 样例 UPDATE 口径 + ASYNC 边界 | 不把本请求改成真算 |
| 合规用例 | 237 可演 + 形态期望 | — |

## 3. 读法 / 键名（钉死）

`structured_elements`（JSON 对象）**中文键**：

| 键 | 对应分句 |
|---|---|
| `核心内容` | 237-3 |
| `支持对象` | 237-4 |
| `申报条件` | 237-5 |
| `支持力度` | 237-6 |

- 关键词 → 列 `auto_tags`（JSON 数组或逗号分隔均可；FE `tagList` 已兼容）
- 摘要 → 列 `summary`
- 返回前仍去掉 `clauses`、`clause_meta`
- FE：固定五区；其余非条款键可放「其它要素」折叠或忽略，**不得**用 rank/publish_year 顶替五标签

## 4. 样例行内容（可演）

政策：`18318861`（六部门蚕桑丝绸产业高质量发展行动计划相关通知，与原用例一致）

建议写入（实现可微调措辞，键名不可改）：

- `summary`：一段可读摘要（非空）
- `auto_tags`：`["蚕桑丝绸","高质量发展","产业扶持"]`（示例）
- `structured_elements`：
  - 核心内容：行动计划目标与重点任务摘要
  - 支持对象：蚕桑丝绸产业链相关企业与经营主体
  - 申报条件：按通知适用的申报资格要点（可列 2～3 条）
  - 支持力度：财政与政策工具口径一句

UPDATE 只改该 `policy_id` 一行；保留原 `title`；`metric_id` 仍为 `M_POLICY_TEXT_PARSE`（若列存在则不改）。

## 5. ASYNC 边界（卡2=B）

本 FDE **不**：注册 Job 键、进 `PolicyAnalysisTypes`、请求路径调解析模型。  
`POL-L2-DS12-SIM-237-ASYNC-L01` 另定可调用服务与写路径（须避免 `run()` 清空整表）。

## 6. B 波收口

监管人已批样例与 UPDATE → 进 C（说明书/四单短回写）与 D（库 UPDATE + FE + 用例）。
