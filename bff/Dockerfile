# FastAPI BFF image for Azure Container Apps.
# Includes Microsoft ODBC Driver 18 for SQL Server (required for DATA_SOURCE=fabric via pyodbc).
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# System deps + Microsoft ODBC Driver 18 (Debian 12 / bookworm).
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl gnupg2 ca-certificates apt-transport-https gcc g++ unixodbc-dev \
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -sSL https://packages.microsoft.com/config/debian/12/prod.list -o /etc/apt/sources.list.d/mssql-release.list \
    && sed -i 's#deb https://#deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://#' /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first for layer caching.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source.
COPY app ./app

# Run as a non-root user.
RUN groupadd -r app && useradd -r -g app app
USER app

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
