from pydantic import BaseModel, Field


class GetUserRequest(BaseModel):
    email: str = Field(
        ..., min_length=3, max_length=128, description="Email to retrieve"
    )
