from fastapi import APIRouter, HTTPException, Header, Depends
from models import RegisterUser, LoginUser
from db import users_collection
from utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from datetime import datetime

auth_router = APIRouter(prefix="/api", tags=["Auth"])


@auth_router.post("/register")
def register(user: RegisterUser):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    user_doc = {
        "email": user.email,
        "name": user.name,
        "passwordHash": hashed,
        "createdAt": datetime.utcnow()
    }
    users_collection.insert_one(user_doc)
    return {"message": "User registered successfully"}


@auth_router.post("/login")
def login(user: LoginUser):
    user_doc = users_collection.find_one({"email": user.email})
    if not user_doc or not verify_password(user.password, user_doc["passwordHash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@auth_router.post("/refresh")
def refresh_token(Authorization: str = Header(...)):
    try:
        scheme, token = Authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError
        payload = decode_token(token, token_type="refresh")
        email = payload["sub"]
        # Optionally, check if user still exists
        if not users_collection.find_one({"email": email}):
            raise HTTPException(status_code=404, detail="User not found")
        new_access_token = create_access_token(email)
        return {"access_token": new_access_token}
    except:
        raise HTTPException(status_code=401, detail="Invalid or missing refresh token")


@auth_router.get("/user")
def get_user(Authorization: str = Header(...)):
    try:
        scheme, token = Authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError
        payload = decode_token(token, token_type="access")
        email = payload["sub"]
        user = users_collection.find_one({"email": email}, {"passwordHash": 0})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user["_id"] = str(user["_id"])
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid or missing token")