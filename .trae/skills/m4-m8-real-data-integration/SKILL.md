---
name: "m4-m8-real-data-integration"
description: "科技发展态势 M4-M8 页面真实数据对接流水线。Invoke when user asks to scan/fix hardcoded data, NaN rendering, or fake timestamps on M4-M8 pages before backend cutover."
---

# M4-M8 真实数据对接 Skill

> 适用范围：`lumen-ui-science-pc/src/views/situation/` 下 M4 跨系统创新合作 / M5 湾区创新监测 / M6 全球创新治理 / M7 科技发展历程 / M8 创新环境基础 五个模块页。
> 核心约束：**不改前端样式、格式、布局**；诚实性优先（无源显「—」，伪数据显来源）。

## 前置约束（必须遵守）

1. **样式零侵入**：所有修改限于 `<script>` 内逻辑、`computed` 派生、API 调用、类型；CSS/模板结构/组件嵌套不动。
2. **诚实性原则**：
   - 后端无源 → 显「—」或文案「—」，**不许**编造数值展示。
   - 本地派生数据 → 标注来源（如「前端规则试算」「本地会话」），**不许**伪造真实时间戳 / ID。
   - 阈值/权重/规则 → 若无后端配置下发，不许写死在前端。
3. **后端切前置**：本 Skill 聚焦**前端诚实性修复**（硬编码→动态、NaN→空态、伪时间戳→诚实标注）。后端从 mock 切久新（A1 架构决策）属后端改动，由用户另行安排。

## 流水线（7 步）

### Step 1 — 定位模块

```bash
# 路由表 → 模块映射
Grep path="**/lumen-ui-science-pc/src/router/routes.ts" pattern="situation|bay-area|global-innovation|global-governance|history|foundation"
# 模块目录结构
LS path="**/lumen-ui-science-pc/src/views/situation/<module-name>/"
# 入口 + Tab + components + models + api + types
```

输出：路由路径、目录树、关键文件清单。

### Step 2 — 六类硬编码扫描（对每个 Tab + model + api）

| 类 | 搜索模式 | 举例 |
|---|---|---|
| ① NaN 过滤失效 | `typeof \w+ === 'number'\|typeof value === 'number'` | bayAreaModel.ts 原 `.filter(v => typeof v === 'number')` 挡不住 NaN |
| ② NaN 渲染漏洞 | `\w+ >= 0 \? '+' : ''\|\| \w+ >= 0 \? '+' : \`+\`` | `yoy >= 0 ? '+' : ''}{yoy}%` 后端 NaN 时渲染 "NaN%" |
| ③ 硬编码图表参数 | `min:\s*\d+,\s*max:\s*\d+\|coord:\s*\['\d{4}'\|(\d{4}-){1,4}\d{4}` | Y 轴 min:50/max:100、markPoint coord:['2025']、标题（2020-2025） |
| ④ 硬编码种子字典 | `import.*mock.*\bCities\b\|\bfavoriteIndicatorIds = ref\|\bcompareCities = ref` | 从 mock 导入 11 城、默认选中 ['广州','深圳'] |
| ⑤ 伪时间戳 | `new Date()\.toLocaleString\|Date\.now(\|-\w+)?\|time:\s*['"].+规则['"]` | `time:'当前规则'`、`id:\`${Date.now()}-${threshold}\`` |
| ⑥ 硬编码阈值/权重 | `DEFAULT_\w+_THRESHOLD\s*=\s*\d+\|\bweight[s]?\s*[:=]\s*[{]\s*\w+\s*:\s*\d+` | 四维权重 30/25/25/20、SWOT W:18/T:14/O:8/S:4 |

用 Task subagent 逐文件扫，输出 `[文件:行号] → 问题 → 严重度(P0/P1/P2)`。

### Step 3 — 定级

| 级 | 定义 | 动作 |
|---|---|---|
| **P0** | 真实可触发 bug（NaN 被当作 number、渲染 NaN%、空态被染红） | 必修，优先修 |
| **P1** | 硬编码会导致数据错位/误导（图表轴写死、城市字典绕过真源、伪时间戳伪造来源） | 必修 |
| **P2** | 魔法数但纯视觉/不影响数据正确性（热力 alpha 0.18、能量环圆周 0.205、SWOT 颜色） | 不动（避免越界样式） |

### Step 4 — 按模板修（验证过的修法）

#### 模板 T1：NaN 过滤（P0）
```typescript
// ❌ 原：typeof NaN === 'number' 为 true，挡不住 NaN
.filter((v): v is number => typeof v === 'number')
// ✅ 修：显式过滤 NaN + Infinity
.filter((v): v is number => Number.isFinite(v))
```

#### 模板 T2：NaN 渲染（P0）
```vue
<!-- ❌ 原：NaN >= 0 为 false → 渲染 "-NaN%" -->
<span>{{ yoy >= 0 ? '+' : '' }}{{ yoy }}%</span>
<!-- ✅ 修：复用已有 fmtPctOrDash()；若缺则补：function fmtPctOrDash(v: any) { return Number.isFinite(v) ? `${v >= 0 ? '+' : ''}${v}%` : '—' } -->
<span>{{ fmtPctOrDash(yoy) }}</span>
<!-- ✅ 修（颜色）：NaN 被染成红色，用 trendColor 或 getTrendSemanticColor 包装判断 -->
<span :style="{ color: Number.isFinite(yoy) ? trendColor(yoy) : 'inherit' }">{{ fmtPctOrDash(yoy) }}</span>
```

