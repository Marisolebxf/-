# UX-SPEC-ENT-COMPARE｜系统级多对象对比篮

> 版本：v1.7 · 2026-08-07
> 状态：ready_for_v1
> 四件套版本：v2.9
> Track：Track-MS
> screen_tier：medium_1440_1920

## 1. 权威输入与边界

### 1.1 权威输入

| 类型 | 文件 / 版本 | 本规格使用方式 |
| --- | --- | --- |
| IA | `IA-ENT-COMPARE.md` v2.9 | 产品角色、系统宿主、五类对象边界、任务分发、四类来源宿主去重、页面职责与禁止行为 |
| TRACE | `TRACE-ENT-COMPARE.yaml` v2.9 | Bid 追溯、批准变更、任务合同、差异项、实现缺口与评审挂载 |
| USM | `USM-ENT-COMPARE.md` v2.9 | 8 个故事、主异常路径与验收语言 |
| Wireframe | `Wireframe-ENT-COMPARE.md` v2.9 | F-CMP-00～11、字段、布局、状态、任务路由与 Drawer 接力规则 |
| 评审治理 | `产品定义评审规程.md` v2.2 | Track-MS 的“核心产品包 → UX/UI → V1 首轮会签 → 门 1 → 联合修订冻结 → V2”顺序 |
| 交互规范 | `UX-UE 通用交互组件规范.md` | Arco 组件、状态反馈、键盘、焦点与无障碍基线 |
| 视觉规范 | `Design.md` | `medium_1440_1920`、24 栅格、浮层、Tabs、控件与三宽验收基线 |
| 数据治理 | `data-lineage-policy.md` | 指标与评审追溯的呈现边界 |

### 1.2 本轮边界

- 本规格只把四件套 v2.9 转为可实现、可评审的交互规则；激活范围以 `ASC-ENT-COMPARE-MULTI-OBJECT-ACTIVATE-20260807`（pending_approval）为准，不新增 Bid 叶子。
- 本规格不修改 Demo / lumen 代码，不推进任务状态，不宣告 PDR 闭合、V1 最终冻结或生产就绪。
- 对比篮是系统 Shell 内的非模态可拖动浮层，不是整页大弹窗；展开时不加全页遮罩，用户仍可感知当前业务页面。
- 已启用企业、产业、政策、服务机构 Tab；区域只提供无数量、无对象、无业务动作的“开发中”页。产业 Tab 标签为「产业」，同 Tab 管理 `industry` 与 `industry_chain`，禁止混选分发。
- 对比篮只暂存和分发基础对象，不生成评分、风险结论、图谱、报告或推荐理由。
- “共 X 项”（已启用类型合计）、各 Tab `X/50`、“已选 X”均为交互状态计数，`metric_id=N/A`；本模块没有统计指标，不新增指标语义卡。
- 旧路由 `/enterprise-center/basket` 仅作为兼容入口，打开系统浮层并落在企业 Tab；企业分析左侧二级菜单不再展示“对比篮”。
- 企业评估和风险洞察的对象区以 `open_compare_basket=1` 原位打开本浮层；空对象区为紧凑状态行，不再以整块 Empty 引导离开页面。
- 从本浮层分发到目标配置页时，有效 `analysis_type` 和 `enterprise_codes[]` 是本次配置草稿权威输入；目标页即使未卸载也必须同步，任务态继续使用任务快照。
- 企业查询 `/development/search` 的推荐、普通结果、`mode=advanced` 高级结果工具栏及完整企业详情页顶部不显示聚合“对比篮 / 查看对比篮”或重复数量；画像快览 Drawer 可保留临时接力动作，但必须先关闭 Drawer 再展开系统浮层。

## 2. 四件套同步核对

### 2.1 故事与 Frame 覆盖

| Story | 交互目标 | Frame | 结论 |
| --- | --- | --- | --- |
| `US-ENT-CMP-01` | 从企业来源收集、去重并保持全局一致 | F-CMP-02 | 完整覆盖 |
| `US-ENT-CMP-02` | 找回并管理本人单篮 | F-CMP-00、02、04、06 | 完整覆盖 |
| `US-ENT-CMP-03` | 选择企业并分发到领域分析 / 评估 / 风险配置 | F-CMP-03、04、05 | 完整覆盖 |
| `US-ENT-CMP-04` | 加入招引 / 培育候选 | F-CMP-03、04 | 完整覆盖 |
| `US-ENT-CMP-05` | 从空篮继续发现企业 | F-CMP-01 | 完整覆盖 |
| `US-ENT-CMP-06` | 与系统任务窗口无冲突地拖动和恢复 | F-CMP-00、06 | 完整覆盖 |
| `US-ENT-CMP-07` | 使用五 Tab 壳层中的企业完整能力 | F-CMP-00～07 | 完整覆盖 |
| `US-ENT-CMP-08` | 识别尚未开放的区域对象 | F-CMP-11 | 完整覆盖 |
| `US-ENT-CMP-09` | 产业 / 产业链入篮与分发 | F-CMP-08 | 完整覆盖（ASC 待签） |
| `US-ENT-CMP-10` | 政策入篮与分发 | F-CMP-09 | 完整覆盖（ASC 待签） |
| `US-ENT-CMP-11` | 服务机构入篮与分发 | F-CMP-10 | 完整覆盖（ASC 待签） |

### 2.2 宿主、状态与禁止行为

