# POL-L2-DS10-CMP-BE-L01 · 科创政策全景 · 政策重点比对 · 展示读面与要素只读

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 开工时已是 `in_progress`，本单不改状态 |
| 说明 | 任务已认领。本 handoff 不改 registry 状态 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 沿用已有 display 控制器、element 缺项控制器和 `PolicyAnalysisAdapterImpl`。不新造框架，不加依赖，不新造 `metric_id`，不改 D4 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POL-L2-DS10-CMP-ARCH-SEQ` |
| 图 diff | 未改图。实现按已签收架构：display → topic-policy / element / topic-async-service |
| 会签态 | 架构稿记 `draft`（源文件无 frontmatter） |
| 说明 | 浏览器入口仍是 `/display/v1/policy/**` |

## 修改内容

仓库 `lumen-svc-platform`，分支 `dev`，commit `896956ecbcfa65cdd6062862c3feb2b5f366fbd6`。

现成类都在，没有另起一套：

- `gkxlumen-display` `PolicyPanoramaController` / `PolicyPanoramaService`
- `gkxlumen-element` `PolicyGapfillController`（`ElementDao.listOrEmpty`）
- `gkxlumen-topic-async-service` `PolicyAnalysisAdapterImpl`（白名单在 `PolicyAnalysisTypes`）

调用链：

| 浏览器资源 | 做法 |
|---|---|
| `GET /display/v1/policy/panorama/version-diff` | display → element 只读 `gkxlumenx_gapfill.gapfill_policy_version_diff`。缺 `policy_id` 或两个发布时间则空。日期成对、次序不限。不拼高亮 |
| `GET .../panorama/search` | 仍只委托 `gkxlumen-topic-policy` `GET /topic/v1/policy/search` |
| `GET .../panorama/{id}/detail` | 正文仍走 `GET /topic/v1/policy/docs/{id}`。无正文则详情空。有正文时，未传 `dimension` 或勾了申报条件/申报材料，element 只读 `gapfill_policy_detail_compare`，把 `apply_condition`、`apply_material` 带上。无行则这两列空。受理部门仍是正文里的值 |
| `GET .../panorama/stats` | 区域和类别仍委托 topic-policy 的 metrics / indicators。同一次向 element 要实施部门、支持力度、对标对象。某一块失败不把另一块写成 0 |
| `GET .../panorama/benchmark-report` | element 只读 `gapfill_policy_benchmark_report`。至少两个对象且字段属于政策类型、支持力度、覆盖范围才查。响应没有 PDF / Word 字节 |
| `POST .../panorama/jobs` | display 仍只提交 `POST /topic/v1/analysis/tasks`。`policy_intensity` 与原有 `policy_effect`、`policy_match` 一起放行。不直接打 `jobs/execute` |

要素内部路径（浏览器不打）：

- `GET /v1/element/policy/version-diff`
- `GET /v1/element/policy/detail-compare`
- `GET /v1/element/policy/compare-stats`
- `GET /v1/element/policy/benchmark-report`

`PolicyAnalysisTypes` 增加 `policy_intensity`，不走产业 VID 二选一，以便适配器把 `sub_type=policy_intensity` 转发到已有 `POST /internal/policy/jobs/execute`。Python 是否执行这个 `sub_type` 不在本单。

### 支持力度读哪张表

`ads.policy_intensity` 没有支持力度列。已有 `polan.eval.intensity.run()` 把 `M_POLICY_SUPPORT_STRENGTH` 写在同库 `policy_metric_timeseries`（`metric_id` 这一列，`metric_value` 为值，`region_code` 为地区）。DATA 第 2 节写明不补列。element 同步读的是这张已有表，不调用 `run()`，不进 Job。无行则 `support_strength.records` 为空，不造 0。空值保持空。

对标对象从 `policy_intensity` 里 `scope_type=province` 的 `scope_code`、`scope_name` 带出，不带力度分。范围是「全球科创领先城市」时对象和力度都空（没有海外城市）。未选范围时对象仍返回，力度为空。范围是「国内先进地区」、至少两个对象、且勾了「支持力度」才筛力度行。

实施部门：只传一个部门，或方面不是「项目类别 / 技术类别」，则部门块空。不按发布机构去重。

查询参数用数据叶列名，契约冻结仍归 `BE-POL-CONTRACT-01`：`policy_id`、`publish_date_a`、`publish_date_b`、`dimension`、`region_name`、`impl_dept`、`aspect`、`benchmark_scope`、`benchmark_object`、`compare_field`。

## 测试结果

本机 JDK 17 + Maven 3.9.9：

- `PolicyGapfillControllerTest` 6 通过
- `PolicyPanoramaServiceTest` 3 通过
- `PolicyAnalysisTypesTest`、`PolicyAnalysisAdapterImplTest`、`AnalysisAdapterRegistryChainTest` 共 17 通过

未跑整仓 CI。推送后由流水线编译。

## 遗留风险

- 四张 `gapfill_` 表由 `POL-L2-DS10-CMP-GAPFILL-L01` 建表灌数。表不在时读失败返回空列表，不在请求里建表
- Python 尚未挂 `policy_intensity` 时，任务会失败或结果为空，Java 不补演示分
- 对标报告的 PDF / Word 未做。契约写导出可以不做。没有行就不产生文件
- 216 的「政策类型」「覆盖范围」不改挂成别的指标。未勾支持力度时力度卡空
- 未改 D4，未新造 `metric_id`，未把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开

## 架构合规自检

1. 调用链：前端 → display → topic-policy / element / topic-async-service。display 不直连 Python、不直连库。✅
2. 算法仍在 Python。本单只放行转发。✅
3. 未写 nGQL。✅
4. 未新设计观测点，沿已有 Feign。✅
5. CI 待推送后的流水线。✅ 本机单测已过
6. 未 merge demo。✅
7. 未调用 `demo-*`。✅
8. 未改 D4，未新造 `metric_id`。✅
9. 缺项只读 `gkxlumenx_gapfill`。支持力度只读已有 ADS 时序表。✅
10. 无行不返回写死差异、分数或 PDF。✅

## CI/CD

- 分支：`dev`
- commit：`896956ecbcfa65cdd6062862c3feb2b5f366fbd6`
- pipeline：推送后由 GitLab 触发
- 部署：本单未做 rollout

## 涉及文件

- `gkxlumen-display` `PolicyPanoramaController`、`PolicyPanoramaService`、`RemoteElementClient` 及对应测试
- `gkxlumen-element` `PolicyGapfillController`、`PolicyGapfillControllerTest`
- `gkxlumen-topic-async-service-biz` `PolicyAnalysisTypes`、`PolicyAnalysisAdapterImpl` 及对应测试
