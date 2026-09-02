# 跳板 SSH MCP + 现网 K8s 调试（团队上手）

> **给谁看**：要查 demo 现网部署、网关路由、Pod 日志、链路的同事（联调 / 后端 / 算法 / DevOps / QA）  
> **做什么**：本机 Cursor 挂 `ssh-executor`，经跳板 SSH 进现网机，再 `kubectl` / 查库 / 打探测  
> **上游工具**：[mcp-ssh-executor](https://github.com/gulbelhuai/mcp-ssh-executor)（本机 clone 后启动，不是远程托管 MCP）  
> **不要和这些混淆**：编排仓必挂的 `task-registry` / `metric-registry`；本机 `kubernetes` MCP（多数笔记本打不到现网 API）  
> **口令**：跳板密码向架构师 / 运维领取。**本文、飞书、git、聊天、handoff 一律不写明文。**

---

## 0. 为什么要装这个

本机直接挂 `kubernetes` MCP，常见会连到内网 API（例如 `172.18.3.194`），笔记本超时。  
现网能从外网进去的入口是 **SSH 跳板**，不是本机 kubeconfig。

| 入口 | 地址 | 是什么 | 能不能当管理后台 / 改路由 |
|------|------|--------|---------------------------|
| 跳板 SSH | `111.198.38.90:50122` | 现网跳板（机名常见 `htsvr050`） | 上去后 `kubectl`、看日志、改 demo 库 |
| 联调台 | `http://111.198.38.90:50100` | `demo-ui-system-test` | 只是前端联调台，**不是** PigX 管理后台 |
| 外网 Nacos `50148` | lumen Nacos | dataId 已是 `gkxlumen-gateway-dev.yml` | **禁止**往这里贴 demo 路由（D12） |
| 本机 kubernetes MCP | 内网 API | 多数人连不上 | 装了也查不到现网 |

demo 网关业务路由运行时真源：

```text
gkxx.sys_route_conf  →  UPMS 灌 Redis `gl:gateway_route_key`  →  网关内存
```

只改 Nacos yml、只重启网关，**经常不生效**。要改正式链路径，改 `gkxx` 这张表，再重启 `demo-platform-upms` + `demo-platform-gateway`。

---

## 1. 一次性准备

| 项 | 要求 |
|----|------|
| Node.js | **18+**（`node -v`） |
| Cursor | 能打开 MCP 面板（插头图标） |
| 跳板账号 | `root@111.198.38.90:50122`，口令当面/私聊领取 |
| 本机目录 | 自选。示例：`~/tool/mcp-ssh-executor`（不要提交到业务仓） |

**每人自己生成主密钥、自己加密密码。**  
`servers.json` 里的密文绑定你自己的 `MCP_SSH_MASTER_KEY`。不要互拷别人的 `servers.json`，除非同时拿到对方主密钥（不推荐，等于共享口令保险柜钥匙）。

---

## 2. 下载并编译

macOS / Linux：

```bash
mkdir -p ~/tool
cd ~/tool
git clone https://github.com/gulbelhuai/mcp-ssh-executor.git
cd mcp-ssh-executor
npm install
npm run build
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\tool"
Set-Location "$HOME\tool"
git clone https://github.com/gulbelhuai/mcp-ssh-executor.git
Set-Location mcp-ssh-executor
npm install
npm run build
```

确认存在 `dist/index.js`。`servers.json`、`.master-key` 已被 `.gitignore`，不要 `git add`。

---

## 3. 生成主密钥 + 加密跳板密码

在项目根执行（先不要把密码写进命令历史，交互输入更安全）：

```bash
cd ~/tool/mcp-ssh-executor   # Windows: $HOME\tool\mcp-ssh-executor

# 1) 生成主密钥，整段复制保存（只放本机）
npm run encrypt-password generate-key
```

记下输出的那一长串 hex，后面叫 **主密钥**。

```bash
# 2) 把主密钥放进当前终端（仅本次会话）
export MCP_SSH_MASTER_KEY="你刚刚生成的主密钥"
# Windows: $env:MCP_SSH_MASTER_KEY = "你刚刚生成的主密钥"

# 3) 交互加密（不要把明文密码写在命令行参数里）
npm run encrypt-password
```

按提示输入跳板密码，得到 `passwordEncrypted` 那一长串。

也可让 Cursor Agent 调 MCP 工具 `ssh_generate_master_key` / `ssh_encrypt_password`，效果相同。

---

## 4. 写 `servers.json`

```bash
cp servers.example.json servers.json
```

改成**只有现网跳板这一条**（server 名请统一用 `gkx-k8s`，方便大家跟 Agent 说同一套话）：

```json
{
  "servers": {
    "gkx-k8s": {
      "host": "111.198.38.90",
      "port": 50122,
      "username": "root",
      "passwordEncrypted": "上一步生成的密文"
    }
  },
  "masterKeyEnv": "MCP_SSH_MASTER_KEY"
}
```

权限（macOS / Linux）：

```bash
chmod 600 servers.json
```

不要用示例里的明文 `password` 字段。不要把这份文件发到飞书群。

---

## 5. 挂到 Cursor（用户级 MCP，不要写进编排仓）

打开 **Cursor 用户级** MCP 配置：

- macOS：`~/.cursor/mcp.json`
- Windows：`%USERPROFILE%\.cursor\mcp.json`

在已有 `mcpServers` 里**追加**（保留你原来的 `task-registry` 等），把路径换成你本机的绝对路径：

```json
{
  "mcpServers": {
    "ssh-executor": {
      "command": "node",
      "args": [
        "/Users/你的用户名/tool/mcp-ssh-executor/dist/index.js"
      ],
      "env": {
        "MCP_SSH_MASTER_KEY": "你的主密钥",
        "MCP_SSH_CONFIG_PATH": "/Users/你的用户名/tool/mcp-ssh-executor/servers.json"
      }
    }
  }
}
```

Windows 路径示例：`C:\\Users\\你的用户名\\tool\\mcp-ssh-executor\\dist\\index.js`（JSON 里反斜杠要转义）。

**不要**写进 `gkx-orchestration/.cursor/mcp.json`：那里是团队可移植配置，禁止塞本机绝对路径和密钥。

然后：

1. 保存 `mcp.json`
2. 打开 Cursor **MCP 面板**，看 `ssh-executor` 是否绿
3. 不绿就 **Reload MCP** 或重启 Cursor
4. 绿了应能看到：`ssh_connect` / `ssh_execute` / `ssh_list_servers` / `ssh_list_connections` 等

本会话若刚加配置、Agent 还调不到这些工具：重开一个 Agent 聊天再试。

---

## 6. 第一次连通（5 分钟自检）

对新开的 Agent 说：

```text
用 ssh-executor 连 gkx-k8s，执行：
1. hostname
2. kubectl config current-context
3. kubectl -n dev get deploy | egrep 'demo-platform-(gateway|upms|innov|entan-py)'
不要打印任何密码。
```

期望：

| 检查 | 正常结果 |
|------|----------|
| 能连上 | `ssh_connect(serverName: "gkx-k8s")` 成功 |
| 主机 | 类似 `htsvr050` |
| kube context | `kubernetes-admin@cluster.local` |
| namespace | 业务在 **`dev`** |
| 四个 Deployment | `demo-platform-gateway` / `upms` / `innov` / `entan-py` 都 Running |

手动等价（Agent 调 `ssh_execute`）：

```bash
hostname
kubectl config current-context
kubectl -n dev get deploy,po -l app.kubernetes.io/name --no-headers 2>/dev/null | head
kubectl -n dev get deploy | grep demo-platform
```

---

## 7. 现网怎么查（给 Agent 的常用话术）

先说清 **只动 demo、不动 lumen**。

### 7.1 看部署 / 日志

```text
连 gkx-k8s，查 ns=dev：
- demo-platform-gateway / upms / innov / entan-py 的 READY 和最近一次 rollout
- gateway、upms 最近 200 行日志，只摘路由加载、报错
```

常用命令：

```bash
kubectl -n dev get deploy demo-platform-gateway demo-platform-upms demo-platform-innov demo-platform-entan-py
kubectl -n dev rollout status deploy/demo-platform-gateway --timeout=120s
kubectl -n dev logs deploy/demo-platform-upms --tail=200 | grep -E '加载路由|gkx-comp-graph|ERROR'
kubectl -n dev logs deploy/demo-platform-gateway --tail=200 | grep -E '加载路由|gkx-comp-graph|ERROR'
```

### 7.2 看 demo 网关路由是否在库里

库是 **`gkxx`**（不是 `gkxlumenx`）。MySQL 在内网 `192.168.88.43`。口令从 **upms Pod 环境变量**取，不要写进文档：

```bash
kubectl -n dev exec deploy/demo-platform-upms -- printenv MYSQL_HOST MYSQL_PORT MYSQL_DATABASE MYSQL_USERNAME
# 密码：printenv MYSQL_PASSWORD   ← 只在跳板上用，禁止回传到聊天
```

查路由（在跳板上用客户端连 88.43，库 `gkxx`）：

```sql
SELECT route_id, uri, sort_order, predicates, filters
FROM sys_route_conf
WHERE route_id LIKE 'gkx-%'
ORDER BY sort_order, route_id;
```

综合图谱正式链应有 `gkx-comp-graph` → `lb://gkx-innov`，Path 含 `/industry-comp/v1/comp/graph**`，**filters 为空（不要 StripPrefix）**。

### 7.3 外网打一枪（笔记本浏览器 / curl 即可）

```bash
curl -sS "http://111.198.38.90:50100/api/industry-comp/v1/comp/graph?limit=2"
curl -sS "http://111.198.38.90:50100/api/entan/internal/comp/graph?limit=1"
```

怎么读结果：

| HTTP | 含义 |
|------|------|
| **404** 且 msg 带 `industry-comp/` | 网关没匹配到动态路由（表 / Redis / 网关内存没刷） |
| **424** `token expired` | 路由已通，打到了 `gkx-innov` 鉴权（UI 带登录态可过） |
| **200** + `op_id` | 到了业务（`/entan/internal` 常见已白名单） |

### 7.4 改路由时的标准顺序（demo only）

1. `INSERT` / `UPDATE` **`gkxx.sys_route_conf`**（id 自拟、不要碰 lumen 库）
2. `kubectl -n dev rollout restart deploy/demo-platform-upms`
3. 等 UPMS 日志出现 `加载路由ID：<你的 route_id>`
4. `kubectl -n dev rollout restart deploy/demo-platform-gateway`
5. 等 gateway rollout 绿，再 curl 外网 `50100`

只改 Nacos、只重启网关 = 不够。不要开 `nacosConfigInit.runOnUpgrade`。

---

## 8. 红线（违反就停）

1. **禁止**把跳板 / MySQL / Redis 明文密码写进聊天、handoff、git、飞书文档。
2. **禁止**改 `gkxlumenx`、`gkxlumen-platform-*`、外网 Nacos `50148` 里的 lumen 路由（D12：demo 不进正式）。
3. **禁止** `git push --force`，禁止把 `servers.json` / `.master-key` / 用户 `mcp.json` 提交到任何仓。
4. **禁止**在跳板上对生产库做无备份的 `DELETE` / `DROP`。改 `sys_route_conf` 先 `SELECT` 确认库名是 `gkxx`。
5. 本机 `kubernetes` MCP 连不上现网是正常的，不要改集群证书来“迁就”笔记本。

---

## 9. 排障

| 现象 | 先查 |
|------|------|
| MCP 面板没有 `ssh-executor` | 用户级 `mcp.json` 路径是否绝对路径；`dist/index.js` 是否已 build；重启 Cursor |
| `decrypt failed` / 连不上认证失败 | 主密钥和加密时用的不是同一把；重新 `encrypt-password` |
| SSH 超时 | 公司网是否放行 `111.198.38.90:50122`；别写成 22 端口 |
| `kubectl` 不是现网 | `kubectl config current-context` 应为 `kubernetes-admin@cluster.local` |
| 改了 Nacos 仍 404 | 去 `gkxx.sys_route_conf` + 重启 UPMS **再**重启 gateway |
| Agent 说没有 ssh 工具 | 当前聊天开在加 MCP **之前**，新开一个 Agent 会话 |

---

## 10. 和本机 kubernetes MCP 的分工

| | `ssh-executor`（本文） | 本机 `kubernetes` MCP |
|--|------------------------|------------------------|
| 连谁 | 跳板 `111.198.38.90:50122`，再在那台上 `kubectl` | 本机 kubeconfig / 内网 API |
| 谁该装 | **要查现网的人都装** | 仅当你本机已经能直连集群时有用 |
| 改库 / 刷 Redis | 跳板上做 | 通常做不到 |

装好后，对 Agent 一句话就够：

```text
用 ssh-executor 连 gkx-k8s，只动 ns=dev 的 demo-platform-*，不要碰 gkxlumen*。
```

---

## 11. 参考

| 文档 | 用途 |
|------|------|
| 本仓 `agent-delivery/architecture-baseline.md` § D12 | demo / lumen 隔离 |
| 上游 `mcp-ssh-executor/README.md` | 工具全集、异步任务、上传文件 |
| `agent-delivery/task-mcp-usage-guide.md` | 任务看板 MCP（另一套，必挂） |
| 综合图谱联调手记 | `agent-handoffs/算法库联调-ALGO-LIB/DEMO-COMP-GRAPH-TRIPLE-UI-L01.md`（S3-1 已按本文改库刷路由） |

口令领取：找架构师。配好后在 MCP 面板截一张「`ssh-executor` 已绿」给 mentor 即可，**不要**截主密钥或 `servers.json`。
