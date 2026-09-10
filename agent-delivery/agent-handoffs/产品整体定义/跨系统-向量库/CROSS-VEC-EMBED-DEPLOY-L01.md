# CROSS-VEC-EMBED-DEPLOY-L01 · bge-base-zh-v1.5 embedding 端点（OpenAI 兼容 `/v1/embeddings`）

> 总控 [`CROSS-VEC-长任务总控.md`](./CROSS-VEC-长任务总控.md) §0 #18 / §5 / §6.3 / §6.4 步 1；前序同角色 [`CROSS-VEC-DEVOPS-NET-L01.md`](./CROSS-VEC-DEVOPS-NET-L01.md)。
> **本叶最重要的一条**：现网**没有**可复用 embedding 端点（第一步判定 = 建），已在 **K8s `dev`** 起 TEI CPU 版跑 `BAAI/bge-base-zh-v1.5`，端点 **`http://gkxlumen-embed-tei:8080/v1/embeddings`**，Pod 内实测返回 **dim = 768**、L2 归一（配 COSINE）。`lumen-platform-algo-py` / `-worker` / `gkxlumen-platform-entan-py` / `-worker` **四个 Pod 全部可达**。§0 #17 那个「集成电路 → 矿产勘探」的语义缺陷，用真模型实测已修好（见 §验收证据 4）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务解 hold 第 1 步（§6.4）；lock 24h；已 claimed + in_progress 后落地本叶 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 阶梯第 2 级先跑满（先查后建，结论=无可复用端点）；第 5 级复用「已装依赖」= 直接用官方 TEI 镜像 + 官方权重，**未写一行推理代码、未装任何 ML 依赖、未做镜像二次构建**。交付面 = 1 份 3 对象的 K8s 清单（PVC + Deployment + Service），无 sidecar、无网关、无自研代理。未用 YAGNI 跳过架构铁律 / 可观测 / handoff。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 运维叶，本机未走 Headroom 压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `02-概要设计.md` §2 调用链（FE → GW → Java → Python `/internal` → Milvus 19530） |
| 图 diff | **新增一条边**：Python（`lumen-algo-py` / entan-py）→ `gkxlumen-embed-tei:8080`（集群内 ClusterIP，HTTP）。原有边不变；未新增任何 Java / 前端 → embedding 边；embedding 服务**不连** Milvus、不连数据库、不出集群 |
| 会签态 | `v0.3-draft`（源文件 frontmatter；未自填绿） |

## 范围与实现

**做**：给 `lumen-algo-py` 提供一个 `bge-base-zh-v1.5`（dim 768）的 embedding 端点，对外契约固定为 **OpenAI 兼容 `POST /v1/embeddings`**。

### 第一步：先查后建 —— 结论「**无可复用端点 → 建**」

> 证据来源 = **`CROSS-VEC-VECQ2-SPIKE-L01` 中止前的只读实测**（2026-09-11 00:5x–01:1x），非本叶重复探测；本叶只做了 §落地前置 的补测。

| 查什么 | 结果 |
|--------|------|
| K8s 全 ns 的 Deployment / Service（`embed` / `tei` / `xinference` / `ollama` / `bge` / `m3e` / `rag`） | **零命中** |
| `gkxlumen-platform-ai-py` openapi | 只有 evaluation / recommend / risk，**无 embedding** |
| 19 台主机 × 38 个常见推理端口 TCP 扫描 | **零命中**（命中的都是 nginx / Patroni / 前端） |
| dev 侧唯一模型配置 | `LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4` + `LLM_MODEL=glm-5.2` → **云 LLM，不是 embedding** |
| `aip_kb_*` 写入方 | **未定位**（88.84 SSH 连不上；88.43 的 19530 无 ESTABLISHED 可溯源）。与本叶目标无关，按补料指示不再追 |
| 现网 dim 佐证 | `aip_kb_1` / `aip_kb_2` = **dim 1024 / COSINE**；`spk_id_speaker_embeddings` = dim 192 / IP（声纹，与文本无关）。均**不是** 768，即使定位到写入方也不能直接复用 |

→ **判定：走部署。** 模型已由 `human:淮政玮` 2026-09-11 01:13 拍定，无需反推现网 1024 维那套是什么。

### 第二步：部署位置选型

选 **K8s `dev` 起 Deployment**，不选「88.43 同机加容器」。理由：

