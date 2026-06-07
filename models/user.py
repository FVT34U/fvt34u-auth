from pydantic import BaseModel, ConfigDict, EmailStr
import uuid
from datetime import date, datetime

class User(BaseModel):
    username: str
    password_hash: str

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    birthday: date | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)