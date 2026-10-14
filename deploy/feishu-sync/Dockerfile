# gkx-orchestration · Feishu sync (Webhook + Cron) — Node only
# Build from repo root:
#   docker build -f deploy/feishu-sync/Dockerfile -t 10.50.62.9:30303/zp-tts/gkx-feishu-sync:latest .

ARG NODE_BASE_IMAGE=10.50.62.9:30303/zp-tts/node:22.12.0-alpine
FROM ${NODE_BASE_IMAGE}

RUN sed -i 's#https://dl-cdn.alpinelinux.org/alpine#https://mirrors.aliyun.com/alpine#g' /etc/apk/repositories \
  && apk add --no-cache git curl bash ca-certificates tzdata \
  && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && echo "Asia/Shanghai" > /etc/timezone

WORKDIR /orch

COPY . .

RUN chmod +x deploy/feishu-sync/*.sh scripts/lib/git-push-registry.sh

ENV NODE_ENV=production \
    TZ=Asia/Shanghai \
    FEISHU_BITABLE_WEBHOOK_HOST=0.0.0.0 \
    FEISHU_BITABLE_WEBHOOK_PORT=8787

EXPOSE 8787

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8787/health || exit 1

ENTRYPOINT ["/bin/bash", "/orch/deploy/feishu-sync/entrypoint.sh"]
