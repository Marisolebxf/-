# LUMEN-SVC-SEARCH-ES-SWITCH-L01 · 服务机构检索切 ES 引擎 — dev 灰度切换 + engine 埋点补接 + 组合词地域拆分

> 收尾 handoff。前置：[ES-L01 handoff](./handoff.md)（双引擎代码交付，已签收）· [S4-验证报告](./S4-验证报告.md)（回归基线）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:徐滕强` |
| supervised_by | `human:淮政玮` |
| task_type | tech_task（P0，E7-产业服务链分析，repo lumen-topic-py，3 分 / M） |

## 范围与实现

ES-L01 交付后遗留的灰度窗口动作，三件事一次收口：

### 1. dev 灰度切换（配置）
- `k8s/dev-search-py.yaml`：search-py Deployment 新增 `SVC_SEARCH_ENGINE=es`
- 影响面：仅 svc org 检索消费该变量；企业搜索不受影响
- 回退：删除该环境变量重启（`engine_pref()` 默认回落 mysql），或切 `SVC_SEARCH_ENGINE=mysql`

### 2. engine 灰度埋点补接（ES-L01 唯一遗留项）
- `gkx_svc_service/views/search.py`：`search_orgs` 视图层单点结构化日志
- 内容：`engine_pref`（配置开关）/ `engine`（实际引擎）/ `data_source` / `total` / `took_ms` / `kw`（截断 50 字）/ `filters` 条数
- 覆盖全部路径：ES 成功 / ES 降级回 MySQL / 默认 MySQL / 闸门拒绝——`engine_pref != engine` 即降级发生，Loki 可查

### 3. keyword 地域词拆分（组合词兜底，用户裁定并入本单）
- 背景：智能检索「深圳 检验检测」「知识产权 广东」组合词前端闭集解析不出（城市词表 8 裸名无省名、行业词不在闭集），整串回落机构名 keyword ≈ 0 命中
- `search_es.py`：`_GEO_VARIANTS` 词表（3 省/6 市/8 区 + 裸名短形态，来自线上 agg 实测值）+ `split_geo_keyword` 纯函数
  - 分词：空格/顿号/中英文逗号；**整段等于地域变体才拆**（机构名嵌段不拆，wildcard 完整性优先）
  - 地域真值归一带后缀（深圳→深圳市）；拆出词不留在 keyword；全地域词时 keyword=None
- `repo.py::search_orgs`：引擎路由前单点接入，双引擎（含降级路径）共用
  - 显式入参优先（keyword 拆分不覆盖已传的 city/province/area）
  - 单地区 → 落参数（MySQL LIKE 兼容）；同字段多地区 → `filters in` OR（ES terms；MySQL 引擎走 `unsupported_under_mysql` 闸门诚实拒绝）
- 前端零改动；filters DSL 高筛路径不受影响

## 偏离说明

无范围偏离。注：纯城市名 keyword 语义变化（「深圳」从名含深圳 → 全深圳市 14,033 家）为设计意图；词表未含广州/惠州部分区（黄埔/天河/番禺等 12 区缺），「天河 检验检测」类输入不拆分回落原行为，待测试反馈后补词表。

## 产物清单

| 文件 | 内容 |
|---|---|
| `lumen-topic-py` `8341ac4` | 灰度开关 + engine 埋点 + `test_view_engine_telemetry_log` |
| `lumen-topic-py` `9f4f772` | 地域词拆分（词表 + 纯函数 + repo 单点接入 + `test_split_geo_keyword`/`test_repo_routes_geo_from_keyword`） |
| `k8s/dev-search-py.yaml` | `SVC_SEARCH_ENGINE=es` + 回退注释 |

## 验收证据

- 测试：SVC 全套 **39 项 pytest 绿**（新增 3 个测试：埋点日志 / 拆分纯函数 7 组断言 / repo 路由）；全量套件 8 个收集错误为本机缺 sqlalchemy 既有环境问题（干净工作区复现验证，与改动无关）
- 审查：Bugbot 两轮（首变更 finding 全部被 validator 判误报移除）+ /code-review 5 项 finding（1 项多地区 OR 已修，其余按用户裁定挂起待测试反馈）+ Bugbot 定向 5 问（直辖市/边界/叠加/降级/一致性）全部实证通过
- 活体：
  - ES 模拟「深圳 检验检测」组合查询 = 3 家真实机构（宁深/金众/英思太检验检测）
  - 直辖市：`province=北京市` 与 `city=北京市` 各 3 家同批，不漏检
  - **CI/CD：pipeline 2652 / 2658 全绿（smoke+三镜像），deploy:search-py 两次触发均 Job succeeded，rollout 完成（ns=zhipu-tts，镜像 8341ac40 → 9f4f772d），健康探针 ok**
  - **用户页面验证通过（2026-10-21 12:15）：`http://10.50.69.111:30892/service-center/search?mode=smart` 组合词搜索符合预期**
- 回退验证：ES-L01 S4 已锚定（切回 mysql 行为逐字一致）；本次回退通道同（删变量重启）

## 架构合规自检

| 铁律 | 状态 |
|---|---|
| 调用链（前端→Java→Python /internal） | ✅ 未动，Java 透传零改动 |
| 算法只在 Python | ✅ 拆分/检索均在 Python |
| ES 禁直写 | ✅ 仅读索引；ETL 写入走 lumen-etl-es-py（ES-L01 交付） |
| 可观测埋点 | ✅ engine 埋点补接（本单核心交付之一） |
| D12 lumen 隔离 | ✅ 仅动 lumen-topic-py，未触 demo 仓 |
| 前端规范 D8/D9/D10 | ✅ 前端零改动 |

## cost 回填

| 字段 | 值 |
|---|---|
| estimated_tokens | 80,000 |
| actual_tokens | 95,000 |
| model_used | cursor-auto |
| actual_cost | 3.8 |
| cost_warn | green（< $10） |
