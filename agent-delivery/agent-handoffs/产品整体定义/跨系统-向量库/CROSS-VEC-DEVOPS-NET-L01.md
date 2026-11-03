# CROSS-VEC-DEVOPS-NET-L01 · Python 出网 Milvus 19530（env / helm / 只读探测）

> **现行环境（2026-11-02）**：下文「尚未创建」是本叶探测当时的输出。现在 lumen 正式集合在库 `gkxlumen` 的 `gkxlumen_industry_anchor`，已建并 load，0 条。库 `default` 的同名集合是 demo。

> 派单包 `派单/CROSS-VEC-DEVOPS-NET-L01-派单包.md`；总控 §0 #4 #5 #11 / §1；设计 `03-详细设计.md` §0。
> **本叶最重要的一条**：总控冻结的 `192.168.88.48:19530` **现网没有 Milvus**；实测监听在 **`10.50.69.111:19530`**（Milvus v2.4.0 standalone，docker）。配置按实测地址落地，地址口径变更升级给监管人（下方 §问题清单 A）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控段 B；lock 24h；已 claimed + in_progress 后落地本叶 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只加 2 个环境变量 + 1 个 optional Secret 位 + 1 个 stdlib 探测脚本（不引 pymilvus，走 Milvus 2.4 HTTP v2）。未用 YAGNI 跳过可观测 / 架构铁律 / handoff；探测脚本自带 `--self-check` 作为可跑检查。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 运维叶，本机未走 Headroom 压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `02-概要设计.md` §2 调用链（FE → GW → Java → Python `/internal` → Milvus 19530） |
| 图 diff | 边不变（仍只 Python 连 19530）；**节点地址修正**：`Milvus 192.168.88.48:19530` → `10.50.69.111:19530`（实测）。未新增任何 Java / 前端 → Milvus 边 |
| 会签态 | `v0.3-draft`（源文件 frontmatter；未自填绿） |

## 范围与实现

**做**：`lumen-algo-py` api / worker 与 entan（api + worker）运行时出网 Milvus gRPC 的 env 落盘 + 文档 + 只读探测。

1. **env 真源**
   - api / worker：`lumen-algo-py/k8s/api.yaml`、`k8s/worker.yaml`（本仓 raw manifest，CI `deploy:api` / `deploy:worker` 用 `sed __IMAGE__ | kubectl apply` 生效）。
   - entan：`lumen-svc-platform/helm/gkxlumen-platform/values.yaml` 的 `entanPy.env` / `entanPyWorker.env`（`values-lumen.yaml` 未覆盖这两张 env 表，改一处即生效；对照 `innovPy.env` 是整表覆盖，需两边同改）。

| 变量 | 默认值 | 放哪 |
|------|--------|------|
| `MILVUS_URI` | `http://10.50.69.111:19530` | 上述 4 处 env |
| `MILVUS_COLLECTION_PREFIX` | `gkxlumen_industry_` | 同上 |
| `MILVUS_TOKEN` | **不设**（现网未开鉴权） | Secret `lumen-algo-milvus`（api/worker 已挂 `secretRef optional:true`；entan 启用鉴权后按 `innovPy` 的 `LLM_API_KEY` 写法加 `secretKeyRef`）。**不进 git** |

2. **前缀必须用下划线**：Milvus 拒绝连字符名，实测 `describe gkxlumen-industry-anchor` → `code 1100 Invalid collection name ... can only contain numbers, letters and underscores`；`gkxlumen_industry_anchor` → `code 100 can't find collection`（合法但未创建，留给 PY-INDEX 建）。同理 `amcpdp-frame` 也被 1100 拒 → 该实例上不可能存在 `amcpdp-` 前缀的 collection。

3. **最小权限**：现网 `authorizationEnabled: false`（`docker exec milvus grep` 实读），无账号体系 → 现在**做不到**账号级收权，任何能连 19530 的进程都是超级权限。本叶交付的是网络与配置层最小面：只给 Python 侧注入变量（Java / 前端未加任何 Milvus 变量，D12 保持），并在 `k8s/README.md` 写死「`create/drop/insert` 只允许发生在 `gkxlumen_industry_` 前缀内，实例上其余 collection（`aip_kb_1` / `aip_kb_2` / `spk_id_speaker_embeddings`）与多媒体帧库一律只读」。账号级收权见升级项 B。

4. **只读探测**：`lumen-algo-py/scripts/milvus_probe.py`（stdlib：socket + urllib，无新依赖）。只做 TCP + `collections/list`；不 create、不 insert、不 drop；前缀非法直接非 0 退出。

