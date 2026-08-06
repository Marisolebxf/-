# FUNC-DESIGN · 产业链总览 / 门户全景图谱

> **状态**：skeleton（v0.1）· 待按交互五件套填满工程章节  
> **日期**：2026-08-06  
> **Track**：Track-MS  
> **derived_only**：`true`（禁止本文件扩 scope；冲突先回写五件套 / DEC）  
> **规程**：`产品定义评审规程.md` §3.5（v2.7）  
> **CMS 文案落位**：同目录 `SPEC-CMS-CHAIN-PORTAL-CONTENT.md`（门户五块文案；企业数/机构数等程序算，CMS 不背数）

---

## 0. 权威与派生关系

| 类型 | 路径 / ID | 版本（填表时核对） |
| --- | --- | --- |
| DEC | `DEC-CHAIN-PORTAL-OVERVIEW-L0-L1-20260806.md`（同目录） | 2026-08-06 已批 |
| DEC | `DEC-CHAIN-PORTAL-OVERVIEW-PANORAMA-SCOPE-20260806.md`（同目录） | 2026-08-06 已批 |
| IA | `IA-CHAIN-PORTAL-OVERVIEW-产业链总览.md`（同目录） | v1.5-portal-panorama-scope |
| TRACE | `TRACE-CHAIN-PORTAL-OVERVIEW-产业链总览.yaml`（同目录） | 与 IA 同版 |
| USM | `USM-CHAIN-PORTAL-OVERVIEW-产业链总览.md`（同目录） | 与 IA 同版 |
| Wireframe | `Wireframe-CHAIN-PORTAL-OVERVIEW-产业链总览.md`（同目录） | 与 IA 同版 |
| UX-SPEC | `UX-SPEC-CHAIN-PORTAL-OVERVIEW-产业链总览.md`（同目录） | v1.5-portal-panorama-scope |
| Bid（门户全景叶子） | `bid-reference/智慧服务门户系统-要素相关.md` §1.1.1.1.1.1.1.1 | 约 300–307 行 |
| CMS 附录 | `SPEC-CMS-CHAIN-PORTAL-CONTENT.md` | v0.2-portal-only |
| 专题全景（对照，非本页改造范围） | `CHAIN-TOPIC-PANORAMA-*` 交互五件套 | 本文件不削砍专题详情组 |

**Q2 已确认控制边界（写入本说明书）**：

1. **图谱画布**：只渲染产业链结构（节点 / 边 / 上中下游分区）；节点上不挂企业徽章、技术路线徽章、市场规模徽标。  
2. **详情宿主**（常驻右栏 40%）：可展示节点基础信息 + 简介 + **企业列表**（对齐门户 Bid 与 `DEC-PANORAMA-SCOPE`）。  
3. 技术路线 / 演进 / 科研服务机构 / 市场规模：**不承接**于门户全景（归专题 `CHAIN-TOPIC-PANORAMA`）。

---

## 1. 模块目标与不承接

### 1.1 目标（派生自 IA §1）

- 用户选择 **L0 产业**（`industry_id`）后，在 `/industry-center/overview` 同一上下文浏览：全景（默认）、概况、资讯、历程、深圳现状。  
- 全景首屏展示该 L0 下的 **L1 总链**；支持结构 **逐级下钻** 与面包屑返回。  
- 可将当前 L0 产业加入 `industry` 共享对比篮（不写 `industry_chain`）。

### 1.2 不承接

- 专题 IC-30：动态演进、主流技术、市场规模、科研/服务机构详情 Tab。  
- 本页任务提交、报告生成、趋势诊断 / 区域评价 / 深圳决策配置。  
- CMS 后台编辑 UI（见 CMS 落位说明；本页只消费已发布内容）。  
- 专题全景 Modal 对象合同并入本页。

---

## 2. 对象 / 身份 / 路由参数

| 对象 | 稳定身份 | 职责 | 禁止 |
| --- | --- | --- | --- |
| L0 产业 | `industry_id` | 五 Tab 唯一对象控制器 | Tab 内再切换产业/子链 |
| L1+ 结构节点 | `node_id` + 下钻栈 | 图谱选中 / 详情 / 下钻 | 把工艺叶子默认铺满首屏 |
| 对比篮项 | `elementKey=industry` | 加入/移出当前 L0 | 写入 `industry_chain` |

| 路由 | 说明 |
| --- | --- |
| `/industry-center/overview` | 主路由 |
| `?industry_id=` | 主参；旧 `chain_id` 只读兼容解析 |
| `?tab=panorama\|profile\|news\|history\|shenzhen` | 默认 `panorama` |
| 下钻栈 | **页内状态**（不强制一级路由）；切换 L0 时清空 |

---

## 3. 功能点清单（骨架 · 待 TRACE 逐条勾完）

