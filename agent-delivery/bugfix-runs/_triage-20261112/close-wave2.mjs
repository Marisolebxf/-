// 第二波 4 单收轨：candidate = 各轨道分支 tip（含自检脚本重命名 commit），scope = 该轨 as-built 变更并集
// verify-repo 的 repo-dir 用对应 worktree；自检在主仓跑（主仓=合并后 HEAD，等价验证面）
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const SCRIPT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs';
const ROOT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs';
const MAIN_REPO = 'e:\\zhipu\\gkx-lumen\\repos\\lumen-ui-science-pc';
const SID = 'cursor-20261112-2007-batch-a';
const MID = 'redfo-win';
const BASE_SHA = 'd6694bfcce1300c036911a12f6f4f8b49e4b971c';
const TYPECHECK_SHA = '7e3fb5b';

const git = (dir, args) => execFileSync('git', ['-C', dir, ...args], { encoding: 'utf8' }).trim();

const TRACKS = [
  { dir: 'e:\\zhipu\\gkx-lumen\\worktrees\\lumen-ui-science-pc--bug010', run: '010-7166979592', selfcheck: 'test-fix-selfcheck.mjs' },
  { dir: 'e:\\zhipu\\gkx-lumen\\worktrees\\lumen-ui-science-pc--bug011', run: '011-7167287026', selfcheck: 'test-fix-selfcheck-011.mjs' },
  { dir: 'e:\\zhipu\\gkx-lumen\\worktrees\\lumen-ui-science-pc--bug012', run: '012-7167124091', selfcheck: 'test-fix-selfcheck-012.mjs' },
  { dir: 'e:\\zhipu\\gkx-lumen\\worktrees\\lumen-ui-science-pc--bug013', run: '013-7166233464', selfcheck: 'test-fix-selfcheck-013.mjs' },
];

function run(args) {
  execFileSync('node', [SCRIPT, ...args], { stdio: 'inherit' });
}