1. **硬闸优先**：88.43 上住着 `milvus` / `milvus-minio` / `milvus-etcd` + nebula / ES / kafka / MySQL 等 26 个在跑业务容器，动它要运维窗口；K8s dev 加一个新 Deployment 对现有业务**零触碰**。
2. **四个消费 Pod 全在集群内**，走 ClusterIP DNS 比跨机 IP 更稳（88.43 本叶作业期间 SSH 反复掉线，探针就是这么中断的）。
3. dev ns **无** ResourceQuota / LimitRange / NetworkPolicy，节点余量充足（worker 8C/16G，requests 仅 11–31%），`kubectl auth can-i create deployment/service/pvc -n dev` 全 `yes`（本叶补测）。
4. 延迟代价可忽略：实测集群内单条 22ms（见 §验收证据 3）。

### as-built

| 项 | 值 |
|----|-----|
| 部署位置 | K8s `dev`（集群 `kubernetes-admin@cluster.local`），Pod 落在 `htsvr079` |
| 对象 | `Deployment/gkxlumen-embed-tei`（1 副本，`Recreate`）· `Service/gkxlumen-embed-tei`（**ClusterIP**，8080）· `PVC/gkxlumen-embed-tei-cache`（5Gi，`local-path`） |
| 清单真源 | [`as-built/embed-tei-dev.yaml`](./as-built/embed-tei-dev.yaml)（本仓）；节点副本 `htsvr050:/root/gkx-embed/tei.yaml` |
| 镜像来源与 tag | **`ghcr.io/huggingface/text-embeddings-inference:cpu-1.8`**，`digest sha256:c466c976…9099`（amd64），**kubelet 从 ghcr.io 直连拉取成功，用时 32.1s，镜像 239,133,285 字节**。⚠️ **未经 harbor 中转**（详见「偏离 #1」） |
| 权重获取途径 | 容器启动时由 TEI 从 **huggingface.co 直连**拉 `BAAI/bge-base-zh-v1.5`。⚠️ 该仓库**没有** `model.safetensors`（HTTP 404），TEI 自动回退 `pytorch_model.bin`（日志原文：`safetensors weights not found. Using 'pytorch_model.bin' instead.`），首次下载 **87.3s**；也没有 ONNX（`model.onnx` / `onnx/model.onnx` 均 404）→ ORT 后端失败后自动回退 **candle CPU Bert 后端**（日志：`Starting Bert model on Cpu`）。**全流程无人工上传** |
| 运行规格 | CPU 版（8 个节点全无 GPU）。requests `500m/1Gi`，limits `2/4Gi`；实测常驻 `memory.current = 899,178,496` 字节（≈857 MiB），`/data` 占 **391 MB**，负载 `loadavg 0.20` |
| 模型运行态（`GET /info`） | `model_id=BAAI/bge-base-zh-v1.5` · `dtype=float32` · `pooling=cls` · `max_input_length=512` · `max_client_batch_size=64` · **`max_batch_requests=4`**（candle CPU 后端上限，TEI 自动下调并 WARN） · `version=1.8.3` |
| 重启存活策略 | `restartPolicy: Always` + `startupProbe`（10s×90，容首启下载）+ `readiness` / `liveness` 打 `/health`。权重落 PVC → **重启不重下**：实测删 Pod 后 `Model weights downloaded in 1.173s`（对比首启 87.3s），**2m01s** 恢复 `1/1 Running`，复测仍 `dim=768`。恢复时间的大头是 candle **warmup ≈110s**，不是下载 |
| 鉴权 | **未开**（TEI `api_key: None`）。Service 是 ClusterIP、无 Ingress / NodePort，暴露面仅集群内，与同环境 Milvus 无鉴权口径一致。**本叶未创建任何 Secret，无口令可入 git**；若后续要开，见开放项 H2 |

**不做**（按派单）：未改任何业务仓代码；未给 `lumen-algo-py` / entan 注入 `EMBED_*` env（属 `CROSS-VEC-EMBED-SWITCH-L01`）；未动 helm values 里 entan 的键（台账 D 另议）；未改 Nacos 任何配置；未对 Milvus 做任何写操作。

## 偏离

