# ZMATE-RPT-FE-DEMO-L01 · 按签收稿重做 demo-ui-topic 战略报告原型

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 任务已 in_progress；本叶按签收 WF/UI-HIFI/ARCH 废稿重做 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 D8 Design / 可观测 track / 人闸与分站契约 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶纯前端 Demo 重写，未挂载 headroom |

## 范围与实现

对照签收：

- `Wireframe-ZMATE-战略报告创作.md`
- `UI-HIFI-ZMATE-战略报告创作.md`
- `ARCH-ZMATE-战略报告创作.md`
- `USM-ZMATE-战略报告创作.md` 验收句 ZMATE-USM-01～13

**仓**：仅 `demo-ui-topic`（D12 Demo 样机 / 纯 Mock）。  
**Q161**：旧 Graph 单页脚手架 `ZmateStrategyTaskPage` 删除；分站按 WF 重做。

### 路由清单（对齐 IA/WF §9.2）

| Frame | 路由 |
| --- | --- |
| 创作壳 | `/zmate-strategy-demo` |
| Graph Hub | `/zmate-strategy-demo/run/:runId` |
| 澄清 | `…/clarify` |
| Planner | `…/planner` |
| 辩论 | `…/debate` |
| 切片 | `…/slice` |
| Seeker | `…/seeker` |
| Writer | `…/writer` |
| Judge | `…/judge` |
| 旧链兼容 | `/zmate-strategy-demo/task/:id` → Hub |

### 行为合同落地

1. **人闸解锁**：澄清确认+研判卡 → Planner → **辩论 ∥ 切片** → 切片批准 → Seeker →（辩论结束或 Hub 显式跳过）+ 取数 → Writer → Judge  
2. **禁止**单页一键跑完全链；Hub 无「一键跑完」  
3. **术语**：辩论知识卷宗 ≠ 专题切片/研判卡（站顶提示 + 评审术语卡）  
4. **Judge Default-FAIL**；职责文案 ≠ 战略胜负裁判  
5. **右侧报告宿主**：等待需求确认 / 生成中骨架不出正文 / 终稿只读；对抗审查 V3 抽屉壳  
6. **菜单只增不删**：`Layout`「战略报告 Demo」入口保留  
7. **可观测**：`track(...)` 各站 view/done + 创建/跳过辩论  
8. **内部评审**：`ReviewMounts` 自闸；关模式零泄漏条款字样

## 偏离说明

- 无。局部对照旧 L01–L08 状态机语义重写，未默认保留旧单页。

## 产物清单

- 代码：`repos/demo-ui-topic/src/app/pages/zmate-strategy/**`（含 `ReportHost` / `ReviewMounts`）  
- 路由：`src/app/routes.tsx`  
- 菜单：`src/app/components/Layout.tsx`（仅注释更新，入口未删）  
- 删除：`ZmateStrategyTaskPage.tsx`（废稿）

## 测试结果

- `pnpm build`：**绿**（vite build ~36s，exit 0）

## 架构合规自检

| 铁律 | 结论 |
| --- | --- |
| D12 demo/lumen | ✅ 仅 demo-ui-topic；无 lumen 直连 |
| 调用链 | ✅ 纯 Mock / localStorage |
| D8 Design | ✅ `#165DFF` / `#D8E7FC` / 控件 32px / Arco |
| D9 | ✅ 四态诚实 Mock；禁假 live；评审开可见 Mock 角标 |
| D10 | ✅ 人闸 / 锁定 Tooltip / 分站 |
| 可观测 | ✅ track |
| 菜单 | ✅ 只增不删 |

## CI/CD（必填）

- 分支：`origin/dev`（demo-ui-topic）
- commit：见推送后 SHA（本 handoff 同批登记）
- pipeline：push 后 GitLab CI 自动
- 部署：demo 仓 CI → K8s/静态站惯例
- K8s rollout：随 CI（非本叶手工）
- 本地验证：`pnpm build` 绿

## 可观测性（建议）

- 事件前缀：`zmate_strategy_*` / `zmate_stage_*`
- OTEL：Demo 页走仓内 `observability.ts` console sink

## 涉及文件

- `src/app/pages/zmate-strategy/*`（重写）
- `src/app/routes.tsx`
- `src/app/components/Layout.tsx`

## 遗留风险

- 项目轨「示例任务」点进依赖本机 localStorage run；新建任务后轨内 id=runId 可恢复  
- Judge 对 Demo 缺口指标默认 FAIL（符合 Default-FAIL）；带着 known_gaps 仍可开终稿只读入口  

## 默认签收

监管人 `human:淮政玮` 派单含默认签收授权；本叶完成后按授权推进 registry。
