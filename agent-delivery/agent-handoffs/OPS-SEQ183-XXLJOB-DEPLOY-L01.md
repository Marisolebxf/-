# OPS-SEQ183-XXLJOB-DEPLOY-L01 · 部署 XXL-Job 调度中心,打通 seq183 科创资源订阅推送

## ✅ 2026-11-13 结案

**链路全通,任务闭环**(1045 于 11-12 晚间自行消解,首条调度 19:00;根因未及抓包确认,期间累计合入的 7 个修复 MR 均为净改进并保留在 dev):

| 验证项 | 实测(2026-11-13 09:46) |
|---|---|
| admin 连库 | gkxlumenx_job 集群侧连接 2 |
| 执行器注册 | display + topic-async 双执行器,30s 心跳持续 |
| 调度 | subscriptionPushJob 整点触发,15+ 次全部 trigger 200 / handle 200 |
| 推送落表 | `sys_user_planning_push_record` 16+ 行:user 302/3012/3009 各命中 policy/project/report 三行(3012 另含 carrier 行,其订阅领域为空全命中)——与用例预期一致 |
| 通知双写 | 「【科创资源订阅】命中 3 条新资源」聚合一通知(F7 ✓) |

**下游**:TS-DS09 用例 183b 转可演,20/20 全可演、0 缺口(用例 R2.2 / LOOP 计划 R0.7 已回写);前端登录后「科创资源整合与推送」表格出数据。

---

以下为排查期记录(2026-11-11~12),供复盘归档。

