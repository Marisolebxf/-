# ENT-OPS Product Definition Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create and validate the E-37 maintenance-management IA, TRACE, USM, and Wireframe as a reviewable Track-MS core product package.

**Architecture:** Treat the Bid section §1.1.1.2.4.5.6.3～3.3 as the only original requirement source and the approved design specification as the source of current human decisions. Keep the four artifacts mutually consistent around one workflow-first medium-screen CMS, six content types, three separated roles, a four-stage governance flow, and six named Frames. Validate trace coverage and review mounts mechanically before handoff.

**Tech Stack:** Markdown, YAML, Ruby standard-library YAML parser, Git.

---

## File map

- Create `agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/IA-ENT-OPS.md`: module boundary, roles, navigation, route/state ownership, and cross-module boundaries.
- Create `agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml`: machine-readable authority inventory, story-to-source mapping, decisions, Frames, states, review mounts, exclusions, and coverage counts.
- Create `agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/USM-ENT-OPS.md`: role-based stories, primary and abnormal walkthroughs, and testable acceptance scenarios.
- Create `agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/Wireframe-ENT-OPS.md`: six Frame specifications, field contracts, interactions, states, responsive rules, and machine-readable review trace contract.
- Read-only input `docs/superpowers/specs/2026-07-22-ent-ops-product-package-design.md`: approved product decisions.
- Read-only input `agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md`: original requirement authority.

### Task 1: Create IA-ENT-OPS

**Files:**
- Create: `agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/IA-ENT-OPS.md`
- Reference: `agent-delivery/templates/ia-template.md`
- Reference: `docs/superpowers/specs/2026-07-22-ent-ops-product-package-design.md`

- [ ] **Step 1: Verify the target does not already contain an unreviewed IA**

Run:

```bash
test ! -e 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/IA-ENT-OPS.md'
```

Expected: exit 0. If the file exists, stop and review only the exact current ENT-OPS four-pack before editing.

- [ ] **Step 2: Create the IA with the frozen boundary**

Write these sections with complete content:

```text
1. 模块边界
2. 原始需求与批准解释分层
3. 用户入口与产品角色
4. 信息架构
5. 页面 / 节点职责
6. 路由与状态保留
7. 跨模块边界
8. 与 Bid 差异说明
9. 来源清单与 IA 自检
```

The IA tree must contain `内容工作台`, six content-type entries, `审核中心`, `发布中心`, and `版本与审计`. Use `/enterprise/content-management` as the root route. Record content editor, content reviewer, and release administrator as approved product interpretations; do not call permissions documents original sources.

- [ ] **Step 3: Verify IA coverage and forbidden scope**

Run:

```bash
rg -n '企业基础档案|成长轨迹|重点企业全景|能力榜单|明星企业介绍|深圳企业介绍|审核中心|发布中心|版本与审计' 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/IA-ENT-OPS.md'
! rg -n '自动计算.*技术力|自动计算.*商业力|修改工商|修改资质' 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/IA-ENT-OPS.md'
```

Expected: all required nodes are found; forbidden scope search returns no match.

- [ ] **Step 4: Commit the IA**

```bash
git add -- 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/IA-ENT-OPS.md'
git commit -m 'docs(product): add ENT-OPS information architecture'
```

### Task 2: Create TRACE-ENT-OPS

**Files:**
- Create: `agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml`
- Reference: `agent-delivery/产品定义评审规程.md` §3.2
- Reference: `agent-delivery/data-lineage-policy.md`

- [ ] **Step 1: Define module and authority metadata**

Create a YAML document whose `module` contains:

```yaml
id: ENT-OPS
name: 维护管理
requirement_ids: [E-37]
task_id: ENT-MOD-OPS-PACK-L01
version: "1.0"
updated_at: "2026-07-22"
status: local_review
owner_experience: human:高颖
owner_semantic: human:何老师
owner_compliance: human:郭万迎
delivery_track: Track-MS
delivery_stage: v1_hifi_round1
screen_tier: medium
responsive_tiers: []
planned_tier: null
root_route: /enterprise/content-management
```

Add separate `original_requirement_sources`, `approved_decision_sources`, and `derived_definition_sources`. The original list must contain only the Bid file and §1.1.1.2.4.5.6.3～3.3. The approved-decision list contains the user-confirmed 2026-07-22 design specification. The derived list contains only the four current ENT-OPS artifacts; the design specification is not classified as original or derived product authority.

- [ ] **Step 2: Encode direct requirements and approved interpretations**

Create one `direct_requirement` record for E-37 with six named capabilities and the exact Bid anchors. Create `product_interpretation` records for three-role separation, master-data read-only partition, manual leaderboard curation, workflow-first IA, immutable published versions, and audited high-risk operations. Set `product_enhancements: []` and `approved_scope_changes: []`.

- [ ] **Step 3: Encode stories and landing points**

