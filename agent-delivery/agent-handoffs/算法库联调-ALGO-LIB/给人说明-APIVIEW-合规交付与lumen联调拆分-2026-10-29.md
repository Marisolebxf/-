# APIVIEW 合规交付与 lumen 联调拆分

> **日期**：2026-10-29（晚间按验收表再校端口与对外入口）
> **状态**：前端拆分已按方案 A 落代码并推 `origin/dev`。合理台 NodePort 定 **30894**（30899 被 kubepi 占用）。登录 AES key 已对齐 lumen auth（`gkx-lumen-gkx-lu`）。69 条清单、密封包、镜像 digest 仍待 `human:唐绍祖`。架构基线未把方案 A 升成新决策。
> **提出**：把现有算法联调台拆成「合规交付」和「线上试算」两条链，并冻结合同内 69 条算法的 Python 闭包。
> **待签字**：`human:唐绍祖`（69 条清单与锁定 tag）。方案 A 已按 2026-10-29「开始落地」写入 nginx，产品前端仍走 Java 链。
> **本文件角色**：拆分方案与锁定清单模板。冲突时的展示名以 [`算法合规与合理区分规约.md`](../../算法合规与合理区分规约.md) 为准（D17）。

**一句话**：合规展示留在 demo 链并锁定；`lumen-ui-algo-apiview` 改去测线上 lumen 算法进程。两条链锁定之后不再互相 merge。

---

## 1. 要解决的事

拆分前占着 NodePort **30897** 的是 `gkx-lumen-algo-apiview`，算法请求却打 demo 进程。拆分后 **30897 留给合规台**（`demo-ui-algo-apiview`），demo upstream 不变；合理调试改挂 **30894**（原计划 30899，被 `default/kubepi` 占用后改绑）。

| 页面族 | 现网服务 | 代码仓 |
| --- | --- | --- |
| 创新监测、产业链 | `demo-platform-innov-py` | `demo-algo-science` |
| 企业、政策、产业综合、人才、机构、技术基础 | `demo-platform-entan-py` | `demo-algo-ent-analysis` |
| 登录 `/api/auth/**`（合规台） | `demo-platform-gateway` → `gkx-auth` | `demo-svc-platform` |
| 登录 `/api/auth/**`（合理台） | `gkxlumen-platform-gateway` → `gkxlumen-auth` | `lumen-svc-platform` |

这和 D12 相反：lumen 前端调用链不得打到 `demo-*` 服务。同时，合同合规交付需要一份与算法中台当前算法一致、锁定后别人不能改结果的展示；业务侧还要能在 lumen 环境上继续试算。两件事不能共用同一个前端、同一套可随意修改的 Python。

仓库里算法库合同 L 的书面范围是 **97 叶**（`bid-reference/srs/05-深度挖掘算法/科技专题服务算法库`）。本次锁定范围按提出人口径是 **69 条**。69 与 97 的差集以唐绍祖签字清单为准，不按目录名猜测。

---

## 2. 两条链

```text
合规交付（锁定后只给验收看）  NodePort 30897
demo-ui-algo-apiview
  → demo-platform-innov-py      代码仓 demo-algo-science
  → demo-platform-entan-py      代码仓 demo-algo-ent-analysis
  登录仍走 demo-platform-gateway → gkx-auth（不进算法锁定）

合理调试（按业务继续改）  NodePort 30894
lumen-ui-algo-apiview
  → gkxlumen-platform-innov-py / gkxlumen-platform-entan-py（方案 A 直连 + X-Apiview-Direct）
  登录兜底 gkxlumen-platform-gateway → gkxlumen-auth
  代码仓 lumen-algo-py（vendor/innov-py、vendor/entan-py）
```

