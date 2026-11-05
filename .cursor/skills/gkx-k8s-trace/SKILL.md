---
name: gkx-k8s-trace
description: >
  Connect to GKX K8s via SSH MCP jump host and investigate OTel traces by
  traceId (Tempo/Loki/Grafana). Use when the user mentions K8s、kubectl、
  jumpserver、zphz-jump、traceId、Tempo、Loki、Grafana 排查、链路不通、
  or observability debugging. Never kubectl from the laptop; never leave
  kubeconfig copies on the jump host.
---

# GKX K8s 跳板连接 + Trace 排查

本机**不能**直连集群。`user-kubernetes` MCP 常不可用。标准路径 = **SSH MCP → jumpserver → kubectl / Tempo API**。

## 何时用

- 要跑 `kubectl` / 查 pod / svc / NodePort
- 用户给了 **traceId**（32 位 hex）要查链路
- Grafana / Tempo / Loki 地址不清楚，或旧 `192.168.88.34:3000` 已废弃

只改代码、不碰运行态 → 不用本 skill。

## 0. 铁律

1. **禁止**本机 `kubectl`（本机通常未装或无凭证）
2. **禁止**把 kubeconfig / 证书内容贴进对话或 commit
3. 作业完 **立刻删** 跳板机 `/tmp` 下的 kubeconfig 副本
4. `user-kubernetes` MCP 若 `needsAuth` / discovery 失败 → **不要死磕**，走 SSH 路径

## 1. 一分钟接通（照抄）

MCP 命名空间：`user-ssh-executor`。先 `GetDynamicTools`，再调用。

```
1) ssh_list_connections
   → 已有 connectionId（常见 zphz-jump）直接用
   → 没有则 ssh_list_servers → ssh_connect（服务器名常见 zphz-jump / jumpserver.zphz.cn）

2) 准备 kubeconfig（sudo 前台会挂住，必须用 nohup 后台）:
   nohup sudo bash -c 'cp /root/.kube/config /tmp/admin-kc.yaml && chown $(id -u):$(id -g) /tmp/admin-kc.yaml && chmod 600 /tmp/admin-kc.yaml' >/tmp/sudocp.log 2>&1 & echo LAUNCHED
   sleep 1～2s 后再 ls /tmp/admin-kc.yaml

3) 验证:
   export KUBECONFIG=/tmp/admin-kc.yaml
   kubectl get ns | head
```

### 已知坑（不要再试错）

| 现象 | 原因 | 做法 |
|---|---|---|
| 裸 `kubectl` → Authentication required | 当前用户无 `~/.kube/config` | 用 `/root/.kube/config` 副本 |
| `sudo cp` / `sudo -n true` **超时挂死** | sudoers `use_pty` + MCP 非交互 | **`nohup sudo bash -c '…' &`** |
| `sudo cat /etc/kubernetes/kubelet.conf` 有时能出 | 有输出的 sudo 偶发可过 | 仍优先用 nohup 模式 |
| `user-kubernetes` mcp_auth 30s 超时 | MCP 服务挂了 | 改走本 skill SSH 路径 |
| `ssh_execute` 超时 / 卡住 | **多半是命令慢**，不是 SSH 断了 | 缩短命令 + `timeout N` 再试 **1** 次；**禁止** `echo alive` 探活循环（见 `ssh-executor-authorized.mdc`） |
| 跳板机上扫 NodePort / 集群 DNS 不通 | 跳板机 **不在** Pod 网 | 用 `kubectl`/`sudo kubectl --kubeconfig=…` 查 svc/endpoints；不要在跳板机本机瞎扫端口当「连不上」 |

跳板机现状参考（会变，以现场为准）：主机常为 `node01` / `10.50.69.111`；用户如 `huaizhengwei_*`，`sudo -l` 为 `(ALL) NOPASSWD: ALL`。配置服务器名以 `ssh_list_servers` 为准（常见仅 `zphz-jump`）。

## 2. 可观测栈速查（ns）

在跳板机上（已 export KUBECONFIG）：

