# Wireframe-ENT-SZSTATUS.md

> **模块**：深圳企业现状分析（E-25）
> **版本**：v1.7-draft
> **对应 IA**：`IA-ENT-SZSTATUS.md`
> **对应 USM / TRACE**：`USM-ENT-SZSTATUS.md` / `TRACE-ENT-SZSTATUS.yaml`
> **阶段**：Track-MS；门 1 PDR 输入；V1 高保真首轮定义基线
> **屏幕层级**：`medium_1440_1920`
> **权威路由**：`/enterprise-center/shenzhen-enterprise-status-analysis`
> **范围真源**：`bid-reference/科技信息展示系统和科技专题服务系统.md` → `§1.1.1.2.4.2.3.5～§1.1.1.2.4.2.3.5.2`

## 1. Frame 清单

| Frame | 触发入口 | 目的 | 原始需求 / TRACE |
| --- | --- | --- | --- |
| F-SZSTATUS-00 页面壳与共享坐标系 | 新权威路由 | 固定深圳并选择产业链、分析任务 | E-25 / US-01～04 |
| F-SZSTATUS-01 产业链定位与企业清单 | 默认 Tab | 理解深圳企业数量、环节和链中角色，并编组企业对象 | E-25.1 / US-01、02 |
| F-SZSTATUS-02 完整企业详情宽幅 Drawer | 企业表格“查看详情” | 不离开定位上下文查看完整企业详情页签 | US-02 产品解释 |
| F-SZSTATUS-03 多城市横向对标 | 对标 Tab | 比较深圳、全国及重点城市 | E-25.2 / US-03 |

## 2. Frame F-SZSTATUS-00：页面壳与共享坐标系

### 2.1 中屏线框图

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ 深圳企业现状分析                                      数据更新至 2026-XX-XX │
│ 聚焦深圳企业在当前产业链中的位置、相对优势与生态完整性                     │
├──────────────────────────────────────────────────────────────────────────┤
│ 城市锚点  [ 深圳（固定） ]   产业链  [ 请选择产业链                 ▾ ]     │
├──────────────────────────────────────────────────────────────────────────┤
│ [ 产业链定位 ] [ 多城市横向对标 ]                                        │
├──────────────────────────────────────────────────────────────────────────┤
│ 当前 Tab 专属输入与结果区                                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

### 2.2 区块与字段

| 区块 / 控件 | 用户目的 | 字段 | 默认与联动规则 |
| --- | --- | --- | --- |
| 页面标题 | 明确任务 | `深圳企业现状分析` | 不随 Tab 改名 |
| 数据更新时间 | 理解结果时点 | `display_updated_at` | 业务可见 |
| 城市锚点 | 明确分析主语 | `anchor_city=深圳` | 只读，不渲染可编辑城市选择 |
| 产业链选择 | 建立共同分析对象 | `industry_chain_id` | 必选；无值时两个结果区待选择 |
| 分析 Tab | 切换定位与对标 | `view` | 默认 `chain-position` |

### 2.3 交互

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 选择产业链 | 刷新两个视图；定位环节回到全部；清除旧链页内勾选 | 不删除对比篮已有对象 |
| 切换 Tab | 显示当前 Tab 专属输入；共享深圳、产业链与更新时间 | 不把环节转换成城市条件 |
| 刷新页面 | 从合法 URL 状态恢复 Tab 与产业链；非法值回到安全默认 | 不回退旧路由或旧页面 |

### 2.4 状态

| 状态 | 表现 | 用户下一步 |
| --- | --- | --- |
| 未选产业链 | 结果区显示“请选择产业链开始分析” | 选择产业链 |
| 加载 | 共享上下文不抖动；结果区骨架 | 等待 |
| 错误 | 保留产业链和 Tab，显示重试 | 重试 |
| 无权限 | 页面说明锁态，结果和动作不可用 | 返回或申请权限 |

## 3. Frame F-SZSTATUS-01：产业链定位与企业清单

