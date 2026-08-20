# DONE A13

| 项 | 值 |
|----|----|
| sheet | 深度挖掘算法 |
| filter | 全表数据行（deep_mining_14col：招标描述 G，六级 M，需规正文 N） |
| excel_rows | 4–119 |
| expected_data_rows | 116 |
| written_leaves | 116 |
| files | `05-深度挖掘算法/README.md`；`05-深度挖掘算法/科技专题服务算法库/科技专题服务算法库.md`（97）；`05-深度挖掘算法/语义计算工具库/语义计算工具库.md`（19） |
| gaps | G 空 96 行（写「（本行空）」+ `bid_desc_inherited`，未把组首行复制进正文）；六级 M 为 `/` 共 5 行（109/112/117/118/119，标题保留 `/`）；本表无备注列（notes 记「本表无备注列」）；N/G 抽样与 officecli JSON 原文一致，未见截断；officecli 8 块均成功 |

对账：`###` 叶子 116；`excel_row` 4–119 无缺无重。K 拆分：科技专题服务算法库 4–100（97）、语义计算工具库 101–119（19）。未 commit / 未改 Excel。
