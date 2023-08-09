from typing import Annotated

from fastapi import Header, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from application.database import SessionLocal
from application.config import SECRET_KEY, ALGORITHM
from application.service.users import get_user_by_id

# 用户认证
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 认证和权限验证
def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    user = get_user_by_id(db, user_id)
    if user is not None:
        return user
    raise HTTPException(status_code=401, detail="User not found")
