"""Condense an agent session transcript into a short readable markdown file.

Works on any harness that stores sessions as JSON lines (Claude Code, Codex, Qwen Code,
and most others) by pulling the human-readable text out of each record, whatever the
schema. goose keeps sessions in SQLite instead, so it has its own mode.

  python3 session_log.py <transcript.jsonl>     condense one JSONL transcript
  python3 session_log.py goose --list           goose sessions for the current folder
  python3 session_log.py goose <session_id>     condense one goose session
Prints the output path and the session's cost (span, records, tool calls, errors).
"""
import json, os, sqlite3, sys, tempfile

TEXT_KEYS = {"text", "content", "thinking", "command", "cmd", "arguments", "input",
             "output", "result", "message", "query", "summary"}
SKIP_KEYS = {"signature", "id", "uuid", "parentUuid", "timestamp", "sessionId", "cwd",
             "encrypted_content", "data", "image_url", "source"}
NOISE_LABELS = {"attachment", "session_meta", "system", "developer", "queue-operation",
                "turn_context", "summary", "api-request-shape"}   # harness boilerplate, not the work
ERR_WORDS = ("Traceback", "Error:", "error:", "FAILED", "No such file", "command not found")


def strings(x, key=None, out=None):
    """All readable strings under text-like keys, in document order."""
    out = [] if out is None else out
    if isinstance(x, dict):
        for k, v in x.items():
            if k not in SKIP_KEYS:
                strings(v, k, out)
    elif isinstance(x, list):
        for v in x:
            strings(v, key, out)
    elif isinstance(x, str) and key in TEXT_KEYS and x.strip():
        out.append(x.strip())
    return out


def label(rec):
    for path in (("message", "role"), ("role",), ("payload", "type"), ("type",)):
        v = rec
        for p in path:
            v = v.get(p) if isinstance(v, dict) else None
        if isinstance(v, str):
            return v
    return "record"


def jsonl(path):
    out = os.path.join(tempfile.gettempdir(), "session_" + os.path.basename(path) + ".md")
    n = tools = errs = 0
    times = []
    with open(path, errors="replace") as f, open(out, "w") as w:
        for line in f:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            n += 1
            if isinstance(rec, dict) and isinstance(rec.get("timestamp"), str):
                times.append(rec["timestamp"])
            blob = json.dumps(rec)[:20000]
            if '"tool_use"' in blob or '"function_call"' in blob or '"toolRequest"' in blob \
                    or '"tool_call' in blob or '"functionCall"' in blob:
                tools += 1
            txt = "\n".join(strings(rec))
            if not txt or label(rec) in NOISE_LABELS or txt.startswith("<system-reminder>"):
                continue
            if any(e in txt for e in ERR_WORDS):
                errs += 1
            w.write(f"\n## {label(rec)}\n{txt[:800]}\n")
    span = f"{times[0]} -> {times[-1]}" if times else "no timestamps"
    report(out, f"{span}, {n} records, ~{tools} tool calls, ~{errs} with errors")


def goose(arg):
    db = sqlite3.connect("file:" + os.path.expanduser(
        "~/.local/share/goose/sessions/sessions.db") + "?mode=ro", uri=True)
    if arg == "--list":
        for sid, name, upd, n in db.execute("""select s.id, s.name, s.updated_at, count(m.id)
                from sessions s left join messages m on m.session_id = s.id
                where s.working_dir = ? group by s.id order by s.updated_at desc limit 10""",
                                            (os.getcwd(),)):
            print(f"{sid}  {upd}  {n:4d} msgs  {name}")
        print("(the newest one is probably the current session)")
        return
    out = os.path.join(tempfile.gettempdir(), f"session_goose_{arg}.md")
    tools = errs = 0
    with open(out, "w") as w:
        for role, cj in db.execute("select role, content_json from messages where session_id=? "
                                   "order by created_timestamp, id", (arg,)):
            for c in json.loads(cj):
                if c.get("type") == "toolRequest":
                    tools += 1
                txt = "\n".join(s for s in strings(c) if "<turn-context>" not in s)
                if txt:
                    errs += any(e in txt for e in ERR_WORDS)
                    w.write(f"\n## {role}/{c.get('type')}\n{txt[:800]}\n")
    name, tok, t0, t1 = db.execute("""select s.name, s.accumulated_total_tokens, min(m.timestamp),
        max(m.timestamp) from sessions s join messages m on m.session_id = s.id
        where s.id = ?""", (arg,)).fetchone()
    report(out, f"'{name}' {t0} -> {t1}, {tok or 0:,} tokens, {tools} tool calls, ~{errs} with errors")


def report(out, stats):
    kb = os.path.getsize(out) // 1024
    print(f"{stats}\nwrote {out} ({kb} KB) - "
          + ("read it in chunks, not all at once" if kb > 60 else "small enough to read whole"))
    print("(time span is wall clock and includes idle gaps)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "goose":
        goose(sys.argv[2] if len(sys.argv) > 2 else "--list")
    else:
        jsonl(sys.argv[1])
