# UX-SPEC-ENT-KEYENT｜重点企业分析

> 版本：v1.1 · 2026-07-31
> 状态：ready_for_v1
> 四件套版本：v2.0
> Track：Track-MS
> screen_tier：medium_1440_1920

## 1. 权威输入与边界

本规格只把当前四件套中的产品行为转换为可执行交互，不改变产品范围，也不修改 Demo：

- `IA-ENT-KEYENT.md` v2.0
- `TRACE-ENT-KEYENT.yaml` v2.0
- `USM-ENT-KEYENT.md` v2.0
- `Wireframe-ENT-KEYENT.md` v2.0
- `agent-delivery/产品定义评审规程.md`
- `agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md`
- `agent-delivery/Design.md`
- `agent-delivery/data-lineage-policy.md`

原始需求仍只有 Bid `§1.1.1.2.4.2.3`、`.3.1`、`.3.2` 及其叶子。`DEC-KEYENT-COMPARE-INPLACE-20260731` 是本次经 human:高颖 确认的产品解释：系统对比篮拥有对象选择与管理，重点企业领域页只消费对象并生成 E-22 结果。它不新增 Bid 叶子、不声明 Gate 通过、不分配实际 `delivery_tier`。

明确排除：E-23～E-30、E-33 的分析结果；对比篮生命周期管理；新的导出、推荐、权重编辑、任务管理；`small_reflow` 与 Track-L。

## 2. 四件套同步核对

### 2.1 故事与落点

| Story | 角色 | 主落点 | 关键交互 |
| --- | --- | --- | --- |
| US-KEYENT-01 | 政府产业治理人员 | F-KEYENT-00/01 | 按范围、时间、产业与类型发现企业 |
| US-KEYENT-02 | 园区招商与企业服务人员 | F-KEYENT-01/02 | 地图/列表透视、清单 Drawer、加入对比篮 |
| US-KEYENT-03 | 投资机构产业研究人员 | F-KEYENT-03/04 | 消费明确企业对象并查看领域布局 |
| US-KEYENT-04 | 园区招商与企业服务人员 | F-KEYENT-02/03 | 从类型结果编组对象，并由系统对比篮分发/调整 |
| US-KEYENT-05 | 政府产业治理人员 | F-KEYENT-04/05 | 核验领域识别依据并继续研判 |

### 2.2 Frame、路由、状态与禁止行为

| Frame | 宿主 | 必备状态 | 主要禁止行为 |
| --- | --- | --- | --- |
| F-KEYENT-00 | `/enterprise-center/key-enterprise-analysis` | default/loading/error/permission | Tab 后置；跨 Tab 串用条件；业务模式泄漏内部词 |
| F-KEYENT-01 | `?view=type` | default/loading/empty/error/permission/peer-insufficient | 第二个区域选择器；地图反写顶部范围；补造同级对象 |
| F-KEYENT-02 | 企业清单宽 Drawer | default/loading/empty/error/permission/partial-selected | 关闭后丢失上下文；搜索全选误选不可见企业 |
| F-KEYENT-03 | `?view=domain` 对象状态行 | empty/validating/populated/partial-invalid/all-invalid/error/permission | 页内企业选择器、可删除 Tag、“返回对比篮”、重复 CTA |
| F-KEYENT-04 | `?view=domain` 结果主区 | loading/populated/empty/error/permission | 对象集不一致；Q013 未闭合指标占位；页面级横向滚动 |
| F-KEYENT-05 | 领域识别依据 Drawer | loading/populated/empty/error/permission | 无证据输出强结论；关闭后丢失选中关系 |

四件套一致性结论：6 个 Frame、5 个故事、1 个权威路由、`medium_1440_1920` 与 14 个 review mount 均有明确落点。ENT-COMPARE v2.8 已冻结“重点企业分析 → 领域分布分析”、`analysis_type=key-enterprise-domain`、1～50 家对象范围和配置草稿替换动作；F-KEYENT-03 已具备 V1 实施条件。

## 3. 用户旅程与任务流

### 3.1 J-KEYENT-TYPE｜发现并编组重点企业

角色：政府产业治理人员、园区招商与企业服务人员。故事：US-KEYENT-01、02、04。

