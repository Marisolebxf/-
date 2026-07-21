# build_dispatch_ppt.ps1
# 构建「自动派单与飞书确认-团队协作培训.pptx」（角色 × 飞书场景）
# 用法：powershell -ExecutionPolicy Bypass -File .\build_dispatch_ppt.ps1
#
# 说明：officecli 对中文路径编码不稳定，先写 ASCII 临时文件再 Copy 到中文主文件名。

$ErrorActionPreference = "Stop"
$OC = "$env:LOCALAPPDATA\OfficeCLI\officecli.exe"
$Batch = Join-Path $PSScriptRoot "build-dispatch-training-batch.json"
$PPTBuild = Join-Path $PSScriptRoot "2026-07-21_dispatch-feishu-training.pptx"

if (-not (Test-Path $OC)) {
    Write-Error "officecli 未安装：$OC"
}
if (-not (Test-Path $Batch)) {
    Write-Error "batch 文件不存在：$Batch"
}

# 主交付物：非 dated 前缀的中文 pptx（避免 officecli 中文路径问题）
$PPTMain = Get-ChildItem -LiteralPath $PSScriptRoot -Filter "*.pptx" |
    Where-Object { $_.Name -notmatch '^2026-' } |
    Select-Object -First 1
if (-not $PPTMain) {
    Write-Error "未找到主文件 *团队协作培训.pptx，请确认 agent-delivery/培训/ 目录"
}

if (Test-Path $PPTBuild) { Remove-Item $PPTBuild -Force }

Write-Host "[init] 创建 PPT (build): $PPTBuild" -ForegroundColor Cyan
& $OC create $PPTBuild | Out-Null
Start-Sleep -Milliseconds 400

Write-Host "[batch] 执行 $($Batch | Split-Path -Leaf) ..." -ForegroundColor Yellow
& $OC batch $PPTBuild --input $Batch
if ($LASTEXITCODE -ne 0) { throw "officecli batch failed" }

Write-Host "[save] 保存 build 副本 ..." -ForegroundColor Cyan
& $OC close $PPTBuild | Out-Null

Write-Host "[copy] 同步主文件: $($PPTMain.Name)" -ForegroundColor Cyan
Copy-Item -LiteralPath $PPTBuild -Destination $PPTMain.FullName -Force

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  派单培训 PPT 构建完成" -ForegroundColor Green
Write-Host "  主文件: $($PPTMain.FullName)" -ForegroundColor Green
Write-Host "  副本:   $PPTBuild" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