**不做**（按派单）：未创建任何 collection（`gkxlumen_industry_*` 仍为空，PY-INDEX 的活）；未动多媒体检索；未改 Java / 前端；未点 `helm:deploy`。

## 偏离

| # | 偏离 | 理由 / as-built |
|---|------|-----------------|
| 1 | 地址不用总控 §0 #4 的 `192.168.88.48:19530`，改为 `10.50.69.111:19530` | 88.48（`htsvr048`）上 **无 Milvus 容器、无进程、19530 无监听**；从 K8s 节点与 4 个 Pod 内探测均 `Connection refused`。若按 #4 落配置，交付的必然是跑不通的死配置。实测 10.50.11.76（`htsvr043`）跑 `milvusdb/milvus:v2.4.0` standalone 且版本与设计稿写的「2.4.0 standalone」完全一致 → 判断为文档 IP 笔误。**地址口径仍须监管人 / 架构确认**（升级项 A），改回只需改这 4 处 env 值。 |
| 2 | collection 前缀写 `gkxlumen_industry_`，不是 03 §0 的 `gkxlumen-industry-` | Milvus 硬校验拒绝连字符（实测 `code 1100`）。设计稿的名字物理上建不出来。SAD 属架构文件，本叶不擅自改，登记为升级项 C。 |
| 3 | 未在集群侧建 NetworkPolicy / Milvus 受限账号 | ns `dev` 当前 **没有任何 NetworkPolicy**（出网默认全通，实测 Pod 可达 19530）；受限账号需先由运维打开 `authorizationEnabled` 并重启 Milvus（影响 `aip_kb_*` 等在用系统）→ 超出本叶权限，升级项 B。 |

未违反硬闸：未对 `amcpdp-*` 做任何操作（该实例上此类名字非法且不存在）；未把口令写进 git；未 force push；探测全程只读。

## 产物清单

- `lumen-algo-py/k8s/api.yaml`、`k8s/worker.yaml`（env + optional Secret 位）
- `lumen-algo-py/k8s/README.md`（Milvus 变量表 / 最小权限 / 探测命令 / 回滚，本叶新增小节）
- `lumen-algo-py/scripts/milvus_probe.py`（只读探测 + `--self-check`）
- `lumen-algo-py/.env.example`（本地 env 契约 2 行）
- `lumen-svc-platform/helm/gkxlumen-platform/values.yaml`（`entanPy.env` / `entanPyWorker.env`）
- 本 handoff

## 验收证据

**探测真实执行过**（`ssh-executor` → dev 节点 `htsvr050`，context `kubernetes-admin@cluster.local`；全部只读）。

1. 现网实例盘点（`10.50.11.76`，`docker ps`）：

```text
milvus        harbor.htmisoft.net/internet/milvusdb/milvus:v2.4.0   Up 34 hours   0.0.0.0:19530->19530/tcp
milvus-minio  minio:latest                                          Up 34 hours
milvus-etcd   quay.io/coreos/etcd:v3.5.0                            Up 34 hours
```

`192.168.88.48`（总控写的地址）：`NO_MILVUS_CONTAINER` / `NO_MILVUS_PROC` / `NO_19530_LISTEN`。

2. Pod 内出网（4 个 Deployment 全过，`python -c` socket 探测）：

```text
=== lumen-platform-algo-py ===            10.50.11.76 19530 TCP_OK   | 192.168.88.48 19530 TCP_FAIL ConnectionRefusedError
=== lumen-platform-algo-py-worker ===     10.50.11.76 19530 TCP_OK   | 192.168.88.48 19530 TCP_FAIL ConnectionRefusedError
=== gkxlumen-platform-entan-py ===        10.50.11.76 19530 TCP_OK   | 192.168.88.48 19530 TCP_FAIL ConnectionRefusedError
=== gkxlumen-platform-entan-py-worker === 10.50.11.76 19530 TCP_OK   | 192.168.88.48 19530 TCP_FAIL ConnectionRefusedError
```

3. 本叶脚本在 **Pod 内**跑（`kubectl cp` 到 `/tmp` 执行后已删除，未留残留）：

```text
TCP 10.50.69.111:19530 ok
collections=3 本前缀(gkxlumen_industry_)=尚未创建
只读不动（禁止 drop/insert）：['aip_kb_1', 'aip_kb_2', 'spk_id_speaker_embeddings']
exit=0
```

节点上跑总控冻结地址：`FAIL TCP 192.168.88.48:19530 不通：ConnectionRefusedError` → `exit=1`（脚本诚实红，不伪造成功）。

