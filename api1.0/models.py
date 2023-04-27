from pydantic import BaseModel


class SignupModel(BaseModel):
    name: str
    email: str
    phonenumber: str
    password: str
    isActive: str = False


class LoginModel(BaseModel):
    name: str
    password: str
