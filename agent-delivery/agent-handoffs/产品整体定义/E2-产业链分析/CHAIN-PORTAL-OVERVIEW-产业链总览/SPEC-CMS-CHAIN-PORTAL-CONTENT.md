# SPEC-CMS · 门户产业链总览文案落位说明

> **模块**：CHAIN-PORTAL-OVERVIEW / 产业链总览  
> **版本**：v0.2-portal-only  
> **日期**：2026-08-06  
> **性质**：功能设计说明书条件附录（`产品定义评审规程.md` §3.5）  
> **derived_only**：`true`（不新增 Bid 叶子；不定义算法输入输出）  
> **范围**：仅门户总览页 CMS 文案块；不含全景节点挂载、产业运行诊断、数仓加工细则

---

## 0. 权威与派生关系

| 类型 | 路径 | 用途 |
| --- | --- | --- |
| Bid | `bid-reference/智慧服务门户系统-要素相关.md` §1.1.1.1.1.1.1（概况介绍、历程、深圳现状等） | 文案板块存在性 |
| IA | `IA-CHAIN-PORTAL-OVERVIEW-产业链总览.md` §3 / §跨模块 | Tab 与 CMS→总览边界 |
| Wireframe | `Wireframe-CHAIN-PORTAL-OVERVIEW-产业链总览.md` F-06 / F-08 / F-09 | 字段与栏位落点 |
| UX-SPEC | `UX-SPEC-CHAIN-PORTAL-OVERVIEW-产业链总览.md` | 前台只读与空态 |
| 消费侧引用 | `FUNC-DESIGN-CHAIN-PORTAL-OVERVIEW-PANORAMA.md` | 总览功能设计一小节引用 |

**硬边界**：

1. 下表板块为**纯文案 / 富文本（及历程条目）**，由 **CMS 录入维护**。  
2. **不与算法层耦合**：不作为周期 / 关键环节 / 堵点模型的特征输入；算法任务不得读写这些 CMS 字段。  
3. **不与 DWD/ADS 混存混用**：计数、分布、快照时间等程序结果不进 CMS 正文库。  
4. 前台总览只读 `published`；草稿 / 审核 / 发布在维护端完成；总览页不提供编辑入口。

---

## 1. 一句话

选定 L0（`industry_id`）后，总览各文案块按同一产业对象从 CMS 取已发布内容；企业数、机构数、区域分布等由程序 / ADS 计算，**CMS 不背数**。

---

## 2. CMS 内容清单（落位表）

| block_key | 展示名 | Tab | Frame | Wireframe 锚点 | 内容形态 | 初始化 |
| --- | --- | --- | --- | --- | --- | --- |
| `industry_intro` | 产业介绍 | `profile` | F-CHAIN-OV-06 | 字段「产业介绍」 | 富文本 | 人工编写，或大模型生成后人工校对 |
| `dev_history` | 发展历程 | `history` | F-CHAIN-OV-08 | 阶段 / 里程碑 / 影响与证据文案 | 时间线条目（标题、日期、正文；来源可选） | 同上 |
| `sz_feature` | 特色优势（深圳状况） | `shenzhen` | F-CHAIN-OV-09 右栏 | 字段「特色优势」 | 富文本 | 同上 |
| `cluster_effect` | 集群效应 | `shenzhen` | F-CHAIN-OV-09 右栏 | 字段「集群效应」 | 富文本 | 同上 |
| `competitive_position` | 竞争地位 | `shenzhen` | F-CHAIN-OV-09 右栏 | 字段「竞争地位」 | 富文本 | 同上 |

说明：

- 五个块均绑定当前页 **`industry_id`（L0）**；切换顶部产业选择器后整页更换对应已发布内容。  
- 「深圳状况」与 Wireframe「特色优势」同栏落点，使用 `sz_feature`，避免另造悬空 Tab。  
- **本轮不纳入本文**：全景节点简介、产业资讯事件线、图谱结构/标签/市场规模等（另文约定）。

---

## 3. 程序计算边界（CMS 不背数）

