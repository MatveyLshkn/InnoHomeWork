
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from . import models, schemas, auth
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JSONPlaceholder API",
    description="A RESTful API that replicates JSONPlaceholder with JWT authentication",
    version="1.0.0"
)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user with hashed password
    db_user = models.User(
        name=user.name,
        username=user.username,
        email=user.email,
        password_hash=auth.get_password_hash(user.password),
        phone=user.phone,
        website=user.website
    )
    
    # Create address
    address = models.Address(
        street=user.address.street,
        suite=user.address.suite,
        city=user.address.city,
        zipcode=user.address.zipcode
    )
    
    # Create geo
    geo = models.Geo(
        lat=user.address.geo.lat,
        lng=user.address.geo.lng
    )
    address.geo = geo
    db_user.address = address
    
    # Create company
    company = models.Company(
        name=user.company.name,
        catchPhrase=user.company.catchPhrase,
        bs=user.company.bs
    )
    db_user.company = company
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields
    for key, value in user.dict(exclude={'password'}).items():
        if key not in ['address', 'company']:
            setattr(db_user, key, value)
    
    # Update address
    if db_user.address:
        for key, value in user.address.dict(exclude={'geo'}).items():
            setattr(db_user.address, key, value)
        # Update geo
        if db_user.address.geo:
            for key, value in user.address.geo.dict().items():
                setattr(db_user.address.geo, key, value)
    
    # Update company
    if db_user.company:
        for key, value in user.company.dict().items():
            setattr(db_user.company, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"} 