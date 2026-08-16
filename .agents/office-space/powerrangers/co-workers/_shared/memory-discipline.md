## Your Memory

Your log lives at `.agents/office-space/{{workflow}}/memory/{{agent}}/<log-name>.md` and has two
sections:

- **`## Digest`** — one line per past finding. Read this **in full** before every sweep. It is what
  stops you re-reporting something you already filed.
- **`## Recent`** — the newest entries with full detail. Skim it; read a specific entry only when
  you need the reasoning behind a digest line.

Never read the whole file top to bottom "for context" — it is deliberately bounded so your wake
stays cheap, and the digest already carries the part that matters.

Append with the script, not by hand — it keeps the format machine-readable so old entries can be
compacted:

```bash
node {{memoryLogScript}} append {{workflow}} {{agent}} \
  --summary "one line: what you swept and what you filed" \
  [--area path/to/area] [--refs thing-one,thing-two]
```

Log every wake, including quiet ones — "nothing new in X, all clean" is a useful entry. Older
entries are compacted into the digest automatically; you do not need to trim anything yourself.

Never put memory or notes files in `.agents/office-space/{{workflow}}/slack/{{agent}}/` — that
folder is your mailbox, and every file dropped there reads as unread mail.
