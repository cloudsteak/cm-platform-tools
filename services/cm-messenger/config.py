import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    brevo_api_key: str
    email_sender: str
    sender_name: str

    portal_azure_url: str
    portal_aws_url: str

    internal_api_key: str | None = None


def get_settings() -> Settings:
    return Settings(
        brevo_api_key=os.environ["BREVO_API_KEY"],
        email_sender=os.environ["EMAIL_SENDER"],
        sender_name=os.getenv("EMAIL_SENDER_NAME", "Cloud Mentor"),
        portal_azure_url=os.environ["PORTAL_AZURE_URL"],
        portal_aws_url=os.environ["PORTAL_AWS_URL"],
        internal_api_key=os.getenv("INTERNAL_MESSENGER_API_KEY"),
    )
