# 环境对照留档：现网联调 vs 云环境

| 项 | 值 |
|---|---|
| 文档状态 | 送审稿 v0.1 |
| 编制 | 交付实施组 |
| 日期 | 2026-11-11 |
| 关联任务 | `TOPIC-GOLIVE-DEPLOY-DOCS-L01` |
| 密级 | 内部 · **凭证不入库**（口令/AK/SK 见飞书《国科信主卖时间点》·「云环境」表，或 K8s Secret） |

> **铁律**：内测上线目标环境与现网联调环境**物理/逻辑隔离**。禁止用现网地址冒充云环境；禁止云环境流水线继续走 GitLab Runner；云环境 CI/CD **只认容器化管理平台**。  
> `gitlab-runner` 虚机（`192.168.202.172`）**仅**承载 GDF 用 PostgreSQL，**不是**业务 CI/CD 执行器。

---

## 1. 一眼对照

| 维度 | 现网联调（日常联调） | 云环境 |
|---|---|---|
| 定位 | 项目组日常联调 / CI 自动发业务工作区 | 总集内测上线验收与云环境运行 |
| 计算入口 | 节点 `10.50.69.111`（node01）等 | 容器化管理平台控制台 `https://192.168.152.72/...` · 工作区 `业务工作区` |
| 外网固定 IP | （现网入口另册） | `111.198.38.90` |
| 代码仓 | `https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen` | 云环境侧 GitLab `http://192.168.152.88:30010/<业务组>`（VPN：`http://183.62.232.62:30010/<业务组>`）；门户相关业务组 |
| 镜像仓 | `旧镜像仓库` | Harbor 内网 `192.168.152.88:32001` / 外网 `183.62.232.62:32001`；业务镜像组、公共镜像组 |
| **CI/CD** | GitLab CI + Runner（tag=`gkx`，现网） | **容器化管理平台 Pipeline**（devops 工作区）；**禁止** gitlab-runner 跑业务构建/发布 |
| K8s 命名空间（业务） | 业务工作区（现网集群） | `业务工作区`（云环境 / 容器化管理平台工作区，与现网**不是同一集群**） |
| 对象存储 | 现网 RustFS `10.50.69.111:19000` 等（见架构基线 D14 现网口径） | 云环境 S3 兼容 `http://obs.cc.cs`；桶/目录见下表 |
| 向量库 | 现网 TEI / Milvus 另册 | Milvus 集群内 `milvus-proxy.infra.svc.cluster.local:19530` |
| ES | 现网集群另册 | 先用 3 台：`192.168.202.139`–`141`（16C/64G，磁盘 100+500G）；项目组侧企业/政策各约 1 亿量级预留 |
| Redis | 现网 | 主从，2C/4G；用途：用户 token、首页加载 |
| GDF | 现网 | 虚机 `192.168.202.171`（8C/32G，100+200G） |
| 图库 | Nebula / TRSGraph 现网口径 | TRSGraph（燕大主建，全项目共用）· 云环境接入点 **TBD** |
| 可观测 | 现网 Tempo/Loki/Grafana | 云环境放入 `infra` 命名空间（日志 / Grafana / Prometheus） |

---

## 2. 云环境对象存储

业务正式只写桶 **`gkx-lumen`** 下目录（禁止业务写 `milvus` 桶；可观测独立桶）：

| 桶 / 路径 | 用途 |
|---|---|
| `gkx-lumen/gkx-analysis-results` | 展示 / 专题分析中间结果 JSON |
| `gkx-lumen/gkx-user-reports` | 用户生成 HTML / PDF |
| `gkx-lumen/gkx-source-reports` | 政策原始文件、三方报告 PDF |
| `gkx-lumen/gkx-cms-images` | CMS HTML 配图等 |
| `gkx-lumen/gkx-user-assets` | 头像等零碎上传 |
| `gkx-lumen/gkx-others` | 杂项 |
| `tempo-blocks` | Tempo 链路 |
| `loki-chunks` | Loki 日志 |
| `milvus` | Milvus 自用 · **业务禁止写入** |

访问 endpoint：`http://obs.cc.cs`（S3 协议）。**AK/SK 不进本文**，放入 Secret / 飞书凭证表。

---

## 3. 云环境入口

| 组件 | 入口（内网优先） | 备注 |
|---|---|---|
| 容器化管理平台 · 业务工作区 | `https://192.168.152.72/console-acp/workspace/<业务工作区>/overview` | 账号见飞书表 · 用户示例 `<服务账号>` |
| 容器化管理平台 · CI/CD Pipeline | `https://192.168.152.72/console-acp/workspace/devops/pipeline/pipelines` | **唯一**云环境构建发布通道 |
| Harbor | `192.168.152.88:32001` | 外网 `183.62.232.62:32001` |
| GitLab（云环境侧） | `http://192.168.152.88:30010/<业务组>` | VPN 外网同端口 `183.62.232.62` |
| Milvus 运维台 | `http://192.168.202.164:30301/#/connect` | |

---

## 4. 与现网文档的关系

| 现网真源（勿混用于云环境） | 云环境本稿 |
|---|---|
| `agent-delivery/cicd-pipeline.md` | 本文 + 《部署手册》容器化管理平台章节 |
| `agent-delivery/devops/环境说明.md` | 本文 §1 |
| 架构基线 D14（现网 `10.50.69.111:19000`） | 云环境 endpoint 换 `obs.cc.cs`，**目录名不变** |

修订时：改云环境表 → 同步本文版本号；改现网 → 不改本文「云环境」列。