### 3.1 中屏线框图

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ 产业链定位                     产业链环节 [ 全部环节              ▾ ]      │
├──────────────────┬──────────────────┬──────────────────┬─────────────────┤
│ 深圳相关企业数    │ 覆盖环节数       │ 重点环节企业数    │ 产业链完整度      │
│ 128 家            │ 8 / 10           │ 63 家             │ 80%              │
├──────────────────────────────────────┬───────────────────────────────────┤
│ 产业链环节分布（主视图）              │ 链中角色分布                       │
│ 上游 → 中游 → 下游                    │ 链主 / 上游 / 中游 / 下游           │
│ 各节点企业数与选中态                  │ 当前筛选集合的角色结构               │
├──────────────────────────────────────┴───────────────────────────────────┤
│ 深圳相关企业                                                  共 128 家   │
│ [搜索企业名称                              ]                              │
├────┬──────────────────┬────────┬────────────┬──────────┬────────────────┤
│ 选 │ 企业名称          │ 所在区  │ 所属环节    │ 链中角色  │ 操作            │
├────┼──────────────────┼────────┼────────────┼──────────┼────────────────┤
│ □  │ 企业 A            │ 南山区  │ 核心器件    │ 上游      │ 查看详情         │
│ □  │ 企业 B            │ 宝安区  │ 系统集成    │ 链主      │ 查看详情         │
├────┴──────────────────┴────────┴────────────┴──────────┴────────────────┤
│ [全选当前结果]  已选 2 家                                  [加入对比篮]  │
└──────────────────────────────────────────────────────────────────────────┘
```

> 图中数值仅说明布局，不构成正式业务口径或验收数据。

### 3.2 字段与指标

| 区块 / 控件 | 用户目的 | 字段 / metric_id | 默认与联动规则 |
| --- | --- | --- | --- |
| 环节选择 | 收窄深圳企业集合 | `industry_chain_node_id` | 默认全部；只影响定位视图 |
| 深圳相关企业数 | 掌握本地产业基础 | `M_ENT_SZ_COUNT` | 当前链 + 当前环节 |
| 覆盖环节数 | 理解覆盖范围 | `M_ENT_KEY_NODE_COUNT` 的覆盖节点派生 | 当前链；口径在评审说明 |
| 重点环节企业数 | 识别关键节点企业规模 | `M_ENT_KEY_NODE_COUNT` | 当前链 + 环节 |
| 产业链完整度 | 理解生态完整性 | `M_ENT_CHAIN_COMPLETENESS` | 公式待闭合 |
| 环节分布 | 理解企业落点 | `industry_chain_node_id` + 企业数 | 点击节点只改变定位局部选择 |
| 链中角色分布 | 理解企业作用 | `M_ENT_SZ_CHAIN_POSITION` | 缺失角色单列“暂未标注” |
| 企业表格 | 核验定位结果 | 企业名称 / 所在区 / 所属环节 / 链中角色 | 直接位于页面内；首列为选择控件，故固定左侧前两列“选择 + 企业名称”，操作列固定右侧 |
| 查看详情 | 核验完整企业详情 | 无图标文字按钮 | 位于固定操作列；不显示前置图标，点击仍打开 F-02 |
| 全选当前结果 | 批量编组对象 | `selected_enterprise_codes[]` | 无搜索时作用于当前筛选结果；有搜索时只作用于当前搜索结果 |
| 已选数量 | 理解当前批量对象 | `selected_count` | 翻页保留；切换产业链清空 |
| 加入对比篮 | 继续使用对象 | 企业编码和来源上下文 | 不自动跳转，不显示“查看对比篮” |

### 3.3 交互

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 选择环节 | KPI、两个分布区和企业清单同时刷新 | 不改变城市对标城市集合 |
| 点击环节节点 | 选中节点并收窄企业集合，表格数量同步 | 不自动打开 Drawer |
| 点击角色项 | 收窄企业清单并反馈当前角色 | 不反写环节选择 |
| 点击全选当前结果 | 选择当前筛选或搜索结果；控件进入全部选择态 | 不选择当前结果之外的不可见对象 |
| 部分对象已选 | 全选控件显示部分选择态 | 不把部分选择误显示为全部选择 |
| 点击取消全选 | 只取消当前筛选或搜索结果中的对象 | 不清空其他筛选条件下已保留的对象 |
| 点击查看详情 | 打开 F-02，传入企业编码和当前返回上下文 | 不跳转完整页面，不打开第二层清单 Drawer |
| 点击加入对比篮 | 提交明确选择的企业并显示成功/重复/超限反馈 | 不自动跳转，不生成目标模块结果 |
| 横向滚动企业表 | 只移动所在区、产业链环节和链中角色；选择、企业名称与操作列保持固定 | 不改变分页、筛选或已选对象 |

### 3.4 状态

| 状态 | 表现 | 用户下一步 |
| --- | --- | --- |
| 默认 | 摘要、环节分布、角色分布和页内企业表格 | 探索、查看详情或批量选择 |
| 当前环节无企业 | 稳定空态，保留环节控件 | 改为全部或更换链 |
| 角色数据部分缺失 | “暂未标注”作为正常分组 | 查看清单 |
| 搜索无结果 | 表格空态；全选不可用；已选对象不清空 | 清除搜索 |
| 部分选择 | 全选控件显示部分选择态，底栏显示已选数量 | 继续选择或取消 |
| 对比篮容量已满 | 禁止继续选择并说明剩余容量 | 减少选择 |
| 完整度公式待确认 | 业务模式按批准的 Demo 披露规则展示；评审模式 Pending | 继续查看其他指标 |

## 4. Frame F-SZSTATUS-02：完整企业详情宽幅 Drawer

### 4.1 中屏线框图

```text
背景：产业链定位页（条件、表格、选择和滚动位置保持）
                 ┌────────────────────────────────────────────────────────┐
                 │ 企业名称  [在营]       资质/产业标签       [加入/已加入] │
                 │ 法定代表人 / 注册资本 / 成立时间 / 所属产业 / 信用代码   │
                 │ 链位：当前产业链环节 · 链中角色                 [关闭]   │
                 ├────────────────────────────────────────────────────────┤
                 │ 工商概况 | 主要团队 | 资质荣誉 | 知识产权 | 经营财务     │
                 │ 供应链关系 | 关系图谱 | 舆情动态 | 风险信息 | 招投标      │
                 ├────────────────────────────────────────────────────────┤
                 │ 当前页签完整业务内容                                    │
                 │ 默认：工商概况                                          │
                 │ 字段、权限、脱敏、状态和内部追溯归 ENT-PROFILE           │
                 └────────────────────────────────────────────────────────┘
