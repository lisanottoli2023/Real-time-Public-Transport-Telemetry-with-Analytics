FROM python:3.11-slim


WORKDIR /Producer

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates apt-utils && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml uv.lock ./


RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY . .


CMD ["uv", "run", "producer.py"]
