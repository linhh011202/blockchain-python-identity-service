from pydantic import BaseModel


class RegisterResponse(BaseModel):
    email: str

    class Config:
        from_attributes = True
