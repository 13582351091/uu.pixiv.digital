from fastapi import FastAPI
from randomSubscribeUrl import router as randomSubscribeUrlRouter
import uvicorn

app = FastAPI()
#全局路由
app.include_router(randomSubscribeUrlRouter, prefix="/randomSubscribeUrl")

#这个是部署hf上
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=7860)
