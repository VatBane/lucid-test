from pydantic import BaseModel, Field, ConfigDict


class UserData(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserFullData(UserData):
    id_: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
