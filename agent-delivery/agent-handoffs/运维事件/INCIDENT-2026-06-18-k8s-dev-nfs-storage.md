# P0 事故报告：dev K8s 集群控制面瘫痪（根因 NFS 存储 IO 崩溃）

- **事故级别**：P0（dev 集群控制面不可用，影响 CI/CD 自动部署与 demo2 预览更新）
- **发生时间**：2026-06-17 约 22:14 起，持续至 2026-06-18 凌晨（进行中）
- **影响范围**：dev K8s 集群（`api.k8s.htmi.tech:6443`）控制面间歇/持续不可用
- **根因**：NFS 共享存储（`NFS100-SSD` / TrueNAS 后端）IO 性能崩溃，拖垮所有 master 的 etcd
- **诊断/处置**：AI agent 经 SSH（仅 K8s 节点，未触碰存储/虚拟化平台）逐层定位
- **状态**：网络/VIP 层已修复并加固；**核心根因（NFS）待运维处理**，已交接

---

## 1. 集群拓扑（事后查明）

| 角色 | 节点 | 管理 IP | 备注 |
|---|---|---|---|
| control-plane | htsvr050 | 192.168.88.50 | etcd1 `7091a7ecb1386a6b` |
| control-plane | htsvr051 | 192.168.88.51 | etcd2 `2e0e2fc07d1bcbad`；**VIP 现钉在此** |
| control-plane | htsvr052(hostname htsvr100) | 192.168.88.52 | etcd3 `113e04d41b1efd37` |
| worker | htsvr053/076/077/078/079 | — | 5 节点 |

- **API 入口**：`api.k8s.htmi.tech → 192.168.88.100`（control-plane VIP）
- **VIP 管理**：kube-vip（ARP + leader election，`plndr-cp-lock`），**长期 CrashLoopBackOff 265+ 次/151 天**
- **etcd**：external，systemd 管理，3 成员，证书 `/etc/ssl/etcd/ssl/`
- **存储**：所有 master 的 vmdk 位于 **`NFS100-SSD`** datastore（VMware，MAC 前缀 00:50:56；后端 TrueNAS NFS，见 `truenas_nfs_v41`）

---

## 2. 现象演变时间线

| 时间 | 现象 | 当时报错精确含义 |
|---|---|---|
| 22:14 | kubectl 全断，CI Job #16294 `cluster-info` timeout | `no route to host`：VIP 88.100 未绑在任何网卡 |
| 22:50 | 手动 `ip addr add 88.100/24` 到 50，短暂恢复 | 误判为"IP 丢失"，实为存储好窗口 |
| 23:31+ | 再次 `connection refused` / `unexpected EOF` | VIP 在坏节点 / etcd 抖动 |
| 23:39 | etcd `failed to commit proposal`，term 148→152→153 持续选举 | etcd 无 quorum |
| 23:40 | iostat：50 磁盘 **0 吞吐却 100% util、fsync 2~5s** | 50 存储 hang |
| 00:09 | 52 启动→etcd 短暂恢复→又垮 | 51/52 磁盘同样慢 |
| 00:38 | iostat 三台对比 + iotop：master 本机写入仅 KB/s | **确证：master 是受害者，非肇事者** |
| 00:50 | vCenter 截图：master vmdk 全在 `NFS100-SSD` | **根因锁定：NFS 后端** |
| 00:54 | 禁用 kube-vip + VIP 钉死 51 | VIP "总丢"问题根治 |
| 01:01 | VIP 稳定，但 apiserver 仍 CrashLoop | 卡点完全收敛到 NFS |

---

## 3. 逐层穿透诊断（关键证据）

### 3.1 网络层（已排除）
- 节点间 ping：0% 丢包、延迟 0.2~0.3ms（优秀）→ 排除网络

### 3.2 etcd 层（表象）
- 频繁选举：raft term 148→152→153 持续增长
- commit 失败：`failed to commit proposal: context deadline exceeded`
- 无 alarm、无 corrupt、DB 仅 35MB → 排除 NOSPACE/数据损坏

### 3.3 磁盘层（中层根因）
| 节点 | %util | w_await | 判断 |
|---|---|---|---|
| 50 | 97%（0吞吐） | 654~855ms | 卡死（最重） |
| 52 | 93% | 432ms | 很慢 |
| 51 | 4.5%（好窗口） | 9ms | 较轻，但 loadavg 7.46、jbd2/runc D-state |
- etcd 要求 fsync <10ms，实测秒级

### 3.4 存储后端（最终根因）
- **iotop 实测**：master 本机写入仅 KB/s（50 本机零 IO 进程却 100% util）
- **结论**：几十 KB/s 的写都要等几百 ms = 底层 NFS 已饱和/故障；master 是受害者
- **vCenter**：所有 master vmdk 在 `NFS100-SSD`（NFS/TrueNAS）→ 后端慢 = 所有 VM 同时慢

---

## 4. 已执行的处置（全部可逆，附回滚方式）