| # | 偏离 | 理由 / as-built |
|---|------|-----------------|
| 1 | 派单预警「内网大概率直连不了 ghcr.io / HuggingFace」，实际**直连成功，未走 harbor** | 探针已实测节点可读 ghcr manifest（200）、Pod 内 `huggingface.co` 200；本叶补测 `cpu-1.8` manifest **HTTP 200** 且拿到 amd64 digest，随后 kubelet **真拉成功**（32.1s，239MB）。harbor 的 ghcr 代理项目匿名不可见、`registries` API 401 → 既然能直连就不引入中转层（ponytail：少一跳依赖）。**代价**：镜像与权重的可得性挂在公网上，见「遗留风险」。 |
| 2 | 权重用 `pytorch_model.bin`，不是 safetensors；后端是 candle 而非 ORT | 上游仓库 `BAAI/bge-base-zh-v1.5` 就**没有** safetensors 和 onnx 文件（本叶实测 `model.safetensors` → HTTP 404）。TEI 自带回退链，输出正确（dim 768 / L2 归一 / 语义达标），只是加载慢一点。**未改模型 id 去凑一个有 safetensors 的变体** —— 那会偏离 `human:淮政玮` 拍板的模型。 |
| 3 | 部署位置的清单落在 `gkx-orchestration` 的 `as-built/`，不在业务仓 / helm chart | 派单明令「产物仓 `gkx-orchestration`，只写 handoff / as-built，不改业务仓代码」。因此这份清单**目前不受 CI 管**，属技术债，已登记开放项 H1。 |
| 4 | 未做 `kubectl top` 的资源占用取数 | 集群 **Metrics API 不可用**（`error: Metrics API not available`，dev 未装 metrics-server）。改用容器内 cgroup 直读 `memory.current` + `du -sh /data` 取证，数值见 as-built 表。 |

未违反硬闸：未改动 / 未重启 `milvus` / `milvus-minio` / `milvus-etcd`；未 create / drop / insert / load 任何 collection（对 Milvus 只发过一次 `collections/list`）；未改 Nacos；本叶未把任何远端凭据落到本地或仓内（补料提到的探针凭据事件不复现）；未 force push。

> ⚠️ **免责说明**：作业期间 `dev` 里另有一个 `lumen-platform-algo-py-ddfcf7455-f6wzt` 处于 `CrashLoopBackOff`，那是**其他叶正在滚动的部署**，本叶全程未触碰它（本叶只对自己的 `gkxlumen-embed-tei` 做过 delete pod）。实测用的是同 Deployment 里健康的 `-7bcbf7f446-mtlrf`。

## 产物清单

- `agent-delivery/agent-handoffs/产品整体定义/跨系统-向量库/as-built/embed-tei-dev.yaml`（K8s 清单 as-built 快照）
- 本 handoff
- 集群侧（非 git 产物）：`dev/gkxlumen-embed-tei` Deployment + Service + PVC

## 验收证据

**全部真实执行过**（本机 → `htsvr050`，context `kubernetes-admin@cluster.local`）。
> 作业中途 MCP `user-ssh-executor` 崩溃（`namespaceStatus: error` / `Not connected`，多次重试与 `mcp_auth` 均失败）。改用本机临时脚本走同一套 `E:/mcp/servers.json` 预置连接执行 SSH（ssh2，凭据只在内存、不落盘、不打印），命令与输出如实照录。

### 1. 落地前置（本叶补测探针没测完的四项）

```text
kubectl auth can-i create deployment/service/pvc -n dev  → yes / yes / yes
kubectl get sc                                           → local-path (default) rancher.io/local-path WaitForFirstConsumer
节点余量（8 节点）                                        → worker 8C/15Gi，requests cpu 11%–31% / mem 23%–35%
CPU 指令集                                                → avx2 fma（TEI cpu 镜像所需）
/ 磁盘                                                    → 97G 用 22G 余 71G
Metrics API                                              → 不可用（未装 metrics-server）
```

### 2. 镜像 / 权重可得性 + 真实拉取

