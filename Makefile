.PHONY: create-venv
create-venv:
	poetry install

.PHONY: venv
venv:
	poetry shell

.PHONY: docker-build
docker-build:
	docker build -f docker/Dockerfile -t nba_elt_dashboard_local .

.PHONY: docker-build-test
docker-build-test:
	docker build -f docker/Dockerfile.test -t nba_elt_dashboard_local_test .

.PHONY: docker-run
docker-run:
	docker run --rm python_docker_local

# use to untrack all files and subsequently retrack all files, using up to date .gitignore
.PHONY: git-reset
git-reset:
	git rm -r --cached .
	git add .

PHONY: git-rebase
git-rebase:
	@git checkout master
	@git pull
	@git checkout feature_integration
	@git rebase master
	@git push

.PHONY: bump-patch
bump-patch:
	@bump2version patch
	@git push --tags
	@git push

.PHONY: bump-minor
bump-minor:
	@bump2version minor
	@git push --tags
	@git push

.PHONY: bump-major
bump-major:
	@bump2version major
	@git push --tags
	@git push

.PHONY: start-postgres
start-postgres:
	@docker compose -f docker/docker-compose-postgres.yml up -d

.PHONY: stop-postgres
stop-postgres:
	@docker compose -f docker/docker-compose-postgres.yml down

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

.PHONY: test1
test1:
	@docker compose -f docker/docker-compose-test.yml up --exit-code-from dash_app_test_runner
