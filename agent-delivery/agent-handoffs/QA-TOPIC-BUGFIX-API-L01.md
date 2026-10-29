# QA-TOPIC-BUGFIX-API-L01 · 接口侧 500 / 默认聚合 / B 类数据缺口

## 任务认领

| 字段 | 值 |
|------|-----|
| supervised_by | `human:徐滕强` |
| agent | `api-agent` |
| 依赖 | **先** `QA-TOPIC-BUGFIX-API-DICT-L01`（A 类 VO），再本单 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |

## 一、P0 链路缺陷

### BUG-028-005 · 关系图谱 500

| 项 | 内容 |
|----|------|
| 入口 | 企业详情 Tab「关系图谱」 |
| 接口 | `POST /enterprise/topic/v1/profile/graph/subgraph`（以仓内 paths 为准） |
| 预期 | FUNC-02110：无数据时「暂无关系图谱」，非 500 |
| 前端过渡 | `EnterpriseProfileTabPanel.vue` 已 `.catch→null` 空态；**须查 K8s 日志/trace 修根因** |

排查建议：org_id 参数校验、Nebula/ADS 空图、未捕获异常；修复后 FE 可保留 soft-fail 或改为显式业务空响应。

## 二、B 类 · 默认条件 / 数据缺口（禁止前端伪闭合）

| BUG-ID | 判定 | 说明与动作 |
|--------|------|------------|
| 026-001 | **后端默认聚合** | 重点企业类型分析：空 `chain_codes`/`tag_codes` 时 map/kpi 为空；带 `region_id=440300`、默认 year 仍应返回聚合。接口：`overview-kpi`、`map-distribution`、`region-insight` |
| 026-002 | 同 026-001 | 区域洞察默认无 total/清单，选条件后正常 → 同上链路默认参数 |
| 027-004 | **部分 API** | 识别依据弹窗空：查 `domain-evidence` 是否 200 空体 vs 未实现；FE 已空态文案 |
| 027-005 | **数据缺口 D16** | 重点领域无识别依据：按 gapfill 流程，禁止写 ODS/ADS 供应方库 |
| 027-008 | **指标未闭合 + 数据** | 深圳对标 `city-benchmark` 维度 Q013/Q014/Q016；保持「无数据」诚实态，灌数走 gapfill |

关联用例：FUNC-00382/00384/00385、FUNC-01695/01691、FUNC-02117。

## 三、深圳现状 · 环节筛选（与 FE 兜底分工）

| BUG-ID | 说明 |
|--------|------|
| 028-003 | FE 已按 `node_stage` 请求 + 清单 client narrow；**KPI/分布/清单 total 须 Java #132–134 按 `node_stage` 过滤**。Mock 已补 `node_stage` 序号 |

## 四、环节下拉与用例

- 产品要求「全部环节」选项；FUNC-02095 断言仅 4 个环节名 → PM/QA 需定稿是否更新用例（5 项含「全部环节」）。

## 五、未派后端（本单范围外）

| BUG-ID | 归属 |
|--------|------|
| 028-011 | 前端路由/门户权限卡死，FE 暂缓专查 |
| 028-010/012 等 | 已在 FE-L01 闭合 |

## 联调与 DoD

- [ ] 028-005 500 消除或改为业务空响应（trace 入 bug-registry）
- [ ] 026-001/002 默认条件 dev 复测 FUNC-00382/00385
- [ ] 027-004/005/008 按上表判定修链路或 gapfill 登记
- [ ] 028-003 Java 环节过滤与 FE 联调
- [ ] note 含「联调通过」；handoff 更新 + cost 回填

## 参考

- 缺陷台账：`agent-delivery/qa/bug-registry.yaml`
- 人工登记详情：`agent-delivery/qa/bugs/KJZTFWXT/R1-20261023-脚本修订.md`
- 前端 handoff：`agent-handoffs/QA-TOPIC-BUGFIX-FE-L01.md`
