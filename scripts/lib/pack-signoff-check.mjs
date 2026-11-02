/**
 * 派单包签收闸门。ready_to_sign → done 写入前由 task-update-status 调用。
 * ponytail: 只认任务 ID 前缀；新派单包维度要改本文件的正则。
 * 运行：node scripts/lib/pack-signoff-check.mjs
 */
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const ORCH_ROOT = path.resolve(HERE, '..', '..');

const GDF_RE = /^GDF-(POLICY|ENT|CHAIN)-WORKPACK-/i;
const GRAPH_RE = /^KG-(ENT|CHAIN)-GRAPH-LOAD-/i;

export function packSignoffSpec(taskId) {
  const id = String(taskId || '');
  if (GDF_RE.test(id)) {
    return {
      kind: 'gdf',
      script: path.join(ORCH_ROOT, '.cursor/skills/gkx-gdf-ddl-signoff/scripts/check_gdf_ddl.py'),
      args: ['--task', id],
    };
  }
  if (GRAPH_RE.test(id)) {
    return {
      kind: 'graph',
      script: path.join(ORCH_ROOT, '.cursor/skills/gkx-graph-pack-signoff/scripts/check_graph_pack.py'),
      args: ['--task', id],
    };
  }
  return null;
}

export function runPackSignoff(taskId, opts = {}) {
  const spec = packSignoffSpec(taskId);
  if (!spec) return { ok: true, skipped: true };
  const r = spawnSync('python', [spec.script, ...spec.args], {
    cwd: opts.root || ORCH_ROOT,
    encoding: 'utf8',
    timeout: opts.timeout ?? 180000,
    env: process.env,
    windowsHide: true,
  });
  if (r.error) {
    const reason = r.error.code === 'ETIMEDOUT'
      ? '派单包自检超时，未签收'
      : `派单包自检没跑成，未签收：${r.error.message}`;
    return { ok: false, kind: spec.kind, reason };
  }
  if (r.status === 0) return { ok: true, kind: spec.kind };
  const text = `${r.stdout || ''}\n${r.stderr || ''}`.trim().slice(0, 4000);
  return { ok: false, kind: spec.kind, reason: text || `派单包自检退出码 ${r.status}` };
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const assert = (cond, msg) => {
    if (!cond) {
      console.error(msg);
      process.exit(1);
    }
  };
  assert(packSignoffSpec('GDF-POLICY-WORKPACK-V2-L01')?.kind === 'gdf', 'GDF 派单包应触发');
  assert(packSignoffSpec('KG-CHAIN-GRAPH-LOAD-L01')?.kind === 'graph', 'Graph 派单包应触发');
  assert(packSignoffSpec('FE-POL-01B') === null, '其他任务不触发');
  const graph = runPackSignoff('KG-ENT-GRAPH-LOAD-L01');
  assert(graph.ok === true && graph.kind === 'graph', graph.reason || 'Graph 自检应通过');
  console.log('pack-signoff-check ok');
}
