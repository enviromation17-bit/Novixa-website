# Novixa — Decisions Log

Every real decision gets an entry here: what we chose, why, and what else we
considered. This is what lets the founder explain the system confidently
without re-deriving it each time. Keep entries short — a few sentences each.

Format:
```
## [Date] Decision Title
**What:** one line
**Why:** one or two sentences
**Alternatives considered:** one line
**Status:** Active / Superseded by [link]
```

---

## [2026-08-xx] Containerize backend with Docker
**What:** Backend (FastAPI app) runs in a Docker container via
`backend/Dockerfile` + `docker-compose.yml`.
**Why:** Consistent runtime across dev/prod, matches roadmap Day 18 Night task.
**Alternatives considered:** Running uvicorn directly on host — rejected,
doesn't match roadmap's cloud-deployment goal (Day 20).
**Status:** Active

## [2026-08-31] Two-team structure: Team A (Delivery) / Team B (Research)
**What:** Split company into Team A (client delivery, business-model problem
solving) and Team B (research + SaaS pipeline for repetitive/data problems).
**Why:** Prevents trying to build the full AI-org-chart architecture before
having a single working client proof point. Team B validates ideas with real
signal before Team A or the company invests engineering time.
**Alternatives considered:** Build all departments (Sales, Marketing, Eng,
etc.) simultaneously — rejected as unrealistic for a 3-person team (founder +
2 AI assistants) and prone to building infrastructure nobody uses.
**Status:** Active

## [2026-08-31] Differentiation = proof, not org-chart concept
**What:** Competitive positioning rests on documented real results ("here's
the problem, here's the system, here's the result"), not on the AI-CEO/
Director/Employee structure itself.
**Why:** Hierarchical multi-agent "AI workforce" structures are an actively
crowded space (multiple funded startups building similar patterns as of
2026). The org chart alone is not defensible; a track record of solved,
verifiable client problems is.
**Alternatives considered:** Marketing the org-chart concept as the unique
selling point — rejected, not actually unique, and unverifiable to
prospects until backed by real case studies.
**Status:** Active

## [2026-09-02] Day 19 Night — Fixed two volume-persistence bugs
**What:** SQLite database and application logs were both being written
*outside* their intended Docker volume mounts, meaning both would be
permanently destroyed on every container recreation.
- DB: `DATABASE_URL` (relative path) and `alembic.ini` (hardcoded, ignores
  env var) both pointed to `/app/novixa.db` instead of `/app/data/novixa.db`.
  Fixed by setting `DATABASE_URL=sqlite:////app/data/novixa.db` and updating
  `alembic.ini`'s `sqlalchemy.url` to match, then rebuilding the image.
- Logs: `docker-compose.yml` had no volume mount for `/app/logs` at all
  (only `./data:/app/data` existed). Fixed by adding `./logs:/app/logs`.
**Why:** Both were proven with an evidence-based test (write test data,
destroy container, recreate, check if data survived) rather than assumed
fixed. Both failed the first time, both passed after the fix.
**Alternatives considered:** None — these were bugs, not design choices.
**Status:** Active (fixed). Commit `09b7f8f`.

## [2026-09-02] Day 19 Night — Compose `.env` interpolation warning
**What:** Escaped every `$` in `ADMIN_PASSWORD_HASH` (Argon2id format) as
`$$` in `.env`, since Docker Compose interpolates `.env` for its own
variable substitution separately from `env_file:` passing values to the app.
**Why:** Eliminates cosmetic warnings on every `docker compose` command
without touching the real secret value (Compose un-escapes `$$` back to `$`
before the app ever sees it).
**Status:** Active (fixed).

## [2026-09-02] Day 19 Night — Deferred security findings (not fixed yet)
Queued deliberately rather than fixed same-session, to avoid risking newly
verified working config:
1. **Container runs as root** — no `USER` directive in Dockerfile. Fix
   requires also adjusting file permissions on `/app/data` and `/app/logs`
   (the volumes just fixed) — needs its own careful, tested session.
2. **`/health` hardcodes "Novixa"** — will drift once brand name (currently
   "Renolt" on frontend) is finalized. Low risk, quick fix when name is locked.
3. **`ADMIN_PASSWORD` + `ADMIN_PASSWORD_HASH` both in `.env`** — plaintext
   password defeats the purpose of the hash. Do not remove the plaintext
   until admin login is tested working via the hash alone.
4. **Alembic ignores `DATABASE_URL`** — `alembic.ini` hardcodes its own DB
   path independent of the app's env var. Today's fix edited `alembic.ini`
   directly; durable fix is wiring `alembic/env.py` to read `DATABASE_URL`
   with `alembic.ini` as fallback only.
**Status:** Open — revisit in a dedicated session, not bundled into
unrelated roadmap days.

## [2026-09-03] Brand architecture: single brand, no vertical spin-offs (yet)
**What:** Renolt stays one brand. If a vertical (e.g. AI Security, AI
Fashion) proves itself through Team B's research process, it becomes a
sub-labeled offering under Renolt (e.g. "Renolt Security"), not a separate
company/brand.
**Why:** Modeled on Google's product-suite pattern (one trust umbrella,
sub-named products) rather than Alphabet's holding-company pattern (fully
separate brands/teams/capital). The latter only works with the scale and
capital to build multiple brands' trust independently — not available to a
solo-founder + AI-assistant team pre-revenue.
**Alternatives considered:** Separate brand per vertical — rejected as
resource-prohibitive at current stage; re-earning credibility from zero
multiple times simultaneously.
**Status:** Active. Revisit only if/when a vertical reaches independent
scale (real team, real capital, real client base of its own).

## [2026-09-03] Team B: research multiple verticals, commit to one for first case study
**What:** Team B's weekly research loop can explore several candidate
industries (e.g. AI security, AI fashion, others) rather than one
predetermined vertical. But the company commits engineering depth to only
ONE vertical for its first real case study — selected by evidence (real
recurring pain + willingness to pay + buildable with current skills), not
by founder interest alone.
**Why:** Prevents spreading thin across many industries with no single
credible proof point. Matches the "here's the problem, here's what we
built, here's the result" trust-building principle — applied to market
selection, not just individual products.
**Status:** Active — applies starting Phase 3 (Day 21+), not before.

## [2026-09-03] Roadmap discipline: capture strategic ideas here, don't chase mid-task
**What:** When a new strategic idea (brand architecture, vertical focus,
new nav structure, etc.) surfaces while working a different roadmap item,
log it in this file and continue the current task, rather than switching
focus immediately.
**Why:** Strategic ideas don't arrive on schedule, but roadmap discipline —
finishing Day N before starting Day N+1 — is what actually ships a
50-day plan. This file exists specifically so good ideas aren't lost
without derailing the current day's work.
**Status:** Active, ongoing practice.

---
*Add new entries above this line, most recent at the bottom of the file
above this marker.*
