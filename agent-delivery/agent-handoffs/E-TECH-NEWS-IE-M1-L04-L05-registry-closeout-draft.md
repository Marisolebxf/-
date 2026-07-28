# Registry 关单草稿 · E-TECH-NEWS-IE-M1-L04 / L05

> **性质**：关单草稿（供 coordinator / 监管人粘贴或确认后写入 `task-registry.yaml`）  
> **写入权限**：Agent **不得**自行 `status: done`；本草稿默认建议 `review`，由监管人验收后由 **coordinator** 改 `done`。  
> **日期**：2026-07-28  
> **说明**：L04/L05 为 M1 后质量加固与 UX 补齐，**事后补登**（工作已完成并 push）；非倒填 `claimed` 开工态。

---

## 1. 关单摘要（给人看）

| task-id | 标题 | 执行 Agent | 建议监管人 | 建议状态 | Evidence |
|---------|------|------------|------------|----------|----------|
| `E-TECH-NEWS-IE-M1-L04` | 四要素质量加固：门控 / impact / 金标 / Java 超时 | `algorithm-agent`（+ api 超时） | `human:淮政玮`（算法）兼知会 `human:孙英哲`（联调） | **review** → done | `agent-handoffs/E-TECH-NEWS-IE-M1-L04.md` |
| `E-TECH-NEWS-IE-M1-L05` | 复核页门控 warning UX + impact「暂无」 | `frontend-agent` | `human:孙英哲` | **review** → done | `agent-handoffs/E-TECH-NEWS-IE-M1-L05.md` |

### DoD 自检（L04）

| DoD | 证据 |
|-----|------|
| 文类门控软拒绝 HTTP 200 + error.code | Python 点验 V1/V2 PASS；`03-dev-verify.json` |
| impact 优先非空 + matter≠impact | 金标 mock 28/28；V3 impact 非空 |
| 金标 G01–G28 + 评测 CLI | `tests/tech_news_ie/gold/`；`tech-news-gold-eval.ps1` |
| algo push | `demo-algo-science` `0ec4013` @ `origin/dev` |
| Java read-timeout 120s | demo-svc `d8f2456` / lumen-svc `59d9f6c` |
| handoff + 点验清单 | L04.md + evidence `03-dev-verify-checklist.md` |

### DoD 自检（L05）

| DoD | 证据 |
|-----|------|
| 门控 Alert warning（非系统失败语气） | `lumen-ui-science-pc` `546ebb1f` |
| impact null →「暂无」 | 同上 |
| handoff | `E-TECH-NEWS-IE-M1-L05.md` |

### 开放项（写入 acceptance_note，不挡 review）

- 本机网关 `9999` 曾 502；UI 登录截图待环境恢复后补（与 L03 同类残留）
- 正式 epic 是否要把 L04/L05 记入 WBS：请 PM/coordinator 确认

---

## 2. 建议粘贴到 `task-registry.yaml`（插在 L03 之后、`E-INNOV-M1-L01` 之前）

