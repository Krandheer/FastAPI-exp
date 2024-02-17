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

fake_db = {
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
