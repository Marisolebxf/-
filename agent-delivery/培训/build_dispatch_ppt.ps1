# build_dispatch_ppt.ps1
# 构建「自动派单与飞书确认」培训 PPT（角色 × 飞书场景）
# 用法：powershell -ExecutionPolicy Bypass -File .\build_dispatch_ppt.ps1

$ErrorActionPreference = "Stop"
$OC = "$env:LOCALAPPDATA\OfficeCLI\officecli.exe"
$Batch = Join-Path $PSScriptRoot "build-dispatch-training-batch.json"
$PPT = Join-Path $PSScriptRoot "2026-07-21_dispatch-feishu-training.pptx"

if (-not (Test-Path $OC)) {
    Write-Error "officecli 未安装：$OC"
}
if (-not (Test-Path $Batch)) {
    Write-Error "batch 文件不存在：$Batch"
}

if (Test-Path $PPT) { Remove-Item $PPT -Force }

Write-Host "[init] 创建 PPT: $PPT" -ForegroundColor Cyan
& $OC create $PPT | Out-Null
Start-Sleep -Milliseconds 400

Write-Host "[batch] 执行 $($Batch | Split-Path -Leaf) ..." -ForegroundColor Yellow
& $OC batch $PPT --input $Batch
if ($LASTEXITCODE -ne 0) { throw "officecli batch failed" }

Write-Host "[save] 保存 ..." -ForegroundColor Cyan
& $OC close $PPT | Out-Null

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  派单培训 PPT 构建完成" -ForegroundColor Green
Write-Host "  $PPT" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
