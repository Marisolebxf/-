# Set GitLab default_branch=dev for gkx-lumen business repos (excludes gkx-orchestration).
# Token: GITLAB_TOKEN env, or parsed from any repo origin URL (https://user:TOKEN@host/...).

param(
    [string]$GitLabHost = "gitlab.htmisoft.net",
    [string]$Group = "gkx-lumen",
    [int[]]$ExcludeProjectIds = @(215)  # gkx-orchestration stays on main
)

$ErrorActionPreference = 'Continue'

function Get-GitLabToken {
    if ($env:GITLAB_TOKEN) { return $env:GITLAB_TOKEN }
    $candidates = @(
        'F:\gkx-lumen\repos\demo-algo-science',
        'F:\gkx-lumen\repos\lumen-svc-platform',
        'F:\gkx-lumen\repos\demo-svc-platform',
        'F:\gkx-lumen\gkx-orchestration'
    )
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
    $uri = "https://$GitLabHost/api/v4/groups/$Group/projects?include_subgroups=true&per_page=100&page=$page"
    $batch = Invoke-RestMethod -Uri $uri -Headers $headers -Method Get
    if ($batch) { $all += $batch }
    $page++
} while ($batch.Count -eq 100)

foreach ($p in $all) {
    if ($ExcludeProjectIds -contains $p.id) {
        Write-Host "SKIP $($p.path) (orchestration, keep main)"
        continue
    }
    $hasDev = git -C "F:\gkx-lumen\repos\$($p.path)" rev-parse --verify origin/dev 2>$null
    if (-not $hasDev) {
        Write-Host "SKIP $($p.path) (no origin/dev locally)"
        continue
    }
    Set-ProjectDefaultBranch -ProjectId $p.id -Path $p.path_with_namespace -Token $token -HostName $GitLabHost
}

Write-Host "Done."
