# 文档 vs Demo 范围对照表（模板）

> **用途**：防止「文档写了 = Demo 已交付」。  
> **用法**：复制到 `{模块包}/DOC-vs-DEMO-SCOPE-{MODULE}.md`；与 TRACE / INDEX 同步维护。  
> **闸门**：标为「V1 Demo 必跑」却无 Demo 证据 → 不得称 Demo 完成；「本轮不做」必须写原因与恢复条件。

---

## 0. 元数据

| 字段 | 值 |
|---|---|
| module_key | `{MODULE}` |
| 业务包路径 | |
| Demo 仓 / 路由前缀 | 例：`demo-ui-topic` · `/policy/*` |
| 填写人 / 日期 | |
| 状态 | `draft` / `aligned` |

---

## 1. 三栏对照（主表）

| ID | 能力 / 页面 / 菜单项 | 文档落点（IA/USM/Wireframe） | 分类 | Demo 证据（路由/组件/截图） | 备注 |
|---|---|---|---|---|---|
| S-01 | 例：政策查询入篮 | US-… / F-… | `demo_must` | | |
| S-02 | 例：维护管理·门户内容样例 | US-… | `demo_must` | | |
| S-03 | 例：维护管理·图谱绘制 | US-… | `placeholder` | 菜单可达+占位页 | V1 禁止删菜单 |
| S-04 | 例：某高级配置 | US-… | `out_of_round` | — | 未排期；见 Q-… |

**分类枚举（只能选一）**

| 值 | 含义 |
|---|---|
| `defined_only` | 仅文档，未承诺本轮 Demo |
| `demo_must` | V1 Demo / 高保真必跑，须有可点证据 |
| `placeholder` | 菜单/路由可达，页内明确「占位/开发中」，**禁止伪造成完整能力** |
| `out_of_round` | 本轮明确不做；须写恢复条件 |
| `system_shared` | 能力在系统包，本域只做接入（链到接入登记卡） |

---

## 2. 系统能力引用（避免重复造壳）

| 系统能力 | 本域分类 | 接入登记卡章节 | Demo 是否按金样例验收 |
|---|---|---|---|
| SYS-ANALYSIS-JOBS | system_shared | §3 | ☐ |
| ENT-COMPARE | system_shared | §4 | ☐ |
| ENT-EXPORT | system_shared | §5 | ☐ |

---

## 3. 维护管理 / 门户写侧（若有）

| 菜单项 / block | 文档 | 分类 | Demo |
|---|---|---|---|
| 门户内容工作流 | | demo_must / placeholder | |
| 其它 15 项（逐项或分组） | | | |

规则：

- 文档写「完整样例」→ 必须 `demo_must` 且可点通状态机。  
- 文档写「占位」→ `placeholder`，菜单不可删。  
- 禁止第三种：文档写全、Demo 无入口又无占位。

---

## 4. 样式合规挂载

| 项 | 范围页列表 | 证据 | ☐ |
|---|---|---|---|
| Design.md §14 | | | |
| UX-UE §19 | | | |
| 未遵守点清单（若有） | | 登记 as-built 或修 | |

---

## 5. 变更纪律

1. 文档新增能力默认进 `defined_only`，人工决定升为 `demo_must` 后才排 Demo。  
2. Demo 先做、文档未写 → 补文档或标 as-built 偏差，禁止长期双真源。  
3. 本表与 TRACE `delivery_stage` / INDEX 状态冲突时，以**本表 + 人类同学决定**回写 TRACE。
