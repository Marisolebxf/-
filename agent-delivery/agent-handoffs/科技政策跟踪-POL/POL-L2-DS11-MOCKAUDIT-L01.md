# POL-L2-DS11-MOCKAUDIT-L01 · 政策分析评价 真实/mock 全量盘点 + 评审模式来源标注

- 任务：`POL-L2-DS11-MOCKAUDIT-L01`（audit + feature，P1，2 点）
- 仓：`lumen-ui-science-pc`（角标/评审层改造）+ `gkx-orchestration`（盘点表落盘）
- 执行：`agent:frontend-agent`；监管：`human:淮政玮`
- 状态：**backlog**（2026-11-11 用户指示新建，待认领派单）
- 上游：`POL-L2-DS11-PLAN-WIRING-L01`（done，227–231 已接真轨）；VIZ/READ 两侧接线单（`POL-L2-DS11-VIZ-WIRING-L01` / `POL-L2-DS11-READ-WIRING-L01`，ready）未完成的叶按分册设计稿盘点并如实标「接线未完成」
- 关联背景：`POL-MOCK-BTN-B03-FIX01`（评价按钮与种子批双源冲突，熔断中）——本单盘点不触发任何重灌

## 一、任务目标（用户原话拆解）

> 针对「政策分析评价」，梳理清楚哪些是真实现，哪些是 mock 或包含 mock（**mock 仅允许通过 gapfill 数据库的方式**），在内部评审模式上要体现。

1. **梳理**：DS-11 政策分析评价三个二级、序号 219–231 全量 13 叶 + 页面块级清单，逐项判定真实/mock/混合，写明数据出处。
2. **合规口径**：mock 的唯一合规形态 = 读 `gkxlumenx_gapfill.gapfill_policy_eval_*` 缺项表（`is_mock=1`）。任何「接口写死返回」「前端 fixture 造数」「代码内嵌假数据」都是违规项，登记并挂修复子单，本单不顺手改。
3. **评审模式体现**：`?review=1`（或 localStorage `lumen-review-mode`）开启时，页面上每块都能看出它属于哪一层；关闭时 DOM 零泄漏（沿用 `src/review/` 既有机制，`MockBadge` reason 统一口径）。

## 二、盘点范围与判定口径

### 范围（DS-11 三二级 × 序号 × 页面块）

| 二级 | 序号 | 页面（lumen-ui-science-pc） |
|---|---|---|
| VIZ 政策分析报告可视化呈现 | 219 多维指标趋势图 / 220 分区群体对比 / 221 多维结构关联 / 222 报告模板定制导出 | 政策分析评价 · 报告可视化 Tab（趋势/分区/关联图/模板卡） |
| READ 结果解读报告多维展示 | 223 热点问题看板 / 224 分主题互动解读 / 225 多媒体辅助解读 / 226 智能摘要推送 | 政策分析评价 · 结果解读 Tab（看板/解读/多媒体/摘要推送块） |
| PLAN 推荐方案报告交互展示 | 227 方案对照 / 228 参数模拟 / 229 路径风险 / 230 互动意见 / 231 方案报告导出 | 政策分析评价 · 推荐方案 Tab（对比卡/方案卡/模拟卡/路径卡/意见卡/导出弹窗） |

页面块级盘点还须覆盖不属于 219–231 序号但同页存在的演示交互（闸门 Switch、分享/汇报/流转提示、综合报告导出等），判定为 C 类并标注，防混淆。

### 判定口径（三层，唯一允许的 mock = B）

| 层 | 定义 | 出处示例（以分册为准，盘点时逐叶核实） |
|---|---|---|
| **A 真·读面** | 数据来自真实库表读面（ADS/DWD 等），非缺项表 | 223 短板条数（`demo_gkxlumenx_ads.policy_effect` region_gap）、226 摘要（`demo_gkxlumenx_ads.policy_text_parse.summary`）——具体以 `POL-L2-DS11-READ-API/METRIC` 分册判定为准 |
| **B gapfill mock（唯一合规 mock）** | 读 `gkxlumenx_gapfill.gapfill_policy_eval_*`（`is_mock=1`），有行即写可演，无行则空 | 219/220（`gapfill_policy_eval_trend/partition`）、222（`…_template`）、224/225（`…_shell`）、227–230（`…_scheme`）、231（同 227/230 行拼装，不产文件） |
| **C 前端演示态（非数据 mock）** | 不落库、不进请求的页面行为；契约内的「从当次行生成」不算 mock | 闸门演示 Switch、分享/汇报/流转 toast、页面新意见只留浏览器（230 契约内）、导出弹窗格式选择 |

注意：**D4=mock、`metric_id` 挂 mock 指标**是 B 类的属性而非违规；违规专指「绕过 gapfill 表的数据伪造通道」（接口写死、前端 fixture、种子直返拦截器等）。

## 三、产出

1. **盘点表**：落盘 `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-MOCKAUDIT-L01-盘点表.md`，两张表：
   - 逐叶表：219–231 每行 = 判定层（A/B/C/混合）+ 数据出处（库.表 / 接口路径 / 前端行为）+ 现有角标状态 + 缺口（接线未完成/角标缺失/reason 口径不符）；
   - 块级表：分析页三个 Tab 每个卡/图/按钮一行（含非序号块的 C 类标注）。
2. **评审模式标注改造**（`lumen-ui-science-pc`）：
   - `MockBadge` reason 统一口径：B → `gapfill 缺项表 mock（出处 库.表）`；C → `前端演示态（不落库）`；A → 不挂 mock 角标（真实现不需要 apology badge；若需可挂 ⓘ 说明行，新组件进 `src/review/`）；
   - 同块混合（如卡内既有 B 数据又有 C 按钮）：块级角标注 B，C 部分在控件旁单独小标；
   - 关闭评审模式 DOM 零泄漏：`class="mock-badge"` 检索计数保持既有自检通过。
3. **自检**：扩展 `FE-POL-02A.test.mjs`（或新增 `FE-POL-02C` 段），断言：219–231 每叶对应块的角标存在且 reason 含「gapfill」或「演示态」字样；无「无角标的 B 类块」残留。
4. **违规清单**（如有）：盘点表末节单列，每项挂独立修复单号（格式 `POL-L2-DS11-MOCKAUDIT-FIX-xx`），本单只登记不修。

## 四、DoD

1. 盘点表覆盖 13 叶 + 块级清单，每行有判定与出处，无「未判」行；
2. 评审模式开启：政策分析评价页每块可见来源标注；关闭：零泄漏（自检绿）；
3. 违规清单单列且各挂修复单号（无违规则写「核查无」）；
4. 本单状态回填 + 盘点表随 handoff 一起提交 `gkx-orchestration`（带 `[agent:frontend-agent]`）。

## 五、约束

- 不改后端（display/element/algo 均不动）；不新增任何 mock 通道；不触发评价按钮重灌（见 B03-FIX01）。
- 诚实性：不把 C 类粉饰成数据 mock，也不把 B 类写成真实现；「接线未完成」的叶如实标注，不脑补实现状态。
- token/口令不进 git；连库核对只读。

## 六、记录

（执行时回填：判定过程、连库核对时间、自检输出）
