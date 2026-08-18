# 构建「向他人介绍编排智能体」PPT（16 页 + speaker notes）
# 主题色对齐 Design.md：主色 #165DFF、页面底 #D8E7FC
# 用法：powershell -ExecutionPolicy Bypass -File .\build_orch_intro_ppt.ps1

$ErrorActionPreference = "Stop"
$OC = "$env:LOCALAPPDATA\OfficeCLI\officecli.exe"
if (-not (Test-Path $OC)) { $OC = "officecli" }
$PPT = Join-Path $PSScriptRoot "2026-08-18_编排智能体介绍.pptx"

$Primary = "165DFF"
$Dark    = "0B1F4D"
$Ice     = "D8E7FC"
$Text    = "1D2129"
$Muted   = "4E5969"
$Card    = "F2F6FC"
$Warn    = "F53F3F"
$White   = "FFFFFF"
$Font    = "Microsoft YaHei"
$Total   = 16

if (Test-Path $PPT) { Remove-Item $PPT -Force }

Write-Host "[init] 创建 $PPT" -ForegroundColor Cyan
& $OC create $PPT | Out-Null
Start-Sleep -Milliseconds 400
& $OC open $PPT | Out-Null
Start-Sleep -Milliseconds 800

function New-Slide {
    param([string]$Background = $script:White)
    & $OC add $script:PPT / --type slide --prop layout=blank --prop background=$Background | Out-Null
}
function Add-Band {
    param([int]$Idx, [string]$Color = $script:Primary)
    & $OC add $script:PPT "/slide[$Idx]" --type shape --prop name=MotifBand --prop geometry=rect `
        --prop x=0cm --prop y=0cm --prop w=0.4cm --prop h=19.05cm `
        --prop fill=$Color --prop line=none | Out-Null
}
function Add-Title {
    param([int]$Idx, [string]$Text, [string]$Color = $script:Text)
    & $OC add $script:PPT "/slide[$Idx]" --type shape --prop name=Title --prop geometry=rect `
        --prop x=1.5cm --prop y=0.9cm --prop w=30.8cm --prop h=2cm `
        --prop "text=$Text" --prop font=$script:Font --prop size=36pt --prop bold=true `
        --prop color=$Color --prop fill=none --prop line=none --prop align=left | Out-Null
}
function Add-Sub {
    param([int]$Idx, [string]$Text)
    & $OC add $script:PPT "/slide[$Idx]" --type shape --prop name=Subtitle --prop geometry=rect `
        --prop x=1.5cm --prop y=3.0cm --prop w=30.8cm --prop h=1.35cm `
        --prop "text=$Text" --prop font=$script:Font --prop size=20pt `
        --prop color=$script:Muted --prop fill=none --prop line=none --prop align=left | Out-Null
}
function Add-Footer {
    param([int]$Idx)
    & $OC add $script:PPT "/slide[$Idx]" --type shape --prop name=Footer --prop geometry=rect `
        --prop x=1.5cm --prop y=18.05cm --prop w=26cm --prop h=0.8cm `
        --prop text="GKX 编排智能体介绍" --prop font=$script:Font --prop size=10pt `
        --prop color=$script:Muted --prop fill=none --prop line=none --prop align=left | Out-Null
    & $OC add $script:PPT "/slide[$Idx]" --type shape --prop name=PageNum --prop geometry=rect `
        --prop x=28.5cm --prop y=18.05cm --prop w=3.8cm --prop h=0.8cm `
        --prop text="$Idx / $script:Total" --prop font=$script:Font --prop size=10pt `
        --prop color=$script:Muted --prop fill=none --prop line=none --prop align=right | Out-Null
}
function Add-Notes {
    param([int]$Idx, [string]$Text)
    & $OC add $script:PPT "/slide[$Idx]" --type notes --prop "text=$Text" | Out-Null
}
function Add-CardBg {
    param([int]$Idx, [string]$Name, [double]$X, [double]$Y, [double]$W, [double]$H, [string]$Fill = $script:Card)
    & $OC add $script:PPT "/slide[$Idx]" --type shape --prop name=$Name --prop geometry=roundRect `
        --prop x=${X}cm --prop y=${Y}cm --prop w=${W}cm --prop h=${H}cm `
        --prop fill=$Fill --prop line=none | Out-Null
}

# ========== 1 封面 ==========
Write-Host "[build] 1/16 封面" -ForegroundColor Yellow
New-Slide -Background $Dark
Add-Band -Idx 1 -Color $Primary
& $OC add $PPT "/slide[1]" --type shape --prop name=Kicker --prop geometry=rect `
    --prop x=1.8cm --prop y=4.3cm --prop w=30cm --prop h=1.2cm `
    --prop text="国科信  ·  科技信息展示 + 科技专题服务" `
    --prop font=$Font --prop size=18pt --prop color=$Ice --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[1]" --type shape --prop name=HeroTitle --prop geometry=rect `
    --prop x=1.8cm --prop y=5.6cm --prop w=30cm --prop h=3.2cm `
    --prop text="向他人介绍编排智能体" `
    --prop font=$Font --prop size=44pt --prop bold=true --prop color=$White --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[1]" --type shape --prop name=HeroSub --prop geometry=rect `
    --prop x=1.8cm --prop y=9.2cm --prop w=30cm --prop h=1.4cm `
    --prop text="定义轨过三门才开工  ·  人看飞书，机器认 registry" `
    --prop font=$Font --prop size=20pt --prop color=$Ice --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[1]" --type shape --prop name=Meta --prop geometry=rect `
    --prop x=1.8cm --prop y=16.2cm --prop w=30cm --prop h=1.1cm `
    --prop text="2026-08-18  ·  15 到 18 分钟  ·  会后带走一页纸" `
    --prop font=$Font --prop size=16pt --prop color="8FA3C8" --prop fill=none --prop line=none --prop align=left | Out-Null
