from fastapi import FastAPI
from .utils import config
from .getNode import router as GetNodeRouter

app = FastAPI()

@app.get("/uu.json", tags=["Root"])
async def read_root() -> dict:
    return config

#全局路由
app.include_router(GetNodeRouter, prefix="/getNode")


