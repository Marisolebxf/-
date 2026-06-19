# Handoff · UX 企业要素文档收口（IA / Wireframe / Gap 扩到全集 + 检索 + 角色分级）

| 属性 | 内容 |
|------|------|
| 任务 | WP1 ux-agent：将 ENT-IA / ENT-wireframe / ENT-gap 从"分析层 E-20~E-30"收口到"企业要素全集 E-20~E-37 + 检索 SE + 角色分级" |
| 角色 | ux-agent（IA 段）+ 协调补完（wireframe/gap 段，因 ux-agent 子任务 resource_exhausted 中断后由编排侧补完） |
| 分支 | `topic_demo` · `feat/ent-elements-build` |
| 日期 | 2026-06-19 |

## 1. 产物清单（均在 `topic_demo/docs/ia/enterprise/`）

| 文件 | 变更 |
|------|------|
| `ENT-IA.md` | ✅ 重写为两层全集站点图（mermaid）：门户层 `/development/{overview,search,key-enterprises,star-enterprises,shenzhen}` + 整页画像 `/development/enterprise/:code` + 分析层；页面清单含路由/验收点/D8 组件 |
| `ENT-wireframe.md` | ✅ 标题扩为"企业要素"；新增**第二部分**：检索工作台 DS、概况改造 D0、重点企业 D1、明星企业 D2、深圳企业 D3、统一画像、角色分级通用线框；字段表带 metric_id；检索/画像详图引用 `ENT-search-design.md` §4~§7 避免重复 |
| `ENT-gap-analysis.md` | ✅ 标题扩为全集；新增 §3.5（表 C 门户 E-31~E-37 / 表 D 检索 SE-01~06 / 表 E 角色分级 U1/U2/S1/S2），含现状（development/* + 孤儿页）与缺口动作+优先级；§4 自检更新 |

## 2. 覆盖范围

- 验收点：E-20~E-37 全集 + 检索体验 SE-01~06 + 角色分级 U1/U2/U3/S1/S2。
- 与上位文档一致性：对齐 `ENT-element-master-design.md`（两层）、`ENT-search-design.md`（检索/画像/范式/去 SCRM 无关化 SD-01~07）、`ENT-userflow.md`（角色矩阵/埋点）。

## 3. 与 D8 / D9 合规

- D8：组件命名用 §9 通用组件；主色 `#165DFF`、控件 32px、抽屉 720px、克制风格；现栈偏离（Tailwind+recharts vs Arco+ECharts+G6+Leaflet）记为 lumen 复刻阶段事项。
- D9：wireframe 字段表第 6 列均含 `metric_id`；统计字段标 ⓘ，Mock 标 🧪，待定口径标 ⚠️。

## 4. 开放项（登记客户决策清单）

- K-O30 重点企业/高企/专精特新判定口径阈值；K-O31 风险信息 Tab 数据源；K-O32 智能搜索词典范围；K-O33 导出字段/权限；K-O34 用户级别划分与权限矩阵；K-O35 公众可见字段脱敏口径 + 导出配额。

## 5. 备注

- 原 ux-agent 子任务在完成 ENT-IA 后因 `resource_exhausted` 中断；wireframe/gap 段 + 本 handoff 由编排侧补完，内容口径与设计文档一致。
- 下游：frontend-agent（WP3a 基础层已并行启动）按本组文档 + `ENT-ui-spec.md` + `design-tokens.css` 实现。
