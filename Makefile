COVERAGE_THRESHOLD ?= 90

.PHONY: build
build:
	docker build -f docker/Dockerfile -t nba_elt_dashboard_local .

.PHONY: test
test:
	uv sync --group test
	uv run pytest --cov=src --cov-report=term-missing \
		--cov-fail-under=$(COVERAGE_THRESHOLD) tests/

.PHONY: test-unit
test-unit:
	uv sync --group test
	uv run pytest tests/unit

.PHONY: ci-test
ci-test:
	uv sync --group test
	uv run pytest --cov=src --cov-report=term-missing \
		--cov-fail-under=$(COVERAGE_THRESHOLD) tests/

.PHONY: up
up:
	@docker compose -f docker/docker-compose-local.yml up -d

.PHONY: down
down:
	@docker compose -f docker/docker-compose-local.yml down

.PHONY: restart
restart:
	@docker compose -f docker/docker-compose-local.yml restart dash_app

.PHONY: follow-logs
follow-logs:
	@docker compose -f docker/docker-compose-local.yml logs dash_app --follow

.PHONY: lint
lint:
	uv sync --all-groups
	uv run ruff check .
	uv run ruff format --check .

.PHONY: format
format:
	uv sync --all-groups
	uv run ruff format .
	uv run ruff check --fix .
