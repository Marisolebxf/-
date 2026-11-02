# Graph

与 `data/GDF/` 平级。图谱的建图和入图放这里。GDF 继续只做贴源、洗数和调度，不把图的派单包放进 GDF 工作包。

| 目录 | 内容 |
|---|---|
| [建图/](建图/) | 图空间、Tag、Edge，以及按维度整理的本侧抽取说明。燕大要执行的语句在入图包的 schema 文件里，空间名是 `gkx_chain` |
| [入图需求和派单/](入图需求和派单/) | 按要素分批写入。企业维 [KG-ENT-WORKPACK-v0.1](入图需求和派单/KG-ENT-WORKPACK-v0.1/)（WBS-07-00G），产业链维 [KG-CHAIN-WORKPACK-v0.1](入图需求和派单/KG-CHAIN-WORKPACK-v0.1/)（WBS-07-00H）。空间、schema、库账号只在企业包里 |

图库口令和读接口密钥不进这个目录。MySQL 只读口令在入图包的环境文件里。