| 核对维度 | 同步结论 |
| --- | --- |
| 系统宿主 | `app-shell#system-compare-basket`；登录后的业务页面持续可达 |
| 旧路由 | `/enterprise-center/basket` 只触发展开并默认企业 Tab，不恢复独立页面 IA |
| 默认位置 | 任务入口 `right:24px / top:80px`；对比篮入口 `right:24px / bottom:24px` |
| 共存规则 | 两个收起入口同时可见；同一时刻只允许一个系统面板展开；另一面板自动收起但状态不丢失 |
| 拖动规则 | 收起入口整体和展开标题拖动区可拖动；按钮、Tabs、更多菜单及业务控件不是拖动区 |
| 碰撞规则 | 拖动中临时置顶；结束后夹取视口并保持至少 16px。并发几何变化采用单向避让：任务窗拥有坐标优先权，对比篮监听任务窗出现、移动、展开与收起并重新解析自身位置，避免双向吸附竞态 |
| 五类对象 / Tab | 企业；产业（industry+industry_chain）；政策；服务机构；区域；各 object_type 容量 50 且不共享 |
| 启用状态 | 企业 / 产业 / 政策 / 服务机构存储与业务动作生效；区域不建立存储 |
| 企业操作栏 | 固定底部并保持现有顺序和位置，不移入标题或筛选区 |
| 禁止内容 | 不显示篮内分析结果；不做跨 Tab 混选；不伪造开发中对象；不把任务状态与对比篮合并 |
| 企业查询入口 | 保留逐企业加入状态并即时同步系统角标；不渲染页内常驻聚合按钮、重复数量或第二套管理入口 |

### 2.3 差异与实现缺口

四件套 v2.9 相互一致；业务开放项为 `ASC-ENT-COMPARE-MULTI-OBJECT-ACTIVATE-20260807` 待签字。`GAP-IMPL-01/02/03/06/07/08/09` 是 V1、Demo 或 lumen 的实现对齐项：

- V1 / Demo 应对齐 50 容量、全选三态、系统浮层、五 Tab、企业迁移，以及产业 / 政策 / 服务机构启用与区域占位。
- 正式环境还需闭合用户级持久化 / API 所有权、lumen 返回上下文和 50 家容量，不得用现状反向修改 UX。
- 本规格状态可为 `ready_for_v1`，但 ASC 未签与 lumen 差距仍会阻断后续生产就绪或 V2 会签。

## 3. 用户旅程与任务流

### 3.1 J-CMP-GOV｜政府科技管理与决策人员

**Story**：`US-ENT-CMP-01、02、03、05、06、07`

主路径：

1. 用户在企业查询、重点企业分析、企业总览或企业画像逐项加入企业，系统 Shell 入口角标即时更新且重复加入不增加数量；企业查询页不渲染第二个常驻聚合入口。
2. 用户从任意已登录业务页面展开对比篮；若任务面板已展开，任务面板自动收起为入口。
3. 系统恢复本人企业篮、企业 Tab、筛选、选择和滚动现场；用户搜索、按企业类型筛选并逐项或全选当前可见企业。
4. 用户点击“发起分析”，在上层 Modal 中选择 3 类企业评估或 2 类风险洞察任务。
5. 用户点击“下一步：前往配置”，目标模块成功接管对象与返回上下文后，对比篮面板收起但入口保留；返回后重新展开并恢复原现场。

异常与恢复：

- 第 51 家单个加入失败并说明满额；批量超限只加入剩余容量前 N 家并反馈未加入数量。
- 恢复失败时保留浮层外壳，显示内联错误和“重试”；旧结构可读时继续用旧数据，成功迁移前不删除。
- 已选超过 2 家时“供应链关系分析”保留并禁用，说明“最多选择 2 家企业”；用户关闭 Modal 后缩减选择。
- 目标页返回时对象失效，按有效对象取交集恢复并提示失效数量；不自动清空篮。

退出与恢复：

- 关闭展开面板只收起为入口。
- 取消任务选择只关闭 Modal，焦点回到“发起分析”，篮内容和选择不变。
- 浏览器后退或“返回对比篮”均使用同一 `return_context_id` 恢复。

### 3.2 J-CMP-PARK｜产业园区运营 / 企业服务人员

**Story**：`US-ENT-CMP-01、02、04、06、07`

主路径：

1. 用户汇集园区关注企业，展开对比篮并形成当前选择。
2. 用户点击“加入招引候选”或“加入培育候选”。
3. 系统保持用户所在页面和对比篮展开态，反馈新增数量与重复数量。
4. 用户可从标题区“查看引育名单”进入对应名单；目标路由成功切换后对比篮收起为图标入口，返回或重新展开时仍保留篮内现场。

异常与恢复：

- 未选择企业时两个候选动作禁用，辅助说明“请先选择企业”。
- 无名单写权限时动作保留、禁用并说明权限原因，不静默隐藏。
- 部分对象已在名单中时按幂等写入，反馈“新增 N 家，已存在 M 家”；不将重复视为失败。
- 写入失败时保持原选择并提供重试，不自动跳转。

退出与恢复：

- “取消选择”清除全部选择，包括筛选后不可见的选择，但不移除篮内企业。
- “清空对比篮”必须二次确认；取消确认返回原状态。

### 3.3 J-CMP-INVEST｜投资机构产业研究人员

**Story**：`US-ENT-CMP-01、02、03、06、07、08`

主路径：

1. 用户从检索或画像暂存候选企业，通过系统入口查看企业 `X/50`。
2. 用户拖动入口或面板到不遮挡研究页面的位置，位置按用户保存。
3. 用户选择企业并进入企业评估或风险洞察配置，不在篮内直接读取结论。
4. 用户切换产业 / 政策 / 服务机构 Tab 可管理对象；切换区域 Tab 明确看到“开发中”，再返回企业 Tab。

异常与恢复：

- 拖动与另一系统浮层重叠时自动吸附，保持至少 16px 间距。
- 窗口缩放导致越界时自动夹取；用户也可通过“更多 → 恢复默认位置”恢复当前浮层坐标。
- 区域开发中 Tab 被深链或会话恢复时只显示对应占位，不创建数量、对象或操作。
- 返回企业 Tab 时恢复企业筛选、选择和滚动位置。

