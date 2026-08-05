# UX-SPEC-SVCCHAIN-ECOSYSTEM｜服务链生态 交互规格

> **版本**：v1.0-r2
> **交互权威**：`UX-UE 通用交互组件规范.md`；视觉 token 以 `Design.md` 为准
> **配套**：USM（故事与 AC）、Wireframe（结构与字段）、TRACE（追溯）

## 1. 用户旅程

```text
J1 补链强链决策（GOV）：进入链路页签 → 看全链结构 → 读瓶颈判定 →
   定位问题环节 → 环节详情看供给机构 → （入对比篮/开画像核实）→ 形成补链判断
J2 生态枢纽洞察（PARK）：进入图谱页签 → 过滤关系/节点类型 →
   看网络结构与中心性 TOP → 下钻机构画像 → 识别关键枢纽
J3 能级对标研判（RESEARCH）：进入深圳现状页签 → 读统一框架与口径 →
   选对比指标 → 看五城市对比与梯队 → 读优势短板结论（知悉演示口径）
```

## 2. 状态机

### 2.1 页面外壳

```text
ready ──切页签/领域──▶ ready（重算）
```

页面无空集合闸门（链路/图谱/对比不依赖用户先选机构）；领域切换即重算，不弹确认。

### 2.2 环节详情面板

`closed ⇄ open(stage_id)`；URL `segment` 参数为唯一真源；参数非法 → 清参数 + Message，不进入 open。领域切换时若面板开启则原环节刷新数据（环节结构不随领域变化，机构列表随领域重算）。

### 2.3 图谱过滤

```text
default(全选) ──改过滤──▶ filtered ──重置──▶ default
                              │过滤后空
                              ▼
                        empty_hint（图区文案，过滤器保留）
```

### 2.4 深圳对比

```text
ready ──改指标选择──▶ ready（重绘）
         │全部取消
         ▼
   need_metric（提示"至少选择一个对比指标"，保留上次图形不渲染空轴）
```

## 3. 反馈与错误恢复

| 场景 | 反馈 | 恢复 |
| --- | --- | --- |
| 判定行点击定位 | 对应环节卡高亮 + 滚动入视口 | 高亮 2s 后消退 |
| 图表渲染异常 | 容器内 Alert + 重试按钮 | 点击重试重新渲染 |
| localStorage 恢复失败 | 回落默认 + Message"已恢复默认配置" | 重新配置 |
| URL 参数非法（field/segment/org/tab） | 清除该参数 + Message | 页面按余下参数正常渲染 |
| 机构加入对比篮 | Message"已加入对比篮"；重复点击=移除 | 系统篮入口角标即时同步 |
| 对比篮已满（50） | Message"对比篮已满，请移除部分机构后再加入"，不写入 | 打开系统篮移除 |

## 4. 键盘与无障碍

- 页签 Tabs：←/→ 切换，Enter 激活；`role=tablist/tab`，`aria-selected` 同步。
- 环节卡、判定行、中心性 TOP 机构名、环节详情机构行：Tab 可达、Enter 触发，带 `aria-label`。
- Drawer：打开焦点入内、Esc 关闭、关闭后焦点回触发元素。
- 图谱节点键盘不可逐个聚焦（EChart canvas 限制）：统计面板与摘要区提供等价文本路径（中心性 TOP 列表可下钻同一抽屉）。
- 问题标注不只靠颜色：红/橙高亮伴随"服务空白/薄弱环节/资源瓶颈"文字标签；柱状图 hover 有数值文本。

## 5. 响应式（medium_1440_1920）

- ≥1680：链路 6 环节单行；图谱 + 统计面板并排（图 70% / 面板 30%）。
- 1440：链路环节 3×2 两行折行（保留箭头方向指示）；统计面板换行至图下方。
- 环节详情 Drawer 520px、画像抽屉 480px 不变。

## 6. 持久化契约（localStorage，key `topic-svc-eco`，版本字段 `v`）

| 字段 | 内容 | 版本策略 |
| --- | --- | --- |
| `tab` | 激活页签 chain/graph/shenzhen | `v` 不符→回默认 |
| `fieldId` | 产业领域 | 同上（与 R1 叶子独立持久化，语义同源字典） |
| `graphRelTypes` | 关系类型多选 | 同上 |
| `graphNodeTypes` | 节点类型多选 | 同上 |
| `graphFocusOrg` | 聚焦机构 org_id 或 null | 失效 org → 清除 |
| `szMetrics` | 深圳对比指标多选 | 未知指标 → 过滤剔除 |

URL 参数（`tab/field/segment/org`）优先级高于 localStorage；两者随交互双向同步。

## 7. ReviewMode 集成

- 所有 D9 角标经 `ServiceReviewMount`（R1 已建，扩展数据）：`reviewMode=false` 时组件返回 null（自闸），DOM 零泄漏。
- mount_id 命名：`SVC-ECO-{FRAME}-{FIELD}-{KIND}`，如 `SVC-ECO-F02-BOTTLENECK-MISSING`。
- D1 missing（`M_SVC_CHAIN_BOTTLENECK` / `M_SVC_GRAPH_INFLUENCE` / `M_SVC_SZ_CHAIN_COMPLETENESS`）点开只显 Q-SVCCHAIN-03/04 治理引用，不显伪 8 件套。

## 8. 机器可读交付契约

```yaml
frames:
  - {id: F-SVC-ECO-01, route: /service/chain-analysis, component: ServiceChainEcosystemPage(shell)}
  - {id: F-SVC-ECO-02, route: "?tab=chain", component: ChainLinkView}
  - {id: F-SVC-ECO-03, route: "?tab=graph", component: EcosystemGraphView}
  - {id: F-SVC-ECO-04, route: "?tab=shenzhen", component: ShenzhenCompareView}
  - {id: F-SVC-ECO-05, route: "?segment=stage-*", component: StageDetailDrawer}
  - {id: F-SVC-05, route: "?org=svc-org-*", component: OrgProfileDrawer(复用 R1)}
stores:
  - {file: src/app/pages/service-center/serviceEcosystemStore.ts, pattern: reducer + localStorage, key: topic-svc-eco}
data:
  - {file: src/app/pages/service-center/serviceEcosystemData.ts, deterministic: true}
review:
  - {mount: ServiceReviewMount, readiness: serviceReadinessSeed.ts(扩展), reviewData: serviceReviewData.ts(扩展)}
acceptance_source: USM-SVCCHAIN-ECOSYSTEM.md#4（AC-US-SVC-ECO-01..06）
```
