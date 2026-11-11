/**
 * v2 基线得分行最小自检（POL-SIM-HEADER-SCORE-L01，ponytail：一个 assert 脚本）
 * run: node scripts/test/policy_sim_score.test.mjs
 * 校验两仓改动契约：Java 读 SQL / 前端 kind 与空态文案 / 镜像 v2 公式注记存在。
 * 无 DB、无框架：纯文本锚断言；Java 编译与 FE 自检由各自正式门把守。
 */
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'

const fe = 'e:/zhipu/gkx-lumen/repos/lumen-ui-science-pc'
const java = 'e:/zhipu/gkx-lumen/repos/lumen-svc-platform'

// 1) Java 读侧：页面得分 kind 打 score 表，只读
const ctrl = readFileSync(`${java}/gkxlumen-element/src/main/java/com/topcomm/gkxlumen/element/controller/PolicySimulationReadController.java`, 'utf8')
assert.match(ctrl, /gapfill_policy_sim_score/)
assert.match(ctrl, /"页面得分"/)
assert.match(ctrl, /WHERE row_kind = \? ORDER BY metric_id, id/)
assert.ok(!/INSERT INTO|UPDATE |DELETE FROM/.test(ctrl.split('SCORE_SQL')[1] ?? ''), '得分读取段禁写操作')

// 2) display 白名单放行
const svc = readFileSync(`${java}/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/service/PolicySimulationService.java`, 'utf8')
assert.match(svc, /"页面得分"/)

// 3) 前端 API kind + 页面接线（得分待发布空态 + ⚠️ + 利益攸关条数）
const api = readFileSync(`${fe}/src/api/policySimulation.ts`, 'utf8')
assert.match(api, /kind: '页面得分'/)
assert.match(api, /pendingRef/)
const page = readFileSync(`${fe}/src/views/policy/simulation/index.vue`, 'utf8')
assert.match(page, /得分待发布（D4 接入中）/)
assert.ok(!page.includes('没有接口得分'), '旧空态文案必须清除')
assert.match(page, /isMock !== 1 && !row\.pendingRef/)
assert.match(page, /stakeholderCount/)

// 4) 镜像（只读，禁改）：v2 公式与 D4=mock 注记在案
const mirror = readFileSync(`${fe}/src/views/policy/policyMetricsMirror.gen.ts`, 'utf8')
assert.match(mirror, /有效率×0\.5\+力度均值×50/)

console.log('policy_sim_score 契约自检 4/4 通过')
