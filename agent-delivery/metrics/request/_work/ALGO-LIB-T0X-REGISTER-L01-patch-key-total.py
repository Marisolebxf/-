from pathlib import Path

p = Path(__file__).resolve().parents[2] / "registry" / "metric-readiness-matrix-ENT.yaml"
text = p.read_text(encoding="utf-8")
old = (
    "    d1_def_status: missing\n"
    "    d1_pending_ref: Q038\n"
    '    d1_note: "未入 cfg_metric-ENT-seed，待王惠正式化；重点企业识别阈值归 Q038；'
    'ADS-facts-contract-E31 提示重点企业计数禁止复用 M_ENT_TOTAL_COUNT"'
)
new = (
    "    d1_def_status: draft\n"
    "    d1_pending_ref: Q038\n"
    '    d1_note: "ALGO-LIB-T0X-REGISTER-L01 已写入 seed 身份；algorithm_type=UNKNOWN；'
    '阈值仍归 Q038，不视为王惠已正式化。D2/D3/D4 维持原值。"'
)
# unique to KEY_TOTAL block: only replace within that metric
start = text.find("  - metric_id: M_ENT_KEY_TOTAL\n")
if start < 0:
    raise SystemExit("KEY_TOTAL not found")
end = text.find("\n  - metric_id:", start + 10)
block = text[start:end]
if "d1_def_status: missing" not in block:
    raise SystemExit("expected missing in KEY_TOTAL block")
block2 = block.replace("metric_name_zh: 重点企业总数（未注册）", "metric_name_zh: 重点企业总数", 1)
block2 = block2.replace("d1_def_status: missing", "d1_def_status: draft", 1)
block2 = block2.replace(
    'd1_note: "未入 cfg_metric-ENT-seed，待王惠正式化；重点企业识别阈值归 Q038；ADS-facts-contract-E31 提示重点企业计数禁止复用 M_ENT_TOTAL_COUNT"',
    'd1_note: "ALGO-LIB-T0X-REGISTER-L01 已写入 seed 身份；algorithm_type=UNKNOWN；阈值仍归 Q038，不视为王惠已正式化。D2/D3/D4 维持原值。"',
    1,
)
p.write_text(text[:start] + block2 + text[end:], encoding="utf-8")
print("patched")