## 4. Frame 与承载映射

| Frame | 入口 | 宿主 / 路由 | 核心控件与状态 | 出口、上下文和恢复 |
| --- | --- | --- | --- | --- |
| F-CMP-00 系统收起入口 | 登录后 Shell、面板关闭 | `app-shell#system-compare-basket` | 40px 圆形纯篮图标、右上红色数量角标、Tooltip、拖动区；default / hover / focus / dragging / restricted | 点击展开 F-CMP-06；拖动只改位置；0 隐藏角标、99 以上显示 99+；`aria-label` 宣告完整数量，计数含全部已启用类型 |
| F-CMP-01 空篮启动页 | 企业数量为 0 | 同上，`active_type=enterprise&state=empty` | 来源说明、“去企业查询”；loading / empty / error | 到 `/development/search` 并保留返回来源；不展示推荐 |
| F-CMP-02 有对象未选择 | 恢复或加入后 | 同上，`state=populated` | 名称搜索、企业类型、重置、卡片、移除、清空、画像、底部操作栏 | 列表独立滚动；筛选和滚动写入会话上下文 |
| F-CMP-03 有对象已选择 | 勾选 1～N 家 | 同上，`state=selected` | 全选三态、已选数、取消选择、三个业务动作、任务选择 Modal | 分发到目标模块或写入候选；取消 Modal 返回原焦点 |
| F-CMP-04 受限 / 错误 | 权限、恢复、读取或写入失败 | 当前浮层局部状态 | disabled + 原因、Alert、重试 | 重试成功回原 Frame；无权限不隐藏动作 |
| F-CMP-05 分发后 / 返回 | 目标配置页返回或后退 | 目标路由 + 系统浮层 | 来源提示、已带入对象、返回对比篮 | 用 `return_context_id` 恢复筛选、选择、滚动；失效对象取交集 |
| F-CMP-06 展开壳层共存 | 点击入口、旧路由、拖动或缩放 | `app-shell#system-compare-basket` | 标题拖动区、更多、关闭、五 Tabs；dual-dock / single-expanded / collision-resolved | 打开任务面板时自动收起；不丢业务状态 |
| F-CMP-07 五 Tab / 企业启用 | 展开或旧路由 | `active_type=enterprise` | 企业 `X/50`、产业/政策/服务机构启用 Tabs、区域开发中、完整企业内容 | Tab 切换保存现场；旧数据幂等迁移 |
| F-CMP-08 产业启用 | 点击产业 Tab | `active_type=industry` | 产业+产业链列表、搜索、选择、发起分析 | 禁止混选分发；深链 `industry_chain` 落本 Tab |
| F-CMP-09 政策启用 | 点击政策 Tab | `active_type=policy` | 政策列表、搜索、选择、发起分析 | 同域分发；篮内无结论 |
| F-CMP-10 服务机构启用 | 点击服务机构 Tab | `active_type=service_org` | 服务机构列表、搜索、选择、发起分析 | 同域分发；篮内无结论 |
| F-CMP-11 区域开发中 | 点击区域 Tab | `active_type=region` | 对象类型、未来用途、开发中 Empty | 返回已启用 Tab；无数量、存储和动作 |

跨模块分发参数：

| 字段 | 规则 |
| --- | --- |
| `enterprise_codes[]` | 统一企业标识数组；目标模块自行校验对象和字段 |
| `source` | 固定 `compare-basket` |
| `analysis_type` | `key-enterprise-domain / technology / business / competitiveness / supply-chain / pain-points` |
| `return_context_id` | 会话级往返标识；关联当前 Tab、筛选、选择、滚动和来源页面 |

## 5. 交互与状态转换

### 5.1 系统浮层状态机

| 当前状态 | 触发 | 下一状态 | 可逆 / 保持规则 |
| --- | --- | --- | --- |
| collapsed | 点击对比篮入口 | expanded | 若任务面板展开，先收起任务面板；任务状态保持 |
| expanded | 点击关闭或打开任务面板 | collapsed | 当前 Tab、筛选、选择、滚动保持 |
| expanded | 选择有效任务并成功分发 | collapsed | 先保存当前 Tab、来源路由、筛选、选择和列表滚动；保留系统入口与篮内容，返回时重新展开 |
| expanded | 查看招引 / 培育候选名单并成功跳转 | collapsed | 目标候选工作台接管后收起面板；保留系统入口、篮内容、筛选、选择和列表滚动 |
| collapsed / expanded | 从拖动区按下并超过阈值 | dragging | 未超过阈值仍按点击处理 |
| dragging | 指针释放 | collision-resolved | 先夹取到 Header 下沿 `top ≥ 80px`，再与另一浮层保持至少 16px 并保存用户位置 |
| expanded | 更多 → 恢复默认位置 | expanded | 只重置当前浮层坐标；默认位置时菜单项 disabled |
| any visible | 首次挂载、旧坐标恢复、任务窗几何更新或 viewport resize | viewport-clamped | 统一执行 `top ≥ 80px` 与 16px 碰撞避让；任务窗保留坐标、对比篮重新让位，当前活动面板优先，两个入口始终可访问 |

拖动把手必须使用明确的可拖动光标和命中区。交互控件调用 `stopPropagation` 或等效机制，避免点击 Tabs、按钮、菜单、输入框时启动拖动。拖动开始后临时提升当前表面层级，结束后回到共享层级协议。

### 5.2 企业筛选、选择与管理

