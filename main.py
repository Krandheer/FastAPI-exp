import os
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWSError, jwt
from passlib.context import CryptContext
from pydantic_core.core_schema import BoolSchema
from dotenv import load_dotenv


BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, ".env"))

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


db = {
    "tim": {
        "username": "ravi",
        "full_name": "ravi coder",
        "email": "ravi@xyz.come",
        "hashed_password": "",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str
    fullname: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()


def verify_password(plain_password, hashed_password):
    """password verification"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hashed(password):
    """hashing the password"""
    return pwd_context.hash(password)


def get_user(db, username: str):
    """get user"""
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)
    return {"err": "user not found in dd"}


def authenticate_user(db, username: str, password: str):
    """authenticate user"""
    user = get_user(db, username)
    if not user:
        return False
    hashed_password = get_password_hashed(password)
    if not verify_password(password, hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """generate access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


class Data(BaseModel):
    name: str


@app.post("/create/")
async def create(data: Data):
    """create data"""
    return {"data": data}


# @app.get("/")
# async def home():
#     """first api in fastapi"""
#     return {"api": "home page"}
#
#
# @app.get("/{item_id}")
# async def hello_api(item_id: str):
#     """checking params"""
#     return {"api": item_id}
#
#
# @app.get("/{queries}")
# async def query_params(queries: str, query: int = 1):
#     """checking query_params"""
#     return {"api": queries, "query_param": query}
