/**
 * Project auto-created *-DG-G3 leaves to Feishu with 派单门控=待确认.
 */
import { loadDotEnv } from './feishu-bitable-config.mjs';
import { syncOneTask, loadBitableConfig } from './board-task-status.mjs';
import { loadAllTasks } from './task-registry-lib.mjs';

export async function projectAutoCreatedDgToFeishu(dgIds = [], opts = {}) {
  loadDotEnv();
  const dryRun = !!opts.dryRun;
  const cfg = loadBitableConfig();
  const { byId } = loadAllTasks();
  const results = [];

  for (const dgId of dgIds) {
    const t = byId.get(dgId);
    if (!t) {
      results.push({ ok: false, dgId, error: 'not in registry' });
      continue;
    }
    const task = {
      id: t.id,
      title: t.title,
      status: t.status || 'ready',
      agent: t.agent || 'product-agent',
      epic: t.epic || 'E-ENT-SCRUM-PDR',
      delivery_phase: 'definition',
      priority: 'P0',
      record_id: t.feishu_bitable_record_id || t.record_id || '',
      note: t.note || '',
      supervised_by: t.supervised_by || 'human:淮政玮',
    };
    try {
      const r = await syncOneTask(task, cfg, dryRun, {
        dispatchGate: 'pending',
        dispatchConfirmBy: 'human:淮政玮',
        dispatchTrigger: `[门3自动创建] 建单已采纳检测到缺 ${dgId}，请淮政玮确认/拍板`,
      });
      results.push({ ...r, dgId, taskId: dgId });
    } catch (e) {
      results.push({ ok: false, dgId, error: e.message });
    }
  }
  return { count: dgIds.length, results };
}
