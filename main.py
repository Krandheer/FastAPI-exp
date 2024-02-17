from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()


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
