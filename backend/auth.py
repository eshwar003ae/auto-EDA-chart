from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from models import User

router = APIRouter()

# Secure password handling context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory user storage for this example (replace with a real database)
users_db = {}

# JWT secret key and algorithm
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Utility function to create a JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoint for user registration
@router.post("/register")
async def register_user(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    users_db[user.email] = {"email": user.email, "hashed_password": hashed_password}

    return {"message": "User registered successfully"}

# Endpoint for user login
@router.post("/login")
async def login_user(user: User):
    user_in_db = users_db.get(user.email)
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not pwd_context.verify(user.password, user_in_db["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}