4. 名字规则与鉴权（只读 `describe` / 读配置）：

```text
describe gkxlumen-industry-anchor → {"code":1100,"message":"Invalid collection name ... only contain numbers, letters and underscores"}
describe gkxlumen_industry_anchor → {"code":100,"message":"can't find collection[database=default][collection=gkxlumen_industry_anchor]"}
describe amcpdp-frame            → {"code":1100,"message":"Invalid collection name ..."}
/milvus/configs/milvus.yaml:586  → authorizationEnabled: false
```

5. 脚本自检（本机，不连网）：`python scripts/milvus_probe.py --self-check` → `self-check ok`（exit 0）。

6. 未写入证明：全程只用 `collections/list` / `collections/describe` 与 TCP connect；`gkxlumen_industry_*` 至今 **0 个** collection（见证据 3），`aip_kb_*` / `spk_id_*` 三个 collection 名单前后一致，未 drop / 未 insert。

## 问题清单 / 开放项（升级给 `human:淮政玮`）

| # | 事项 | 谁做 | 状态 |
|---|------|------|------|
| A | **地址口径**：总控 §0 #4 / 01 §2.1 / 02 §2 / 03 §0 的 `192.168.88.48:19530` 与现网不符，请拍板改为 `10.50.69.111:19530`（或指出另有一台 88.48 上的实例待运维恢复） | 淮政玮 + 架构（李伟 / 徐滕强） | 🟡 |
| B | **最小权限落地**：现网 `authorizationEnabled=false`。要真正做到「产业账号不能 drop 别人的 collection」，需运维开鉴权 + 建受限角色（`gkxlumen_industry_*` 的 CRUD，其余只读），并把口令放 Secret `lumen-algo-milvus`。开鉴权会影响同实例在用系统（`aip_kb_*` 等），须运维窗口 | 运维 + 淮政玮 | 🟡 |
| C | **collection 命名修订**：03 §0 的 `gkxlumen-industry-*` 物理非法，建议改写为 `gkxlumen_industry_*`（本叶 env 已按合法名） | 架构（SAD 属他们的文件） | 🟡 |
| D | **entan 生效时机**：helm values 已改，但未点 `helm:deploy`（前叶 `DEVOPS-LUMEN-INNOV-ENTAN-PIN-SHA-L01` 明令只点 `helm:chart`）。entan Pod 拿到 `MILVUS_URI` 需一次 helm upgrade 或 `kubectl set env`；在 PY-INDEX 把向量代码放进 entan 镜像之前**不影响**任何功能 | devops + 淮政玮 | 🟡 |
| E | 同实例还有 88.49 / 88.54 / 88.249 三台 19530（88.54 像多媒体 / 资产库：`clip_image_collection` / `assets*`）。本叶配置**不指向**它们；若甲方口中的「`amcpdp-*` 帧库」在 88.54，需另行确认后写入盘点，不要凭文档 | 架构 + 数据 | 🟡 |

## 修改内容

| 文件 | 改了什么 |
|------|----------|
| `k8s/api.yaml` / `k8s/worker.yaml` | `MILVUS_URI` + `MILVUS_COLLECTION_PREFIX` 两个 env；`envFrom` 追加 `secretRef: lumen-algo-milvus optional:true`（鉴权位） |
| `helm/.../values.yaml` | `entanPy.env` / `entanPyWorker.env` 各加同两个 env（含最小权限注释） |
| `scripts/milvus_probe.py` | 新增：TCP + list collections 只读探测，前缀非法 / 不通均非 0 退出，`--self-check` 校验名字规则与 URI 解析 |
| `k8s/README.md` | 新增「Milvus 向量库（产业锚点）」小节：变量表、env 真源、最小权限、Pod 内探测命令、回滚 |
| `.env.example` | 本地 env 契约 2 行（口令仍不写） |

## 测试结果

- `python scripts/milvus_probe.py --self-check` → `self-check ok`（本机 + 节点各跑一次，均 exit 0）
- 节点 / 4 个 Pod 内探测 10.50.11.76:19530 → 全 OK；88.48:19530 → 全 refused（脚本 exit 1）
- 未跑仓内 pytest（本叶未改 Python 业务代码；`scripts/` 不在 `py:test` 的 compileall 范围，脚本已由 `--self-check` 覆盖）

## 遗留风险

