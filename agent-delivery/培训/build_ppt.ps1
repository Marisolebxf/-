# build_ppt.ps1
# 用 officecli 构建团队宣讲 PPT（31 页 + speaker notes）
# 主题：从 Vibe Coding 到团队 AI 协作
# 日期：2026-06-18 团队宣讲（1 小时）
# 用法：powershell -ExecutionPolicy Bypass -File .\build_ppt.ps1
# 重跑：删 .pptx 文件后重跑即可（脚本是 create + add 模式）

$ErrorActionPreference = "Stop"
$OC = "$env:LOCALAPPDATA\OfficeCLI\officecli.exe"
$PPT = Join-Path $PSScriptRoot "2026-06-18_团队AI协作宣讲.pptx"

# 调色板（Teal Trust，科技 + 信任 + 成长）
$Primary   = "028090"   # 海蓝
$Secondary = "00A896"   # 青翠
$Accent    = "02C39A"   # 翡翠
$Text      = "2D3B3B"   # 深炭
$Muted     = "5E8C8C"   # 灰蓝
$BgLight   = "FFFFFF"
$BgDark    = "0B3B3F"   # 深绿青色（封面/divider）
$CardLight = "F4F8F8"
$Warn      = "F96167"   # 警示红（红线/告警）
$Font      = "Microsoft YaHei"

# 删除旧文件，重新构建
if (Test-Path $PPT) { Remove-Item $PPT }

Write-Host "[init] 创建 PPT: $PPT" -ForegroundColor Cyan
& $OC create $PPT | Out-Null
Start-Sleep -Milliseconds 500

# 显式启动 resident process 接管文件，避免 auto-start 竞态导致的 file lock 冲突
Write-Host "[init] 启动 resident 进程..." -ForegroundColor Cyan
& $OC open $PPT | Out-Null
Start-Sleep -Milliseconds 1500

# ============ 辅助函数 ============

function New-Slide {
    param([string]$Background = $BgLight)
    & $OC add $PPT / --type slide --prop layout=blank --prop background=$Background | Out-Null
}

function Add-Motif {
    # 左侧 0.4cm 色带（统一视觉锚点）
    param([int]$Idx, [string]$Color = $script:Primary)
    & $OC add $PPT "/slide[$Idx]" --type shape `
        --prop geometry=rect --prop x=0cm --prop y=0cm --prop w=0.4cm --prop h=19.05cm `
        --prop fill=$Color --prop line.width=0 | Out-Null
}

function Add-Title {
    param([int]$Idx, [string]$Text, [string]$Color = $script:Text, [int]$Size = 36, [double]$Y = 1.0)
    & $OC add $PPT "/slide[$Idx]" --type shape `
        --prop geometry=rect --prop x=1.2cm --prop y=${Y}cm --prop w=31cm --prop h=2cm `
        --prop text=$Text --prop font=$script:Font --prop size=${Size}pt --prop bold=true `
        --prop color=$Color --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
}

function Add-SubTitle {
    param([int]$Idx, [string]$Text, [string]$Color = $script:Muted, [int]$Size = 18, [double]$Y = 3.2)
    & $OC add $PPT "/slide[$Idx]" --type shape `
        --prop geometry=rect --prop x=1.2cm --prop y=${Y}cm --prop w=31cm --prop h=1.2cm `
        --prop text=$Text --prop font=$script:Font --prop size=${Size}pt `
        --prop color=$Color --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
}

function Add-Body {
    param([int]$Idx, [string]$Text, [double]$X = 1.2, [double]$Y = 5.0,
          [double]$W = 31, [double]$H = 12, [int]$Size = 18, [string]$Color = $script:Text,
          [string]$Align = "left", [string]$Fill = "transparent")
    & $OC add $PPT "/slide[$Idx]" --type shape `
        --prop geometry=rect --prop x=${X}cm --prop y=${Y}cm --prop w=${W}cm --prop h=${H}cm `
        --prop text=$Text --prop font=$script:Font --prop size=${Size}pt `
        --prop color=$Color --prop fill=$Fill --prop line.width=0 --prop align=$Align `
        --prop lineSpacing=1.4x | Out-Null
}

function Add-Card {
    # 圆角卡片 = 1 个 roundRect 背景 + 1 个 text shape 在其上
    param([int]$Idx, [double]$X, [double]$Y, [double]$W, [double]$H,
          [string]$Title, [string]$Body,
          [string]$Fill = $script:CardLight, [string]$TitleColor = $script:Primary,
          [int]$TitleSize = 20, [int]$BodySize = 14)
    & $OC add $PPT "/slide[$Idx]" --type shape `
        --prop geometry=roundRect --prop x=${X}cm --prop y=${Y}cm --prop w=${W}cm --prop h=${H}cm `
        --prop fill=$Fill --prop line.width=0 | Out-Null
    & $OC add $PPT "/slide[$Idx]" --type shape `
        --prop geometry=rect `
        --prop x=$($X + 0.4)cm --prop y=$($Y + 0.3)cm --prop w=$($W - 0.8)cm --prop h=0.9cm `
        --prop text=$Title --prop font=$script:Font --prop size=${TitleSize}pt --prop bold=true `
        --prop color=$TitleColor --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
    & $OC add $PPT "/slide[$Idx]" --type shape `
        --prop geometry=rect `
        --prop x=$($X + 0.4)cm --prop y=$($Y + 1.3)cm --prop w=$($W - 0.8)cm --prop h=$($H - 1.5)cm `
        --prop text=$Body --prop font=$script:Font --prop size=${BodySize}pt `
        --prop color=$script:Text --prop fill=transparent --prop line.width=0 --prop align=left `
        --prop lineSpacing=1.4x | Out-Null
}

function Add-BigStat {
    # KPI 巨数 = 1 个大数字（60pt bold）+ 1 行副标
    param([int]$Idx, [double]$X, [double]$Y, [double]$W,
          [string]$Number, [string]$Caption,
          [string]$NumberColor = $script:Primary, [int]$NumberSize = 60, [int]$CaptionSize = 14)
    & $OC add $PPT "/slide[$Idx]" --type shape `
        --prop geometry=rect --prop x=${X}cm --prop y=${Y}cm --prop w=${W}cm --prop h=2.5cm `
        --prop text=$Number --prop font=$script:Font --prop size=${NumberSize}pt --prop bold=true `
        --prop color=$NumberColor --prop fill=transparent --prop line.width=0 --prop align=center | Out-Null
    & $OC add $PPT "/slide[$Idx]" --type shape `
        --prop geometry=rect --prop x=${X}cm --prop y=$($Y + 2.6)cm --prop w=${W}cm --prop h=1cm `
        --prop text=$Caption --prop font=$script:Font --prop size=${CaptionSize}pt `
        --prop color=$script:Muted --prop fill=transparent --prop line.width=0 --prop align=center | Out-Null
}

function Add-Footer {
    param([int]$Idx, [string]$Text)
    & $OC add $PPT "/slide[$Idx]" --type shape `
        --prop geometry=rect --prop x=1.2cm --prop y=18.2cm --prop w=31cm --prop h=0.6cm `
        --prop text=$Text --prop font=$script:Font --prop size=10pt --prop color=$script:Muted `
        --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
}

