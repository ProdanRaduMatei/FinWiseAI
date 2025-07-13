from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    email: EmailStr
    name: str
    password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str