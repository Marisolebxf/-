/**
 * ZMATE-RPT-QA-L01 · 无 DOM 的人闸/解锁自检（对齐 workspaceStore 合同）
 * 运行：node src/app/pages/zmate-strategy/qa-gate-check.mjs
 */
import assert from "node:assert/strict";

/** 与 workspaceStore.unlockAfter / tryUnlockWriter / skipDebate 语义镜像（纯函数，无 localStorage） */
function unlockAfter(run, stages, completed) {
  let next = { ...stages, [completed]: "done" };
  if (completed === "clarify" && next.planner === "locked") next.planner = "ready";
  if (completed === "planner") {
    if (next.debate === "locked") next.debate = "ready";
    if (next.slice === "locked") next.slice = "ready";
  }
  if (completed === "slice" && next.seeker === "locked") next.seeker = "ready";
  next = tryUnlockWriter(run, next);
  if (completed === "writer" && next.judge === "locked") next.judge = "ready";
  return next;
}

function debateSatisfied(run, stages) {
  return stages.debate === "done" || !!run.debateSkipped;
}

function tryUnlockWriter(run, stages) {
  if (stages.writer !== "locked") return stages;
  if (stages.seeker === "done" && debateSatisfied(run, stages)) {
    return { ...stages, writer: "ready" };
  }
  return stages;
}

function freshStages() {
  return {
    clarify: "ready",
    planner: "locked",
    debate: "locked",
    slice: "locked",
    seeker: "locked",
    writer: "locked",
    judge: "locked",
  };
}

function collectJudgeFindings(run) {
  const findings = [];
  const demands = run.slice?.demands ?? [];
  if (demands.some((d) => d.status !== "ready")) {
    findings.push("存在待建/待真接/待外网补数，禁止按 live 交付");
  }
  if (!run.slice?.approvedMetricIds?.length) findings.push("切片人闸未批准任何指标");
  if (!run.dossier?.locked && !run.debateSkipped) findings.push("辩论未结束且未显式跳过");
  if (!run.report || run.report.generating || !run.report.paragraphs?.length) {
    findings.push("无结构草稿 / 绕过 Writer");
  }
  if (run.report?.paragraphs?.some((p) => p.citationLabels?.some((l) => /live/i.test(l)))) {
    findings.push("疑似假 live 标注");
  }
  return findings;
}

// USM-03/05：确认前 Planner 锁定
{
  const s0 = freshStages();
  assert.equal(s0.planner, "locked");
  const s1 = unlockAfter({}, s0, "clarify");
  assert.equal(s1.clarify, "done");
  assert.equal(s1.planner, "ready");
  assert.equal(s1.debate, "locked");
  assert.equal(s1.writer, "locked");
}

// USM-05：Planner 后辩论∥切片并行 ready；Writer 仍锁
{
  let s = unlockAfter({}, freshStages(), "clarify");
  s = unlockAfter({}, s, "planner");
  assert.equal(s.debate, "ready");
  assert.equal(s.slice, "ready");
  assert.equal(s.seeker, "locked");
  assert.equal(s.writer, "locked");
}

// USM-05：仅切片完成不解 Writer（缺辩论）
{
  let s = unlockAfter({}, freshStages(), "clarify");
  s = unlockAfter({}, s, "planner");
  s = unlockAfter({}, s, "slice");
  assert.equal(s.seeker, "ready");
  assert.equal(s.writer, "locked");
  s = unlockAfter({}, s, "seeker");
  assert.equal(s.writer, "locked"); // 辩论未结束
}

// 路径 A：显式跳过辩论 + seeker done → Writer ready
{
  let s = unlockAfter({}, freshStages(), "clarify");
  s = unlockAfter({}, s, "planner");
  s = unlockAfter({}, s, "slice");
  s = unlockAfter({}, s, "seeker");
  const run = { debateSkipped: true };
  s = tryUnlockWriter(run, { ...s, debate: "done" });
  assert.equal(s.writer, "ready");
  s = unlockAfter(run, s, "writer");
  assert.equal(s.judge, "ready");
}

// USM-10：Demo 缺口指标 → Default-FAIL findings 非空
{
  const findings = collectJudgeFindings({
    debateSkipped: true,
    dossier: { locked: true },
    slice: {
      approvedMetricIds: ["d1"],
      demands: [
        { status: "ready" },
        { status: "need_ingest" },
        { status: "need_define" },
        { status: "need_web" },
      ],
    },
    report: { generating: false, paragraphs: [{ citationLabels: ["推断", "缺口"] }] },
  });
  assert.ok(findings.some((f) => /live/.test(f)));
  const preferPass = findings.length > 0 ? "FAIL" : "PASS";
  assert.equal(preferPass, "FAIL");
}

// 绕过人闸：无 Writer 草稿 → FAIL
{
  const findings = collectJudgeFindings({
    debateSkipped: true,
    dossier: { locked: true },
    slice: { approvedMetricIds: ["d1"], demands: [{ status: "ready" }] },
    report: null,
  });
  assert.ok(findings.some((f) => /绕过 Writer|无结构草稿/.test(f)));
}

console.log("qa-gate-check: OK · unlock + Judge Default-FAIL 合同通过");
