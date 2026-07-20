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

echo "==> gkx-feishu-sync deploy"
echo "    namespace : $NS"
echo "    image     : $IMAGE"
echo "    deployment: $DEPLOYMENT"

if ! command -v kubectl >/dev/null; then
  echo "ERROR: kubectl not found" >&2
  exit 1
fi

if ! kubectl get namespace "$NS" >/dev/null 2>&1; then
  echo "→ creating namespace $NS"
  kubectl create namespace "$NS"
fi

if ! kubectl -n "$NS" get secret gkx-feishu-sync >/dev/null 2>&1; then
  echo "ERROR: secret/gkx-feishu-sync not found in ns=$NS" >&2
  echo "       请先按 deploy/feishu-sync/README.md §2 创建 Secret（不进 CI）。" >&2
  exit 1
fi

if ! kubectl -n "$NS" get secret harbor-pull >/dev/null 2>&1; then
  echo "WARN: secret/harbor-pull not found in ns=$NS — 若 Pod ImagePullBackOff，请从 dev 复制 pull secret"
fi

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
