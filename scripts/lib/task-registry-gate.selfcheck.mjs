/**
 * ponytail: ceiling = pending_test→testing 闸门真值表；加新豁免时改本文件。
 * 运行：node scripts/lib/task-registry-gate.selfcheck.mjs
 */
import assert from 'node:assert/strict';
import { checkTransitionGate } from './task-registry-lib.mjs';

const daily = {
  claimed_by: 'agent:frontend-agent',
  supervised_by: 'human:孔东',
};
const longTask = {
  claim_type: 'coordinator_dispatch',
  claimed_by: 'agent:algorithm-agent',
  supervised_by: 'human:淮政玮',
};

assert.equal(
  checkTransitionGate('pending_test', 'testing', daily, { agent: 'agent:coordinator-agent' }).ok,
  false,
  '日常短任务 coordinator 不得绕过黄敬洲闸门',
);
assert.equal(
  checkTransitionGate('pending_test', 'testing', longTask, { agent: 'agent:coordinator-agent' }).ok,
  true,
  '长任务 coordinator 必须能转 testing',
);
assert.equal(
  checkTransitionGate('pending_test', 'testing', longTask, { agent: 'qa-agent' }).ok,
  true,
  'bare qa-agent actor',
);
assert.equal(
  checkTransitionGate('pending_test', 'testing', { ...daily, claimed_by: 'agent:qa-agent' }, { agent: 'agent:qa-agent' }).ok,
  true,
  'agent:qa-agent 前缀',
);
assert.equal(
  checkTransitionGate('pending_test', 'testing', daily, { agent: 'human:黄敬洲' }).ok,
  true,
  'actor=human:黄敬洲 即使 task.supervised_by 不是他',
);
assert.equal(
  checkTransitionGate('pending_test', 'testing', longTask, { agent: 'human:淮政玮' }).ok,
  false,
  '总控授权人本人不能代替 QA 闸门',
);

console.log('task-registry-gate.selfcheck ok');
