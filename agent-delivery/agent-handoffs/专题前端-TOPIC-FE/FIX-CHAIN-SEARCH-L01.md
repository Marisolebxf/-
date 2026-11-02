# FIX-CHAIN-SEARCH-L01 · 产业链高级筛选 400 修复 — industry/search 条件 value 兼容数组（后端）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent`（本 Cursor 会话执行） |
| supervised_by | `human:徐滕强`（2026-11-02 用户裁定：侯佳伟离职，api-agent 划归徐滕强） |
| claim_type | `coordinator_dispatch` |
| 说明 | 名词与流程见 [`task-claiming-guide.md`](../task-claiming-guide.md) |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最小 diff 修根因：`value` 字段 `String`→`Object` 一处改动；未新增依赖；未做前端改动；未跳过 D8/D9/D10、可观测、架构铁律 |

## 问题清单

- 线上报障（2026-11-02 14:58）：产业链高级筛选提示「产业查询不可用」。traceID `cbf0f78478b907d37598cba1f86ebaf1`（lumen 平面）：`gkxlumen-topic-chain-biz` POST `/topic/v1/industry/search` → 400，Loki 日志 `HttpMessageNotReadableException: Cannot deserialize value of type 'java.lang.String' from Array value (token 'JsonToken.START_ARRAY')`。
- 根因：`IndustrySearchCondition.value` 定义为 `String`，高级筛选 `operator=in` 前端传字符串数组 → Jackson 反序列化失败 → 400，请求未进业务逻辑。
- 排查确认：下游 Python（lumen-algo-py `/internal/v1/chain/search`）**已兼容数组**（`_industry_link_condition_matches`：`raw if isinstance(raw, list) else [raw]`；单测 `test_industry_link_leaf_filters_catalog_objects` 即用数组 value）。断点纯在 Java DTO。

## 修改内容

- `gkxlumen-topic-chain-api/.../dto/IndustrySearchCondition.java`：`value` 字段类型 `String` → `Object`（`@Schema` 描述同步注明「字符串或字符串数组」）。
  - Jackson 对 `Object` 天然接受标量与数组，两种入参均不再 400；
  - `searchPost` 经 `objectMapper.convertValue` 编 Map 后原样透传 Python，数组形态保留，Python 端按数组消费语义不变；
  - GET 路径 `encodeConditions` 序列化 conditions，同样保留数组形态；
  - 唯一 Java 侧调用点 `IndustryFacadeServiceImplTest.condition.setValue("industry")`：Lombok setter 形参收 `Object`，字面量兼容，无需改动。
- `gkxlumen-topic-chain-biz/.../IndustryFacadeControllerTest.java`：新增 `searchPostAcceptsArrayConditionValue` 用例（线上原始报错体 200 + 数组形态断言 + 标量向后兼容断言），并补 `Assertions` 静态导入。

## 测试结果

- **最小自检（本机，因 nexus 不可达无法整仓 mvn）**：直接 javac 编译修改后 DTO + 自检类，验证三组断言全过：
  - 线上原始报错体反序列化成功，`value` 为 `List`，首元素 `CL-SEI-01|INB1303|INB130301` 不变；
  - 标量 `value:"industry"` 行为不变；
  - `convertValue` 透传 payload 中 `value` 保持数组形态（Python 可按数组消费）。
  - 输出：`ALL CHECKS PASSED`（6 ok）。
- **仓内回归用例**：`IndustryFacadeControllerTest#searchPostAcceptsArrayConditionValue` 已就位（MockMvc standalone，需 CI 环境执行）。
- ⚠️ 本机限制：`nexus.mo.com` NXDOMAIN、整仓依赖树本地缓存不全，`mvn test` 无法本地跑通；单测验证依赖 CI。

## 架构合规自检（公约 §2）

| 铁律 | 自检 |
|------|------|
| 1 算法只在 Python | ✅ 未引入任何算法逻辑，仅 DTO 类型放宽 |
| 2 调用链 前端→Java→Python /internal | ✅ 链路未动，透传语义保持 |
| 4 可观测 | ✅ 未动埋点；trace 透传不变 |
| 8 数据策略 | ✅ 不涉数据 |
| D12 demo/lumen 隔离 | ✅ 只改 lumen-svc-platform |

## 遗留风险

- `value` 变 `Object` 后，Java 侧若未来有代码需要标量字符串，需自行 `String.valueOf(...)` 收敛（当前仓内无此消费点）。
- Python GET 路径（`conditions` JSON 串）同样带数组透传，Python 已兼容；如后续 Python 回归覆盖 GET 路径更稳。
- 简单筛选等既有前端路径全部传标量，行为不受影响（自检已覆盖）。

## CI/CD（必填）

- 分支：`dev`（本地工作区，**未 commit 未 push**——人工验收闸门，2026-10-20 用户裁定；本单未获「完工即推」授权）
- commit：待监管人验收后提交
- pipeline URL / ID：待 push 后生成
- 部署 namespace / 镜像 tag：待 CI
- K8s rollout：待 CI
- dev 测试 URL / 命令与结果：CI 绿后按派单包 §6.4 回归：
  `curl -X POST http://10.50.69.111:30892/api/chain/topic/v1/industry/search -H 'Content-Type: application/json;charset=UTF-8' -H 'systemCode: topic' --data-raw '{"mode":"advanced","keyword":"","logic":"all","conditions":[{"id":"f14","field":"industry_link","operator":"in","value":["CL-SEI-01|INB1303|INB130301"]}]}'`

## 涉及文件

- `gkxlumen-topic-chain/gkxlumen-topic-chain-api/src/main/java/com/topcomm/gkxlumen/topic/chain/api/dto/IndustrySearchCondition.java`
- `gkxlumen-topic-chain/gkxlumen-topic-chain-biz/src/test/java/com/topcomm/gkxlumen/topic/chain/controller/IndustryFacadeControllerTest.java`
