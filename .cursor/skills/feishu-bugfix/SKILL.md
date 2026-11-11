---
name: feishu-bugfix
description: Process bugs assigned to the current user from Feishu Project using the official Feishu Project MCP. Use when the user asks to inspect, fix, verify, or ship their OPEN/REOPEN Feishu Project bugs.
---

# Feishu Project Bug Fix

Use the official `feishu-project-native` MCP. Do not use a self-hosted Project MCP or a direct OpenAPI wrapper.

Authentication belongs to the client MCP configuration. For Codex, use HTTP OAuth against `https://project.feishu.cn/mcp_server/v1`; Cursor/Trae may use HTTP Header mode. Never put tokens or secrets in this Skill or the repository.

Project defaults:

- Project: `GKX 生产`
- project_key: `6a687a81e231818dec771f9a`
- Work item type: `issue` / 缺陷
- Query `OPEN`; include `REOPEN` only when the project returns that state

## Operating principles

1. **Evidence before inference.** Business behavior must be grounded in the main orchestration repo, the business repository, or the latest explicit human decision. Do not infer requirements from a screenshot alone.
2. **Smallest safe change.** Fix the failing path, not the whole subsystem. Expand scope only with recorded evidence.
3. **Risk-matched process.** S-level work is lightweight. M adds one targeted independent review. L or cross-repository work exits this lightweight flow.
4. **Local first.** Reproduce and verify locally whenever practical. Shared dev is for one post-ship integration check, not the inner development loop.
5. **One run, one current truth.** Per-run state lives under `agent-delivery/bugfix-runs/<auto_number>-<work_item_id>/`; Feishu owns business status.
6. **Stop instead of guessing.** Missing requirements, unavailable environment, unrelated red baseline, or unsafe data access are blockers, not reasons to invent behavior.

## Main-repo source map

Read only the sources relevant to the current defect. Start from `.cursor/skills/feishu-bugfix/references/BUG-PLAYBOOK.md` for the full type-specific guide.

| Need | Canonical source |
|---|---|
| Repo, service, CI, dev URL | `agent-delivery/repo-registry.yaml`, `agent-delivery/paths.yaml`, repo `.gitlab-ci.yml` |
| Business scope/background | `agent-delivery/bid-reference/**`, `agent-delivery/工程过程/**` |
| SRS and acceptance | `agent-delivery/验收文档/**`, `agent-delivery/formal-docs-registry.yaml` |
| UI/design rules | `agent-delivery/Design.md`, `agent-delivery/Design-mobile.md` |
| Data semantics/lineage | `agent-delivery/data/**`, `agent-delivery/data-source-mapping-registry.yaml`, `agent-delivery/data-lineage-policy.md`, `agent-delivery/数据库设计.md` |
| Tests and ownership | `agent-delivery/qa/**` |
| Coding/push/long-task rules | `.cursor/rules/**`, business repo `AGENTS.md`, business repo docs |

`requirement_refs` must contain a concrete file path + section, API/test ID, or Feishu comment anchor. A bare statement such as “按需规” is invalid.

## Workflow

### 0. Preflight

Before changing code:

1. Resolve `GKX_ROOT` from `gkx-orchestration/.env`; never hardcode the workspace root.
2. Read the business repo's `AGENTS.md` and the relevant rules/docs from the source map.
3. Record the target branch SHA and confirm the worktree state.
4. Check the latest target-branch pipeline:
   - Red for an unrelated baseline reason: report the owner, URL and failure, then block without charging a patch round.
   - Red in the suspected path: continue diagnosis.
5. Confirm local dependencies/run conditions and that no other active run owns the defect.

### 1. Claim

Immediately after selecting the bug, and before downloading images, inspecting code, writing data or creating a branch:

1. Call `get_transitable_states`.
2. If `OPEN`/`REOPEN` and `IN PROGRESS` is available, call `get_transition_required`, then `transition_state`.
3. Add one concise `[agent-claim]` comment with `【auto_number】title`, claim/session ID, timestamp and scope.
4. Preserve `claim_comment_ref` and `claim_operator` in the run ledger.
5. If already `IN PROGRESS`, treat it as another active run and stop. Take over only for the complete message `接管【auto_number】`.
6. Never transition the bug to `RESOLVED`; final acceptance belongs to a human/business action.

Use human-readable references in conversation and comments: `【auto_number】title（内部ID: work_item_id）`.

### 2. Build the Bug Contract

Before requesting `进入开发`, record:

- observed symptom and reproduction;
- expected behavior with explicit quantifiers such as default/all/only/never;
- affected page/API/service/repo/table/permission;
- non-goals;
- authoritative sources;
- verification method and required evidence.

If the expected behavior is missing or conflicts with the latest human decision, ask only the blocking question. Do not implement a guess.

### 3. Classify and route

Load the matching section of `references/BUG-PLAYBOOK.md`:

| Type | Typical route |
|---|---|
| UI/interaction/chart | local browser + DOM/ECharts assertions |
| API/business logic | contract + unit/integration + error/auth cases |
| Data/SQL/ETL | lineage + read-only check + scoped writes + rollback |
| Algorithm/model | deterministic fixture + golden output + performance |
| Config/release/CI | dry-run + pipeline/job/rollout + rollback |
| Permission/security | least privilege + positive/negative authorization tests |
| Cross-repo/unknown | route to existing long-task flow or block after bounded triage |

Record the chosen risk level and verification plan. Do not apply a frontend playbook to a data or algorithm defect.

### 4. Reproduce and fix