```yaml
  - id: E-TECH-NEWS-IE-M1-L04
    epic: E-TECH-NEWS-IE-M1
    delivery_phase: implementation
    title: Phase D — 四要素质量加固（门控/impact/金标回归）+ Java 读超时
    agent: algorithm-agent
    repo: [innov_py.demo, backend.demo, backend.lumen]
    language: [python, java]
    depends_on: [E-TECH-NEWS-IE-M1-L03]
    status: review
    claimed_by: agent:algorithm-agent
    supervised_by: human:淮政玮
    claim_type: pull
    note: |
      事后补登：质量波次已在 2026-07-28 完成并 push；本条用于监管验收关单，不倒填开工认领锁。
      含 api 侧 timeout 调整（demo-svc / lumen-svc）。
    completed_at: "2026-07-28T16:30:00+08:00"
    claimed_at: "2026-07-28T12:00:00+08:00"
    lock_until: "2026-07-28T16:00:00+08:00"
    worktree_branch: dev
    commit_sha: 0ec4013
    estimated_tokens: 180_000
    effort_points: 5
    difficulty: M
    effort_source: retro_estimate
    model_used: cursor-grok-4.5
    actual_tokens: 0
    actual_cost: 0.0
    cost_warn: green
    design_refs:
      - agent-delivery/designs/tech_news_ie/docs/java-integration.md
      - agent-delivery/agent-handoffs/E-TECH-NEWS-IE-M1-L04.md
    definition_of_done:
      - 文类门控（政策/时论/零售）软拒绝 HTTP 200，error.code 可区分
      - impact 优先非空；禁止 matter 复述与跨事件复制；无效果句可为 null
      - 金标回归集 ≥20 条；mock 金标全绿；提供 gold/web 评测 CLI
      - demo-algo-science 已 push origin/dev；handoff 已提交
      - Java tech-news 读超时 ≥120s（demo-svc + lumen-svc）已 push
      - 本机 Python 直连点验（门控×2 + 抽取 impact）通过并留 evidence
    acceptance_note: |
      【待监管人签字】建议 human:淮政玮 验收算法；知会 human:孙英哲（Java/联调）。
      algo 0ec4013；demo-svc d8f2456；lumen-svc 59d9f6c；orchestration handoff L04 + 03-dev-verify 3/3 PASS。
      残留：网关/UI 端到端截图待环境恢复（不挡算法关单）。
    evidence: agent-delivery/agent-handoffs/E-TECH-NEWS-IE-M1-L04.md

  - id: E-TECH-NEWS-IE-M1-L05
    epic: E-TECH-NEWS-IE-M1
    delivery_phase: implementation
    title: Phase D′ — 复核页门控 warning UX + impact 空文案
    agent: frontend-agent
    repo: lumen-ui-science-pc
    language: typescript
    depends_on: [E-TECH-NEWS-IE-M1-L04]
    status: review
    claimed_by: agent:frontend-agent
    supervised_by: human:孙英哲
    claim_type: pull
    note: |
      事后补登：对齐 L04 门控软拒绝契约；UI 已合入 origin/dev。
    completed_at: "2026-07-28T16:28:00+08:00"
    claimed_at: "2026-07-28T16:20:00+08:00"
    lock_until: "2026-07-28T20:20:00+08:00"
    worktree_branch: feat/E-TECH-NEWS-IE-M1-L05
    commit_sha: 546ebb1f
    estimated_tokens: 40_000
    effort_points: 2
    difficulty: S
    effort_source: retro_estimate
    model_used: cursor-grok-4.5
    actual_tokens: 0
    actual_cost: 0.0
    cost_warn: green
    design_refs:
      - agent-delivery/agent-handoffs/E-TECH-NEWS-IE-M1-L04.md
      - agent-delivery/Design.md
    definition_of_done:
      - 门控 error.code 以 warning「文类已拦截」展示，不以系统失败语气误导
      - impact 为 null/空时显示「暂无」
      - 仅调 Java；合入 origin/dev；handoff 已提交
    acceptance_note: |
      【待监管人签字】建议 human:孙英哲 验收。
      UI merge 546ebb1f @ origin/dev；handoff E-TECH-NEWS-IE-M1-L05.md。
      残留：登录态截图待网关恢复后补。
    evidence: agent-delivery/agent-handoffs/E-TECH-NEWS-IE-M1-L05.md
```

---

## 3. Coordinator 关单话术（可选）

```text
请验收 E-TECH-NEWS-IE-M1-L04 / L05（status=review）：
- L04：算法质量 + 金标 + Java 120s 超时；Python 点验 3/3
- L05：门控 warning + impact「暂无」
签字后请将两条改为 status: done，并补 acceptance_note 监管人确认句。
开放项：网关 UI 截图（非阻塞）。
```

---

## 4. 请你确认后再落库

回复其一即可：

1. **写入 registry（review）** — 我把上表 YAML 插入 `task-registry.yaml` 并 push  
2. **直接 done** — 需你（或以 coordinator 身份）明确授权监管人已验收  
3. **改监管人/文案后再写** — 指出要改的字段
