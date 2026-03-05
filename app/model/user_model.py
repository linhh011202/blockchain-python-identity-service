from sqlmodel import Field

from app.model.base_model import BaseModel


class UserModel(BaseModel, table=True):
    __tablename__ = "tb_users"

    email: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(nullable=False)