| # | 操作 | 节点 | 可逆方式 |
|---|---|---|---|
| 1 | 手动加/清理 VIP 88.100 | 50 | 已清理，无残留 |
| 2 | `systemctl stop etcd` → 后 `start` | 50 | 已恢复，etcd 现 3 成员 |
| 3 | netplan 持久化 VIP `88.100/32` | 51 | 备份 `99-netcfg-vmware.yaml.bak.20260618_003122` |
| 4 | netplan 修正 `88.100/24→88.52/24`（拆克隆炸弹，未 apply） | 52 | 备份 `*.bak.20260618_003434` |
| 5 | **禁用 kube-vip**（manifest 移走） | 50/51/52 | `mv /root/kube-vip.yml.disabled /etc/kubernetes/manifests/kube-vip.yml` |
| 6 | VIP `88.100/32` 静态钉死 | 51 | netplan + 运行时，重启不丢 |

### 附带发现并修复的隐患
- **52 netplan 克隆炸弹**：`99-netcfg-vmware.yaml` 误写 `192.168.88.100/24`（应为 `.52`）。52 一旦重启/apply 会抢 VIP 并丢失自身 etcd peer 地址 → 已改正（待 apply）。
- **kube-vip 长期 CrashLoop**：265+ 次/151 天，VIP 实际一直靠手动/残留 IP 维持，并非真正 HA。

---

## 5. 待办清单（交接运维，P0）

### 🔴 P0 — 唯一根因：NFS100-SSD / TrueNAS 存储
1. 登录 **TrueNAS**：`zpool status`（坏盘/resilver/scrub）、CPU、ARC 命中率、网络带宽
2. **vCenter → NFS100-SSD datastore 监控**：延迟（正常 <20ms）、哪台 VM 在狂打 IO
3. 重点怀疑：scrub/resilver 在跑、快照风暴、或同 datastore 某 VM 狂写拖垮 NFS
4. **存储延迟恢复后，etcd 自动稳定 → apiserver 自愈 → 集群恢复**（VIP 已钉好，无需额外操作）

### 🟡 P1 — 存储恢复后补做
- 52 上执行 `netplan apply`（验证 netplan 修复；当前文件已对、重启已安全）
- 评估 kube-vip 根治或更换 HA 方案（kube-vip 长期 crash，当前为静态单点 VIP，无自动故障转移）
- 核对 worker 节点（53/76-79）netplan 是否同样有 `100` 克隆残留

### 🟢 可选高危应急（仅 NFS 短期无法修复且急需集群可用时）
- 51 上 etcd `--force-new-cluster` 降单成员（先备份 etcd 数据目录）：commit 只需 51 自身 fsync，绕开多数派等待。有损（丢冗余）、高危。

---

## 6. 当前状态基线

- ✅ **VIP 88.100 稳定钉死在 51**，重启不丢（kube-vip 已禁用，无人再删）
- ✅ etcd 3 成员在线、数据完好（35MB，无 corrupt/alarm）
- ✅ 52 netplan 炸弹已拆、51 VIP 已持久化
- ⚠️ **apiserver 随 NFS 间歇 CrashLoop**：kubectl 通不通取决于查询那一刻 apiserver 在 crash 周期的相位
- ⚠️ **核心症结 = NFS 存储慢，未解决**

---

## 7. 经验教训

1. **ARP `(incomplete)` ≠ 主机离线**：secondary IP 未绑定时，外部现象与物理离线完全相同，曾导致首轮误判。
2. **逐层穿透，勿停于表象**：VIP→etcd quorum→磁盘 fsync→NFS 后端，每层都像"根因"，真正根因在最底层存储。
3. **iotop 是分清"受害者/肇事者"的关键**：本机 IO 量极小却磁盘满 util = 后端问题，而非本机。
4. **K8s 控制面对存储 fsync 延迟极度敏感**：etcd 要求 <10ms，NFS 抖动会直接瘫痪整个控制面。
5. **隐藏架构债**：kube-vip 长期 crash（伪 HA）、VMware 克隆模板把多节点 netplan 写成同一 VIP（IP 冲突源），均为本次放大故障的诱因。

---

## 8. 架构改进建议（下次 retro）

- **存储**：K8s etcd/控制面不应跑在易抖动的 NFS 上；建议 etcd 数据目录用本地 SSD 或低延迟块存储；为 NFS datastore 做延迟监控告警。
- **HA 入口**：修复或替换 kube-vip（评估 keepalived+haproxy / metallb / 外部 LB），消除静态单点 VIP。
- **节点模板**：修正 VMware 克隆模板的 netplan，避免多节点共用同一静态 IP。
- **可观测性**：补 etcd `wal fsync`、datastore latency 监控大盘，提前预警。

---

*本报告由 AI agent 基于 SSH 只读诊断 + 受控可逆处置生成；所有存储/虚拟化平台层操作均交人工/运维执行。SSH 诊断范围仅限 K8s 节点（88.50 及其跳板可达的 51/52），未触碰 TrueNAS/vCenter。*
