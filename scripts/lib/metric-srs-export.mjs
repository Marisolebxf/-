/**
 * 跑 registry/export「指标需求来源」xlsx（注册表全量 + srs_refs）。
 * 不写 seed / 矩阵 / metric-srs-map.yaml。MCP 工具 metric-srs-export 走这里。
 * 与飞书进度表分文件，禁止往进度表加列。
 */
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { ORCH_ROOT } from './metric-registry-lib.mjs';

export const SRS_EXPORT_SCRIPT = path.join(
  ORCH_ROOT,
  'agent-delivery',
  'metrics',
  'registry',
  'export',
  'export_metric_srs_board.py',
);

function pythonLauncher() {
  const candidates = [
    ['python', []],
    ['py', ['-3']],
    ['python3', []],
  ];
  for (const [cmd, prefix] of candidates) {
    const probe = spawnSync(cmd, [...prefix, '--version'], {
      encoding: 'utf8',
      windowsHide: true,
      timeout: 8000,
    });
    if (probe.status === 0) return { cmd, prefix };
  }
  return null;
}

export function exportMetricSrsBoard() {
  if (!fs.existsSync(SRS_EXPORT_SCRIPT)) {
    return { ok: false, error: `script missing: ${SRS_EXPORT_SCRIPT}` };
  }
  const py = pythonLauncher();
  if (!py) {
    return { ok: false, error: 'python not found (tried python / py -3 / python3)' };
  }
  const r = spawnSync(py.cmd, [...py.prefix, SRS_EXPORT_SCRIPT, '--json'], {
    encoding: 'utf8',
    cwd: ORCH_ROOT,
    timeout: 120000,
    windowsHide: true,
    env: { ...process.env, PYTHONIOENCODING: 'utf-8', PYTHONUTF8: '1' },
  });
  const stdout = (r.stdout || '').trim();
  const stderr = (r.stderr || '').trim();
  if (r.status !== 0) {
    return {
      ok: false,
      error: stderr || stdout || `python exit ${r.status}`,
      code: r.status,
    };
  }
  const line = stdout.split(/\r?\n/).filter(Boolean).pop() || '';
  try {
    const payload = JSON.parse(line);
    return payload?.ok ? payload : { ok: false, error: 'json missing ok', raw: payload };
  } catch {
    return { ok: false, error: 'stdout is not JSON', stdout: line.slice(0, 500) };
  }
}
