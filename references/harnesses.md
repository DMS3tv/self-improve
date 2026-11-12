# Where an agent's setup lives

Every harness has the same five kinds of setup surface. Find yours before proposing
anything: list the folders, read the files. Locations below are the usual ones; versions
move things, so confirm by looking, and ask the user if you cannot find a surface.

| Surface | What it is | Cost |
|---|---|---|
| Always-on rules | Instructions loaded into every session | Paid on every turn: keep lines short |
| Skills | `<name>/SKILL.md` folders, loaded only when relevant | Cheap until used |
| Tools / scripts | Commands, MCP servers, helper scripts | Tool descriptions may be always-on |
| Settings | Model, effort, permissions, hooks, compaction, extensions | Changes behaviour globally |
| Transcripts | Records of past sessions: the evidence for a retrospective | Read only |

## Common harnesses

**goose**
- Always-on rules: `~/.config/goose/.goosehints` (global), `.goosehints` (project);
  optional custom system prompt `~/.config/goose/prompts/system.md`
- Skills: `~/.agents/skills/`, `.agents/skills/` (project)
- Recipes (launchable workflows): `~/.agents/recipes/`, `~/.config/goose/recipes/`
- Settings: `~/.config/goose/config.yaml` (extensions, thinking effort, compaction threshold)
- Transcripts: SQLite `~/.local/share/goose/sessions/sessions.db`
  (`session_log.py goose --list`, then `session_log.py goose <id>`)

**Claude Code**
- Always-on rules: `~/.claude/CLAUDE.md` (global), `CLAUDE.md` (project)
- Skills: `~/.claude/skills/`, `.claude/skills/` (project)
- Subagents / slash commands: `~/.claude/agents/`, `~/.claude/commands/`
- Settings and hooks: `~/.claude/settings.json`, `.claude/settings.json`
- Transcripts: `~/.claude/projects/<folder-path-with-dashes>/<session-id>.jsonl`

**Codex CLI / app**
- Always-on rules: `~/.codex/AGENTS.md` (global), `AGENTS.md` (project)
- Skills: `~/.codex/skills/` (some versions also read `~/.agents/skills/`)
- Settings: `~/.codex/config.toml`
- Transcripts: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`

**Qwen Code** (and other Gemini-CLI-style harnesses)
- Always-on rules: a context file such as `QWEN.md` / `GEMINI.md` (global in the
  harness's home folder, or per project); check `settings.json` for its name
- Skills: `~/.qwen/skills/`
- Settings: `~/.qwen/settings.json`
- Transcripts: `~/.qwen/projects/<folder-path-with-dashes>/chats/*.jsonl`

**Anything else**
Look in the harness's home folder (`~/.<name>/`, `~/.config/<name>/`) for: a markdown
rules or persona file, a `skills/` folder, a settings file, and a `sessions/`,
`projects/` or `chats/` folder. Most transcripts are JSON lines;
`session_log.py <file.jsonl>` condenses any of them.

## Sharing one skill across harnesses
A skill folder is plain files, so one copy can serve several harnesses: keep it in one
place and symlink it into each harness's skills folder
(`ln -s ~/.agents/skills/<name> ~/.claude/skills/<name>`). Propose this when a lesson
applies to every harness the user runs; do not do it unasked.
