from datetime import timedelta
import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select
from db import get_session, Session
from models.users import UserCredentials, UserNewCredentials, Users,  UserInfo
from dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, decode_access_token


scheme = HTTPBearer()

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(credentials_to_login: UserCredentials, session: Session = Depends(get_session)):
    statement = select(Users).where(Users.email == credentials_to_login.email)
    user_from_query = session.exec(statement).one()

    if bcrypt.checkpw(credentials_to_login.password.encode(), user_from_query.password.encode()):
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": credentials_to_login.email}, expires_delta=access_token_expires
            )
        return {"access_token": access_token, "token_type": "bearer"}
    
    else:
        raise HTTPException(status_code=404)

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

@router.get('/me')
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(scheme), session: Session = Depends(get_session)):
    decoded_sub = decode_access_token(credentials.credentials)
    try:
        statement = select(Users.id, Users.email, Users.name, Users.lname).where(Users.email == decoded_sub)
        result = session.exec(statement).one()
        id, email, name, lname = result
        if result:
            return UserInfo(id=id,email=email,name=name,lname=lname)
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

    except Exception as e:
        session.rollback()
        return None

