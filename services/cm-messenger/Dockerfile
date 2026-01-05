FROM python:3.11-slim

WORKDIR /app

# UV telepítése
RUN pip install --no-cache-dir uv

# Dependency definition
COPY pyproject.toml ./

# Dependencies install (no venv, system site-packages)
RUN uv pip install --system --no-cache-dir .

# App source
COPY . .

EXPOSE 8000

CMD ["uvicorn", "messenger:messenger", "--host", "0.0.0.0", "--port", "8000"]
