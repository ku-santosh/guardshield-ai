from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.core.config import settings
from backend.app.core.security import verify_password, create_access_token
from backend.app.repositories.base import get_db_session
from backend.app.repositories.mock_repo import MockUserRepository
from backend.app.models.domain import DBUser
from backend.app.models.schemas import Token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db_session)):
    user = None
    if settings.USE_DATABASE and db:
        result = await db.execute(select(DBUser).where(DBUser.email == form_data.username))
        user = result.scalars().first()
    else:
        user = await MockUserRepository.get_mock_user_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect email authentication payload context."
        )
        
    access_token = create_access_token(data={"sub": user.email, "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role.value}