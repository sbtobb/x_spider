from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from application.schemas import UserRegister, User
from application.service.users import authenticate_user, create_access_token, get_user, create_user, get_user_by_id


from application.dependencies import get_db

router = APIRouter(
    prefix="/auth",
)


# 注册用户
@router.post("/register")
def register(user: UserRegister, db=Depends(get_db)):
    exist_user = get_user(db, user.username)
    if exist_user is not None:
        raise HTTPException(status_code=400, detail="Username already registered")

    create_user(db, user.username, user.password)
    return {"message": "User registered successfully"}


# 生成JWT令牌
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}





@router.get("/me")
def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
