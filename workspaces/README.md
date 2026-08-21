# 瘦工作区（降 Token）

> **不要默认打开** 上级目录的 `gkx-lumen.code-workspace`（17 根业务仓 + worktrees，已不含 dataease）。  
> 多根会把各仓 `CLAUDE.md` / `AGENTS.md` 全部注入 always-applied，单轮可白烧 ~15k tokens。

## 怎么用

Cursor / VS Code：`File → Open Workspace from File` → 选本目录下对应文件。

| 文件 | 适用任务 | 打开的 folder |
|------|----------|---------------|
| `orch-only.code-workspace` | 派单 / 文档 / 编排 | 仅主仓 |
| `gdf.code-workspace` | GDF 产线 / CDC Skill / 派单包 | 仅主仓（GDF 成员用这个；指南 `agent-delivery/data/GDF/GDF协作指南.md`） |
| `fe-science.code-workspace` | 科技展示前端 | 主仓 + science-pc + demo-ui-science |
| `fe-topic.code-workspace` | 专题前端 | 主仓 + topic + demo-ui-topic |
| `java-api.code-workspace` | Java API | 主仓 + lumen-svc-platform |
| `algo-py.code-workspace` | Python 算法 / ETL | 主仓 + algo 仓 + etl（不含算法前端） |
| `fe-algo.code-workspace` | 算法前端正式交付 | 主仓 + lumen-algo-platform |
| `admin-ui.code-workspace` | 管理后台 UI | 主仓 + lumen-ui-admin（需要对照再临时加 demo） |
| `../gkx-lumen.code-workspace` | 跨仓大重构 / 检索 | **全量 17 根 + worktrees，慎用** |

## 命名约定

`folders[].name` **只用短英文 id**（如 `gkx-orchestration`），禁止括号、斜杠、长中文说明。  
否则 Ctrl+Click / 部分工具会把显示名拼进路径导致「Unable to open …」。

## 一张 G（图谱 · 开仓必读）

SAD：**只建一张图。** 产业链为底图；展示六模块和专题都是这张图的**窗口**，不是不同的图。  
**从建库起就是这一张**，没有「二期并库 / 可选二期 `gkx_topic`」。

```text
  展示六模块          专题全景 / 深度分析
       \                    /
        \                  /
         ▼                ▼
      一张 G  =  demo_gkx_chain / gkx_chain
      底图 = 产业链环节；企业/机构/人才/政策/服务挂接
```

| 项 | 口径 |
|----|------|
| Demo 落点 | Nebula **`demo_gkx_chain`**（正式 `gkx_chain`） |
| 现网多 space | `entan` / `gkx_policy` 等是模块联调 as-built，**不是**目标态分域 |
| 施工 | 灌数据 / 投影往这一张 G 写；禁止先分库再留到「二期汇总」 |
| 真源 | `agent-delivery/data/data-design/storage/README.md` 决策 #7 · `graph-engine.md` §3.1 · SAD `跨系统-知识图谱/INDEX.md` |

## 相关

- `.cursorignore`：各仓根目录（编排仓已有）
- `agent-delivery/budget-estimate.md` §6 / §6.1
