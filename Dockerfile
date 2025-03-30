FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Disable Python downloads, because we want to use the system interpreter across both images.
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /action/workspace
RUN apt update \
  && apt install -y --no-install-recommends git \
  && apt clean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /github/workspace \
  && git config --system --add safe.directory /github/workspace \
  && git config --global user.email "generate-changelog@github.actions" \
  && git config --global user.name "Generate Changelog"

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
COPY . /action/workspace
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Then, use a final image without uv
FROM python:3.12-slim-bookworm

ARG USERNAME=app
ARG USER_UID=1000
ARG USER_GID=$USER_UID
USER $USERNAME

ENV PATH="/action/workspace/.venv/bin:$PATH"

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

LABEL com.github.actions.name="Run Generate Changelog" \
    com.github.actions.description="Run generate-changelog to create or update a changelog." \
    com.github.actions.icon="file-text" \
    com.github.actions.color="black" \
    maintainer="@coordt" \
    org.opencontainers.image.authors="Calloway Project https://github.com/callowayproject" \
    org.opencontainers.image.created=2025-03-22T16:21:25Z \
    org.opencontainers.image.url="https://github.com/callowayproject/generate-changelog" \
    org.opencontainers.image.source="https://github.com/callowayproject/generate-changelog" \
    org.opencontainers.image.version="0.13.0" \
    org.opencontainers.image.licenses=MIT \
    org.opencontainers.image.documentation="https://github.com/callowayproject/generate-changelog" \
    org.opencontainers.image.description="Run generate-changelog to create or update a changelog."

COPY --from=builder --chown=app:app /action/workspace/ /action/workspace/

ENTRYPOINT ["/action/workspace/entrypoint.sh"]