| 控件 / 触发 | 前置状态 | 结果 | 禁止行为 |
| --- | --- | --- | --- |
| 企业名称搜索 | 企业有对象 | 过滤当前篮；不改变已选集合 | 不搜索统一社会信用代码或全库 |
| 企业类型 | 企业有对象 | 与名称条件取交集 | 不新增地区、产业、风险等复杂筛选 |
| 重置 | 任意筛选 | 只恢复名称和类型默认值 | 不取消选择、不清空篮 |
| 单项勾选 | 对象可用 | 合并 / 移出选择集合 | 不影响其他 Tab |
| 全选当前筛选结果 | 当前可见集合非空 | 将全部可见对象并入既有选择 | 不清除隐藏选择，不选择全库 |
| 取消全选 | 当前可见对象有选择 | 只移出当前可见对象 | 不等同“取消选择” |
| 取消选择 | 已选数大于 0 | 清除全部已选对象 | 不移除篮内对象 |
| 单个移除 | 对象存在 | 立即移除并反馈，可提供短时撤销 | 不弹二次确认 |
| 清空篮 | 企业有对象 | 二次确认后清空，进入 F-CMP-01 | 不与取消选择混用 |

全选复选框三态只按当前可见集合计算：

- 未选：可见对象均未选。
- 半选：可见对象部分已选。
- 全选：可见对象全部已选。
- 当前筛选无结果：disabled；隐藏选择仍计入“已选 X 家”。

### 5.3 底部固定操作栏

布局原位迁移，顺序固定为：

`全选当前筛选结果 → 已选 X 家 → 取消选择 → 分隔线 → 发起分析 → 加入招引候选 → 加入培育候选`

- 标题、筛选区和底部操作栏固定；只有中间企业列表纵向滚动。
- 未选择企业时，“取消选择”和三个业务动作禁用并说明“请先选择企业”。
- “发起分析”为唯一主按钮；两个候选动作为次按钮。
- 不能把全选移入筛选栏、把已选数移入标题区、删除分隔线或改变三个动作的相对顺序。

### 5.3A 企业查询来源页入口去重

| 触点 | 交互结果 | 反馈 | 禁止行为 |
| --- | --- | --- | --- |
| 企业卡片 / 行内“加入对比篮” | 按企业唯一键写入或合并来源；按钮切换为“已加入” | 轻量提示“已加入对比篮”，系统 Shell 红色角标即时增加 | 不创建页内常驻聚合入口，不跳转旧篮页面 |
| 企业卡片 / 行内“已加入” | 保持已加入状态；如既有契约支持移除，则移除后回到“加入对比篮” | 系统 Shell 红色角标即时同步 | 不显示第二套聚合数量 |
| 瞬时反馈中的“查看对比篮” | 原位展开 `app-shell#system-compare-basket` | 反馈关闭后只保留系统入口 | 不渲染永久按钮，不导航 `/enterprise-center/basket` 独立页 |
| 推荐结果工具栏 | 不渲染页内“对比篮”按钮及 Badge | 使用系统 Shell 图标 | 不因视觉空位恢复同义入口或文本数量 |
| 普通查询结果工具栏 | 不渲染页内“对比篮”按钮及 Badge | 使用系统 Shell 图标 | 不保留结果级聚合入口 |
| `mode=advanced` 高级筛选结果工具栏 | 不渲染页内“对比篮”按钮及 Badge | 使用系统 Shell 图标 | 不因查询模式变化恢复旧入口 |
| 完整企业详情页顶部 | 移除“查看对比篮”，保留“加入 / 已加入”和其他对象级动作 | 使用系统 Shell 图标 | 不把详情页动作区作为聚合管理入口 |
| 企业画像快览 Drawer 底部 | 可保留临时“查看对比篮”；点击即锁定重复提交，先触发 Drawer 关闭，等待退出完成后再展开系统浮层 | 焦点进入浮层标题或首个可操作项；关闭浮层后回到触发该 Drawer 的“查看画像” | 不在 Drawer 未关闭时展开，不与遮罩叠加，不把篮嵌入 Drawer |

系统入口的可发现性由 Shell 图标、Tooltip / 无障碍名称和红色角标承担；来源页只承担对象发现与逐项采集。Drawer 临时动作属于阻塞容器内的表面接力，不是第二个常驻系统入口。该调整不新增 Frame，也不改变企业查询的信息架构或企业卡片位置。

### 5.4 分析任务选择

1. 点击“发起分析”打开 Arco `Modal` 或等价共享容器，Modal 位于系统浮层之上并阻止指针穿透。
2. 标题为“选择分析任务”；其下、任务分组前固定显示“已选择 X 家企业”。
3. 重点企业分析分组提供领域分布分析；企业评估分组提供技术力、商业力、综合竞争力；风险洞察分组提供供应链关系、发展痛难点。
4. 从通用系统入口或独立对比篮页打开时默认不预选任务；从已明确分析类型的目标页原位打开时，按来源上下文预选对应任务（领域分布分析页对应 `key-enterprise-domain`）。预选只更新单选态，不自动跳转。
5. 未选任务时“下一步：前往配置”禁用。
6. 超过 2 家时供应链关系分析保留、禁用并说明数量限制；不自动截取前两家。
7. 点击下一步才创建分发上下文并跳转；目标路由成功接管后收起对比篮面板但保留系统入口，篮内不执行模型、指标或权限之外的业务校验。
8. 取消、关闭、Esc、权限不足、数量校验失败或跳转失败后焦点回“发起分析”，对比篮继续展开。

目标路由：

| 任务 | 路由 |
| --- | --- |
| 领域分布分析 | `/enterprise-center/key-enterprise-analysis?view=domain` |
| 技术力评估 | `/enterprise-center/evaluation?tab=capability&capabilityType=tech` |
| 商业力评估 | `/enterprise-center/evaluation?tab=capability&capabilityType=business` |
| 综合竞争力评估 | `/enterprise-center/evaluation?tab=competitiveness` |
| 供应链关系分析 | `/enterprise-center/risk?tab=supply-chain` |
| 发展痛难点分析 | `/enterprise-center/risk?tab=pain-points` |

