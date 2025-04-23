from fastapi import APIRouter, Depends
from sqlmodel import select
from db import get_session, Session
from models import UserUpdate, Users
import bcrypt

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register")
async def create_user(new_user: Users, session: Session = Depends(get_session)):
    try:
        hashed_password = bcrypt.hashpw(new_user.password.encode(), bcrypt.gensalt())
        new_user.password = hashed_password.decode()
        session.add(new_user)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()

@router.post("")
async def update_user(user_new_data: UserUpdate, session: Session = Depends(get_session)):
    try:
        statement = select(Users).where(Users.id == user_new_data.id)
        user_to_update = session.exec(statement).one()
        user_to_update.id = user_new_data.id
        user_to_update.name = user_new_data.name
        user_to_update.lname = user_new_data.lname
        user_to_update.email = user_new_data.email
        session.add(user_to_update)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()

