from pydantic import BaseModel


class LoginResponse(BaseModel):
    email: str

    class Config:
        from_attributes = True