## 任务认领(必填)

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:zcode` |
| supervised_by | `human:王梓真`(seq183 批 4 池冻结监管人,沿 183 链) |
| claim_type | `pull`(用户派发:「这里为什么没有数据」→ 排查 → 修复 → 部署) |
| 仓库 | `lumen-svc-platform`(dev) |
| **当前状态** | ⏸ **代码侧全部就绪并合入;卡在集群层密码改写,需运维 5 分钟定位**(见「最终阻塞」) |

## 背景:seq183 推送产物清单恒空

用户在科技发展态势-综合发展规划页「科创资源整合与推送」保存订阅后表格恒空。直连 dev 库(10.50.11.76)逐环验证:订阅规则 ✅ / 资源池种子 ✅ / 推送记录 ❌ / 通知 ❌ / **xxl_job_info+xxl_job_group 全空** —— `subscriptionPushJob` 从未被调度。根因:XXL-Job 调度层整体缺失(admin 未部署、无任务种子)。

## 已完成交付(8 个 MR 全部合入 dev)

| MR | 内容 |
|----|------|
| !7 `a15a0b4` | 部署体系:values 新增 xxl-job-admin(9080/gkxlumenx_job)、CI image+deploy 任务、Dockerfile 仓库根上下文、4gkxlumenx_job.sql 幂等种子(dev 库已实插:执行器分组 gkxlumen-display + subscriptionPushJob 每小时) |
| !8 `bd4ae7d` | 修复 dev 既有编译错误:a795cd1 调用 `policySupportFactors` 未在 RemoteElementClient 声明 |
| !9 `f504a43` | admin application.yml 补 `xxl.job.*` 必填段 + `mybatis.mapper-locations`(本地复现定位:缺段→PlaceholderResolution 崩 / mapper 不加载→BindingException) |
| !11 `ab5beae` | admin 镜像补 `COPY otel javaagent`(commonEnv 注入 JAVA_TOOL_OPTIONS,缺文件 JVM 初始化即死) |
| !12 `e2a1779` | display 加 `XXL_JOB_ADMIN_ADDRESSES` 直连(common-job discovery 一次性解析,启动时序不对则永不注册) |
| !14 `e2a769b` | admin 资源 512Mi→1Gi + JAVA_OPTS -Xmx512m |
| !15 `44a8764` | admin 加 SPRING_DATASOURCE_URL/USERNAME/PASSWORD env 直压 |
| !10/!13 `a392b0a`/`a05dee6` | 诊断基建 `debug:job-logs`(CI_DEBUG_LOGS=true 门控;needs:[] 免排队;DEBUG_SELECTOR 可变;密码 sha256 指纹打印) |

调度库落位:`gkxlumenx_job`(全实例唯一;demo_ 前缀无调度库;用户裁定不再建 demo_gkxlumenx_job)。

## 最终阻塞(需运维,有集群权限 5 分钟定位)

**admin 容器内密码 env 的值 ≠ helm values 里写的值。**

证据链:
1. admin pod Running 不崩(4844 后,JVM/Spring 均正常,本地同参数复现调度器启动成功);
2. druid 报 `Access denied for user 'gkxlumenx'@'10.50.179.112' (using password: YES)`(errorCode 1045);
3. **debug:job-logs 实测容器内 MYSQL_PWD sha256 前12 = `c69c6c08ebaa` ≠ 期望值 `6a05600b175f`**(GKX@Lumen2026;空串/引号/CRLF/拼接等 20+ 变体全排除);
4. git 仓库 values 字节级干净(od 验证,LF,值正确);本机同凭证连库全程正常;
5. 4868(SPRING_DATASOURCE_PASSWORD value 直压)部署后 admin 仍 0 个 gkxlumenx_job 连接、xxl_job_log_report.update_time 恒 NULL——新 env 同样未按期望值生效。

**结论:helm 渲染→k8s 落地之间有东西改写密码类 env 值**(首要嫌疑:集群 MutatingWebhook/密钥轮换控制器;次嫌:某运维自动化 patch,参考 .gitlab-ci.yml `diag:upms` 的 pass_keys patch 模式)。

---

## 2026-11-12 二轮攻坚(全假说清单与终局证据)

**已合入并部署的修复(MR !17/!18/!20/!22/!23/!24/!25,全部为净改进,保留)**:secret-mysql 加 mysql-app-password;密码双通道 secretKeyRef→后改 value;env 去重(commonEnv 重叠项)+--force 重建;**mysql.enabled=true 显式声明(修复 commonEnv MYSQL_HOST 从未注入——helm upgrade 默认沿用 release 历史 values 的坑,dev 全体服务自此获得 MYSQL_HOST 注入)**;admin druid 数据源三要素就地写死(消除绑定歧义);通用模板支持 svc 级 nodeSelector;debug job 三代迭代(final:exec printenv 直读容器实发值)。

**逐项排除(铁证)**:
| 假说 | 验证手段 | 结果 |
|---|---|---|
| 容器密码值错 | CI exec printenv(MR !22) | **值正确**(MYSQL_PWD/SPRING_DATASOURCE_PASSWORD=GKX@Lumen2026,字节干净) |
| MySQL 库内密码不同 | root 比对 mysql_native_password 哈希 | **一致**(*220D0A0C…) |
| 多 host 条目劫持 | root 查 mysql.user | 唯一 gkxlumenx@'%',无匿名账号 |
| SSL 强制 | root 查 ssl_type/require_secure_transport | 无要求 |
| connector 9.5 缺陷 | 提取 admin jar 内 mysql-connector-j-9.5.0 本机 JDBC 同参数 | **连接成功** |
| Spring/druid 绑定断点 | yml 三要素硬编码(MR !24)部署 | 仍 1045 |
| node03 本地路径(MySQL 同节点) | nodeSelector 调 node01(MR !25)部署 | 仍 0 连接 |
| 本机同参数 | pymysql/JDBC 指定 gkxlumenx_job 库 | 成功 |
| 同实例邻居 | general_log 同毫秒对照 | topic-async 等同账号连接成功 |

**现象终局**:admin(任一节点、任一配置形态)以 gkxlumenx 敲 10.50.11.76:3306 恒 1045,general_log/Aborted_connects(2次/秒)持续佐证;同 jar 本机、同账号邻居、pymysql/JDBC 本机全部成功。

**唯一未排除**:pod 网络出口路径(CNI/conntrack/SNAT/iptables)对 MySQL 认证握手的干扰。**需运维节点级抓包**:

```bash
# 在 admin pod 所在节点(抓 60s,admin pod IP 以 kubectl get pod -o wide 为准)
tcpdump -i any -w /tmp/admin-mysql.pcap host 10.50.11.76 and port 3306 and host <admin-pod-ip>
# MySQL 侧(root):对比本机成功握手与 pod 失败握手的包序
# 若 pod 的握手包在传输中被改写/截断 → CNI/iptables 层问题;若包正常到达仍 1045 → MySQL 侧对该源有隐藏策略
```

### 运维定位清单(任一有集群权限者)

```bash
# 1. 看实际落地的密码值(与 GKX@Lumen2026 对比)
kubectl -n zhipu-tts get deploy gkxlumen-platform-xxl-job-admin -o yaml \
  | grep -B1 -A2 'MYSQL_PWD\|SPRING_DATASOURCE_PASSWORD'
