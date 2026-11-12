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
2. **Requirement coverage is mandatory.** Every defect must map to an SRS functional point, formal acceptance item, QA case, or the latest explicit human decision. Fixing the screenshot without covering the requirement is not done.
3. **Smallest safe change.** Fix the failing path, not the whole subsystem. Expand scope only with recorded evidence.
4. **Risk-matched process.** S-level work is lightweight. M adds one targeted independent review. L exits this lightweight flow. Multiple repositories for the same Feishu bug stay in one run as a cross-repo Bundle; they are not split into separate bugs.
5. **Local first.** Reproduce and verify locally whenever practical. Shared dev is for one post-ship integration check, not the inner development loop.
6. **One run, one current truth.** Per-run state lives under `agent-delivery/bugfix-runs/<auto_number>-<work_item_id>/`; Feishu owns business status.
7. **Stop instead of guessing.** Missing requirements, unavailable environment, unsafe data access, or a red baseline that blocks the affected path are blockers, not reasons to invent behavior.

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
4. Check the latest target-branch pipeline and separate development from shipping:
   - Red for an unrelated reason and disjoint from the defect path: record the repo/SHA, failing job, owner and URL as an open **ship blocker**; local development and targeted verification may continue, and the failure does not consume a patch round.
   - Red for an unrelated reason but it prevents local reproduction, the affected build/type-check, or required full verification: block development with the same owner/URL evidence.
   - Red in the suspected path: continue diagnosis and fix path.
   - The baseline must be green before `READY_SHIP`/`提测`; never merge/deploy against a knowingly red target branch and call it shipped.
5. Confirm local dependencies/run conditions and that no other active run owns the defect.

### 1. Claim

Immediately after selecting the bug, and before downloading images, inspecting code, writing data or creating a branch:

1. Call `get_transitable_states`.
2. If `OPEN`/`REOPEN` and `IN PROGRESS` is available, call `get_transition_required`, then `transition_state`.
3. Add one concise `[agent-claim]` comment with `【auto_number】title`, claim/session ID, timestamp and scope.
4. Preserve `claim_comment_ref` and `claim_operator` in the run ledger.
5. If already `IN PROGRESS`, treat it as another active run and stop. Take over only for the complete message `接管【auto_number】`.
6. Never transition the bug to `RESOLVED` until the human sends the complete exact message `验收通过` (or `验收通过<auto_number>` when multiple active runs). Natural language such as “可以了”“没问题”“算修复了” does not unlock acceptance.

Use human-readable references in conversation and comments: `【auto_number】title（内部ID: work_item_id）`.

### 2. Build the Bug Contract

Before requesting `进入开发`, record:

- observed symptom and reproduction;
- expected behavior with explicit quantifiers such as default/all/only/never;
- matching SRS functional point(s): SRS path + sequence/feature path, or the explicit accepted human requirement;
- affected page/API/service/repo/table/permission;
- non-goals;
- authoritative sources;
- verification method and required evidence.

If the expected behavior is missing or conflicts with the latest human decision, ask only the blocking question. Do not implement a guess.

### 2.1 SRS functional-point coverage

Before `进入开发`:

1. Search `agent-delivery/bid-reference/srs/**` by page, menu, feature and bug keywords. Also check `agent-delivery/验收文档/**` and `agent-delivery/qa/**` when present.
2. Record every in-scope functional point in `diagnosis.requirement_refs` as `path#序号/五级功能路径`. A generic document path without the functional point is not sufficient.
3. Map each functional point to the affected implementation path and expected observable behavior.
4. If one bug spans multiple requirement behaviors, list all of them; do not silently verify only the screenshot's first visible case.
5. Verification must explicitly cover the mapped functional behavior. For broader requirements such as zoom levels, tabs, switches or all cards, cover every mode affected by the change.

If no matching functional point exists, use a formal acceptance item, QA case, or latest explicit human decision and record that anchor. If none can be found, stop instead of inventing the expected behavior.

Use `references/REQUIREMENT-COVERAGE-CHECKLIST.md` to enumerate every SRS sub-function before coding; for “missing data/少模块/少指标” defects follow the data-loss triage order in `references/BUG-PLAYBOOK.md §3.1`.

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
| Cross-repo | one bug = one run/Bundle; per-repo candidates + dependency-ordered shipping |
| Unknown | bounded triage, then block or L route |

Record the chosen risk level and verification plan. Do not apply a frontend playbook to a data or algorithm defect.

### 3.1 Same-bug cross-repo Bundle

When one Feishu bug requires changes in multiple repositories:

