from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth import get_current_active_user
from app.db.database import get_db
from app.db.models import Document
from app.storage.object_storage import ObjectStorage
from app.ingestion.pipeline import ingest_document

router = APIRouter()

storage = ObjectStorage()


@router.post("/documents")
async def upload_document(
    file: UploadFile = File(...),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):

    document_id = uuid4()

    storage_key = await storage.upload(
        file=file,
        document_id=document_id,
    )

    document = Document(
        id=document_id,
        user_id=current_user["user"].email,
        filename=file.filename,
        storage_key=storage_key,
        status="PROCESSING",
    )

    db.add(document)
    db.commit()
    db.refresh(document)
    
    ingest_document(
    document,
    db,
    )
    
    

    return {
        "id": str(document.id),
        "filename": document.filename,
        "status": document.status,
        "storage_key": document.storage_key,
    }
    
@router.get('/documents')
async def get_documents(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):  
    user_id = current_user["user"].email
    documents = db.scalars(select(Document).filter_by(user_id=user_id)).all()
    
    return documents
    