| | 合规交付 | 合理调试 |
| --- | --- | --- |
| 前端仓 | `demo-ui-algo-apiview` | `lumen-ui-algo-apiview` |
| NodePort | **30897** | **30894** |
| 验收内网 | http://10.50.69.111:30897 | http://10.50.69.111:30894 |
| 验收对外 | https://edu.itic-sci.com/dma/algovwz/ | **不对外** |
| 算法进程 | `demo-platform-innov-py`、`demo-platform-entan-py` | `gkxlumen-platform-innov-py`、`gkxlumen-platform-entan-py` |
| 算法代码 | `demo-algo-science`、`demo-algo-ent-analysis` | `lumen-algo-py` |
| 登录 AES key | demo `gkxgkxgkxgkxgkxg`（对齐 demo auth） | lumen `gkx-lumen-gkx-lu`（对齐 gkxlumen-auth） |
| 用途 | 与算法中台当前合规算法一致的验收展示 | 测线上 lumen 环境里的算法 |
| 锁定后 | 69 条闭包、对应页面目录、nginx upstream、运行镜像 tag 冻结 | 继续开发；不回灌 demo 锁定闭包 |

验收环境（与验收表一致，2026-10-29）：

| 验收环境 | 前端仓 | 内网 | 对外 |
| --- | --- | --- | --- |
| 验收环境-实现-算法 preview（合规交付） | `demo-ui-algo-apiview` | http://10.50.69.111:30897 | https://edu.itic-sci.com/dma/algovwz/ |
| 验收环境-实现-算法 preview（合理调试用） | `lumen-ui-algo-apiview` | http://10.50.69.111:30894 | 不对外 |

端口调整：**30897 留给合规台**，Service/`demo-ui-algo-apiview`，upstream 仍是 `demo-platform-innov-py` 与 `demo-platform-entan-py`。`lumen-ui-algo-apiview` 从 30897 挪走，改挂 **30894**，upstream 改为 lumen 算法进程（方案 A）。30897 不再改去打 `gkxlumen-*`。CI 先 apply Service 再 apply ConfigMap/Deployment，避免 NodePort 失败时半更新 nginx。

`demo-svc-platform` 只承担合规台登录。改网关业务路由不算改合规算法，但不得把合规台的算法请求改去别的服务。

展示前端、专题前端仍走 `gkxlumen-platform-gateway` → Java → Python `/internal/*`。本拆分不给这两条产品链开直连 Python 的口。

---

## 3. 仓与发布

`demo-ui-algo-apiview` 从 `lumen-ui-algo-apiview` 整仓复制为新 Git 远程。复制后两边不再 merge。工作区：`workspaces/fe-algo.code-workspace`（主仓 + 两台前端）；全量 `gkx-lumen.code-workspace` 亦已收录 `demo-ui-algo-apiview`。

合规台 nginx 指向 `demo-platform-innov-py` 与 `demo-platform-entan-py`，NodePort **30897**。`lumen-ui-algo-apiview` nginx 改为第 6 节 lumen 目标，NodePort **30894**。

发布约定：

- 合规台镜像名独立，NodePort **30897**。合理调试台 NodePort **30894**。两个端口不互换、不共用一个 Service。
- 登记 `agent-delivery/repo-registry.yaml` 与 `agent-delivery/paths.yaml`。
- 分支仍是 `origin/dev`，禁止直推 `main`。
- 本地 `pnpm dev`：合规台代理到 demo 算法进程；lumen 台代理到 lumen 算法进程。

`lumen-algo-py` 里已有的 `vendor/innov-py`、`vendor/entan-py` 是历史对照副本，不是合规锁定对象。线上业务探索写在 `lumen-algo-py`，部署到 `gkxlumen-*`。

---

## 4. 锁定什么

锁定对象是唐绍祖签字的 69 条在 `demo-algo-science`、`demo-algo-ent-analysis` 中的**调用闭包**，不是把两个仓整仓封死。

一条算法的闭包包括：

- 入口函数与对外路由
- 该入口调用到的全部中间函数
- 这些函数读到的模块级变量和常量
- 企业侧若该条走到 worker，worker 里同一条调用链一并纳入

别人要在算法中台试新算法或改行为：在闭包外加新模块、新路由。若必须基于某条已锁定算法改，把该条从入口到依赖的全过程复制到新包，只改副本。新路由不得复用已锁定的 URL。

这样就会同时存在两条算法：锁定原条，以及复制后改过的副本。两条都要在算法中台里看得见，展示名必须分开，不能共用一个名字。

算法中台指 `demo-ui-system-test`。有冲突时，指标展示名成对出现：