- keep one Feishu work item, one claim, one run ledger, one Bug Contract and the same development/ship/acceptance gates;
- if another repository is discovered later, add it to the existing Bundle and invalidate the current gate; never create a second Feishu bug for the same defect;
- record every repository in `state.repos[]` with `role`, `depends_on` and `ship_order`;
- use risk **M** at minimum; cross-repo alone is no longer L and is never a reason to split the bug;
- verify every repository independently, then add at least one `integration` verification whose `repo_ids` covers the complete Bundle;
- merge/deploy in `ship_order`, with dependencies earlier than consumers;
- if any repository fails, the whole Bundle remains in rework/verification failure; never mark the bug complete from one successful repository.

### 4. Reproduce and fix

1. Reproduce with the smallest local or read-only method.
2. Add a failing regression test or equivalent machine assertion when practical.
3. Work on a dedicated `fix/<work-item-id>-<short-slug>` branch/worktree.
4. Make the smallest correct change and preserve unrelated dirty work.
5. Run only the relevant test groups while iterating; run the full required self-check once before review.

Avoid repeated screenshots. For UI work, use DOM/API/deployed-chunk assertions and cover below-the-fold content programmatically. If visual evidence is genuinely required, keep at most one before/after target-area screenshot per side (S); never use repeated full-screen captures as an exploration tool.

### 5. Verification

Every repository needs:

- `fix`: the reported failure now passes;
- `regression`: adjacent behavior remains correct.

Add only applicable categories from `boundary`, `integration`, `data`, `algorithm`, `security`, `performance`, or `rollback`. M/L work must include at least one non-happy-path category. A cross-repo Bundle must include an `integration` verification covering every repo in the Bundle. A PASS verification may reference only reviewable evidence whose raw artifact was retained.

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
  (multi-repo: each repo has role + depends_on + ship_order)
-> approve-gate enter_dev -> advance IMPLEMENTING
-> verify-repo -> record-review -> record-verification
-> verify-evidence -> advance READY_SHIP
-> approve-gate ship -> advance SHIPPING
-> record-ship-package -> verify-evidence
-> advance DEV_VERIFYING -> advance AWAITING_ACCEPTANCE
-> exact 验收通过 -> finalize-acceptance
-> Feishu transition_state RESOLVED -> record-acceptance(mode=chat_exact)
-> advance RESOLVED

