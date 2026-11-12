---
name: self-improve
description: Retrospective on how a recent task was handled (code, docs, data, anything), run from a fresh session, to improve the agent itself on any harness or model. Finds mistakes, slowness and waste, traces each to a gap in the agent's own setup (rules files, skills, tools, settings), and proposes numbered fixes that fit with what is already there, so future tasks on ANY project go better. Does not fix or improve the project itself. Use for retros, postmortems, "what went wrong", "why did that take so long", "how can you do better next time".
---

# Self-improve

This is a retrospective on **how the agent worked**, not on the project. The project is
only the evidence. The output is a set of changes to the agent's own setup that would
make it handle future tasks, on any project, better.

Run it from a fresh session (a new chat, or a subagent) that did not do the work. The
session that did it is anchored on its own choices; you are not. Form your own view
BEFORE reading how or why the work was done.

Two questions, both always:
1. **Where did the work go wrong?** Mistakes, wrong turns, claims that were not true.
2. **Where was the process slow or wasteful?** Even correct work can take far longer or
   cost far more than it needed to.
For each answer, the real question is: **what in the agent's setup let this happen, and
what change to that setup would prevent it next time, on a different project?**

## Rules

- Do not fix, improve or propose changes to the project: not its code, docs, data, notes
  or project-level rules files. Problems in the work are recorded as evidence (one line).
- Change nothing until the user picks proposals in their reply. Running a script that
  rewrites project files counts as a change: copy what you need to a temp folder first.
- Evidence over opinion. A finding needs a check you ran or a moment you can point to in
  the record. "Looks wrong" is a hypothesis, not a finding.
- Do not invent problems. "The process was sound and reasonably quick" is a good result;
  then propose little or nothing.
- Keep context small: limit command output, read big files in chunks.
- Budget: stop after about 3 approaches (or ~10 tool calls) on any one check; record it
  as "could not verify" and move on. This is a retrospective, not a redo of the task.

## Steps

### 1. Pin the goal (without the old reasoning)
From the user's request or the task description, write in 2-3 lines what the task was
supposed to achieve and how anyone would know it succeeded. Do not read handoff notes,
logs or the old transcript yet.

### 2. Look at the result first-hand
Open the actual outputs: run the code or tests, read the document as its reader would,
view the file. Note what it does, not what it claims. Did it meet the goal?

### 3. Spot-check the key claims
List the 2-4 claims the result most depends on (it works, it is accurate, it is
complete, it was verified). For each, ask: was it checked with evidence the work itself
did not produce? A check that reuses the same data, reference or reasoning is circular:
it proves consistency, not correctness. Run a cheap independent check where you can.
Mark each: HELD / FAILED / COULD NOT VERIFY. A failed or circular claim is evidence of a
process gap, not something to fix here.

### 4. Find the simple path
Knowing what you know now: what was the shortest route to this result? Compare with the
route actually taken (inputs, stages, files, turns). A big gap is the most common source
of slowness.

### 5. Review the process
Find the record of how the work was done: the session transcript, handoff notes, git log.
`references/harnesses.md` lists where common harnesses keep transcripts. The bundled
`scripts/session_log.py` condenses one into a short markdown file and prints its cost
(time span, records, tool calls, errors): `python3 scripts/session_log.py <file.jsonl>`,
or `python3 scripts/session_log.py goose --list` for goose (paths are relative to this
skill's folder; use the full path if your shell is elsewhere). Read the result in chunks.
Find:
- where the time and tokens went, and whether that part mattered;
- the same thing retried or fixed repeatedly (wrong approach, not wrong code);
- the moment a wrong assumption entered, and what would have caught it sooner;
- detours: work built then abandoned, checks that could not fail, output dumped into
  context, context running out, handoffs that carried a false claim forward;
- what the agent lacked: a rule, a procedure, a tool or script, knowledge, a setting;
- what went well and should be kept.

### 6. Turn lessons into setup gaps
For each lesson, ask: **would this have helped on a different project?** If not, drop it
or mention it in one line. If yes, it points at a gap in the agent's setup.

Then take stock of the setup as it is now (see `references/harnesses.md` for where it
lives): read the always-on rules files in full, list the skills and skim the relevant
ones, check settings, tools and any custom system prompt. Note which harnesses the user
runs; a lesson may belong in more than one.

For each gap, pick the narrowest place a fix belongs:
- **always-on rules** (paid on every turn of every session: short, broadly useful lines only);
- **a skill** for a repeatable procedure, loaded only when relevant (edit one or add one);
- **a script or tool** for a step the agent did by hand, slowly or repeatedly;
- **a setting** (effort, compaction, permissions, hooks, extensions);
- **no change**: the lesson is already covered and was not followed. Say which rule was
  ignored, and whether it needs to be stronger, shorter, or moved where it will be seen.

### 7. Check proposals against what exists, and against each other
Before writing any proposal, compare it with every existing rule, skill, setting and
tool you found in step 6, and with the other proposals:
- **Duplicate**: already said elsewhere. Do not add a second copy. Sharpen or move the
  existing one instead, or drop the proposal.
- **Overlap**: partly covered. Extend the existing text rather than adding a parallel rule.
- **Contradiction**: it pulls the opposite way from an existing rule or another proposal
  (e.g. "always ask first" vs "act without asking"; "be brief" vs "explain everything").
  Do not leave both in place. Weigh them: what each protects, how often each situation
  comes up, what this task's evidence says. Recommend one of: replace the old rule (say
  exactly what gets removed), scope both so they no longer collide ("X for Y, Z
  otherwise"), or drop the new proposal. If it is a close call, say so and give both
  options; the user decides.
- **Cross-harness drift**: if the user runs several harnesses, check whether the same rule
  already exists in another one with different wording. Prefer one shared version.
Record the outcome on each proposal (step 8). Never apply a change that leaves two rules
contradicting each other.

### 8. Report and propose
Use this shape, plain words, no padding:

```
Outcome: goal met / partly met / not met — one line.
Process: efficient / slow / wasteful — where the cost went (time, tokens, turns).

What went wrong (evidence only, not for fixing here)
- what happened — where in the record — what it cost

What went well (keep)
- ...

Setup gaps
- the gap — the lessons it explains — would it recur on other projects, and why

Proposed changes (reply with the numbers to apply)
1. [rules | skill | script | setting] title — which harness(es)
   Prevents: which gap, and what it would have saved this time
   Change: the exact file and the exact text, code or setting to add / replace / remove
   Fits with: none found / extends <existing rule> / replaces <existing rule> /
              conflicts with <rule or proposal N>: the weighing, and the recommendation
   Cost/risk: what it costs to keep (context on every turn, speed) and what could go wrong
```

How to write proposals:
- Each one ready to apply as written: the file and the actual text. "Be more careful" is
  not a proposal; "add this line to <rules file>" is.
- Never a change to the project.
- Always-on text is paid for on every turn: at most two lines per proposal. If it needs
  more, propose a skill instead.
- Three good proposals beat ten weak ones. Order by value. Zero is fine if nothing is missing.

Then stop and wait for the user's reply.

### 9. Apply what the user picks
- Apply only the numbers the user chose, exactly as proposed (or as they amended),
  including any removals or replacements the proposal named.
- Back up any existing file before editing it (`cp file file.bak-YYYYMMDD`).
- Re-read every file you changed and confirm no two rules now contradict each other.
- Verify each change took: run a new script once, use the harness's own validator where
  one exists (a recipe or config check), and for rules or skills confirm the file reads
  back correctly (best: ask a fresh session to quote it). Report what was applied, how it
  was checked, and how to undo it.
