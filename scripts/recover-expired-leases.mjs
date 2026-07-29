#!/usr/bin/env node
/**
 * recover-expired-leases.mjs
 * 回收 task-registry 中 lock_until 已过期的 claimed 任务（→ ready，清空认领字段）。
 *
 * 用法：
 *   node scripts/recover-expired-leases.mjs --dry-run
 *   node scripts/recover-expired-leases.mjs --apply
 *   node scripts/recover-expired-leases.mjs --apply --include-in-progress   # 慎用：仅告警默认；加此 flag 才对 in_progress 标 blocked
 *
 * 策略：
 *   - status=claimed + lock_until < now → status=ready，清空 claimed_by / supervised_by / claim_type / claimed_at / lock_until
 *   - status=in_progress + lock_until < now → 默认仅报告（不自动抹工作进度）；--include-in-progress 时标 blocked_by=lease_expired
 *   - status=review 不处理（已进入验收）
 *
 * 关联：task-registry.yaml#claim_policy · 手册 §13.1 / §十六 · coordinator.mdc 站会前清单
 */

import {
  loadAllTasks,
  readRegistryText,
  writeRegistryText,
  findTaskBlock,
  upsertField,
  applyBlockUpdate,
  getScalar,
  touchUpdateTime,
} from './lib/task-registry-lib.mjs';

function parseArgs(argv) {
  const out = { dryRun: true, apply: false, includeInProgress: false, help: false };
  for (const a of argv) {
    if (a === '--apply') {
      out.apply = true;
      out.dryRun = false;
    } else if (a === '--dry-run') out.dryRun = true;
    else if (a === '--include-in-progress') out.includeInProgress = true;
    else if (a === '--help' || a === '-h') out.help = true;
  }
  if (out.apply) out.dryRun = false;
  return out;
}

function parseLockUntil(iso) {
  if (!iso) return null;
  const t = Date.parse(iso);
  return Number.isNaN(t) ? null : t;
}

function clearClaimFields(blockLines) {
  // Set empty / remove-like by writing empty string then strip — upsert empty quotes
  for (const key of ['claimed_by', 'supervised_by', 'claim_type', 'claimed_at', 'lock_until']) {
    const existing = getScalar(blockLines, key);
    if (existing) {
      // Delete field lines entirely for cleanliness
      const re = new RegExp(`^\\s+${key}:\\s*`);
      for (let i = 0; i < blockLines.length; i++) {
        if (!re.test(blockLines[i])) continue;
        // remove single-line field (claim fields are scalars)
        blockLines.splice(i, 1);
        break;
      }
    }
  }
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    console.log(`Usage:
  node scripts/recover-expired-leases.mjs --dry-run
  node scripts/recover-expired-leases.mjs --apply
  node scripts/recover-expired-leases.mjs --apply --include-in-progress`);
    process.exit(0);
  }

  const now = Date.now();
  const { byId } = loadAllTasks();
  const expiredClaimed = [];
  const expiredInProgress = [];
  const expiredOther = [];

  for (const t of byId.values()) {
    const until = parseLockUntil(t.lock_until);
    if (until === null || until >= now) continue;
    if (t.status === 'claimed') expiredClaimed.push(t);
    else if (t.status === 'in_progress') expiredInProgress.push(t);
    else if (t.status === 'review') expiredOther.push(t);
  }

  console.log('=== recover-expired-leases ===');
  console.log(`模式: ${opts.apply ? 'APPLY' : 'DRY-RUN'}  now=${new Date(now).toISOString()}`);
  console.log(`过期 claimed: ${expiredClaimed.length}`);
  console.log(`过期 in_progress: ${expiredInProgress.length}${opts.includeInProgress ? '（将标 blocked）' : '（仅报告）'}`);
  console.log(`过期 review（忽略）: ${expiredOther.length}`);
  console.log('');

  const actions = [];

  for (const t of expiredClaimed) {
    actions.push({
      id: t.id,
      from: 'claimed',
      to: 'ready',
      action: 'release_claim',
      lock_until: t.lock_until,
      supervised_by: t.supervised_by,
      claimed_by: t.claimed_by,
    });
  }

  if (opts.includeInProgress) {
    for (const t of expiredInProgress) {
      actions.push({
        id: t.id,
        from: 'in_progress',
        to: 'blocked',
        action: 'block_lease_expired',
        lock_until: t.lock_until,
        supervised_by: t.supervised_by,
        claimed_by: t.claimed_by,
      });
    }
  } else {
    for (const t of expiredInProgress) {
      console.log(
        `⚠️  SKIP in_progress ${t.id}  lock_until=${t.lock_until}  supervised_by=${t.supervised_by || '-'}  （加 --include-in-progress 才标 blocked）`,
      );
    }
  }

  if (!actions.length) {
    console.log(expiredInProgress.length ? '无可自动回收项（仅有 in_progress 告警）。' : '✅ 无过期 lease。');
    process.exit(0);
  }

  console.log('将执行:');
  for (const a of actions) {
    console.log(
      `  ${a.id}: ${a.from} → ${a.to}  (${a.action})  was supervised_by=${a.supervised_by || '-'}  lock_until=${a.lock_until}`,
    );
  }

  if (!opts.apply) {
    console.log('\n（dry-run：加 --apply 才会写 registry）');
    process.exit(0);
  }

  let lines = readRegistryText().split(/\r?\n/);
  for (const a of actions) {
    const loc = findTaskBlock(lines, a.id);
    if (!loc) {
      console.error(`Task not found: ${a.id}`);
      continue;
    }
    const block = lines.slice(loc.start, loc.end);
    if (a.action === 'release_claim') {
      upsertField(block, 'status', 'ready');
      clearClaimFields(block);
    } else if (a.action === 'block_lease_expired') {
      upsertField(block, 'status', 'blocked');
      upsertField(block, 'blocked_by', `lease_expired at ${a.lock_until}; was supervised_by=${a.supervised_by || '-'}`);
    }
    touchUpdateTime(block);
    lines = applyBlockUpdate(lines, loc, block);
  }
  writeRegistryText(lines.join('\n'));
  console.log(`\n✅ 已更新 ${actions.length} 条任务。建议接着跑 sync-task-ready-status.ps1。`);
}

main();