```

### 4.2 容器与内容契约

| 区块 / 动作 | 规则 |
| --- | --- |
| Drawer 宽度 | `clamp(1040px, 80vw, 1520px)`；属于 `standard_with_extension` |
| 企业头部 | 企业名称、经营状态、资质/产业标签、法定代表人、注册资本、成立时间、所属产业、统一社会信用代码、当前链位 |
| 完整页签 | 工商概况、主要团队、资质荣誉、知识产权、经营财务、供应链关系、关系图谱、舆情动态、风险信息、招投标 |
| 默认页签 | 工商概况 |
| 内容所有权 | 企业字段、权限、脱敏、页签状态和内部评审挂点归 `ENT-PROFILE`；E-25 不复制定义 |
| 返回上下文 | 关闭后恢复产业链、环节、角色、搜索、分页、滚动和已选对象 |
| 对比篮动作 | 只保留“加入 / 已加入对比篮”；不提供“查看对比篮” |

### 4.3 交互与状态

| 触发 / 状态 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 打开详情 | 传入 `enterprise_code` 和 `return_context_id`，默认显示工商概况 | 不只显示企业摘要 |
| 切换页签 | 只更新 Drawer 内容，保持底层定位上下文 | 不改变 E-25 筛选或选择 |
| 单页签无权限 | 保留头部与其他可用页签，目标页签显示锁态 | 不关闭整个 Drawer |
| 单页签加载失败 | 当前页签显示错误与重试 | 不丢失其他页签状态 |
| 关闭 Drawer | 回到原表格位置并恢复上下文 | 不清空选择，不强制刷新 |

## 5. Frame F-SZSTATUS-03：多城市横向对标

### 5.1 中屏线框图

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ 多城市横向对标        固定：深圳、全国参照                               │
│ 对标城市 [ 北京 × ] [ 上海 × ] [ 苏州 × ] [ 广州 × ] [ + 添加城市 ]      │
├──────────────────────────────────┬───────────────────────────────────────┤
│ 同口径多指标雷达对比               │ 当前产业链相对观察                    │
│ 对象 A [ 深圳（固定） ]            │ 当前对比：深圳 vs 对象 B              │
│ 对象 B [ 全国参照 ▼ ]              │ 优势：仅描述可比指标相对高值           │
│ 归一化 0～100；最多展示 A / B       │ 短板：仅描述可比指标相对低值           │
│ [        雷达图 + 底部图例       ]  │ 不输出综合得分或总排名                 │
├──────────────────────────────────┴───────────────────────────────────────┤
│ 城市 × 指标对比表                         数据更新至 2026-XX-XX           │
│ 固定左：对象      ← 中间指标横向滚动 →      固定右：数据状态              │
├────────┬────────────┬────────────┬──────────┬──────────┬───────────────┤
│ 对象    │ 平均技术力  │ 平均商业力  │ 企业密度  │ 完整度    │ 数据状态       │
│ 深圳    │ ...        │ ...        │ ...      │ ...      │ ...           │
│ 全国    │ ...        │ ...        │ ...      │ ...      │ ...           │
│ 北京…   │ ...        │ ...        │ ...      │ ...      │ ...           │
└────────┴────────────┴────────────┴──────────┴──────────┴───────────────┘
│ 共 N 条                                           < 1 / N >              │
```

