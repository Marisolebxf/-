#!/usr/bin/env node
/**
 * Read-only GitLab pipeline helper for bugfix runs.
 *
 * Why: manual browser/AX checks are slow and brittle. This script reads the
 * repository's origin remote, calls the GitLab API, and prints the pipeline
 * terminal state, SHA and deploy jobs.
 *
 * Auth: uses `GITLAB_API_TOKEN` / `GITLAB_TOKEN` when present; otherwise tries
 * the password embedded in the origin remote (deploy tokens may not have API
 * access). Never prints the token.
 *
 * Usage:
 *   node pipeline-status.mjs --repo-dir <path> [--ref dev] [--sha <sha>] [--pipeline-id <id>] [--json]
 */
import { execFileSync } from 'node:child_process';
import { parseArgs } from 'node:util';

const { values } = parseArgs({
  options: {
    'repo-dir': { type: 'string' },
    ref: { type: 'string', default: 'dev' },
    sha: { type: 'string' },
    'pipeline-id': { type: 'string' },
    limit: { type: 'string', default: '5' },
    json: { type: 'boolean', default: false },
    help: { type: 'boolean', short: 'h' },
  },
});

if (values.help || !values['repo-dir']) {
  process.stdout.write(`Usage: node pipeline-status.mjs --repo-dir <path> [options]\n\nOptions:\n  --ref <branch>          default: dev\n  --sha <commit>          filter pipelines by commit SHA\n  --pipeline-id <id>      read one pipeline\n  --limit <n>             list size, default 5\n  --json                  machine-readable output\n\nAuth: GITLAB_API_TOKEN / GITLAB_TOKEN, or origin remote credentials.\n`);
  process.exit(values.help ? 0 : 2);
}

function git(args) {
  return execFileSync('git', ['-C', values['repo-dir'], ...args], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim();
}

function parseRemote(urlText) {
  const url = new URL(urlText);
  const pathname = url.pathname.replace(/^\//, '').replace(/\.git$/, '');
  return {
    host: url.hostname,
    project: pathname,
    username: decodeURIComponent(url.username || ''),
    password: decodeURIComponent(url.password || ''),
  };
}

const remote = parseRemote(git(['config', '--get', 'remote.origin.url']));
const token = process.env.GITLAB_API_TOKEN || process.env.GITLAB_TOKEN || remote.password;
const encodedProject = encodeURIComponent(remote.project);
const base = `https://${remote.host}/api/v4/projects/${encodedProject}`;

async function getJson(path) {
  const headers = { Accept: 'application/json' };
  if (token) headers['PRIVATE-TOKEN'] = token;
  const response = await fetch(`${base}${path}`, { headers });
  if (!response.ok) {
    const hint = response.status === 401 || response.status === 403 || response.status === 404
      ? '\nGitLab API rejected the credential. Set GITLAB_API_TOKEN with api scope.'
      : '';
    throw new Error(`GitLab API ${response.status} ${response.statusText}${hint}`);
  }
  return response.json();
}

function localContains(sha) {
  if (!values.sha) return null;
  try {
    git(['cat-file', '-e', `${values.sha}^{commit}`]);
  } catch {
    return 'unknown';
  }
  try {
    git(['merge-base', '--is-ancestor', values.sha, sha]);
    return true;
  } catch {
    return false;
  }
}

async function summarize(pipelineId) {
  const pipeline = await getJson(`/pipelines/${pipelineId}`);
  const jobs = await getJson(`/pipelines/${pipelineId}/jobs?per_page=100`);
  const jobSummary = jobs.map((job) => ({ name: job.name, stage: job.stage, status: job.status }));
  const deployJobs = jobSummary.filter((job) => /deploy|rollout/i.test(`${job.stage} ${job.name}`));
  return {
    id: pipeline.id,
    iid: pipeline.iid,
    sha: pipeline.sha,
    ref: pipeline.ref,
    status: pipeline.status,
    source: pipeline.source,
    web_url: pipeline.web_url,
    created_at: pipeline.created_at,
    updated_at: pipeline.updated_at,
    contains_candidate: localContains(pipeline.sha),
    jobs: jobSummary,
    deploy_jobs: deployJobs,
  };
}

let result;
if (values['pipeline-id']) {
  result = await summarize(values['pipeline-id']);
} else {
  const limit = Math.max(1, Math.min(100, Number(values.limit) || 5));
  const params = new URLSearchParams({ ref: values.ref, per_page: String(limit), order_by: 'id', sort: 'desc' });
  if (values.sha) params.set('sha', values.sha);
  const pipelines = await getJson(`/pipelines?${params.toString()}`);
  result = await Promise.all(pipelines.map((pipeline) => summarize(pipeline.id)));
}

if (values.json) {
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
} else {
  const rows = Array.isArray(result) ? result : [result];
  for (const row of rows) {
    process.stdout.write(`#${row.id} ${row.status} ${row.ref} ${row.sha} contains_candidate=${row.contains_candidate}\n`);
    for (const job of row.deploy_jobs) process.stdout.write(`  deploy: ${job.name} (${job.stage}) ${job.status}\n`);
    process.stdout.write(`  ${row.web_url}\n`);
  }
}