主路径：

1. 进入权威路由，默认聚焦“类型与区域分析”。
2. 修改区域、时间、产业或企业类型；局部加载后更新 KPI、地图/列表和区域洞察。
3. 在地图范围内下钻，或切换同层级列表；两种视图共享 `mapPath`、当前区域与洞察。
4. 从区域洞察打开企业清单 Drawer；搜索、逐项选择或全选当前结果。
5. 点击“加入对比篮”，收到新增、重复、超限与无效数量汇总；关闭 Drawer 后恢复原工作现场。

异常恢复：当前条件无数据时不自动放宽；下级无数据时保留返回；同级不足 2 个时不渲染比较；点位无坐标时转企业清单；加入失败保留选择并允许重试。

### 3.2 J-KEYENT-DOMAIN｜从系统对比篮分析领域布局

角色：投资机构产业研究人员、园区招商与企业服务人员。故事：US-KEYENT-03、04、05。

主路径：

1. 用户在系统对比篮选择 1～N 家企业并确认“重点企业领域分布分析”。
2. 分发成功后对比篮面板收起；目标页进入 `view=domain`，F-KEYENT-03 显示“来自对比篮 · N 家”、单行企业摘要和“打开对比篮调整对象”。
3. 对象校验完成后，F-KEYENT-04 使用同一 `enterprise_codes[]` 展示领域布局概览、企业领域覆盖、跨领域布局和重点领域分布。
4. 用户打开 F-KEYENT-05 核验领域识别依据；关闭 Drawer 后焦点与选中关系回到触发点。
5. 需要调整对象时，点击 F-KEYENT-03 动作，在当前页原位展开系统对比篮；再次成功分发后更新配置草稿并收起面板。

异常恢复：部分编码无效时移除并汇总提示，剩余对象继续；全部无效时回到单一无对象状态行；对比篮取消、关闭或校验失败时保持展开且不改变目标页草稿；运行中任务与已生成报告保持原快照。

### 3.3 J-KEYENT-DOMAIN-EMPTY｜无对象进入领域分析

角色：投资机构产业研究人员。故事：US-KEYENT-03、04。

主路径：直接切换领域 Tab → F-KEYENT-03 显示“尚未选择分析对象”与唯一“打开对比篮” → 原位展开系统浮层并将任务选择器预选为“领域分布分析” → 用户点击“下一步：前往配置”成功分发后切换为有对象态并加载结果。

异常恢复：无权限打开对比篮时动作保留但禁用并关联原因；空篮时由系统对比篮展示其自身空态；目标页不渲染 F-KEYENT-04/F-KEYENT-05，也不再提供第二个 CTA。

## 4. Frame 与承载映射

| Frame | 入口 | 出口 | 上下文保持 | 跨模块交接 |
| --- | --- | --- | --- | --- |
| F-KEYENT-00 | 权威/兼容路由 | F-01 或 F-03 | 两个 Tab 分别缓存会话状态 | 兼容路由归一，不复制页面 |
| F-KEYENT-01 | `view=type` | F-02、`view=domain` | 顶部筛选与地图浏览状态分离；切换视图保留 | 企业编码及来源摘要可加入 ENT-COMPARE |
| F-KEYENT-02 | 区域洞察次级动作 | 关闭、加入/打开对比篮 | 关闭恢复地图、列表页码、洞察与滚动 | 只发送企业标识与来源，不发送分析结果 |
| F-KEYENT-03 | `view=domain` 或对比篮分发 | F-04、系统对比篮浮层 | 原位开篮不离开路由；成功分发更新配置草稿 | 接收 `analysis_type`、`enterprise_codes[]`、`return_context_id` |
| F-KEYENT-04 | F-03 校验成功 | F-05、后续研判 | 所有结果区共享同一对象集 | 向目标模块传企业编码、来源 Tab 和返回上下文 |
| F-KEYENT-05 | 关系/领域证据动作 | 关闭、企业详情、其他研判 | 关闭后恢复触发关系、滚动与分页 | 只传对象与证据上下文，目标模块自行计算 |

## 5. 交互与状态转换