Use these stable story IDs:

```text
US-ENT-OPS-01 管理统一内容待办
US-ENT-OPS-02 编辑六类企业发展内容
US-ENT-OPS-03 审核内容与版本差异
US-ENT-OPS-04 发布或退回已审核内容
US-ENT-OPS-05 下线或回滚已发布版本
US-ENT-OPS-06 处理并发编辑冲突
US-ENT-OPS-07 发起企业主数据纠错
```

Every story must include role, source relation, acceptance IDs, route, Frame IDs, states, prohibited behaviors, compliance refs, and review mount IDs. Use F-OPS-01 through F-OPS-06; US-ENT-OPS-07 lands in F-OPS-02.

- [ ] **Step 4: Encode conditional gates and coverage**

Set:

```yaml
metrics:
  applicability: N/A
  reason: 本模块维护 CMS 内容与人工策展顺序，不产生统计字段或算法指标
  required: 0
  mapped: 0
open_questions: []
blocking_gaps: []
coverage_summary:
  leaves_required: 1
  leaves_mapped: 1
  direct_requirements: 1
  product_interpretations: 6
  product_enhancements: 0
  stories_required: 7
  stories_mapped: 7
  frames_required: 6
  frames_mapped: 6
  metrics_required: 0
  metrics_mapped: 0
```

- [ ] **Step 5: Parse and assert TRACE invariants**

Run:

```bash
ruby -ryaml -e '
p="agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml"
d=YAML.load_file(p)
m=d.fetch("module")
c=d.fetch("coverage_summary")
abort unless m.fetch("requirement_ids")==["E-37"]
abort unless m.fetch("delivery_track")=="Track-MS"
abort unless m.fetch("delivery_stage")=="v1_hifi_round1"
abort unless m.fetch("screen_tier")=="medium"
abort unless c.fetch("leaves_required")==1 && c.fetch("leaves_mapped")==1
abort unless c.fetch("stories_required")==7 && c.fetch("stories_mapped")==7
abort unless c.fetch("frames_required")==6 && c.fetch("frames_mapped")==6
abort unless c.fetch("metrics_required")==0 && c.fetch("metrics_mapped")==0
puts "TRACE invariants OK"
'
```

Expected: `TRACE invariants OK`.

- [ ] **Step 6: Commit TRACE**

```bash
git add -- 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml'
git commit -m 'docs(product): add ENT-OPS trace matrix'
```

### Task 3: Create USM-ENT-OPS

**Files:**
- Create: `agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/USM-ENT-OPS.md`
- Reference: `agent-delivery/templates/usm-template.md`

- [ ] **Step 1: Write the role and story map**

Use the three approved product roles and the exact seven TRACE story IDs. Each story must be written as As/Want/So that, cite its source relation, and name its IA node and Frame landing point.

- [ ] **Step 2: Write primary walkthroughs**

Include three complete primary flows:

```text
编辑：进入待我处理 → 选择或新建内容 → 查看只读主数据 → 编辑 CMS 载荷 → 预览 → 保存草稿 → 提交审核
审核：进入审核中心 → 查看内容与版本差异 → 核对来源说明 → 通过或带原因退回
发布：进入发布中心 → 查看影响摘要 → 填写原因与生效时间 → 二次确认 → 发布
```

- [ ] **Step 3: Write abnormal walkthroughs**

Cover empty list, load failure, no permission, save failure, review return, publish failure, concurrent modification, master-data correction, and rollback. State explicitly that user input is preserved on failures and that rollback creates a new published version.

- [ ] **Step 4: Write testable acceptance scenarios**

Create acceptance IDs `ENT-OPS-USM-01` through `ENT-OPS-USM-14`. At minimum verify six-type coverage, role separation, master-data read-only behavior, manual-ranking disclosure, immutable published versions, audit evidence, all failure states, and business-mode absence of review markers.

- [ ] **Step 5: Verify story and acceptance counts**

Run:

```bash
test "$(rg -o 'US-ENT-OPS-[0-9]{2}' 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/USM-ENT-OPS.md' | sort -u | wc -l | tr -d ' ')" = 7
test "$(rg -o 'ENT-OPS-USM-[0-9]{2}' 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/USM-ENT-OPS.md' | sort -u | wc -l | tr -d ' ')" = 14
```

Expected: both commands exit 0.

- [ ] **Step 6: Commit USM**

```bash
git add -- 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/USM-ENT-OPS.md'
git commit -m 'docs(product): add ENT-OPS user story map'
```

### Task 4: Create Wireframe-ENT-OPS

**Files:**
- Create: `agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/Wireframe-ENT-OPS.md`
- Reference: `agent-delivery/templates/wireframe-template.md`
- Reference: `agent-delivery/data-lineage-policy.md`

- [ ] **Step 1: Write the six-Frame inventory**

