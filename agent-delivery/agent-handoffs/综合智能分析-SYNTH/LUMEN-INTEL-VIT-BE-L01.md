# LUMEN-INTEL-VIT-BE-L01

区域创新活力 — Java 任务中心白名单与 Feign 转发。完工停在本地,未 commit/push。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:backend-agent` |
| supervised_by | `human:唐绍祖` |
| 状态 | 代码完成 + 单测 8/8(2026-10-28);集群网络验证待联调 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未跳失败语义/审计/配额释放;报告类型回归测试通过 |

## 实现范围

仓 `repos/lumen-svc-platform`(dev,本地)。`gkxlumen-topic-async-service-biz`:

新增:
- `support/analysis/SynthVitalityAnalysisTypes.java` — 两键白名单 + 窗归一(1y|3y|5y→中文,
  未知 null 拒绝;空默认最近3年)+ 报告模板号 `synth-vitality-report-v1`。
- `feign/RemoteSynthJobPythonClient.java` + `SynthJobPythonFeignConfig.java` — 只调
  `POST /internal/v1/synth/jobs/execute`;NEVER_RETRY(重试双开算子);5s/300s;
  url `${gkxlumen.topic.async.synth.algo-base-url:http://gkxlumen-platform-entan-py:8000}`。
- `service/adapter/analysis/SynthVitalityAnalysisAdapterImpl.java` — validate(region/compare
  必填;窗非法拒绝)+ buildExecuteBody(task_id/leaf=vitality/region/compare/window 中文;
  analysis_fp/force 不进下游)+ createDownstream(code!=0 或 Feign 异常 → 任务 failed,
  不写演示 JSON)+ normalizeSucceeded。
- 测试两类 7 例(白名单/窗归一/body/失败/成功/注册)。

修改:
- `support/artifact/ArtifactAnalysisTypes.java` — REPORT_TYPES +
  `region_innovation_vitality_report`;parentAnalysisTypeOf → `region_innovation_vitality`。
- `support/analysis/AnalysisTaskIdGenerator.java` — 前缀:分析键 `VIT-`、报告键 `REP-`。
- `service/impl/analysis/AnalysisTaskServiceImpl.java` — `synthVitalityJob` 分支走政策同款
  同步链(落库 → adapter.createDownstream → applySvcSyncResult 签发 res-{taskId} 快照 →
  SSE;失败释放配额)。subType=region_innovation_vitality,totalNodes=1。

Java 全程零公式(等权/归一/缺维收缩只在 Python 装包);任务失败格 = null 由 Python 返回,
Java 原样落 `result_payload`。

## 偏离

无口径偏离。唯一取舍:走政策同步链而非独立 worker(装包秒级,复用 applySvcSyncResult 签发)。

## 验收证据

- `mvn test -Dtest='SynthVitalityAnalysisTypesTest,SynthVitalityAnalysisAdapterImplTest,ArtifactAnalysisTypesTest'`
  → Tests run: 8, Failures: 0(含既有 ArtifactAnalysisTypesTest 回归)
- 日志样例:`synth execute envelope taskId=VIT-3 pyCode=0 leaf=vitality`
- 集群网络(`gkxlumen-platform-entan-py:8000` 可达)本机不可验,联调时核

## 架构合规自检

- ✅ 调用链:Java 只 Feign lumen-algo-py `/internal/*`;无 demo-*
- ✅ 算法只在 Python:Adapter 无任何公式
- ✅ D12:未引入 demo 回落;未用 chain.algo-base-url 复用(独立配置键)
- ✅ 可观测:审计/日志同既有链路;重试禁用防双开
- ✅ 结果快照:Python 不自签 result_snapshot_id;Java applySvcSyncResult 签发

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | ~65000 |
| model_used | cursor-glm-5.3 |
| actual_cost | ~0.32 |
| cost_warn | green |

## CI/CD

- 分支:lumen-svc-platform dev(本地未提交)
- dev 测试:mvn 单测 8/8 绿(内部依赖 gkxlumen-common-* 已本地 install)

## 涉及文件

- repos/lumen-svc-platform/gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz/src/main/java/com/topcomm/gkxlumen/topic/async/{support/analysis/SynthVitalityAnalysisTypes.java,feign/RemoteSynthJobPythonClient.java,feign/SynthJobPythonFeignConfig.java,service/adapter/analysis/SynthVitalityAnalysisAdapterImpl.java}(新)
- .../support/artifact/ArtifactAnalysisTypes.java、support/analysis/AnalysisTaskIdGenerator.java、service/impl/analysis/AnalysisTaskServiceImpl.java(改)
- .../src/test/java/.../SynthVitalityAnalysisTypesTest.java、SynthVitalityAnalysisAdapterImplTest.java(新)
