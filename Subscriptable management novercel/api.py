from fastapi import FastAPI
from randomSubscribeUrl import router as randomSubscribeUrlRouter

app = FastAPI()
#全局路由
app.include_router(randomSubscribeUrlRouter, prefix="/randomSubscribeUrl")


