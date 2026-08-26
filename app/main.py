from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from sqlalchemy.orm import Session
from app import config
from app.db.database import get_db
from app.db.models import User
from app.schemas import UserCreate
from app.storage.object_storage import ObjectStorage
from starlette.middleware.sessions import SessionMiddleware
from app.api import auth, chat, documents
storage = ObjectStorage()


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.ensure_bucket()
    yield

origins = [
    config.FRONTEND_URL,
]

app = FastAPI(
    title="AI Research RAG",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware, 
    secret_key=config.SESSION_SECRET_KEY
)


app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(documents.router)


templates = Jinja2Templates(
    directory="templates"
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )
