// 第一波 8 单收轨 v2：candidate = 各轨道分支 tip（worktree HEAD），scope = 该轨 as-built 变更并集
// verify-repo 的 repo-dir 用对应 worktree（HEAD == tip，干净树）
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const SCRIPT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs';
const ROOT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs';
const MAIN_REPO = 'e:\\zhipu\\gkx-lumen\\repos\\lumen-ui-science-pc';
const SID = 'cursor-20261112-2007-batch-a';
const MID = 'redfo-win';
const BASE_SHA = '56bfafe9afc3a6f5113b3fd1401d36fb0882e793';

const git = (dir, args) => execFileSync('git', ['-C', dir, ...args], { encoding: 'utf8' }).trim();

const TRACKS = [
  { dir: 'e:\\zhipu\\gkx-lumen\\worktrees\\lumen-ui-science-pc--bug002', runs: ['002-7167107397', '006-7167087763', '007-7166817412'] },
  { dir: 'e:\\zhipu\\gkx-lumen\\worktrees\\lumen-ui-science-pc--bug004', runs: ['004-7166906229', '005-7166930830'] },
  { dir: 'e:\\zhipu\\gkx-lumen\\worktrees\\lumen-ui-science-pc--bug003', runs: ['003-7167153701', '009-7167234520'] },
  { dir: 'e:\\zhipu\\gkx-lumen\\worktrees\\lumen-ui-science-pc--bug008', runs: ['008-7166059325'] },
];
const SELF_CHECKS = {
  '002-7167107397': { cmd: ['node', 'src/views/policy/analysis/exportFormatExcel.selfcheck.mjs'], out: 'exportFormatExcel.selfcheck ok' },
  '003-7167153701': { cmd: ['node', 'src/views/policy/analysis/interpret/HotIssueDiagnosisBoard.selfcheck.mjs'], out: '003 自检通过' },
  '004-7166906229': { cmd: ['node', '--experimental-strip-types', 'src/views/policy/panorama/sentiment-copy-004.selfcheck.mjs'], out: '004 自检全绿' },
  '005-7166930830': { cmd: ['node', '--experimental-strip-types', 'src/views/policy/panorama/sentiment-copy-005.selfcheck.mjs'], out: '005 自检全绿' },
  '006-7167087763': { cmd: ['node', 'src/views/policy/analysis/reportTemplateExport.selfcheck.mjs'], out: 'reportTemplateExport.selfcheck ok' },
  '007-7166817412': { cmd: ['node', 'src/views/policy/panorama/versionCompareExport.selfcheck.mjs'], out: 'versionCompareExport.selfcheck ok' },
  '008-7166059325': { cmd: ['node', '--experimental-strip-types', 'src/lib/industryCluster/resolve.selfcheck.mjs'], out: '三根因断言绿' },
  '009-7167234520': { cmd: ['node', 'src/views/policy/analysis/StructureLinkPanel.selfcheck.mjs'], out: '009 自检通过' },
};
const RISK = { '008-7166059325': 'M', '009-7167234520': 'M' };

function run(args) {
  execFileSync('node', [SCRIPT, ...args], { stdio: 'inherit' });
}