### 5.1 F-KEYENT-03 对象状态机

| 当前态 | 触发 | 下一态 | 反馈 / 可逆性 |
| --- | --- | --- | --- |
| empty | 点击“打开对比篮” | basket-expanded | 焦点进入系统对比篮标题；关闭后回到按钮 |
| basket-expanded | 取消/关闭 | empty 或 populated | 不改变目标页草稿；焦点回触发按钮 |
| basket-expanded | 成功分发 | validating | 面板收起；状态行保留 64px 并局部 loading |
| validating | 全部有效 | populated | 更新来源、数量、摘要并加载 F-04 |
| validating | 部分无效 | partial-invalid → populated | `Message` 汇总移除数量，继续有效对象 |
| validating | 全部无效 | all-invalid → empty | 汇总提示；F-04/F-05 不渲染 |
| populated | 点击“打开对比篮调整对象” | basket-expanded | 当前结果保留至新分发成功，不提前清空 |
| populated | 新分发成功 | validating | 覆盖配置草稿；运行任务/报告快照保持 |

F-KEYENT-03 的对象名称只读，不提供 Select、可删除 Tag、逐项移除或返回导航。无对象时页面只能存在一个对比篮 CTA。

### 5.2 其他核心交互

- Tab：`ArrowLeft/ArrowRight` 移动，`Enter/Space` 激活；切换只替换当前专属区域，不串改另一 Tab。
- 顶部区域：修改后重置地图到新范围根；地图下钻不反写。
- 地图/列表：只替换 F-01 主舞台；共享面包屑、当前区域、类型选择和洞察。
- 企业清单：全选三态仅按当前搜索结果计算；“取消全选”只移除当前可见集合，“取消选择”清除全部已选。
- 领域结果：KPI、矩阵、图谱、表格均绑定经校验的同一对象集；分页或打开 Drawer 不改变对象集。

## 6. 反馈与异常恢复

| 场景 | 页面反馈 | 恢复动作 |
| --- | --- | --- |
| 首次加载 | 保留 Tab、输入/状态行与各 Frame 尺寸，内容区 Skeleton | 成功后就地替换；失败显示局部重试 |
| 类型结果为空 | 保留筛选与地图容器，说明当前条件无匹配企业 | 调整筛选，不自动放宽 |
| 无领域对象 | 仅 F-03 显示单一 CTA | 原位打开对比篮 |
| 部分对象无效 | `Message` 汇总“已移除 Y 家不可用企业”，继续有效对象 | 打开对比篮补选 |
| 全部对象无效 | F-03 回 empty，结果区不渲染 | 原位打开对比篮重选 |
| 结果加载失败 | F-04 保留标题、工具与容器，显示错误和重试 | 重试不清空对象上下文 |
| 对比篮无权限 | 按钮可见、`aria-disabled=true`，Tooltip/说明关联原因 | 申请权限或继续查看既有结果 |
| 证据为空 | F-05 显示无可核验证据，不输出强结论 | 关闭 Drawer 回到原关系 |

业务模式不显示 Q/GAP、Mock、算法版本或技术批次；评审信息只由既有 review mount 承载。

## 7. 组件、键盘与无障碍

| 交互对象 | Arco / 共享基座 | 键盘与焦点 | ARIA / 状态 |
| --- | --- | --- | --- |
| 一级 Tab | 定制页签 + Tabs 语义 | 左右键移动，Enter/Space 激活 | `role=tablist/tab/tabpanel`、`aria-selected` |
| 类型筛选 | Form、Select、Cascader、DatePicker | Tab 顺序按视觉顺序；Esc 关闭弹层 | label 与控件关联；loading/disabled/error 不只靠颜色 |
| 地图/列表切换 | Segmented/Radio.Group | 左右键选择 | 可访问名称说明当前视图 |
| 对象状态行动作 | Button primary/secondary | Tab 聚焦，Enter/Space 打开系统浮层 | 无权限用真实 disabled 或 `aria-disabled` 并关联原因 |
| 系统对比篮浮层 | 系统共享组件 | 打开后焦点进入标题/首项；关闭或分发后回到触发点或目标页首个有效结果 | `aria-modal=false` 的系统浮层仍需明确标签与焦点边界 |
| 结果表格 | Table、Pagination | 方向键/Tab 浏览，Enter 打开证据 | 表头语义、固定列、无页面级横向溢出 |
| 识别依据 | Drawer | 打开后焦点入标题；Esc 关闭；关闭回触发关系 | 标题关联、loading/error/empty 可感知 |

