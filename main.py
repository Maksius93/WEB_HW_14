import asyncio

import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from starlette.background import BackgroundTasks
from starlette.middleware.cors import CORSMiddleware

from src.routes import contacts, auth, users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')


async def task():
    await asyncio.sleep(3)
    print("Send email")
    return True


@app.on_event("startup")
async def startup(settings=None):
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
def read_root(background_tasks: BackgroundTasks):
    background_tasks.add_task(task)
    return {"message": "CONTACT API"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", reload=True, log_level="info", port=5000)