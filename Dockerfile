# FROM prefecthq/prefect:3.4.1-python3.10
FROM --platform=linux/amd64 ghcr.io/osgeo/gdal:ubuntu-small-3.10.3

# ---- 1. Environment variables ----
ENV PIP_ROOT_USER_ACTION=ignore
ENV PIP_BREAK_SYSTEM_PACKAGES=1
ENV UV_LINK_MODE=copy

# ---- 2. Set working directory ----
COPY entrypoint.sh /opt/prefect/entrypoint.sh
WORKDIR /opt/prefect/app

# ---- 3. System packages (minimal needed only) ----
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python-is-python3 \
    curl \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# ---- 4. Install pip and uv ----
RUN curl -o /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py && \
    python3 /tmp/get-pip.py && \
    pip install uv --break-system-package && \
    rm -f /tmp/get-pip.py

# ---- 5. Install Python dependencies ----
COPY pyproject.toml uv.lock /opt/prefect/app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# ---- 6. Copy application source ----
COPY main.py main.py

# ---- 7. Compile Python to bytecode ----
RUN python3 -m compileall /opt/prefect/app

# ---- 8. Remove build-time dependencies ----
RUN apt-get purge -y build-essential python3-dev && \
    apt-get autoremove -y && \
    rm -rf /root/.cache /var/lib/apt/lists/* /tmp/*

# ---- 9. Set working directory again explicitly ----
WORKDIR /opt/prefect/app