### 5.2 字段与指标

| 区块 / 控件 | 用户目的 | 字段 / metric_id | 默认与联动规则 |
| --- | --- | --- | --- |
| 固定对象 | 明确本地与全国坐标 | 深圳、全国参照 | 不可移除 |
| 对标城市 | 选择重点城市 | `benchmark_city_codes[]` | 临时默认北上苏广，Q016 待确认 |
| 雷达对象 A | 保持深圳分析锚点 | `radar_object_a=shenzhen` | 固定深圳，不可切换 |
| 雷达对象 B | 聚焦一个外部参照 | `radar_object_b` | 从全国参照与已选城市中单选；默认全国 |
| 平均技术力 | 比较创新能力 | `M_ENT_CITY_AVG_TECH_POWER` | 依赖 Q014 |
| 平均商业力 | 比较商业能力 | `GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER` | metric_id 待登记 |
| 企业密度 | 比较企业集聚 | `M_ENT_CITY_DENSITY` | 分母待确认 |
| 产业链完整度 | 比较生态覆盖 | `M_ENT_CHAIN_COMPLETENESS` | 公式待闭合 |
| 雷达图 | 快速识别深圳与单一参照的相对结构 | 可比指标归一化值 | 可比指标不少于 3 个；最多 A / B 两条轮廓 |
| 对比表 | 核验原始值和单位 | 城市行 × 指标列 / 单位 / 状态 | 始终保留；每页 5 行；深圳固定首行，全国参照固定第二行 |
| 相对观察 | 总结深圳相对对象 B 的优势与短板 | 规则化可比描述 | 与雷达使用同一 A / B；不生成综合得分或排名 |

### 5.3 可比性规则

- 城市间必须使用同一产业链、统计周期、指标版本和单位。
- 全国参照按同一产业链聚合，不使用全产业全国总量。
- 表格以城市为行、指标为列；增加城市只增加行，避免中屏横向膨胀。
- 上层对标城市多选管理完整城市池；雷达对象 B 的可选池为全国参照与当前已选重点城市。
- 雷达对象 A 固定深圳；对象 B 默认全国参照；雷达不同时叠加完整城市池。
- 深圳固定首行并使用轻量强调；全国参照固定第二行；其他城市按用户选择顺序排列。
- 全表数据时点一致时放在表格标题区；只有城市或指标时点不一致时才显示行级状态。
- 单位优先放在列标题或数值旁；表格是精确值主载体，雷达只承担归一化结构概览。
- 缺失值显示正常不可用态，不填 0、不插值、不沿用其他城市值。
- 少于 3 个可比指标时隐藏雷达图；没有可比指标时不输出相对观察。
- 平均商业力正式指标未登记前不得用综合竞争力、营收或利润率替代。
- 表格“对象”列固定左侧，“数据状态”列固定右侧，中间指标列横向滚动；分页每页 5 行。

### 5.4 交互

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 添加/移除对标城市 | 刷新对象 B 可选池和完整对比表；当前 B 仍有效时保持不变 | 不移除深圳或全国参照 |
| 移除当前对象 B 对应城市 | 对象 B 回退全国参照，刷新雷达与相对观察 | 不保留失效对象或显示空白雷达 |
| 切换雷达对象 B | 只刷新雷达与相对观察，完整城市对比表不裁剪 | 不改变上层城市池 |
| 切换城市表页码 | 只切换当前 5 行 | 不改变城市池、雷达 A / B 或相对观察 |
| 横向滚动城市表 | 只移动中间指标列，首尾列保持固定 | 不带动整页或首尾列 |
| 悬停雷达轴 | 显示归一化值、原始值、单位和时点 | 不只显示无单位分数 |
| 点击表格不可用态 | 业务模式提供简洁说明；评审模式可查看 Pending | 不暴露 Q 或内部表名给业务用户 |

