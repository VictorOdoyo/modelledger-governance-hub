FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN useradd --create-home --uid 10001 modelledger
COPY pyproject.toml uv.lock ./
COPY modelledger ./modelledger
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev

USER modelledger
EXPOSE 8088
CMD ["/app/.venv/bin/uvicorn", "modelledger.api.app:app", "--host", "0.0.0.0", "--port", "8088"]