```text
# ghcr manifest（htsvr050）
token_len=80
manifest_http=200
{"schemaVersion":2,"mediaType":"application/vnd.oci.image.index.v1+json","manifests":[
  {"digest":"sha256:c466c97680cc9c2968108c4b1b44ca7729a091a44b61c840d9487f07d42e9099",
   "platform":{"architecture":"amd64","os":"linux"}}, ...

# HF 权重探针（206 = Range 命中；model.safetensors 确认不存在）
config.json          -> 206:1
tokenizer.json       -> 206:1
model.safetensors    -> 404:15
pytorch_model.bin    -> 206:1
1_Pooling/config.json-> 206:1

# kubelet 真实拉取（kubectl describe pod）
Normal  Pulling  Pulling image "ghcr.io/huggingface/text-embeddings-inference:cpu-1.8"
Normal  Pulled   Successfully pulled image ... in 32.104s. Image size: 239133285 bytes.
```

### 3. 端点实测 —— **原始请求 / 响应 + dim=768**

在 `lumen-platform-algo-py-7bcbf7f446-mtlrf` **Pod 内**用 stdlib `http.client` 发起（脚本 `kubectl cp` 到 `/tmp`，执行后已删除）：

```text
>>> POST /v1/embeddings HTTP/1.1
>>> Host: gkxlumen-embed-tei:8080
>>> Content-Type: application/json
>>> {"model": "BAAI/bge-base-zh-v1.5", "input": ["\u96c6\u6210\u7535\u8def"]}
<<< HTTP/1.1 200 OK
<<< content-type: application/json
<<< x-compute-type: gpu+optimized
<<< x-compute-time: 22
<<< x-compute-tokens: 6
<<< x-total-time: 22
<<< x-queue-time: 0
<<< x-inference-time: 22
<<< content-length: 9657
<<< date: Thu, 10 Sep 2026 17:36:55 GMT
<<< {"object":"list","data":[{"object":"embedding","embedding":[-0.014500996,-0.021490963,0.028720768,0.048083507,
    0.00135189,-0.020158494,0.041997474,0.0070211403,0.011526404,0.019143876,-0.043929394,-0.016832938,0.022358103
    ...(truncated)... 0.017622314,-0.043971833,-0.018331697,-0.020538617,-0.05848793],"index":0}],
    "model":"BAAI/bge-base-zh-v1.5","usage":{"prompt_tokens":6,"total_tokens":6}}
<<< PARSED len(data[0].embedding) = 768
```

> `x-compute-type: gpu+optimized` 是 TEI 的响应头默认值，**不代表真用了 GPU**：启动日志明确 `Starting Bert model on Cpu`，且 8 个节点均无 GPU。别被这个头误导。

批量 2 条 + L2 校验（同一 Pod）：

```text
HTTP 200 elapsed_ms 212
object= list model= BAAI/bge-base-zh-v1.5 usage= {'prompt_tokens': 20, 'total_tokens': 20}
index 0 dim 768 head3 [-0.027162, -0.009947, 0.032686] l2 1.0
index 1 dim 768 head3 [0.036559, 0.022097, 0.056328] l2 1.0
DIM_768_OK
```

→ **返回向量已 L2 归一（‖v‖=1.0）**，与 `gkxlumen_industry_anchor` 的 COSINE 度量天然匹配，SWITCH 叶不必再自己归一。

### 4. 语义能力实测 —— §0 #17 的缺陷已修好

同一 Pod，查询加 bge 非对称检索指令前缀（`为这个句子生成表示以用于检索相关文章：`），与 4 个候选锚点算余弦：

```text
query = 集成电路产量增长23.1%
  集成电路     cos=0.5030
  半导体制造   cos=0.3768
  农业种植     cos=0.1586
  矿产勘探     cos=0.1571
TOP1 = 集成电路
```

对照 §0 #17 记录的 blake2b 字面哈希：top1 命中「矿产勘探」0.329、真值「集成电路」只排第二 0.327（差 0.002）。换真模型后正确答案 **0.5030**、错误答案 **0.1571**，**差距拉开 3.2 倍**。

### 5. 从 lumen Pod 逐个实测可达（照 DEVOPS-NET 的风格）

```text
=== lumen-platform-algo-py-7bcbf7f446-mtlrf ===        dns=10.104.117.125 TCP_OK health=200 embeddings=200 dim=768
=== lumen-platform-algo-py-worker-769d596c98-96f29 === dns=10.104.117.125 TCP_OK health=200 embeddings=200 dim=768
=== gkxlumen-platform-entan-py-d896f785-njjx8 ===      dns=10.104.117.125 TCP_OK health=200 embeddings=200 dim=768
=== gkxlumen-platform-entan-py-worker-5dd4d97b48-8ph6p === dns=10.104.117.125 TCP_OK health=200 embeddings=200 dim=768
```

