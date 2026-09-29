from fastapi import APIRouter, Depends, HTTPException
from auth import verify_api_key
from models.user import User, CreateUser, ReadUser
from sqlmodel import Session, select
from database import get_session

router = APIRouter(prefix='/users', tags=['users'])

@router.post('/',response_model=ReadUser)
def create_user(
    user_data: CreateUser,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    existing_data = select(User).where(User.email == user_data.email)
    if existing_data:
        raise HTTPException(status_code=400, detail='Entered email is already registered')

    user = User(**user_data.model_dump())

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get('/',response_model=list[ReadUser])
def get_user(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users