所有自定义图表、地图、图谱提供等价列表/表格或文本摘要；焦点环不可因视觉还原移除；状态不只依赖颜色；正文与控件遵守 WCAG AA 对比度基线。

## 8. 响应式行为

本模块只支持 `medium_1440_1920`，必须覆盖三个宽度：

| 宽度 | 导航 / 主区 | F-KEYENT-03 | F-KEYENT-01 / F-KEYENT-04 |
| --- | --- | --- | --- |
| 1920 | 导航可展开；24 栅格、16px gutter | 单行 64px；摘要优先完整显示 | 地图 17～18 列、洞察 6～7 列；领域结果并排保持 |
| 1680 | 保持用户导航状态；主区列宽收缩 | 单行 64px；摘要弹性截断，动作不换行 | 地图优先；结果双栏按最小宽度收缩 |
| 1440 | 默认导航收起至 64px；仍为中屏 | 单行 64px；保留来源、数量、动作，企业摘要最先截断 | 地图有效高度不少于 520px；表格只在内部横滑，结果区必要时纵向分段 |

任何宽度均不得把对象动作移到第二张卡或重复空态，不得出现页面级横向滚动，不得切换为移动端导航或底部抽屉。

## 9. 内部评审投影

UX-SPEC 不新增评审标识，只投影 Wireframe 已声明的 14 个挂点：

| Frame | review mounts | 业务模式 |
| --- | --- | --- |
| F-KEYENT-00 | ENT-KEYENT-F00-DATA-TRACE、ENT-KEYENT-F00-INPUT-OWNERSHIP | 全部 absent |
| F-KEYENT-01 | ENT-KEYENT-F01-TITLE-REQ、TYPE-METRIC、TYPE-PENDING、GEO-REQ、GEO-PENDING | 全部 absent |
| F-KEYENT-02 | ENT-KEYENT-F02-SOURCE-REQ | absent |
| F-KEYENT-03 | ENT-KEYENT-F03-OBJECT-REQ、ENT-KEYENT-F03-OBJECT-PENDING | 全部 absent |
| F-KEYENT-04 | ENT-KEYENT-F04-TITLE-REQ、ENT-KEYENT-F04-DOMAIN-METRIC、ENT-KEYENT-F04-DOMAIN-PENDING | 全部 absent |
| F-KEYENT-05 | ENT-KEYENT-F05-EVIDENCE-REQ | absent |

F-03 挂点只落在对象状态行的具名宿主，不落在“打开对比篮”按钮、企业摘要或系统浮层入口上。评审模式开关不得改变对象、字段、权限、布局高度或分发语义。

## 10. Demo 实施交接

建议页面包仍由权威路由承载，优先复用现有 `EnterpriseKeyAnalysisV2Page`、地图/列表状态、企业详情 Drawer 与系统对比篮协调器。F-03 应拆成独立 `DomainObjectContextBar` 候选组件，输入仅含有效对象摘要、校验态、权限态和 `onOpenCompareBasket`，不拥有篮数据写操作。

建议状态：

- `activeView: type | domain`
- `domainObjectState: empty | validating | populated | partial-invalid | error | permission`
- `domainEnterpriseCodes[]`、`domainEnterpriseNames[]`、`returnContextId`
- `openCompareBasket: boolean` 由系统 Shell 协调器管理
- `domainDraftVersion` 只在成功分发后递增

测试关注点：无对象单 CTA；有对象无 Select/可删除 Tag/返回导航；原位打开；取消不改草稿；成功分发收起并更新；部分/全部无效；运行快照不变；1920/1680/1440 无横向溢出；键盘焦点往返；业务模式 14 个挂点均 absent。

明确排除：本 UX-SPEC 不写 Demo 代码、不新增系统浮层能力、不修改任务注册、不宣告 V1 视觉已验证、不改变指标口径。

