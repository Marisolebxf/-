# E-INNOV-M1-L07 · gkx_lumen_fronted_pc 迁入 innov 模块

## 任务信息

| 字段 | 值 |
|------|-----|
| task-id | E-INNOV-M1-L07 |
| agent | frontend-agent |
| repo | lumen-ui-science-pc（原 gkx_lumen_fronted_pc） |
| branch | feat/E-INNOV-M1-L07 |
| commit | 2f6dfc8948514482e5420d7e166e6084743ee337 |

## 范围与实现

### Bootstrap

- 从 `SZCGKX/gkx_lumen_fronted_pc`（main）复制脚手架至空仓 `gkx-lumen/lumen-ui-science-pc`
- 保留：Arco Design + Vue3 + Vite7、`observability.ts`、`request.ts` 拦截器、`.gitlab-ci.yml`、`k8s/lumen-pc.yaml`（NodePort 30891）

### innov 模块迁入

| 源（demo-ui-system-test） | 目标（lumen-ui-science-pc） |
|---------------------------|----------------------------|
| `src/views/innov/**` | `src/views/innov/**`（Element Plus → **Arco Design Vue**） |
| `src/api/innov/index.ts` | `src/api/innov/index.ts`（`@/` 别名，适配 request 解包） |

- API 基路径：`/innov/v1/*` → 网关 `/api/innov/v1/*` → `lb://gkx-innov`
- 路由：`/innov`（name=`innov`）；菜单「全球创新监测」(`global-innovation-monitor`) 同组件

### 环境变量

| 文件 | VITE_APP_API_URL | 说明 |
|------|------------------|------|
| `.env.development` | `http://10.50.69.111:9999` | 本地 dev 直连 dev 网关 |
| `.env.production` | （空） | K8s nginx 反代 `/api` → `gkx-gkx-platform-gateway:9999` |

### CI/CD 调整

- `feat/E-INNOV-M1-*` 分支触发 `frontend:image` + `deploy:k8s`（dev 命名空间）

## Design.md §14 检查清单

| # | 检查项 | 状态 | 说明 |
|---|--------|------|------|
| 1 | 浅蓝白科技工作台（非深色大屏） | ✅ | 继承 DefaultLayout + `#D8E7FC` 页面底色 |
| 2 | Header + 左侧导航 + 主内容容器 | ✅ | DefaultLayout 保留 |
| 3 | 选中态 `#165DFF` / `#E8F3FF` | ✅ | Arco 主题 primary |
| 4 | 表单/按钮/分页/标签 Arco 节奏 | ✅ | innov 全量 Arco 组件 |
| 5 | 地图工具栏尺寸克制 | ✅ | size=small |
| 6 | loading/empty/error 状态 | 🟡 | API 错误 Message + traceId；空态 a-empty |
| 7 | 图表色序列 | ✅ | ECharts 沿用 demo 配色 |
| 8 | 无霓虹/营销 hero/emoji | ✅ | |
| 9 | 依赖 `@arco-design/web-vue` 非 antd | ✅ | package.json 已含 |
| 10 | 首屏地图/图谱工作台感 | ✅ | M1 EventMap 默认 Tab |
| 11 | Header ~64px | ✅ | layout.css |
| 12 | 侧栏 ~200px | ✅ | |
| 13 | 控件高 ~32px | ✅ | size=small |
| 14 | 主色 `#165DFF` | ✅ | |
| 15 | 背景 `#D8E7FC` | ✅ | |
| 16 | 中央主视图 > 右侧面板 | ✅ | EventMap 14:10 列比 |

## 架构合规自检（architecture-baseline §2）

| 铁律 | 状态 |
|------|------|
| 前端只调 Java REST | ✅ `/api/innov/v1` 经网关 |
| 禁止 merge demo2 | ✅ 只读参考 demo-ui-system-test |
| 新页 Arco 禁 antd | ✅ |
| observability.ts | ✅ 保留 + 错误 Message 附 traceId |
| NebulaGraph / 算法越层 | N/A（本任务纯 UI） |

## 可观测性

- **工具模块**：`src/utils/observability.ts`（继承老仓）
- **请求拦截**：`src/utils/request.ts` — 成功响应 dev 模式 console.debug Tempo/Loki 深链；失败 Message 附 `traceId`
- **环境变量**：`VITE_GRAFANA_BASE_URL` / `TEMPO_DS` / `LOKI_DS` 已配置
- **抽样 traceId**：待 L05 后端就绪后 dev 实测；本地 build 已通过

## 测试证据

### 本地 build

```
npm run build  →  exit 0（2026-06-20）
vue-tsc --build  →  0 errors
vite build  →  dist/ 产出正常
```

### GitLab Pipeline

| 字段 | 值 |
|------|-----|
| pipeline_url | https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-science-pc/-/pipelines/4118 |
| branch | feat/E-INNOV-M1-L07 |
| commit_sha | 2f6dfc8948514482e5420d7e166e6084743ee337 |
| deploy_namespace | dev（目标） |
| image_tag | 2f6dfc89（CI_COMMIT_SHORT_SHA） |

| Job | 状态（2026-06-20 实测） |
|-----|-------------------------|
| frontend:build | ✅ success |
| frontend:image | ✅ success |
| deploy:k8s | 🟡 running（推送后约 20min 仍在 rollout） |
| trivy:frontend | 🟡 running |

### K8s dev 访问

- **目标 URL**：http://10.50.69.111:30891/innov
- **状态**：本机探测超时（内网不可达或 deploy 未完成）；待 `deploy:k8s` 绿后由内网验收

## 产物清单

- 代码：`gkx-lumen/lumen-ui-science-pc` @ `feat/E-INNOV-M1-L07`
- innov 页面：5 Tab（M1–M5）
- API 客户端：`src/api/innov/index.ts`（20+ 端点）

## 偏离说明

- demo-ui-system-test 使用 Element Plus；lumen 正式仓统一 **Arco Design Vue**（D8），组件 API 已重写
- innov API 响应在 lumen `request.ts` 已解包 `{code,data}`，组件内直接取返回值（非 `res.data`）

## 阻塞项 / 风险

| # | 项 | 严重度 | 负责人 |
|---|-----|--------|--------|
| 1 | 新仓 GitLab CI Variables（`KUBECONFIG_B64`/`HARBOR_*`）可能未从老仓迁移 | 🟡 | devops |
| 2 | `gkx-innov` Java 服务（L05）未就绪时 API 404，页面可开但无数据 | 🟡 | api-agent |
| 3 | dev 网关 `:9999` 外网可达性待联调确认 | 🟡 | integration |

## cost 回填

| estimated_tokens | actual_tokens | model_used | actual_cost | cost_warn |
|------------------|---------------|------------|-------------|-----------|
| 500_000 | TBD | claude-sonnet-4.5 | TBD | green |

## 建议下一任务

- **L08** frontend-agent：EventMap 联调真实 API（替换 mock，地图点位+热力+列表+详情）
