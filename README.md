# self-improve

A skill for AI coding agents. It reviews how a finished task was handled and proposes
changes to the agent's own setup so later tasks go better. It does not change the project
it reviews.

Works with any harness that loads `SKILL.md` skills (goose, Claude Code, Codex, Qwen Code,
others) and any model.

## What it does

Run from a fresh session that did not do the work:

1. States the task's goal before reading any notes from the session that did it.
2. Checks the result directly and spot-checks its key claims. Flags checks that were
   circular (verified using the same data that produced the result).
3. Works out the shortest path to the result and compares it with the path taken.
4. Reads the session transcript: where time and tokens went, repeated retries,
   abandoned work, wrong assumptions, what went well.
5. Keeps lessons that would apply to other projects and maps each to a gap in the
   agent's setup: rules file, skill, script, or setting.
6. Compares every proposal with the existing setup and with the other proposals.
   Duplicates are dropped, overlaps extend existing text, contradictions are weighed
   and resolved (replace, scope, or drop).
7. Reports, then waits. Nothing is changed until the user picks proposals.

## Output

```
Outcome: goal met / partly met / not met
Process: efficient / slow / wasteful, and where the cost went

What went wrong      evidence only, with where it happened
What went well       to keep
Setup gaps           the missing rule, procedure, tool or setting

Proposed changes (reply with the numbers to apply)
1. [rules | skill | script | setting] title, target harness
   Prevents:  the gap, and what it would have saved
   Change:    exact file and exact text
   Fits with: none / extends X / replaces X / conflicts with X, and the recommendation
   Cost/risk: per-turn context cost, what could go wrong
```

Reply with the numbers to apply (e.g. "1 and 3"). The agent backs up each file, applies
the changes, checks that no rules now contradict each other, and reports how to undo.

## Install

Clone into your harness's skills folder:

```bash
git clone https://github.com/DMS3tv/self-improve ~/.agents/skills/self-improve
```

Other harnesses: symlink it into their skills folder, e.g.
`ln -s ~/.agents/skills/self-improve ~/.claude/skills/self-improve`.
`references/harnesses.md` lists the usual folders per harness.

## Use

Ask in a new session: "use the self-improve skill on <task / folder / session>".

goose only: `goose/self-improve.yaml` is a recipe that starts the fresh session for you.
Copy it into `~/.agents/recipes/` (a symlink is not picked up), then:

```bash
goose run --recipe self-improve --params target="what to review" --params focus="why it was slow"
```

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | The procedure the agent follows |
| `references/harnesses.md` | Where each harness keeps rules, skills, settings and transcripts |
| `scripts/session_log.py` | Condenses a session transcript (any JSONL, or goose's database) and prints its cost |
| `goose/self-improve.yaml` | Optional goose recipe |

`session_log.py` needs only Python 3.
