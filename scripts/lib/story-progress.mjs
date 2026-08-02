/**
 * 用户故事「实现状态」进度推导（由关联 task-registry 任务滚动汇总）。
 * 飞书展示名见 STORY_STATUS_ZH；库内 status 写英文枚举。
 *
 * 优先级（瓶颈 / 流水线，靠后覆盖靠前时按下列顺序判定）：
 *   已完成 → 测试中 → 联调中 → 开发完成 → 开发中 → 已排Sprint → 已定义
 *
 * 口径（与 task 状态机对齐）：
 *   - 已定义：无关联实现向任务
 *   - 已排Sprint：已挂 sprint_id，尚未进入 claimed/in_progress
 *   - 开发中：存在 claimed / in_progress（或仍有任务未离开开发态且已有联调参差时优先开发中）
 *   - 开发完成：实现向任务全部恰好为 integration（齐步交件进联调门）
 *   - 联调中：存在 integration，且并非「全部恰好 integration」
 *   - 测试中：存在 pending_test / testing
 *   - 已完成：全部 ≥ ready_to_sign（含 done）
 */
export const STORY_STATUS_ZH = {
  defined: '已定义',
  sprint_planned: '已排Sprint',
  developing: '开发中',
  dev_complete: '开发完成',
  integrating: '联调中',
  testing: '测试中',
  done: '已完成',
};

/** 看板分组建议顺序 */
export const STORY_STATUS_ORDER = [
  'defined',
  'sprint_planned',
  'developing',
  'dev_complete',
  'integrating',
  'testing',
  'done',
];

const TASK_RANK = {
  backlog: 0,
  ready: 1,
  blocked: 1,
  claimed: 2,
  in_progress: 3,
  integration: 4,
  pending_test: 5,
  testing: 6,
  review: 6, // legacy
  'needs-revision': 3,
  ready_to_sign: 7,
  done: 8,
  completed: 8,
};

function rankOf(status) {
  return TASK_RANK[status] ?? 0;
}

/**
 * 滚动汇总时优先看实现/横切 leaf；若故事只挂了定义轨任务，则退回全部关联任务。
 * @param {Array<{ status?: string, sprint_id?: string, delivery_phase?: string }>} linkedTasks
 * @returns {keyof typeof STORY_STATUS_ZH}
 */
export function deriveStoryProgressStatus(linkedTasks) {
  const all = (linkedTasks || []).filter(Boolean);
  if (!all.length) return 'defined';

  const implish = all.filter(
    (t) => t.delivery_phase === 'implementation' || t.delivery_phase === 'crosscut',
  );
  const use = implish.length ? implish : all;
  const statuses = use.map((t) => t.status || 'backlog');
  const has = (...xs) => statuses.some((s) => xs.includes(s));
  const everyRankAtLeast = (n) => statuses.every((s) => rankOf(s) >= n);
  const anySprint = use.some((t) => Boolean(t.sprint_id && String(t.sprint_id).trim()));

  // 已完成：全部待签收或已完成
  if (everyRankAtLeast(7)) return 'done';

  // 测试中
  if (has('pending_test', 'testing', 'review')) return 'testing';

  // 联调 / 开发完成（integration）
  if (has('integration')) {
    if (has('claimed', 'in_progress', 'ready', 'backlog', 'blocked', 'needs-revision')) {
      return 'developing';
    }
    if (statuses.every((s) => s === 'integration')) return 'dev_complete';
    return 'integrating';
  }

  // 开发中
  if (has('claimed', 'in_progress', 'needs-revision')) return 'developing';

  // 已排 Sprint（含仅 ready/backlog 但已写入 sprint）
  if (anySprint) return 'sprint_planned';

  // 有关联任务但未排 Sprint、未开工
  if (use.length) return 'defined';

  return 'defined';
}

export function storyStatusZh(code) {
  return STORY_STATUS_ZH[code] || STORY_STATUS_ZH.defined;
}
