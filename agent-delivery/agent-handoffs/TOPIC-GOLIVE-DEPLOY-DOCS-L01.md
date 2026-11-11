# TOPIC-GOLIVE-DEPLOY-DOCS-L01 · 科技专题服务系统 + 专题算法库：本周各出一版《上线部署方案》《部署手册》

> 阶段：**草稿交付**（md 齐套；docx 套版与 TBD 回填未完）。内容按本次实测与落盘实写。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-11-11 以淮政玮身份认领；先出草稿，生产环境与现网隔离，CI/CD 改灵雀云 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |
| 说明 | 本叶为上线验收文档草稿，无业务代码改动 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 文档起草未挂载 headroom |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶未改架构图；部署架构以文字版写入方案草稿 §3.1 |
| 会签态 | N/A |
| 说明 | 文档类；正式套版前若需 ARCH 部署图再补 Mermaid |

## 格式参考（可选）

| 项 | 对齐来源 |
|----|---------|
| 章节结构 | `templates/handoff-template.md` |
| 方案大纲 | `验收文档/上线验收材料/0-材料清单与总集要求/模板_12-上线部署方案.docx` |
| 手册大纲 | `验收文档/上线验收材料/0-材料清单与总集要求/模板_13-部署手册(CI构建手册).docx` |
| 环境对照 | 飞书《国科信主卖时间点》·「生产环境」表（凭证不入库） |

## 问题清单

- 生产域名 / Ingress / NodePort 终值未定（方案中标 TBD）
- Redis 实例名、TRSGraph 生产 endpoint、生产 Nacos 实例未回填
- 灵雀云具体流水线 ID / 名称未登记
- 算法库生产开通子集（innov/entan/etl/apiview）待产品+算法裁定
- 四份正式 **docx** 尚未按模板套版（当前仅 md 草稿）
- 聊天补充材料含明文口令：正文已禁写；建议仅保留飞书凭证表并视情况轮换

## 修改内容

1. **环境隔离留档**：写明现网开发（`10.50.69.111` / aminer GitLab CI / `harbor.test.com`）与生产算力云（灵雀云 `zhipu-tts`、Harbor `192.168.152.88:32001`、生产 GitLab `zp-tts`、外网固定 IP `111.198.38.90`）对照；强调 **CI/CD 只走灵雀云**，`192.168.202.172` 仅 GDF PG、非业务 CI。
2. **专题系统**：按模板_12 / 模板_13 大纲起草《上线部署方案》《部署手册》md 草稿。
3. **专题算法库**：新建目录 `2-专题算法库/`，同样两份 md 草稿；模板「写作组件」章节标 N/A。
4. **安全**：AK/SK、GitLab/Harbor/灵雀云口令均不进 git；指向飞书表 / K8s Secret。
5. **对象存储**：生产 endpoint `http://obs.cc.cs`，目录语义对齐架构基线 D14。

## 测试结果

- 模板大纲抽取：`officecli view` 对模板_12 / 模板_13 成功（方案 1–5 章 + 时间表；手册环境/准备/中间件/业务/问题等节）。
- 未跑业务 CI / K8s rollout（本阶段无代码发布）。
- 草稿已 push `origin/dev`（见下 CI/CD）。

## 遗留风险

- md 草稿 ≠ 总集最终 docx；未套版前不能宣称材料终验完成。
- 若生产侧仍误配 gitlab-runner 或现网地址，存在串环境风险——手册已设检查点，需发布前人工勾选。
- 凭证曾在会话明文出现：仓内无落盘，但会话侧需人工管控。

## CI/CD（必填）

- 分支：`dev`
- commit（草稿落盘）：`651936988` — `docs(golive): TOPIC-GOLIVE-DEPLOY-DOCS-L01 四份部署草稿+环境对照留档 [human:淮政玮]`
- 认领相关 registry：此前已 push（含 `TOPIC-GOLIVE-DEPLOY-DOCS-L01` → `in_progress` / `claimed_by=human:淮政玮`）
- pipeline URL / ID：N/A（编排仓文档，无业务 Pipeline）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- 验证：本地确认五份 md 路径存在；`officecli` 读模板大纲通过

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A（文档叶）
- traceId：N/A
- Tempo / Loki：N/A；方案/手册中已登记生产可观测落 `infra` NS、桶 `tempo-blocks` / `loki-chunks`

## 涉及文件

| 路径 | 说明 |
|---|---|
| `agent-delivery/验收文档/上线验收材料/0-材料清单与总集要求/环境对照-现网开发vs生产上线_留档_v0.1.md` | 现网 vs 生产对照留档 |
| `agent-delivery/验收文档/上线验收材料/1-科技专题服务系统/12-科技专题服务系统_上线部署方案_草稿_v0.1.md` | 模板12 草稿 |
| `agent-delivery/验收文档/上线验收材料/1-科技专题服务系统/13-科技专题服务系统_部署手册_草稿_v0.1.md` | 模板13 草稿 |
| `agent-delivery/验收文档/上线验收材料/2-专题算法库/12-专题算法库_上线部署方案_草稿_v0.1.md` | 模板12 草稿 |
| `agent-delivery/验收文档/上线验收材料/2-专题算法库/13-专题算法库_部署手册_草稿_v0.1.md` | 模板13 草稿 |
| `agent-delivery/agent-handoffs/TOPIC-GOLIVE-DEPLOY-DOCS-L01.md` | 本 handoff |

## 产物 ↔ 模板对照表

| 系统 | 模板 | 草稿路径 | 正式 docx |
|---|---|---|---|
| 科技专题服务系统 | 模板_12 | `1-…/12-…_草稿_v0.1.md` | 待套版 |
| 科技专题服务系统 | 模板_13 | `1-…/13-…_草稿_v0.1.md` | 待套版 |
| 专题算法库 | 模板_12 | `2-…/12-…_草稿_v0.1.md` | 待套版 |
| 专题算法库 | 模板_13 | `2-…/13-…_草稿_v0.1.md` | 待套版 |

## 架构合规自检（文档叶摘要）

| 铁律 | 结果 |
|---|---|
| 调用链 FE→Java→Python `/internal/*` | ✅ 方案文字架构已写 |
| D12 禁 lumen 调 demo | ✅ 算法手册写明 |
| D14 对象存储目录 | ✅ 对照留档与方案对齐目录名；生产 endpoint 单独标注 |
| D17 合规/合理 | ✅ 算法方案提及锁定边界 |
| 密钥不进 git | ✅ |
| CI 生产 = 灵雀云 | ✅ 多处强调；禁 gitlab-runner 业务 CI |

## 下一步（未完项）

1. 回填 TBD（域名、流水线 ID、中间件终址、算法开通子集、上线窗口）
2. 按模板_12/13 套出 4 份正式 docx 落入对应目录
3. 终稿后更新本 handoff 状态说明；再推进 registry（chore 完工路径）

## Cost（草稿阶段估算）

| 字段 | 值 |
|------|-----|
| actual_tokens | ~90000（估） |
| model_used | cursor-composer |
| actual_cost | ~2.0（估 USD） |
| cost_warn | green |
