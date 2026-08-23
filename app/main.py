import os

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from sqlalchemy.orm import Session
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
    os.environ["FRONTEND_URL"],
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
    # to generate secret_key run: openssl rand -hex 32
    secret_key=os.environ["SESSION_SECRET_KEY"]
)  # Replace with a secure, random key!

# 🔹 Registering Routers
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


@app.post('/register')
async def register(register_data: UserCreate, db: Session = Depends(get_db)):
    user = db.get(User, {"email": register_data.email})
    if user:
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Account already exists",
                )
    new_user = auth.create_user(email=register_data.email, password=register_data.password, full_name=register_data.full_name, db=db)
    

    return {
        "message": "Account created successfully!",
    }
    
    