| 展示名 | 指哪一条 | 调用 |
| --- | --- | --- |
| `{原名}-合规` | 锁定闭包，合同验收用 | 已锁定的路由 |
| `{原名}-合理` | 复制全过程后再按业务改过的副本 | 新路由 |

例如原名是「产业链变化趋势指数」，冲突后中台上是「产业链变化趋势指数-合规」和「产业链变化趋势指数-合理」。没有冲突的指标保持原名，不加后缀。

`-合规` 只挂锁定入口。`-合理` 只挂新路由，不进 `demo-ui-algo-apiview`，也不回写锁定闭包。两条的 `metric_id`、路由、Python 入口各自独立，中台列表、详情和计算结果都按这个展示名区分。

禁止：修改锁定闭包里的任何函数、以及这些函数引用到的任何变量。这种修改会让合规结果发生变化。

确认后打标签，建议名 `compliance-lock-YYYYMMDD`。同一个 tag 同时钉住：

1. `demo-algo-science`、`demo-algo-ent-analysis` 的该提交
2. `demo-ui-algo-apiview` 里这 69 条的目录、请求路径和 nginx upstream
3. 集群中 `demo-platform-innov-py`、`demo-platform-entan-py`（含 entan worker）正在跑的镜像 tag

只冻源码、不冻镜像时，CI 仍可以把合规服务换成新镜像。三样必须一起钉。

解锁、换 tag、改清单，只由唐绍祖提交。

---

## 5. 规约四层

口头约定守不住共享函数。用下面四层。

### 5.1 清单与签字

编排仓保存锁定清单：69 条入口、闭包文件列表、内容哈希、tag、镜像 digest。模板见第 7 节。签字人只有唐绍祖。

### 5.2 源码隔离

锁定时把 69 条闭包收进单独包（建议名 `compliance_locked/`）。入口只从该包引用。这一步就是「全过程复制」：复制进密封包；原共享函数留给后续探索；密封包与探索代码不再共用同一份函数和变量。

CODEOWNERS：

| 路径 | 所有人 |
| --- | --- |
| 两个 demo 算法仓的 `compliance_locked/` 与锁定清单 | `human:唐绍祖` |
| `demo-ui-algo-apiview` 的接口目录与 nginx upstream | `human:唐绍祖` |

### 5.3 CI

- 合并请求改动密封包内任何文件，作者不是唐绍祖，则失败。
- 对 69 个入口再做一次 import / 调用扫描。锁定入口引用到密封包以外的业务函数，也失败。防止入口被改去调新函数，而密封包文件一个字没动。
- `demo-platform-innov-py`、`demo-platform-entan-py` 的部署只接受锁定镜像 tag。

### 5.4 人与 agent 可读的规则

架构基线增加一条决策，团队公约铁律指向该条。算法仓和编排仓各放一条 Cursor 规则，写明：

- 禁止改 `compliance_locked/`
- 禁止改锁定入口的引用
- 新算法只能新模块、新路由
- 基于锁定算法的变体，必须先复制全过程再改副本
- 副本与锁定原条冲突时，`demo-ui-system-test` 的指标展示名分成 `{原名}-合规` 与 `{原名}-合理`；合规台只保留锁定原条，不挂 `-合理`

冲突时的展示名已写入 D17 与 `算法合规与合理区分规约.md`。密封包和 69 条清单签字前不写入架构基线。方案 A 只记在本文件和联调台 nginx。

---

## 6. lumen 联调台接法

2026-10-29 按「开始落地」采用方案 A，只写在 `lumen-ui-algo-apiview` 的 nginx 上。展示前端、专题前端仍走 `gkxlumen-platform-gateway` → Java → `/internal/*`。

| 项 | 落地 |
| --- | --- |
| 算法 upstream | `gkxlumen-platform-innov-py.zhipu-tts.svc.cluster.local:8000`、`gkxlumen-platform-entan-py.zhipu-tts.svc.cluster.local:8000` |
| 登录兜底 | `gkxlumen-platform-gateway.zhipu-tts.svc.cluster.local:9999` |
| innov `/v1` | helm 仍是 `INNOV_EXPOSE_PUBLIC_API=0`。本台 nginx 加 `X-Apiview-Direct: 1`，innov 中间件只对这个头放行 `/v1`。没有该头的调用方仍是 404 |
| entan `/v1` | 当前 `vendor/entan-py` 不读 `ENTAN_EXPOSE_PUBLIC_API`，不另加门禁 |
| innov 上线 | `deploy:innov` 在 `dev` 上默认手动。镜像进仓后要点该作业，进程才会带上放行头 |