## 6. 响应式与视觉约束

- **页面类型**：标准分析工作台；`screen_tier=medium_1440_1920`。
- **系统边界**：科技专题服务系统不创建小屏/移动交付；浏览器小于 1440px 时只保证安全溢出，不重构为移动导航。
- **布局**：遵循 `Design.md` 中屏 Header、Sidebar、24 栅格和 16px 内容节奏。
- **组件**：产业链、环节和城市使用 Arco Select；Tab、Table、Drawer、Empty、Spin、Alert 使用 Arco 或项目共享封装。
- **企业详情 Drawer**：宽度 `clamp(1040px, 80vw, 1520px)`，属于 `standard_with_extension`；内部完整企业详情可纵向滚动，企业头部与一级页签保持可见。
- **复合控件安全**：禁止原生 `<label>` 包裹 Select；标签和控件作为同级节点或使用 Form.Item。
- **图表边界**：图表引擎只负责环节分布、角色分布和雷达图；条件、标题、图例、空态和详情由页面组件负责。
- **稳定性**：加载、空数据、部分可比和错误状态保持内容区尺寸稳定。

## 7. 业务模式与评审模式矩阵

| 内容 | 业务模式 | 评审模式 |
| --- | --- | --- |
| 深圳、产业链、环节、城市条件 | 显示 | 原样显示 |
| KPI、图表、企业表格、城市对比表 | 显示 | 使用完全相同的业务值 |
| 全选、查看详情、加入对比篮 | 显示并遵循业务权限 | 权限与行为不变 |
| 企业详情头部、页签和当前页签内容 | 显示 | 使用相同对象、页签和内容 |
| 数据更新时间 | 显示 | 显示 |
| Demo 数据披露 | 不进入 DOM | 显示“演示数据，仅用于功能展示” |
| 雷达归一化与承载边界说明 | 不进入 DOM | 显示归一化范围、最多双对象及完整城市池承载位置 |
| RequirementTrace | 不进入 DOM | 在具名宿主显示 |
| metric_id、公式、来源表、版本 | 不进入 DOM | MetricSpec 显示 |
| Mock 批次、来源系统、替换计划 | 不进入 DOM | MockBadge 显示 |
| Q014/Q016 与公式/来源缺口 | 不进入 DOM | PendingBadge 显示 |

- 切换模式不得改变筛选、指标值、城市顺序、企业选择、企业详情当前页签、权限结果或对比篮状态。
- 企业详情 Drawer 内部业务字段和评审挂点归 `ENT-PROFILE`；下方 E-25 合同只登记 Drawer 容器宿主，不复制内部挂点。

## 8. review_trace_contract

