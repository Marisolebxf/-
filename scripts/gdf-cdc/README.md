# gdf-cdc

GDF 派单包 → 两张 CDC 预填表。Skill：`.cursor/skills/gkx-gdf-cdc-workpack/`  
v1 明细模板填写规则：`.cursor/skills/gkx-gdf-cdc-workpack/v1-dwd-cdc-template-rules.md`

```bash
python scripts/gdf-cdc/parse_workpack.py --workpack "<WORKPACK>" -o inventory.json
python scripts/gdf-cdc/fill.py both --workpack "<WORKPACK>" --inventory inventory.json --out "<WORKPACK>/预填作业"

# v1 校准（只写 校准生成/，禁止写执行结果/）
python scripts/gdf-cdc/extract_v1_recipes.py
python scripts/gdf-cdc/fill.py both --calibrate --workpack "<V1_WORKPACK>" --inventory inventory.json --out "<V1_WORKPACK>/校准生成"
python scripts/gdf-cdc/diff_cdc.py --gold "<V1_WORKPACK>/执行结果" --gen "<V1_WORKPACK>/校准生成" -o "<V1_WORKPACK>/校准生成/DIFF.md"
```