1. Reproduce with the smallest local or read-only method.
2. Add a failing regression test or equivalent machine assertion when practical.
3. Work on a dedicated `fix/<work-item-id>-<short-slug>` branch/worktree.
4. Make the smallest correct change and preserve unrelated dirty work.
5. Run only the relevant test groups while iterating; run the full required self-check once before review.

Avoid repeated screenshots. For UI work, use programmatic state assertions and cover below-the-fold content. Keep at most one final screenshot if visual evidence is genuinely required.

### 5. Verification

Every repository needs:

- `fix`: the reported failure now passes;
- `regression`: adjacent behavior remains correct.

Add only applicable categories from `boundary`, `integration`, `data`, `algorithm`, `security`, `performance`, or `rollback`. M/L work must include at least one non-happy-path category. A PASS verification may reference only reviewable evidence whose raw artifact was retained.

Evidence should be minimal and high-signal:

- exact command and exit code;
- relevant stdout/test log;
- commit SHA and environment;
- pipeline/deploy/job URL for shipped facts;
- data write authorization and policy/scope hashes when applicable.

Do not store every exploratory command. Do not describe Agent-recorded pipeline facts as locally verified facts.

### 6. Run ledger

The canonical helper is `scripts/bugflow-state.mjs`. Use its commands rather than hand-editing `state.json`:

```bash
node .cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs --help
node .cursor/skills/feishu-bugfix/scripts/bugflow-state.selfcheck.mjs
```

Typical sequence:

```text
init -> record-diagnosis -> record-plan -> set-repos
-> approve-gate enter_dev -> advance IMPLEMENTING
-> verify-repo -> record-review -> record-verification
-> verify-evidence -> advance READY_SHIP
-> approve-gate ship -> advance SHIPPING
-> record-ship-package -> verify-evidence
-> advance DEV_VERIFYING -> advance AWAITING_ACCEPTANCE
```

Use `block`, `cancel`, `reopen`, `takeover` for side paths. Write data authorization through `check-data-write`, never by editing policy fields.

Read `references/P0-DESIGN.md` only when gate/hash/evidence details matter.

### 7. Gates and rework

- `进入开发` authorizes code changes, a dedicated fix branch and a Draft MR. Request it only after the Bug Contract, scope, plan and current baseline are explicit.
- `提测` authorizes merge to `dev`, push, CI/CD, dev deployment and one dev verification. It never authorizes production.
- Rework after failed acceptance within the same scope and risk keeps the existing claim and source analysis; redo diff/review/verification and request only `提测` again.
- Scope expansion, new repository, data write, permission model change, production risk or L routing invalidates old assumptions and requires a fresh decision.

### 8. Ship and failure handling

Before merge:

1. Refresh the latest `dev`; never merge an assumption from an old local ref.
2. Confirm the baseline pipeline is green or that its red path is unrelated.
3. Merge/rebase only the authorized candidate and push `dev`.
4. Track the real pipeline, image tag, deployed SHA and rollout.

If remote `dev` advances after the first full local validation, decide whether a second full local pass is necessary instead of automatically rebuilding:

```bash
node .cursor/skills/feishu-bugfix/scripts/revalidation-plan.mjs \
  --repo-dir <repo> \
  --candidate-ref <candidate-sha> \
  --remote-ref origin/dev \
  --remote-pipeline-status success \
  --premerge-checks-passed \
  --json
```

- `no_revalidation`: candidate already reached remote; do not rebuild.
- `targeted`: remote is green, conflict-free and disjoint; run `git diff --check` plus the narrow target test, then rely on CI for full integration.
- `full`: candidate files overlap, remote touches shared config/types/API/dependencies, pipeline is unknown, or pre-merge checks were not completed; rerun type-check/build and the relevant regression set.
- `block`: baseline is red; stop and report the owner instead of charging another patch round.

Classify failures as `merge`, `push`, `pipeline`, `rollout`, `dev_verify` or `rework`.

- Unrelated baseline/CI failure: block with owner and URL; do not increment the bug patch round.
- Same environmental/runner failure twice with no progress: block and retry only after the condition changes.
- Code failure: fix, increment the patch round, and stop after 3 rounds.

### 9. Acceptance

At `AWAITING_ACCEPTANCE`:

- write the ship summary to Feishu with fix, tests, pipeline, image and rollout;
- list concise manual acceptance steps;
- wait for the human to move the Feishu state to `RESOLVED` or back to `REOPENED`;
- record the observed status; never call `transition_state` to resolve it yourself.

Only the claim comment, ship summary and final acceptance summary are required external comments. Do not write one comment per internal phase.

## Time boxes and stop-loss

- S: target 30–60 minutes from contract to dev deployment.
- M: target 1–2 hours.
- At 90 minutes without a clear blocker resolution, report progress and ask for a decision instead of continuing blind retries.
- At the third code patch round, stop and reassess as unknown/L.
- Never count unrelated baseline failures as patch rounds.

## Screenshot-only requests

A screenshot or clipboard image is evidence, not a claimable work item. Before inspecting code, querying data or creating a branch, locate the matching claimed Feishu bug assigned to the current user. If none exists, ask for the work-item identifier/title; do not invent a bug from the image alone.

## Stop conditions

- No active bug assigned to the current user.
- Another active run owns the item and no valid takeover exists.
- Missing expected behavior or authoritative requirement source.
- Missing reproduction environment, credentials or permissions.
- Unrelated red baseline or unrecoverable CI/environment failure.
- Required data write is outside policy/scope.
- Cross-repo, schema, permission or production risk exceeds the lightweight flow.
- Three code patch rounds have failed without a new hypothesis.

Report the work item, blocker, evidence already checked and exact human action needed. Leave business status unchanged unless an explicit legal transition exists.
