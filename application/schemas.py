from typing import Optional, Union

from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: Union[str, None] = None


class User(BaseModel):
    id: int
    username: str