Define F-OPS-01 内容工作台, F-OPS-02 内容编辑器, F-OPS-03 审核详情, F-OPS-04 发布确认, F-OPS-05 版本与审计, and F-OPS-06 冲突处理. Each inventory row must include trigger, purpose, story IDs, source relation, route/state, and `review_mounts`.

- [ ] **Step 2: Specify every Frame**

For each Frame include an ASCII wireframe, six-column field table (`名称 / 类型 / 来源 / 必填 / 示例 / metric_id`), interaction table, prohibited behavior table, and default/loading/empty/error/no-permission states plus applicable operation states. Use `—（明细字段）` for `metric_id`; do not invent statistical metrics.

- [ ] **Step 3: Add the review trace contract**

Define exactly these unique mounts:

```text
ENT-OPS-F01-WORKBENCH-TITLE
ENT-OPS-F02-EDITOR-TITLE
ENT-OPS-F02-MASTER-DATA-BOUNDARY
ENT-OPS-F03-REVIEW-TITLE
ENT-OPS-F04-PUBLISH-RISK
ENT-OPS-F05-VERSION-AUDIT-TITLE
ENT-OPS-F06-CONFLICT-TITLE
```

Every contract entry must contain `mount_id`, `frame_id`, `host_label`, `marker_type`, `source_relation`, `trace_refs`, `required_payload`, `review_mode: present`, and `business_mode: absent`. List prohibited mount positions: input labels, operation buttons, table cells, workflow badges, and confirmation primary buttons.

- [ ] **Step 4: Add responsive and exclusion rules**

Declare `screen_tier: medium`, no LARGE/SMALL entry, and the under-1280px preview-drawer behavior. Repeat the module exclusions for main-data writes, algorithm scoring, automatic ranking, analytics, recommendation, export, user/role management, and physical audit deletion.

- [ ] **Step 5: Verify Frame and mount uniqueness**

Run:

```bash
test "$(rg -o 'F-OPS-[0-9]{2}' 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/Wireframe-ENT-OPS.md' | sort -u | wc -l | tr -d ' ')" = 6
mounts=$(rg -o 'ENT-OPS-F[0-9]{2}-[A-Z0-9-]+' 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/Wireframe-ENT-OPS.md')
test "$(printf '%s\n' "$mounts" | sort -u | wc -l | tr -d ' ')" = 7
```

Expected: six unique Frames and seven unique mounts.

- [ ] **Step 6: Commit Wireframe**

```bash
git add -- 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/Wireframe-ENT-OPS.md'
git commit -m 'docs(product): add ENT-OPS wireframe contract'
```

### Task 5: Cross-document validation and handoff

**Files:**
- Verify: all four files under `agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/`

- [ ] **Step 1: Check file set and formatting**

Run:

```bash
test "$(find 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理' -maxdepth 1 -type f | wc -l | tr -d ' ')" = 4
git diff --check -- 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理'
```

Expected: exactly four files and no whitespace errors.

- [ ] **Step 2: Check cross-document identifiers**

Run:

```bash
for id in 01 02 03 04 05 06 07; do
  rg -q "US-ENT-OPS-$id" 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml'
  rg -q "US-ENT-OPS-$id" 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/USM-ENT-OPS.md'
done
for id in 01 02 03 04 05 06; do
  rg -q "F-OPS-$id" 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml'
  rg -q "F-OPS-$id" 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/Wireframe-ENT-OPS.md'
done
```

Expected: every story and Frame resolves in both required artifacts.

- [ ] **Step 3: Check authority inventories and conditional gates**

Run:

```bash
rg -q 'original_requirement_sources' 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml'
rg -q 'derived_definition_sources' 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml'
rg -q '§1.1.1.2.4.5.6.3' 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml'
rg -q 'applicability: N/A' 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml'
! rg -n 'delivery_tier:|PDR.*已通过|门 1.*通过' 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理'
```

Expected: typed inventories and N/A gate exist; no acceptance conclusion is declared.

- [ ] **Step 4: Review intended diff only**

Run:

```bash
git status --short -- 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理'
git diff --stat -- 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理'
```

Expected: only the four ENT-OPS files appear in the scoped output; unrelated working-tree changes remain untouched.

- [ ] **Step 5: Commit any consistency-only corrections**

If cross-document validation required corrections, stage only the four package files and commit:

```bash
git add -- 'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/IA-ENT-OPS.md' \
  'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml' \
  'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/USM-ENT-OPS.md' \
  'agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/Wireframe-ENT-OPS.md'
git commit -m 'docs(product): align ENT-OPS package contracts'
```

If no correction was required, do not create an empty commit.

- [ ] **Step 6: Report package readiness**

Report `核心产品包可评审`, not PDR passed. Include `leaves_mapped=1/1`, `stories_mapped=7/7`, `frames_mapped=6/6`, `metrics=N/A (0/0)`, `open_questions=[]`, the five required reviewers, and the four artifact paths.