```bash
# 找 Grafana / Tempo / Loki / OTel
for ns in zhipu-tts zp-tts monitoring; do
  echo "== $ns =="
  kubectl get svc -n $ns | grep -iE 'grafana|tempo|loki|otel' || true
done
```

**2026-10-29 实测（NodePort 挂在 10.50.69.111）**：

| 用途 | 位置 | NodePort |
|---|---|---|
| Grafana（新） | `ns=monitoring` `grafana` | **31300** |
| Tempo Demo | `ns=zhipu-tts` `demo-platform-tempo` | **30200** |
| Tempo Lumen | `ns=zhipu-tts` `gkxlumen-platform-tempo` | **30202** |
| Loki Demo | `ns=zhipu-tts` `demo-platform-loki` | 30310 |
| Loki Lumen | `ns=zhipu-tts` `gkxlumen-platform-loki` | 30311 |

旧 Grafana `192.168.88.34:3000` = **已清理，勿再连**。

demo 链路服务名常见：`gkx-gateway` / `gkx-innov` / `gkx-innov-py`（pod 前缀 `demo-platform-innov*`）。lumen 对应 `gkxlumen-platform-*`。

## 3. 按 traceId 排查（标准流程）

输入：32 位 hex，如 `f5c12eb92266a588a7941a454330f97f`。

### 3.1 拉全量 trace（先 Demo Tempo，再 Lumen）

```bash
TID=f5c12eb92266a588a7941a454330f97f
# Demo
timeout 20 curl -s "http://10.50.69.111:30200/api/traces/$TID" -H 'Accept: application/json' > /tmp/trace.json
# 空则试 Lumen
# timeout 20 curl -s "http://10.50.69.111:30202/api/traces/$TID" ...
```

有数据时 `/api/search?tags=traceID=$TID` 可能仍空——**直接打 `/api/traces/{id}`**。

### 3.2 压成 span 树（跳板机 python3）

把 JSON 里的 base64 `spanId`/`parentSpanId` 解成 hex，按 `service.name` + duration + name 打印。关注：

1. **入口服务 / HTTP 路由 / status_code**
2. **跨语言是否同 traceId**（gateway → Java → Python）
3. **DB 操作序列**（TRUNCATE / INSERT / SELECT）→ 判断写的是 ODS/DWD/ADS 哪层
4. **短 HTTP span + 长后台 SQL**：常见是 daemon 线程异步跑 pipeline（HTTP 先 200），属设计行为不是断链

模板脚本见 [trace-summarize.py](trace-summarize.py)（拷到跳板 `/tmp` 跑，或 `python3 -c` 内联）。

### 3.3 对照代码

| Trace 信号 | 去哪读代码 |
|---|---|
| `POST …/run-chain-pipeline` | `demo-algo-science/api/main.py` → `scripts/run_all.py` → `chainan/llm_ods/` |
| `POST …/policy/sync-ods` | `demo-algo-ent-analysis/polan/ods_sync.py` |
| 只有 TRUNCATE+INSERT ODS、无外部 SELECT 三方库 | 可能是**码表灌数**而非真源贴源 |

### 3.4 Loki（可选）

NodePort 或 Grafana Explore LogQL：`{service_name=~".+"} |~ "<traceId>"`。

## 4. 收工清单

```bash
rm -f /tmp/admin-kc.yaml /tmp/sudocp.log /tmp/trace.json
```

对话里只保留：**结论 + 服务链 + 关键 span 名/耗时/HTTP 码**，不贴证书、不贴整段 kubeconfig。

## 5. 给用户的最短结论模板

```
链路：✅/❌  gateway → {java} → {python}  同 traceId={…}
入口：{METHOD path} → HTTP {code}  ({dur}ms)
关键步骤：…
数据源判断：真源 ODS / 码表 / 仅读 ADS …（依据 span+代码）
瑕疵：异步 pipeline 导致 parent span 早关 / …
Tempo：Demo :30200 或 Lumen :30202；Grafana :31300
```

## 附加

- 更长的 curl / python 样例：[examples.md](examples.md)
- 架构约定：`agent-delivery/architecture-baseline.md` 可观测节；UI 深链 helper 在各前端 `observability.ts`（旧默认 Grafana 地址已过时，以本 skill §2 为准）
