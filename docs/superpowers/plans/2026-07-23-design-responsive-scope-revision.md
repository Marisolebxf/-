# Design Responsive Scope Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align `Design.md`, the topic-system Demo shell, governance status, and three reusable GKX skills with the approved medium-screen, small-screen, and independent large-screen boundaries.

**Architecture:** Keep `Design.md` authoritative for the shared `1440–1920px` medium workbench and the information-display system's `<1440px` mobile reflow, while routing `>1920px` large-screen work to Track-L. Enforce the boundary with deterministic contract scripts, then align the existing topic Demo shell without changing business pages or unrelated working-tree changes.

**Tech Stack:** Markdown governance docs, Node.js contract scripts, React/Vite CSS, YAML task registry, Codex skill packages.

---

## Execution constraints

- Work in the existing non-main feature branches because the approved specification is already committed there and the three personal skills live outside either Git repository.
- Preserve all unrelated dirty-worktree changes. Stage and commit only clean, fully owned files; do not stage the already-dirty `task-registry.yaml`.
- Do not create or use subagents: the active collaboration policy does not authorize delegation. Replace skill forward-testing with deterministic negative/positive contract tests and direct scenario review.
- Apply each skill update and validate it before moving to the next skill.

### Task 1: Add the responsive-scope contract in RED

**Files:**
- Create: `/Users/ying/.codex/skills/gkx-ui-design-standards/scripts/check-responsive-scope.mjs`

- [ ] **Step 1: Create a target-aware checker**

The script accepts `--target ui|product|demo|workspace|all` and `--workspace <path>`. It asserts:

```text
ui: the UI skill and source map contain medium_1440_1920, small_reflow, large_screen_track_l; topic rejects small_reflow
product: the product-package skill defines the three tiers and system constraints
demo: the Demo skill branches Design.md usage by screen_tier
workspace: Design.md contains the approved matrix and no >=1920 shared-workbench rule
```

- [ ] **Step 2: Verify RED**

Run each target before changing the skills or `Design.md`. Expected: every command fails on a missing approved token or obsolete breakpoint rule.

### Task 2: Revise Design.md and governance status

**Files:**
- Modify: `/Users/ying/Documents/codex/gkx-lumen/gkx-orchestration/agent-delivery/Design.md`
- Modify: `/Users/ying/Documents/codex/gkx-lumen/gkx-orchestration/agent-delivery/task-registry.yaml`
- Modify: `/Users/ying/Documents/codex/gkx-lumen/gkx-orchestration/agent-delivery/agent-handoffs/产品整体定义/Design-通用交互组件栅格体系-轻量评审单.md`

- [ ] **Step 1: Rewrite the scope and breakpoint contract**

Add the explicit matrix:

```text
>1920px: topic undefined; information-display large-screen work uses Track-L and a separate specification
1440–1920px: both systems use medium_1440_1920
<1440px: topic unsupported; information-display uses small_reflow
```

Rename scope-bearing PC-wide terminology to medium workbench. Preserve the existing 24-column calculations at the 1920 baseline.

- [ ] **Step 2: Replace composite-control labels**

Import `Form` in the minimum template and replace each native label around `Select` or `DatePicker.RangePicker` with an Arco `Form.Item`, for example:

```jsx
<Form.Item label="地域范围" field="region">
  <Select placeholder="全球" />
</Form.Item>
```

- [ ] **Step 3: Close task status consistently**

Set only `E-PROD-UXUE-COMP-L03` to `status: done`. Mark review item R2 `in_progress` until frontend verification closes it.

- [ ] **Step 4: Verify workspace contract**

Run `git diff --check` for the three exact files and the responsive checker with `--target workspace`. Expected: both pass.

### Task 3: Update gkx-ui-design-standards

**Files:**
- Modify: `/Users/ying/.codex/skills/gkx-ui-design-standards/SKILL.md`
- Modify: `/Users/ying/.codex/skills/gkx-ui-design-standards/references/source-map.md`

- [ ] **Step 1: Replace obsolete layout rules**

Define the three `screen_tier` values, support matrix, medium breakpoints, information-display mobile-reflow order, and Track-L exclusion. Keep full details in `source-map.md`.

- [ ] **Step 2: Verify the UI skill**

Run:

```bash
node /Users/ying/.codex/skills/gkx-ui-design-standards/scripts/check-responsive-scope.mjs --target ui --workspace /Users/ying/Documents/codex/gkx-lumen
python /Users/ying/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/ying/.codex/skills/gkx-ui-design-standards
node /Users/ying/.codex/skills/gkx-ui-design-standards/scripts/check-composite-labels.test.mjs
node /Users/ying/.codex/skills/gkx-ui-design-standards/scripts/test-review-extension-contract.mjs
```