#### 模板 T3：硬编码图表轴（P1）
```typescript
// ❌ 原
yAxis: { type: 'value', min: 50, max: 100 }
// ✅ 修：去掉 min/max 让 ECharts 自适应，或 computed 算真实 min/max
yAxis: { type: 'value' }
```

#### 模板 T4：markPoint 年份写死（P1）
```typescript
// ❌ 原
coord: ['2025', history[history.length - 1]?.score ?? 0]
// ✅ 修：取真实 history 最后一年 + 空态跳过
coord: history.length ? [String(history[history.length - 1]!.year), history[history.length - 1]!.score] : undefined
```

#### 模板 T5：标题年份写死（P1）
```vue
<!-- ❌ 原 -->
<span>头部城市创新能力趋势（2020-2025）</span>
<!-- ✅ 修：computed 动态算 + 空则不显示年份 -->
<span>头部城市创新能力趋势<template v-if="trendYearRange">（{{ trendYearRange }}）</template></span>
```
```typescript
// 对应 computed
const trendYearRange = computed(() => {
  const years = Array.from(new Set(props.cities.flatMap(c => c.history?.map(h => String(h.year)) ?? []))).sort()
  if (!years.length) return ''
  return years.length === 1 ? years[0]! : `${years[0]}-${years[years.length - 1]}`
})
```

#### 模板 T6：硬编码字典绕过 API 真源（P1）
```vue
<!-- ❌ 原：直接从 mock 导入 -->
import { bayAreaCities } from '@/mock/modules/bayAreaInnovation'
<!-- ✅ 修：从父组件 props 透传（后端 dataset.cities），保留 mock 作 fallback -->
import { bayAreaCities as _fallbackCities } from '@/mock/modules/bayAreaInnovation'
const props = defineProps<{ cities?: BayAreaCity[] }>()
const effectiveCities = computed(() => props.cities?.length ? props.cities : _fallbackCities)
// 加 watch：后端加载完后重新同步选中列表（避免残留不存在的城市）
watch(effectiveCities, (cities) => {
  const next = new Set(cities.map(c => c.name))
  const cur = new Set(selectedCities.value)
  if (cur.size !== next.size || ![...cur].every(c => next.has(c))) {
    selectedCities.value = cities.map(c => c.name)
  }
})
```

#### 模板 T7：伪时间戳（P1）
```typescript
// ❌ 原
const updatedAt = new Date().toLocaleString('zh-CN')
const rule = { time: '当前规则', id: `${Date.now()}-${threshold}` }
// ✅ 修：诚实标注
const updatedAt = '本地会话'
const rule = { time: '前端规则试算', id: `rule-${from}→${to}` }
```

### Step 5 — 验证

```bash
# 类型检查（pnpm engines 限制 Node 20.19.0+，本地 20.18.0，直接 npx 绕过）
Set-Location "<repo-path>"
npx vue-tsc --noEmit
# 构建验证
npx vite build
```

必看退出码：0 通过，非零定位错误文件。

### Step 6 — 汇总修复清单

输出表格：

| 级 | 编号 | 文件:行号 | 原问题 | 修法 |
|---|---|---|---|---|
| P0 | xxx | | | |
| P1 | xxx | | | |
| — | 未修 | — | 纯视觉魔法数 / 后端下发后统一改 | 不动（附原因） |

## 已知坑

| 坑 | 说明 | 应对 |
|---|---|---|
| Node engines | `package.json` 要求 Node ^20.19.0，本地 v20.18.0 | `npx vue-tsc` / `npx vite build` 绕过，不要 `pnpm` 直接跑 |
| pnpm 不支持 `&&` | PowerShell 下 `&&` 是错误语法 | 用 `Set-Location ...; <cmd>` 或分号分隔 |
| NaN >= 0 为 false | `NaN` 是 number 类型但与任何值比较都是 false | 所有「符号 + 数值」拼接场景必须 `Number.isFinite` 先判 |
| watch 时序 | props.cities 初始 undefined → fallback 到 mock → 后端回来后 selectedCities 仍是 fallback 选中项 | watch(effectiveCities, ...) 同步重置，带差集判断避免覆盖用户手动选择 |
| build chunk 超 500KB | 非本次改动引入，历史遗留 | 不在 Skill 范围，build 输出末尾的 warning 可忽略 |

## Skill 不覆盖的事

- **后端切换**（RemoteInnovClient → RemoteShowPythonClient）：需后端 Java 环境，用户另行安排。
- **指标算法对接**（真实 calc-logic / py 回填）：属数据治理任务，不在本 Skill 范围。
- **评审层门控**（D1-D4 就绪度角标）：按 `AGENTS.md` D9 约束走 `@/review` 评审层，本 Skill 不碰。
- **commit/push**：用户明确要求「不提交推送等我自己触发」，Skill 只改代码不动 git。
