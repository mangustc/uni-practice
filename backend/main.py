from fastapi import FastAPI
from api import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_tables, new_session
from Function import deactivate_expired_new_products
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.isfile("./data.db"):
        await create_tables()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(deactivate_expired_new_products, "interval", days=1)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:80",
    "http://localhost:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



