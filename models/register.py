from pydantic import BaseModel, ConfigDict, Field
from pydantic import EmailStr
from datetime import date


class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=16,
    )
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=50,
    )
    birthday: date | None = None

    model_config = ConfigDict(extra="forbid")