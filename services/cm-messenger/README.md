# CM-Messenger

Cloud Mentor messaging service - email-based notification microservice.

## Overview

CM-Messenger is a FastAPI-based REST API service that handles email notifications using Brevo (formerly Sendinblue) as the external service provider. It is primarily designed to send notifications about lab environment (Azure/AWS) provisioning with access credentials.

## Key Features

- Email sending based on Jinja2 templates
- Azure and AWS lab environment access credential notifications
- Brevo (Sendinblue) integration
- API key-based authentication
- Health check endpoint
- Docker and Kubernetes support

## Requirements

- Python 3.11+
- uv (dependency management)
- Brevo API key

## Installation

### 1. Local Development Environment

#### Using uv

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies (automatically creates venv if needed)
uv sync

# Set environment variables
export BREVO_API_KEY="your-brevo-api-key"
export EMAIL_SENDER="sender@example.com"
export EMAIL_SENDER_NAME="Cloud Mentor"
export PORTAL_AZURE_URL="https://portal.azure.com"
export PORTAL_AWS_URL="https://console.aws.amazon.com"
export INTERNAL_MESSENGER_API_KEY="your-internal-api-key"  # optional

# Run the application
uv run uvicorn messenger:messenger --reload --host 0.0.0.0 --port 8000
```

### 2. Using Docker

```bash
# Build Docker image
docker build -t cm-messenger:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e BREVO_API_KEY="your-brevo-api-key" \
  -e EMAIL_SENDER="sender@example.com" \
  -e EMAIL_SENDER_NAME="Cloud Mentor" \
  -e PORTAL_AZURE_URL="https://portal.azure.com" \
  -e PORTAL_AWS_URL="https://console.aws.amazon.com" \
  -e INTERNAL_MESSENGER_API_KEY="your-internal-api-key" \
  --name cm-messenger \
  cm-messenger:latest
```

### 3. Using Kubernetes Helm Chart

```bash
# Install Helm chart (from chart directory)
helm install cm-messenger ./chart \
  --set env.BREVO_API_KEY="your-brevo-api-key" \
  --set env.EMAIL_SENDER="sender@example.com" \
  --set env.EMAIL_SENDER_NAME="Cloud Mentor" \
  --set env.PORTAL_AZURE_URL="https://portal.azure.com" \
  --set env.PORTAL_AWS_URL="https://console.aws.amazon.com" \
  --set env.INTERNAL_MESSENGER_API_KEY="your-internal-api-key"

# Check status
kubectl get pods -l app=cm-messenger

# Upgrade
helm upgrade cm-messenger ./chart --reuse-values
```

## Environment Variables

| Variable Name | Required | Default | Description |
|--------------|----------|---------|-------------|
| `BREVO_API_KEY` | Yes | - | Brevo API key |
| `EMAIL_SENDER` | Yes | - | Sender email address |
| `EMAIL_SENDER_NAME` | No | "Cloud Mentor" | Sender name |
| `PORTAL_AZURE_URL` | Yes | - | Azure Portal URL |
| `PORTAL_AWS_URL` | Yes | - | AWS Console URL |
| `INTERNAL_MESSENGER_API_KEY` | No | - | API key for endpoint protection |

## API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "ok"
}
```

### Send Email

```bash
curl -X POST http://localhost:8000/v1/emails/send \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-internal-api-key" \
  -d '{
    "template": "lab_ready_default",
    "recipient": "user@example.com",
    "subject": "Your lab environment is ready!",
    "username": "testuser",
    "password": "SecurePass123!",
    "cloud_provider": "azure",
    "ttl_seconds": 86400
  }'
```

Response:
```json
{
  "status": "sent",
  "provider": "brevo",
  "template": "lab_ready_default",
  "recipient": "user@example.com",
  "message_id": "abc123..."
}
```

## Development

### Run Tests

```bash
# Install dev dependencies
uv sync --extra dev

# Run tests
uv run pytest
```

### API Documentation

Available after running the application:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Adding a New Template

1. Create a new HTML file in the `templates/` directory
2. Add the template name to the `_ALLOWED_TEMPLATES` set in `emailer.py`
3. Extend the context builder function if necessary

## Project Structure

```
services/cm-messenger/
├── messenger.py           # FastAPI application, main endpoints
├── emailer.py            # Email sending, template rendering logic
├── models.py             # Pydantic models (request/response)
├── config.py             # Configuration and environment variables
├── templates/            # Jinja2 email templates
│   └── lab_ready_default.html
├── pyproject.toml        # Project definition (uv compatible)
├── Dockerfile           # Docker image build description
├── chart/               # Kubernetes Helm chart
└── README.md            # This file
```

## License

Cloud Mentor Platform Tools

## Contact

Cloud Mentor Team
