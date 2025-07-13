from fastapi import APIRouter, HTTPException, Depends, Header
from models import RegisterUser, LoginUser
from db import users_collection
from utils import hash_password, verify_password, create_token, decode_token

auth_router = APIRouter(prefix="/api", tags=["Auth"])

@auth_router.post("/register")
def register(user: RegisterUser):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    user_doc = {
        "email": user.email,
        "name": user.name,
        "passwordHash": hashed
    }
    users_collection.insert_one(user_doc)
    return {"message": "User registered successfully"}

@auth_router.post("/login")
def login(user: LoginUser):
    user_doc = users_collection.find_one({"email": user.email})
    if not user_doc or not verify_password(user.password, user_doc["passwordHash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user.email)
    return {"access_token": token}

@auth_router.get("/user")
def get_user(Authorization: str = Header(...)):
    try:
        scheme, token = Authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError
        payload = decode_token(token)
        email = payload["sub"]
        user = users_collection.find_one({"email": email}, {"passwordHash": 0})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user["_id"] = str(user["_id"])
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid or missing token")