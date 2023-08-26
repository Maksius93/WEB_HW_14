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
    """
    The task function is a coroutine that sleeps for 3 seconds and then prints
    &quot;Send email&quot;. It returns True.


    :return: A boolean value
    :doc-author: Trelent
    """
    await asyncio.sleep(3)
    print("Send email")
    return True


@app.on_event("startup")
async def startup(settings=None):
    """
    The startup function is called when the application starts up.
    It can be used to initialize things that are needed by the app, such as a database connection pool or an external API client.
    The startup function must be a coroutine and it receives one argument: settings.

    :param settings: Pass in the fastapilimiter settings
    :return: The redis connection object
    :doc-author: Trelent
    """
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
def read_root(background_tasks: BackgroundTasks):
    """
    The read_root function is a ReST endpoint that returns the message &quot;CONTACT API&quot;.

    :param background_tasks: BackgroundTasks: Add a task to the background queue
    :return: A dictionary with a key of message and a value of contact api
    :doc-author: Trelent
    """
    background_tasks.add_task(task)
    return {"message": "CONTACT API"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", reload=True, log_level="info", port=5000)