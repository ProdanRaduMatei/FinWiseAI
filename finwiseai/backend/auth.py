from fastapi import APIRouter, HTTPException, Header, Depends, Request
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
from firebase_config import auth as firebase_auth

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

@auth_router.post("/oauth/google")
def google_oauth(request: Request):
    data = request.json()
    id_token = data.get("idToken")

    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        email = decoded_token["email"]
        name = decoded_token.get("name", "Google User")

        # Optional: store user in DB if not exists
        user = users_collection.find_one({"email": email})
        if not user:
            users_collection.insert_one({
                "email": email,
                "name": name,
                "googleAuth": True
            })

        access_token = create_access_token(email)
        return {"access_token": access_token}

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Google ID token")

@auth_router.post("/google-login")
def google_login(id_token: str):
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        email = decoded_token["email"]
        name = decoded_token.get("name", "No Name")

        # Check if user exists
        user_doc = users_collection.find_one({"email": email})
        if not user_doc:
            users_collection.insert_one({
                "email": email,
                "name": name,
                "passwordHash": None  # Not used for Google auth
            })

        # Issue local JWT access token
        access_token = create_access_token(email)
        refresh_token = create_refresh_token(email)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "email": email,
            "name": name
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid Google token: {str(e)}")

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

        try:
            payload = decode_token(token)
            email = payload["sub"]
        except:
            # Not a local JWT, try Firebase
            decoded = firebase_auth.verify_id_token(token)
            email = decoded["email"]

        user = users_collection.find_one({"email": email}, {"passwordHash": 0})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user["_id"] = str(user["_id"])
        return user

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or missing token")