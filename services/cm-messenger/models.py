from pydantic import BaseModel, Field
from typing import Literal


CloudProvider = Literal["azure", "aws"]


class SendEmailRequest(BaseModel):
    template: str = Field(default="lab_ready_default", min_length=1)
    recipient: str = Field(min_length=3)
    subject: str = Field(default="A labor környezeted elkészült!")

    username: str
    password: str
    cloud_provider: CloudProvider
    ttl_seconds: int = Field(ge=0)


class SendEmailResponse(BaseModel):
    status: Literal["sent", "failed"]
    provider: Literal["brevo"]
    template: str
    recipient: str
    message_id: str | None = None
    error: str | None = None