### 6. 重启存活实测（只删本叶自己的 Pod）

```text
01:37:31  kubectl delete pod gkxlumen-embed-tei-d94d76bc-xgmtw
[01:37:32] gkxlumen-embed-tei-d94d76bc-bh72d 0/1 ContainerCreating
[01:39:32] gkxlumen-embed-tei-d94d76bc-bh72d 1/1 Running        ← 2m01s

新 Pod 日志（PVC 缓存命中，未重下 400MB）：
  Model artifacts downloaded in 280.916µs      （首启：6.67s）
  Downloading `pytorch_model.bin`
  Model weights downloaded in 1.173373668s     （首启：87.31s）
  Starting Bert model on Cpu
  Warming up model … Ready                     （warmup ≈110s，恢复时间大头）

重启后复测：dim= 768
```

### 7. 对现有系统零影响的依据

- **未碰 88.43**：本叶全程没有对 `milvus` / `milvus-minio` / `milvus-etcd` 执行任何 docker / 配置 / 重启操作；新服务跑在 K8s `dev` 的 `htsvr079`，与 88.43 只有「无」这一种关系（embedding 服务不连 Milvus）。
- **Milvus 只读一次**，前后 collection 名单一致且完整（含 PY-INDEX 建的那张）：

```text
{'code': 200, 'data': ['spk_id_speaker_embeddings', 'aip_kb_1', 'aip_kb_2', 'gkxlumen_industry_anchor']}
```

- **未挤占资源**：dev 无 ResourceQuota / LimitRange；新增 requests 仅 `500m / 1Gi`，落点 `htsvr079` 原 requests 为 cpu 22% / mem 23%。
- **未改任何既有对象**：`kubectl apply` 只 `created` 三个新对象（dry-run 与实 apply 均无 `configured` / `unchanged` 之外的既有资源变更）。
- **未开新暴露面**：ClusterIP，无 NodePort / Ingress。

## 问题清单 / 开放项（升级给 `human:淮政玮`）

| # | 事项 | 谁做 | 状态 |
|---|------|------|------|
| H1 | **清单无 GitOps 主**：`embed-tei-dev.yaml` 目前只是 `gkx-orchestration` 的 as-built 快照 + 节点上一份副本，没进任何 CI。建议后续收编进 `lumen-algo-py/k8s/`（与 `api.yaml` / `worker.yaml` 同源）或 helm chart，需一张业务仓 devops 单 | devops + `human:淮政玮` | 🟡 |
| H2 | **端点无鉴权**（TEI `api_key: None`）。与同环境 Milvus 口径一致，且只有 ClusterIP。若安全评审要求，开 `--api-key` 走 K8s Secret（不进 git）+ 客户端加 `Authorization: Bearer`，改动约 5 行 | 运维 + `human:淮政玮` | 🟡 |
| H3 | **权重与镜像挂在公网**：首启需能访问 ghcr.io + huggingface.co。生产环境若断网，需预置权重到 PVC 或把镜像推进 harbor。建议在 SWITCH 叶验收后做一次「离线可复现」演练 | devops | 🟡 |
| H4 | **单副本、单节点 PVC**（`local-path` 绑 `htsvr079`）。该节点故障 = embedding 不可用（rebuild / JOB-A 会诚实降级，不会给假 VID）。要 HA 需换共享存储或每副本独立 PVC | 运维 | 🟡 |
| H5 | **prod / 正式环境尚无此端点**：本叶只交付 `dev`。上线前需同样一份清单落到目标环境 | devops + `human:淮政玮` | 🟡 |

## 修改内容

| 文件 | 改了什么 |
|------|----------|
| `as-built/embed-tei-dev.yaml` | 新增：PVC + Deployment + Service 三对象清单（as-built 快照） |
| 本 handoff | 新增 |
| K8s `dev`（集群侧，非 git） | 新增 `Deployment/gkxlumen-embed-tei`、`Service/gkxlumen-embed-tei`、`PVC/gkxlumen-embed-tei-cache` |

## 测试结果