BLOCKED recovery:
block -> satisfy resume_condition -> resume --to <resume_phase> --evidence-ref ...
```

Use `block` + `resume`, `cancel`, `reopen`, `takeover` for side paths. Every command that touches a run directory is serialized by a per-run lock. Use `record-evidence --evidence-batch-file` when recording multiple evidence items; never launch concurrent independent writers against one manifest. Write data authorization through `check-data-write`, never by editing policy fields.

Read `references/P0-DESIGN.md` only when gate/hash/evidence details matter.

### 7. Gates and rework

- `进入开发` authorizes the complete repository set in the Bundle, one dedicated fix branch per repo and Draft MRs. Request it only after the Bug Contract, scope, dependency order, plan and current baseline are explicit.
- `提测` authorizes merge to `dev`, push, CI/CD, dev deployment and one dev verification. It never authorizes production.
- `验收通过` authorizes one Feishu `RESOLVED` transition only when the run is at `AWAITING_ACCEPTANCE`; it never authorizes production or bypasses claim/session/evidence checks.
- If the human already moved Feishu to `RESOLVED` after the exact token, record `chat_exact` observation without issuing a duplicate transition. An approved `chat_exact` gate must never be downgraded to `policy_only` in the same run.
- Rework after failed acceptance within the same scope and risk keeps the existing claim and source analysis; redo diff/review/verification and request only `提测` again.
- Scope expansion, adding a repository to the Bundle, changing Bundle dependency order, data write, permission model change, production risk or L routing invalidates old assumptions and requires a fresh decision.

### 7.1 S-lite：S 级最小合规通道

S 级可以轻，但不能无痕。**S-lite 不是“跳过流程”，而是把同一套事实压缩到最小必填项**：

1. 仍必须创建 run：`init`（可 `--phase INTAKE`），保留 `claim_comment_ref`、`claim_operator`。
2. 仍必须写 `diagnosis.requirement_refs`（具体需规文件 + 条款/序号；不接受“按需规”）。
3. 仍必须记录：变更范围、commit SHA、验证证据、pipeline/deploy 结果。
4. 仍必须走 `提测` gate 与 `验收通过` gate；**不得直接 push 或直接关单**。
5. 验收阶段必须使用 `finalize-acceptance`，并按 §9 的硬规则完成 `transition_state` 与 `record-acceptance`。

S-lite 仅豁免：独立 review、非 happy-path 验证类别、完整 Bundle 集成验证（单仓时）。清单见 `references/S-LITE-CHECKLIST.md`。

### 8. Ship and failure handling

Before merge:

1. Refresh the latest `dev`; never merge an assumption from an old local ref.
2. Confirm the candidate can build and deploy against a green baseline. An unrelated red baseline may allow local development, but it never authorizes merge or `提测`; wait for a successful target-branch pipeline or block shipping with the owner and URL.
3. Merge/rebase only the authorized candidates and push `dev` in Bundle `ship_order`.
4. Track every repository's pipeline, image tag, deployed SHA and rollout; do not verify only the last repository. Prefer `scripts/pipeline-status.mjs` (requires `GITLAB_API_TOKEN` with api scope; otherwise fall back to the GitLab page) over manual screenshot polling.

Pipeline wait rule: follow only pipelines whose commit contains the authorized candidate (`git merge-base --is-ancestor <candidate> <pipeline-sha>`). Stop waiting for that repository at the first terminal success: pipeline success plus successful deploy/rollout, or a current live deployed SHA that contains the candidate. If the first pipeline is canceled or superseded, continue to the next candidate-containing pipeline and stop at its first terminal success. Do not switch to an unrestricted "latest dev pipeline" poll.

Record the terminal success in `ship_package.pipeline_id/pipeline_status/pipeline_url/deployed_sha`; later unrelated pipelines belong in the observation/summary, not in the blocking state.

A later pipeline on a newer commit is outside this run's stop condition. If it is still running, or fails with deploy skipped, do not block this run when the last successful deployed SHA still contains the candidate; record the observation and verify the current live deployment. Only a failure before any candidate-containing terminal success belongs to this run's pipeline failure path. For a Bundle, each repository independently needs one terminal success.

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

- Unrelated baseline/CI failure before candidate deployment: if disjoint, keep it as an open ship blocker while local development proceeds; if it blocks the affected path or the required verification, pause development. In both cases record owner/URL and do not increment the bug patch round. `提测` remains blocked until the target baseline is green.
- Later unrelated running/failed pipeline after candidate deployment: record as observation only; do not wait indefinitely and do not increment the patch round when live SHA still contains the candidate.
- Same environmental/runner failure twice with no progress: block and retry only after the condition changes.
- Code failure: fix, increment the patch round, and stop after 3 rounds.

### 9. Acceptance

At `AWAITING_ACCEPTANCE`:

- write the ship summary to Feishu with fix, tests, pipeline, image and rollout;
- list concise manual acceptance steps;
- wait for the human’s complete exact message `验收通过` (or `验收通过<auto_number>` when multiple active runs);
- reject “可以了”“没问题”“算修复了” and other natural-language inference;
- call `get_transitable_states` and `get_transition_required` for the current work item;
- run `finalize-acceptance --message 验收通过 --current-status <current Feishu status>`; this validates ship evidence and approves the acceptance gate in one step;
- call `transition_state` with the returned legal transition and satisfy required fields first;
- record `mode=chat_exact`, `approval_message=验收通过`, approval ref/session/machine, the Feishu transition result and acceptance evidence;
- advance the ledger to `RESOLVED` only after the Feishu transition succeeds.

**硬规则（2026-11-13，因 2342/2343 事故新增）：收到裸词 `验收通过` 后，禁止只汇报 pipeline/deploy 结果就结束回合。必须在同一回合内完成：`finalize-acceptance` → `transition_state` → `record-acceptance` → `advance RESOLVED` → 回写验收总结。任一步失败必须显式报告失败原因并保持 Feishu 状态不变，禁止声称“已关闭”。**

If the human moves Feishu manually without the exact chat token, keep the existing `policy_only` observation path and do not fabricate an acceptance gate. Only the claim comment, ship summary and final acceptance summary are required external comments.

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
- Unrelated red baseline that blocks the affected local path or full verification.
- A red target baseline when attempting `READY_SHIP`/`提测`; local development may already have proceeded if the failing path was disjoint.
- Required data write is outside policy/scope.
- L, schema, permission or production risk exceeds the lightweight flow. Cross-repo alone is not a blocker; an incomplete Bundle contract or integration verification is.
- Three code patch rounds have failed without a new hypothesis.

Report the work item, blocker, evidence already checked and exact human action needed. Leave business status unchanged unless an explicit legal transition exists.
