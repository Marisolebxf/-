import hashlib, json, pathlib

run = pathlib.Path(r"d:\web\gkx-lumen\gkx-orchestration\agent-delivery\bugfix-runs\7168001613-7168001613")
state = json.loads((run / "state.json").read_text(encoding="utf-8"))

def sha256(obj):
    payload = "null" if obj is None else json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()

diagnosis_hash = sha256({"diagnosis": state["diagnosis"], "plan": state["plan"]})
plan_hash = sha256(state["plan"])

binding = json.loads((run / "gate-enter-dev.json").read_text(encoding="utf-8"))
# 与 state.repos 完全一致的字段集
binding["repos"] = [
    {
        "repo_id": r["repo_id"],
        "repo_name": r["repo_name"],
        "base_branch": r["base_branch"],
        "base_sha": r["base_sha"],
        "planned_change_scope": r["planned_change_scope"],
        "candidate_sha": None,
        "role": r["role"],
        "depends_on": r["depends_on"],
        "ship_order": r["ship_order"],
    }
    for r in state["repos"]
]
binding["diagnosis_hash"] = diagnosis_hash
binding["plan_hash"] = plan_hash
binding["risk_level"] = state["risk"]["level"]
binding["data_policy_version"] = state["data_policy"]["policy_version"]
binding["data_policy_hash"] = state["data_policy"]["policy_hash"]
binding["data_scope_hash"] = state["data_policy"]["scope_hash"]

# svc 基线已平移 4c177f9f：state.repos 里的 base_sha 需要同步更新才能过 exactRepoSet 校验
for r in state["repos"]:
    if r["repo_id"] == "backend":
        r["base_sha"] = "4c177f9f"

(run / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for r in binding["repos"]:
    if r["repo_id"] == "backend":
        r["base_sha"] = "4c177f9f"

(run / "gate-enter-dev.json").write_text(json.dumps(binding, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("diagnosis_hash:", diagnosis_hash)
print("plan_hash:", plan_hash)
print("binding updated")
