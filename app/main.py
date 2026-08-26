import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app import config
from app.logging import configure_logging
from app.storage.object_storage import ObjectStorage
from starlette.middleware.sessions import SessionMiddleware
from app.api import auth, chat, documents

storage = ObjectStorage()
configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    logger.info("Ensuring MinIO bucket")
    storage.ensure_bucket()
    logger.info("MinIO bucket ready")
    yield
    logger.info("Application shutdown")


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

logger = logging.getLogger(__name__)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    logger.info("Requested home page!")
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

@app.get("/health/live")
async def health():
    return {"status": "ok"}