```yaml
review_trace_contract:
  - mount_id: ENT-SZSTATUS-F00-TITLE-REQ
    frame_id: F-SZSTATUS-00
    host_label: 深圳企业现状分析页面标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-25, BID-ENT-SZSTATUS, PI-SZSTATUS-01, PI-SZSTATUS-02]
    required_payload: [source_location, source_summary, current_placement, source_relation, interpretation_submodules]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-SZSTATUS-F00-DATA-MOCK
    frame_id: F-SZSTATUS-00
    host_label: 页面标题行数据更新时间后
    marker_type: mock_badge
    source_relation: product_interpretation
    trace_refs: [PI-SZSTATUS-02]
    required_payload: [display_updated_at, calc_batch_id, source_systems, provenance_type, mock_until, planned_tier]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-SZSTATUS-F00-DEMO-DISCLOSURE
    frame_id: F-SZSTATUS-00
    host_label: 共享条件条右侧
    marker_type: review_copy
    source_relation: product_interpretation
    trace_refs: [SZSTATUS-USM-21]
    required_payload: [copy, visibility_rule]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-SZSTATUS-F01-TITLE-REQ
    frame_id: F-SZSTATUS-01
    host_label: 产业链定位标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-25, BID-ENT-SZSTATUS-CHAIN, US-SZSTATUS-01]
    required_payload: [source_location, source_summary, current_placement, source_relation, interpretation_submodules]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-SZSTATUS-F01-CHAIN-METRIC
    frame_id: F-SZSTATUS-01
    host_label: 产业链定位标题
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [US-SZSTATUS-01]
    required_payload: [metric_id, definition, formula, source_tables, source_systems, update_freq, version]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-SZSTATUS-F01-CHAIN-PENDING
    frame_id: F-SZSTATUS-01
    host_label: 产业链定位标题
    marker_type: pending_badge
    source_relation: direct_requirement
    trace_refs: [GAP-SZSTATUS-CHAIN-COMPLETENESS-FORMULA]
    required_payload: [pending_ref, owner, temporary_default, deadline]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-SZSTATUS-F01-LIST-REQ
    frame_id: F-SZSTATUS-01
    host_label: 深圳相关企业清单标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-25, BID-ENT-SZSTATUS-CHAIN, US-SZSTATUS-02, PI-SZSTATUS-03]
    required_payload: [source_location, source_summary, current_placement, source_relation, interpretation_submodules]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-SZSTATUS-F01-BASKET-REQ
    frame_id: F-SZSTATUS-01
    host_label: 深圳相关企业清单标题
    marker_type: requirement_trace
    source_relation: product_interpretation
    trace_refs: [US-SZSTATUS-02, PI-SZSTATUS-03, DEC-SZSTATUS-ENTERPRISE-ACTIONS-20260723]
    required_payload: [source_location, source_summary, current_placement, source_relation, interpretation_submodules]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-SZSTATUS-F02-DETAIL-REQ
    frame_id: F-SZSTATUS-02
    host_label: 完整企业详情宽幅 Drawer 标题
    marker_type: requirement_trace
    source_relation: product_interpretation
    trace_refs: [US-SZSTATUS-02, PI-SZSTATUS-03, DEC-SZSTATUS-FULL-DETAIL-DRAWER-20260723]
    required_payload: [source_location, source_summary, current_placement, source_relation, interpretation_submodules, detail_owner, return_context_id]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-SZSTATUS-F02-DETAIL-MOCK
    frame_id: F-SZSTATUS-02
    host_label: 完整企业详情宽幅 Drawer 标题
    marker_type: mock_badge
    source_relation: product_interpretation
    trace_refs: [US-SZSTATUS-02, DEC-SZSTATUS-FULL-DETAIL-DRAWER-20260723]
    required_payload: [enterprise_code, provenance_type, source_systems, calc_batch_id, mock_until]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-SZSTATUS-F03-TITLE-REQ
    frame_id: F-SZSTATUS-03
    host_label: 多城市横向对标标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-25, BID-ENT-SZSTATUS-CITY, US-SZSTATUS-03, PI-SZSTATUS-04]
    required_payload: [source_location, source_summary, current_placement, source_relation, interpretation_submodules]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-SZSTATUS-F03-CITY-METRIC
    frame_id: F-SZSTATUS-03
    host_label: 多城市横向对标标题
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [US-SZSTATUS-03]
    required_payload: [metric_id, definition, formula, source_tables, source_systems, update_freq, version]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-SZSTATUS-F03-CITY-PENDING
    frame_id: F-SZSTATUS-03
    host_label: 多城市横向对标标题
    marker_type: pending_badge
    source_relation: direct_requirement
    trace_refs: [Q014, Q016, GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER, GAP-SZSTATUS-DENSITY-DENOMINATOR, GAP-SZSTATUS-CHAIN-COMPLETENESS-FORMULA]
    required_payload: [pending_ref, owner, temporary_default, deadline]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-SZSTATUS-F03-RADAR-NOTE
    frame_id: F-SZSTATUS-03
    host_label: 独立雷达工作区对象选择下方
    marker_type: review_copy
    source_relation: product_interpretation
    trace_refs: [SZSTATUS-USM-21]
    required_payload: [normalization_range, max_series, precision_surface]
    review_mode: present
    business_mode: absent
```

### 8.1 挂载规则

- `mount_id` 在本模块内唯一；定义、覆盖、渲染必须按集合一致，不只比较数量。
- 同一宿主的顺序为需求追溯 → 指标说明 → Mock → Pending。
- 页面级评审说明使用独立 `review_copy` 挂点；其他产品解释仍收纳在 `requirement_trace` 的 `interpretation_submodules`。
- 指标、Mock 和 Pending 分别表达定义、来源和待确认状态，不合并为单一图标。
- 业务模式移除全部挂点节点，不保留空图标、空容器、内部说明或布局间距。
- E-25 的 14 个挂点不包含 `ENT-PROFILE` 嵌入内容内部挂点；后者由企业详情自身合同验证，不得重复计数。