方案 B（Java 转发 `/internal/*`）没有现成路由，这次没有做。若架构师改回 B，再撤掉本台直连和放行头。

端口：原计划 **30899** 被 `default/kubepi` 占用，现网合理台定为 **30894**。清单里 CI **先 apply Service** 再 apply ConfigMap/Deployment。Service NodePort 失败则停，避免只改 nginx 半更新。Harbor `/data` 满盘会导致 `frontend:image` 推镜像失败，需清历史镜像后再重跑 pipeline。

登录：合理台必须用 lumen auth 的 `encode-key`（`gkx-lumen-gkx-lu`）。前端误用 demo key `gkxgkx…` 时表现为「用户名或密码错误」；连续失败会把 `admin` 写库锁定（`lock_flag=9`）。默认账号 `admin` / `gkx@2026`。

---

## 7. 数据面核对

UI 指到 lumen 进程，测到的是该进程的代码和它当时连接的库。切前端时单独核对：

- Deployment 镜像是 `lumen-algo-py` 构建的 `gkxlumen-innov-py`、`gkxlumen-entan-py-api`、`gkxlumen-entan-py-worker`
- 进程实际读取的库名

这是数据面核对，与仓隔离分开记录。镜像已经是 lumen 制品、库仍是 demo 库时，页面测到的是 lumen 代码加 demo 数据，要在核对记录里写明。

---

## 8. 实施顺序

69 条锁定仍未做。前端拆分发布顺序（避免抢 30897、避免 NodePort 失败半更新）：

1. 唐绍祖填写第 9 节清单后再打 `compliance-lock-*`、收 `compliance_locked/`、钉合规镜像。这次不代替他做。
2. 先发布 `lumen-algo-py` 的 innov 放行头，再手动点 `deploy:innov`。
3. 再发布 `lumen-ui-algo-apiview`：Service **30894** + 第 6 节 upstream + 登录 AES key `gkx-lumen-gkx-lu`（`5104f52` 已推）。Harbor 绿后确认 http://10.50.69.111:30894 。
4. 30897 空出来之后再发布 `demo-ui-algo-apiview`，Service **30897**，upstream 仍是 `demo-platform-*`；对外入口 https://edu.itic-sci.com/dma/algovwz/ 。
5. 69 条签字之后，再把锁定决策补进架构基线。

---

## 9. 锁定清单模板

由唐绍祖填写。满 69 行后签字。闭包文件列表由入口扫描生成，贴在本表之后或单独附件，并记录内容哈希。

| # | 合同条目或 metric_id | 仓 | 入口函数 | 对外路由 | 是否含 worker |
| --- | --- | --- | --- | --- | --- |
| 1 |  | `demo-algo-science` / `demo-algo-ent-analysis` |  |  | 是 / 否 |
| 2 |  |  |  |  |  |
| … |  |  |  |  |  |
| 69 |  |  |  |  |  |

锁定元数据：

| 项 | 值 |
| --- | --- |
| tag | `compliance-lock-YYYYMMDD` |
| `demo-algo-science` 提交 |  |
| `demo-algo-ent-analysis` 提交 |  |
| 复制为 `demo-ui-algo-apiview` 的前端提交 |  |
| `demo-platform-innov-py` 镜像 digest |  |
| `demo-platform-entan-py` 镜像 digest |  |
| entan worker 镜像 digest |  |
| 闭包哈希 |  |
| 相对 97 叶未纳入本次锁定的条目 |  |

---

## 10. 签字

| 角色 | 人 | 签什么 | 日期 | 结果 |
| --- | --- | --- | --- | --- |
| 算法 Lead | `human:唐绍祖` | 69 条清单、tag、闭包哈希、合规镜像 digest |  | 待签 |
| 架构 / 项目负责人 | 架构师或 `human:淮政玮` | 方案 A 已落地；若改回方案 B 再签 |  | 待确认 |
