from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User, UserInDB, SignUpForm
from app.helper.auth import verify_password, get_password_hash, \
                            create_access_token
from app.helper.auth import get_current_user
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.helper.database import db, UserExistsException, UserNotFoundException


fake_users_db = {
    "gianafrancisco@gmail.com": {
        "username": "gianafrancisco@gmail.com",
        "first_name": "Francisco",
        "last_name": "Giana",
        "email": "gianafrancisco@gmail.com",
        "hashed_password": get_password_hash("secret"),
        "disabled": False,
    }
}

db.add(UserInDB(**fake_users_db.get('gianafrancisco@gmail.com')))

router = APIRouter()


async def get_current_active_user(
        current_user: User = Depends(get_current_user)
        ):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/auth/signin")
async def signin_users(form_data: OAuth2PasswordRequestForm = Depends()):
    user: User = None
    try:
        user = db.get(form_data.username)
    except UserNotFoundException:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/me")
async def read_users_me(current_user: UserInDB = Depends(
        get_current_active_user)):
    user = User(**current_user.dict())
    return user


@router.post("/auth/signup")
async def signup_users(form_data: SignUpForm = Depends()):
    user = {
        "username": form_data.email,
        "email": form_data.email,
        "first_name": form_data.first_name,
        "last_name": form_data.last_name,
        "hashed_password": get_password_hash(form_data.password),
        "disabled": False,
    }
    try:
        db.add(UserInDB(**user))
    except UserExistsException:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {}


@router.post("/auth/logout")
async def logout_users():
    # TODO: Implement logout
    return {}
