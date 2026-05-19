FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
RUN pip install uv && uv sync
RUN uv run python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

COPY . .

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
