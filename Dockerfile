FROM prefecthq/prefect:3.4.1-python3.10

WORKDIR /opt/prefect/app

# 1. Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && uv --version

# 2. Copy pyproject.toml and (optionally) uv.lock to install dependencies
COPY pyproject.toml .
COPY uv.lock . 

# 3. Install Python dependencies into the system interpreter
RUN uv pip install --no-managed-python --requirements pyproject.toml

# 4. Copy the rest of your flow code
COPY main.py main.py