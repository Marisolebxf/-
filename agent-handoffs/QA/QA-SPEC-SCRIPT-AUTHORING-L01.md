# QA-SPEC-SCRIPT-AUTHORING-L01 · 脚本编写规约落地 handoff

> **任务**：QA脚本编写规约落地：试点retro编写侧条款修订（_script.md/schema.md/spec v1.3/X9 expect双层/母表闸门/X5机检）  
> **执行**：agent:qa-agent · **监管**：human:黄敬洲 · **完成**：2026-10-14 12:25  
> **范围边界**：只处理**编写测试脚本**侧条款；执行侧（X1/X6/X7/X10、runner X9 落地）与用例册 C1~C4 不在本单，后续批次处理。

## 1. 范围与实现

来源：脚本重写试点 retro（`qa/as-built/retro/20261013-script-rewrite-pilot.md` §4）编写侧条目，经用户 2026-10-14 逐条拍板后落地：

| 条目 | 落点 | 内容 |
|---|---|---|
| D1/D2 母表闸门 | `as-built/prompts/_script.md` 新增「编号母表闸门」节 | 母表只锁金样 id；落笔前逐行比对用例册「自动化用例ID」回填列，不一致以用例册为准并回告派单方；落盘后四方机检 |
| P1~P6 编写条款 | `_script.md` 新增「编写条款」表 | 实勘优先 / click 后跨 tick 断言 / 评审模式前置关闭 / 弹层 DOM 收场 / 级联父容器回退 / CDP 同步求值 |
| X9 expect 双层 | `_script.md`（格式定义）+ `schema.md`（字段引用） | `{note: 必填人话, assert: Playwright原生表达式, manual?}`；存量 65 条转换完成前允许裸字符串，之后禁止 |
| X2~X4 断言条款 | `schema.md` | 可视性断言（非节点存在）/ 地图瓦片参数代理证据 / 遮挡浮层 DOM 事件优先 |
| X8 viewport | `schema.md`（标准字段）+ 两功能 fixtures | `viewport: {1920×1080, device_scale_factor: 1}` |
| S1/S2 | `qa-test-case-spec.md` **v1.2→v1.3** §8 | allow_skip 边界（被测功能自身行为缺失不适用 skip）+ 跨 tick 时序提示；修订记录补行 |
| X5 机检工具 | `as-built/tools/check-run-consistency.py` 新增 | 四方一致性机检（目录名=case_id=func_id=steps 标题）；tools/README 挂条目 |
| P3/P5 fixtures 补充 | 两功能 `fixtures/testdata.yaml` | 评审模式开关路径、级联分组容器口径 |

## 2. 验收证据

- 机检工具自检：两个 r2 run 实跑通过（`✓ keytype 24 条`、`✓ search 41 条`，退出码 0）
- 提交：`2d8d5835`（规约落地 8 文件）+ `a2b1c243`（registry 合并），均 push origin/dev
- retro §4.5 D1/D2 影响文件列已同步修正（QA 侧闸门，不碰派单手册；用户裁定 2026-10-14）

## 3. 偏离说明

1. `a2b1c243`（registry 冲突合并）混入 4 个工作区既有的他人 QA 文档修正（FUNCLIST 系统码、BLINE Excel 路径、README perf-baseline 行）——stash pop 时已在暂存区，内容无害但与本提交主题无关；如需剥离可 revert 后由责任人重提。
2. `_dispatch.md` 任务书模板未建（用户未选），母表闸门以 `_script.md` 侧拦截先行。

## 4. 遗留与下游

- 执行侧批次：X1（C1 导出断头话术）/ X6/X7（截图必选+异常截图）/ X10（run 级 prompts-used.md 自检）→ `_result.md`/`schema.md`，待用户启动
- X9 存量转换 + 原生 Playwright runner（校准跑 KEYENT 24 条）→ tools/，待用户启动
- 用例册 C1~C4 → 下次用例册修订并入
- retro §4.6 六项缺陷单 → bug-registry，铺开前录入

## 5. 架构合规自检

§2 铁律逐条：仅编排仓文档/工具改动，不涉业务仓、调用链、图谱、CI/CD——1~12 全 N/A ✅；commit 标记 `[agent:qa-agent]` ✅；无 force push ✅。

ponytail: full（规约条款为 DoD 明确要求，无 YAGNI 裁剪；机检工具为最小单文件实现）