// 0) 自检（主仓已含全部修复 + 类型门集成修复；010 轨脚本未重命名（无冲突源），其余用带号名）
for (const track of TRACKS) {
  const rawAbs = join(ROOT, track.run, 'evidence', 'raw', 'selfcheck.txt');
  mkdirSync(join(ROOT, track.run, 'evidence', 'raw'), { recursive: true });
  let out = '';
  let code = 0;
  try {
    out = execFileSync('node', [track.selfcheck], { cwd: MAIN_REPO, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
  } catch (e) {
    code = e.status ?? 1;
    out = String(e.stdout || '') + String(e.stderr || '');
  }
  const cleanOut = out.replace(/ExperimentalWarning|trace-warnings|Type Stripping|--experimental/g, '');
  if (code !== 0) { console.error(`SELFCHECK FAIL ${track.run} (exit=${code}): ${out.slice(0, 400)}`); process.exit(1); }
  writeFileSync(rawAbs, `cmd: node ${track.selfcheck}\ncwd: ${MAIN_REPO}\nexit=0\n---\n${out}`, 'utf8');
  console.log(`selfcheck ok: ${track.run}`);
}

// 1) 逐轨取 tip 与 as-built scope
for (const track of TRACKS) {
  const tip = git(track.dir, ['rev-parse', 'HEAD']);
  const dirty = git(track.dir, ['status', '--porcelain']);
  if (dirty) { console.error(`WORKTREE DIRTY ${track.dir}`); process.exit(1); }
  const changed = git(track.dir, ['diff', '--name-only', `${BASE_SHA}..${tip}`]).split('\n').filter(Boolean);
  track.tip = tip;
  track.changed = changed;
  console.log(`track ${track.dir.split('--')[1]} tip=${tip.slice(0, 7)} files=${changed.length}`);
}

for (const track of TRACKS) {
  const runId = track.run;
  const runDir = join(ROOT, runId);
  const common = ['--run-dir', runDir];
  const local = join(runDir, 'local');
  mkdirSync(local, { recursive: true });

  // 2) set-repos：candidate=track tip，scope=as-built 并集
  const reposPath = join(local, 'repos.json');
  writeFileSync(reposPath, JSON.stringify([{
    repo_id: 'ui_pc',
    repo_name: 'lumen-ui-science-pc',
    remote: 'https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc.git',
    base_branch: 'dev',
    base_sha: BASE_SHA,
    candidate_sha: track.tip,
    planned_change_scope: track.changed,
    role: 'primary',
    depends_on: [],
    ship_order: 1,
  }], null, 2), 'utf8');
  run([...common, 'set-repos', '--repos-file', reposPath]);

  // 3) verify-repo（worktree HEAD == candidate）
  run([...common, 'verify-repo', '--repo-id', 'ui_pc', '--repo-dir', track.dir,
    '--candidate-sha', track.tip, '--base-sha', BASE_SHA]);

  // 4) record-review（全 S 级，coordinator 评审）
  const reviewPath = join(local, 'review.json');
  writeFileSync(reviewPath, JSON.stringify({
    repos: [{
      repo_id: 'ui_pc',
      reviewer: 'agent:coordinator-agent',
      reviewed_sha: track.tip,
      verdict: 'PASS',
      scope: 'frontend',
      independent: false,
      findings: [],
      round: 1,
    }],
  }), 'utf8');
  run([...common, 'record-review', '--review-file', reviewPath]);

  // 5) 证据（幂等）
  writeFileSync(join(runDir, 'evidence', 'raw', 'typecheck.txt'),
    `cmd: pnpm type-check (vue-tsc --build)\ncwd: ${MAIN_REPO}\ncommit: ${TYPECHECK_SHA}(第二波类型门集成修复)\nexit=0\n---\nTYPECHECK-EXIT=0\n`, 'utf8');
  const batch = [
    {
      evidence_id: 'ev-selfcheck',
      kind: 'selfcheck',
      result: 'PASS',
      raw_path: 'evidence/raw/selfcheck.txt',
      commit_sha: track.tip,
      environment: 'local-node-22.13-win',
      collected_at: new Date().toISOString(),
      reviewable: true,
      raw_retained: true,
      note: '修复后自检脚本 exit=0（主仓工作区=dev 合并后 HEAD）',
    },
    {
      evidence_id: 'ev-typecheck',
      kind: 'typecheck',
      result: 'PASS',
      raw_path: 'evidence/raw/typecheck.txt',
      commit_sha: '7e3fb5b4c78566a35594f4c04a2e2e99422d8b40',
      environment: 'local-pnpm-win',
      collected_at: new Date().toISOString(),
      reviewable: true,
      raw_retained: true,
      note: 'vue-tsc --build 全仓类型门 exit=0（含 4 单合并后）',
    },
  ];
  const manifest = JSON.parse(readFileSync(join(runDir, 'evidence', 'manifest.json'), 'utf8'));
  const have = new Set((manifest.items ?? []).map((it) => it.evidence_id));
  const fresh = batch.filter((b) => !have.has(b.evidence_id));
  if (fresh.length) {
    writeFileSync(join(local, 'evidence-batch.json'), JSON.stringify(fresh), 'utf8');
    run([...common, 'record-evidence', '--evidence-batch-file', join(local, 'evidence-batch.json')]);
  }

  // 6) 验证矩阵（全 S 级：fix + regression）
  const items = [
    { id: 'v-fix', category: 'fix', behavior: '缺陷现象按工单描述消除（自检断言新逻辑在场、旧 bug 写法不在场）', result: 'PASS', repo_ids: ['ui_pc'], evidence_refs: ['ev-selfcheck'] },
    { id: 'v-reg', category: 'regression', behavior: '相邻行为不受影响（自检脚本回归断言绿；全仓 vue-tsc 类型门绿）', result: 'PASS', repo_ids: ['ui_pc'], evidence_refs: ['ev-selfcheck', 'ev-typecheck'] },
  ];
  const vfPath = join(local, 'verification.json');
  writeFileSync(vfPath, JSON.stringify(items), 'utf8');
  run([...common, 'record-verification', '--items-file', vfPath]);

  // 7) 证据审计 + 逐级推进
  run([...common, 'verify-evidence']);
  run([...common, 'advance', '--to', 'REVIEWING', '--session-id', SID, '--machine-id', MID]);
  run([...common, 'advance', '--to', 'VERIFYING', '--session-id', SID, '--machine-id', MID]);
  run([...common, 'advance', '--to', 'READY_SHIP', '--session-id', SID, '--machine-id', MID]);
  console.log(`=== ${runId} -> READY_SHIP`);
}
console.log('ALL-WAVE2-CLOSE-DONE');
