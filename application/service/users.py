from datetime import datetime, timedelta

from jose import jwt

from application.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from application.models import Auth
from sqlalchemy.orm import Session


def create_user(db: Session, username, password):
    user = Auth(username=username, password=password)
    db.add(user)
    db.commit()
    return user


def get_user(db: Session, username):
    user = db.query(Auth).filter_by(username=username).first()
    return user


def get_user_by_id(db: Session, id):
    user = db.query(Auth).filter_by(id=id).first()
    return user


def update_user(db: Session, user, password):
    user.password = password
    db.commit()


def delete_user(db: Session, user):
    db.delete(user)
    db.commit()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session, username, password):
    user = get_user(db,username)
    if user is None:
        return None
    if user.password != password:
        return None

    return user
