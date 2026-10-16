FROM python:3.15-slim AS base

# libtk8.6: tkinter の実行に必要です (slim イメージには入っていません)。
RUN apt-get update \
    && apt-get install -y --no-install-recommends libtk8.6 fonts-ipafont-gothic \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 1000 app


FROM base AS app

# tigervnc / novnc: 仮想ディスプレイの画面をブラウザで見るために使います。
# TigerVNC はクリップボードを UTF-8 で受け取れるので、日本語を貼り付けられます。
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tigervnc-standalone-server tigervnc-tools novnc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /data && chown app:app /data

COPY CocCharamakeSupport.py /app/
COPY docker/start.sh /usr/local/bin/start.sh

USER app
# compose で uid を変えたとき (HOME に書き込めないとき) も fontconfig のキャッシュを置けるようにします。
ENV XDG_CACHE_HOME=/tmp/.cache
# OUTPUT ボタンの出力先です。
WORKDIR /data
EXPOSE 6080
CMD ["start.sh"]


FROM base AS dev

# xvfb-run (xvfb + xauth): GUI テストを仮想ディスプレイで動かすために使います。
RUN apt-get update \
    && apt-get install -y --no-install-recommends xvfb xauth \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /usr/local/bin/uv
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    PATH=/opt/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked
RUN chown app:app /app
COPY --chown=app:app . .

USER app
ENTRYPOINT ["xvfb-run", "--auto-servernum", "--server-args=-screen 0 1400x1000x24"]
CMD ["pytest"]
