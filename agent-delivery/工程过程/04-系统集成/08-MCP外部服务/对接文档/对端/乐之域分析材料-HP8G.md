<!-- feishu-doc {"doc": "HP8Gd88BOo5RMUxbPFecyLiVndg"} 只改标记下面的文字；不要删改 <!-- b:... --> 标记 -->
<!-- b:IvpJdBIGUo2hGUxLz70cYn3dnhf ordered -->
首先，战略问题是一个无定解命题，所以不存在“全局最优”结果。核心在于，言之有物，论之有理。我们的重点不应该放在 最后写出来的报告上，而是应该放在一个给agent的 开放 自由的环境上。在不断的延伸和对抗中产出有深度的猜想和论断。
<!-- b:ZwLJdVMTJoj5rMx1I6KcDLvQnhe ordered -->
战略分析的核心不在最后的呈现的形态，而在于对于命题的研究剖析，猜想推理和推理对抗。即便用户存在主观的偏向，但可能性假设，分析逻辑，催化剂等应该是客观的。故建议将产品功能拆解成为如下三个部分：
<!-- b:ORXBdBtCjoqsgdxvAQzc2xKingg ordered -->
命题澄清：进行命题扩写，材料范围选取和补充
<!-- b:ZxaMdXlRAoIw5FxjETecNlnrncd ordered -->
辩论研究阶段【重点】：通过可控的多轮交叉正反智能体辩论，动态构建战略知识体系。
<!-- b:ISqEdrBlmob9yox8dhVcBveKnWh ordered -->
制品产出：根据研究阶段结果，进行制品生成。此处用户可以再定义所需材料，写作偏向，观点偏向等
<!-- b:X4XgdyIKzoZfhIxx2jCcINsCndh ordered -->
辩论研究阶段设计：
<!-- b:C8P5diaylol6BBxMDSvcOqXQnqd ordered -->
首先正反两方智能体，一次基于完整的双方辩论知识体系，进行材料检索+分析+本轮论点论据的生成。应该有如下约束：首先，必须至少提出的是一个全新的论点，甚至论据不可以重复。其次需要针对对方的已有推理，提出质疑和证伪，综合产出多个论点作为本轮研究结果。
<!-- b:LfXDdkkMfoOpYdx5DDBc3yMdnWe ordered -->
研究结果由三层组成（参考知识金字塔）：最下层为原始信源组成的论据（信源层），中层为支撑论点的核心的检索/推理/计算过程（推理层），上层为本轮研究的多个核心论点（结论层）。一个论点可以被拆解成多个中间层交叉映射。
<!-- b:VQ5ede3vBoiN0RxtfwxcGkz6nlf ordered -->
在跨轮次的研究结果间可以存在关联关系，简单来说就是：同方可以继承已有的论点，进行延伸和补充。不同方可以根据对方的已有论点，进行反驳和证伪
<!-- b:CKI4dIwEqofrFixeXIzcqmu9nud ordered -->
每一轮全新的论点是重要的，保证了辩论的生命力和不会落入局部循环。可以由人控制大的辩论轮次。如果在已有的辩论流程没有出现我们需要的方向，可以在追加轮次中引导（只提供方向，不提供偏向）。
<!-- b:UaaEdculIoo6bPxIDbhcQOLlnwe ordered -->
由于我们的目标不是得到全局最优，所以我个人认为无需judge agent，也无需一个第三方因素控制。在后续的写作过程中可以加入人的倾向，或者进行已有辩论的总结判断
<!-- b:Z71UdPxB9oKcaRxpUy2c7aCtnAf ordered -->
动态战略知识体系：
<!-- b:HRtKdJx2foOZfHxHH49c8B3HnOb ordered -->
参考展示给招商的经营体系的模式，辩论中的每一轮agent都有读写权限。首先agent可以首先查看完整的一生成动态简历的辩论论点卷宗。
<!-- b:SUTTdabM0opCjIxxzgncjC6cnxf ordered -->
针对需要反驳的观点，通过卷宗下探分析方式+信源，从而了解到完整的论据，从而引导新的论点的提出
<!-- b:DEC7d6NnEoXurCxwTF6cI8QXnSO ordered -->
每一轮完成后，调用写的能力，完成本轮卷宗内容的写入（包括上中下层的完整内容）
<!-- b:IID5dyIVWonFDlxkHdEcTwhrnZf ordered -->
制品产出阶段：
<!-- b:X18CdXZk5oad05x5i4rcVMl4nff ordered -->
将前一阶段构建的动态战略知识体系导入，只提供 读 权限
<!-- b:T79ld5gYyoTEtzxbd8pcaFyGnVc ordered -->
完全开放最终制品的形态，包括但不限于文档，ppt，html等。此处不再进行research和动态搜索，所有参考只依赖动态战略知识体系。如果要补充内容，则回到前阶段继续构建辩论
<!-- b:X1FDdL7gBob9NZxhcwacnD6LnHh ordered -->
产品copilot设计：左侧为会话区，会话区分为 澄清，辩论研究，报告生成三个chunk。进入研究流程后，依次展示每次正方/反方智能体的研究过程（工具执行链路）。右侧为预览区，可以查看完整的知识体系（上，中，下层层递进，论点之间的关联关系等），或者制品（word，ppt，html预览）
<!-- b:YTxadkdMUoTzsBxlIeQcrppZnyc ordered -->
实现难度：
<!-- b:X0J8dkILMonXkUxkzvncOlyqnAc ordered -->
动态战略知识体系：基于已有 招商经营分析知识构建改造
<!-- b:Tskhd9s7hohERBxMdptc9lZLnkd ordered -->
research阶段：基于AaaS模式重新设计
<!-- b:UsncdhYY3ogwxCxLZSicQg4Hn8f ordered -->
澄清和产出制品阶段：基于现有智库报告写作技术方案扩展
<!-- b:RlkYdl7e2oeE3axUT0pc0E6pnAF text -->