### 5.5 五 Tab 与启用 / 开发中状态

- Tabs 使用对象类型命名，企业为默认项；旧路由也默认企业。五个 Tab 在 1920 / 1680 / 1440 均完整横向单行显示。
- 企业 / 产业 / 政策 / 服务机构显示 `X/50`（产业为双对象合计口径）；区域开发中 Tab 只显示名称与“开发中”，不显示 `0/50`。
- 区域开发中内容只显示对象类型、未来用途与暂未开放说明。
- 切换 Tab 不重置企业筛选、选择或滚动。
- 禁止跨 Tab 选择、联合分析、Mock 对象、占位类型存储和来源模块加入入口。

## 6. 反馈与异常恢复

| 场景 | 反馈方式 | 恢复动作 |
| --- | --- | --- |
| 初次恢复企业篮 | 列表区域 Skeleton；标题、Tabs、关闭与两个系统入口保持稳定 | 成功进入 F-CMP-01/02；失败显示局部 Alert + 重试 |
| 单个重复加入 | 轻量 Message“已在对比篮中” | 保持现状并允许打开对比篮 |
| 第 51 家加入 | Error Message“对比篮已满，请移除部分企业后再加入” | 打开篮移除企业后重试 |
| 批量超限 | Success/Warning Message“已加入 N 家，M 家因容量未加入” | 查看篮或调整来源选择 |
| 当前筛选无结果 | 列表 Empty；保留筛选区和固定操作栏 | 重置或调整筛选；全选 disabled |
| 移除单项 | Success Message，可提供短时“撤销” | 撤销后恢复对象及原排序位置 |
| 清空篮 | Modal 二次确认 | 取消保持原状；确认后进入空篮 |
| 无分析 / 名单权限 | 控件保留 disabled，Tooltip 或邻近说明原因 | 申请权限或改选可用任务 |
| 候选写入部分重复 | Message“新增 N 家，已存在 M 家” | 保持选择，可继续其他动作 |
| 候选写入失败 | 局部错误或 Message，不清除选择 | 重试 |
| 旧数据迁移失败 | Alert 说明继续读取旧篮 | 重试迁移；成功写入前不删除旧数据 |
| 返回对象部分失效 | Warning“X 家企业已失效，已恢复其余对象” | 查看有效集合或重新添加 |
| 保存位置失败 | 非阻断 Message；本次位置仍生效 | 下次拖动重试，或恢复默认位置 |
| 窗口缩放越界 | 无打断夹取；必要时用轻量提示说明位置已调整 | 更多 → 恢复默认位置 |
| 区域开发中 Tab | 稳定 Empty，说明用途和“开发中” | 返回已启用 Tab |
| 企业查询加入企业 | 轻量 Message“已加入对比篮”；系统 Shell 红色角标即时更新 | 继续浏览，或通过系统入口 / 瞬时“查看对比篮”原位展开浮层 |

错误不能只使用红色边框表达；动态成功、警告和错误消息使用文本并由 `aria-live` 宣告。loading、empty、error、permission 均保持浮层尺寸和标题区稳定，避免入口跳动。

## 7. 组件、键盘与无障碍

### 7.1 组件映射

| 交互 | 推荐组件 | 关键约束 |
| --- | --- | --- |
| 系统收起入口 / 展开面板 | 定制 `SystemFloatingSurface` + Arco `Button / Badge / Tooltip / Dropdown` 语义 | 收起态纯图标、红色数量角标与完整无障碍名称；共享位置、互斥展开、碰撞与持久化协调器 |
| 五对象 Tabs | Arco `Tabs` 语义 + GKX 一级 Tab 样式 | 支持方向键切换、active 状态和开发中标签 |
| 名称搜索 / 类型筛选 | `Input.Search` / `Select` | 有可见 label 或 `aria-label` |
| 全选与单项选择 | `Checkbox` | 支持 checked / indeterminate / disabled |
| 企业列表 | 语义列表 + Card/Row | 列表为唯一业务滚动区 |
| 更多 / 恢复位置 | `Dropdown` + MenuItem | 默认位置时 disabled；触发器有 `aria-haspopup` |
| 清空确认 / 任务选择 | `Modal` | 焦点陷阱、Esc、关闭后焦点回触发器 |
| 企业画像 | 共享详情 `Drawer` 或现有详情路由 | 关闭后回到“查看画像” |
| 状态反馈 | `Skeleton` / `Empty` / `Alert` / `Message` / `Tooltip` | 不私造基础反馈组件 |

### 7.2 键盘与焦点

- `Tab / Shift+Tab` 按视觉顺序遍历：系统入口 → 标题操作 → Tabs → 筛选 → 列表选择 / 行操作 → 底部操作栏。
- `Enter / Space` 激活入口、按钮、复选框和菜单项；Tabs 支持左右方向键、Home、End。
- `Esc` 先关闭最上层 Modal / Dropdown / Drawer，再收起对比篮；关闭层级后焦点返回各自触发器。
- 拖动不是完成任务的唯一方式；键盘用户可使用“更多 → 恢复默认位置”，且所有业务操作不依赖拖动。
- 展开时初始焦点进入标题或第一个可操作项；不强制锁住非模态面板中的焦点。Modal / Drawer 按规范建立焦点陷阱。
- 拖动结束不改变当前焦点；窗口夹取不抢焦点。

### 7.3 ARIA 与可感知性

