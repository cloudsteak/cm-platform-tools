from pathlib import Path

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from jinja2 import Environment, FileSystemLoader, select_autoescape

from config import Settings


class TemplateNotFoundError(Exception):
    pass


_ALLOWED_TEMPLATES = {"lab_ready_default"}


def _jinja_env() -> Environment:
    templates_dir = Path(__file__).parent / "templates"
    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )


def render_template(template_name: str, context: dict) -> str:
    if template_name not in _ALLOWED_TEMPLATES:
        raise TemplateNotFoundError(f"Template not allowed: {template_name}")

    env = _jinja_env()
    filename = f"{template_name}.html"

    try:
        template = env.get_template(filename)
    except Exception as e:
        raise TemplateNotFoundError(f"Template not found: {filename}") from e

    return template.render(**context)


def build_lab_ready_context(
    settings: Settings,
    username: str,
    password: str,
    cloud_provider: str,
    ttl_seconds: int,
) -> dict:
    if cloud_provider == "azure":
        cloud_console_url = settings.portal_azure_url
        effective_username = f"{username}@evolvia.hu"
    else:
        cloud_console_url = settings.portal_aws_url
        effective_username = username

    ttl_minutes = int(ttl_seconds / 60) if ttl_seconds else 0

    return {
        "cloud_console_url": cloud_console_url,
        "username": effective_username,
        "password": password,
        "ttl_minutes": ttl_minutes,
        "cloud_provider": cloud_provider,
    }


def send_email_via_brevo(
    settings: Settings,
    recipient: str,
    subject: str,
    html_content: str,
) -> str | None:
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.brevo_api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": recipient}],
        html_content=html_content,
        sender={"email": settings.email_sender, "name": settings.sender_name},
        subject=subject,
    )

    try:
        response = api_instance.send_transac_email(email)
        return getattr(response, "messageId", None)
    except ApiException:
        raise