Expected: all commands exit 0. Keep `agents/openai.yaml` unchanged if it contains no obsolete breakpoint.

### Task 4: Update gkx-product-definition-package

**Files:**
- Modify: `/Users/ying/.codex/skills/gkx-product-definition-package/SKILL.md`

- [ ] **Step 1: Add the screen-tier gate**

Require exactly one of:

```yaml
screen_tier: medium_1440_1920
screen_tier: small_reflow
screen_tier: large_screen_track_l
```

Reject `small_reflow` for the topic system. Require `large_screen_track_l` to use Track-L without inheriting the medium shell.

- [ ] **Step 2: Verify the product skill**

Run the responsive checker with `--target product` and `quick_validate.py` on the skill. Expected: both exit 0. Inspect metadata for conflicts.

### Task 5: Update gkx-definition-to-demo

**Files:**
- Modify: `/Users/ying/.codex/skills/gkx-definition-to-demo/SKILL.md`

- [ ] **Step 1: Add screen-tier routing**

Branch before implementation:

```text
medium_1440_1920 -> Design.md medium shell and 24-column rules
small_reflow -> information-display mobile reflow; reject topic modules
large_screen_track_l -> Track-L large-screen package; do not inherit medium Header/Sidebar/24-column shell
missing or conflicting tier -> block and return to product definition
```

- [ ] **Step 2: Verify the Demo skill**

Run the responsive checker with `--target demo`, `quick_validate.py`, then the checker with `--target all`. Expected: all exit 0. Inspect metadata for conflicts.

### Task 6: Align topic Demo shell and checks

**Files:**
- Modify: `/Users/ying/Documents/codex/gkx-lumen/repos/demo-ui-topic/scripts/check-design-contract.mjs`
- Modify: `/Users/ying/Documents/codex/gkx-lumen/repos/demo-ui-topic/src/styles/theme.css`
- Modify: `/Users/ying/Documents/codex/gkx-lumen/repos/demo-ui-topic/src/styles/design-tokens.css`
- Modify: `/Users/ying/Documents/codex/gkx-lumen/repos/demo-ui-topic/scripts/check-trend-semantics.mjs`

- [ ] **Step 1: Establish RED for shell dimensions**

Change contract assertions to require `200px / 64px / 64px` and forbid old application-shell declarations using `224px` or `68px`. Run `npm run design:check`; expected failure before CSS changes.

- [ ] **Step 2: Align shell CSS**

Change only shell declarations:

```css
.app-sidebar { width: 200px; }
.app-top-header { left: 200px; height: 64px; }
.app-main { margin-left: 200px; padding: 64px 16px 16px; }
.app-content-panel { height: calc(100vh - 80px); }
.app-modal-overlay { left: 200px; top: 64px; }
```

At `max-width: 1679px`, apply collapsed `64px` geometry without mobile navigation. Do not modify unrelated component dimensions that use `68px`.

- [ ] **Step 3: Update stale token documentation**

State that Arco is the common component base while Tailwind, Recharts, and lucide remain implementation details.

- [ ] **Step 4: Repair trend contract**

Remove only the obsolete requirement that `DevelopmentOverview.tsx` contain trend variables when it no longer renders KPI trend text. Preserve token-mirror, `MetricCard`, `industryShared`, and forbidden-legacy assertions.

- [ ] **Step 5: Verify frontend**

Run:

```bash
npm run design:check
node scripts/check-trend-semantics.mjs
node /Users/ying/.codex/skills/gkx-ui-design-standards/scripts/check-composite-labels.mjs src/app/components/Layout.tsx
npm run build
```

Expected: all commands exit 0.

### Task 7: Close evidence and inspect diffs

**Files:**
- Modify: `/Users/ying/Documents/codex/gkx-lumen/gkx-orchestration/agent-delivery/agent-handoffs/产品整体定义/Design-通用交互组件栅格体系-轻量评审单.md`

- [ ] **Step 1: Close R2 with verified evidence**

Record the verified `200px / 64px / 64px` shell, the `1680px` medium breakpoint behavior, and the explicit exclusion of topic-system `<1440px` support. Do not claim information-display mobile pages were implemented.

- [ ] **Step 2: Run final combined checks**

Run `git diff --check` on exact orchestration paths and the responsive checker with `--target all`. Expected: both exit 0.

- [ ] **Step 3: Preserve unrelated changes**

Review exact-path diffs and `git status --short` in both repositories. Commit only clean owned files. Leave `task-registry.yaml` unstaged if it still contains unrelated changes and report its scoped one-line edit as uncommitted.

