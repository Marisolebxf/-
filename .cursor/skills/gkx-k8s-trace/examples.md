# gkx-k8s-trace 样例

## A. 接通并查 ns

```text
# MCP CallDynamicTool user-ssh-executor / ssh_execute
connectionId: zphz-jump
command: |
  nohup sudo bash -c 'cp /root/.kube/config /tmp/admin-kc.yaml && chown $(id -u):$(id -g) /tmp/admin-kc.yaml && chmod 600 /tmp/admin-kc.yaml' >/tmp/sudocp.log 2>&1 &
  sleep 2
  export KUBECONFIG=/tmp/admin-kc.yaml
  kubectl get ns | head -20
```

## B. 拉 trace + 摘要

```bash
export KUBECONFIG=/tmp/admin-kc.yaml
TID=f5c12eb92266a588a7941a454330f97f
timeout 20 curl -s "http://10.50.69.111:30200/api/traces/$TID" -H 'Accept: application/json' > /tmp/trace.json
# 把 trace-summarize.py 内容 scp / 粘贴到 /tmp 后：
python3 /tmp/trace-summarize.py /tmp/trace.json
```

## C. 2026-10-29 产业链重建结论样例

- Trace：`f5c12eb92266a588a7941a454330f97f`
- 链路：`gkx-gateway` → `gkx-innov` `POST /v1/industry/internal/run-chain-pipeline` 200 → `gkx-innov-py` `POST /internal/run-chain-pipeline`
- 数据：码表 `chainan/llm_ods/generate.py` → 灌 Demo ODS → 模拟 GDF → DWD → ADS；**不是**读三方真源 ODS
- 观测瑕疵：HTTP server span ~2.6ms 先关，后台 TRUNCATE/INSERT 数百 ms（daemon 线程）
