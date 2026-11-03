# E-E7-POLICY-M1-L10 · 专题政策门面 · 检索结果导出与分享

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过调用链、D14 对象存储和诚实空态。未 commit，未 push，未改 task-registry，未标 done。 |

## 范围与实现

展示侧只委托本入口，不在展示侧组装文件。浏览器仍打开 `GET /display/v1/policy/panorama/share`。本单只在专题门面 `GET /topic/v1/policy/share` 增加导出与分享，路径写在 `/{id}` 之前。

导出对象是已有 search 返回的政策目录。门面先调已有 `search`，不另写查询，不打 Python 新路径，不改 `lumen-algo-py`。`format`、`channel` 不进 search。

| 项 | 行为 |
|---|---|
| `format=excel` | 对象键 `gkx-others/policy-panorama-search-export/{日期}/policy-panorama-search-{时分秒}.xlsx` |
| `format=pdf` | 对象键 `gkx-user-reports/science/pdf/{用户}/{日期}/policy-panorama-search-{时分秒}.pdf` |
| 桶 | 只写已有桶 `gkx-lumen`。不调用 `createBucket`，不新造桶或顶层目录 |
| `channel=link` | `share_url` 为 `/display/v1/policy/panorama/share?...` |
| `channel=email` | 不发信。`mail` 为空，`honesty.mail=unavailable:no_mail_service` |
| 响应 | 目录、展示侧链接；写出文件时另给桶名、对象键、下载权限。响应里没有文件字节，没有预签名公开 URL |
| 下载权限 | 当前登录用户 id。匿名不写对象 |
| 库 | `gkxlumenx_topic_policy.policy_share_export` 只存 `bucket_name`、`object_key`、`download_permission` |
| 空目录 | HTTP 成功，导出空结果，不改 501 |
| 客户端未启用 | HTTP 成功，桶名和对象键为空，`honesty.engine` 指向 `OssTemplate`，`fabricated=false` |

对象存储客户端用仓内已有 `com.topcomm.gkxlumen.common.file.oss.service.OssTemplate`（`gkxlumen-common-oss`）。不用 `LocalFileTemplate`。本服务 Nacos 未设 `file.oss.enable=true`，运行时没有这个 Bean，入口走诚实空态，不写桶。

对标报告 217、核增研报 614–618、`report/jobs` 不走本入口。

## 偏离

- 现网政策门面没有打开 `file.oss.enable`。代码在 Bean 存在时调用 `OssTemplate.putObject`；Bean 不存在时不新建客户端、不写本地盘。单测用 mock 验证对象键和文件头。
- PDF 用 JDK 写最小 PDF：可见页是 ASCII 说明，目录原文（含中文标题）在同一文件的 UTF-8 流里。未加 PDF 库，也没有 CJK 字体。
- Excel 用 JDK 打 xlsx，列只有 search 已返回的 `policy_id`、`title`。
- 未改展示服务。展示委托关系按已签收架构稿，本单不在展示侧组文件。
- 未自建邮件服务。

## 产物清单

- `gkxlumen-topic-policy-biz`：`PolicyFacadeController`、`PolicyFacadeService`、`PolicyFacadeServiceImpl`
- 新增 `PolicyShareRecordStore`、`JdbcPolicyShareRecordStore`
- `pom.xml` 增加已有模块 `gkxlumen-common-oss`，未加外部对象存储包
- `db/9x_gkxlumenx_topic_policy.sql` 只追加 `policy_share_export`，未改历史表和收藏表
- 测试：`PolicyFacadeControllerTest`、`PolicyFacadeServiceImplTest`

## 验收证据

只跑了改到的两个测试类，未跑全仓。

```
mvn -pl gkxlumen-topic-policy/gkxlumen-topic-policy-biz -am test -Dtest=PolicyFacadeControllerTest,PolicyFacadeServiceImplTest -Dsurefire.failIfNoSpecifiedTests=false
```

- `PolicyFacadeControllerTest`：Tests run: 18, Failures: 0, Errors: 0
- `PolicyFacadeServiceImplTest`：Tests run: 34, Failures: 0, Errors: 0
- 合计 Tests run: 52, Failures: 0, Errors: 0

未 commit，未 push，无 pipeline。

## 架构合规自检

- ✅ 算法只在 Python。本入口不打分、不推理，目录来自已有 search。
- ✅ 调用链仍是门面 search → Python `/internal/policy`。未让浏览器改打 `/topic/v1/policy`。
- ✅ 不写 nGQL，不碰图谱。
- ✅ 不调用 demo-* 服务。
- ✅ D14：只准备写桶 `gkx-lumen` 的已有目录 `gkx-user-reports` 与 `gkx-others`。不新造桶，不调用 `createBucket`，不用本地盘模板。
- ✅ 前端不直连对象存储。响应无文件字节、无预签名公开 URL。
- ✅ 分享链接只给 `/display/v1/policy/panorama/share`。
- ✅ 不自建邮件服务。
- ✅ 不把对标报告 217 和研报 614–618 当作本入口。
- ✅ 展示侧只委托本入口，不在展示侧组装文件。
- ✅ 库只存桶名、对象键、下载权限。文件字节不进 MySQL。

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 20000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.11 |
| cost_warn | green |

无控制台分项。按本单 `estimated_tokens` 20000、api-agent 80/20、B 档 `$3/$15` 回填：`20000×0.80×3/1e6 + 20000×0.20×15/1e6 = 0.108`，记 `0.11`。
