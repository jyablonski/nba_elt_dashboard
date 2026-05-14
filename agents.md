# NBA ELT Dashboard — agent guide

Concise orientation for coding agents and new contributors. For user-facing setup, see [README.md](README.md).

## What this is

A **Plotly Dash** web app (Python **3.14**) that visualizes NBA analytics loaded from **Postgres** (typically `gold.*` tables from the upstream dbt pipeline). It is **not** the ingestion/dbt/ML repo—those live elsewhere (README links). This repo is the **read-only dashboard** plus Docker/CI wiring.

## Stack

| Piece                                | Role                                                    |
| ------------------------------------ | ------------------------------------------------------- |
| `dash` + `dash-bootstrap-components` | UI; theme **Bootswatch SLATE** via `dbc.themes.SLATE`   |
| `pandas`                             | In-memory tables exposed as module-level `*_df` globals |
| `sqlalchemy` + `psycopg2`            | DB reads                                                |
| `pyyaml`                             | `config.yaml` + env substitution                        |

## Entry point and app shape

- **Run:** `python -m src.server` (or Docker per `make up`).
- **`src/server.py`** constructs `dash.Dash`, registers **`dbc.Tabs`** as the main shell (no separate top brand row—**`app.title`** still sets the browser tab title), and assigns each tab’s `children=` to a page layout imported from **`src/pages/`**.
- **Navigation:** single-page app with tabs (not multipage URLs). Tab counts/badges are built at import time in `server.py` using `src.shell` helpers.
- **Assets:** `assets_folder="../static"` relative to the app module; CSS lives under **`static/`** (`styles.css` for global tokens and chrome; **`tab_shell.css`** for the shell tab rail scoped under `.nba-shell-tabs` — dbc `Tabs` renders **`ul#tabs.nav.nav-tabs`**, and Bootswatch SLATE layers gradients on `.nav-tabs .nav-link`).

## Data loading (important)

**`src/database.py`** runs at **import time**:

1. Loads **`config.yaml`** via `src.yaml_config.load_yaml_with_env` keyed by **`ENV_TYPE`** (default `dev`).
2. Opens a SQLAlchemy engine with **`src.db_connection.sql_connection`**.
3. Calls **`generate_data`**, which loops **`src.data.source_tables`** and assigns each result to a **module-level global** named `{table}_df` (e.g. `standings_df`, `player_stats_df`).

**Implications:** Importing `src.server` or `src.database` pulls the full dataset into memory and **requires a live DB** unless tests use mocks/Testcontainers. **`src/pages/*`** and **`src/utils`** often import from **`src.database`** directly.

Supporting modules: **`src/data.py`** (table list), **`src/db_connection.py`** (queries), **`src/config.py`** (shared constants / re-exports where noted).

## Directory map

```
src/
  server.py          # Dash app, tabs, layout shell
  database.py        # Import-time load → *_df globals
  db_connection.py   # Engine + get_data
  data.py            # source_tables list
  yaml_config.py     # YAML + env placeholders
  config.py          # App constants / shared helpers
  shell.py           # Season label, tab label strings
  utils.py           # Dropdowns, Plotly helpers, etc.
  theme/plotly.py    # Dark layout + trace hover defaults
  ui/                # Reusable layout: cards, tables, sections, badges
  pages/             # One module per tab (layouts + callbacks co-located)
  data_cols/         # Dash DataTable column specs per domain table
static/
  styles.css         # Design tokens, DataTable/dropdown overrides, shell chrome
  tab_shell.css      # Tab rail only (scoped; fights SLATE explicitly)
tests/
  unit/              # Fast; no Docker
  integration/       # Testcontainers Postgres + bootstrap SQL
docker/              # Dockerfile, compose, postgres_bootstrap.sql
.github/workflows/   # ci_cd, python-quality, deploy
```

## Pages and callbacks

Each **`src/pages/<name>.py`** typically defines:

- `<name>_layout` — `html.Div` / `dbc` tree.
- `@callback` functions bound to controls on that tab.

**`src/ui/`** centralizes repeated patterns (`dark_datatable`, KPI cards, `page_hero`, `section_header`). **`src/theme/plotly.py`** applies consistent dark styling to figures.

**`src/data_cols/*.py`** holds `list[dict]` column definitions for `dash_table.DataTable` (often with `FormatTemplate` / `Format`).

## Configuration

- **`config.yaml`** — per-environment host, port, credentials, schema. **`ENV_TYPE`** selects the block; values can use **`${VAR}`** env substitution (see `yaml_config`).
- Local Docker: **`docker/docker-compose-local.yml`** aligns env with the compose Postgres service.

## Tests and quality

| Command                            | Purpose                                                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `make test-unit`                   | Unit tests only; no Docker                                                                                                |
| `make test`                        | Full pytest + coverage (≥90% on measured `src/`; **`src/pages/*` omitted** from coverage denominator in `pyproject.toml`) |
| `SKIP_INTEGRATION=1 pytest tests/` | Skip integration without Docker                                                                                           |

Integration tests use **Testcontainers** to start Postgres, load **`docker/postgres_bootstrap.sql`**, then import app/data paths. **Docker must be running** for the full suite.

**`ty`** is configured to type-check only **`src/theme`** and **`src/ui`** (`[tool.ty.src]`). **Ruff** lint/format applies repo-wide; pre-commit mirrors that plus pyupgrade.

## Docker / deploy

- **`docker/Dockerfile`** builds the Dash image; **`docker-compose-local.yml`** runs app + Postgres for dev.
- **Local compose** bind-mounts `src/` and `static/` but **Python does not reload** unless the process restarts. The compose file sets **`DASH_RELOAD=1`**, which turns on **Flask’s `use_reloader`** (not Dash `debug=True`, which breaks on Python 3.12+ because Dash still uses `pkgutil.find_loader`). If you disable that or run a one-off container, use **`make restart`** (or `docker compose … restart dash_app`). Production images need a **rebuild/redeploy** to pick up shell changes.
- **CI:** `.github/workflows/ci_cd.yaml` runs tests on PR/push; deploy workflow (ECR/ECS) is separate per README badges.

## Conventions for agents

- Prefer **small, focused diffs**; match existing patterns in `src/ui` and `pages` rather than new abstractions unless requested.
- **Tab shell styling:** change **`static/tab_shell.css`** and the **`html.Div(..., className="nba-shell-tabs")`** wrapper in `server.py`, not ad-hoc global `.nav-tabs` overrides in `styles.css` (SLATE will fight you).
- **New data surfaces:** add the table to **`src/data.source_tables`**, consume `your_table_df` from **`src.database`** (or pass through a thin helper), and add **`src/data_cols/`** specs if tabular.
- **Callbacks:** keep `id=` stable if tests or docs reference them; register outputs/inputs consistently with Dash 2 patterns.

## Design doc

High-level redesign notes (palette, phases, out-of-scope items): **`docs/2025-05-13-redesign-plan.md`**. Treat it as intent, not a spec—verify against code.