Add-Notes -Idx 1 -Text "今天不讲怎么写提示词，讲我们项目怎么把招标范围变成可派单、可验收的多智能体交付。听完应能回答五件事：和 ChatGPT 写代码有何不同；人还管什么；定义和实现为什么分开；人在飞书上看什么；一张单从范围到签收怎么走。开场点明本场两个重点：双轨、飞书看板。一页纸会后带走。"

# ========== 2 电梯稿 ==========
Write-Host "[build] 2/16 电梯稿" -ForegroundColor Yellow
New-Slide
Add-Band -Idx 2
Add-Title -Idx 2 -Text "三十秒电梯稿"
Add-Sub -Idx 2 -Text "人拍板；双轨过三门才开工；人看飞书，机器认 registry"
$kpis = @(
    @("58", "功能点基线，正负百分之十"),
    @("2", "轨道：定义轨 / 实现轨"),
    @("3", "门：梳理、会签、拍板"),
    @("3x", "人数加 Agent 的产能标尺")
)
$x0 = 1.5; $w = 7.3; $gap = 0.76
for ($i = 0; $i -lt 4; $i++) {
    $x = $x0 + $i * ($w + $gap)
    Add-CardBg -Idx 2 -Name "KpiBg$i" -X $x -Y 4.6 -W $w -H 6.4 -Fill $Primary
    & $OC add $PPT "/slide[2]" --type shape --prop name="KpiNum$i" --prop geometry=rect `
        --prop x=${x}cm --prop y=5.2cm --prop w=${w}cm --prop h=2.6cm `
        --prop "text=$($kpis[$i][0])" --prop font=$Font --prop size=48pt --prop bold=true `
        --prop color=$White --prop fill=none --prop line=none --prop align=center --prop valign=middle | Out-Null
    & $OC add $PPT "/slide[2]" --type shape --prop name="KpiCap$i" --prop geometry=rect `
        --prop x=$($x+0.3)cm --prop y=8.2cm --prop w=$($w-0.6)cm --prop h=2.2cm `
        --prop "text=$($kpis[$i][1])" --prop font=$Font --prop size=18pt `
        --prop color=$Ice --prop fill=none --prop line=none --prop align=center | Out-Null
}
& $OC add $PPT "/slide[2]" --type shape --prop name=Hook --prop geometry=rect `
    --prop x=1.5cm --prop y=11.5cm --prop w=30.8cm --prop h=5.8cm `
    --prop text="Coordinator 不写代码。每张单有完工定义、handoff、CI 与 K8s 证据。\n达不到约三倍人力，就是用 AI 用错了。" `
    --prop font=$Font --prop size=20pt --prop color=$Text --prop fill=none --prop line=none --prop align=left | Out-Null
Add-Footer -Idx 2
Add-Notes -Idx 2 -Text "国科信展示加专题，58 项功能点，多仓并行。一个 Coordinator 加十余类专项 Agent，按任务注册表派活。人拍板范围和架构。交付分定义轨和实现轨：三门评审过完才解锁工程。人看飞书看板，机器认 registry。衡量只有一条：团队人数加 Agent，能不能约等于原来三倍人力。这一页念完停两秒。第 7、8 页就是展开双轨和飞书。"

# ========== 3 三个陷阱 ==========
Write-Host "[build] 3/16 三个陷阱" -ForegroundColor Yellow
New-Slide
Add-Band -Idx 3 -Color $Warn
Add-Title -Idx 3 -Text "个人 AI 的三个团队陷阱"
Add-Sub -Idx 3 -Text "一个人加 AI 像十倍；十个人加十个 AI 不是一百倍"
$traps = @(
    @("不可复用", "张三 prompt 出的组件，李四再写一遍接口就不一样。风格漂移，三个月后没人能维护。"),
    @("不可审计", "甲方问这段谁写的、为什么这样。只能答 AI 写的。出了问题没人扛。"),
    @("不可扩展", "提示词五花八门，产物互相冲突。并行改同一文件，评审和成本一起失控。")
)
for ($i = 0; $i -lt 3; $i++) {
    $x = 1.5 + $i * 10.54
    Add-CardBg -Idx 3 -Name "TrapBg$i" -X $x -Y 4.6 -W 9.78 -H 10.4 -Fill "FDECEC"
    & $OC add $PPT "/slide[3]" --type shape --prop name="TrapT$i" --prop geometry=rect `
        --prop x=$($x+0.45)cm --prop y=5.0cm --prop w=8.88cm --prop h=1.4cm `
        --prop "text=$($traps[$i][0])" --prop font=$Font --prop size=24pt --prop bold=true `
        --prop color=$Warn --prop fill=none --prop line=none --prop align=left | Out-Null
    & $OC add $PPT "/slide[3]" --type shape --prop name="TrapB$i" --prop geometry=rect `
        --prop x=$($x+0.45)cm --prop y=6.6cm --prop w=8.88cm --prop h=7.8cm `
        --prop "text=$($traps[$i][1])" --prop font=$Font --prop size=18pt `
        --prop color=$Text --prop fill=none --prop line=none --prop align=left --prop lineSpacing=1.3x | Out-Null
}
Add-Footer -Idx 3
Add-Notes -Idx 3 -Text "个人用 AI 确实快。团队会塌在三件事。不可复用、不可审计、不可扩展。不是 AI 的错，是个人用 AI 的范式不适合团队。所以要编排，而且要把定什么和做什么分开。共情，不要骂 vibe coding。"

# ========== 4 一句话 ==========
Write-Host "[build] 4/16 一句话" -ForegroundColor Yellow
New-Slide -Background $Dark
Add-Band -Idx 4
& $OC add $PPT "/slide[4]" --type shape --prop name=QuoteKicker --prop geometry=rect `
    --prop x=1.8cm --prop y=2.3cm --prop w=30cm --prop h=1.2cm `
    --prop text="人机分工的一句话" --prop font=$Font --prop size=20pt --prop color=$Ice `
    --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[4]" --type shape --prop name=QuoteBody --prop geometry=rect `
    --prop x=1.8cm --prop y=4.2cm --prop w=30cm --prop h=8.2cm `
    --prop text="人做：决策、评审、创意、客户沟通\n\nAI 做：执行、起草、标准化、并行重复劳动\n\n接口只有三件套：DoD + Handoff + Evidence" `
    --prop font=$Font --prop size=24pt --prop bold=true --prop color=$White `
    --prop fill=none --prop line=none --prop align=left --prop lineSpacing=1.35x | Out-Null
Add-CardBg -Idx 4 -Name QuoteBar -X 1.8 -Y 14.2 -W 30 -H 2.4 -Fill "132A63"
& $OC add $PPT "/slide[4]" --type shape --prop name=QuoteBarText --prop geometry=rect `
    --prop x=2.2cm --prop y=14.5cm --prop w=29.2cm --prop h=1.8cm `
    --prop text="定义轨三道门全是人签字。飞书派单确认，也是人点。" `
    --prop font=$Font --prop size=18pt --prop color=$Ice --prop fill=none --prop line=none --prop align=left --prop valign=middle | Out-Null