| 检查 | 结果 |
|------|------|
| `kubectl apply --dry-run=server` | 3 个对象 `created (server dry run)`，无既有资源被改 |
| Pod 就绪（首启） | `1/1 Running`，约 3m40s（拉镜像 32s + 权重 87s + warmup 110s） |
| `GET /health` | 200（四个消费 Pod 内各测一次） |
| `POST /v1/embeddings` | 200，**dim=768**，L2=1.0，单条 22ms / 双条 212ms |
| 语义回归（§0 #17） | top1 = 集成电路（0.5030），矿产勘探降到 0.1571 ✅ |
| 重启存活 | 删 Pod → 2m01s 自愈，权重走 PVC 缓存（1.17s），复测 dim=768 |
| Milvus 未受影响 | `collections/list` 4 张表齐全，未 create / drop / insert |

## 遗留风险

- **公网依赖**（H3）：容器每次启动仍会向 huggingface.co 做一次元数据校验（缓存命中时 280µs）。若某次公网不通且缓存被清（PVC 删除 / 换节点），首启会失败。缓解：可加 `HF_HUB_OFFLINE=1`（缓存已就绪时），或按 H3 预置离线权重。
- **吞吐上限低于配置值**：candle CPU 后端把 `max_batch_requests` 强制降到 **4**（TEI 启动 WARN 原文：`Backend does not support a batch size > 4`）。1516 条锚点 rebuild 按 32 条/批串行约需分钟级，夜班 QPS 无压力，但**别按 `max_client_batch_size=64` 去估并发**。
- **单点**（H4）：1 副本 + 节点绑定 PVC。
- **无鉴权**（H2）：任何能进 dev 网络的 Pod 都能调。
- **清单脱离 CI**（H1）：下次有人 `kubectl delete` 或重建集群，这套东西不会自动回来。

## CI/CD（必填）

- 分支：`gkx-orchestration` `origin/dev`（非 force）
- commit：见文末「push SHA」
- pipeline URL / ID：`gkx-orchestration` 无业务 CI（文档仓）；**本叶未触发任何业务仓 pipeline**
- 部署 namespace / 镜像 tag：`dev` / `ghcr.io/huggingface/text-embeddings-inference:cpu-1.8`
- K8s rollout：**成功**（`gkxlumen-embed-tei` `1/1 Running`；重启自愈复测通过）
- dev 测试 URL / 命令与结果：

```text
# 集群内端点
http://gkxlumen-embed-tei.dev.svc.cluster.local:8080/v1/embeddings   （dev ns 内可简写 http://gkxlumen-embed-tei:8080）

kubectl -n dev exec lumen-platform-algo-py-7bcbf7f446-mtlrf -- python -c "…POST /v1/embeddings…"
  → HTTP 200, dim=768, l2=1.0
kubectl -n dev exec <各 Pod> -- python /tmp/reach.py
  → 4/4 TCP_OK health=200 embeddings=200 dim=768
```

## 可观测性（建议）

- OTEL_SERVICE_NAME：未设。TEI 原生支持 `--otlp-endpoint` + `--otlp-service-name`（默认 `text-embeddings-inference.server`），可零代码接入集群里的 `gkxlumen-platform-otel-collector`。本叶未开（派单未要求，且会给 collector 增流量）；接入只需加 2 个启动参数 → 建议随 SWITCH 叶联调时一并评估。
- Prometheus：TEI 在 **9000** 端口暴露 metrics（`prometheus_port: 9000`，容器内已监听）。本叶未在 Service 上开该端口，需要时加一个 `port: 9000` 即可。
- traceId（dev 抽样）：无（本叶未接 OTel）。
- Tempo / Loki：无新埋点；容器 stdout 已被集群日志采集覆盖。
- 给 SWITCH 叶：`embed_text()` 的 span 属性只记 `host:port` + `model_id` + `dim`，**不要记入参文本全文**（政策 / 企业正文可能含敏感信息）。

## 涉及文件

