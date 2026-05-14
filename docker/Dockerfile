FROM python:3.14-slim AS base

ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/.venv/bin:/root/.cargo/bin:$PATH" \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=3.14

# install OS-level deps once in base (so we don't repeat in each stage)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# -------------------------------
# Stage: Install Python deps
# -------------------------------
FROM base AS python-deps

ARG INSTALL_DEV_DEPENDENCIES=false

COPY pyproject.toml uv.lock ./

RUN pip install uv==0.11.14 && \
    if [ "$INSTALL_DEV_DEPENDENCIES" = "true" ]; then \
    uv sync --frozen --group test; \
    else \
    uv sync --frozen --no-dev; \
    fi

# -------------------------------
# Stage: Runtime
# -------------------------------
FROM base AS runtime

# Add build argument for git commit SHA
ARG GIT_COMMIT=unknown
ENV GIT_COMMIT=${GIT_COMMIT}

COPY --from=python-deps ./.venv ./.venv

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY config.yaml .
COPY src/ src/
COPY static/ static/

EXPOSE 9000

CMD ["python", "-m", "src.server"]
