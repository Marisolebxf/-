# P0-18 逐步实际操作

1. click「查企业」tab → 单独读态 active=查企业（hero 搜索框可见）
2. click「高级筛选」tab → 读态 active=高级筛选（高筛面板/结果区出现）
3. click「智能搜索」tab → 读态 active=智能搜索（hero 回归）
4. click「查企业」tab → 读态 active=查企业
5. 全程无两个 tab 同时 selected=true
6. 判定 Pass

> 技术备注：tab 点击的状态更新为异步（React setState），同一 eval 内 click+读会得到旧值；
> 分「点击 eval」与「读态 eval」两步执行则全部正确。自动化脚本需按此模式写等待。
