#!/usr/bin/env bash
# gkx-feishu-sync · kubectl apply + rollout（由 GitLab CI deploy:feishu-sync 调用）
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
K8S_DIR="$ROOT/deploy/feishu-sync/k8s"

TAG="${CI_COMMIT_TAG:-${CI_COMMIT_SHORT_SHA:-latest}}"
REGISTRY="${HARBOR_REGISTRY:-harbor.htmisoft.net}"
PROJECT="${HARBOR_PROJECT:-gkx}"
IMAGE="${REGISTRY}/${PROJECT}/gkx-feishu-sync:${TAG}"
NS="${DEPLOY_NAMESPACE:-gkx-dev}"
DEPLOYMENT="${FEISHU_SYNC_DEPLOYMENT:-gkx-feishu-sync}"
HARBOR_PULL_SRC="${HARBOR_PULL_SOURCE_NAMESPACE:-dev}"

echo "==> gkx-feishu-sync deploy"
echo "    namespace : $NS"
echo "    image     : $IMAGE"
echo "    deployment: $DEPLOYMENT"

if ! command -v kubectl >/dev/null; then
  echo "ERROR: kubectl not found" >&2
  exit 1
fi

ensure_namespace() {
  if ! kubectl get namespace "$NS" >/dev/null 2>&1; then
    echo "→ creating namespace $NS"
    kubectl create namespace "$NS"
  fi
}

copy_harbor_pull_secret() {
  if kubectl -n "$NS" get secret harbor-pull >/dev/null 2>&1; then
    return 0
  fi
  if ! kubectl -n "$HARBOR_PULL_SRC" get secret harbor-pull >/dev/null 2>&1; then
    echo "WARN: secret/harbor-pull not found in ns=$NS or ns=$HARBOR_PULL_SRC"
    return 0
  fi
  echo "→ copy secret/harbor-pull from ns=$HARBOR_PULL_SRC → ns=$NS"
  kubectl -n "$HARBOR_PULL_SRC" get secret harbor-pull -o yaml \
    | sed "s/namespace: ${HARBOR_PULL_SRC}/namespace: ${NS}/" \
    | grep -vE '^\s*(resourceVersion|uid|creationTimestamp):' \
    | kubectl apply -f -
}

bootstrap_app_secret_from_ci() {
  # 首次 deploy：若 GitLab 组变量已配置，自动 upsert（值不进 git）
  local missing=()
  for v in FEISHU_APP_ID FEISHU_APP_SECRET FEISHU_BITABLE_WEBHOOK_SECRET GKX_GITLAB_TOKEN; do
    if [[ -z "${!v:-}" ]]; then
      missing+=("$v")
    fi
  done
  if ((${#missing[@]} > 0)); then
    return 1
  fi

  echo "→ bootstrap secret/gkx-feishu-sync from CI variables"
  kubectl -n "$NS" create secret generic gkx-feishu-sync \
    --from-literal=FEISHU_APP_ID="${FEISHU_APP_ID}" \
    --from-literal=FEISHU_APP_SECRET="${FEISHU_APP_SECRET}" \
    --from-literal=FEISHU_BITABLE_WEBHOOK_SECRET="${FEISHU_BITABLE_WEBHOOK_SECRET}" \
    --from-literal=GKX_GITLAB_USER="${GKX_GITLAB_USER:-oauth2}" \
    --from-literal=GKX_GITLAB_TOKEN="${GKX_GITLAB_TOKEN}" \
    --from-literal=GKX_GITLAB_BASE="${GKX_GITLAB_BASE:-https://gitlab.htmisoft.net}" \
    --from-literal=GKX_GITLAB_GROUP="${GKX_GITLAB_GROUP:-gkx-lumen}" \
    --from-literal=GIT_BRANCH="${GIT_BRANCH:-dev}" \
    --dry-run=client -o yaml | kubectl apply -f -
  return 0
}

ensure_app_secret() {
  if kubectl -n "$NS" get secret gkx-feishu-sync >/dev/null 2>&1; then
    return 0
  fi

  if bootstrap_app_secret_from_ci; then
    return 0
  fi

  echo "ERROR: secret/gkx-feishu-sync not found in ns=$NS" >&2
  echo "       一次性运维（任选其一）：" >&2
  echo "       1) 本机：./scripts/k8s-apply-feishu-sync-secret.sh  （读 .env）" >&2
  echo "       2) GitLab 组变量补：FEISHU_APP_ID / FEISHU_APP_SECRET /" >&2
  echo "          FEISHU_BITABLE_WEBHOOK_SECRET / GKX_GITLAB_TOKEN → 重跑 deploy" >&2
  echo "       3) kubectl apply -f deploy/feishu-sync/k8s/secret.yaml（勿 commit）" >&2
  exit 1
}

ensure_namespace
copy_harbor_pull_secret
ensure_app_secret

apply_manifest() {
  local file="$1"
  sed "s|harbor.htmisoft.net/gkx/gkx-feishu-sync:latest|${IMAGE}|g" "$file" \
    | kubectl -n "$NS" apply -f -
}

echo "→ apply Service / Deployment / CronJob"
apply_manifest "$K8S_DIR/service.yaml"
apply_manifest "$K8S_DIR/deployment.yaml"
apply_manifest "$K8S_DIR/cronjob.yaml"

if [[ -n "${FEISHU_INGRESS_HOST:-}" && -n "${FEISHU_TLS_SECRET:-}" ]]; then
  echo "→ apply Ingress (host=$FEISHU_INGRESS_HOST)"
  sed -e "s|__INGRESS_HOST__|${FEISHU_INGRESS_HOST}|g" \
      -e "s|__TLS_SECRET_NAME__|${FEISHU_TLS_SECRET}|g" \
      -e "s|harbor.htmisoft.net/gkx/gkx-feishu-sync:latest|${IMAGE}|g" \
      "$K8S_DIR/ingress-path.yaml" | kubectl -n "$NS" apply -f -
else
  echo "→ skip Ingress（未设 FEISHU_INGRESS_HOST / FEISHU_TLS_SECRET CI 变量）"
fi

echo "→ rollout deployment/$DEPLOYMENT"
kubectl -n "$NS" rollout status "deployment/${DEPLOYMENT}" --timeout=5m

POD="$(kubectl -n "$NS" get pod -l app=gkx-feishu-sync,component=feishu-sync \
  -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"
if [[ -n "$POD" ]]; then
  echo "→ in-pod /health"
  kubectl -n "$NS" exec "$POD" -- curl -sf "http://127.0.0.1:8787/health" || \
    echo "WARN: in-pod health probe failed"
fi

kubectl -n "$NS" get deploy,svc,cronjob -l app=gkx-feishu-sync
echo "==> deploy OK"