| 页面呈现 | 典型落点 | 数据来源 | CMS |
| --- | --- | --- | --- |
| 企业数 / 机构数 | F-06 概况 KPI；F-09 深圳 KPI | ADS / 指标服务（`metric_id`） | ❌ 不背数 |
| 区域分布（全球/全国/区域地图或列表） | F-06～07 | 程序聚合 | ❌ |
| 深圳各区地图 / 列表及区级计数 | F-09 左栏 | 程序聚合 + 指标 | ❌ |
| 快照时间（若界面展示） | 概况 / 深圳元信息 | ADS 物化元数据 | ❌ |
| §2 五个文案块 | 见上表 | CMS `published` | ✅ |

并存规则：同一屏可同时出现「CMS 正文 + 指标数字」；CMS 正文**不得**内嵌不可追溯的假指标数字顶替 ADS。

---

## 4. 内容对象合同（最小集）

### 4.1 通用字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `block_key` | string | §2 键 |
| `industry_id` | string | L0 产业 |
| `title` | string | 可选 |
| `body_richtext` | html/md | 单块正文（介绍 / 特色 / 集群 / 竞争） |
| `locale` | string | 默认 `zh-CN` |
| `status` | enum | `draft` / `in_review` / `published` / `archived` |
| `published_at` | datetime | 前台只读此态 |
| `version` | int | 乐观并发 |
| `updated_by` | string | 审计 |

### 4.2 发展历程条目扩展

| 字段 | 说明 |
| --- | --- |
| `event_date` | 排序键 |
| `title` | 阶段或里程碑标题 |
| `body_richtext` | 说明 |
| `source_name` / `source_url` | 可选证据 |

---

## 5. 前台消费规则

| 规则 | 说明 |
| --- | --- |
| 对象键 | 仅用当前 `industry_id`；与顶部 L0 选择器一致 |
| 只读 published | `status != published` 不出现在业务模式 |
| 缺块 | 该块空态说明；**禁止**用算法实时生成正文冒充 CMS |
| 本页无维护 | 不提供编辑、审核、发布控件（IA：CMS→总览只读） |
| 评审模式 | 可挂内容版本 / 来源说明；业务模式 DOM 不出现评审层文案 |

---

## 6. 维护端边界

| 承接 | 不承接 |
| --- | --- |
| 按 `industry_id` + `block_key` CRUD §2 五块 | 图谱节点/边、上中下游标签、投入产出、市场规模 |
| 发布 / 撤回 / 版本 | 企业数 / 机构数 / 区域分布的录入或改数 |
| L4 OPS/SYS 维护权限 | 把 CMS 正文写入诊断 Python 特征或 DWD 指标事实表 |

维护壳可复用产业维护导航壳层；`content_type` 与字段须产业域新建，不复用企业维护字段。

---

## 7. 接口骨架（最小）

| 方法 | 路径建议 | 说明 |
| --- | --- | --- |
| GET | `/topic/v1/cms/industries/{industry_id}/blocks?keys=` | 前台批量取已发布块（及历程条目） |
| * | `/admin/v1/cms/...` | 维护端（权限域与业务 API 分离） |

调用链：前台 / 维护 UI → Java；**禁止**为填充 CMS 调用诊断类 Python `/internal/*`。

---

## 8. 开放项

| ID | 问题 | 建议 |
| --- | --- | --- |
| CMS-OV-01 | 历程是否拆「阶段」与「里程碑」两套 content_type | 体验 Owner 按 Wireframe F-08 定一版后回填 §4.2 |
| CMS-OV-02 | 富文本附件存储桶 | 架构定稿后补路径，不阻塞落位表 |
| CMS-OV-03 | 与 CHAIN-OPS 维护菜单挂接 | coordinator 登记实现任务时引用本文 §2 |

---

## 9. 检查清单

- [x] 五块均有 Tab / Frame / Wireframe 锚点  
- [x] CMS 与程序算项对照表已写清  
- [x] 明确不耦合算法、不混用 DWD/ADS  
- [ ] 维护端 content_type 与 Demo/admin 路由落地（实现阶段）  
- [ ] 前台空态文案与 UX-SPEC 联调确认  
