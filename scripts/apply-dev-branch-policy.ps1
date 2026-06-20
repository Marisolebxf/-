# Apply dev-branch CI policy and create/push dev branches (excludes gkx-orchestration).
# Usage: pwsh -File scripts/apply-dev-branch-policy.ps1 [-Push] [-SkipMerge]

param(
    [switch]$Push,
    [switch]$SkipMerge,
    [string[]]$OnlyRepos = @()
)

$ErrorActionPreference = 'Continue'
$ReposRoot = 'F:\gkx-lumen\repos'

$WorkflowBlock = @"

# 分支策略（2026-06-20）：仅 dev 触发 CI/CD；feature/* 合并到 dev 后再跑流水线
workflow:
  rules:
    - if: '`$CI_COMMIT_BRANCH == "dev"'
    - when: never

"@

function Add-WorkflowBlock {
    param([string]$CiPath)
    $content = Get-Content -Raw -Path $CiPath
    if ($content -match '(?m)^workflow:\s*$') {
        Write-Host "  workflow already present in $CiPath"
        return $false
    }
    if ($content -match '(?m)^stages:\s*$') {
        $content = $content -replace '(?m)^stages:\s*$', ($WorkflowBlock + "stages:")
        Set-Content -Path $CiPath -Value $content -NoNewline
        return $true
    }
    throw "Cannot locate stages: in $CiPath"
}

function Patch-DemoUiScienceCi {
    param([string]$CiPath)
    $content = Get-Content -Raw -Path $CiPath
    $content = $content -replace '\$CI_COMMIT_BRANCH == "dev" \|\| \$CI_COMMIT_BRANCH == "main"', '$CI_COMMIT_BRANCH == "dev"'
    Set-Content -Path $CiPath -Value $content -NoNewline
}

$RepoMergePlan = @{
    'demo-algo-science'      = @('origin/feat/E-INNOV-M1-L02')
    'demo-algo-ent-analysis' = @('origin/feat/E-PLATFORM-P0-L03', 'origin/feat/E-PLATFORM-P0-L04')
    'demo-ui-science'        = @('origin/main')
    'demo-ui-system-test'    = @('origin/main')
    'demo-ui-topic'          = @('origin/main')
    'demo-svc-platform'      = @('origin/main')
    'lumen-svc-platform'     = @(
        'origin/feat/E-PLATFORM-P0-L06',
        'origin/feat/E-INNOV-M1-L02b',
        'origin/feat/E-INNOV-M1-L03',
        'origin/feat/E-INNOV-M1-L04',
        'origin/feat/E-INNOV-M1-L06'
    )
    'lumen-ui-science-pc'    = @('origin/feat/E-INNOV-M1-L07', 'origin/feat/E-INNOV-M1-L08')
    'lumen-ui-science-topic' = @('origin/main', 'origin/feat/E-PLATFORM-P0-L00', 'origin/feat/E-PLATFORM-P0-L07')
}

foreach ($repo in $RepoMergePlan.Keys) {
    if ($OnlyRepos.Count -gt 0 -and ($OnlyRepos -notcontains $repo)) {
        continue
    }
    $path = Join-Path $ReposRoot $repo
    if (-not (Test-Path $path)) {
        Write-Warning "SKIP missing repo: $repo"
        continue
    }

    Write-Host "`n========== $repo =========="
    Push-Location $path
    try {
        $hasCommits = git rev-parse HEAD 2>$null
        if (-not $hasCommits) {
            Write-Warning "SKIP empty repo (no commits): $repo"
            continue
        }

        git fetch origin --prune 2>&1 | Out-Null

        $hasOriginDev = git rev-parse --verify origin/dev 2>$null
        if ($hasOriginDev -and -not $SkipMerge) {
            git show origin/dev:.gitlab-ci.yml 2>$null | Select-String -Pattern '^workflow:' -Quiet | Out-Null
            if ($? -and (git show origin/dev:.gitlab-ci.yml 2>$null | Select-String -Pattern '^workflow:')) {
                Write-Host "  origin/dev already has workflow policy — skip"
                continue
            }
        }

        $ciPath = Join-Path $path '.gitlab-ci.yml'

        if (-not $SkipMerge) {
            $refs = $RepoMergePlan[$repo]
            $base = $refs[0]
            $mergeRefs = if ($refs.Count -gt 1) { $refs[1..($refs.Count - 1)] } else { @() }
            git checkout -B dev $base 2>&1 | ForEach-Object { Write-Host "  $_" }
            if ($LASTEXITCODE -ne 0) { throw "checkout dev failed for $repo" }
            foreach ($ref in $mergeRefs) {
                Write-Host "  merging $ref ..."
                git merge $ref -m "chore: merge $ref into dev [agent:devops-agent]" --no-edit 2>&1 | ForEach-Object { Write-Host "  $_" }
                if ($LASTEXITCODE -ne 0) {
                    throw "Merge failed for $ref in $repo"
                }
            }
        } else {
            git checkout dev 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) { git checkout -B dev origin/dev 2>&1 | Out-Null }
        }

        if (Test-Path $ciPath) {
            if (Add-WorkflowBlock -CiPath $ciPath) {
                Write-Host "  added workflow block"
            }
            if ($repo -eq 'demo-ui-science') {
                Patch-DemoUiScienceCi -CiPath $ciPath
                Write-Host "  patched demo-ui-science build rules (dev only)"
            }
        }

        if (Test-Path $ciPath) {
            git add .gitlab-ci.yml
        }
        $dirty = git status --porcelain
        if ($dirty) {
            git commit -m "chore(ci): restrict pipelines to dev branch only [agent:devops-agent]" 2>&1 | ForEach-Object { Write-Host "  $_" }
            if ($LASTEXITCODE -ne 0) { throw "commit failed for $repo" }
        }

        if ($Push) {
            git push -u origin dev 2>&1 | ForEach-Object { Write-Host "  $_" }
            if ($LASTEXITCODE -ne 0) { throw "push failed for $repo" }
            Write-Host "  pushed dev"
        }
    }
    finally {
        Pop-Location
    }
}

Write-Host "`nDone."