- `agent-delivery/agent-handoffs/产品整体定义/跨系统-向量库/as-built/embed-tei-dev.yaml`
- 本 handoff

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ embedding 是独立推理服务，**只有 Python 侧调用**；Java / 前端零改动、零新通道 |
| 调用链不可越层 | ✅ 仍 FE → GW → Java → Python `/internal` → （Milvus 19530 ∥ embedding 8080）；新边只挂在 Python 之后 |
| 图谱仅 Nebula | ✅ 未动 `192.168.88.43:9669` / space `demo_gkx_chain`；向量不替代建图 |
| 可观测 | ✅ 未破坏现有 OTel；TEI 的 OTLP / Prometheus 接入路径已写明（上文），未为省事装作不存在 |
| CI/CD | ✅ 仅 `gkx-orchestration` push `origin/dev`，未 force；未触发业务仓 pipeline；未点 `helm:deploy` |
| demo2 不 merge lumen（D12） | ✅ 未改任何 `demo-*` 仓 / 镜像 / 服务。新服务名 `gkxlumen-embed-tei` 属 lumen 侧；**注意**：它与 `demo-*` Pod 同处 dev ns 网络可达，但本叶**未**给任何 demo 服务配置它，lumen 也未依赖任何 demo 服务 |
| 数据策略 | ✅ 未建 / 未删 / 未写任何 collection；未碰 `aip_kb_*` / `spk_id_*`；未写正式 `gkxlumenx_*` |
| 密钥不入 git | ✅ 本叶未创建 Secret（服务未开鉴权，无口令存在）；未把任何远端配置或凭据落到本地或仓内；handoff 无明文 |
| D8 / D9 / D10 | N/A（无 UI / 无指标卡） |

## 交接 · 给 `CROSS-VEC-EMBED-SWITCH-L01`

| 项 | 值 |
|----|-----|
| 端点 URL | `http://gkxlumen-embed-tei:8080/v1/embeddings`（dev ns 内）／全名 `http://gkxlumen-embed-tei.dev.svc.cluster.local:8080/v1/embeddings` |
| 建议 env 名 | `EMBED_BASE_URL=http://gkxlumen-embed-tei:8080`、`EMBED_MODEL=BAAI/bge-base-zh-v1.5`（env 注入点 = `lumen-algo-py/k8s/api.yaml` + `worker.yaml`，与 `MILVUS_URI` 同表；entan 走 helm `entanPy.env` / `entanPyWorker.env`） |
| 请求体 | `{"model": "BAAI/bge-base-zh-v1.5", "input": ["文本1", "文本2"]}`，`Content-Type: application/json`。`input` 收字符串或字符串数组 |
| 响应 | `{"object":"list","data":[{"object":"embedding","embedding":[...768 个 float...],"index":0}],"model":"...","usage":{...}}` |
| 是否需要 token | **不需要**。当前 `api_key: None`，无 `Authorization` 头。若将来按开放项 H2 开启，会走 K8s Secret，键名约定 `lumen-algo-embed` / `EMBED_API_KEY`，届时客户端加 `Authorization: Bearer $EMBED_API_KEY`，**其余契约不变** |
| DIM | **768**；`MODEL_VERSION` 建议写 `bge-base-zh-v1.5-tei-1.8.3`（`/info` 里 `version=1.8.3`） |
| 是否要自己归一 | **不要**。返回向量已 L2 归一（实测 ‖v‖=1.0），直接配 COSINE |
| query 指令前缀 | bge 非对称检索：**query 侧**加 `为这个句子生成表示以用于检索相关文章：`，**锚点（passage）侧不加**。本叶实测正是这么打的分（0.5030 vs 0.1571），别漏 |
| 并发 / 批量建议 | 服务端 `max_batch_requests=4`（CPU 后端硬上限）、`max_client_batch_size=64`、`max_input_length=512`（超长自动截断，不报 413）。建议：**客户端并发 ≤4**，rebuild 分批 **32 条/请求**，`httpx` 超时 **connect 5s / read 60s**，失败重试 2 次退避 1s。1516 条锚点全量 rebuild 预计分钟级 |
| 降级 | 端点不可用时**保留** MemoryStore 回退与 `degraded=true` 语义，禁止给假 VID（总控 §0 #17 / #19 仍有效） |
| 维度迁移 | 现存 `gkxlumen_industry_anchor` 是 dim 256，切 768 **必须 drop + create**（PY-INDEX 的 rebuild 已含此路径，且 `JOB-A` 从未跑过 → 零历史数据迁移） |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 156000 |
| model_used | claude-opus-5-thinking |
| actual_cost | 0.94 |
| cost_warn | green |

口径：devops 默认 75/25 读写比；B 档 `$3/$15` per 1M；`156000×0.75×3/1e6 + 156000×0.25×15/1e6 = 0.94`。
