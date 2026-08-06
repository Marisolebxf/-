# Wireframe-CHAIN-OPS-维护管理

> **模块**：CHAIN-OPS · 产业链维护管理  
> **版本**：v0.1 · 2026-08-06  
> **轨道**：Track-MS · medium  
> **路由**：`/industry-center/maintenance?tab={zone}`

## F-CHAIN-OPS-00 · 全量菜单壳

| 区域 | 内容 |
| --- | --- |
| 页头 | 标题「维护管理」；副文案「内容运营 5 · 图谱运营 4 · 分析配置 6」 |
| 左栏 | 三分组导航，15 项一级能力（见能力全清单 §E） |
| 右栏 | 当前 tab 工作区 |
| 权限 | 无 `menu:chain:maintenance` → 全页锁态，不渲染写控件 |

**状态**：默认 `tab=portal`；切换写 URL `?tab=`；占位项显示「占位」角标但可进入。

---

## F-CHAIN-OPS-01 · 门户内容工作台（A1）

| 字段/控件 | 说明 | metric_id |
| --- | --- | --- |
| 产业选择 | L0 `industry_id` | — |
| 内容类型 | `block_key`：industry_intro / dev_history / sz_feature / cluster_effect / competitive_position | — |
| 列表列 | 标题、产业、类型、状态、更新时间、编辑人、版本 | — |
| 职责 Tab | 待我处理 / 全部 / 审核中心 / 发布中心 / 版本与审计 | — |
| 主操作 | 新建、编辑、保存草稿、提交审核、通过/退回、发布、下线 | — |
| 正文 | 富文本 / 历程条目（date+title+body） | — |
| 禁止区 | 企业数、机构数、区域分布计数录入 | ADS 只读，CMS 不背数 |

**空态**：无草稿时说明「可新建产业全景内容」；**错误态**：无权限锁；并发冲突提示乐观锁版本。

---

## F-CHAIN-OPS-02 / 03 · 审核发布 / 版本

复用 F-01 壳内职责 Tab；审核中心仅 `pending_review`；发布中心仅 `pending_publish`；版本中心展示快照列表与「基于此版本开草稿」。

---

## F-CHAIN-OPS-04～11 · 占位可评页

| Frame | tab | 必备信息 |
| --- | --- | --- |
| F-04 | entity | 能力名、招标锚点、路由、占位说明 |
| F-05 | entity_dynamics | 同上 |
| F-06 | expert_knowledge | 同上 |
| F-07 | visualization | 同上 + IC-42 |
| F-08 | lifecycle | 同上 |
| F-09 | relation_lifecycle | 同上 |
| F-10 | entity_attrs | 同上 |
| F-11 | graph_draw | 同上 + §5.6.1.1 |

占位页 **Alert**：能力已列入全量菜单，禁止删除；深度交互后续迭代。

---

## F-CHAIN-OPS-12 · 分析配置入口

左栏 C1–C6 任一项进入同一占位模板；评审模式显示「角色待确认」⚠（GAP-CHAIN-OPS-ROLE）。

## 检查清单

- [x] 15 项导航齐全  
- [x] A1 对齐 SPEC-CMS 五块  
- [x] CMS 不背 ADS 计数  
- [x] 权限锁态  
- [x] 不硬套企业字段  
