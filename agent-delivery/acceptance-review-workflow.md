# 验收对照工作流（qa-agent / doc-agent）

> **给检查 Agent 的指令**（Coordinator 派单 qa 类 leaf 时附带）  
> 功能点清单以 `2-概要设计/2-1需求分析` 为准；**章节原文对照**读 `agent-delivery/bid-reference/*.md`，**按文档标题结构**定位，与 dev 实现对照输出验收意见。  
> **范围真源**：两份 MD 为工作出发点；实现可因数据/算法调整，功能点总量不得超出基线 **±10%**（`scope-baseline.yaml`）。

---

## 1. 输入

| 类型 | 路径 |
|------|------|
| 功能点台账 | `docs_root/2-概要设计/2-1需求分析/需求调研和澄清/csv/08~14` |
| 验收 catalog | `agent-delivery/acceptance-catalog/catalog-*.yaml` |
| **招标章节 MD（主读）** | `agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` |
| | `agent-delivery/bid-reference/科技专题服务算法库.md` |
| 章节索引 | `agent-delivery/bid-reference/README.md` |
| 实现证据 | `agent-handoffs/`、dev K8s（`:30891`）、GitLab Pipeline |
| 输出模板 | `templates/acceptance-test-report-template.md` |

---

## 2. 你必须做的事

1. 打开 `bid-reference/` 下 **Markdown**，按 **编号标题结构** 找到与功能点对应的章节（见 `bid-reference/README.md` 对照表）。**不要读 PDF**；**不要**用 officecli `query` 搜段落代替结构导航。
2. 阅读该节功能/技术要求描述，与 `acceptance-catalog` 条目（如 DS-xx）及 **dev 环境页面/API** 逐项对照。
3. 形成 **验收意见结果**：PASS / PARTIAL / FAIL / DEMO_OK；注明 MD 章节编号、功能点 ID、route、证据。
4. 写入 `验收文档/{模块}-{任务}-验收对照意见.md`。

---

## 3. MD 对照范围

### 3.1 `科技信息展示系统和科技专题服务系统.md`

| 范围 | 结构入口 |
|------|----------|
| 展示系统 7 模块 | `#### 1.1.1.1.` → `###### 1.1.1.1.4.1`~`.4.7` → 子节 `1.1.1.1.4.x.y` |
| 专题服务（战略分析等） | `#### 1.1.1.2.` → `###### 1.1.1.2.4.2` 战略分析 |

子功能与 `catalog-display-7modules.yaml`（DS-01~30）一一对应。

### 3.2 `科技专题服务算法库.md`

| 范围 | 结构入口 |
|------|----------|
| 基础指标（七要素） | `1.2.1.1.1.1.4.1` 及 `4.1.1`~`4.1.7` |
| 产业全要素图谱 | `1.2.1.1.1.1.4.2` |
| 深度分析模型 | `1.2.1.1.1.1.4.3` 及七要素子模型 |

与 `catalog-topic-*.yaml`、`system-wbs.yaml#elements` 对照。

---

## 4. 推荐操作（直接读 MD）

```powershell
$BR = "E:\gkx_src\agent-delivery\bid-reference"
$display = "$BR\科技信息展示系统和科技专题服务系统.md"
$algo = "$BR\科技专题服务算法库.md"

# 按编号定位章节（示例：全球创新监测 DS-04）
Select-String -Path $display -Pattern "1.1.1.1.4.1.4" -Context 0,40

# 算法库政策指标（示例）
Select-String -Path $algo -Pattern "1.2.1.1.1.1.4.1.6" -Context 0,30
```

或在 IDE 中打开 MD，用大纲/搜索跳转到 `1.1.1.1.4.1.4. **全球创新监测**`。

---

## 5. 对照表（输出必填列）

| 功能点 ID | MD 文件 | 章节编号 | 章节标题 | tier | route | 验收结论 | 证据 |
|-----------|---------|----------|----------|------|-------|----------|------|
| DS-04 | 展示+专题.md | 1.1.1.1.4.1.4 | 全球创新监测 | FULL | /innov | PASS | :30891/innov |

**结论枚举**：`PASS` | `PARTIAL` | `FAIL` | `DEMO_OK` | `NOT_IN_SCOPE` | `REMOVED`

---

## 6. 三层关系

```text
2-1需求分析 CSV/需规  →  验什么（功能点 ID）
bid-reference/*.md    →  原文怎么写（按结构找章节）
dev 实现 + handoff    →  做得怎样
```

冲突时以 **bid-reference/*.md**（范围真源）为准；`2-1需求分析` 台账作澄清补充，差异记入备注（优先级见 `scope-baseline.yaml#precedence`）。

---

## 7. officecli（可选）

`bid-reference/*.docx` 为 Word 归档。仅 MD 不够用或需核对版式时：

```powershell
& "$env:LOCALAPPDATA\OfficeCLI\officecli.exe" view "...\五、实施方案-智能服务集群....docx" outline
```

---

## 8. Coordinator 派单话术

```markdown
你是 qa-agent。执行验收对照：

1. 读 task DoD 与 acceptance-catalog 相关条目。
2. 在 `E:\gkx_src\agent-delivery\bid-reference\` 的 **MD 文件**中按结构定位展示系统/七要素章节（见 bid-reference/README.md），阅读要求描述。
3. 对照 dev 实现，形成验收意见，写入 `验收文档/`。
4. 不读 PDF；DEMO 项与 demo-fallback-registry.yaml 一致。
```

---

## 9. 版本

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-06-16 | DOCX + officecli |
| v2.0 | 2026-06-16 | **改为 bid-reference MD 按结构读章节** |
