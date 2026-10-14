#!/usr/bin/env bash
# 从旧 Harbor 拉取构建基础镜像，推到新 Harbor 公开项目 library。
# 在能同时访问两边、且 docker 已把 10.50.62.9:30303 配进 insecure-registries 的机器上跑（node01）。
#
#   export HARBOR_USERNAME=admin
#   export HARBOR_PASSWORD='...'          # 新 Harbor，不写进脚本
#   # 旧库若匿名拉不动再加：
#   # export SRC_USERNAME=...
#   # export SRC_PASSWORD=...
#   bash scripts/mirror-library-images.sh
#
# 可选：DOCKER='sudo docker'

set -euo pipefail

SRC="${SRC_REGISTRY:-harbor.htmisoft.net}"
DST="${DST_REGISTRY:-10.50.62.9:30303}"
DST_PROJECT="${DST_PROJECT:-library}"
DOCKER="${DOCKER:-docker}"

if [[ -z "${HARBOR_PASSWORD:-}" ]]; then
  echo "ERROR: 请先 export HARBOR_PASSWORD（新 Harbor ${DST}）" >&2
  exit 1
fi

echo "$HARBOR_PASSWORD" | $DOCKER login "$DST" -u "${HARBOR_USERNAME:-admin}" --password-stdin

if [[ -n "${SRC_PASSWORD:-}" ]]; then
  echo "$SRC_PASSWORD" | $DOCKER login "$SRC" -u "${SRC_USERNAME:?set SRC_USERNAME}" --password-stdin
fi

mirror() {
  local src="$1" name="$2" tag="$3"
  local dest="${DST}/${DST_PROJECT}/${name}:${tag}"
  echo "→ pull ${src}"
  $DOCKER pull "$src"
  $DOCKER tag "$src" "$dest"
  echo "→ push ${dest}"
  $DOCKER push "$dest"
}

# 源路径是旧 Harbor 上的原仓库；目标仓库名与现有 library/mysql、library/redis 一样，挂在项目 library 下。
mirror "${SRC}/internet/library/nginx:1.27-alpine"              nginx            1.27-alpine
mirror "${SRC}/internet/library/maven:3.9.6-eclipse-temurin-17" maven            3.9.6-eclipse-temurin-17
mirror "${SRC}/htmitech/python-algo-base:3.11"                  python-algo-base 3.11
mirror "${SRC}/internet/aquasec/trivy:0.50.0"                   trivy            0.50.0
mirror "${SRC}/internet/dtzar/helm-kubectl:3.15.4"              helm-kubectl     3.15.4
# 前端扫描作业还要漏洞库，和 trivy 一起迁。
mirror "${SRC}/gkx/aquasecurity/trivy-db:2"                     trivy-db         2

echo "done"
