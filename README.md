# NBA Dashboard

![CI/CD](https://github.com/jyablonski/nba_elt_dashboard/actions/workflows/ci_cd.yaml/badge.svg) ![Python quality](https://github.com/jyablonski/nba_elt_dashboard/actions/workflows/python-quality.yml/badge.svg) ![Deployment](https://github.com/jyablonski/nba_elt_dashboard/actions/workflows/vm_deploy.yml/badge.svg)

The NBA Dashboard has the following functionalities:

- Overview of Standings, Contract Value, and Top Player Analysis
- Recent Games Analysis
- NBA Win Prediction Percentages & other Schedule Metrics for upcoming games
- Social Media Analysis

The Project is hosted on cloud infrastructure at https://nbadashboard.jyablonski.dev

## Running The App

Use **Python 3.14** locally (see [`.python-version`](.python-version); `uv` will pick it up).

Clone the Repo & run `make up` which spins up the App locally served [here](http://localhost:9000/) using 2 Docker Containers:

- Postgres Database
- Dash Server

When finished run `make down`.

## Tests

Integration tests use **[Testcontainers](https://testcontainers-python.readthedocs.io/)** to start a disposable Postgres 16 instance, load `docker/postgres_bootstrap.sql`, and run the suite against it. **Docker must be running** for the full suite (`make test` or `pytest tests/`).

- **`make test`** — syncs test deps and runs `pytest` with coverage (≥90% on measured `src/` modules; `src/pages/*` is omitted from the coverage denominator because page modules are mostly layout wiring exercised indirectly by integration imports).
- **`make test-unit`** — runs `tests/unit/` only; no Postgres or Docker required.
- **`SKIP_INTEGRATION=1 pytest tests/`** — skips integration tests if you need a quick pass without Docker (coverage is not enforced in that mode unless you pass `--cov` yourself).

**Tests** run on every pull request and on pushes to **`main`** or **`master`** via [`.github/workflows/ci_cd.yaml`](.github/workflows/ci_cd.yaml). **Deploy** (ECR build + ECS cycle) runs only on **pushes to `main`**, after tests pass. **Ruff**, **Ruff format (`--check`)**, and scoped **`ty`** run in [`.github/workflows/python-quality.yml`](.github/workflows/python-quality.yml) when Python paths or tooling change.

## Linting

- **`make lint`** — `uv sync --all-groups`, then `ruff check` and `ruff format --check` on the repo.
- **`make format`** — applies Ruff formatting and safe fixes (`ruff check --fix`).
- **Pre-commit** — install hooks once with `uv run pre-commit install`, then they run on commit; includes **ruff-check**, **ruff-format**, **pyupgrade**, **`uv run ty check`**, and light file hygiene (see [`.pre-commit-config.yaml`](.pre-commit-config.yaml)).

## Project

![nba_pipeline_diagram](https://github.com/jyablonski/nba_elt_dashboard/assets/16946556/e41ee516-9f38-4b4a-bbeb-8447ce35d480)

1. Links to other Repos providing infrastructure for this Project
   - [Ingestion Script](https://github.com/jyablonski/nba_elt_ingestion)
   - [dbt](https://github.com/jyablonski/nba_elt_dbt)
   - [ML Pipeline](https://github.com/jyablonski/nba_elt_mlflow)
   - [Terraform](https://github.com/jyablonski/aws_terraform)
   - [REST API](https://github.com/jyablonski/nba_elt_rest_api)
   - [Internal Documentation](https://doqs.jyablonski.dev)
