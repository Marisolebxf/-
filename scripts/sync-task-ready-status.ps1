# sync-task-ready-status.ps1
# 按 Kanban 状态机迁移 legacy status，并刷新 backlog/ready/blocked
# 用法：.\scripts\sync-task-ready-status.ps1 [-RegistryPath path] [-WhatIf]

param(
    [string]$RegistryPath = (Join-Path $PSScriptRoot "..\agent-delivery\task-registry.yaml"),
    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"
$content = Get-Content -Path $RegistryPath -Encoding UTF8 -Raw
$lines = $content -split "`r?`n"

$inTasks = $false
$tasks = @()
$current = $null

function Parse-InlineList([string]$value) {
    $value = $value.Trim()
    if ($value -match '^\[(.*)\]$') {
        $inner = $matches[1].Trim()
        if ([string]::IsNullOrWhiteSpace($inner)) { return @() }
        return $inner -split ',\s*' | ForEach-Object { $_.Trim() }
    }
    return @($value)
}

foreach ($line in $lines) {
    if ($line -match '^tasks:\s*$') {
        $inTasks = $true
        continue
    }
    if (-not $inTasks) { continue }

    if ($line -match '^\s+- id:\s*(.+)$') {
        if ($null -ne $current) { $tasks += [pscustomobject]$current }
        $current = @{
            id = $matches[1].Trim()
            status = $null
            depends_on = @()
            blocked_by = $null
            statusLine = $null
        }
        continue
    }

    if ($null -eq $current) { continue }

    if ($line -match '^\s+status:\s*(.+)$') {
        $current.status = $matches[1].Trim()
        $current.statusLine = $line
    }
    elseif ($line -match '^\s+depends_on:\s*(.+)$') {
        $current.depends_on = Parse-InlineList $matches[1]
    }
    elseif ($line -match '^\s+blocked_by:\s*(.+)$') {
        $current.blocked_by = $matches[1].Trim()
    }
}

if ($null -ne $current) { $tasks += [pscustomobject]$current }

$doneIds = [System.Collections.Generic.HashSet[string]]::new(
    [string[]]($tasks | Where-Object { $_.status -in @('done', 'completed') } | ForEach-Object { $_.id })
)

$changes = @()

foreach ($task in $tasks) {
    $old = $task.status
    $new = $old

    switch ($old) {
        'completed' { $new = 'done' }
        'pending' {
            if ($task.blocked_by) {
                $new = 'blocked'
            }
            else {
                $deps = @($task.depends_on | Where-Object { $_ })
                if ($deps.Count -eq 0 -or ($deps | ForEach-Object { $doneIds.Contains($_) } | Where-Object { -not $_ }).Count -eq 0) {
                    $new = 'ready'
                }
                else {
                    $new = 'backlog'
                }
            }
        }
        default { }
    }

    if ($new -ne $old) {
        $changes += [pscustomobject]@{
            id = $task.id
            old = $old
            new = $new
        }
    }
}

Write-Host "Task state sync: $($changes.Count) change(s)"
$changes | Format-Table -AutoSize

if ($WhatIf) {
    Write-Host "WhatIf: no file written."
    exit 0
}

if ($changes.Count -eq 0) {
    Write-Host "No changes needed."
    exit 0
}

$newContent = $content
foreach ($change in $changes) {
    $id = [regex]::Escape($change.id)
    # Replace status only within the task block (first status after this id)
    $pattern = "(  - id: $id[\s\S]*?    status: )$([regex]::Escape($change.old))"
    $replacement = "`${1}$($change.new)"
    $newContent = [regex]::Replace($newContent, $pattern, $replacement, 1)
}

Set-Content -Path $RegistryPath -Value $newContent -Encoding UTF8 -NoNewline
Write-Host "Updated: $RegistryPath"