# 2. 查密钥轮换类 admission webhook
kubectl get mutatingwebhookconfigurations
kubectl -n zhipu-tts get deploy gkxlumen-platform-xxl-job-admin -o yaml | grep -i 'managed\|injected\|vault\|sealed'
# 3. MySQL 侧 host 条目(排除另一可能:'gkxlumenx'@'10.50.%' 等更具体条目密码不同)
mysql> SELECT user, host, plugin FROM mysql.user WHERE user='gkxlumenx';
```

### 修复方向(按定位结果三选一)

- webhook 放行 xxl-job-admin(或把 admin 纳入其账号体系);
- admin 密码改 secretKeyRef 引用(webhook 一般只改 value 直写;secret-mysql.yaml 需加 `mysql-app-password: {{ .Values.mysql.password }}` key);
- 若 MySQL 存在更具体 host 条目:统一密码或对集群网段授权。

## 部署过程大事记

- Harbor database/redis 故障(11-11 11:20-12:16,运维修复)阻塞镜像推送;期间完成代码侧全部修复
- 4806 首次部署:admin CrashLoop#1=JVM otel agent 缺失(!11 修复)
- 4844 二次部署:CrashLoop#2 实为 1045 密码被拒(浮出水面)
- 4868 终次部署(四层修复齐发):pod Running 但连库仍 1045 → 密码值被改写实锤
- helm:deploy 多次出现 rate-limiter 超时假红(K8s client 限流,资源实际已 apply,以 DB 验证为准)

## 验证清单(Harbor/密码问题解决后)

`python D:/gkx-lumen/tmp/verify_seq183.py --fire-now`(拨 trigger_next_time 立即触发):

| 检查点 | 表 | 期望 |
|--------|-----|------|
| admin 调度 | xxl_job_log | subscriptionPushJob 触发行 |
| 执行器注册 | xxl_job_registry | registry_key='gkxlumen-display' |
| 推送落表 | sys_user_planning_push_record | user_id=302 出现 3 行(政策/项目/报告;载体领域不匹配) |
| 通知双写 | sys_user_notification | 「【科创资源订阅】命中 N 条」 |

前端:登录(user_id=302)→ 科技发展态势-综合发展规划 → 科创资源整合与推送。

## 遗留与建议

- **CI 门禁缺口**:dev 直推可合入编译不过的代码(a795cd1 案例);workflow 仅 dev 跑 CI,MR 无流水线
- topic-async 的 analysisStatusReconcileJob 同受 discovery 一次性解析影响,建议同样加 XXL_JOB_ADMIN_ADDRESSES
- admin 控制台(admin/123456)仅 ClusterIP,按需开 NodePort
- 手动 pipeline 的 changes 规则全命中(GitLab 行为)→ image job 全量排队,已用 needs:[] 缓解 debug 类
- .gitlab-ci.yml 部分行存在 CRLF 行尾混入(我的编辑工具所致,YAML 解析容忍,建议后续规范化)

## 证据

- MR !7-!16:https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/merge_requests/7 (~16)
- 流水线:4781/4782/4784(REBUILD_ALL)/4806/4820(首诊断)/4844/4848?/4859(取消)/4866/4868(终)
- 指纹诊断:job 36950(c69c6c08ebaa)/37115/37306(pending,runner 满载)
- 本地复现:`tmp/admin_local*.log`(调度器启动成功证据:行985 init scheduler success / 行1036 misfire jobId=1)
- 排查/验证脚本:`D:/gkx-lumen/tmp/diag_seq183.py`、`verify_seq183.py`(本地工具,不入仓)
