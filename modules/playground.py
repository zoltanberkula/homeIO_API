from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

app = FastAPI()

# Define your secret key and token expiration time
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Example user model
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

# Example of users (normally this would be in a database)
users_db = {
    "user1": User(username="user1", password="$2b$12$7c3c.dchVf1pUugFmxyvCuI0gYl4A0Ie1dxmT7Hrs8.aJdQnJ6SLK"),  # Hashed password: "password1"
    "user2": User(username="user2", password="$2b$12$2yM6szk1ey.HUc7OW2YXNOGQc9d5.T5BVaW7k8cwqPhNGFT7kTsNu"),  # Hashed password: "password2"
}

# Hash passwords using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define a function to authenticate users
def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if user and pwd_context.verify(password, user.password):
        return user

# Define a function to create access tokens
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Define OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Endpoint for user login and token generation
@app.post("/token")
def login_for_access_token(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Protected endpoint that requires authentication
@app.get("/protected")
def protected_route(current_user: User = Depends(oauth2_scheme)):
    return {"message": f"Welcome, {current_user.username}! You accessed a protected route."}
