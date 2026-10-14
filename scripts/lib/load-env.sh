#!/usr/bin/env bash
# 从 gkx-orchestration/.env 加载环境变量（RFC-002 §6 路径真源）
# 用法（在主仓根目录）：
#   source scripts/lib/load-env.sh
#   source scripts/lib/load-env.sh /path/to/gkx-orchestration
# 加载后可用：GKX_ROOT GKX_DOCS_ROOT GKX_GITLAB_* GKX_ROOT_EXPANDED

_gkx_load_env() {
    local orchestration_dir="${1:-}"

    if [[ -z "$orchestration_dir" ]]; then
        if [[ -f ".env" ]] && [[ -d "agent-delivery" ]]; then
            orchestration_dir="$(pwd)"
        elif [[ -n "${BASH_SOURCE[0]:-}" ]]; then
            orchestration_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
        else
            echo "load-env.sh: cannot locate gkx-orchestration root" >&2
            return 1
        fi
    fi

    local env_file="$orchestration_dir/.env"
    if [[ ! -f "$env_file" ]]; then
        echo "load-env.sh: missing $env_file (copy from .env.example)" >&2
        return 1
    fi

    set -a
    # shellcheck disable=SC1090
    source "$env_file"
    set +a

    if [[ -z "${GKX_ROOT:-}" ]]; then
        echo "load-env.sh: GKX_ROOT is required in $env_file" >&2
        return 1
    fi

    GKX_ROOT_EXPANDED="$(eval echo "$GKX_ROOT")"
    GKX_ORCHESTRATION_DIR="$GKX_ROOT_EXPANDED/gkx-orchestration"
    GKX_REPOS_DIR="$GKX_ROOT_EXPANDED/repos"
    GKX_WORKTREES_DIR="$GKX_ROOT_EXPANDED/worktrees"
    GKX_AGENT_DELIVERY_DIR="$GKX_ORCHESTRATION_DIR/agent-delivery"

    GKX_GITLAB_BASE="${GKX_GITLAB_BASE:-https://aminer-edu-gitlab.jyzhang.cn}"
    GKX_GITLAB_GROUP="${GKX_GITLAB_GROUP:-sz-gkx/gkx-lumen}"

    export GKX_ROOT GKX_ROOT_EXPANDED GKX_ORCHESTRATION_DIR GKX_REPOS_DIR
    export GKX_WORKTREES_DIR GKX_AGENT_DELIVERY_DIR
    export GKX_DOCS_ROOT GKX_GITLAB_BASE GKX_GITLAB_GROUP GKX_GITLAB_USER GKX_GITLAB_TOKEN
}

if [[ "${BASH_SOURCE[0]:-}" == "${0}" ]]; then
    _gkx_load_env "${1:-}" || exit 1
    echo "GKX_ROOT=$GKX_ROOT_EXPANDED"
    echo "GKX_ORCHESTRATION_DIR=$GKX_ORCHESTRATION_DIR"
    echo "GKX_REPOS_DIR=$GKX_REPOS_DIR"
else
    _gkx_load_env "${1:-}" || return 1
fi