- 系统入口使用可读名称“打开对比篮，共 X 项”，展开态使用 `aria-expanded=true` 并关联面板。
- 展开面板使用具名区域语义，例如 `role=region`、`aria-label=对比篮`；非模态面板不得误标 `aria-modal=true`。
- 拖动把手提供名称“拖动对比篮”，并在帮助文本说明可通过更多菜单恢复位置。
- Tabs 使用 `tablist / tab / tabpanel` 关系；开发中是业务状态文本，不仅依靠颜色。
- Checkbox 暴露 `aria-checked=true/false/mixed`；disabled 控件同时给出可访问原因。
- 动态计数、迁移结果、写入结果和失效对象使用礼貌级 `aria-live`。
- focus-visible 使用 GKX 主蓝焦点环；文字、图标和控件对比度满足现行中屏规范，禁用原因不能只靠灰度。
- 最小指针命中区保持可操作，关闭、更多和拖动区域相互分离。

## 8. 响应式行为

本模块仅支持科技专题服务系统 `medium_1440_1920`，不定义 `<1440px` 移动端，也不继承 `>1920px` Track-L。

| 宽度 | Shell 与导航 | 浮层 | 企业内容 | 底部操作栏 |
| --- | --- | --- | --- | --- |
| 1920 | 保持用户导航选择，24 栅格 / 16px gutter | 基准宽 760px，按 `min(760px, calc(100vw - 32px))` 夹取；最大高 `calc(100vh - 96px)` | 五 Tabs 完整单行；筛选同排；列表独立滚动 | 保持现有顺序，可单行 |
| 1680 | 保持用户导航选择或按 Shell 规则 | 同一 760px 策略，确保与任务入口和视口边缘 16px 安全间距 | 五 Tabs 完整单行；筛选可换行 | 空间不足时在操作栏内部换行，不换序 |
| 1440 | 左侧导航默认收起至 64px | 同一 760px 策略；用户保存位置越界时夹取 | 五 Tabs 完整单行；搜索与类型可纵向或两行排列 | 分组换行，选择摘要与业务动作仍在底部固定区 |

共同规则：

- Tabs 不折行、不截断，也不使用水平滚动隐藏；筛选区和底部操作栏可按既定顺序换行。
- 不把浮层扩展成整页 Modal；不遮罩页面；浮层宽高不超过安全视口。
- 标题、Tabs、筛选和底部操作栏固定，中部列表使用 `min-height:0` 和内部纵向滚动。
- 短列表不把操作栏上推；长列表不增长页面主体。
- 两个系统入口在三种宽度下都可访问；当前活动面板优先，碰撞后保持至少 16px 间距。
- 三宽都需验证 default、empty、populated、selected、task-picker、permission、error、dual-dock、developing 状态。

## 9. 内部评审投影

内部评审模式只增加追溯说明，不改变业务数据、选择集合、动作结果或布局。业务模式下以下挂载必须完全 absent，不能只用 CSS 隐藏；“全选当前筛选结果”是纯业务交互，`review_mounts: []`。

| mount_id | Frame | 评审态内容 | 业务模式 |
| --- | --- | --- | --- |
| `ENT-COMPARE-F06-SCOPE-CHANGE-TRACE` | F-CMP-06 | 系统浮层范围变更：移除左侧入口、可拖动、双浮层协调与位置恢复 | absent |
| `ENT-COMPARE-F07-MULTI-OBJECT-SCOPE-TRACE` | F-CMP-07 | 五类对象、独立容量及 v2.9 启用边界说明 | absent |
| `ENT-COMPARE-F08-INDUSTRY-ACTIVE-TRACE` | F-CMP-08 | 产业 Tab 双对象规则与分发边界追溯 | absent |
| `ENT-COMPARE-F09-POLICY-ACTIVE-TRACE` | F-CMP-09 | 政策 Tab 启用与分发边界追溯 | absent |
| `ENT-COMPARE-F10-SERVICE-ACTIVE-TRACE` | F-CMP-10 | 服务机构 Tab 启用与分发边界追溯 | absent |
| `ENT-COMPARE-F11-REGION-DEVELOPING-TRACE` | F-CMP-11 | 行政区域未来用途与占位追溯 | absent |

评审挂载规则：

- 每个挂载 ID 只用于表中唯一 Frame，不复用、不生成新的挂载 ID。
- F-CMP-00～05 没有批准挂载，不出现评审标记。
- 业务 / 评审模式共用相同篮内容、Tab、筛选、选择、滚动和用户位置。
- 评审态提示使用局部 `i` / Popover 或占位页局部说明，不使用常驻大面积蓝底条。

## 10. Demo 实施交接

### 10.1 页面包与共享候选

| 层 | 建议职责 |
| --- | --- |
| `SystemFloatingSurfaceCoordinator` | 注册任务 / 对比篮表面，管理展开互斥、临时层级、16px 避让、夹取与按用户持久化 |
| `SystemCompareBasket` | 系统入口、展开壳层、五 Tabs、标题操作与业务 / 评审模式切换 |
| `EnterpriseBasketPanel` | 企业空态、筛选、列表、选择、清空、候选与返回恢复 |
| `EnterpriseBasketActionBar` | 原位迁移固定操作栏，维持既有顺序、三态全选和 disabled 原因 |
| `AnalysisTaskPicker` | 任务选择 Modal、“已选择 X 家企业”、1+3+2 任务和下一步 |
| `DevelopingObjectTab` | 四类占位的共享结构，仅替换对象名和未来用途 |
| `CompareBasketMigrationAdapter` | 旧企业篮幂等迁移与失败回退 |
| `CompareBasketReturnContext` | 保存 / 恢复 Tab、筛选、选择、滚动与来源页面 |

### 10.2 建议状态模型

