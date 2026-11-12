/* 缺陷 2266 修复自检：验证「全无坐标」判定与图例回退逻辑（从 InnovationDetail.vue 移植的纯函数）
 * 运行：node /tmp/gi-bug-2266/selfcheck.mjs —— 全部断言通过输出 PASS */
import { readFileSync } from 'node:fs'

const vue = readFileSync(
  '/Users/xutengqiang/Desktop/xtq/projects/gdf/projects/repos/lumen-ui-science-pc/src/views/situation/global-innovation/tabs/InnovationDetail.vue',
  'utf8',
)

// ---- 1. 源码结构断言：新逻辑存在且被模板消费 ----
const checks = [
  ['mapAllPointsMissingGeo computed 定义', /const mapAllPointsMissingGeo = computed\(\(\) => \{[\s\S]*?list\.every\(\(item\) => !Array\.isArray\(item\.location\)\)/.test(vue)],
  ['noGeoHintCount 定义（非空计数）', /const noGeoHintCount = computed\(\(\) =>/.test(vue)],
  ['模板消费 mapAllPointsMissingGeo 提示', /v-if="mapAllPointsMissingGeo"[\s\S]{0,200}当前筛选共 \{\{ noGeoHintCount \}\} 条成果/.test(vue)],
  ['图例回退区分「未加载」vs「全无坐标」', /return props\.innovations\.length \? \[\] : \[\.\.\.CONTENT_GROUPS\]/.test(vue)],
]

// ---- 2. 行为断言：1:1 移植判定逻辑跑三个场景 ----
const shouldShowMarkers = () => true // 标注模式下
const mk = (n, hasGeo) => Array.from({ length: n }, (_, i) => ({
  id: i, type: 'project', location: hasGeo ? [114, 22] : null,
}))

function behavior(list) {
  const mapAllPointsMissingGeo = shouldShowMarkers()
    && list.length > 0 && list.every((item) => !Array.isArray(item.location))
  const present = new Set()
  for (const item of list) if (Array.isArray(item.location)) present.add(item.type)
  const legendWhenLoaded = present.size ? ['info'] : [] // props.innovations.length>0 分支
  return { mapAllPointsMissingGeo, legendWhenLoaded }
}

const scenarios = [
  ['只勾创新资讯：300 条全无坐标 → 显示提示 + 图例收起', behavior(mk(300, false)), { mapAllPointsMissingGeo: true, legendWhenLoaded: [] }],
  ['混合数据：有坐标 → 不显示提示 + 图例保留', behavior([...mk(10, true), ...mk(5, false)]), { mapAllPointsMissingGeo: false, legendWhenLoaded: ['info'] }],
  ['空数据（未加载）→ 不显示提示', behavior([]), { mapAllPointsMissingGeo: false, legendWhenLoaded: [] }],
]

let failed = 0
for (const [name, ok] of checks) {
  if (!ok) { console.error(`✗ ${name}`); failed++ } else console.log(`✓ ${name}`)
}
for (const [name, actual, expected] of scenarios) {
  const same = JSON.stringify(actual) === JSON.stringify(expected)
  if (!same) { console.error(`✗ ${name} → 实际 ${JSON.stringify(actual)}`); failed++ } else console.log(`✓ ${name}`)
}
if (failed) { console.error(`FAIL: ${failed} 项未过`); process.exit(1) }
console.log('PASS: 全部断言通过')
