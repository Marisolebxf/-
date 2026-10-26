# 集群 Secret

> 2026-10-25。命名空间 `zhipu-tts`。本文只写名字和键，不写值。

口令不进 git，不进镜像层。业务配置一个用途一份 Secret。Deployment 用 `secretKeyRef` 读键，清单里不写模型名、地址或密钥的字面量。

## 模型：`gkx-zhipu-llm`

全系统智谱调用只读这一份。2026-10-25 已在集群创建，并挂到下面的 Deployment。

| 键 | 含义 | 当前值（非密钥） |
|---|---|---|
| `api-key` | 智谱 API Key | 只在 Secret 和 GitLab 变量里 |
| `model` | 模型名 | `glm-5.3-flash` |
| `base-url` | OpenAI 兼容根地址 | `https://open.bigmodel.cn/api/paas/v4` |
| `chat-url` | 产业链用的完整对话地址 | `base-url` + `/chat/completions` |

`chat-url` 由发布脚本从 `base-url` 拼出来。Kubernetes 不能把两个 Secret 键拼成一个环境变量，所以产业链单独要这一键。人只改模型和根地址，不单独维护对话地址。

| 进程 | 环境变量 | 读的键 |
|---|---|---|
| 政策润色、条款抽取（entan api / worker） | `ENTAN_LLM_API_KEY` / `ENTAN_LLM_MODEL` / `ENTAN_LLM_BASE_URL`，以及同值的 `GKX_LLM_*` | `api-key`、`model`、`base-url` |
| 企业叙事、产业链（algo api / worker） | 上一行，再加 `LUMEN_ALGO_CHAIN_LLM_API_KEY` / `LUMEN_ALGO_CHAIN_LLM_MODEL` / `LUMEN_ALGO_CHAIN_LLM_URL` | 再加 `chat-url` |
| 科技新闻（`gkxlumen-platform-innov-py`、`demo-platform-innov-py`） | `LLM_API_KEY` / `LLM_MODEL` / `LLM_BASE_URL` | `api-key`、`model`、`base-url` |

代码在没挂到这些环境变量时，会按同一顺序互认 `ENTAN_LLM_*`、`GKX_LLM_*`、`LLM_*`。清单仍然把本进程原来的变量名都指到这一份 Secret，这样当前镜像不用等发版也能读到。

`tech-news-zhipu-llm` 是旧的新闻密钥。上述 Deployment 已不再引用。Secret 对象还在集群里，删除前要人审，并再查一遍还有没有引用。

## 其它已在用的 Secret

新增时在本表补一行，不要在清单里再写一份口令。

| Secret | 用途 | 依据 |
|---|---|---|
| `gkxlumen-platform-mysql` | lumen 平台库账号 | 集群 Deployment 引用 |
| `demo-platform-mysql` | demo 平台库账号 | 集群 Deployment 引用 |
| `lumen-algo-mysql` | algo 可选库账号（`envFrom`，`optional`） | `lumen-algo-py/k8s/api.yaml` |
| `lumen-algo-milvus` | Milvus 口令。现网未开鉴权时可空 | 同上 |
| `lumen-algo-embed` | TEI 口令。现网无 token 时可空 | 同上 |
| `gkxlumen-platform-rustfs` | 对象存储凭证 | 架构基线 D14 |
| `portal-sso-bridge` | 门户 SSO | 集群 Deployment 引用 |

数据库口令、对象存储凭证、Harbor 口令、`KUBECONFIG_B64` 的改法各自走原入口，不并进 `gkx-zhipu-llm`。
