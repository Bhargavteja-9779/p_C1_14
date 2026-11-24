#!/usr/bin/env python3
"""Usage: q.py JOB_ID STATUS [note]  -> updates state/queue.json, agent_state.step, heartbeat."""
import json, sys, os, datetime as dt
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = os.path.join(R, "state/queue.json")
q = json.load(open(P)); jid, st = sys.argv[1], sys.argv[2]
hit = [x for x in q["jobs"] if x["id"] == jid]
if not hit: q["jobs"].append(hit := {"id": jid, "status": st, "attempts": 0}) or None; hit = [q["jobs"][-1]]
hit[0]["status"] = st
if st == "running": hit[0]["attempts"] += 1
if len(sys.argv) > 3: hit[0]["note"] = sys.argv[3]
tmp = P + ".tmp"; json.dump(q, open(tmp, "w"), indent=1); os.replace(tmp, P)
open(os.path.join(R, "state/heartbeat"), "w").write(dt.datetime.now(dt.timezone.utc).isoformat())
