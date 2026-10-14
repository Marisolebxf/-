# Set GitLab default_branch=dev for sz-gkx/gkx-lumen business repos (excludes gkx-orchestration).
# Token: GITLAB_TOKEN env, or parsed from any repo origin URL (https://user:TOKEN@host/...).

param(
    [string]$GitLabHost = "aminer-edu-gitlab.jyzhang.cn",
    [string]$Group = "sz-gkx/gkx-lumen",
    [string[]]$ExcludePaths = @('gkx-orchestration')
)

$ErrorActionPreference = 'Continue'

function Get-GitLabToken {
    if ($env:GITLAB_TOKEN) { return $env:GITLAB_TOKEN }
    $candidates = @()
    if ($env:GKX_ROOT) {
        $candidates += @(
            (Join-Path $env:GKX_ROOT 'repos\demo-algo-science'),
            (Join-Path $env:GKX_ROOT 'repos\lumen-svc-platform'),
            (Join-Path $env:GKX_ROOT 'repos\demo-svc-platform'),
            (Join-Path $env:GKX_ROOT 'gkx-orchestration')
        )
    }
    foreach ($repo in $candidates) {
        if (-not (Test-Path $repo)) { continue }
        $url = git -C $repo remote get-url origin 2>$null
        if ($url -match 'https://[^:/@]+:([^@]+)@') { return $Matches[1] }
    }
    throw "GITLAB_TOKEN not set and no token found in git remotes"
}

function Set-ProjectDefaultBranch {
    param([int]$ProjectId, [string]$Path, [string]$Token, [string]$HostName)
    $uri = "https://$HostName/api/v4/projects/$ProjectId"
    $headers = @{ 'PRIVATE-TOKEN' = $Token }
    try {
        $proj = Invoke-RestMethod -Uri $uri -Headers $headers -Method Get
        if ($proj.default_branch -eq 'dev') {
            Write-Host "OK $Path (id=$ProjectId) already default=dev"
            return
        }
        $body = (@{ default_branch = 'dev' } | ConvertTo-Json -Compress)
        Invoke-RestMethod -Uri $uri -Headers $headers -Method Put -ContentType 'application/json' -Body $body | Out-Null
        Write-Host "OK $Path (id=$ProjectId) default_branch -> dev"
    }
    catch {
        Write-Warning "FAIL $Path (id=$ProjectId): $($_.Exception.Message)"
    }
}

$token = Get-GitLabToken
$headers = @{ 'PRIVATE-TOKEN' = $token }
$page = 1
$all = @()

do {
    $groupId = [uri]::EscapeDataString($Group)
    $uri = "https://$GitLabHost/api/v4/groups/$groupId/projects?include_subgroups=true&per_page=100&page=$page"
    $batch = Invoke-RestMethod -Uri $uri -Headers $headers -Method Get
    if ($batch) { $all += $batch }
    $page++
} while ($batch.Count -eq 100)

foreach ($p in $all) {
    if ($ExcludePaths -contains $p.path) {
        Write-Host "SKIP $($p.path) (orchestration, keep current default)"
        continue
    }
    $repoRoot = if ($env:GKX_ROOT) { Join-Path $env:GKX_ROOT "repos\$($p.path)" } else { $null }
    $hasDev = $false
    if ($repoRoot -and (Test-Path $repoRoot)) {
        git -C $repoRoot rev-parse --verify origin/dev 2>$null | Out-Null
        $hasDev = ($LASTEXITCODE -eq 0)
    }
    if (-not $hasDev) {
        Write-Host "SKIP $($p.path) (no local origin/dev; set GKX_ROOT to check)"
        continue
    }
    Set-ProjectDefaultBranch -ProjectId $p.id -Path $p.path_with_namespace -Token $token -HostName $GitLabHost
}

Write-Host "Done."
