# Frontend handoff · E-PLATFORM-P0-L07 专题分析前端壳

| 项 | 值 |
|---|---|
| 任务 | E-PLATFORM-P0-L07 |
| Epic | E-PLATFORM-P0 |
| 角色 | frontend-agent |
| 仓 | `lumen-ui-science-topic`（GitLab project 232） |
| 分支 | `feat/E-PLATFORM-P0-L07` |
| Commit | `0378bcf` |
| 日期 | 2026-06-20 |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 证据 |
|--------|------|------|
| `src/views/topic/**` + `/topic` 路由 | ✅ | `src/views/topic/index.vue`；`src/router/routes.ts` name=`topic` |
| TopicLayout + MetricCard + GraphPanel 占位 | ✅ | `src/components/topic/*` |
| 仅调 Java gkxlumen-topic / gkxlumen-metrics（经网关 `/api`） | ✅ | `src/api/topic/index.ts`、`src/api/metrics/index.ts` |
| 复用 observability.ts | ✅ | `src/utils/observability.ts` 保留；`request.ts` 错误 Message 附 traceId |
| push → `frontend:build` 绿 | 🟡 | 本地 `npm run build` exit 0；CI 待 push 后观测 |
| `:30892/topic` 可打开 | 🟡 | P0-L00 `deploy:k8s` blocked（K8s API 不可达），待 infra 恢复后验收 |

## 产物清单

### lumen-ui-science-topic

| 路径 | 说明 |
|------|------|
| `src/views/topic/index.vue` | 专题工作台壳：七要素切换 + 健康探测 + 指标/图谱占位 |
| `src/components/topic/TopicLayout.vue` | 三栏骨架（顶栏 + 主视图 + 右侧分析，Design.md §8） |
| `src/components/topic/MetricCard.vue` | KPI 卡（ⓘ 八件套 Popover + 🧪 Mock 角标） |
| `src/components/topic/GraphPanel.vue` | 图谱占位（Wave 1 G6） |
| `src/api/topic/index.ts` | `/topic/v1/health`、`/{element}/metrics`、`/{element}/graph/summary` |
| `src/api/metrics/index.ts` | `/metrics/v1/catalog` |
| `src/types/topic.ts` | 七要素 + catalog 类型 |
| `src/router/routes.ts` | 注册 `/topic` |
| `src/utils/request.ts` | traceId 错误提示 + `silentError`（壳页探测静默） |
| `.env.development` | `VITE_APP_API_URL=http://10.50.69.111:9999`（dev 网关） |

### API 调用链（方案 A）

```
浏览器 → nginx /api/* → gkx-gkx-platform-gateway:9999
  ├─ /topic/v1/**   → gkxlumen-topic
  └─ /metrics/v1/** → gkxlumen-metrics
```

前端 **不直连 Python**。

## Design.md §14 检查清单

| # | 检查项 | 状态 | 说明 |
|---|--------|------|------|
| 1 | 浅蓝白科技工作台 | ✅ | 继承 DefaultLayout `#D8E7FC` |
| 2 | Header + 侧栏 + 主内容 + 中央主视图 + 右侧分析 | ✅ | TopicLayout grid 主:侧 ≈ 中央 > 320px 右栏 |
| 3 | 选中态 `#165DFF` | ✅ | Arco primary + 竖条强调 |
| 4 | Arco 控件节奏 | ✅ | size=small，高 ~32px |
| 6 | loading / empty / error | ✅ | a-spin / a-empty / GraphPanel warning |
| 9 | `@arco-design/web-vue` | ✅ | 仓内已有 |
| 10–16 | 工作台感 / 尺寸 / 主色 / 背景 | ✅ | 与 P0-L00 布局 CSS 一致 |

## 架构合规自检

| 铁律 | 状态 |
|------|------|
| D1 方案 A 共享聚合 | ✅ 仅 topic + metrics Java API |
| D4 observability.ts | ✅ 保留 + request traceId |
| D8 Arco 栈 | ✅ Vue3 + Arco Web Vue |
| 禁止 merge demo2 | ✅ 参考 demo-ui-topic 组件语义，未 merge |
| 算法只在 Python | ✅ 前端无算法 |

## 测试证据

### 本地 build

```
npm run build  →  exit 0（2026-06-20）
vue-tsc --build  →  0 errors
vite build  →  dist/ 含 topic chunk
```

### GitLab Pipeline

| 字段 | 值 |
|------|-----|
| branch | `feat/E-PLATFORM-P0-L07` |
| commit_sha | `0378bcf` |
| pipeline_url | （push 后由 coordinator 回填） |
| 预期 job | `frontend:build` ✅（MR/分支 push 触发） |

### K8s dev 访问

- **目标 URL**：http://10.50.69.111:30892/topic
- **状态**：🟡 依赖 P0-L00 `deploy:k8s` 恢复；本机 curl 内网可能超时
- **本地 dev**：`pnpm dev` → http://localhost:3000/topic

## 偏离说明

- 后端 P0-L05 未就绪时，壳页 API 探测使用 `silentError` 静默失败，UI 展示占位 MetricCard + GraphPanel empty，不阻塞 build。
- Design.md 权威栈写 React + `@arco-design/web-react`；本仓沿用 P0-L00 决策 **Vue3 + Arco Web Vue**（与 lumen-ui-science-pc 一致）。

## 阻塞项

1. **P0-L00 deploy:k8s** — K8s API `10.50.69.111:6443` refused，:30892 暂不可验。
2. **P0-L05 topic Java** — `/topic/v1/health`、`/metrics/v1/catalog` 就绪后可去掉占位 KPI。

## 接力清单

| 下游 | 动作 |
|------|------|
| **integration / infra** | 恢复 K8s → retry deploy → 验 :30892/topic |
| **api-agent** | P0-L05 完成后联调 health/catalog/metrics |
| **coordinator** | CI 绿后标记 done；回填 task-registry cost |

## Cost

| estimated_tokens | actual_tokens | model_used | actual_cost | cost_warn |
|------------------|---------------|------------|-------------|-----------|
| 500_000 | 0 | claude-sonnet-4.5 | 0.0 | green |
