# 开放项 1 · 网关登记证据（E-TECH-NEWS-IE-M1-L03）

## 结论

**无需新增独立路由。** 现网 / Helm 配置已用通配覆盖：

| 环境 | 配置文件 | 路由 | 下游 |
|------|----------|------|------|
| lumen | `helm/gkxlumen-platform/configs/gkxlumen-gateway-dev.yml` | `Path=/innov/**` + `StripPrefix=1` | `lb://gkxlumen-innov` |
| demo | `helm/gkx-platform/configs/gkx-gateway-dev.yml` | `Path=/innov/**` + `StripPrefix=1` | `lb://gkx-innov` |

前端路径 `/api/innov/v1/tech-news/**` → 网关 `/innov/v1/tech-news/**` → 服务 `/v1/tech-news/**`。

## As-built 注释

已在上述两份 gateway-dev.yml 的 `gkx(lumen)-innov` 路由处补充注释，标明覆盖 `/innov/v1/tech-news/**`（分支 `feat/E-TECH-NEWS-IE-M1-L03-gw`）。

## 探测

- `http://10.50.69.111:9999/innov/v1/tech-news/extractions`：本机探测超时（dev 网关本会话不可达）
- 配置层覆盖结论不依赖在线探测