Add-Notes -Idx 4 -Text "人做决策、评审、创意、客户沟通。AI 做执行、起草、标准化、并行重复劳动。接口是 DoD、Handoff、Evidence。定义轨的三道门全是人签字。飞书上的派单确认也是人点。这一页慢讲，接到第 7 页。"

# ========== 5 三层 ==========
Write-Host "[build] 5/16 三层" -ForegroundColor Yellow
New-Slide
Add-Band -Idx 5
Add-Title -Idx 5 -Text "三层协作架构"
Add-Sub -Idx 5 -Text "Coordinator 是 Mayor，不是全栈工程师"
$layers = @(
    @($Primary, "战略层", "架构委员会 + PM。范围正负百分之十、架构铁律、对甲方承诺。"),
    @("3C7EFF", "编排层", "coordinator + 架构师。读队列、派 goal、收 handoff。这一层不写业务代码。"),
    @("0B1F4D", "执行层", "各团队 = 人 + 专项 Agent。Lead 定标评审，工程师攻坚，Agent 出量。")
)
for ($i = 0; $i -lt 3; $i++) {
    $y = 4.6 + $i * 4.15
    & $OC add $PPT "/slide[5]" --type shape --prop name="Layer$i" --prop geometry=roundRect `
        --prop x=1.5cm --prop y=${y}cm --prop w=30.8cm --prop h=3.8cm `
        --prop fill=$($layers[$i][0]) --prop line=none | Out-Null
    & $OC add $PPT "/slide[5]" --type shape --prop name="LayerT$i" --prop geometry=rect `
        --prop x=2.1cm --prop y=$($y+0.3)cm --prop w=29.6cm --prop h=1.4cm `
        --prop "text=$($layers[$i][1])" --prop font=$Font --prop size=22pt --prop bold=true `
        --prop color=$White --prop fill=none --prop line=none --prop align=left | Out-Null
    & $OC add $PPT "/slide[5]" --type shape --prop name="LayerB$i" --prop geometry=rect `
        --prop x=2.1cm --prop y=$($y+1.55)cm --prop w=29.6cm --prop h=1.8cm `
        --prop "text=$($layers[$i][2])" --prop font=$Font --prop size=18pt `
        --prop color=$Ice --prop fill=none --prop line=none --prop align=left | Out-Null
}
Add-Footer -Idx 5
Add-Notes -Idx 5 -Text "战略层管范围和铁律。编排层读队列、派 goal、收 handoff，不写业务代码。执行层是人加 Agent。定义轨、实现轨都经 Coordinator 调度，但他自己不写业务代码。用手指三层讲。"

