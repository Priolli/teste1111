from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from betsavior.api import db
from betsavior.api.routes import chat, uploads, users

app = FastAPI(title="BetSavior API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(uploads.router)
app.include_router(users.router)


@app.on_event("startup")
async def startup_event() -> None:
    db.init_db()
