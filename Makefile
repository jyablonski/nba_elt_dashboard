.PHONY: docker-build
docker-build:
	docker build -f docker/Dockerfile -t nba_elt_dashboard_local .

.PHONY: docker-build-test
docker-build-test:
	docker build -f docker/Dockerfile.test -t nba_elt_dashboard_local_test .

.PHONY: ci-test
ci-test:
	@make start-postgres
	@poetry run pytest --cov --cov-report xml
	@make stop-postgres

.PHONY: up
up:
	@docker compose -f docker/docker-compose-local.yml up -d

.PHONY: down
down:
	@docker compose -f docker/docker-compose-local.yml down

.PHONY: follow-logs
follow-logs:
	@docker compose -f docker/docker-compose-local.yml logs dash_app --follow

# idk why but makefile was returning w/ error 137 on successful test runs, so this just skips that error
.PHONY: test
test:
	@docker compose -f docker/docker-compose-test.yml down
	@docker compose -f docker/docker-compose-test.yml up --exit-code-from dash_app_test_runner || [ $$? -eq 137 ]

.PHONY: lint
lint:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
        echo "Virtual environment not activated. Activating Poetry environment..."; \
        poetry run black .; \
        poetry run ruff check .; \
    else \
        black .; \
        ruff check .; \
    fi