# ========== 6 流转 ==========
Write-Host "[build] 6/16 流转" -ForegroundColor Yellow
New-Slide
Add-Band -Idx 6
Add-Title -Idx 6 -Text "一张单的流转"
Add-Sub -Idx 6 -Text "规范在 git，任务在 registry，证据在 handoff，进度在飞书"
$steps = @("范围 MD", "定义三门", "派 /goal", "handoff", "人签收")
$caps  = @("bid-reference\n不读招标 PDF", "门3 才解锁\n工程 ready", "新会话\n干净上下文", "PR · CI · K8s\n架构自检", "自动验收后\n飞书可见")
for ($i = 0; $i -lt 5; $i++) {
    $x = 1.5 + $i * 6.2
    $name = "Step$i"
    & $OC add $PPT "/slide[6]" --type shape --prop name=$name --prop geometry=roundRect `
        --prop x=${x}cm --prop y=4.7cm --prop w=5.4cm --prop h=2.6cm `
        --prop "text=$($steps[$i])" --prop font=$Font --prop size=20pt --prop bold=true `
        --prop fill=$Primary --prop color=$White --prop line=none --prop align=center --prop valign=middle | Out-Null
    & $OC add $PPT "/slide[6]" --type shape --prop name="StepCap$i" --prop geometry=rect `
        --prop x=${x}cm --prop y=7.6cm --prop w=5.4cm --prop h=2.4cm `
        --prop "text=$($caps[$i])" --prop font=$Font --prop size=18pt `
        --prop color=$Muted --prop fill=none --prop line=none --prop align=center | Out-Null
}
for ($i = 0; $i -lt 4; $i++) {
    $a = $i; $b = $i + 1
    & $OC add $PPT "/slide[6]" --type connector `
        --prop "from=/slide[6]/shape[@name=Step$a]" `
        --prop "to=/slide[6]/shape[@name=Step$b]" `
        --prop shape=straight --prop color=$Primary --prop tailEnd=triangle | Out-Null
}
Add-CardBg -Idx 6 -Name FlowHookBg -X 1.5 -Y 10.6 -W 30.8 -H 6.4 -Fill $Card
& $OC add $PPT "/slide[6]" --type shape --prop name=FlowHook --prop geometry=rect `
    --prop x=2.1cm --prop y=11.0cm --prop w=29.6cm --prop h=5.5cm `
    --prop text="下一页把「定义三门」拆开：先过定义轨，再进实现轨。\n\n不在某个人的聊天记录里。" `
    --prop font=$Font --prop size=20pt --prop color=$Text --prop fill=none --prop line=none --prop align=left | Out-Null
Add-Footer -Idx 6
Add-Notes -Idx 6 -Text "范围从 bid-reference 来。做多少看 58 点正负百分之十。定义三门过完才把工程叶标 ready。Coordinator 开新会话按角色派 goal。做完交 handoff。人签收后飞书上看见。不要在这里展开状态机。把时间留给第 7、8 页。"

# ========== 7 定义轨与实现轨 ==========
Write-Host "[build] 7/16 双轨" -ForegroundColor Yellow
New-Slide
Add-Band -Idx 7
Add-Title -Idx 7 -Text "定义轨与实现轨"
Add-Sub -Idx 7 -Text "不要把「AI 已经在写页面」理解成「产品已经定完」"
Add-CardBg -Idx 7 -Name TrackL -X 1.5 -Y 4.5 -W 15.3 -H 8.6 -Fill $Primary
& $OC add $PPT "/slide[7]" --type shape --prop name=TrackLT --prop geometry=rect `
    --prop x=2.1cm --prop y=4.8cm --prop w=14.1cm --prop h=1.35cm `
    --prop text="定义轨  ·  做什么" --prop font=$Font --prop size=22pt --prop bold=true `
    --prop color=$White --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[7]" --type shape --prop name=TrackLB --prop geometry=rect `
    --prop x=2.1cm --prop y=6.2cm --prop w=14.1cm --prop h=6.5cm `
    --prop text="PACK / UX / 指标\n门 1 梳理 → 故事入库（只提案）\n门 2 会签 → 门 3 拍板\n\nV2 准生产会签仍属定义轨" `
    --prop font=$Font --prop size=18pt --prop color=$Ice --prop fill=none --prop line=none --prop align=left --prop lineSpacing=1.25x | Out-Null
Add-CardBg -Idx 7 -Name TrackR -X 17.56 -Y 4.5 -W 15.3 -H 8.6 -Fill $Ice
& $OC add $PPT "/slide[7]" --type shape --prop name=TrackRT --prop geometry=rect `
    --prop x=18.16cm --prop y=4.8cm --prop w=14.1cm --prop h=1.35cm `
    --prop text="实现轨  ·  怎么做完" --prop font=$Font --prop size=22pt --prop bold=true `
    --prop color=$Primary --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[7]" --type shape --prop name=TrackRB --prop geometry=rect `
    --prop x=18.16cm --prop y=6.2cm --prop w=14.1cm --prop h=6.5cm `
    --prop text="门 3 之后才标 ready\n故事拆单 → 认领联调\nCI / K8s → 人签收\n\n结束标志：leaf done" `
    --prop font=$Font --prop size=18pt --prop color=$Text --prop fill=none --prop line=none --prop align=left --prop lineSpacing=1.25x | Out-Null
Add-CardBg -Idx 7 -Name TrackBar -X 1.5 -Y 13.4 -W 30.8 -H 3.6 -Fill "FDECEC"
& $OC add $PPT "/slide[7]" --type shape --prop name=TrackBarT --prop geometry=rect `
    --prop x=2.1cm --prop y=13.55cm --prop w=29.6cm --prop h=1.15cm `
    --prop text="三条硬边界" --prop font=$Font --prop size=18pt --prop bold=true `
    --prop color=$Warn --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[7]" --type shape --prop name=TrackBarB --prop geometry=rect `
    --prop x=2.1cm --prop y=14.7cm --prop w=29.6cm --prop h=2.1cm `
    --prop text="门 3 前工程不得开工。门 1 后提案不得直接标 ready。故事已完成不等于单张任务 done。" `
    --prop font=$Font --prop size=18pt --prop color=$Text --prop fill=none --prop line=none --prop align=left | Out-Null
Add-Footer -Idx 7
Add-Notes -Idx 7 -Text "这是本场第一重点。左边定义轨：管做什么、长什么样、口径。PACK、UX、指标，过门 1 梳理，故事入库但只是提案；门 2 会签；门 3 项目负责人拍板。V2 准生产会签仍属定义轨，不是联调完成。右边实现轨：门 3 之后才把工程叶标 ready。按用户故事拆单，认领、联调、CI、K8s，最后人签收。三条硬边界。门 3 之前工程不得开工。门 1 之后提案不得直接标 ready。故事已完成不等于单张任务 done，关联叶全部测通才算。被问那现在写的代码算哪边，就答：看有没有过门 3，以及任务的交付阶段是定义还是实现。"

# ========== 8 飞书同步看板 ==========
Write-Host "[build] 8/16 飞书" -ForegroundColor Yellow
New-Slide
Add-Band -Idx 8
Add-Title -Idx 8 -Text "飞书同步看板"
Add-Sub -Idx 8 -Text "人看飞书多维表格；机器认 git 里的 task-registry"
$fs = @(
    @("一张表，分视图", "列「交付阶段」= 定义 / 实现 / 横切。视图：定义看板、实现看板、模块总览。站会不要混着拖。"),
    @("改状态走统一入口", "update-task-status 写 registry 并推板。禁止只改 YAML 结束会话。主动推秒级，投影机一小时兜底。"),
    @("确认才派，故事禁拖", "飞书「派单门控」改成已确认，任务才可派。Loop 不会自动打开 Cursor。故事实现状态禁止手拖。")
)
for ($i = 0; $i -lt 3; $i++) {
    $x = 1.5 + $i * 10.54
    Add-CardBg -Idx 8 -Name "Fs$i" -X $x -Y 4.5 -W 9.78 -H 8.4
    & $OC add $PPT "/slide[8]" --type shape --prop name="FsT$i" --prop geometry=rect `
        --prop x=$($x+0.4)cm --prop y=4.8cm --prop w=8.98cm --prop h=1.6cm `
        --prop "text=$($fs[$i][0])" --prop font=$Font --prop size=20pt --prop bold=true `
        --prop color=$Primary --prop fill=none --prop line=none --prop align=left | Out-Null
    & $OC add $PPT "/slide[8]" --type shape --prop name="FsB$i" --prop geometry=rect `
        --prop x=$($x+0.4)cm --prop y=6.6cm --prop w=8.98cm --prop h=5.9cm `
        --prop "text=$($fs[$i][1])" --prop font=$Font --prop size=18pt `
        --prop color=$Text --prop fill=none --prop line=none --prop align=left --prop lineSpacing=1.25x | Out-Null
}
Add-CardBg -Idx 8 -Name FsBar -X 1.5 -Y 13.2 -W 30.8 -H 3.8 -Fill $Dark
& $OC add $PPT "/slide[8]" --type shape --prop name=FsBarT --prop geometry=rect `
    --prop x=2.1cm --prop y=13.6cm --prop w=29.6cm --prop h=3.0cm `
    --prop text="拖看板列不能代替 git 真源。建单、解锁仍以 registry / MCP / 确认队列为准。" `
    --prop font=$Font --prop size=20pt --prop bold=true --prop color=$White --prop fill=none --prop line=none --prop align=left --prop valign=middle | Out-Null
Add-Footer -Idx 8
Add-Notes -Idx 8 -Text "这是本场第二重点。全员不能去读 YAML。人看飞书多维表格，机器认 git 里的任务注册表。一张表三个视图：定义看板、实现看板、模块总览。改状态必须走统一入口，写 registry 同时推板。禁止只改 YAML 结束会话。主动推板秒级，投影机一小时兜底。派单要人在飞书把派单门控改成已确认，任务才可派。Coordinator 的循环不会自动打开 Cursor。用户故事的实现状态禁止手拖，由关联任务滚动。拖看板列不能代替 git 真源。领导听人看飞书、分定义实现两块板、确认才派。技术同行可提 MCP 和 webhook，不要演示改表。"

# ========== 9 角色禁区 ==========
Write-Host "[build] 9/16 角色禁区" -ForegroundColor Yellow
New-Slide
Add-Band -Idx 9
Add-Title -Idx 9 -Text "角色、仓与禁区"
Add-Sub -Idx 9 -Text "角色不是提示词分类；七个子协调域不是再加一层老板"
Add-CardBg -Idx 9 -Name RoleL -X 1.5 -Y 4.6 -W 15.3 -H 12.4
& $OC add $PPT "/slide[9]" --type shape --prop name=RoleLT --prop geometry=rect `
    --prop x=2.0cm --prop y=4.9cm --prop w=14.3cm --prop h=1.35cm `
    --prop text="必须守住的禁区" --prop font=$Font --prop size=20pt --prop bold=true `
    --prop color=$Primary --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[9]" --type shape --prop name=RoleLB --prop geometry=rect `
    --prop x=2.0cm --prop y=6.3cm --prop w=14.3cm --prop h=10.2cm `
    --prop text="Coordinator / 架构师不写业务代码\n\nui 只进 demo 沙箱，禁止改 lumen\n\nfrontend 复刻已评审页，禁止另起一套\n\n算法只在 Python；前端 → Java → /internal/*" `
    --prop font=$Font --prop size=18pt --prop color=$Text --prop fill=none --prop line=none --prop align=left --prop lineSpacing=1.25x | Out-Null
Add-CardBg -Idx 9 -Name RoleR -X 17.56 -Y 4.6 -W 15.3 -H 12.4 -Fill $Ice
& $OC add $PPT "/slide[9]" --type shape --prop name=RoleRT --prop geometry=rect `
    --prop x=18.06cm --prop y=4.9cm --prop w=14.3cm --prop h=1.35cm `
    --prop text="七个子协调域" --prop font=$Font --prop size=20pt --prop bold=true `
    --prop color=$Primary --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[9]" --type shape --prop name=RoleRB --prop geometry=rect `
    --prop x=18.06cm --prop y=6.3cm --prop w=14.3cm --prop h=10.2cm `
    --prop text="平台　数据算法　血缘\n指标　交互　质量　文档\n\n分担横切风险\n不是再加一层老板 Agent" `
    --prop font=$Font --prop size=18pt --prop color=$Text --prop fill=none --prop line=none --prop align=left --prop lineSpacing=1.3x | Out-Null
Add-Footer -Idx 9
Add-Notes -Idx 9 -Text "角色不是提示词分类，是仓和禁区。对领导一句话带过：各工种有禁区，不能一个助手改全家。对技术同行展开 ui、frontend、Python、调用链。七域用来分担横切，不是再加一层老板。5 分钟场可跳。"

# ========== 10 真源 ==========
Write-Host "[build] 10/16 真源" -ForegroundColor Yellow
New-Slide
Add-Band -Idx 10
Add-Title -Idx 10 -Text "真源分层"
Add-Sub -Idx 10 -Text "抄走的人只记这一页：问什么，看哪份"
$rows = @(
    @("做什么", "bid-reference 两份 MD，不读招标 PDF"),
    @("定义过没过", "产品定义评审规程：门 1 梳理、门 2 会签、门 3 拍板"),
    @("工程能不能开工", "门 3 通过 + 产品实现规程；否则不得标 ready"),
    @("人怎么盯进度", "飞书看板；真源仍是 task-registry，经 MCP"),
    @("代码在哪", "repo-registry：demo 原型，lumen 正式，禁止 merge")
)
for ($i = 0; $i -lt 5; $i++) {
    $y = 4.5 + $i * 2.5
    Add-CardBg -Idx 10 -Name "SrcBg$i" -X 1.5 -Y $y -W 30.8 -H 2.2
    & $OC add $PPT "/slide[10]" --type shape --prop name="SrcQ$i" --prop geometry=rect `
        --prop x=2.0cm --prop y=$($y+0.4)cm --prop w=7.2cm --prop h=1.4cm `
        --prop "text=$($rows[$i][0])" --prop font=$Font --prop size=18pt --prop bold=true `
        --prop color=$Primary --prop fill=none --prop line=none --prop align=left --prop valign=middle | Out-Null
    & $OC add $PPT "/slide[10]" --type shape --prop name="SrcA$i" --prop geometry=rect `
        --prop x=9.4cm --prop y=$($y+0.4)cm --prop w=22.2cm --prop h=1.4cm `
        --prop "text=$($rows[$i][1])" --prop font=$Font --prop size=18pt `
        --prop color=$Text --prop fill=none --prop line=none --prop align=left --prop valign=middle | Out-Null
}
Add-Footer -Idx 10
Add-Notes -Idx 10 -Text "做什么看 bid-reference。定义过没过看三门规程。工程能不能开工看门 3。人盯进度看飞书，真源仍是 registry。代码在哪看 repo-registry。不要逐文件念路径。第 8 页已经讲过飞书。"

# ========== 11 生命周期 ==========
Write-Host "[build] 11/16 生命周期" -ForegroundColor Yellow
New-Slide
Add-Band -Idx 11
Add-Title -Idx 11 -Text "生命周期与质量门"
Add-Sub -Idx 11 -Text "缺证据不收；签收仍是项目负责人；实现叶进实现看板"
$states = @("backlog", "ready", "claimed", "开发", "联调/测试", "待签收", "done")
for ($i = 0; $i -lt 7; $i++) {
    $x = 1.5 + $i * 4.5
    $fill = if ($i -eq 6) { $Primary } else { $Card }
    $col  = if ($i -eq 6) { $White } else { $Text }
    & $OC add $PPT "/slide[11]" --type shape --prop name="St$i" --prop geometry=roundRect `
        --prop x=${x}cm --prop y=4.6cm --prop w=4.1cm --prop h=2.2cm `
        --prop "text=$($states[$i])" --prop font=$Font --prop size=18pt --prop bold=true `
        --prop fill=$fill --prop color=$col --prop line=none --prop align=center --prop valign=middle | Out-Null
}
$gates = @(
    @("机审", "CI 绿、Pipeline、K8s 可访问"),
    @("架构合规", "铁律自检，architect 里程碑扫描"),
    @("业务签收", "lead / QA 评审后，负责人签字")
)
for ($i = 0; $i -lt 3; $i++) {
    $x = 1.5 + $i * 10.54
    Add-CardBg -Idx 11 -Name "Gate$i" -X $x -Y 8.0 -W 9.78 -H 8.8
    & $OC add $PPT "/slide[11]" --type shape --prop name="GateT$i" --prop geometry=rect `
        --prop x=$($x+0.45)cm --prop y=8.4cm --prop w=8.88cm --prop h=1.4cm `
        --prop "text=$($gates[$i][0])" --prop font=$Font --prop size=22pt --prop bold=true `
        --prop color=$Primary --prop fill=none --prop line=none --prop align=left | Out-Null
    & $OC add $PPT "/slide[11]" --type shape --prop name="GateB$i" --prop geometry=rect `
        --prop x=$($x+0.45)cm --prop y=10.1cm --prop w=8.88cm --prop h=6.2cm `
        --prop "text=$($gates[$i][1])" --prop font=$Font --prop size=18pt `
        --prop color=$Text --prop fill=none --prop line=none --prop align=left | Out-Null
}
Add-Footer -Idx 11
Add-Notes -Idx 11 -Text "不要念完整状态机。点两句：认领必须有执行人和真人监管人；Agent 交的不是一段能跑的代码，是带证据的 handoff。实现叶须带 delivery_phase implementation，飞书进实现看板。同仓碰到同一文件就串行，叫 Convoy。"

# ========== 12 长任务 ==========
Write-Host "[build] 12/16 长任务" -ForegroundColor Yellow
New-Slide
Add-Band -Idx 12
Add-Title -Idx 12 -Text "长任务仍走派单"
Add-Sub -Idx 12 -Text "可以直接跑，只免除逐叶问聊天，不免除体系和飞书确认"
Add-CardBg -Idx 12 -Name LongL -X 1.5 -Y 4.6 -W 15.3 -H 12.4 -Fill $Primary
& $OC add $PPT "/slide[12]" --type shape --prop name=LongLT --prop geometry=rect `
    --prop x=2.1cm --prop y=5.1cm --prop w=14.1cm --prop h=1.3cm `
    --prop text="总控一次授权之后" --prop font=$Font --prop size=22pt --prop bold=true `
    --prop color=$White --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[12]" --type shape --prop name=LongLB --prop geometry=rect `
    --prop x=2.1cm --prop y=6.7cm --prop w=14.1cm --prop h=9.6cm `
    --prop text="跨仓闭环或预计过夜\n不必每叶再问聊天\n签收可以积压，主链不停\n同仓同时只派一张 coding 单" `
    --prop font=$Font --prop size=20pt --prop color=$Ice --prop fill=none --prop line=none --prop align=left --prop lineSpacing=1.45x | Out-Null
Add-CardBg -Idx 12 -Name LongR -X 17.56 -Y 4.6 -W 15.3 -H 12.4
& $OC add $PPT "/slide[12]" --type shape --prop name=LongRT --prop geometry=rect `
    --prop x=18.16cm --prop y=5.1cm --prop w=14.1cm --prop h=1.3cm `
    --prop text="每一叶仍然必须有" --prop font=$Font --prop size=22pt --prop bold=true `
    --prop color=$Primary --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[12]" --type shape --prop name=LongRB --prop geometry=rect `
    --prop x=18.16cm --prop y=6.7cm --prop w=14.1cm --prop h=9.6cm `
    --prop text="registry 任务 ID\n认领 + 真人监管人\nhandoff 与自动验收\n飞书派单确认不免除" `
    --prop font=$Font --prop size=20pt --prop color=$Text --prop fill=none --prop line=none --prop align=left --prop lineSpacing=1.45x | Out-Null
Add-Footer -Idx 12
Add-Notes -Idx 12 -Text "跨仓闭环或预计过夜，可以开长任务。禁止开一个超长会话按感觉改代码。无人值守不等于无单无证。飞书确认和看板推送不免除。产业链过夜是现成案例，点到即可，不要展开段 E。"

# ========== 13 裁剪 ==========
Write-Host "[build] 13/16 裁剪" -ForegroundColor Yellow
New-Slide
Add-Band -Idx 13
Add-Title -Idx 13 -Text "按听众裁剪"
Add-Sub -Idx 13 -Text "不要一套稿打天下"
$aud = @(
    @("领导 / 甲方", "人审、双轨三门、飞书两块板。不讲 MCP 和状态机。"),
    @("其他项目组", "编排者-工人、注册表、handoff、角色禁区。"),
    @("新人", "心智 + 自己那一角 mdc + 认领。不讲七域全表。"),
    @("Coordinator", "手册第六、九、十六章 + 长任务规约 + 飞书确认。")
)
for ($i = 0; $i -lt 4; $i++) {
    $col = $i % 2; $row = [Math]::Floor($i / 2)
    $x = 1.5 + $col * 16.06
    $y = 4.6 + $row * 6.4
    Add-CardBg -Idx 13 -Name "Aud$i" -X $x -Y $y -W 15.3 -H 5.9
    & $OC add $PPT "/slide[13]" --type shape --prop name="AudT$i" --prop geometry=rect `
        --prop x=$($x+0.5)cm --prop y=$($y+0.45)cm --prop w=14.3cm --prop h=1.4cm `
        --prop "text=$($aud[$i][0])" --prop font=$Font --prop size=22pt --prop bold=true `
        --prop color=$Primary --prop fill=none --prop line=none --prop align=left | Out-Null
    & $OC add $PPT "/slide[13]" --type shape --prop name="AudB$i" --prop geometry=rect `
        --prop x=$($x+0.5)cm --prop y=$($y+2.1)cm --prop w=14.3cm --prop h=3.3cm `
        --prop "text=$($aud[$i][1])" --prop font=$Font --prop size=18pt `
        --prop color=$Text --prop fill=none --prop line=none --prop align=left | Out-Null
}
Add-Footer -Idx 13
Add-Notes -Idx 13 -Text "今天这场默认合作方或技术同行，双轨和飞书已经加厚。5 分钟场只留封面、电梯稿、一句话、双轨、飞书、带走，也就是 1 到 2、4、7 到 8、16。"

# ========== 14 三问 ==========
Write-Host "[build] 14/16 三问" -ForegroundColor Yellow
New-Slide
Add-Band -Idx 14
Add-Title -Idx 14 -Text "现场三问"
Add-Sub -Idx 14 -Text "被问到就翻到这一页"
$qs = @(
    @("没过评审代码不是在写吗", "那是定义轨的 V1 / V2 或提案，不是实现轨开工。门 3 之前工程叶不得标 ready。"),
    @("和 ChatGPT 有何不同", "ChatGPT 是会话。我们是队列。进度在飞书，真源在 registry，证据在 handoff。"),
    @("能不能无人值守", "长任务可以连夜派叶。飞书派单门控仍要人点确认。无人值守不等于无单无证。")
)
for ($i = 0; $i -lt 3; $i++) {
    $x = 1.5 + $i * 10.54
    Add-CardBg -Idx 14 -Name "Q$i" -X $x -Y 4.6 -W 9.78 -H 12.4
    & $OC add $PPT "/slide[14]" --type shape --prop name="QT$i" --prop geometry=rect `
        --prop x=$($x+0.45)cm --prop y=5.05cm --prop w=8.88cm --prop h=2.8cm `
        --prop "text=$($qs[$i][0])" --prop font=$Font --prop size=20pt --prop bold=true `
        --prop color=$Primary --prop fill=none --prop line=none --prop align=left | Out-Null
    & $OC add $PPT "/slide[14]" --type shape --prop name="QB$i" --prop geometry=rect `
        --prop x=$($x+0.45)cm --prop y=8.1cm --prop w=8.88cm --prop h=8.3cm `
        --prop "text=$($qs[$i][1])" --prop font=$Font --prop size=18pt `
        --prop color=$Text --prop fill=none --prop line=none --prop align=left --prop lineSpacing=1.3x | Out-Null
}
Add-Footer -Idx 14
Add-Notes -Idx 14 -Text "有人提前问双轨或飞书，跳回第 7、8 页。没有问，自己讲完再进索引。三句都要能脱稿。"

# ========== 15 索引 ==========
Write-Host "[build] 15/16 索引" -ForegroundColor Yellow
New-Slide
Add-Band -Idx 15
Add-Title -Idx 15 -Text "原文索引"
Add-Sub -Idx 15 -Text "文档在 git 里，不是某个人硬盘上的 PPT"
$idx = @(
    @("定义三门", "产品定义评审规程.md"),
    @("实现开工", "产品实现规程.md"),
    @("飞书看板", "feishu/README.md"),
    @("今天带走", "培训/编排智能体一页纸.md")
)
for ($i = 0; $i -lt 4; $i++) {
    $x = 1.5 + ($i % 2) * 16.06
    $y = 4.6 + [Math]::Floor($i / 2) * 6.4
    Add-CardBg -Idx 15 -Name "Idx$i" -X $x -Y $y -W 15.3 -H 5.9
    & $OC add $PPT "/slide[15]" --type shape --prop name="IdxT$i" --prop geometry=rect `
        --prop x=$($x+0.5)cm --prop y=$($y+0.7)cm --prop w=14.3cm --prop h=1.5cm `
        --prop "text=$($idx[$i][0])" --prop font=$Font --prop size=22pt --prop bold=true `
        --prop color=$Primary --prop fill=none --prop line=none --prop align=left | Out-Null
    & $OC add $PPT "/slide[15]" --type shape --prop name="IdxB$i" --prop geometry=rect `
        --prop x=$($x+0.5)cm --prop y=$($y+2.5)cm --prop w=14.3cm --prop h=2.6cm `
        --prop "text=$($idx[$i][1])" --prop font=$Font --prop size=18pt `
        --prop color=$Text --prop fill=none --prop line=none --prop align=left | Out-Null
}
Add-Footer -Idx 15
Add-Notes -Idx 15 -Text "定义看产品定义评审规程。实现看产品实现规程。看板看 feishu 目录。不要念文件名，指一页纸底部。操作手册和协作公约也在同一仓。"

# ========== 16 带走 ==========
Write-Host "[build] 16/16 带走" -ForegroundColor Yellow
New-Slide -Background $Dark
Add-Band -Idx 16
& $OC add $PPT "/slide[16]" --type shape --prop name=CloseKicker --prop geometry=rect `
    --prop x=1.8cm --prop y=2.5cm --prop w=30cm --prop h=1.25cm `
    --prop text="带走的三句话" --prop font=$Font --prop size=20pt --prop color=$Ice `
    --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[16]" --type shape --prop name=Close1 --prop geometry=rect `
    --prop x=1.8cm --prop y=4.2cm --prop w=30cm --prop h=2.6cm `
    --prop text="Coordinator 是 Mayor，不是全栈工程师。" `
    --prop font=$Font --prop size=24pt --prop bold=true --prop color=$White `
    --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[16]" --type shape --prop name=Close2 --prop geometry=rect `
    --prop x=1.8cm --prop y=7.2cm --prop w=30cm --prop h=2.6cm `
    --prop text="定义轨过三门，实现轨才开工。" `
    --prop font=$Font --prop size=24pt --prop bold=true --prop color=$Ice `
    --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[16]" --type shape --prop name=Close3 --prop geometry=rect `
    --prop x=1.8cm --prop y=10.2cm --prop w=30cm --prop h=3.2cm `
    --prop text="人看飞书看板，真源仍是 registry。不在聊天记录里。" `
    --prop font=$Font --prop size=24pt --prop bold=true --prop color=$White `
    --prop fill=none --prop line=none --prop align=left | Out-Null
& $OC add $PPT "/slide[16]" --type shape --prop name=CloseAsk --prop geometry=rect `
    --prop x=1.8cm --prop y=15.8cm --prop w=30cm --prop h=1.2cm `
    --prop text="会后请带走一页纸。问题现在问。" `
    --prop font=$Font --prop size=18pt --prop color="8FA3C8" --prop fill=none --prop line=none --prop align=left | Out-Null
Add-Notes -Idx 16 -Text "结束不要加新概念。三句念完停。冷场就抛：谁觉得页面已经出来了等于可以标 ready 开工？会后请带走一页纸。"

Write-Host "[save] close" -ForegroundColor Cyan
& $OC close $PPT | Out-Null
Write-Host "[done] $PPT" -ForegroundColor Green
