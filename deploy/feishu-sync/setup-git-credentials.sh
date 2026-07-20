#!/usr/bin/env bash
# 非交互 git push（K8s Secret 注入 GKX_GITLAB_TOKEN）
set -u

ROOT="${ROOT:-/orch}"
cd "$ROOT" || exit 1

if [[ -z "${GKX_GITLAB_TOKEN:-}" ]]; then
  echo "[WARN] GKX_GITLAB_TOKEN not set; git push may fail"
else
  USER="${GKX_GITLAB_USER:-oauth2}"
  BASE="${GKX_GITLAB_BASE:-https://gitlab.htmisoft.net}"
  GROUP="${GKX_GITLAB_GROUP:-gkx-lumen}"
  REPO="${GKX_ORCH_REPO:-gkx-orchestration}"
  BRANCH="${GIT_BRANCH:-dev}"

  git config --global user.email "coordinator@gkx-lumen.local"
  git config --global user.name "gkx-feishu-sync"
  git config --global pull.rebase true
  git config --global credential.helper store

  HOST="${BASE#https://}"
  HOST="${HOST#http://}"
  CRED_FILE="${HOME}/.git-credentials"
  echo "https://${USER}:${GKX_GITLAB_TOKEN}@${HOST}/${GROUP}/${REPO}.git" > "$CRED_FILE"
  chmod 600 "$CRED_FILE"

  export GIT_BRANCH="$BRANCH"

  # 若 Pod 内不是 git 仓（仅 COPY 无 .git），尝试 clone
  if [[ ! -d "$ROOT/.git" ]]; then
    echo "[INFO] cloning ${GROUP}/${REPO} branch ${BRANCH}"
    rm -rf /tmp/orch-clone
    git clone --branch "$BRANCH" --depth 1 \
      "${BASE}/${GROUP}/${REPO}.git" /tmp/orch-clone
    cp -a /tmp/orch-clone/. "$ROOT/"
  fi
fi
