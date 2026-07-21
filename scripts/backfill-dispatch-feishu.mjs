#!/usr/bin/env node
/**
 * Backfill Feishu 派单门控 / 确认人 / 解锁说明 for all registry tasks (outbound only).
 *
 *   node scripts/backfill-dispatch-feishu.mjs [--dry-run]
 *   node scripts/backfill-dispatch-feishu.mjs --rescan   # scan pending first
 *   node scripts/backfill-dispatch-feishu.mjs --sprint-id 2026-W30
 */

import { loadDotEnv } from './lib/feishu-bitable-config.mjs';import {
  backfillAllDispatchFields,
  buildPendingTargetMap,
} from './lib/dispatch-feishu-projection.mjs';
import { loadAllTasks } from './lib/task-registry-lib.mjs';
import { loadPending, loadRules, scanTriggers } from './coordinator-dispatch.mjs';

function parseArgs(argv) {
  return {
    dryRun: argv.includes('--dry-run'),
    rescan: argv.includes('--rescan'),
    sprintId: (() => {
      const i = argv.indexOf('--sprint-id');
      return i >= 0 ? argv[i + 1] : '';
    })(),
    help: argv.includes('--help') || argv.includes('-h'),
  };
}

async function main() {  loadDotEnv();
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    console.log(`Usage:
  node scripts/backfill-dispatch-feishu.mjs [--dry-run]
  node scripts/backfill-dispatch-feishu.mjs --rescan [--dry-run]
  node scripts/backfill-dispatch-feishu.mjs --sprint-id 2026-W30

Projects dispatch_gate / dispatch_confirm_by / dispatch_trigger to Feishu for every task
with feishu_bitable_record_id. Does NOT write registry (outbound only).`);
    process.exit(0);
  }

  if (opts.rescan && !opts.dryRun) {
    console.log('Running coordinator-dispatch scan (all done causes)...');
    scanTriggers('', false);
  } else if (opts.rescan) {
    console.log('[DRY] would run coordinator-dispatch scan');
  }

  const rules = loadRules();
  const pendingState = loadPending();
  const pendingMap = buildPendingTargetMap(pendingState.pending);
  const { byId } = loadAllTasks();

  const sprintId = opts.sprintId;
  let tasks = [...byId.values()];
  if (sprintId) {
    tasks = tasks.filter((t) => t.sprint_id === sprintId);
  }

  console.log(
    `Backfill dispatch fields: ${tasks.length} task(s) sprint=${sprintId || '(all)'} pending=${pendingState.pending.length} dryRun=${opts.dryRun}`,
  );

  let lastLog = 0;
  const { summary, failures } = await backfillAllDispatchFields({
    tasks,
    rules,
    pendingMap,
    dryRun: opts.dryRun,
    rateLimitMs: opts.dryRun ? 0 : 200,
    onProgress: ({ taskId, projection, ok }) => {
      const now = Date.now();
      if (now - lastLog < 3000 && projection.gate === 'none') return;
      lastLog = now;
      const flag = ok ? 'OK' : 'FAIL';
      console.log(
        `  ${flag} ${taskId} gate=${projection.gate}${projection.confirmBy ? ` by=${projection.confirmBy}` : ''}`,
      );
    },
  });

  console.log('\nSummary:');
  console.log(`  none=${summary.none} pending=${summary.pending} confirmed=${summary.confirmed}`);
  console.log(`  ok=${summary.ok} fail=${summary.fail} skipped=${summary.skipped}`);
  if (failures.length) {
    console.log('\nFailures (first 10):');
    failures.slice(0, 10).forEach((f) => console.log(`  ${f.taskId}: ${f.error}`));
  }

  process.exit(summary.fail > 0 ? 1 : 0);
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
