from datetime import timedelta
import bcrypt
from fastapi import APIRouter, Depends
from sqlmodel import select
from db import get_session, Session
from models import UserCredentials, UserNewCredentials, Users
from dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token



router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(credentials_to_login: UserCredentials, session: Session = Depends(get_session)):
    statement = select(Users).where(Users.email == credentials_to_login.email)
    user_from_query = session.exec(statement).one()

    if bcrypt.checkpw(credentials_to_login.password.encode(), user_from_query.password.encode()):
        
        # token gen
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": credentials_to_login.email}, expires_delta=access_token_expires
            )
        return {"access_token": access_token, "token_type": "bearer"}
    
    else:
        return False

@router.post("/recovery")
async def recovery(credentials_update: UserNewCredentials, session: Session = Depends(get_session)):
    statement = select(Users).where(Users.id == credentials_update.id)
    user_from_query = session.exec(statement).one()
    if credentials_update.confirmpassword == credentials_update.newpassword:
        if bcrypt.checkpw(credentials_update.oldpassword.encode(), user_from_query.password.encode()):
            hashed = bcrypt.hashpw(credentials_update.newpassword.encode(),bcrypt.gensalt())
            user_from_query.password = hashed.decode()
            try:
                session.add(user_from_query)
                session.commit()
                return True
            except Exception as e:
                session.rollback()

                return False
            finally:
                session.close()
        else:
            return False
    else:
        False
