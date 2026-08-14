# DEVOPS-DEMO-NACOS-RESTORE-L01 · 按历史回滚 demo Nacos upms 数据源

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 21827 hook 把 chart 占位数据源盖进 Nacos。不跑 hook、不点 helm:deploy。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只回滚 Nacos 历史，不改 Java、不把口令写入 git/文档。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 现网 Nacos API。 |

## 问题清单

- 21827 `nacos-config-init` 把 `helm/gkx-platform/configs/*` 灌进 namespace `public`。
- `gkx-upms-biz-dev.yml` 现网变成 chart 占位 `${MYSQL_PASSWORD:…}`（nid 87，815 字节）。盖写前 nid 86 是带 JDBC 的 1229 字节版。
- 其它 4 份「旧版」比 chart 差：auth 旧版无 `encode-key`；gateway 旧版 2 条路由 vs 现 14 条；innov 旧版更短；`application-dev.yml` md5 未变。

## 修改内容

- Nacos `public` / `DEFAULT_GROUP` / `gkx-upms-biz-dev.yml`：从历史 nid 86 发布回现网（现 nid 88）
- `kubectl rollout restart deploy/demo-platform-upms`
- **未**回滚 auth / gateway / innov / application（回滚会丢 encode-key / 路由 / Feign 超时）
- **未**改 `runOnUpgrade=false`（继续禁止 upgrade 重发）
- 无业务仓代码改动

## 测试结果

- 现网 upms DataId：1229 字节，无占位符，md5 `91fdd264`（= nid 86）
- 历史条数 3：88（本次）/ 87（chart 占位）/ 86（盖写前）
- `demo-platform-upms` 1/1；镜像仍 `gkx-upms:08f6ca9e`
- 日志：`Started GkxAdminApplication`；在听 `gkx-upms-biz-dev.yml`

## 遗留风险

- upms Deployment 仍注入 Secret `MYSQL_PASSWORD`（`DEVOPS-DEMO-UPMS-MYSQL-ENV-L01`）。Nacos 已不再依赖占位符，Secret 留作双保险。
- 不要点 `helm:deploy`，也不要把 `nacosConfigInit.runOnUpgrade` 改回 true，否则会再次盖成占位符。
- demo Nacos 里仍有历史 `gkxlumen-*` DataId（与本次无关，未动）。

## CI/CD（必填）

- 分支：无代码提交（现网 Nacos + rollout）
- 部署 namespace：`dev`
- K8s rollout：`demo-platform-upms` 成功
- 验证：Nacos `gkx-upms-biz-dev.yml` md5 `91fdd264`；upms 1/1 Started

## 可观测性（建议）

- 未改 OTel

## 涉及文件

- 无 git 文件。现网：demo Nacos `gkx-upms-biz-dev.yml`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 口令不进新文档 | ✅ 只记 md5 / 字节数 / 是否占位 |
| D12 | ✅ 未把 lumen 配回 demo；innov/gateway 仍指向 `demo-platform-innov-py` |
| 未点 helm:deploy | ✅ |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 22000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.18 |
| cost_warn | green |
