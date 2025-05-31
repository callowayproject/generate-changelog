FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder

ARG APP_DIR=/app
WORKDIR $APP_DIR

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON=python3.13 \
    UV_PYTHON_INSTALL_DIR=/usr/share/uv/python

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
COPY . $APP_DIR
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Then, use a final image without uv
FROM debian:bookworm-slim

ARG USERNAME=app
ARG USER_UID=1001
ARG USER_GID=118
ARG APP_DIR=/app
ARG WORKDIR=/github/workspace

ENV APP_DIR=$APP_DIR

LABEL com.github.actions.name="Run Generate Changelog" \
    com.github.actions.description="Run generate-changelog to create or update a changelog." \
    com.github.actions.icon="file-text" \
    com.github.actions.color="black" \
    maintainer="@coordt" \
    org.opencontainers.image.authors="Calloway Project https://github.com/callowayproject" \
    org.opencontainers.image.created=2025-05-31T12:32:58Z \
    org.opencontainers.image.url="https://github.com/callowayproject/generate-changelog" \
    org.opencontainers.image.source="https://github.com/callowayproject/generate-changelog" \
    org.opencontainers.image.version="0.16.0" \
    org.opencontainers.image.licenses=MIT \
    org.opencontainers.image.documentation="https://github.com/callowayproject/generate-changelog" \
    org.opencontainers.image.description="Run generate-changelog to create or update a changelog."

WORKDIR $WORKDIR

ENV PATH="$APP_DIR/.venv/bin:$PATH"

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN apt update \
  && apt install -y --no-install-recommends git \
  && apt clean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p $WORKDIR \
  && chown $USERNAME:$USER_GID $WORKDIR \
  && git config --system --add safe.directory $WORKDIR \
  && git config --global user.email "generate-changelog@github.actions" \
  && git config --global user.name "Generate Changelog"

USER $USERNAME

COPY --from=builder --chown=$USERNAME:$USER_GID /usr/share/uv/python /usr/share/uv/python
COPY --from=builder --chown=$USERNAME:$USER_GID $APP_DIR $APP_DIR
SHELL ["/bin/bash", "-c"]
ENTRYPOINT $APP_DIR/entrypoint.sh
