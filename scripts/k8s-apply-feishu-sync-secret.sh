#!/usr/bin/env bash
# 从 .env 或当前 shell 环境变量创建/更新 K8s secret gkx-feishu-sync（一次性运维）
# 用法：
#   ./scripts/k8s-apply-feishu-sync-secret.sh
#   DEPLOY_NAMESPACE=zhipu-tts ./scripts/k8s-apply-feishu-sync-secret.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NS="${DEPLOY_NAMESPACE:-zhipu-tts}"
ENV_FILE="${GKX_ENV_FILE:-$ROOT/.env}"

load_dotenv() {
  local file="$1"
  [[ -f "$file" ]] || return 0
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%%#*}"
    line="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    [[ -z "$line" ]] && continue
    [[ "$line" != *=* ]] && continue
    local key="${line%%=*}"
    local val="${line#*=}"
    val="${val%\"}"; val="${val#\"}"
    val="${val%\'}"; val="${val#\'}"
    if [[ -z "${!key:-}" ]]; then
      export "$key=$val"
    fi
  done < "$file"
}

require_var() {
  local name="$1"
  if [[ -z "${!name:-}" ]]; then
    echo "ERROR: $name is required (set in $ENV_FILE or export in shell)" >&2
    exit 1
  fi
}

load_dotenv "$ENV_FILE"

require_var FEISHU_APP_ID
require_var FEISHU_APP_SECRET
require_var FEISHU_BITABLE_WEBHOOK_SECRET
require_var GKX_GITLAB_TOKEN

GKX_GITLAB_USER="${GKX_GITLAB_USER:-oauth2}"
GKX_GITLAB_BASE="${GKX_GITLAB_BASE:-https://aminer-edu-gitlab.jyzhang.cn}"
GKX_GITLAB_GROUP="${GKX_GITLAB_GROUP:-sz-gkx/gkx-lumen}"
GIT_BRANCH="${GIT_BRANCH:-dev}"

if ! command -v kubectl >/dev/null; then
  echo "ERROR: kubectl not found" >&2
  exit 1
fi

kubectl get namespace "$NS" >/dev/null 2>&1 || kubectl create namespace "$NS"

echo "→ upsert secret/gkx-feishu-sync in ns=$NS"
kubectl -n "$NS" create secret generic gkx-feishu-sync \
  --from-literal=FEISHU_APP_ID="$FEISHU_APP_ID" \
  --from-literal=FEISHU_APP_SECRET="$FEISHU_APP_SECRET" \
  --from-literal=FEISHU_BITABLE_WEBHOOK_SECRET="$FEISHU_BITABLE_WEBHOOK_SECRET" \
  --from-literal=GKX_GITLAB_USER="$GKX_GITLAB_USER" \
  --from-literal=GKX_GITLAB_TOKEN="$GKX_GITLAB_TOKEN" \
  --from-literal=GKX_GITLAB_BASE="$GKX_GITLAB_BASE" \
  --from-literal=GKX_GITLAB_GROUP="$GKX_GITLAB_GROUP" \
  --from-literal=GIT_BRANCH="$GIT_BRANCH" \
  --dry-run=client -o yaml | kubectl apply -f -

# harbor-pull：目标命名空间没有时，从 HARBOR_PULL_SOURCE_NAMESPACE 复制
if ! kubectl -n "$NS" get secret harbor-pull >/dev/null 2>&1; then
  SRC_NS="${HARBOR_PULL_SOURCE_NAMESPACE:-zhipu-tts}"
  if kubectl -n "$SRC_NS" get secret harbor-pull >/dev/null 2>&1; then
    echo "→ copy secret/harbor-pull from ns=$SRC_NS"
    kubectl -n "$SRC_NS" get secret harbor-pull -o yaml \
      | sed "s/namespace: ${SRC_NS}/namespace: ${NS}/" \
      | grep -vE '^\s*(resourceVersion|uid|creationTimestamp):' \
      | kubectl apply -f -
  else
    echo "WARN: harbor-pull not found in ns=$SRC_NS — Pod 可能 ImagePullBackOff"
  fi
fi

kubectl -n "$NS" get secret gkx-feishu-sync harbor-pull 2>/dev/null || kubectl -n "$NS" get secret gkx-feishu-sync
echo "==> secret OK"