| # | 功能点 | Bid / 验收索引 | 五件套锚点 | 工程备注 |
| --- | --- | --- | --- | --- |
| F-OV-01 | L0 可检索选择器 | 门户专题全景语境 | US-CHAIN-OV-01；DEC-L0-L1 | Arco Select；与企业「所属产业」同口径 |
| F-OV-02 | 全景首屏 L1 总链 | §1.1.1.1.1.1.1.1 | US-CHAIN-OV-02；UX §1.2 | 不得默认铺 L2+ |
| F-OV-03 | 无限（逐级）结构下钻 + 面包屑 | DEC-L0-L1 D-DRILLDOWN | US-CHAIN-OV-11 | 画布仅结构 |
| F-OV-04 | 节点详情：简介 + 企业列表 | Bid 弹窗/右栏解释 | US-CHAIN-OV-03；DEC-SCOPE | **不在画布挂载** |
| F-OV-05 | 产业概况 / 资讯 / 历程 / 深圳 | IC-38/40/41 等 | US-CHAIN-OV-05~09 | 文案板块见 CMS 附录 |
| F-OV-06 | 加入/移出对比篮 | — | US-CHAIN-OV-10 | 无页内篮 Drawer |

> TODO：从 TRACE `compliance_refs` 逐 leaf 填 `tier` / `route` / 缺口。

---

## 4. 交互与控制边界

### 4.1 状态机（骨架）

```text
[无 industry_id] → 空态引导选产业
       ↓ 选 L0
[L1 总链渲染] ←→ 选中节点 → [详情宿主：简介+企业列表]
       ↓ 下钻
[子结构层] ← 面包屑 / 返回上一级
       ↓ 切换 L0
清空下钻栈、选中、详情 → 重新 L1 首屏
```

### 4.2 画布 vs 详情宿主（Q2）

| 区域 | 允许 | 禁止 |
| --- | --- | --- |
| 图谱画布 | 节点、边、分区、选中高亮、结构下钻入口 | 企业/技术/市场规模节点徽标；演进时间轴控件（门户） |
| 详情宿主 | 基础信息、简介、企业列表、关系语义摘要（可选） | 核心技术 / 科研机构 / 市场规模三 Tab（门户已废止） |

### 4.3 布局

- 全景：固定 **60% 图谱 + 40% 详情**（UX-SPEC）。  
- 权限：L0 可读 L1 默认结构；主体明细 / 加篮按全局权限基线（UX-SPEC §1.2）。

---

## 5. 参数 / 任务快照 / 导出

| 项 | 本模块 |
| --- | --- |
| 分析任务 | **不承接** |
| 参数快照 | **不承接** |
| 报告导出 | **不承接** |
| CMS 内容版本 | 消费已发布内容版本号（见 CMS 附录；接口 TBD） |

---

## 6. 接口与数据合同骨架

> 调用链铁律：前端 → Java REST →（必要时）Python `/internal/*`；前端不直连图库。

| 能力 | 建议 Java 路径（TBD 定稿） | 主要入参 | 主要出参 |
| --- | --- | --- | --- |
| L0 产业字典 | `GET/POST .../meta/industries` 或复用企业产业字典 | keyword | `industry_id`, name, level=L0 |
| L1 结构图 | `GET .../topic/v1/industry/{id}/chain-structure` | `industry_id`, `depth`/`focus_node_id` | nodes[], edges[], level |
| 节点详情 | `GET .../nodes/{node_id}` | `node_id` | intro, enterprises[] |
| CMS 文案块 | `GET .../cms/industry/{id}/blocks` | `industry_id`, `block_keys` | 见 CMS 附录 |

> TODO：补齐请求/响应 JSON 示例（对齐 `重点企业分析-功能设计.md` 粒度）。

---

## 7. 权限与异常态

| 场景 | 行为 |
| --- | --- |
| 无 `industry_id` | 空态 + 选择器焦点；图谱不伪造默认产业 |
| 结构服务失败 | 可重试错误态；不静默空图 |
| 节点无企业 | 详情区空列表说明 |
| 未登录看明细 | 按权限锁态 / 引导登录（UX-SPEC） |
| 评审模式 | 仅评审层挂载；业务 DOM 无评审文案 |

---

## 8. 开放项与待填

| ID | 问题 | 建议处置 |
| --- | --- | --- |
| OV-FDS-01 | 结构 API 路径与字段最终命名 | 架构 + API 定稿后回填 §6 |
| OV-FDS-02 | 企业列表字段集（名称/地区/标签…） | 回写 Wireframe 字段表后再填 |
| OV-FDS-03 | CMS block_key 与 Tab 映射终表 | 见 `SPEC-CMS-CHAIN-PORTAL-CONTENT.md` |
| OV-FDS-04 | 与专题全景入口跳转合同 | TRACE related_only；本页不改造专题 |

---

## 9. 填充检查清单（出 v1.0 前）

- [ ] TRACE 叶子 100% 勾到 §3  
- [ ] UX-SPEC 状态机与本 §4 无冲突句  
- [ ] §6 至少 1 个结构接口有示例 JSON  
- [ ] CMS 附录 block 表已会签「不耦合算法层」  
- [ ] 架构抽检：无前端直连 Nebula / Python  
