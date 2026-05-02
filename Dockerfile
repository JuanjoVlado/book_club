FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
RUN pip install uv && uv sync

COPY . .

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
