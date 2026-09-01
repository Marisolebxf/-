# ALGO-LIB-ODS-MOCK-CHAIN-L01 · 产业链 Mock ODS 主表 CRUD+搜索+翻译

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 用户授权连跑并行；本叶不问人。registry 监管人原为李伟，本会话按授权人淮政玮执行。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用政策 Mock 交互与写门；未新开网关/Feign；未做 tags/product 页签与 AI 填表；未用 YAGNI 跳过写门、服务端搜索、X-Trace-Id。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶实现面窄，未走 Headroom。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（本叶不改存储流图拓扑） |
| 图 diff | 写库方仍 = Demo ODS `dwd_industry_chain_info`；禁止写 DWD/ADS/正式库。 |
| 会签态 | 抄源：CHAIN `01-data-flow.md` 已 `approved`。 |

## 范围与实现

对照 SPEC §产业链 + 派单包：

1. **新页** `/chain/mock`「产业链 Mock」。**未改** `/chain/indana`。
2. 主表 `demo_gkxlumenx_ods.dwd_industry_chain_info`；编辑键 `pk_id`；业务键 `industry_link_code`。
3. 列表 7 列中文列头；搜索 4 字段走 Python `LIKE` AND（禁止前端 filter）。
4. `level` 展示 `第{n}级`（0–7）；未编造领域/链/环节专名。
5. 可选 tags/product 页签本叶不做；禁止产业资讯表。
6. 前端走已有 `/entan/**`：`/entan/v1/chain/mock/...` → Python `/v1/chain/mock/...`。未改 demo-algo-science，未等 /innov Feign。

## 偏离说明

- 并行隔离：未改 policy/entan/svc mock 占用文件；`main.py` 只追加 CHAIN include；router 只在 chain children 追加 `path: 'mock'`。
- 监管人：registry DoD 写 `human:李伟`，本会话授权人为 `human:淮政玮`。

## 产物清单

| 产物 | 路径 |
|------|------|
| CRUD 逻辑 | `demo-algo-ent-analysis/entan/chain_mock.py` |
| 路由 | `demo-algo-ent-analysis/api/chain_mock_routes.py`（前缀 `/v1/chain/mock`） |
| include | `demo-algo-ent-analysis/api/main.py`（`# ALGO-LIB-ODS-MOCK-CHAIN-L01`） |
| 单测 | `demo-algo-ent-analysis/tests/test_chain_mock.py` |
| API 客户端 | `demo-ui-system-test/src/api/chain/mock.ts` |
| 页面 | `demo-ui-system-test/src/views/chain/pages/ChainMockPage.vue` |
| 菜单 | `demo-ui-system-test/src/views/chain/chainMenuConfig.ts`（indana 下） |
| 路由 | `demo-ui-system-test/src/router/index.ts`（chain children `mock`） |

## API

| 方法 | 路径（网关） | 说明 |
|------|-------------|------|
| GET | `/entan/v1/chain/mock/nodes` | 列表+服务端搜索 `q_industry_name/q_industry_link_name/q_industry_code/q_industry_link_code` |
| GET | `/entan/v1/chain/mock/nodes/{pk_id}` | 详情；软删视为未找到 |
| POST | `/entan/v1/chain/mock/nodes` | 新增（仅 Demo） |
| PUT | `/entan/v1/chain/mock/nodes/{pk_id}` | 更新（先读后合并，避免部分字段洗空） |
| DELETE | `/entan/v1/chain/mock/nodes/{pk_id}` | 软删 `is_deleted=1`（无该列则物理删） |

包络 `{code,msg,data}`。空表 `list=[]` + HTTP 200。live 写返回 code=1。`X-Trace-Id` 走现有 middleware。

## 测试结果

- `pytest tests/test_chain_mock.py`：3 passed。
- 直连 `demo_gkxlumenx_ods`（plane=chain）：`total=1273`，`pk_col=pk_id`。
- 服务端搜索 `q_industry_name=人工` → 108 行，全部含「人工」。
- live 写门：`assert_demo_write` 拒绝。
- CRUD 回滚：创建 `CHAINMOCK*` → 部分更新合并保留原列 → 软删后 `get=None`；未写 DWD/ADS。
- 50100 页面待 CI 部署后点验（本叶未等 K8s rollout）。

## 遗留风险

- 自检软删行 `pk_id=10185/10186` 仍在 Demo ODS（`is_deleted=1`，列表不可见）。
- 未做 tags/product 页签。
- 50100 UI 需等 `demo-ui-system-test` + `demo-algo-ent-analysis` CI 绿后点「产业链 Mock」。

## CI/CD（必填）

- 分支：`dev`
- commit：`demo-algo-ent-analysis` `28ce300`；`demo-ui-system-test` `7da2a07`
- pipeline URL / ID：push 后 GitLab
- 部署 namespace / 镜像 tag：现网 demo K8s（CI 触发）
- K8s rollout：本叶提交后由 CI；未在本会话等绿
- dev 测试 URL：50100 `#/chain/mock`（部署后）

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 demo-platform-entan-py
- 新路由经现有 `TraceHeaderMiddleware` / 前端 `observability.ts`

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|------|
| 1 | 算法只在 Python | ✅ CRUD 在 demo-algo-ent-analysis |
| 2 | 调用链 前端→Java→Python | ✅ `/entan/**` 已有网关，未新开 |
| 3 | 图谱 NebulaGraph | ✅ N/A（本叶不写图） |
| 4 | 可观测性 | ✅ 沿用 X-Trace-Id |
| 5 | CI/CD | ✅ push origin/dev |
| 6 | demo 不污染 lumen | ✅ 只改 demo-* |
| 7 | 方案 A | ✅ Java 不直连 ODS |
| 8 | 数据走 ADS | ✅ 只写 Demo ODS |
| 9 | D8 | ✅ 50100 Element Plus，对齐政策 Mock |
| 10 | D9/D10 | ✅ 联调台 Mock，非指标卡页 |
| 12 | D12 lumen 不调 demo | ✅ 未改 lumen-ui-* |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 98000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.15 |
| cost_warn | green |

## 明确未做

- tags / product 可选页签
- 产业资讯表
- 升级 `/chain/indana`
- 改 demo-algo-science / 等 /innov Feign
- 50100 浏览器点验（等 CI）
