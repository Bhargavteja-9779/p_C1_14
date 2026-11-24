#!/usr/bin/env bash
# Layer B supervisor: restarts the agent CLI headlessly until state/agent_state.json says FINISHED.
# For a LOCAL machine with the `claude` CLI logged in. Not useful inside an ephemeral cloud container.
# Start:  nohup scripts/supervisor.sh >/dev/null 2>&1 &     Stop: touch state/STOP   (or kill the PID in state/supervisor.pid)
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"; echo $$ > state/supervisor.pid
LOG=logs/supervisor.log; DELAYS=(300 900 1800 3600); i=0
CLI=$(command -v claude || true)
[ -z "$CLI" ] && { echo "$(date -u) no agent CLI found; paste BOOTSTRAP_PROMPT.txt manually" >> $LOG; exit 1; }
while true; do
  grep -q '"status": "FINISHED"' state/agent_state.json && { echo "$(date -u) FINISHED" >> $LOG; exit 0; }
  [ -f state/STOP ] && { echo "$(date -u) STOP file" >> $LOG; exit 0; }
  echo "$(date -u) starting agent (attempt $i)" >> $LOG
  OUT=$("$CLI" -p "$(cat BOOTSTRAP_PROMPT.txt)" --permission-mode acceptEdits 2>&1 | tail -50); RC=$?
  echo "$OUT" | tail -5 >> $LOG; echo "$(date -u) agent exited rc=$RC" >> $LOG
  RESET=$(echo "$OUT" | grep -oiE 'reset[s]? at [^.]*' | head -1)
  D=${DELAYS[$(( i < 3 ? i : 3 ))]}; i=$((i+1))
  [ -n "$RESET" ] && echo "$(date -u) limit message: $RESET (sleeping $D s)" >> $LOG
  sleep "$D"
done