- `surface`: `collapsed | expanded | dragging`
- `active_type`: `enterprise | industry | policy | service_org | region`（深链可带 `industry_chain` 并映射产业 Tab）
- `enterprise`: `loading | empty | populated | error | restricted`
- `filters`: `{ enterprise_name, enterprise_type }`
- `selected_enterprise_codes`: `Set<string>`
- `analysis_picker`: `{ open, selected_task }`
- `positions`: `{ compare_basket, analysis_jobs }`
- `migration`: `idle | running | success | fallback | error`
- `return_context`: `{ id, active_type, filters, selected_codes, scroll_top, source_route }`
- `review_mode`: `off | on`，只控制批准挂载的渲染。

### 10.3 V1 验证重点

- 1920 / 1680 / 1440 三宽截图与真实指针拖动；验证碰撞、视口夹取、临时置顶和位置恢复。
- 两入口同时可见、单面板展开，自动收起不丢任务或篮状态。
- 50 家容量、重复加入、批量超限和旧数据幂等迁移 / 回退。
- 名称 + 企业类型筛选；全选未选 / 半选 / 全选 / 空结果；隐藏选择保留与取消选择清空全部。
- 底部操作栏位置、顺序、固定和窄宽换行；任务 Modal 中“已选择 X 家企业”的位置。
- 1+3+2 分析任务、领域分析 1～50 家、供应链 1～2 家限制、权限禁用原因、目标路由与返回上下文。
- 候选新增 / 重复 / 失败反馈且不自动跳转。
- 区域开发中 Tab 无数量、存储、对象和动作；已启用 Tab 切换后现场不丢。
- 键盘、焦点、ARIA、对比度以及业务模式无评审节点。

### 10.4 明确排除

- 不在本 UX 文档中实现或修改 React / Vue 代码。
- 不接入区域真实对象；产业 / 政策 / 服务机构按 v2.9 启用（ASC 待签）。
- 不新增企业高级筛选、来源筛选、统一社会信用代码搜索。
- 不在篮内生成分析结果或支持跨类型联合分析。
- 不改变系统任务窗口的业务内容，只复用共享浮层协调能力。
- 不把旧路由保留为左侧菜单入口或独立页面。
- 不在推荐、普通、高级结果工具栏或完整企业详情页顶部恢复常驻“对比篮 / 查看对比篮”、重复数量角标或第二套管理入口；画像快览 Drawer 不得与系统浮层同时呈现。

## 11. 缺口与阻断项

阻断项：无。

说明：

- 四件套 v2.8 已关闭 UX 启动所需的范围、角色、Frame、路由、状态、任务分发、共存及四类企业查询宿主去重 / 接力决策，本规格可进入 V1 高保真首轮制作。
- `GAP-IMPL-01/02/03/06/07/08/09` 仍需由后续实现任务闭合；其中正式用户持久化 / API 所有权、lumen 对齐、系统共享协调器和企业查询重复入口会继续阻断生产或 V2，但不阻断按批准规格制作 V1。
- 若实现发现共享协调器无法同时满足“两个入口可见、只展开一个面板、16px 避让、按用户持久化”，应返回 TRACE / 架构评审，不得通过永久提高 `z-index` 或隐藏另一入口绕过。

## 12. 机器可读交付契约

