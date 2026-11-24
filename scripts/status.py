#!/usr/bin/env python3
"""Print project state: agent state, queue, budget, heartbeat age, data cache, git. Read-only, safe to run any time."""
import json, os, subprocess, time, datetime as dt
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def j(p):
    try: return json.load(open(os.path.join(R, p)))
    except Exception as e: return {"error": str(e)}
s = j("state/agent_state.json"); q = j("state/queue.json"); b = j("state/budget.json")
print(f"status={s.get('status')} cycle={s.get('cycle')} phase={s.get('phase')}\nstep: {s.get('step')}\nlast: {s.get('last_action')}")
for job in q.get("jobs", []): print(f"  [{job['status']:>9}] {job['id']} (attempts {job['attempts']})")
print(f"compute this cycle: {b.get('cycle_4_h')} h / {b.get('cycle_ceiling_h')} h ; global ceiling {b.get('global_ceiling_h')} h")
try:
    hb = open(os.path.join(R, "state/heartbeat")).read().strip(); print("heartbeat:", hb)
except FileNotFoundError: print("heartbeat: none")
ra = os.path.join(R, "data_cache", "ra")
print("data_cache:", f"{len(os.listdir(ra))} cohort files" if os.path.isdir(ra) else "MISSING -> run scripts/rebuild_cache.sh")
print(subprocess.run(["git", "-C", R, "log", "-3", "--oneline"], capture_output=True, text=True).stdout)
print(subprocess.run(["git", "-C", R, "status", "-sb"], capture_output=True, text=True).stdout.splitlines()[0])