## 11. 缺口与阻断项

当前无 `blocks_v1: true` 缺口；以下项目继续阻断对应下游阶段，但均有安全、确定的 V1 处理：

| Gap | blocks_v1 | blocks_stages | V1 处理 | Owner / return_to |
| --- | --- | --- | --- | --- |
| GAP-KEYENT-Q010-TYPE-RULE | false | pdr/v1_final/v2_lumen/production | 使用已授权映射演示；评审挂 Q010 | 何老师 / TRACE |
| GAP-KEYENT-Q012-GEO-METRIC | false | pdr/v1_final/v2_lumen/production | 仅演示已定义层级；未闭合指标退出业务结果 | 何老师 / TRACE |
| GAP-KEYENT-Q013-DOMAIN-FORMULA | false | pdr/v1_final/v2_lumen/production | 只展示确定性关系摘要；正式指标不占位 | 唐绍祖 / TRACE |
| GAP-KEYENT-REGIONAL-METRIC-IDS | false | pdr/v1_final/v2_lumen/production | 省略或正常无数据态，不替代指标 | 何老师 / TRACE |
| GAP-KEYENT-COMPARE-INPLACE-V1 | false | v1_final/v2_lumen/production | V1按本规格实现 F-03，现状只作为差距证据 | 孔东 / Wireframe |

## 12. 机器可读交付契约