```yaml
ux_spec_contract:
  module_key: ENT-COMPARE
  version: "1.6"
  status: ready_for_v1
  source_four_pack:
    - IA-ENT-COMPARE.md
    - TRACE-ENT-COMPARE.yaml
    - USM-ENT-COMPARE.md
    - Wireframe-ENT-COMPARE.md
  screen_tier: medium_1440_1920
  delivery_stage: v1_hifi_round1
  product_scope_mutation: prohibited
  demo_code_mutation: prohibited
  journeys:
    - journey_id: J-CMP-GOV
      role: 政府科技管理与决策人员
      story_refs: [US-ENT-CMP-01, US-ENT-CMP-02, US-ENT-CMP-03, US-ENT-CMP-05, US-ENT-CMP-06, US-ENT-CMP-07]
      primary_flow: [从企业来源加入, 展开并恢复企业篮, 筛选与选择企业, 选择分析任务, 成功分发后收起面板, 返回并重新展开恢复]
      abnormal_flows: [容量超限, 恢复失败, 供应链数量受限, 返回对象失效]
    - journey_id: J-CMP-PARK
      role: 产业园区运营或企业服务人员
      story_refs: [US-ENT-CMP-01, US-ENT-CMP-02, US-ENT-CMP-04, US-ENT-CMP-06, US-ENT-CMP-07]
      primary_flow: [汇集园区关注企业, 形成当前选择, 加入招引或培育候选, 查看结果反馈]
      abnormal_flows: [未选择对象, 名单写权限不足, 候选重复, 写入失败]
    - journey_id: J-CMP-INVEST
      role: 投资机构产业研究人员
      story_refs: [US-ENT-CMP-01, US-ENT-CMP-02, US-ENT-CMP-03, US-ENT-CMP-06, US-ENT-CMP-07, US-ENT-CMP-08]
      primary_flow: [暂存候选企业, 拖动浮层避让页面, 分发到分析配置, 查看开发中对象类型]
      abnormal_flows: [浮层碰撞, 窗口缩放越界, 开发中深链恢复]
  frame_specs:
    - frame_id: F-CMP-00
      route_or_host: app-shell#system-compare-basket
      source_refs: [US-ENT-CMP-02, US-ENT-CMP-06, US-ENT-CMP-07]
      states: [default, hover, focus, dragging, restricted]
      interactions: [点击展开, 拖动入口, 展示企业总数]
    - frame_id: F-CMP-01
      route_or_host: app-shell#system-compare-basket?active_type=enterprise&state=empty
      source_refs: [US-ENT-CMP-05, US-ENT-CMP-07]
      states: [loading, empty, error]
      interactions: [去企业查询, 关闭面板, 恢复默认位置]
    - frame_id: F-CMP-02
      route_or_host: app-shell#system-compare-basket?active_type=enterprise&state=populated
      source_refs: [US-ENT-CMP-01, US-ENT-CMP-02, US-ENT-CMP-07]
      states: [loading, populated, filtered, no_results, error]
      interactions: [搜索企业名称, 筛选企业类型, 重置, 选择, 移除, 清空, 查看画像, 列表滚动]
    - frame_id: F-CMP-03
      route_or_host: app-shell#system-compare-basket?active_type=enterprise&state=selected
      source_refs: [US-ENT-CMP-03, US-ENT-CMP-04]
      states: [selected, indeterminate, task_picker, restricted, submitting]
      interactions: [全选当前筛选结果, 取消选择, 发起分析, 加入招引候选, 加入培育候选]
    - frame_id: F-CMP-04
      route_or_host: app-shell#system-compare-basket?state=restricted_or_error
      source_refs: [US-ENT-CMP-02, US-ENT-CMP-03, US-ENT-CMP-04]
      states: [permission, migration_error, read_error, write_error]
      interactions: [查看禁用原因, 重试, 返回可用状态]
    - frame_id: F-CMP-05
      route_or_host: target-analysis-route+app-shell#system-compare-basket
      source_refs: [US-ENT-CMP-03]
      states: [dispatched, returning, partially_invalid, restored]
      interactions: [返回对比篮, 浏览器后退, 恢复往返上下文]
    - frame_id: F-CMP-06
      route_or_host: app-shell#system-compare-basket
      source_refs: [US-ENT-CMP-02, US-ENT-CMP-05, US-ENT-CMP-06, US-ENT-CMP-07]
      states: [dual_dock, single_expanded, dragging, collision_resolved, viewport_clamped]
      interactions: [展开互斥, 拖动面板, 碰撞吸附, 关闭, 恢复默认位置]
    - frame_id: F-CMP-07
      route_or_host: app-shell#system-compare-basket?active_type=enterprise
      source_refs: [US-ENT-CMP-07]
      states: [loading, empty, populated, selected, migration_fallback]
      interactions: [切换对象Tab, 使用企业完整能力, 兼容旧路由]
    - frame_id: F-CMP-08
      route_or_host: app-shell#system-compare-basket?active_type=industry
      source_refs: [US-ENT-CMP-08]
      states: [developing, review_projection]
      interactions: [搜索产业或产业链, 选择同类型对象, 发起分析, 禁止混选分发]
    - frame_id: F-CMP-09
      route_or_host: app-shell#system-compare-basket?active_type=policy
      source_refs: [US-ENT-CMP-08]
      states: [developing, review_projection]
      interactions: [查看政策未来用途, 返回企业Tab]
    - frame_id: F-CMP-10
      route_or_host: app-shell#system-compare-basket?active_type=service_org
      source_refs: [US-ENT-CMP-08]
      states: [developing, review_projection]
      interactions: [查看服务机构未来用途, 返回企业Tab]
    - frame_id: F-CMP-11
      route_or_host: app-shell#system-compare-basket?active_type=region
      source_refs: [US-ENT-CMP-08]
      states: [developing, review_projection]
      interactions: [查看区域未来用途, 返回企业Tab]
  feedback_rules:
    - trigger: 企业查询逐项加入或移除
      response: 同步逐企业加入状态与系统Shell红色数量角标
      recovery: 通过系统入口或瞬时查看动作原位展开浮层
    - trigger: 恢复企业篮
      response: 列表区域Skeleton或局部错误
      recovery: 重试并在迁移失败时继续读取旧结构
    - trigger: 加入超限
      response: 阻止第51家或反馈批量未加入数量
      recovery: 移除对象后重试
    - trigger: 权限或数量条件不满足
      response: 保留控件并禁用且说明原因
      recovery: 调整选择或申请权限
    - trigger: 候选写入
      response: 反馈新增数和重复数或写入错误
      recovery: 保持选择并允许重试
    - trigger: 返回时对象失效
      response: 按有效对象取交集并提示失效数量
      recovery: 查看有效集合或重新添加
    - trigger: 浮层碰撞或越界
      response: 夹取并吸附到最近安全位置
      recovery: 从更多菜单恢复默认位置
  responsive_widths: [1920, 1680, 1440]
  accessibility_checks: [keyboard, focus, aria, contrast]
  source_page_rules:
    enterprise_search:
      route: /development/search
      route_variants: [recommended, standard_results, advanced_results, full_enterprise_detail, portrait_preview_drawer]
      retained_actions: [加入对比篮, 已加入]
      sole_aggregate_entry: app-shell#system-compare-basket
      remove_aggregate_entry_from: [推荐结果工具栏, 普通查询结果工具栏, 高级筛选结果工具栏, 完整企业详情页顶部]
      drawer_handoff:
        host: 企业画像快览Drawer底部
        action: 查看对比篮
        sequence: [锁定重复提交, 关闭Drawer, 等待退出完成, 按安全位置展开系统浮层, 焦点进入浮层]
        simultaneous_surfaces: prohibited
      prohibited_persistent_elements: [页内对比篮按钮, 页内聚合数量角标, 第二套管理入口]
  review_mounts:
    - ENT-COMPARE-F06-SCOPE-CHANGE-TRACE
    - ENT-COMPARE-F07-MULTI-OBJECT-SCOPE-TRACE
    - ENT-COMPARE-F08-INDUSTRY-ACTIVE-TRACE
    - ENT-COMPARE-F09-POLICY-ACTIVE-TRACE
    - ENT-COMPARE-F10-SERVICE-ACTIVE-TRACE
    - ENT-COMPARE-F11-REGION-DEVELOPING-TRACE
  gaps: []
  blockers: []
```
