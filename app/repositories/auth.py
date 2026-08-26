from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas import UsrInDB

def create_user(email: str, hashed_password: str, full_name: str, db: Session):
    new_user = User(email=email,
    hashed_password=hashed_password,
    full_name=full_name,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# retrieves a user from the database by username
# returns a UsrInDB object if found, None otherwise
def get_user(email: str, db: Session):
    
    user: UsrInDB = db.get(User, {"email": email})
    
    return user
