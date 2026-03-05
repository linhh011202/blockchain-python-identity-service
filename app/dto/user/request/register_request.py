from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=128, description="Email address")
    password: str = Field(..., min_length=6, max_length=128, description="New password")