function Add-PageNum {
    param([int]$Idx, [int]$Total = 31)
    & $OC add $PPT "/slide[$Idx]" --type shape `
        --prop geometry=rect --prop x=31cm --prop y=18.2cm --prop w=2cm --prop h=0.6cm `
        --prop text="$Idx / $Total" --prop font=$script:Font --prop size=10pt --prop color=$script:Muted `
        --prop fill=transparent --prop line.width=0 --prop align=right | Out-Null
}

function Set-Notes {
    param([int]$Idx, [string]$Text)
    & $OC set $PPT "/slide[$Idx]" --prop notes=$Text | Out-Null
}

# ============ 第 1 页：封面 ============
Write-Host "[build] 封面 (1/31)" -ForegroundColor Yellow
New-Slide -Background $BgDark
& $OC add $PPT "/slide[1]" --type shape `
    --prop geometry=rect --prop x=0cm --prop y=0cm --prop w=0.4cm --prop h=19.05cm `
    --prop fill=$Accent --prop line.width=0 | Out-Null
# 主标题
& $OC add $PPT "/slide[1]" --type shape `
    --prop geometry=rect --prop x=2.5cm --prop y=5.5cm --prop w=29cm --prop h=3cm `
    --prop text="从 Vibe Coding 到团队 AI 协作" `
    --prop font=$Font --prop size=54pt --prop bold=true `
    --prop color="FFFFFF" --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
# 副标题
& $OC add $PPT "/slide[1]" --type shape `
    --prop geometry=rect --prop x=2.5cm --prop y=9cm --prop w=29cm --prop h=1.5cm `
    --prop text="国科信「科技信息展示系统 + 科技专题服务系统」团队宣讲" `
    --prop font=$Font --prop size=22pt `
    --prop color=$Accent --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
# 一句话价值
& $OC add $PPT "/slide[1]" --type shape `
    --prop geometry=rect --prop x=2.5cm --prop y=12cm --prop w=29cm --prop h=1.2cm `
    --prop text="让 AI 从「玩具」变成「团队的可扩展产能」" `
    --prop font=$Font --prop size=18pt `
    --prop color="CADCFC" --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
# 日期 + 时长
& $OC add $PPT "/slide[1]" --type shape `
    --prop geometry=rect --prop x=2.5cm --prop y=16cm --prop w=29cm --prop h=0.8cm `
    --prop text="2026-06-18  ·  1 小时  ·  讲者：项目协调组" `
    --prop font=$Font --prop size=14pt `
    --prop color="8899BB" --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
Set-Notes -Idx 1 -Text "开场 1 分钟：大家好，今天我们用 1 小时把团队的 AI 协作方式做一次系统升级。先抛个反问：每个人都在用 Cursor、用 AI 帮自己写代码——但这是不是「团队级别」的 AI 协作？我打个赌：很多人答不上来。今天讲完，每个人都能答上来，而且能落地。背景：这是我们国科信项目的内部宣讲，对象是已经会 vibe coding 的入门 AI 使用者，目标是把大家从「个人玩 AI」升级到「团队系统化用 AI」。"

# ============ 第 2 页：议程 ============
Write-Host "[build] 议程 (2/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 2
Add-Title -Idx 2 -Text "今天 1 小时讲什么"
Add-Card -Idx 2 -X 1.5 -Y 5 -W 15 -H 3.2 -Title "1. 共识 (5 min)" -Body "我们在做什么 · vibe coding 的甜与痛 · 为什么必须升级"
Add-Card -Idx 2 -X 17 -Y 5 -W 15 -H 3.2 -Title "2. 行业 SOTA (10 min)" -Body "Anthropic 多 agent · Spec Kit · Git Worktree · Cursor v3"
Add-Card -Idx 2 -X 1.5 -Y 8.7 -W 15 -H 3.2 -Title "3. 我们的协作架构 (20 min)" -Body "三层 + 11 角色 + 4 类工具 + Cursor team 配置"
Add-Card -Idx 2 -X 17 -Y 8.7 -W 15 -H 3.2 -Title "4. 实操演示 (15 min)" -Body "派单 · agent 干活 · handoff · UX/UI 试点"
Add-Card -Idx 2 -X 1.5 -Y 12.4 -W 15 -H 3.2 -Title "5. 落地行动 (5 min)" -Body "7 条铁律 · 反模式 · 明天你要做什么"
Add-Card -Idx 2 -X 17 -Y 12.4 -W 15 -H 3.2 -Title '6. Q&A (5 min)' -Body '把你的担忧、疑惑、反对意见摆上桌'
Add-PageNum -Idx 2
Set-Notes -Idx 2 -Text '议程 1 分钟。先报家门：今天分 6 块，时间分配请大家盯着——任何一块超时我会主动提醒。重点是第 3 块「协作架构」和第 5 块「明天你要做什么」，前者帮你看懂全局，后者帮你回去就能动手。中间第 4 块演示，是真实截图，不是 PPT 摆设。最后留 5 分钟 Q&A——讲完不留时间问问题，等于白讲。'

# ============ 第 3 页：项目共识 ============
Write-Host "[build] 项目共识 (3/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 3
Add-Title -Idx 3 -Text "我们在做什么"
Add-SubTitle -Idx 3 -Text "国科信「科技信息展示系统 + 科技专题服务系统」"
Add-BigStat -Idx 3 -X 1.5 -Y 5.5 -W 7 -Number "58" -Caption "功能点（30 展示 + 13 专题 + 15 算法）"
Add-BigStat -Idx 3 -X 9 -Y 5.5 -W 7 -Number "7 / 34" -Caption "大模块 / 总页面数"
Add-BigStat -Idx 3 -X 16.5 -Y 5.5 -W 7 -Number "6" -Caption "代码仓（lumen 3 + demo2 + algo 2）"
Add-BigStat -Idx 3 -X 24 -Y 5.5 -W 7 -Number "4" -Caption "月项目周期 / 26–37 人"
Add-Body -Idx 3 -Y 11 -H 4 -Size 16 -Text "范围真源：agent-delivery/bid-reference/*.md（招标需求 MD，唯一真源）`n范围铁律：58 个功能点 ±10% 浮动（52–64），超出必须甲方+架构师签字`n架构铁律 7 条：算法只在 Python、调用链不越层、NebulaGraph、全栈 OTel、CI/CD、demo2 不污染 lumen、共享聚合核心"
Add-PageNum -Idx 3
Set-Notes -Idx 3 -Text "项目共识 2 分钟。先让大家对齐项目盘子有多大：58 个功能点、4 个月、近 30 人——这不是写个 demo 就完事的小项目。重点强调三件事：(1) 范围有真源——是 bid-reference 那两份 MD，不是各种零散需求文档；(2) 范围有铁律——±10% 不能破，否则成本/工期立刻失控；(3) 架构有铁律——7 条已经写进 architecture-baseline.md，每个 agent 派单话术里都带，违反就是技术腐化的开始。这 3 条不是规章制度，是「让 58 个功能点能在 4 个月内交付完成」的物理约束。"

# ============ 第 4 页：vibe coding 的甜 ============
Write-Host "[build] vibe coding 甜 (4/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 4
Add-Title -Idx 4 -Text "Vibe Coding 的「甜」：为什么我们都爱它"
Add-Card -Idx 4 -X 1.5 -Y 5 -W 10 -H 8 -Title "马上能跑" -Body "「写个查城市天气的接口」`n10 秒后：AI 给出一段 Python，复制粘贴，能跑。`n`n→ 反馈即时，多巴胺暴击" -TitleColor $Primary
Add-Card -Idx 4 -X 12 -Y 5 -W 10 -H 8 -Title "心情爽" -Body "不用查 Stack Overflow`n不用看官方文档`n不用记 API 签名`n`n→ 大脑减负，状态心流" -TitleColor $Secondary
Add-Card -Idx 4 -X 22.5 -Y 5 -W 10 -H 8 -Title "产能感" -Body "一个人一天写完一周的活`n个体上感受到 10x 提升`n`n→ 自信爆棚，跟同事炫耀" -TitleColor $Accent
Add-Body -Idx 4 -Y 14 -H 1.5 -Size 18 -Color $Muted -Align "center" -Text "→ 这些感觉都对，但只是「个人甜点」。下一页讲为什么这是个「团队陷阱」"
Add-PageNum -Idx 4
Set-Notes -Idx 4 -Text "vibe coding 甜 2 分钟。先共情、不要上来就批判。承认 vibe coding 真的爽——它满足了三个核心欲望：即时反馈、大脑减负、产能感。这是 AI 工具最大的成功，让每个人都觉得自己变强了。问大家一句：「过去 1 个月，你有没有一刻觉得『有 AI 我能干 10 个人的活』？」——99% 都会点头。这里不要否定，要承认。然后用最后那句话作为转场钩子：「但这只是『个人甜点』，下面讲为什么对团队来说，这是个陷阱。」"

# ============ 第 5 页：vibe coding 的痛 ============
Write-Host "[build] vibe coding 痛 (5/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 5 -Color $Warn
Add-Title -Idx 5 -Text "Vibe Coding 的「痛」：3 个团队陷阱"
Add-Card -Idx 5 -X 1.5 -Y 5 -W 10 -H 8.5 -Title "1. 不可复用" -Body "你 prompt 出来的代码，下次只有你能 prompt 出来`n张三的 AI 风格 ≠ 李四的 AI 风格`n`n团队代码风格漂移`n组件库形同虚设`n3 个月后没人能维护" -Fill "FCEEEE" -TitleColor $Warn
Add-Card -Idx 5 -X 12 -Y 5 -W 10 -H 8.5 -Title "2. 不可审计" -Body "「这段代码谁写的？」「AI 写的。」`n「为什么这么写？」「AI 说要这么写。」`n`n出 bug 没人扛`n架构腐化没人发现`n甲方质疑无法回应" -Fill "FCEEEE" -TitleColor $Warn
Add-Card -Idx 5 -X 22.5 -Y 5 -W 10 -H 8.5 -Title "3. 不可扩展" -Body "1 人 + AI = 10x 产能`n10 人 + 10 个 AI ≠ 100x`n`n大家提示词五花八门`n产物彼此冲突`n评审瓶颈`n成本失控" -Fill "FCEEEE" -TitleColor $Warn
Add-Body -Idx 5 -Y 14 -H 1.5 -Size 18 -Color $Warn -Align "center" -Text "→ 不是 AI 的错，是「个人用 AI」的范式不适合团队"
Add-PageNum -Idx 5
Set-Notes -Idx 5 -Text "vibe coding 痛 3 分钟。从甜到痛，要给真实例子：(1) 不可复用——上周 A 同学 prompt 出一个组件，B 同学想复用，重新 prompt 一遍，结果 API 不一致；(2) 不可审计——甲方问「这段代码为什么是这样的逻辑」，答不上来是非常尴尬的事；(3) 不可扩展——10 人各自跑 AI，产能不是 100x，是混乱 10x。三句话要扎实：每个团队里都有这种事，举手让大家承认。最后一句很关键：「这不是 AI 的错，是『个人用 AI』的范式不适合团队」——把矛头从 AI 转到「我们怎么用 AI」上，铺垫下一页升级。"

# ============ 第 6 页：所以我们升级 ============
Write-Host "[build] 一句话心智 (6/31)" -ForegroundColor Yellow
New-Slide -Background $BgDark
& $OC add $PPT "/slide[6]" --type shape `
    --prop geometry=rect --prop x=0cm --prop y=0cm --prop w=0.4cm --prop h=19.05cm `
    --prop fill=$Accent --prop line.width=0 | Out-Null
# 引子
& $OC add $PPT "/slide[6]" --type shape `
    --prop geometry=rect --prop x=2cm --prop y=2.5cm --prop w=29cm --prop h=1.5cm `
    --prop text="所以我们要升级——一句话心智" `
    --prop font=$Font --prop size=28pt --prop color=$Accent `
    --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
# 主句
& $OC add $PPT "/slide[6]" --type shape `
    --prop geometry=rect --prop x=2cm --prop y=6cm --prop w=29cm --prop h=8cm `
    --prop text="人做：决策 · 评审 · 创意 · 客户沟通`n`nAI 做：执行 · 起草 · 标准化 · 并行重复劳动`n`n人与人、人与 AI、AI 与 AI`n都靠「DoD + Handoff + Evidence」标准化接口" `
    --prop font=$Font --prop size=24pt --prop bold=true `
    --prop color="FFFFFF" --prop fill=transparent --prop line.width=0 --prop align=left --prop lineSpacing=1.5x | Out-Null
# 衡量
& $OC add $PPT "/slide[6]" --type shape `
    --prop geometry=roundRect --prop x=2cm --prop y=15.5cm --prop w=29cm --prop h=2cm `
    --prop fill="143A3D" --prop line.color=$Accent --prop line.width=1 | Out-Null
& $OC add $PPT "/slide[6]" --type shape `
    --prop geometry=rect --prop x=2.5cm --prop y=15.8cm --prop w=28cm --prop h=1.4cm `
    --prop text="衡量标准：(团队人数 + AI agent) 能否等价于原来 3 倍人力的产能" `
    --prop font=$Font --prop size=18pt `
    --prop color=$Accent --prop fill=transparent --prop line.width=0 --prop align=center | Out-Null
Set-Notes -Idx 6 -Text "升级心智 2 分钟。这是全场最重要的一页，建议慢讲、留 5 秒停顿。这一句话已经写进 team-collaboration-playbook.md §0，也写进了 .cursor/rules/00-team-constitution.mdc，是团队公约。三件事：(1) 人做高价值的事，AI 做重复的事——分工要清楚；(2) 不混淆——评审永远是人，量产永远是 AI；(3) 接口标准化——DoD（完工定义）、Handoff（交付证据）、Evidence（可追溯）这三件套保证人机协作不漂移。最后一句「衡量标准」是钩子——团队人数 + AI 如果不等于 3x 原产能，就是用 AI 用错了。"

# ============ 第 7 页：SOTA 标杆 ============
Write-Host "[build] SOTA 速览 (7/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 7
Add-Title -Idx 7 -Text "2026 业界 SOTA：别人怎么用 AI 做团队"
Add-SubTitle -Idx 7 -Text "我们不是闭门造车——这套打法已被 Anthropic / GitHub / Cursor / Augment 等公开验证"
Add-Card -Idx 7 -X 1.5 -Y 5.5 -W 15 -H 4 -Title "Anthropic: Orchestrator-Worker" -Body "Lead Agent 编排不干活 · Subagent 干净上下文并行`n实测复杂任务提速 90%，但贵 15x → 必须控成本"
Add-Card -Idx 7 -X 17 -Y 5.5 -W 15 -H 4 -Title "GitHub Spec Kit (112k star)" -Body "规范驱动开发（SDD）：constitution → specify → clarify`n→ plan → tasks → implement，让规范成为可执行资产"
Add-Card -Idx 7 -X 1.5 -Y 10 -W 15 -H 4 -Title "Augment / Zylos: Git Worktree" -Body "每个 agent 自己的工作树，文件级隔离`nCursor 2.0 原生支持，最多 8 路并行"
Add-Card -Idx 7 -X 17 -Y 10 -W 15 -H 4 -Title "Speckle / Gastown: Mayor 模式" -Body "Mayor 协调者从不写代码 + Polecat 工人用完即弃`n+ Refinery 合并队列 + Convoy 按文件分组防冲突"
Add-Body -Idx 7 -Y 14.5 -H 1 -Size 14 -Color $Muted -Align "center" -Text "完整对标见 agent-delivery/orchestration-maturity-and-roadmap.md"
Add-PageNum -Idx 7
Set-Notes -Idx 7 -Text "SOTA 标杆 3 分钟。重点传达「我们不是拍脑袋」。这 4 个标杆都是 2025-2026 的公开实践：Anthropic 的官方博客有，GitHub Spec Kit 有 11 万 star，Augment 和 Cursor 都有产品支持。底下那行小字告诉大家：完整对标分析在 orchestration-maturity-and-roadmap.md，里面我们的成熟度自评 + 升级路线图都写了。这里不展开每个细节，重点是「我们采用了行业最佳实践」——后面 5 页会逐个展开。"

# ============ 第 8 页：Orchestrator-Worker ============
Write-Host "[build] Orchestrator-Worker (8/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 8
Add-Title -Idx 8 -Text "范式 1: Orchestrator-Worker（编排者-工人）"
Add-SubTitle -Idx 8 -Text "Anthropic 把它叫『指挥+演奏家』，我们项目里就是 coordinator + 各专项 agent"
Add-Card -Idx 8 -X 1.5 -Y 5.5 -W 14 -H 4 -Title "Lead Agent（指挥）" -Body "分析任务 · 规划 · 写 Memory · 派子任务 · 综合结果`n**从不亲自写代码**" -TitleColor $Primary
Add-Card -Idx 8 -X 16.5 -Y 5.5 -W 14 -H 4 -Title "Subagents（工人）" -Body "独立 fresh context · 明确目标 / 输出格式 / 工具 / 边界`n**Anthropic 四要素，缺一则漂移**" -TitleColor $Secondary
Add-BigStat -Idx 8 -X 2 -Y 10.5 -W 9 -Number "90%" -Caption "复杂任务提速（vs 单 agent）"
Add-BigStat -Idx 8 -X 12 -Y 10.5 -W 9 -Number "15x" -Caption "Token 消耗（vs 单 agent）"
Add-BigStat -Idx 8 -X 22 -Y 10.5 -W 9 -Number "≤ 4" -Caption "本地并发（监管极限）" -NumberColor $Warn
Add-Body -Idx 8 -Y 14.5 -H 1 -Size 14 -Color $Muted -Align "center" -Text "本项目实现：coordinator-agent + architect / ux / ui / frontend / api / algorithm / data / devops / qa / doc"
Add-PageNum -Idx 8
Set-Notes -Idx 8 -Text "Orchestrator-Worker 2 分钟。强调三个数字：(1) 90% 提速——这是 Anthropic 实测数据；(2) 15x token 消耗——所以必须管成本，否则烧光预算还没干完事；(3) ≤4 本地并发——这是人脑监管极限，超过 4 个 agent 一起跑你管不过来，必然漂移。重点澄清：「指挥」是 coordinator-agent，从不写代码，只派单和验收。「工人」就是 architect / ux / ui / frontend / api / algorithm / data / devops / qa / doc 这 10 个专项 agent，每个 agent 拿到独立的、干净的上下文。这个模型我们已经在跑——下面会演示。"

# ============ 第 9 页：SDD ============
Write-Host "[build] SDD (9/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 9
Add-Title -Idx 9 -Text "范式 2: Spec-Driven Development（规范驱动）"
Add-SubTitle -Idx 9 -Text "GitHub Spec Kit 的核心思想：让规范成为可执行的资产，而不是一次性文档"
# 流程链（6 个圆角矩形）
$steps = @("Constitution", "Specify", "Clarify", "Plan", "Tasks", "Implement")
$mappings = @("项目工程化交付模式", "bid-reference MD", "scope-baseline", "architecture-baseline", "task-registry.yaml", "各 agent 派单")
$x0 = 1.5
$w = 5.0
$gap = 0.3
for ($i = 0; $i -lt 6; $i++) {
    $x = $x0 + $i * ($w + $gap)
    $step = $steps[$i]
    $mapping = $mappings[$i]
    & $OC add $PPT "/slide[9]" --type shape `
        --prop geometry=roundRect --prop x=${x}cm --prop y=6cm --prop w=${w}cm --prop h=2.5cm `
        --prop text=$step --prop font=$Font --prop size=18pt --prop bold=true `
        --prop fill=$Primary --prop color="FFFFFF" --prop line.width=0 --prop align=center | Out-Null
    & $OC add $PPT "/slide[9]" --type shape `
        --prop geometry=rect --prop x=${x}cm --prop y=8.8cm --prop w=${w}cm --prop h=1.5cm `
        --prop text=$mapping --prop font=$Font --prop size=12pt `
        --prop color=$Muted --prop fill=transparent --prop line.width=0 --prop align=center | Out-Null
}
Add-Body -Idx 9 -Y 11.5 -H 3.5 -Size 16 -Text "→ 每阶段产出 Markdown 工件，下一阶段消费上一阶段的产物`n→ 不是「先写文档再写代码」（那是瀑布），而是「文档可执行 + 自动派生 task」`n→ 本项目已落地：从 bid-reference 到 task-registry 的全链路可机器读"
Add-PageNum -Idx 9
Set-Notes -Idx 9 -Text "SDD 2 分钟。讲清楚和瀑布的区别——这不是「先写文档再写代码」的传统瀑布，是「文档本身可执行」。例子：scope-baseline.yaml 是 yaml 不是 word，Coordinator 能直接读出 58 个功能点；task-registry.yaml 是 yaml 不是 excel，Coordinator 能直接知道哪个 task 待派单。6 个阶段对应到我们项目的文档，全部已就绪。重点：不要让团队觉得「又要写文档」——这些文档每天都在用，不是摆设。"

# ============ 第 10 页：Worktree ============
Write-Host "[build] Worktree (10/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 10
Add-Title -Idx 10 -Text "范式 3: Git Worktree（并行隔离）"
Add-SubTitle -Idx 10 -Text "每个 agent 有自己的工作树，共享同一个 .git 对象库，文件级隔离自动识别冲突"
Add-Card -Idx 10 -X 1.5 -Y 5.5 -W 14 -H 4 -Title "传统：单 worktree" -Body "agent A 改 file.js，agent B 也改 file.js`n→ 串行 / 互相覆盖 / 切分支等待`n→ 多 agent 跑不起来" -Fill "FCEEEE" -TitleColor $Warn
Add-Card -Idx 10 -X 16.5 -Y 5.5 -W 14 -H 4 -Title "Worktree：多 worktree" -Body "agent A 在 wt-A，agent B 在 wt-B`n→ 文件级隔离，谁也不动谁`n→ 合并由 git 标准工具自动处理" -Fill "EAF6F0" -TitleColor $Accent
Add-Body -Idx 10 -Y 10.5 -H 5 -Size 16 -Text "→ Cursor 2.0 原生支持，最多 8 路并行`n→ 本项目 Phase 2 启用（参考 编排手册 §15）`n→ 配合 Convoy 分组：触碰同一文件集的任务给同一 agent 串行`n→ 配合 Background Agents（云端）：长任务上云，节省本地资源"
Add-PageNum -Idx 10
Set-Notes -Idx 10 -Text "Worktree 1.5 分钟。这是当前我们项目还没启用的能力，写在 Phase 2 路线图里。简单讲：以前一个仓只能切一个分支，多 agent 一起跑必然冲突；worktree 让每个 agent 有自己的工作树，文件隔离。Cursor 2.0 直接支持，最多 8 路并行。配合两个东西：(1) Convoy 分组——同一文件集的任务给同一 agent 串行；(2) Background Agents——长任务上云。这些都在 orchestration-maturity-and-roadmap.md 里。Phase 2 启用，大家先有概念。"

# ============ 第 11 页：Cursor v3 ============
Write-Host "[build] Cursor v3 (11/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 11
Add-Title -Idx 11 -Text "范式 4: Cursor v3 的团队级能力"
Add-SubTitle -Idx 11 -Text "我们用的 Cursor 不只是「智能编辑器」，是「团队 AI 操作系统」"
Add-Card -Idx 11 -X 1.5 -Y 5.5 -W 9.5 -H 4 -Title "8 路并行" -Body "本地最多 8 个 agent 同时跑`n配 worktree 隔离，文件不冲突"
Add-Card -Idx 11 -X 11.5 -Y 5.5 -W 9.5 -H 4 -Title "Background Agents" -Body "长任务上云`n本地 IDE 不占资源"
Add-Card -Idx 11 -X 21.5 -Y 5.5 -W 9.5 -H 4 -Title "BugBot" -Body "PR 自动审查`n挂上 architect-agent 双层评审"
Add-Card -Idx 11 -X 1.5 -Y 10 -W 9.5 -H 4 -Title "共享 Rules" -Body ".cursor/rules/ 团队 git 共享`n12 份 mdc 已就绪"
Add-Card -Idx 11 -X 11.5 -Y 10 -W 9.5 -H 4 -Title "MCP 池" -Body "GitLab / 数据库 / K8s / Slack`n让 agent 自助查状态"
Add-Card -Idx 11 -X 21.5 -Y 10 -W 9.5 -H 4 -Title "Teams Analytics" -Body "每团队 AI 使用率 / 成本`n月度找推进者沉淀 SOP"
Add-PageNum -Idx 11
Set-Notes -Idx 11 -Text "Cursor v3 1.5 分钟。强调 Cursor 不是「智能 VS Code」——它是团队级的 AI 操作系统。6 个能力里，最重要的是「共享 Rules」（我们已经做完了，12 份 mdc 全员共享）和 BugBot（PR 自动审，配合人评审，质量门）。其他 4 个 Phase 2 启用。这里不展开技术细节，让大家有「我们有强工具，关键是怎么组合用」的认知。"

# ============ 第 12 页：三层架构 ============
Write-Host "[build] 三层架构 (12/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 12
Add-Title -Idx 12 -Text "我们的协作架构：三层"
Add-SubTitle -Idx 12 -Text "战略 → 编排 → 执行；每层职责清晰，向下不向上传递"
# 战略层
& $OC add $PPT "/slide[12]" --type shape `
    --prop geometry=roundRect --prop x=1.5cm --prop y=5.5cm --prop w=30cm --prop h=2.5cm `
    --prop fill=$Primary --prop line.width=0 | Out-Null
& $OC add $PPT "/slide[12]" --type shape `
    --prop geometry=rect --prop x=2cm --prop y=5.8cm --prop w=29cm --prop h=2cm `
    --prop text="战略层：架构委员会（架构师 + 各 lead + PM）`n→ 决策 · 评审 · 范围守门" `
    --prop font=$Font --prop size=18pt --prop bold=true `
    --prop color="FFFFFF" --prop fill=transparent --prop line.width=0 --prop align=left --prop lineSpacing=1.3x | Out-Null
# 编排层
& $OC add $PPT "/slide[12]" --type shape `
    --prop geometry=roundRect --prop x=1.5cm --prop y=8.5cm --prop w=30cm --prop h=2.5cm `
    --prop fill=$Secondary --prop line.width=0 | Out-Null
& $OC add $PPT "/slide[12]" --type shape `
    --prop geometry=rect --prop x=2cm --prop y=8.8cm --prop w=29cm --prop h=2cm `
    --prop text="编排层：coordinator-agent + PM + architect-agent`n→ 派单 · 验收 · 跨团队接口" `
    --prop font=$Font --prop size=18pt --prop bold=true `
    --prop color="FFFFFF" --prop fill=transparent --prop line.width=0 --prop align=left --prop lineSpacing=1.3x | Out-Null
# 执行层
& $OC add $PPT "/slide[12]" --type shape `
    --prop geometry=roundRect --prop x=1.5cm --prop y=11.5cm --prop w=30cm --prop h=4cm `
    --prop fill=$Accent --prop line.width=0 | Out-Null
& $OC add $PPT "/slide[12]" --type shape `
    --prop geometry=rect --prop x=2cm --prop y=11.8cm --prop w=29cm --prop h=3.5cm `
    --prop text="执行层：各团队 = 人 + AI agent 双轨`n  ├─ 1 名 lead 定标 + 评审`n  ├─ N 名工程师做评审 + 复杂模块`n  └─ 每人带 ≤4 个 agent 并行（编排手册 §14）" `
    --prop font=$Font --prop size=16pt `
    --prop color="FFFFFF" --prop fill=transparent --prop line.width=0 --prop align=left --prop lineSpacing=1.4x | Out-Null
Add-Body -Idx 12 -Y 16 -H 1.2 -Size 14 -Color $Muted -Align "center" -Text "关键点：每个团队同构 — lead 定接口/契约/标准 · 工程师评审 + 攻坚 · agent 出量"
Add-PageNum -Idx 12
Set-Notes -Idx 12 -Text "三层架构 2 分钟。这一页是全局图，让大家「找到自己」。三层：(1) 战略——架构师 + lead + PM，决定方向，不写代码；(2) 编排——coordinator + PM + architect，派单和守门，也不写代码；(3) 执行——各团队人 + agent 双轨，真正出活。重点：每个团队都同构——lead 定接口契约，工程师评审 + 攻坚，agent 出量。下一页讲 11 个角色的具体职责。"

# ============ 第 13 页：11 角色矩阵 ============
Write-Host "[build] 11 角色 (13/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 13
Add-Title -Idx 13 -Text "11 个角色矩阵（人 + AI 同构）"
Add-SubTitle -Idx 13 -Text "每个团队都有自己的 .cursor/rules/{role}.mdc，AI 第一天就懂规矩"
$roles = @(
    @("架构师", "2-3", "Epic 评审 / 里程碑合规"),
    @("PM/协调", "1-2", "甲方 / 范围 / coordinator 监管"),
    @("UI/UE", "3", "甲方沟通 / 视觉 / Figma → tokens"),
    @("前端工程", "3-5", "lumen 复刻 + observability"),
    @("后端 Java", "4-6", "OpenAPI 契约 + 业务实现"),
    @("算法 Python", "3-5", "模型选型 + ETL + 评估"),
    @("数据工程", "2-3", "ADS 标准表 + 数据工厂"),
    @("DevOps", "2-3", "CI / Helm / OTel / K8s"),
    @("QA", "2-3", "测试策略 + 验收 + 三联查"),
    @("集成", "1-2", "网关 / 三方对接 / 契约测试"),
    @("文档", "1-2", "编写+验收 / officecli MCP")
)
$cellW = 5.4; $cellH = 1.7
for ($i = 0; $i -lt $roles.Count; $i++) {
    $col = $i % 6
    $row = [Math]::Floor($i / 6)
    $x = 1.5 + $col * ($cellW + 0.1)
    $y = 5.5 + $row * ($cellH + 0.3)
    & $OC add $PPT "/slide[13]" --type shape `
        --prop geometry=roundRect --prop x=${x}cm --prop y=${y}cm --prop w=${cellW}cm --prop h=${cellH}cm `
        --prop fill=$CardLight --prop line.color=$Primary --prop line.width=1 | Out-Null
    & $OC add $PPT "/slide[13]" --type shape `
        --prop geometry=rect --prop x=$($x + 0.2)cm --prop y=$($y + 0.1)cm --prop w=$($cellW - 0.4)cm --prop h=0.7cm `
        --prop text="$($roles[$i][0])（$($roles[$i][1])人）" `
        --prop font=$Font --prop size=13pt --prop bold=true --prop color=$Primary `
        --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
    $roleDesc = $roles[$i][2]
    & $OC add $PPT "/slide[13]" --type shape `
        --prop geometry=rect --prop x=$($x + 0.2)cm --prop y=$($y + 0.85)cm --prop w=$($cellW - 0.4)cm --prop h=0.8cm `
        --prop text=$roleDesc `
        --prop font=$Font --prop size=11pt --prop color=$Text `
        --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
}
Add-Body -Idx 13 -Y 11.5 -H 4 -Size 16 -Text "总编制约 26–37 人，搭配 30–50 个 agent 并行会话池`n每个团队的工作范式都同构：lead 定标 + 工程师评审 + agent 出量`n详见 agent-delivery/team-collaboration-playbook.md §2 完整矩阵"
Add-PageNum -Idx 13
Set-Notes -Idx 13 -Text "11 角色矩阵 2.5 分钟。让大家找到自己——指着 PPT 问「在座的，举手告诉我你属于哪个团队」。强调 11 个角色都有自己的 .cursor/rules/{role}.mdc——AI 第一天就懂你团队的规矩，不用你每次重新教。重点是「同构」——不管哪个团队，模式都一样：lead 定标 + 工程师评审 + agent 量产。下一页讲人和 AI 怎么分工，绝对不混淆。"

# ============ 第 14 页：人 vs AI 分工 ============
Write-Host "[build] 人 vs AI (14/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 14
Add-Title -Idx 14 -Text "人 vs AI：绝对不能混淆的边界"
Add-Card -Idx 14 -X 1.5 -Y 5.5 -W 15 -H 9 -Title "✅ 人做（不可外包）" -Body "· 架构选型 / 技术选型`n· 与甲方承诺范围 / 工期 / 验收`n· 设计创意 / 品牌一致性`n· 评审决策（架构 / PR / 验收）`n· 跨团队仲裁 / 优先级`n· 商务沟通 / 招聘解雇`n· 出问题时承担责任" -TitleColor $Primary
Add-Card -Idx 14 -X 16.5 -Y 5.5 -W 15 -H 9 -Title "✅ AI 做（人来评审）" -Body "· 模板化代码 / 重复 CRUD`n· 文档起草 / 周报汇编`n· 数据 Mock / 测试 case`n· 跨仓一致性扫描`n· 长上下文规划起草`n· 失败重试 / 探索可行解`n· 不知疲倦地标准化输出" -TitleColor $Accent
Add-Body -Idx 14 -Y 15 -H 1.2 -Size 18 -Color $Warn -Align "center" -Text "→ 红线：AI 输出 → 必经人评审 → 才能外发；决策永远是人拍板"
Add-PageNum -Idx 14
Set-Notes -Idx 14 -Text "人 vs AI 分工 2 分钟。这一页是「不能犯的错」清单。强调三点：(1) 决策永远是人——架构选型、技术选型、与甲方承诺，AI 可以建议、可以列 trade-off，但拍板永远是人；(2) AI 不接触客户——所有甲方沟通经 PM/UE/架构师，AI 产物必经人评审才能展示；(3) AI 输出对外发布前必须有人签字。这三条已经写进 team-collaboration-playbook 第 6 节铁律。后面 FAQ 里有个问题「AI 跟我说『做完了』，但 CI 没绿怎么办」——答案就是 DoD 不满足等于没做完，不要绕过 CI，这就是人的判断不可外包。"

# ============ 第 15 页：需求链 ============
Write-Host "[build] 需求链 (15/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 15
Add-Title -Idx 15 -Text "一条完整需求链：从甲方到上线"
Add-SubTitle -Idx 15 -Text "9 个角色协作，每个交付都有 handoff，全程可追溯"
# 用横向 box 链表示流程
$flow = @(
    @("甲方需求", $Muted),
    @("PM + UE 接收", $Primary),
    @("架构师定基线", $Primary),
    @("ux 起 IA/wireframe", $Secondary),
    @("ui 出 demo2 沙箱页", $Secondary),
    @("UI/UE + 甲方评审", $Primary),
    @("frontend 复刻 lumen", $Accent),
    @("api + algorithm + data 并行", $Accent),
    @("devops CI/K8s dev", $Accent),
    @("qa 验收 + doc 汇编", $Primary),
    @("architect 合规", $Primary),
    @("里程碑签收", $Warn)
)
$boxW = 4.8; $boxH = 1.4
for ($i = 0; $i -lt $flow.Count; $i++) {
    $col = $i % 4
    $row = [Math]::Floor($i / 4)
    $x = 1.5 + $col * ($boxW + 0.5)
    $y = 5.5 + $row * ($boxH + 0.8)
    $flowText = "$($i+1). $($flow[$i][0])"
    $flowColor = $flow[$i][1]
    & $OC add $PPT "/slide[15]" --type shape `
        --prop geometry=roundRect --prop x=${x}cm --prop y=${y}cm --prop w=${boxW}cm --prop h=${boxH}cm `
        --prop text=$flowText `
        --prop fill=$flowColor --prop color="FFFFFF" `
        --prop font=$Font --prop size=14pt --prop bold=true `
        --prop line.width=0 --prop align=center | Out-Null
}
Add-Body -Idx 15 -Y 12.5 -H 4 -Size 15 -Text "关键接口：`n  · PM → 架构师：需求 + 验收 → 架构基线 + Epic 拆分`n  · UE → UI → 前端：IA/wireframe → demo2 沙箱页 → lumen 工程化`n  · qa → doc → PM：测试结果 → 验收 docx → PM 终审 → 对外"
Add-PageNum -Idx 15
Set-Notes -Idx 15 -Text "需求链 2.5 分钟。这是「一个功能点从甲方到上线」的完整旅程，12 步。强调：(1) 不是线性瀑布——里面 ux 完了 ui、api、algorithm、data 是并行的；(2) 每步都有 handoff——证据可追溯；(3) 最后必经 qa + architect 双门——一个看业务、一个看架构。让大家想想自己每天接的活在哪一步——大概率不是「孤立」的，前后都有衔接。"

# ============ 第 16 页：工具1 rules ============
Write-Host "[build] rules (16/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 16
Add-Title -Idx 16 -Text "工具 1：.cursor/rules/ — 团队 AI 公约"
Add-SubTitle -Idx 16 -Text "12 份 mdc 文件，git 共享；任何人开 agent 会话，AI 第一天就懂规矩"
Add-Card -Idx 16 -X 1.5 -Y 5.5 -W 14 -H 4.5 -Title "00-team-constitution.mdc" -Body "alwaysApply: true（所有会话自动加载）`n7 条架构铁律 + 7 条人机协作铁律`n必读文件清单 + 双根路径" -TitleColor $Primary
Add-Card -Idx 16 -X 16.5 -Y 5.5 -W 14 -H 4.5 -Title "11 份角色 mdc" -Body "architect / coordinator / pm / ux / ui /`nfrontend / api / algorithm / data / devops /`nqa / doc — 每份含身份 + 必读 + 铁律 + handoff 模板" -TitleColor $Secondary
Add-Body -Idx 16 -Y 10.5 -H 5 -Size 16 -Text "→ 触发方式：globs 匹配文件路径（如 .java 文件自动命中 api.mdc）`n→ 优势 1：AI 不再「五花八门」，全团队产物风格一致`n→ 优势 2：新人入职第一天，AI 就懂团队规矩`n→ 优势 3：减少每次会话 30% 输入 token（不用重复教）"
Add-PageNum -Idx 16
Set-Notes -Idx 16 -Text "rules 工具 2 分钟。这是我们做的第 1 个重磅工具——12 份 .cursor/rules/ 已经在 git 里了。00 公约是全局生效的（alwaysApply: true），其他 11 份按文件类型自动触发。例子：你打开一个 .java 文件，api.mdc 自动加载，AI 就知道「Java 不写算法、只调 Python、必加 OTel」。三个优势里最重要的是第二个：新人来了第一天，AI 就懂规矩——这是「规模化」的基础。"

# ============ 第 17 页：工具2 编排 + task-registry ============
Write-Host "[build] task-registry (17/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 17
Add-Title -Idx 17 -Text "工具 2：编排手册 + task-registry"
Add-SubTitle -Idx 17 -Text "agent 的「派工单」和「任务队列」"
Add-Card -Idx 17 -X 1.5 -Y 5.5 -W 14 -H 4.5 -Title "智能体编排与派单手册.md" -Body "12 个角色的派单话术模板`n开会话后复制 /goal {role} 即可下发任务`n含人机协作公约 + 并发护栏 + Worktree 规范" -TitleColor $Primary
Add-Card -Idx 17 -X 16.5 -Y 5.5 -W 14 -H 4.5 -Title "task-registry.yaml" -Body "全部 task 的机器可读队列`n字段：id / agent / depends_on / status / DoD / handoff`n新增：estimated_tokens / actual_cost / cost_warn" -TitleColor $Secondary
Add-Body -Idx 17 -Y 10.5 -H 5 -Size 16 -Text "→ coordinator-agent 读 task-registry，找 pending 且依赖已 done 的 leaf`n→ 按编排手册话术下发 /goal，新会话执行`n→ agent 完工写 handoff，coordinator 验收 + 更状态`n→ 整个流程机器可读、可审计、可重放"
Add-PageNum -Idx 17
Set-Notes -Idx 17 -Text "编排 + task-registry 1.5 分钟。这是日常运行的「水电气」。task-registry.yaml 是任务的真源——所有 task 都在里面，按依赖顺序排好。coordinator 每轮读一遍，找出可以派的 leaf 任务。编排手册里有每个角色的派单话术模板——你不用现想，复制粘贴就行。重点：新增了 cost 跟踪字段，每个 task 完工时必须回填实际 token 和成本——这是预算管控的基础。"

# ============ 第 18 页：工具3 铁律 ============
Write-Host "[build] 铁律 (18/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 18
Add-Title -Idx 18 -Text "工具 3：架构铁律 7 条"
Add-SubTitle -Idx 18 -Text "已写进 00-team-constitution.mdc，所有 agent 自动遵守"
$rules = @(
    "1. 算法只在 Python，Java 禁 NLP/模型推理",
    "2. 调用链：前端 → Java REST → Python /internal/*，不可越层",
    "3. 图谱：NebulaGraph（192.168.88.43:9669），禁止 Neo4j",
    "4. 可观测性：Java Agent + Python instrument + 前端 observability.ts",
    "5. CI/CD：push → Pipeline 绿 → K8s dev rollout，对 dev 测试",
    "6. demo2 只读：禁止 merge 进 lumen；UI/UE 沙箱产物只在 demo2",
    "7. 共享聚合核心（方案 A）：前端只调 Java；Java 不写算法、不直连 nGQL、只读 ADS"
)
for ($i = 0; $i -lt $rules.Count; $i++) {
    $y = 5.5 + $i * 1.5
    $rule = $rules[$i]
    & $OC add $PPT "/slide[18]" --type shape `
        --prop geometry=roundRect --prop x=1.5cm --prop y=${y}cm --prop w=30cm --prop h=1.3cm `
        --prop text=$rule --prop font=$Font --prop size=16pt `
        --prop fill=$CardLight --prop color=$Text --prop line.color=$Primary --prop line.width=1 `
        --prop align=left | Out-Null
}
Add-Footer -Idx 18 -Text "→ 违反任一铁律 = architect-agent 拒绝合并 + 暂停 + 人评审"
Add-PageNum -Idx 18
Set-Notes -Idx 18 -Text "7 条铁律 2 分钟。这是「不能碰的电网」，不是建议、是物理约束。逐条快速过，重点解释：(1) 算法只在 Python——这是技术栈隔离，Java 不允许写 NLP；(7) 方案 A——展示和专题两个前端共享 gkxlumen-topic 后端，避免重复造轮子。底下那行小字是关键：违反任一铁律，architect-agent 会拒绝合并、暂停、要求人评审。我们之前已经踩过坑——某个早期版本 Java 写了简单的字符串规则匹配，看起来「不算算法」，但破了铁律 1，所以重构。下一页讲完工证据。"

# ============ 第 19 页：工具4 handoff + cost ============
Write-Host "[build] handoff + cost (19/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 19
Add-Title -Idx 19 -Text "工具 4：Handoff 证据 + Cost 跟踪"
Add-SubTitle -Idx 19 -Text "每个 task 完工必交 = 证据 md + cost 4 字段"
Add-Card -Idx 19 -X 1.5 -Y 5.5 -W 14 -H 8 -Title "Handoff: agent-handoffs/{task-id}.md" -Body "范围与实现（与 bid-reference 章节对照）`n偏离说明 + as-built 理由`n产物清单（PR / 文档 / 截图）`n验收证据（CI 绿 / dev URL / 三联查链接）`n架构合规自检（7 条 ✅/❌）`n阻塞 / 风险（已列入 task-registry）" -TitleColor $Primary
Add-Card -Idx 19 -X 16.5 -Y 5.5 -W 14 -H 8 -Title "Cost: task-registry 必填 4 字段" -Body "estimated_tokens: 派单前估`nactual_tokens: 完工后实测 in+out`nmodel_used: claude-sonnet-4.5 / opus / haiku`nactual_cost: $X.XX 美元`ncost_warn: green / yellow($>5) / orange($>10) / red($>20)" -TitleColor $Accent
Add-Body -Idx 19 -Y 14 -H 1.5 -Size 16 -Color $Warn -Align "center" -Text "→ 缺一不收：coordinator 验收清单 7 条全过才能把 status 改为 done"
Add-PageNum -Idx 19
Set-Notes -Idx 19 -Text "handoff + cost 2 分钟。左边 handoff 是「证据」——agent 完工时必须写一份 md，把所有证据（PR、CI、dev URL、合规自检）链接进去。右边 cost 是「成本」——必须填 4 个字段。预算告警阈值：$5 黄、$10 橙暂停、$20 红 hard stop + architect 评审。这套机制保证 (1) 出问题能追溯；(2) 成本不失控。详细预算估算在 budget-estimate.md，全项目预估 $1230（混合档），月均 $308。后面 FAQ 有人会问「token 烧光怎么办」——答案：每周 retro 排行榜 + 复盘最贵 5 个任务，prompt 优化省 30-60%。"

# ============ 第 20 页：Cursor team 6 项配置 ============
Write-Host "[build] team 6 配置 (20/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 20
Add-Title -Idx 20 -Text "Cursor Team 6 项配置"
Add-SubTitle -Idx 20 -Text "把 Cursor 当「团队 AI 操作系统」来用，不是「智能编辑器」"
$cfg = @(
    @("共享 .cursor/rules/", "12 份 mdc 全员同步", "已做 ✅"),
    @("Background Agents", "长任务上云，省本地", "Phase 2"),
    @("BugBot for PR", "三层质量门 = BugBot + architect + lead", "Phase 2"),
    @("共享 MCP 池", "GitLab / 数据库 / K8s / Slack", "进行中"),
    @("Worktree + 8 路并行", "本地 ≤4 + 云端 Background", "Phase 2"),
    @("Teams Analytics", "月度找推进者，沉淀 SOP", "需 Team 订阅")
)
for ($i = 0; $i -lt $cfg.Count; $i++) {
    $col = $i % 2
    $row = [Math]::Floor($i / 2)
    $x = 1.5 + $col * 15.3
    $y = 5.3 + $row * 3.2
    $cfgTitle = "$($cfg[$i][0])  [$($cfg[$i][2])]"
    $cfgBody = $cfg[$i][1]
    Add-Card -Idx 20 -X $x -Y $y -W 14.8 -H 2.8 `
        -Title $cfgTitle `
        -Body $cfgBody `
        -TitleSize 16 -BodySize 13
}
Add-PageNum -Idx 20
Set-Notes -Idx 20 -Text "Cursor team 6 配置 1.5 分钟。6 个配置里只有第一个已经做完——共享 rules。其他 4 个属于 Phase 2（4-6 周内启用）。重点是让大家知道：我们的工具栈是有规划的，不是想到哪做到哪。Phase 1（共享 rules）→ Phase 2（Background + BugBot + MCP + Worktree）→ Phase 3（自动 coordinator 循环）。详见 orchestration-maturity-and-roadmap.md。"

# ============ 第 21 页：演示 1 - 派单 ============
Write-Host "[build] 演示派单 (21/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 21
Add-Title -Idx 21 -Text "演示 1：怎么派一个任务"
Add-SubTitle -Idx 21 -Text "实战：UI/UE 团队让 ui-agent 实现 DS-15「重点科技人才画像」"
# 模拟终端框
& $OC add $PPT "/slide[21]" --type shape `
    --prop geometry=roundRect --prop x=1.5cm --prop y=5.5cm --prop w=30cm --prop h=10cm `
    --prop fill="1E1E1E" --prop line.color=$Accent --prop line.width=1 | Out-Null
& $OC add $PPT "/slide[21]" --type shape `
    --prop geometry=rect --prop x=2cm --prop y=5.8cm --prop w=29cm --prop h=0.8cm `
    --prop text="● cursor-agent (新会话) — ui-agent" `
    --prop font=$Font --prop size=12pt --prop color=$Accent `
    --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
& $OC add $PPT "/slide[21]" --type shape `
    --prop geometry=rect --prop x=2cm --prop y=6.8cm --prop w=29cm --prop h=8.5cm `
    --prop text="/goal ui-agent`n`n身份：资深 UI 工程师（React 19 + Ant Design v5）`n任务：实现 DS-15 重点科技人才画像，输出 demo2 沙箱页 6 张`n必读：`n  · agent-delivery/repo-registry.yaml#demo-ui-science`n  · demo2/package.json + App.jsx`n  · demo2/docs/ia/sandbox/talent-2026-06-17/* (ux 产物)`n  · agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md#§DS-15`n约束：`n  · 路由前缀 /sandbox/talent-2026-06-17/*，不进主菜单`n  · 只用 mocks/，不接 lumen 真实 API`n  · design tokens only，禁硬编码颜色`n  · 仅 commit，不 push`nDoD：6 张页面 + handoff" `
    --prop font="Consolas" --prop size=11pt --prop color="D4D4D4" `
    --prop fill=transparent --prop line.width=0 --prop align=left --prop lineSpacing=1.3x | Out-Null
Add-Footer -Idx 21 -Text "→ 完整话术模板：agent-delivery/智能体编排与派单手册.md §9.1d ui-agent"
Add-PageNum -Idx 21
Set-Notes -Idx 21 -Text "演示派单 2 分钟。讲这张时打开 Cursor 真实操作：(1) 新开一个 agent 会话；(2) 复制 /goal ui-agent 的话术；(3) 改成具体任务；(4) 回车。强调：你不用现编派单话术——编排手册第 9 章已经给了 12 个角色的完整模板，复制粘贴改 3 个参数就能用。「必读」「约束」「DoD」三段是关键，少一段 agent 都可能跑偏。"

# ============ 第 22 页：演示 2 - agent 干活 + handoff ============
Write-Host "[build] 演示干活 (22/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 22
Add-Title -Idx 22 -Text "演示 2：agent 干活 + 完工 handoff"
Add-SubTitle -Idx 22 -Text "agent 自动按规约执行；完工写 handoff；coordinator 验收 7 条"
Add-Card -Idx 22 -X 1.5 -Y 5.5 -W 14.5 -H 9.5 -Title "agent 跑的过程" -Body "1. 读 rules：自动加载 ui.mdc + 00-team-constitution.mdc`n2. 读必读：bid-reference + repo-registry + ux 产物`n3. 创建文件：src/sandbox/talent-2026-06-17/`n4. 实现 6 张页面 + mocks + 路由桥接`n5. 自检：design tokens / 沙箱隔离 / mock only`n6. 写 handoff：agent-handoffs/科技人才态势-DS15/UI-DS-15-trial.md`n7. commit（不 push）+ 通知人审" -TitleColor $Primary
Add-Card -Idx 22 -X 16.5 -Y 5.5 -W 14.5 -H 9.5 -Title "coordinator 验收 7 条" -Body "✅ 1 handoff 文件按模板`n✅ 2 代码 PR + CI 绿`n✅ 3 K8s dev URL 可访问`n✅ 4 偏离 bid-reference 处有说明`n✅ 5 架构合规自检 7 条`n✅ 6 后续阻塞已列入 task-registry`n✅ 7 cost 字段回填 (actual_tokens / cost)`n→ 任一缺失 = status: needs-revision" -TitleColor $Accent
Add-PageNum -Idx 22
Set-Notes -Idx 22 -Text "agent 干活 + handoff 2 分钟。左边是 agent 自动跑的过程——你不用手把手教，rules 已经让它知道怎么做。右边是 coordinator 验收的 7 条——这是「自动质量门」。重点：第 7 条 cost 回填是新加的，没填等于没完工。讲到这里可以打开真实的 handoff 文件（agent-handoffs/科技人才态势-DS15/UX-DS-15-trial.md）让大家看看实际长什么样。"

# ============ 第 23 页：演示 3 - UX 试点 ============
Write-Host "[build] 演示 UX 试点 (23/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 23
Add-Title -Idx 23 -Text "演示 3：UX 试点产物（DS-15 重点科技人才画像）"
Add-SubTitle -Idx 23 -Text "ux-agent 在沙箱目录跑出 15 个页面的 IA / 用户旅程 / 低保真"
Add-Card -Idx 23 -X 1.5 -Y 5.5 -W 14.5 -H 4.5 -Title "DS-15-IA.md" -Body "页面树：15 页（人才画像 + 关系网络 + 排行 + 趋势）`n路由：/sandbox/talent-2026-06-17/{profile, network, ranking, ...}`n映射：bid-reference §3.2.4.3 → 全覆盖" -TitleColor $Primary
Add-Card -Idx 23 -X 16.5 -Y 5.5 -W 14.5 -H 4.5 -Title "DS-15-userflow.md" -Body "1 条主路径 + 4 条异常路径`n13 个埋点节点（与 observability.md 对齐）`nMermaid 流程图可视化" -TitleColor $Secondary
Add-Card -Idx 23 -X 1.5 -Y 10.2 -W 14.5 -H 4.5 -Title "DS-15-wireframe.md" -Body "15 张子页面的 ASCII/Markdown 块状布局`n字段清单 + 交互注释`n24 个开放项（待 UI/UE 决策视觉细节）" -TitleColor $Accent
Add-Card -Idx 23 -X 16.5 -Y 10.2 -W 14.5 -H 4.5 -Title "README.md（沙箱元信息）" -Body "试点目的 / 覆盖功能点 / 隔离声明`n关键开放项 / 下一步 ui-agent 接力"  -TitleColor $Muted
Add-Footer -Idx 23 -Text "→ 产物位置：demo2/docs/ia/sandbox/talent-2026-06-17/"
Add-PageNum -Idx 23
Set-Notes -Idx 23 -Text "UX 试点 2 分钟。这是真实跑过的试点——ux-agent 跑了大约 1 小时，产出 4 个文档。重点强调「沙箱隔离」：所有产物都在 docs/ia/sandbox/talent-2026-06-17/ 子目录里，不动现有任何文件。这是 UX 团队和 UI/UE 团队的协作起点——UE 评审 IA/wireframe，认可后再让 ui-agent 接力实现。这种做法的好处：风险可控，失败可一行回退（删目录就行）。"

# ============ 第 24 页：演示 4 - UI demo2 沙箱 ============
Write-Host "[build] 演示 UI 沙箱 (24/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 24
Add-Title -Idx 24 -Text "演示 4：UI 沙箱页（接力实现）"
Add-SubTitle -Idx 24 -Text "ui-agent 翻译 wireframe → demo2 真实 React 代码，沙箱路由隔离"
Add-Card -Idx 24 -X 1.5 -Y 5.5 -W 14.5 -H 4.2 -Title "路由隔离" -Body "/sandbox/talent-2026-06-17/profile`n/sandbox/talent-2026-06-17/network`n/sandbox/talent-2026-06-17/ranking ..." -TitleColor $Primary
Add-Card -Idx 24 -X 16.5 -Y 5.5 -W 14.5 -H 4.2 -Title "文件隔离" -Body "src/sandbox/talent-2026-06-17/*`nsrc/mocks/sandbox/talent-2026-06-17/*`n不改 src/components/、App.jsx 主路由" -TitleColor $Secondary
Add-Card -Idx 24 -X 1.5 -Y 9.9 -W 14.5 -H 4.2 -Title "设计 token 复用" -Body "禁硬编码颜色/字号/间距`n只用 demo2 现有 design-system tokens`n保持品牌一致性" -TitleColor $Accent
Add-Card -Idx 24 -X 16.5 -Y 9.9 -W 14.5 -H 4.2 -Title "Mock 数据驱动" -Body "src/mocks/sandbox/.../talent.json`n不接 lumen 真实 API（铁律 6）`n演示数据规模 + 分布合理" -TitleColor $Muted
Add-Footer -Idx 24 -Text "→ 评审通过后由 frontend-agent 复刻到 lumen，加 observability + 接真实 API"
Add-PageNum -Idx 24
Set-Notes -Idx 24 -Text "UI 沙箱 2 分钟。ui-agent 接 ux-agent 的产物，翻译成真实可跑的 React 代码。四个隔离做得很到位：(1) 路由隔离——/sandbox 前缀，不进主菜单；(2) 文件隔离——sandbox/ 子目录，不动现有文件；(3) 设计 token 复用——保持品牌一致；(4) Mock 数据驱动——不接真实 API。这样做的好处：随时可演示给甲方，演示完不影响生产路径。评审通过后，frontend-agent 才把它复刻到 lumen 正式仓，加 observability 和真实 API。"

# ============ 第 25 页：7 条人机铁律 ============
Write-Host "[build] 7 铁律 (25/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 25 -Color $Warn
Add-Title -Idx 25 -Text "人机协作 7 条铁律（违反必处理）"
$human_rules = @(
    "1. 决策不外包给 AI（架构 / 技术 / 甲方承诺，永远是人拍板）",
    "2. AI 不接触客户（甲方沟通经 PM/UE/架构师，AI 产物必经人评审）",
    "3. 每个 commit 标作者：[agent:role] 或 [human:name]",
    "4. 失败可逆：worktree / sandbox / 新分支跑，不动 main",
    "5. 本地并发 ≤4，超过上 Background Agents",
    "6. DoD 必含 handoff：完工必写 agent-handoffs/{task-id}.md",
    "7. cost 字段必回填：actual_tokens / model / cost / warn"
)
for ($i = 0; $i -lt $human_rules.Count; $i++) {
    $y = 5.5 + $i * 1.3
    $hrule = $human_rules[$i]
    & $OC add $PPT "/slide[25]" --type shape `
        --prop geometry=roundRect --prop x=1.5cm --prop y=${y}cm --prop w=30cm --prop h=1.1cm `
        --prop text=$hrule --prop font=$Font --prop size=15pt `
        --prop fill="FCEEEE" --prop color=$Text --prop line.color=$Warn --prop line.width=1 `
        --prop align=left | Out-Null
}
Add-Footer -Idx 25 -Text "→ 已写进 .cursor/rules/00-team-constitution.mdc + team-collaboration-playbook.md §6"
Add-PageNum -Idx 25
Set-Notes -Idx 25 -Text "7 条人机铁律 2 分钟。这是「不能犯的错」。逐条快速过——重点解释 (3) commit 标作者：每个 commit message 加 [agent:xxx] 或 [human:xxx]，CI 会检查，不标拒绝合并。这条很简单但价值大——3 个月后查问题、出 bug、甲方追责，能立刻知道是谁/什么 agent 写的。(5) 本地 ≤4 是物理约束——人脑监管不了更多并发。(7) cost 回填——下次预算审计有据可查。"

# ============ 第 26 页：反模式 ============
Write-Host "[build] 反模式 (26/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 26 -Color $Warn
Add-Title -Idx 26 -Text "5 大反模式：踩过的坑，别再踩"
Add-Card -Idx 26 -X 1.5 -Y 5.5 -W 15 -H 4 -Title "❌ AI 出活，人只 review" -Body "→ 3 个月后没人能独立思考`n✅ 月度 AI off 1 天 + 定期重写关键模块" -Fill "FCEEEE" -TitleColor $Warn
Add-Card -Idx 26 -X 16.5 -Y 5.5 -W 15 -H 4 -Title "❌ Lead 不亲自跑 agent" -Body "→ 派单不准 / 评审不到位`n✅ Lead 每周必须亲跑 ≥3 个任务" -Fill "FCEEEE" -TitleColor $Warn
Add-Card -Idx 26 -X 1.5 -Y 10 -W 15 -H 4 -Title "❌ AI 用得溜 vs 不溜的人产能差 5x" -Body "→ 团队张力 / 沟通成本高`n✅ 沉淀成功 prompt 为 .cursor/rules，新人必学" -Fill "FCEEEE" -TitleColor $Warn
Add-Card -Idx 26 -X 16.5 -Y 10 -W 15 -H 4 -Title "❌ Figma 与代码两套真源" -Body "→ 设计/代码漂移`n✅ Figma 一次性导出 tokens 后弃用，代码直接维护" -Fill "FCEEEE" -TitleColor $Warn
Add-Body -Idx 26 -Y 14.5 -H 1.2 -Size 14 -Color $Muted -Align "center" -Text "完整 10 大反模式：team-collaboration-playbook.md §7"
Add-PageNum -Idx 26
Set-Notes -Idx 26 -Text "反模式 2 分钟。这 4 个是最容易踩的。重点讲 (1) AI 出活人 review——3 个月后会变成「废柴团队」，谁都不能独立思考。对策：月度 AI off 一天，强制手写。讲 (3) 产能差 5x——这是真实风险，团队张力会很大，解决办法是把成功 prompt 沉淀进 rules，让谁用都一样。"

# ============ 第 27 页：onboarding ============
Write-Host "[build] onboarding (27/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 27
Add-Title -Idx 27 -Text "新人 1 天 Onboarding（每个团队照搬）"
Add-SubTitle -Idx 27 -Text "详见 agent-delivery/team-onboarding.md"
Add-Card -Idx 27 -X 1.5 -Y 5.5 -W 15 -H 4 -Title "上午（4h）" -Body "0.5h 读规约（公约 + 角色 mdc）`n1h 装环境（Cursor + repo + 依赖）`n0.5h 验证 rules 命中`n2h 跟 mentor 跑 1 个完整任务" -TitleColor $Primary
Add-Card -Idx 27 -X 16.5 -Y 5.5 -W 15 -H 4 -Title "下午（4h）" -Body "2h 独立跑 1 个简单任务（沙箱/Mock）`n1.5h 评审 1 个别人的 agent PR`n0.5h 1v1 review + 加入团队节奏" -TitleColor $Accent
Add-Body -Idx 27 -Y 10 -H 5 -Size 16 -Text "入职第 1 天检查表（mentor 用）：`n  □ 新人能独立打开 Cursor + 命中 .cursor/rules/`n  □ 跑通 1 个简单任务并写 handoff`n  □ Review 了 1 个别人的 PR`n  □ 加入团队站会 + 飞书群`n  □ 知道 7 条铁律 + 6 条红线`n  □ 有 mentor 的微信 / 飞书直联`n全部 ✅ → 可独立工作；否则延期 1 天"
Add-PageNum -Idx 27
Set-Notes -Idx 27 -Text "Onboarding 1.5 分钟。新人 1 天上手，详细 SOP 在 team-onboarding.md。上午装环境 + 跟跑；下午自己跑 + 评审别人 PR。重点：第一天就必须「评审别人的 PR」——学会「看 AI 产物」比「会派 agent」更重要。底下检查表是 mentor 用的，6 项全过才能独立。"

# ============ 第 28 页：明天你要做什么 ============
Write-Host "[build] 明天做什么 (28/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 28
Add-Title -Idx 28 -Text "明天起，每个团队具体做什么"
Add-Card -Idx 28 -X 1.5 -Y 5.5 -W 15 -H 4 -Title "全员（必做）" -Body "1. 拉最新 agent-delivery + .cursor/rules`n2. 读你对应角色的 mdc`n3. 跑通本周第一个任务（不论大小）"
Add-Card -Idx 28 -X 16.5 -Y 5.5 -W 15 -H 4 -Title "各团队 Lead（额外）" -Body "1. 给团队选 1 名「AI 推进者」`n2. 本周组织 1 次 30 分钟分享（跑通经验）`n3. 给团队的 mdc 提优化 PR" -TitleColor $Accent
Add-Card -Idx 28 -X 1.5 -Y 10 -W 15 -H 4 -Title "PM（架构层）" -Body "1. 跟架构师 + lead 周对齐（每周一）`n2. 设置周成本回顾（每周五）`n3. 触发首个 Epic 完成后预算重校准" -TitleColor $Primary
Add-Card -Idx 28 -X 16.5 -Y 10 -W 15 -H 4 -Title "架构师团队" -Body "1. 每个新 Epic 开工前评审（不写代码）`n2. 里程碑前合规扫描（7 条铁律）`n3. 维护 architecture-baseline.md" -TitleColor $Primary
Add-Footer -Idx 28 -Text "→ 全员承诺：参加每日 9:30 团队 AI 站会（15 分钟）"
Add-PageNum -Idx 28
Set-Notes -Idx 28 -Text "明天做什么 2 分钟。这一页是「行动呼吁」——讲完 PPT 大家必须有可执行的下一步，否则等于白讲。三档动作：(1) 全员 3 件必做；(2) Lead 额外 3 件；(3) PM 和架构师额外动作。最重要：每日 9:30 团队 AI 站会，15 分钟同步昨天 AI 跑了什么、今天派什么——这是「保持节奏」的基础。"

# ============ 第 29 页：FAQ ============
Write-Host "[build] FAQ (29/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 29
Add-Title -Idx 29 -Text "FAQ：你心里现在的担忧"
Add-Card -Idx 29 -X 1.5 -Y 5.5 -W 15 -H 4 -Title "Q1: AI 会不会取代我？" -Body "→ AI 取代不了评审、决策、创意、客户对接`n→ 它取代的是你「不想做的重复活」`n→ 拥抱它的人产能 5x，抗拒的被淘汰" -TitleColor $Primary
Add-Card -Idx 29 -X 16.5 -Y 5.5 -W 15 -H 4 -Title "Q2: AI 写的代码我看不懂怎么办？" -Body "→ 不要合并！必须看懂为止`n→ 要么让 agent 解释`n→ 要么改写到你能看懂" -TitleColor $Warn
Add-Card -Idx 29 -X 1.5 -Y 10 -W 15 -H 4 -Title "Q3: 我跑出来的不一致怎么办？" -Body "→ 检查三件事：rules 命中？prompt 清晰？必读到位？`n→ 都对还跑偏，升级到 mentor / 架构师" -TitleColor $Primary
Add-Card -Idx 29 -X 16.5 -Y 10 -W 15 -H 4 -Title "Q4: 多个 agent 跑出冲突怎么办？" -Body "→ Convoy 分组：同文件给同 agent 串行`n→ Worktree 隔离（Phase 2）`n→ 出冲突由 git 标准工具识别 + 人裁决" -TitleColor $Primary
Add-PageNum -Idx 29
Set-Notes -Idx 29 -Text "FAQ 2.5 分钟。这是大家心里真实的担忧，主动摆上桌。Q1 必须正面回答——AI 取代的是重复活，不是高价值工作；抗拒的人会被淘汰，是事实。Q2 是质量铁律——AI 写的代码看不懂坚决不合并，3 个月后维护时你会感谢现在的自己。Q3 是 debug 三步法。Q4 是并发管理。这页讲完进 Q&A。"

# ============ 第 30 页：资源索引 ============
Write-Host "[build] 资源索引 (30/31)" -ForegroundColor Yellow
New-Slide
Add-Motif -Idx 30
Add-Title -Idx 30 -Text "资源索引（收藏夹必备）"
Add-Card -Idx 30 -X 1.5 -Y 5.5 -W 15 -H 4 -Title "团队公约 + 上手" -Body "agent-delivery/team-collaboration-playbook.md`nagent-delivery/team-onboarding.md`n.cursor/rules/ （00 公约 + 11 角色）"
Add-Card -Idx 30 -X 16.5 -Y 5.5 -W 15 -H 4 -Title "操作手册" -Body "agent-delivery/智能体编排与派单手册.md`nagent-delivery/项目工程化交付模式.md`nagent-delivery/COORDINATOR-START.md"
Add-Card -Idx 30 -X 1.5 -Y 10 -W 15 -H 4 -Title "架构 + 数据" -Body "agent-delivery/architecture-baseline.md`nagent-delivery/数据库设计.md`nagent-delivery/graph-engine.md / observability.md"
Add-Card -Idx 30 -X 16.5 -Y 10 -W 15 -H 4 -Title "预算 + 编排成熟度" -Body "agent-delivery/budget-estimate.md`nagent-delivery/orchestration-maturity-and-roadmap.md`nagent-delivery/cicd-pipeline.md"
Add-Footer -Idx 30 -Text "→ 所有文档在 ${GKX_ROOT}/agent-delivery/ ，git 同步，全员可读可改"
Add-PageNum -Idx 30
Set-Notes -Idx 30 -Text "资源索引 1 分钟。12 份核心文档，按 4 大类。让大家拍照存档——讲完没人能记住，但知道去哪查就行。所有文档在 git 里，全员可读可改（PR 制度），不是死文档。"

# ============ 第 31 页：谢谢 + Q&A ============
Write-Host "[build] 谢谢 (31/31)" -ForegroundColor Yellow
New-Slide -Background $BgDark
& $OC add $PPT "/slide[31]" --type shape `
    --prop geometry=rect --prop x=0cm --prop y=0cm --prop w=0.4cm --prop h=19.05cm `
    --prop fill=$Accent --prop line.width=0 | Out-Null
& $OC add $PPT "/slide[31]" --type shape `
    --prop geometry=rect --prop x=2cm --prop y=5cm --prop w=29cm --prop h=3cm `
    --prop text="Q & A" `
    --prop font=$Font --prop size=72pt --prop bold=true `
    --prop color="FFFFFF" --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
& $OC add $PPT "/slide[31]" --type shape `
    --prop geometry=rect --prop x=2cm --prop y=9cm --prop w=29cm --prop h=2cm `
    --prop text="把你的担忧、疑惑、反对意见摆上桌" `
    --prop font=$Font --prop size=28pt `
    --prop color=$Accent --prop fill=transparent --prop line.width=0 --prop align=left | Out-Null
& $OC add $PPT "/slide[31]" --type shape `
    --prop geometry=rect --prop x=2cm --prop y=13cm --prop w=29cm --prop h=4cm `
    --prop text="一句话总结：`n人决策 / AI 执行 / 接口标准化 / 团队同构 / 不打折扣" `
    --prop font=$Font --prop size=18pt `
    --prop color="CADCFC" --prop fill=transparent --prop line.width=0 --prop align=left --prop lineSpacing=1.5x | Out-Null
Set-Notes -Idx 31 -Text "Q&A 5 分钟。鼓励提问——「现在没问题，我们会假设大家都接受了，下次再质疑要走变更流程」。如果冷场，自己抛 3 个引子：(1) 谁担心 AI 用多了自己废？(2) 谁觉得每天 9:30 站会浪费时间？(3) 谁觉得 cost 跟踪是负担？这三个常见反对意见，主动回应。结束语：「明天 9:30 站会见，记得拉最新 .cursor/rules/」。"

# ============ 收尾：保存 ============
Write-Host ""
Write-Host "[save] 保存 PPT..." -ForegroundColor Cyan
& $OC close $PPT | Out-Null

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  PPT 构建完成！" -ForegroundColor Green
Write-Host "  路径: $PPT" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "下一步验证：" -ForegroundColor Yellow
Write-Host "  & '$OC' view '$PPT' outline" -ForegroundColor Gray
Write-Host "  & '$OC' view '$PPT' stats" -ForegroundColor Gray
Write-Host "  & '$OC' view '$PPT' issues" -ForegroundColor Gray
