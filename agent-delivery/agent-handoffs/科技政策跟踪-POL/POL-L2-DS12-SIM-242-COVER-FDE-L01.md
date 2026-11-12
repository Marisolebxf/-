# POL-L2-DS12-SIM-242-COVER-FDE-L01 · 242 政策解读报告生成 · 需规分句闭合 FDE

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:product-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 监管人确认卡1=B 后「按此计划开始」 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full`（FE D 波）；文档波次 `N/A` |
| 说明 | 未用 YAGNI 跳过 D8/可观测；下载复用已有 situation/report，未新造导出栈 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 headroom MCP |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无新增图；沿用 `POL-L2-DS12-SIM-ARCH-SEQ` 既有 jobs 读面 |
| 图 diff | 下载另轨 `situation/report`，不改 jobs 边 |
| 会签态 | ARCH/API/说明书 C 波已回写（见 C 简报） |

## 修改内容

- **卡1=B**：live 须 Word/PDF 下载，走 `POST /display/v1/situation/report/generate`（`reportType=policy-interpret-report`），对标 217；废止「没有下载」
- **A–E**：产品界面必见 → arch 废止「导出前不实现」→ 会签回写 ARCH/API/说明书 → FE live 接线 → 合规用例形态
- **FE**：`InterpretWorkbench.vue` live 补格式选择 + 下载；复用 `exportInterpretReport`；空态「没有解读报告段落」
- **不扩**：237–241；不新表；不接核增 `report/jobs`；默认不改 Java

## 测试结果

- `lumen-ui-science-pc`：`pnpm type-check`（`vue-tsc --build`）exit 0
- 合规用例 242：已废止「没有下载」；补章节自定义 + 真 PDF/Word 形态期望（E 简报）
- 线上冒烟：本会话未打鉴权后 generate；jobs 四段正文此前 DEMO-ACCEPT 可演；下载链与 217 同构，待 push 后 CI/K8s 复验

## 遗留风险

- FE 推送后需在 dev 用样例 `policy_id=18363390` 点生成 → 勾选章节 → 导出 PDF，确认真字节与文件名
- `policy-interpret-report` 为自由字符串、无白名单；若 generate 失败再最小排查（非默认改 Java）
- 关评审后须确认无「演示」等业务文案泄漏（D 波自检：无新增黑话）

## CI/CD（必填）

- 分支：`dev`
- orchestration：多 commit（A–E 简报 / ARCH·API·说明书 / 用例）；见 `be695510a`…`46ee7c24a` 一带
- FE：`lumen-ui-science-pc` `21844ac`（本 handoff 收口时 push）
- pipeline / rollout：以 push 后 GitLab CI 为准（写 handoff 时未等绿）
- 验收页：展示系统 · 政策效果推演 · 科技政策推演 · 「政策解读报告生成」

## 涉及文件

- `sdd/简报/2026-11-12-政策解读报告生成-需规分句闭合.md`
- `sdd/简报/2026-11-12-SIM-242-COVER-FDE-{A,B,C,D,E}-*.md`
- `sdd/l2/POL-L2-DS12-SIM-ARCH.md` / `-API.md`
- `sdd/科技政策跟踪-系统详细设计说明书.md` §242
- `合规演示用例/POL-L2-DS12-SIM-合规演示用例.md` 242 行
- `repos/lumen-ui-science-pc/.../interpret/InterpretWorkbench.vue`

## 波次简报索引

| 波 | 简报 |
|---|---|
| A | `sdd/简报/2026-11-12-SIM-242-COVER-FDE-A-product.md` |
| B | `sdd/简报/2026-11-12-SIM-242-COVER-FDE-B-arch.md` |
| C | `sdd/简报/2026-11-12-SIM-242-COVER-FDE-C-会签.md` |
| D | `sdd/简报/2026-11-12-SIM-242-COVER-FDE-D-impl.md` |
| E | `sdd/简报/2026-11-12-SIM-242-COVER-FDE-E-case.md` |
