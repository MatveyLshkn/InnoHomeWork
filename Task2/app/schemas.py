from pydantic import BaseModel, EmailStr
from typing import Optional

class GeoBase(BaseModel):
    lat: str
    lng: str

class AddressBase(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoBase

class CompanyBase(BaseModel):
    name: str
    catchPhrase: str
    bs: str

class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone: str
    website: str
    address: AddressBase
    company: CompanyBase

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 