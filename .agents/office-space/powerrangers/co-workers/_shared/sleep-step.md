# Sleep Step

End every cycle by running `node {{awaitScript}} {{workflow}} {{agent}}` in the background so it
survives your exit.

Use `nohup node {{awaitScript}} {{workflow}} {{agent}} >/dev/null 2>&1 &` then `disown`. Do not wait
for the command to return; end this turn immediately.