## 9. metric_id 清单

| metric_id / gap_id | 状态 | 开放项 |
| --- | --- | --- |
| `M_ENT_SZ_COUNT` | 已登记；待真实数据验证 | — |
| `M_ENT_SZ_CHAIN_POSITION` | 已登记；待真实数据验证 | — |
| `M_ENT_KEY_NODE_COUNT` | 已登记；待真实数据验证 | — |
| `M_ENT_CITY_AVG_TECH_POWER` | 已登记；公式/权重待确认 | Q014 |
| `GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER` | Bid 要求；metric_id 待登记 | 何老师 / 辜少彬 / 唐绍祖 |
| `M_ENT_CITY_DENSITY` | 已登记；分母待确认 | GAP-SZSTATUS-DENSITY-DENOMINATOR |
| `M_ENT_CHAIN_COMPLETENESS` | 已登记；公式待确认 | GAP-SZSTATUS-CHAIN-COMPLETENESS-FORMULA |
| 对标城市默认集合 | 临时北上苏广 | Q016 |

## 10. 后续 Demo 验收测试清单

- [ ] 新权威路由直接渲染独立页面，旧 `/enterprise/status-analysis` 未被复用或修改。
- [ ] 一级分析域按“技术链分析 → 产业链分析 → 企业分析”排列；企业分析内部只新增一个条目，位于重点企业分析与对比篮之间。
- [ ] 深圳固定可见且不可编辑；产业链是两个 Tab 的共享必选条件。
- [ ] 默认 Tab 为产业链定位；环节默认全部。
- [ ] 定位 KPI、环节分布、角色分布和企业清单使用同一结果集。
- [ ] 企业清单同时展示所属环节与链中角色，缺失角色显示“暂未标注”。
- [ ] 页内企业表格支持全选当前结果、取消全选和部分选择态；搜索时只影响当前搜索结果，翻页保留已选对象。
- [ ] 查看详情打开 `clamp(1040px, 80vw, 1520px)` 宽幅 Drawer，默认工商概况并提供完整企业详情页签；关闭后保留上下文。
- [ ] 企业详情内部字段、权限、脱敏与评审挂点复用 ENT-PROFILE，不在 E-25 复制。
- [ ] 加入对比篮不自动跳转，E-25 嵌入态不出现“查看对比篮”等第三个企业动作。
- [ ] 城市对标固定包含深圳与全国参照，临时默认城市为北京、上海、苏州、广州。
- [ ] 城市为行、指标为列的表格始终保留；深圳固定首行，全国参照固定第二行；全表统一时点放在标题区。
- [ ] 可比指标少于 3 个时雷达不渲染；缺失值不补 0。
- [ ] 页面不生成综合竞争力得分、总排名、风险、推荐或报告。
- [ ] 评审模式 E-25 挂点集合恰为 14 个；业务模式挂点 DOM 为 0；ENT-PROFILE 内部挂点按自身合同另行验证。
- [ ] 切换业务/评审模式时筛选、指标值、城市顺序、企业选择、详情页签、权限和篮状态不变。
- [ ] 真实指针验证覆盖两个 Tab、产业链 Select、环节 Select、城市多选、企业详情 Drawer 和加入对比篮。
- [ ] 变更 JSX/TSX 通过复合标签检查器，无原生 label 包裹 Arco 复合控件。
- [ ] 1920、1680、1440 三档中屏截图通过同类分析页面几何与密度比较。

## 11. Wireframe 自检

- [x] 4 个 Frame 对应 IA、USM 与 TRACE。
- [x] 固定深圳、共享产业链、两个专属输入的状态关系明确。
- [x] 两项 Bid 子功能均有完整主路径、空态和异常态。
- [x] 企业清单动作严格限于查看详情和加入对比篮。
- [x] 页内清单、全选三态、分页保留与容量限制已定义。
- [x] 查看详情明确为完整企业详情宽幅 Drawer，内容所有权归 ENT-PROFILE。
- [x] 城市表格为精确值主载体，雷达为结构概览。
- [x] 全国参照、城市选择和可比性降级规则明确。
- [x] 所有业务指标均有 metric_id 或显式 gap_id。
- [x] 14 个 E-25 评审挂点具名且业务模式均为 absent；企业详情内部挂点不重复声明。
- [x] 未引入报告、导出、评估、风险或推荐能力。