- 地址在监管人拍板前属「实测优先」状态：若 A 判定要用 88.48，需运维先把实例拉起来，届时只改 4 处 env 值 + README。
- 鉴权未开 → PY-INDEX 的代码守卫是唯一防线：**必须**在客户端侧校验 collection 名以 `MILVUS_COLLECTION_PREFIX` 开头才允许 create/drop/insert，否则一次手滑可以删掉 `aip_kb_*`。
- 该实例与其他系统共用 etcd / minio（`milvus-etcd` / `milvus-minio` 容器），quota 与备份口径未约定（对应 VEC-Q1b，仍 🟡）。
- entan Pod 未 rollout（见升级项 D）。

## CI/CD（必填）

- 分支：`lumen-algo-py` `origin/dev`、`lumen-svc-platform` `origin/dev`（均非 force）
- commit：`lumen-algo-py` `9019505`；`lumen-svc-platform` `bea173e`
- pipeline URL / ID：push 触发 GitLab CI；`lumen-algo-py` dev 自动 `deploy:api` / `deploy:worker`（新 env 随 manifest apply 生效）；`lumen-svc-platform` **未点** `helm:deploy`
- 部署 namespace / 镜像 tag：`dev`；`gkx-lumen-algo-py-api:9019505f` / `gkx-lumen-algo-py-worker:9019505f`
- K8s rollout：**成功**（api + worker `successfully rolled out`；entan 未 rollout，见升级项 D）
- dev 测试 URL / 命令与结果：

```text
kubectl -n dev exec deploy/lumen-platform-algo-py        -- printenv MILVUS_URI MILVUS_COLLECTION_PREFIX
  → http://10.50.69.111:19530 / gkxlumen_industry_
kubectl -n dev exec deploy/lumen-platform-algo-py-worker -- printenv MILVUS_URI MILVUS_COLLECTION_PREFIX
  → http://10.50.69.111:19530 / gkxlumen_industry_
# 新 Pod 只用注入的 env 走一次只读 list（不建库不写向量）
kubectl -n dev exec deploy/lumen-platform-algo-py -- python -c "…collections/list…"
  → {'code': 200, 'data': ['spk_id_speaker_embeddings', 'aip_kb_1', 'aip_kb_2']}
```

## 可观测性（建议）

- OTEL_SERVICE_NAME：未改（`lumen-platform-algo-py` / `-worker` / `gkxlumen-entan-py-api` / `-worker` 保持）
- traceId（dev 抽样）：无（本叶未加 HTTP 接口）
- Tempo / Loki：无新埋点。PY-INDEX 落 `/internal/industry/embed/*` 时按仓内 `observability` 惯例埋 span，并把 `MILVUS_URI` 作为 span 属性时**只记 host:port，不记口令**

## 涉及文件

- `lumen-algo-py/k8s/api.yaml`
- `lumen-algo-py/k8s/worker.yaml`
- `lumen-algo-py/k8s/README.md`
- `lumen-algo-py/scripts/milvus_probe.py`
- `lumen-algo-py/.env.example`
- `lumen-svc-platform/helm/gkxlumen-platform/values.yaml`
- 本 handoff

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 只给 Python 进程注入 Milvus 变量；Java / 前端零改动 |
| 调用链不可越层 | ✅ 仍 FE → GW → Java → Python `/internal` → Milvus；未给 Java / 前端任何 19530 通道 |
| 图谱仅 Nebula | ✅ 未动 `10.50.75.136:9669` / space `demo_gkx_chain`；向量不替代建图 |
| 可观测 | ✅ 未破坏现有 OTel env；本叶无新接口（埋点交 PY-INDEX，已在上文写明约束） |
| CI/CD | ✅ 两仓 push `origin/dev`，未 force，未点 `helm:deploy` |
| demo2 不 merge lumen（D12） | ✅ 未改任何 `demo-*` 仓 / 镜像 / 服务；lumen 仍只连 `gkxlumen-*` 与算法自有下游 |
| 数据策略 | ✅ 未建 collection、未写向量、未碰 `amcpdp-*` / `aip_kb_*` / `spk_id_*`；未写正式 `gkxlumenx_*` |
| 密钥不入 git | ✅ 现网未开鉴权，无口令可写；鉴权位走 optional Secret，文档与 handoff 均无明文 |
| D8 / D9 / D10 | N/A（无 UI / 无指标卡） |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 118000 |
| model_used | claude-opus-5-thinking |
| actual_cost | 0.71 |
| cost_warn | green |

口径：devops 默认 75/25 读写比；B 档 `$3/$15` per 1M；`118000×0.75×3/1e6 + 118000×0.25×15/1e6 = 0.71`。
