# SVC-ALGO-DESIGN-L01 —— 产业服务深度分析算法设计（招标 §9 · 10 模型）

> **任务**：SVC-ALGO-DESIGN-L01
> **执行人**：algorithm-agent（human:唐绍祖）
> **日期**：2026-08-04
> **状态**：🟡 ready_to_sign（唐绍祖已 review，待任务发起人淮政玮/徐腾强审核签收）

---

## 1. 产出物清单

| 文件 | 路径 | 说明 |
|------|------|------|
| 产业服务算法设计说明.md | repos/demo-algo-ent-analysis/docs/ | SVC 10 模型算法设计分册 v0.2（输入输出、指标权重、数据依赖、API、联调台映射、Mock vs 真实、算法流程/容错/动态更新） |
| 算法设计说明.md | repos/demo-algo-ent-analysis/ | 新增第 23 章交叉引用 |
| 客户决策清单跟踪表.md | agent-delivery/ | 新增 Q060~Q063（🟡） |
| SVC-ALGO-DESIGN-L01.md | agent-handoffs/算法库联调-ALGO-LIB/ | 本 handoff |
| task-registry.yaml | agent-delivery/ | SVC-ALGO-DESIGN-L01 claimed → review → ready_to_sign，evidence/cost 回填 |

## 2. 范围证明

- ✅ 覆盖招标 §1.1.1.1.1.1.1.9 全部 10 模型，顺序与招标一致
- ✅ 每模型含输入输出、指标与权重草案（全部 `pending_client`）、ADS/DWD/Nebula 依赖、API 草图、联调台「产业服务算法库」子页映射、Mock vs 真实
- ✅ 复核补强 v0.2：公共运行流程/异常容错/动态更新（§2.5~2.6）、模型 1~10 算法流程与是否需要训练、模型 3~8 输入输出细化
- ✅ 口径歧义 Q060~Q063 已登记客户决策清单，未替甲方拍板
- ✅ 本阶段仅设计，未强制编码、未改动联调台页面

## 3. 架构合规自检

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 算法只在 Python（规划 `svcan/`，Java 只读 ADS） | ✅ |
| 2 | 权重/阈值进 config（`settings_svc.yaml`），草案标 `pending_client` | ✅ |
| 3 | 图谱只使用 NebulaGraph（`gkx_service`），未引入 Neo4j/NetworkX 生产路径 | ✅ |
| 4 | cfg_metric / cfg_model_registry 映射已给草案，注册待实现波次执行 | ✅ |
| 5 | 未替甲方闭合 Q060~Q063 | ✅ |
| 6 | cost 四字段已填写 | ✅ |

## 4. Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 150_000 |
| actual_tokens | 120_000 |
| model_used | gpt-5-codex |
| actual_cost | 0.75 |
| cost_warn | green |

## 5. 验证证据

- `docs/产业服务算法设计说明.md` 含 `SVC_SERVICE_CHAIN_GAP`、`SVC_SERVICE_RELATION_CHAIN`、`SVC_FINANCE_TECH_POWER`、`SVC_IP_TECH_POWER`、`SVC_HR_TECH_POWER`、`SVC_MKT_TECH_POWER`、`SVC_CONSULT_TECH_POWER`、`SVC_INNOV_TECH_POWER`、`SVC_ATTRACTION_RECOMMEND`、`SVC_CULTIVATION_RECOMMEND` 共 10 个模型 ID
- `docs/产业服务算法设计说明.md` §2.5~2.6 与模型 4/5/7/8 算法流程小节已补异常容错、动态更新、是否需要训练
- `算法设计说明.md` 第 23 章交叉引用已追加
- `客户决策清单跟踪表.md` §2.ac 已登记 Q060~Q063，状态 🟡
- 本阶段 `cicd: skip_design_only`，不强制 CI

## 6. 待会签 / 待办

| 项 | 责任 | 状态 |
|----|------|------|
| 设计 review | human:唐绍祖 | ✅ 已完成（2026-08-04） |
| 任务发起人审核 | human:淮政玮 / 徐腾强 | 待审核 |
| Q060~Q063 甲方确认 | PM / 甲方 | 待确认 |
| `svcan/` 实现与 cfg_metric/cfg_model_registry 注册 | algorithm-agent / data-agent | 待实现波次 |
