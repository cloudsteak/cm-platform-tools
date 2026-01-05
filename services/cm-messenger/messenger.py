from fastapi import FastAPI, Header, HTTPException
from sib_api_v3_sdk.rest import ApiException

from config import get_settings
from models import SendEmailRequest, SendEmailResponse
from emailer import (
    render_template,
    build_lab_ready_context,
    send_email_via_brevo,
    TemplateNotFoundError,
)

messenger = FastAPI(
    title="cm-messenger",
    version="0.1.0",
    description="Cloud Mentor messaging service (email first)",
)


@messenger.get("/health")
def health():
    return {"status": "ok"}


@messenger.post("/v1/emails/send", response_model=SendEmailResponse)
def send_email(
    payload: SendEmailRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    settings = get_settings()

    if settings.internal_api_key and x_api_key != settings.internal_api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    context = build_lab_ready_context(
        settings=settings,
        username=payload.username,
        password=payload.password,
        cloud_provider=payload.cloud_provider,
        ttl_seconds=payload.ttl_seconds,
    )

    try:
        html = render_template(payload.template, context)
    except TemplateNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        message_id = send_email_via_brevo(
            settings=settings,
            recipient=payload.recipient,
            subject=payload.subject,
            html_content=html,
        )
        return SendEmailResponse(
            status="sent",
            provider="brevo",
            template=payload.template,
            recipient=payload.recipient,
            message_id=message_id,
        )
    except ApiException as e:
        return SendEmailResponse(
            status="failed",
            provider="brevo",
            template=payload.template,
            recipient=payload.recipient,
            error=str(e),
        )
