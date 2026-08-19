from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from app.api.documents import router as documents_router
from app.api.chat import router as chat_router
from app.storage.object_storage import ObjectStorage

storage = ObjectStorage()


@asynccontextmanager
async def lifespan(app: FastAPI):

    storage.ensure_bucket()

    yield


app = FastAPI(
    title="AI Research RAG",
    lifespan=lifespan,
)

templates = Jinja2Templates(
    directory="templates"
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

app.include_router(
    documents_router
)

app.include_router(
    chat_router
)