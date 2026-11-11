#!/usr/bin/env node
/**
 * Decide whether a concurrent remote update requires a second full local
 * type/build pass after merging into the candidate branch.
 *
 * This command is read-only except for the git commands it runs. Fetch first.
 */
import { execFileSync } from 'node:child_process';
import { parseArgs } from 'node:util';

const { values } = parseArgs({
  options: {
    'repo-dir': { type: 'string' },
    'candidate-ref': { type: 'string', default: 'HEAD' },
    'remote-ref': { type: 'string', default: 'origin/dev' },
    'remote-pipeline-status': { type: 'string', default: 'unknown' },
    'premerge-checks-passed': { type: 'boolean', default: false },
    json: { type: 'boolean', default: false },
    help: { type: 'boolean', short: 'h' },
  },
});

if (values.help || !values['repo-dir']) {
  process.stdout.write(`Usage: node revalidation-plan.mjs --repo-dir <path> [options]\n\nOptions:\n  --candidate-ref <ref>             default: HEAD\n  --remote-ref <ref>                default: origin/dev\n  --remote-pipeline-status <state>  success|failed|unknown\n  --premerge-checks-passed          full local checks already passed before merge\n  --json                            machine-readable output\n`);
  process.exit(values.help ? 0 : 2);
}

const repoDir = values['repo-dir'];
const candidateRef = values['candidate-ref'];
const remoteRef = values['remote-ref'];
const pipelineStatus = String(values['remote-pipeline-status']).toLowerCase();
if (!['success', 'failed', 'unknown'].includes(pipelineStatus)) {
  throw new Error('--remote-pipeline-status must be success, failed, or unknown');
}

function git(args) {
  return execFileSync('git', ['-C', repoDir, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
}

function lines(text) {
  return text ? text.split(/\r?\n/).filter(Boolean) : [];
}

function isSensitive(file) {
  const path = file.replace(/\\/g, '/');
  return [
    /^package\.json$/,
    /^package-lock\.json$/,
    /^pnpm-lock\.yaml$/,
    /^yarn\.lock$/,
    /^tsconfig(?:\..+)?\.json$/,
    /^vite\.config\./,
    /^\.gitlab-ci\.ya?ml$/,
    /^AGENTS\.md$/,
    /^src\/config\//,
    /^src\/api\//,
    /^src\/types\//,
    /^src\/stores\//,
    /^src\/router\//,
  ].some((pattern) => pattern.test(path));
}

const mergeBase = git(['merge-base', candidateRef, remoteRef]);
const candidateSha = git(['rev-parse', candidateRef]);
const remoteSha = git(['rev-parse', remoteRef]);
let candidateAlreadyInRemote = false;
try {
  git(['merge-base', '--is-ancestor', candidateRef, remoteRef]);
  candidateAlreadyInRemote = true;
} catch {
  candidateAlreadyInRemote = false;
}

const candidateFiles = lines(git(['diff', '--name-only', mergeBase, candidateRef]));
const remoteFiles = lines(git(['diff', '--name-only', mergeBase, remoteRef]));
const candidateSet = new Set(candidateFiles);
const overlappingFiles = remoteFiles.filter((file) => candidateSet.has(file));
const sensitiveRemoteFiles = remoteFiles.filter(isSensitive);

let decision;
let reasons = [];
if (candidateAlreadyInRemote) {
  decision = 'no_revalidation';
  reasons.push('candidate is already contained in the remote ref');
} else if (pipelineStatus === 'failed') {
  decision = 'block';
  reasons.push('remote baseline pipeline is failed');
} else if (!values['premerge-checks-passed']) {
  decision = 'full';
  reasons.push('pre-merge full local checks were not marked as passed');
} else if (overlappingFiles.length) {
  decision = 'full';
  reasons.push('remote changes overlap the candidate change set');
} else if (sensitiveRemoteFiles.length) {
  decision = 'full';
  reasons.push('remote changes touch shared dependency/config/type/API files');
} else if (pipelineStatus !== 'success') {
  decision = 'full';
  reasons.push('remote pipeline status is unknown; use full local validation');
} else {
  decision = 'targeted';
  reasons.push('remote baseline is green and its changes are disjoint from the candidate');
}

const checks = decision === 'full'
  ? ['git diff --check', 'targeted regression', 'type-check', 'build']
  : decision === 'targeted'
    ? ['git diff --check', 'targeted regression', 'push and rely on CI for full integration']
    : decision === 'block'
      ? ['stop and report remote baseline failure']
      : ['verify remote already contains the candidate'];

const result = {
  decision,
  reasons,
  candidate_ref: candidateRef,
  candidate_sha: candidateSha,
  remote_ref: remoteRef,
  remote_sha: remoteSha,
  merge_base: mergeBase,
  requires_merge: !candidateAlreadyInRemote,
  candidate_files: candidateFiles,
  remote_files: remoteFiles,
  overlapping_files: overlappingFiles,
  sensitive_remote_files: sensitiveRemoteFiles,
  post_merge_checks: checks,
};

if (values.json) {
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
} else {
  process.stdout.write(`decision=${decision}\n${reasons.map((reason) => `- ${reason}`).join('\n')}\n`);
  if (overlappingFiles.length) process.stdout.write(`overlap=${overlappingFiles.join(', ')}\n`);
  if (sensitiveRemoteFiles.length) process.stdout.write(`sensitive=${sensitiveRemoteFiles.join(', ')}\n`);
  process.stdout.write(`checks=${checks.join(' -> ')}\n`);
}
