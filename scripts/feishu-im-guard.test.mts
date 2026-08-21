import assert from 'node:assert/strict'
import { mkdtempSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import path from 'node:path'
import test from 'node:test'
import {
  assertTaskId,
  checkRateLimit,
  formatNotifyText,
  loadAllowlist,
  normalizeRegistryName,
  parseNamedHumans,
  rateKey,
  resolveAllowedHuman,
} from './lib/feishu-im-guard.mjs'

test('normalizes human names and rejects open_id', () => {
  assert.equal(normalizeRegistryName('徐滕强'), 'human:徐滕强')
  assert.equal(normalizeRegistryName('human:徐滕强'), 'human:徐滕强')
  assert.equal(normalizeRegistryName('ou_83274804b3d85eaa43bdaa4aeb9eaa5c'), '')
})

test('task_id must look like a registry id', () => {
  assert.equal(assertTaskId('ENT-FE-I2-12-ANALYSIS-GATE-L01').ok, true)
  assert.equal(assertTaskId('hello').ok, false)
  assert.equal(assertTaskId('').ok, false)
})

test('allowlist is roster intersect mapped humans', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'feishu-im-'))
  const rosterPath = path.join(dir, 'roster.yaml')
  const userMapPath = path.join(dir, 'map.yaml')
  writeFileSync(rosterPath, `
members:
  - registry_name: human:徐滕强
    name: 徐滕强
  - registry_name: human:郭万迎
    name: 郭万迎
`)
  writeFileSync(userMapPath, `
users:
  - name: "徐滕强"
    registry_name: "human:徐滕强"
    feishu_open_id: "ou_aaa"
  - name: "许丹丹"
    registry_name: "human:许丹丹"
    feishu_open_id: "ou_bbb"
`)
  const allow = loadAllowlist({ rosterPath, userMapPath })
  assert.deepEqual(allow.map((p) => p.registry_name), ['human:徐滕强'])
  const hit = resolveAllowedHuman('徐滕强', { rosterPath, userMapPath })
  assert.equal(hit.ok, true)
  const departed = resolveAllowedHuman('许丹丹', { rosterPath, userMapPath })
  assert.equal(departed.ok, false)
  const rawId = resolveAllowedHuman('ou_aaa', { rosterPath, userMapPath })
  assert.equal(rawId.ok, false)
})

test('rate limit blocks same person and task within the window', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'feishu-im-rate-'))
  const ratePath = path.join(dir, 'rate.json')
  const now = Date.parse('2026-08-21T12:00:00+08:00')
  writeFileSync(ratePath, JSON.stringify({
    [rateKey('human:徐滕强', 'ENT-X')]: now - 60_000,
  }))
  const blocked = checkRateLimit('human:徐滕强', 'ENT-X', now, { ratePath, windowMs: 30 * 60 * 1000 })
  assert.equal(blocked.ok, false)
  const other = checkRateLimit('human:郭万迎', 'ENT-X', now, { ratePath, windowMs: 30 * 60 * 1000 })
  assert.equal(other.ok, true)
})

test('message prepends task id once', () => {
  const first = formatNotifyText('ENT-X', '请回填 cost')
  assert.equal(first.ok, true)
  assert.match(first.text, /^【ENT-X】/)
  const second = formatNotifyText('ENT-X', '【ENT-X】已回填')
  assert.equal(second.text, '【ENT-X】已回填')
})

test('user-map parser keeps open_id off the list payload shape', () => {
  const people = parseNamedHumans(`
users:
  - name: "徐滕强"
    registry_name: "human:徐滕强"
    feishu_open_id: "ou_aaa"
`)
  assert.equal(people[0].name, '徐滕强')
  assert.equal(people[0].registry_name, 'human:徐滕强')
})