```yaml
ux_spec_contract:
  module_key: ENT-KEYENT
  version: "1.1"
  status: ready_for_v1
  source_four_pack:
    - IA-ENT-KEYENT.md
    - TRACE-ENT-KEYENT.yaml
    - USM-ENT-KEYENT.md
    - Wireframe-ENT-KEYENT.md
  screen_tier: medium_1440_1920
  delivery_stage: v1_hifi_round1
  product_scope_mutation: prohibited
  demo_code_mutation: prohibited
  journeys:
    - journey_id: J-KEYENT-TYPE
      role: 政府产业治理人员与园区招商企业服务人员
      story_refs: [US-KEYENT-01, US-KEYENT-02, US-KEYENT-04]
      primary_flow: [设置类型分析条件, 浏览地图或列表, 打开企业清单, 加入对比篮]
      abnormal_flows: [条件无结果时调整筛选, 同级不足时隐藏比较, 加入失败时保留选择]
    - journey_id: J-KEYENT-DOMAIN
      role: 投资机构产业研究人员
      story_refs: [US-KEYENT-03, US-KEYENT-04, US-KEYENT-05]
      primary_flow: [对比篮分发对象, 确认对象上下文, 查看领域结果, 核验识别依据, 原位调整对象]
      abnormal_flows: [部分对象无效后继续, 全部无效后重新选择, 对比篮取消时保持草稿]
    - journey_id: J-KEYENT-DOMAIN-EMPTY
      role: 投资机构产业研究人员
      story_refs: [US-KEYENT-03, US-KEYENT-04]
      primary_flow: [进入无对象态, 原位打开对比篮, 成功分发, 加载领域结果]
      abnormal_flows: [无权限时说明原因, 空篮时使用对比篮自身空态]
  frame_specs:
    - frame_id: F-KEYENT-00
      route_or_host: /enterprise-center/key-enterprise-analysis
      source_refs: [US-KEYENT-01, US-KEYENT-02, US-KEYENT-03, US-KEYENT-04, US-KEYENT-05]
      states: [default, loading, error, permission]
      interactions: [切换分析类型, 恢复各自会话状态]
    - frame_id: F-KEYENT-01
      route_or_host: /enterprise-center/key-enterprise-analysis?view=type
      source_refs: [US-KEYENT-01, US-KEYENT-02]
      states: [default, loading, empty, error, permission, peer_insufficient]
      interactions: [修改顶部范围, 地图下钻, 切换地图列表, 打开企业清单]
    - frame_id: F-KEYENT-02
      route_or_host: enterprise_list_wide_drawer
      source_refs: [US-KEYENT-02, US-KEYENT-04]
      states: [default, loading, empty, error, permission, partial_selected]
      interactions: [搜索, 全选当前结果, 取消选择, 加入对比篮, 关闭恢复]
    - frame_id: F-KEYENT-03
      route_or_host: /enterprise-center/key-enterprise-analysis?view=domain#object-context
      source_refs: [US-KEYENT-03, US-KEYENT-04]
      states: [empty, validating, populated, partial_invalid, all_invalid, error, permission]
      interactions: [原位打开对比篮, 成功分发更新配置草稿, 取消保持草稿]
    - frame_id: F-KEYENT-04
      route_or_host: /enterprise-center/key-enterprise-analysis?view=domain#domain-results
      source_refs: [US-KEYENT-03, US-KEYENT-05]
      states: [loading, populated, empty, error, permission]
      interactions: [查看企业领域关系, 切换图例, 分页, 打开识别依据]
    - frame_id: F-KEYENT-05
      route_or_host: domain-evidence-drawer
      source_refs: [US-KEYENT-05]
      states: [loading, populated, empty, error, permission]
      interactions: [查看证据, 查看企业详情, 进入后续研判, 关闭恢复焦点]
  feedback_rules:
    - trigger: 对象分发成功
      response: 收起系统对比篮并进入对象校验
      recovery: 校验失败时保持可重开入口且不清空篮
    - trigger: 部分对象无效
      response: 汇总移除数量并继续有效对象
      recovery: 原位打开对比篮补选
    - trigger: 结果加载失败
      response: 保留对象上下文和结果容器并显示局部重试
      recovery: 重试不清空对象或Tab状态
  responsive_widths: [1920, 1680, 1440]
  accessibility_checks: [keyboard, focus, aria, contrast]
  review_mounts:
    - ENT-KEYENT-F00-DATA-TRACE
    - ENT-KEYENT-F00-INPUT-OWNERSHIP
    - ENT-KEYENT-F01-TITLE-REQ
    - ENT-KEYENT-F01-TYPE-METRIC
    - ENT-KEYENT-F01-TYPE-PENDING
    - ENT-KEYENT-F01-GEO-REQ
    - ENT-KEYENT-F01-GEO-PENDING
    - ENT-KEYENT-F02-SOURCE-REQ
    - ENT-KEYENT-F03-OBJECT-REQ
    - ENT-KEYENT-F03-OBJECT-PENDING
    - ENT-KEYENT-F04-TITLE-REQ
    - ENT-KEYENT-F04-DOMAIN-METRIC
    - ENT-KEYENT-F04-DOMAIN-PENDING
    - ENT-KEYENT-F05-EVIDENCE-REQ
  gaps:
    - id: GAP-KEYENT-Q010-TYPE-RULE
      summary: 企业类型正式判定规则尚未闭合
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: 使用已授权映射演示并在评审模式关联Q010
      owner: human:何老师
      deadline: before_pdr
      return_to: TRACE
    - id: GAP-KEYENT-Q012-GEO-METRIC
      summary: 行政区划精度与密度集聚口径尚未闭合
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: 未闭合指标退出业务结果并保留评审挂点
      owner: human:何老师
      deadline: before_pdr
      return_to: TRACE
    - id: GAP-KEYENT-Q013-DOMAIN-FORMULA
      summary: 领域广度深度多元化正式公式尚未闭合
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: 业务模式只展示确定性关系摘要且正式指标不占位
      owner: human:唐绍祖
      deadline: before_pdr
      return_to: TRACE
    - id: GAP-KEYENT-REGIONAL-METRIC-IDS
      summary: 区域企业规模与占比尚无正式指标标识和数据源映射
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: 省略字段或显示普通无数据态且不使用替代指标
      owner: human:何老师
      deadline: before_pdr
      return_to: TRACE
    - id: GAP-KEYENT-COMPARE-INPLACE-V1
      summary: 当前Demo尚未对齐系统对比篮原位打开与对象上下文去重
      blocks_v1: false
      blocks_stages: [v1_final, v2_lumen, production]
      v1_disposition: implement_in_v1
      v1_treatment: V1按F-KEYENT-03单一紧凑状态行实现并显式记录现状差距
      owner: human:孔东
      deadline: before_v1_round1_review
      return_to: Wireframe
```
