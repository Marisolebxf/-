# TA 联调 · show_py 启动器（凭据自行从 WORKPACK README 提取，不入仓不入日志）
$readme = "e:\work\上达通\项目\深圳GKX\gkx-lumen\gkx-orchestration\agent-delivery\data\GDF\派单包\技术节点产业映射\GDF-TECH-NODE-WORKPACK\README.md"
$raw = Get-Content $readme -Raw -Encoding UTF8
$env:GKX_JIUXIN_ENABLED = "1"
$env:GKX_JIUXIN_HOST = "47.93.119.170"
$env:GKX_JIUXIN_PORT = "29030"
$env:GKX_JIUXIN_USER = "test2"
$env:GKX_JIUXIN_PASSWORD = [regex]::Match($raw, "密码\s*\|\s*`"?'?([^`"'\r\n。]+?)`"?'?\s*。").Groups[1].Value
$env:GKX_JIUXIN_DATABASE = "gkx_technology_analysis_dev"
$env:GKX_JIUXIN_READ_TIMEOUT = "300"
$env:GKX_JIUXIN_CACHE_TTL_SECONDS = "600"
Set-Location "e:\work\上达通\项目\深圳GKX\gkx-lumen\repos\lumen-topic-py"
& python -m uvicorn gkx_show_service.main:app --host 0.0.0.0 --port 8082 *>> "e:\work\上达通\项目\深圳GKX\gkx-lumen\_ta_show_py.log"
