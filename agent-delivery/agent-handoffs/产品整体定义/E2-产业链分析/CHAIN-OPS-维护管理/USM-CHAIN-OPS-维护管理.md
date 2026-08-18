# USM-CHAIN-OPS-维护管理

> **模块**：CHAIN-OPS · 产业链维护管理  
> **版本**：v0.1 · 2026-08-06 · `[agent:product-agent]`  
> **对应 IA / TRACE / Wireframe**：同目录  
> **验收索引**：`IC-42` / `IC-43`（门户内容管理 · 产业全景）  
> **本轮决策（Q068）**：新增映射维护（C7）；前台产业选择先集群。CMS 对象键仍是 L0 `industry_id`。

## 故事清单

| ID | 标题 | 角色 | 优先级 | 来源关系 |
| --- | --- | --- | --- | --- |
| US-CHAIN-OPS-01 | 编辑产业全景门户内容草稿 | 内容运营 | P0 | direct · §5.6.1 / IC-43 |
| US-CHAIN-OPS-02 | 审核与发布产业全景内容 | 内容审核 / 发布管理 | P0 | direct · §5.6.1 / IC-43 |
| US-CHAIN-OPS-03 | 查看版本与回滚为新草稿 | 内容运营 / 发布管理 | P1 | product_interpretation |
| US-CHAIN-OPS-04 | 维护产业主体标识信息 | 数据治理 | P1 | product_interpretation |
| US-CHAIN-OPS-05 | 维护产业动态与资讯稿 | 内容运营 | P2 | product_interpretation |
| US-CHAIN-OPS-06 | 维护产业专家知识 | 内容运营 / 图谱协作 | P2 | product_interpretation · §5.6.1 |
| US-CHAIN-OPS-07 | 配置产业可视化方案 | 平台产品 | P2 | product_interpretation · IC-42 |
| US-CHAIN-OPS-08 | 管理产业链实体生命周期 | 图谱工程师 | P1 | product_interpretation · §5.3 |
| US-CHAIN-OPS-09 | 管理产业链关系链生命周期 | 图谱工程师 | P1 | product_interpretation |
| US-CHAIN-OPS-10 | 管理产业实体属性 | 图谱工程师 | P2 | product_interpretation |
| US-CHAIN-OPS-11 | 绘制并导出产业链图谱 | 图谱工程师 | P0 | direct · §5.6.1.1 |
| US-CHAIN-OPS-12 | 浏览分析配置六分区入口 | 分析配置运营 | P1 | product_enhancement（壳复用；角色待确认） |
| US-CHAIN-OPS-13 | 维护产业集群到 L0 的映射 | 数据治理 | P0 | product_interpretation · Q068 |

---

### US-CHAIN-OPS-01 · 编辑产业全景门户内容草稿

**作为** 内容运营人员，**我想** 按 `industry_id` + `block_key` 创建或编辑产业介绍 / 历程 / 深圳文案草稿，**以便** 门户总览只展示已发布权威内容。

**验收**：

1. 可选 `block_key` ∈ SPEC-CMS 五块；对象键为 L0 `industry_id`。  
2. 可保存草稿、提交审核；不可在本页直接改 ADS 企业数/机构数。  
3. 无维护权限时入口锁态，不暴露编辑控件。

### US-CHAIN-OPS-02 · 审核与发布

**作为** 审核/发布人员，**我想** 对待审内容通过或退回，并将待发布内容上线，**以便** 前台总览消费 `published` 态。

**验收**：状态机含 draft / returned / pending_review / pending_publish / published / offline；发布后总览只读侧可见；CMS 不背程序计数。

### US-CHAIN-OPS-03 · 版本与回滚

**作为** 发布管理人员，**我想** 查看历史版本并基于旧版本开新草稿，**以便** 纠错可追溯。

### US-CHAIN-OPS-04～07 · 内容运营其余项

各入口在左侧导航独立可见；V1 Demo 允许占位页，但**禁止删除菜单项**。字段为产业域，不出现企业工商字段。

### US-CHAIN-OPS-08～11 · 图谱运营

B1–B4 独立入口；B4 对应「未来产业链图谱维护」结构绘制与关键环节标注（§5.6.1.1）。V1 可为占位+路由可达。

### US-CHAIN-OPS-12 · 分析配置六分区

C1–C6 全量列入；角色正式名称待业务确认（⚠）；不得把 OPS/SYS 实现岗倒灌为源需求岗位。

### US-CHAIN-OPS-13 · 维护产业集群到 L0 的映射

**作为** 数据治理人员，**我想** 在不增删 15 个集群名字的前提下，改某个集群挂上的 L0，**以便** 三个前端菜单不用改名单也能跟上领导关注点。

**验收**：

1. 15 个 `cluster_id` 只读（换政策版除外）。  
2. 映射目标必须是已存在的 L0 `industry_id`；允许 0 条。  
3. 本轮同一 L0 不挂两个集群。  
4. 不改 `industry_chain`，不写 `gkxlumenx_cfg`。

## 非目标

- 不在维护菜单内嵌产业周期/堵点/区域评价业务分析页。  
- 不把 CMS 富文本当作算法输入。  
- 不复制 ENT-OPS 企业 content_type。
