# 按 GITLAB-HTMISOFT-DEV-SYNC.md 把旧目录 dev 合入新仓。
# 默认只对照。-Apply 合并并锁回新侧文件（不推送）。-Push 单独推送。
# 自检：powershell -File scripts/sync-legacy-dev.ps1 -SelfTest

param(
    [switch]$Apply,
    [switch]$Push,
    [switch]$SelfTest,
    [string[]]$OnlyRepos = @(),
    [string]$OldRoot = 'F:\gkx-lumen',
    [string]$NewRoot = 'E:\zhipu\gkx-lumen',
    [string]$BranchName = 'sync/legacy-20261017',
    [string]$CommitMarker = '[agent:devops]'
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Test-IsCiPath {
    param([string]$Path)
    $p = $Path -replace '\\', '/'
    if ($p.StartsWith('./')) { $p = $p.Substring(2) }
    $leaf = $p
    $slash = $p.LastIndexOf('/')
    if ($slash -ge 0) { $leaf = $p.Substring($slash + 1) }
    if ($p -eq '.gitlab-ci.yml') { return $true }
    if ($p -eq 'k8s' -or $p.StartsWith('k8s/')) { return $true }
    if ($p -eq 'helm' -or $p.StartsWith('helm/')) { return $true }
    if ($p -eq 'docker' -or $p.StartsWith('docker/')) { return $true }
    if ($leaf -eq 'Dockerfile' -or $leaf.StartsWith('Dockerfile')) { return $true }
    return $false
}

if ($SelfTest) {
    $cases = @{
        '.gitlab-ci.yml' = $true
        'k8s/demo-ui.yaml' = $true
        'helm/gkxlumen-platform/values.yaml' = $true
        'docker/Dockerfile' = $true
        'docker/Dockerfile.api' = $true
        'gkxlumen-auth/Dockerfile' = $true
        'Dockerfile' = $true
        'src/router/menu.ts' = $false
        'gkx_common/nebula.py' = $false
        '.dockerignore' = $false
        'conf/deploy/k8s/entan-api.yaml' = $false
    }
    $failed = 0
    foreach ($k in $cases.Keys) {
        $got = Test-IsCiPath $k
        if ($got -ne $cases[$k]) {
            Write-Output "FAIL $k expected $($cases[$k]) got $got"
            $failed++
        }
    }
    if ($failed -gt 0) { exit 1 }
    Write-Output 'self-test ok'
    exit 0
}

if ($Apply -and $Push) {
    Write-Error '-Apply 与 -Push 分开执行。先 -Apply，核对结果表，再 -Push。'
    exit 2
}

function Invoke-GitText {
    param([string]$Repo, [string[]]$GitArgs)
    $prev = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    $out = & git -C $Repo -c core.quotepath=false @GitArgs 2>&1
    $code = $LASTEXITCODE
    $ErrorActionPreference = $prev
    $text = (($out | ForEach-Object { "$_" }) -join "`n").Trim()
    return [pscustomobject]@{ Code = $code; Text = $text }
}

function Get-DiffRows {
    param([string]$Repo, [string]$From, [string]$To)
    $r = Invoke-GitText -Repo $Repo -GitArgs @('diff', '--name-status', '--no-renames', $From, $To)
    if ($r.Code -ne 0) { throw "git diff 失败 $($r.Text)" }
    $rows = @()
    foreach ($line in ($r.Text -split "`r?`n")) {
        if ($line -match '^([ADMT])\s+(.+)$') {
            $rows += [pscustomobject]@{ Status = $Matches[1]; Path = $Matches[2].Trim() }
        }
    }
    return $rows
}

function Get-PathList {
    param([string]$Repo, [string[]]$GitArgs)
    $r = Invoke-GitText -Repo $Repo -GitArgs $GitArgs
    if ($r.Code -ne 0) { throw $r.Text }
    if (-not $r.Text) { return @() }
    return @($r.Text -split "`r?`n" | Where-Object { $_ })
}

function Test-SamePath {
    param([string]$A, [string]$B)
    $na = $A.TrimEnd('\', '/')
    $nb = $B.TrimEnd('\', '/')
    return ($na.Equals($nb, [System.StringComparison]::OrdinalIgnoreCase))
}

$repos = @(
    @('gkx-orchestration', 'gkx-orchestration', 'gkx-orchestration'),
    @('demo-admin-ui', 'repos\demo-admin-ui', 'repos\demo-admin-ui'),
    @('demo-algo-ent-analysis', 'repos\demo-algo-ent-analysis', 'repos\demo-algo-ent-analysis'),
    @('demo-algo-science', 'repos\demo-algo-science', 'repos\demo-algo-science'),
    @('demo-svc-platform', 'repos\demo-svc-platform', 'repos\demo-svc-platform'),
    @('demo-svc-topic-py', 'repos\demo-svc-topic-py', 'repos\demo-svc-topic-py'),
    @('demo-ui-gaoduanzhiku-view', 'repos\demo-ui-gaoduanzhiku-view', 'repos\demo-ui-gaoduanzhiku-view'),
    @('demo-ui-gdzk', 'repos\demo-ui-gdzk', 'repos\demo-ui-gdzk'),
    @('demo-ui-science', 'repos\demo-ui-science', 'repos\demo-ui-science'),
    @('demo-ui-system-test', 'repos\demo-ui-system-test', 'repos\demo-ui-system-test'),
    @('demo-ui-topic', 'repos\demo-ui-topic', 'repos\demo-ui-topic'),
    @('lumen-algo-py', 'repos\lumen-algo-py', 'repos\lumen-algo-py'),
    @('lumen-etl-es-py', 'repos\lumen-etl-es-py', 'repos\lumen-etl-es-py'),
    @('lumen-svc-platform', 'repos\lumen-svc-platform', 'repos\lumen-svc-platform'),
    @('lumen-topic-py', 'repos\lumen-topic-py', 'repos\lumen-topic-py'),
    @('lumen-ui-algo-apiview', 'repos\lumen-ui-algo-apiview', 'repos\lumen-ui-algo-apiview'),
    @('lumen-ui-science-mobile', 'repos\lumen-ui-science-mobile', 'repos\lumen-ui-science-mobile'),
    @('lumen-ui-science-pc', 'repos\lumen-ui-science-pc', 'repos\lumen-ui-science-pc'),
    @('lumen-ui-topic', 'repos\lumen-ui-topic', 'repos\lumen-ui-topic'),
    @('lumen-ui-topic-mobile', 'repos\lumen-ui-topic-mobile', 'repos\lumen-ui-topic-mobile')
)

function Resolve-OldDevRef {
    param([string]$OldRepo)
    $heads = Invoke-GitText -Repo $OldRepo -GitArgs @('rev-parse', '--verify', '--quiet', 'refs/heads/dev')
    if ($heads.Code -eq 0 -and $heads.Text) { return 'refs/heads/dev' }
    $origin = Invoke-GitText -Repo $OldRepo -GitArgs @('rev-parse', '--verify', '--quiet', 'refs/remotes/origin/dev')
    if ($origin.Code -eq 0 -and $origin.Text) { return 'refs/remotes/origin/dev' }
    return $null
}

function Get-LockSet {
    param([string]$Repo, [string]$MergeBase, [string]$NewSha, [string[]]$IndexPaths)
    $set = New-Object 'System.Collections.Generic.HashSet[string]'
    foreach ($row in (Get-DiffRows -Repo $Repo -From $MergeBase -To $NewSha)) {
        [void]$set.Add($row.Path)
    }
    $tree = Get-PathList -Repo $Repo -GitArgs @('ls-tree', '-r', '--name-only', $NewSha)
    foreach ($p in $tree) {
        if (Test-IsCiPath $p) { [void]$set.Add($p) }
    }
    foreach ($p in $IndexPaths) {
        if (Test-IsCiPath $p) { [void]$set.Add($p) }
    }
    return @($set)
}

function Test-LockDiffEmpty {
    param(
        [string]$Repo,
        [string]$FromSha,
        [string]$ToRev,
        [string[]]$Section9Paths,
        [System.Collections.Generic.HashSet[string]]$InFromTree
    )
    $ci = Invoke-GitText -Repo $Repo -GitArgs @('diff', '--exit-code', $FromSha, $ToRev, '--', '.gitlab-ci.yml', 'k8s', 'helm', 'docker')
    if ($ci.Code -ne 0) { return $false }
    foreach ($row in (Get-DiffRows -Repo $Repo -From $FromSha -To $ToRev)) {
        if (Test-IsCiPath $row.Path) { return $false }
    }
    $present = @($Section9Paths | Where-Object { $InFromTree.Contains($_) })
    for ($i = 0; $i -lt $present.Count; $i += 40) {
        $end = [Math]::Min($i + 39, $present.Count - 1)
        $slice = @($present[$i..$end])
        $args = @('diff', '--exit-code', $FromSha, $ToRev, '--') + $slice
        $r = Invoke-GitText -Repo $Repo -GitArgs $args
        if ($r.Code -ne 0) { return $false }
    }
    foreach ($p in @($Section9Paths | Where-Object { -not $InFromTree.Contains($_) })) {
        $still = Invoke-GitText -Repo $Repo -GitArgs @('cat-file', '-e', "${ToRev}:${p}")
        if ($still.Code -eq 0) { return $false }
    }
    return $true
}

function Restore-Locked {
    param([string]$Repo, [string]$Sha, [string[]]$Paths, [System.Collections.Generic.HashSet[string]]$InTree)
    $restore = @()
    $remove = @()
    foreach ($p in $Paths) {
        if ($InTree.Contains($p)) { $restore += $p } else { $remove += $p }
    }
    for ($i = 0; $i -lt $restore.Count; $i += 40) {
        $end = [Math]::Min($i + 39, $restore.Count - 1)
        $slice = @($restore[$i..$end])
        $args = @('checkout', $Sha, '--') + $slice
        $r = Invoke-GitText -Repo $Repo -GitArgs $args
        if ($r.Code -ne 0) { throw "checkout 锁定路径失败 $($r.Text)" }
    }
    foreach ($p in $remove) {
        $rm = Invoke-GitText -Repo $Repo -GitArgs @('rm', '-rf', '--ignore-unmatch', '--', $p)
        if ($rm.Code -ne 0) { throw "删除锁定路径失败 $p $($rm.Text)" }
    }
}

function Reset-Apply {
    param([string]$Repo, [string]$Prev, [string]$Branch, [bool]$Created)
    $merge = Invoke-GitText -Repo $Repo -GitArgs @('rev-parse', '--verify', '--quiet', 'MERGE_HEAD')
    if ($merge.Code -eq 0) {
        Invoke-GitText -Repo $Repo -GitArgs @('merge', '--abort') | Out-Null
    }
    if ($Prev -and $Prev -ne 'HEAD') {
        Invoke-GitText -Repo $Repo -GitArgs @('switch', $Prev) | Out-Null
    }
    if ($Created) {
        Invoke-GitText -Repo $Repo -GitArgs @('branch', '-D', $Branch) | Out-Null
    }
}

$rows = @()
$mode = '对照'
if ($Apply) { $mode = '合并' }
if ($Push) { $mode = '推送' }

foreach ($item in $repos) {
    $name = $item[0]
    if ($OnlyRepos.Count -gt 0 -and ($OnlyRepos -notcontains $name)) { continue }
    $newRepo = Join-Path $NewRoot $item[1]
    $oldRepo = Join-Path $OldRoot $item[2]
    $row = [ordered]@{
        Name = $name
        Old = ''
        New = ''
        Ahead = ''
        Behind = ''
        Action = '停止'
        LockOk = ''
        CiDropped = ''
        Note = ''
    }

    if (-not (Test-Path -LiteralPath (Join-Path $newRepo '.git'))) {
        $row.Note = '新目录不是 git 仓'
        $rows += [pscustomobject]$row
        continue
    }
    if (-not (Test-Path -LiteralPath (Join-Path $oldRepo '.git'))) {
        $row.Note = '旧目录不是 git 仓'
        $rows += [pscustomobject]$row
        continue
    }

    $oldRef = Resolve-OldDevRef $oldRepo
    if (-not $oldRef) {
        $row.Note = '旧目录没有 dev 或 origin/dev'
        $rows += [pscustomobject]$row
        continue
    }

    $fetchRef = 'refs/temp/sync-legacy-dev'
    $fetch = Invoke-GitText -Repo $newRepo -GitArgs @('fetch', '--no-tags', $oldRepo, "${oldRef}:${fetchRef}")
    if ($fetch.Code -ne 0) {
        $row.Note = "fetch 失败 $($fetch.Text)"
        $rows += [pscustomobject]$row
        continue
    }
    $oldSha = (Invoke-GitText -Repo $newRepo -GitArgs @('rev-parse', $fetchRef)).Text
    $newSha = (Invoke-GitText -Repo $newRepo -GitArgs @('rev-parse', 'origin/dev')).Text
    $row.Old = $oldSha
    $row.New = $newSha

    $baseR = Invoke-GitText -Repo $newRepo -GitArgs @('merge-base', $newSha, $oldSha)
    if ($baseR.Code -ne 0) {
        $row.Note = '没有共同祖先'
        Invoke-GitText -Repo $newRepo -GitArgs @('update-ref', '-d', $fetchRef) | Out-Null
        $rows += [pscustomobject]$row
        continue
    }
    $mergeBase = $baseR.Text.Trim()
    $countR = Invoke-GitText -Repo $newRepo -GitArgs @('rev-list', '--left-right', '--count', "${newSha}...${oldSha}")
    $parts = $countR.Text -split '\s+'
    $left = [int]$parts[0]
    $right = [int]$parts[1]
    $row.Ahead = "$left"
    $row.Behind = "$right"

    $treeSet = New-Object 'System.Collections.Generic.HashSet[string]'
    foreach ($p in (Get-PathList -Repo $newRepo -GitArgs @('ls-tree', '-r', '--name-only', $newSha))) {
        [void]$treeSet.Add($p)
    }
    # 旧树里的 CI 路径也放进锁定集合，避免旧站在 k8s/helm/docker 里新增的文件被快进带进来。
    $oldTree = Get-PathList -Repo $newRepo -GitArgs @('ls-tree', '-r', '--name-only', $oldSha)
    $lock = @(Get-LockSet -Repo $newRepo -MergeBase $mergeBase -NewSha $newSha -IndexPaths $oldTree)
    $section9 = @(Get-DiffRows -Repo $newRepo -From $mergeBase -To $newSha | ForEach-Object { $_.Path })
    $ciNames = @(Get-DiffRows -Repo $newRepo -From $newSha -To $oldSha | Where-Object { Test-IsCiPath $_.Path })
    $row.CiDropped = $(if ($ciNames.Count -gt 0) { '是' } else { '否' })

    if ($right -eq 0) {
        $row.Action = '跳过'
        $row.LockOk = '是'
        $row.CiDropped = '否'
        $row.Note = '旧 dev 没有新提交'
    }
    elseif ($left -eq 0 -and (Test-LockDiffEmpty -Repo $newRepo -FromSha $newSha -ToRev $oldSha -Section9Paths $section9 -InFromTree $treeSet)) {
        $row.Action = '快进'
        $row.CiDropped = '否'
        $row.Note = '锁定路径与旧 dev 相同，可以快进'
    }
    else {
        $row.Action = '合并'
        $row.Note = '分叉或锁定路径有差异，合并后整文件锁回新 dev'
    }

    if ($Push) {
        if ($row.Action -eq '跳过' -or $row.Action -eq '停止') {
            Invoke-GitText -Repo $newRepo -GitArgs @('update-ref', '-d', $fetchRef) | Out-Null
            $rows += [pscustomobject]$row
            continue
        }
        $branchSha = Invoke-GitText -Repo $newRepo -GitArgs @('rev-parse', '--verify', '--quiet', $BranchName)
        if ($branchSha.Code -ne 0) {
            $row.Action = '停止'
            $row.LockOk = '否'
            $row.Note = "没有分支 $BranchName"
        }
        else {
            $ok = Test-LockDiffEmpty -Repo $newRepo -FromSha $newSha -ToRev $BranchName -Section9Paths $section9 -InFromTree $treeSet
            $dirty = Invoke-GitText -Repo $newRepo -GitArgs @('status', '--porcelain')
            if (-not $ok) {
                $row.Action = '停止'
                $row.LockOk = '否'
                $row.Note = '锁定路径与 origin/dev 不一致，不推送'
            }
            elseif ($dirty.Text) {
                $row.Action = '停止'
                $row.LockOk = '是'
                $row.Note = '工作区不干净，不推送'
            }
            else {
                $pushR = Invoke-GitText -Repo $newRepo -GitArgs @('push', 'origin', "${BranchName}:dev")
                if ($pushR.Code -ne 0) {
                    $row.Action = '停止'
                    $row.LockOk = '是'
                    $row.Note = "push 失败 $($pushR.Text)"
                }
                else {
                    $row.Action = '已推送'
                    $row.LockOk = '是'
                    $row.Note = $pushR.Text
                }
            }
        }
        Invoke-GitText -Repo $newRepo -GitArgs @('update-ref', '-d', $fetchRef) | Out-Null
        $rows += [pscustomobject]$row
        continue
    }

    if (-not $Apply -or $row.Action -eq '跳过') {
        if (-not $Apply) { $row.LockOk = '未执行' }
        Invoke-GitText -Repo $newRepo -GitArgs @('update-ref', '-d', $fetchRef) | Out-Null
        $rows += [pscustomobject]$row
        continue
    }

    $dirty = Invoke-GitText -Repo $newRepo -GitArgs @('status', '--porcelain')
    if ($dirty.Text) {
        $row.Action = '停止'
        $row.LockOk = '否'
        $row.Note = '工作区不干净'
        Invoke-GitText -Repo $newRepo -GitArgs @('update-ref', '-d', $fetchRef) | Out-Null
        $rows += [pscustomobject]$row
        continue
    }

    $remote = Invoke-GitText -Repo $newRepo -GitArgs @('remote', 'get-url', 'legacy')
    if ($remote.Code -ne 0) {
        $add = Invoke-GitText -Repo $newRepo -GitArgs @('remote', 'add', 'legacy', $oldRepo)
        if ($add.Code -ne 0) { throw "remote add 失败 $($add.Text)" }
        $remote = Invoke-GitText -Repo $newRepo -GitArgs @('remote', 'get-url', 'legacy')
    }
    elseif (-not (Test-SamePath $remote.Text $oldRepo)) {
        $row.Action = '停止'
        $row.LockOk = '否'
        $row.Note = "legacy 已指向 $($remote.Text)，与旧目录不一致"
        Invoke-GitText -Repo $newRepo -GitArgs @('update-ref', '-d', $fetchRef) | Out-Null
        $rows += [pscustomobject]$row
        continue
    }
    if ($remote.Text -match 'glpat-|:[^/]+@') {
        $row.Action = '停止'
        $row.LockOk = '否'
        $row.Note = 'legacy URL 含访问令牌'
        Invoke-GitText -Repo $newRepo -GitArgs @('update-ref', '-d', $fetchRef) | Out-Null
        $rows += [pscustomobject]$row
        continue
    }

    $exists = Invoke-GitText -Repo $newRepo -GitArgs @('rev-parse', '--verify', '--quiet', "refs/heads/$BranchName")
    if ($exists.Code -eq 0) {
        $row.Action = '停止'
        $row.LockOk = '否'
        $row.Note = "分支 $BranchName 已存在"
        Invoke-GitText -Repo $newRepo -GitArgs @('update-ref', '-d', $fetchRef) | Out-Null
        $rows += [pscustomobject]$row
        continue
    }

    $prev = (Invoke-GitText -Repo $newRepo -GitArgs @('rev-parse', '--abbrev-ref', 'HEAD')).Text
    $created = $false
    $committed = $false
    try {
        $sw = Invoke-GitText -Repo $newRepo -GitArgs @('switch', '-c', $BranchName, $newSha)
        if ($sw.Code -ne 0) { throw "建分支失败 $($sw.Text)" }
        $created = $true
        if ($row.Action -eq '快进') {
            $ff = Invoke-GitText -Repo $newRepo -GitArgs @('merge', '--ff-only', $oldSha)
            if ($ff.Code -ne 0) { throw "快进失败 $($ff.Text)" }
            $committed = $true
        }
        else {
            $mg = Invoke-GitText -Repo $newRepo -GitArgs @('merge', '--no-commit', '--no-ff', $oldSha)
            if ($mg.Code -gt 1 -and $mg.Text -match 'fatal:') { throw "merge 失败 $($mg.Text)" }
            $indexAfter = Get-PathList -Repo $newRepo -GitArgs @('ls-files')
            $lock = @(Get-LockSet -Repo $newRepo -MergeBase $mergeBase -NewSha $newSha -IndexPaths $indexAfter)
            Restore-Locked -Repo $newRepo -Sha $newSha -Paths $lock -InTree $treeSet
            $unmerged = Invoke-GitText -Repo $newRepo -GitArgs @('ls-files', '-u')
            if ($unmerged.Text) {
                $row.Action = '停止'
                $row.LockOk = '否'
                $row.Note = "业务文件仍有冲突 $($unmerged.Text)"
                throw 'conflicts'
            }
            $staged = Invoke-GitText -Repo $newRepo -GitArgs @('diff', '--cached', '--exit-code', $newSha)
            if ($staged.Code -eq 0) {
                $row.Action = '跳过'
                $row.LockOk = '是'
                $row.CiDropped = '是'
                $row.Note = '旧侧改动都在锁定路径上，已整文件丢弃'
                throw 'empty-merge'
            }
            if (-not (Test-LockDiffEmpty -Repo $newRepo -FromSha $newSha -ToRev 'HEAD' -Section9Paths $section9 -InFromTree $treeSet)) {
                $row.Action = '停止'
                $row.LockOk = '否'
                $row.Note = '锁回后工作区与新 dev 的锁定路径仍有差异'
                throw 'lock-mismatch'
            }
            $msg1 = "merge(legacy): 合入旧站 dev 的业务提交 $CommitMarker"
            $msg2 = "锁定路径与 $newSha 字节一致。CI/CD 与导入之后的新侧文件保持新侧整文件。"
            $cm = Invoke-GitText -Repo $newRepo -GitArgs @('commit', '-m', $msg1, '-m', $msg2)
            if ($cm.Code -ne 0) { throw "commit 失败 $($cm.Text)" }
            $committed = $true
            $row.LockOk = '是'
        }
        if ($committed -and -not (Test-LockDiffEmpty -Repo $newRepo -FromSha $newSha -ToRev 'HEAD' -Section9Paths $section9 -InFromTree $treeSet)) {
            $row.Action = '停止'
            $row.LockOk = '否'
            $row.Note = '提交后锁定路径与 origin/dev 不一致'
        }
        elseif ($row.Action -eq '快进') {
            $row.LockOk = '是'
        }
        Invoke-GitText -Repo $newRepo -GitArgs @('switch', $prev) | Out-Null
    }
    catch {
        if (-not $committed) {
            Reset-Apply -Repo $newRepo -Prev $prev -Branch $BranchName -Created $created
            if (-not $row.Note) { $row.Note = "$_" }
            if ($row.Action -eq '合并') { $row.Action = '停止' }
        }
    }
    Invoke-GitText -Repo $newRepo -GitArgs @('update-ref', '-d', $fetchRef) | Out-Null
    $rows += [pscustomobject]$row
}

$lines = @(
    "# 旧站 dev 同步结果",
    "",
    "- 模式：$mode",
    "- 时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    "- 分支：$BranchName",
    "",
    "| 项目路径 | 旧 HEAD | 新 HEAD | 新侧领先 | 旧侧领先 | 处理 | 锁定路径 diff 是否为空 | 旧侧 CI 被整文件丢弃 | 说明 |",
    "|---|---|---|---:|---:|---|---|---|---|"
)
foreach ($row in $rows) {
    $oldS = if ($row.Old) { $row.Old.Substring(0, [Math]::Min(12, $row.Old.Length)) } else { '' }
    $newS = if ($row.New) { $row.New.Substring(0, [Math]::Min(12, $row.New.Length)) } else { '' }
    $note = ($row.Note -replace '\|', '/').Replace("`r", ' ').Replace("`n", ' ')
    $lines += "| $($row.Name) | $oldS | $newS | $($row.Ahead) | $($row.Behind) | $($row.Action) | $($row.LockOk) | $($row.CiDropped) | $note |"
}
$outPath = Join-Path $NewRoot 'gkx-orchestration\agent-delivery\agent-handoffs\平台基建-PLATFORM\GITLAB-HTMISOFT-DEV-SYNC-result.md'
$utf8 = New-Object System.Text.UTF8Encoding $true
[System.IO.File]::WriteAllLines($outPath, $lines, $utf8)
$rows | ForEach-Object { Write-Output ("{0}`t{1}`t领先{2}`t落后{3}`t锁定{4}`t丢弃CI{5}`t{6}" -f $_.Name, $_.Action, $_.Ahead, $_.Behind, $_.LockOk, $_.CiDropped, $_.Note) }
Write-Output "结果表 $outPath"
$bad = @($rows | Where-Object { $_.Action -eq '停止' })
if ($bad.Count -gt 0) { exit 1 }
exit 0