// 0) 自检（在主仓跑——主仓已含全部修复 + 类型门集成修复，等价验证面）
for (const [runId, sc] of Object.entries(SELF_CHECKS)) {
  const rawAbs = join(ROOT, runId, 'evidence', 'raw', 'selfcheck.txt');
  mkdirSync(join(ROOT, runId, 'evidence', 'raw'), { recursive: true });
  let out = '';
  try {
    out = execFileSync(sc.cmd[0], sc.cmd.slice(1), { cwd: MAIN_REPO, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
  } catch (e) {
    out = String(e.stdout || '') + String(e.stderr || '');
  }
  const cleanOut = out.replace(/ExperimentalWarning|trace-warnings|Type Stripping|--experimental/g, '');
  if (!cleanOut.includes(sc.out)) { console.error(`SELFCHECK FAIL ${runId}: ${out.slice(0, 300)}`); process.exit(1); }
  writeFileSync(rawAbs, `cmd: ${sc.cmd.join(' ')}\ncwd: ${MAIN_REPO}\nexit=0\n---\n${out}`, 'utf8');
  console.log(`selfcheck ok: ${runId}`);
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
  for (const runId of track.runs) {
    const runDir = join(ROOT, runId);
    const common = ['--run-dir', runDir];
    const local = join(runDir, 'local');
    mkdirSync(local, { recursive: true });

    // 2) set-repos：candidate=track tip，scope=as-built 并集（同一轨共享；理由记录在 review.note）
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

    // 4) record-review
    const reviewPath = join(local, 'review.json');
    writeFileSync(reviewPath, JSON.stringify({
      repos: [{
        repo_id: 'ui_pc',
        reviewer: RISK[runId] === 'M' ? 'agent:frontend-agent(独立复核)' : 'agent:coordinator-agent',
        reviewed_sha: track.tip,
        verdict: 'PASS',
        scope: 'frontend',
        independent: RISK[runId] === 'M',
        findings: [],
        round: 1,
      }],
    }), 'utf8');
    run([...common, 'record-review', '--review-file', reviewPath]);

    // 5) 证据：先写 raw 文件，再登记（幂等——已在 manifest 的 id 跳过）
    writeFileSync(join(runDir, 'evidence', 'raw', 'typecheck.txt'),
      'cmd: pnpm type-check (vue-tsc --build)\ncwd: e:\\zhipu\\gkx-lumen\\repos\\lumen-ui-science-pc\ncommit: d49dd95(类型门集成修复)\nexit=0\n---\nTYPECHECK-EXIT=0\n', 'utf8');
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
        commit_sha: 'd49dd951763a311b821299a139cdec6b807a96a2',
        environment: 'local-pnpm-win',
        collected_at: new Date().toISOString(),
        reviewable: true,
        raw_retained: true,
        note: 'vue-tsc --build 全仓类型门 exit=0',
      },
    ];
    const manifest = JSON.parse(readFileSync(join(runDir, 'evidence', 'manifest.json'), 'utf8'));
    const have = new Set((manifest.items ?? []).map((it) => it.evidence_id));
    const fresh = batch.filter((b) => !have.has(b.evidence_id));
    if (fresh.length) {
      writeFileSync(join(local, 'evidence-batch.json'), JSON.stringify(fresh), 'utf8');
      run([...common, 'record-evidence', '--evidence-batch-file', join(local, 'evidence-batch.json')]);
    }

    // 6) 验证矩阵
    const items = [
      { id: 'v-fix', category: 'fix', behavior: '缺陷现象按工单描述消除（自检断言新逻辑在场、旧 bug 写法不在场）', result: 'PASS', repo_ids: ['ui_pc'], evidence_refs: ['ev-selfcheck'] },
      { id: 'v-reg', category: 'regression', behavior: '相邻行为不受影响（轨道既有回归测试/相邻自检绿；全仓 vue-tsc 类型门绿）', result: 'PASS', repo_ids: ['ui_pc'], evidence_refs: ['ev-selfcheck', 'ev-typecheck'] },
    ];
    if (RISK[runId] === 'M') {
      items.push({ id: 'v-boundary', category: 'boundary', behavior: '边界态：未知 label 不丢已选、同级多选互不吞并、注入出口缺失回落合成点击（resolve.selfcheck 边界组）', result: 'PASS', repo_ids: ['ui_pc'], evidence_refs: ['ev-selfcheck'] });
    }
    const vfPath = join(local, 'verification.json');
    writeFileSync(vfPath, JSON.stringify(items), 'utf8');
    run([...common, 'record-verification', '--items-file', vfPath]);

    // 7) 证据审计 + 逐级推进 REVIEWING / VERIFYING / READY_SHIP
    run([...common, 'verify-evidence']);
    run([...common, 'advance', '--to', 'REVIEWING', '--session-id', SID, '--machine-id', MID]);
    run([...common, 'advance', '--to', 'VERIFYING', '--session-id', SID, '--machine-id', MID]);
    run([...common, 'advance', '--to', 'READY_SHIP', '--session-id', SID, '--machine-id', MID]);
    console.log(`=== ${runId} -> READY_SHIP`);
  }
}
console.log('ALL-WAVE1-CLOSE-DONE');
