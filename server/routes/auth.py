from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from bson import ObjectId
import secrets

import sys
sys.path.append('..')

from database import get_database
from models.user import UserCreate, UserLogin, UserResponse, Token
from utils.password import hash_password, verify_password
from utils.jwt import create_access_token
from utils.email import GmailService

router = APIRouter(prefix="/auth", tags=["Authentication"])
gmail_service = GmailService()

@router.post("/signup")
async def signup(user_data: UserCreate):
    db = get_database()
    
    # Check if email already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = await db.users.find_one({"username": user_data.username})
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Generate verification token
    verification_token = secrets.token_urlsafe(32)
    
    # Create user document
    user_doc = {
        "name": user_data.name,
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hash_password(user_data.password),
        "auth_provider": "local",
        "is_verified": False,
        "verification_token": verification_token,
        "created_at": datetime.utcnow()
    }
    
    await db.users.insert_one(user_doc)
    
    # Send verification email
    email_sent = gmail_service.send_verification_email(user_data.email, verification_token)
    
    if not email_sent:
        # Note: You might want to rollback user creation or mark as failed here
        # For now, we'll just return a message
        print("Failed to send verification email")
    
    return {"message": "Signup successful! Please check your email to verify your account."}

@router.post("/verify/{token}")
async def verify_email(token: str):
    db = get_database()
    
    user = await db.users.find_one({"verification_token": token})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
        
    await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"is_verified": True}, "$unset": {"verification_token": ""}}
    )
    
    return {"message": "Email verified successfully! You can now log in."}

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    db = get_database()
    
    # Find user by email
    user = await db.users.find_one({"email": credentials.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check verification status
    if not user.get("is_verified", False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please verify your email address before logging in."
        )
    
    # Verify password
    if not user.get("hashed_password") or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create response
    user_response = UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        username=user["username"],
        email=user["email"],
        is_verified=user.get("is_verified", True),
        created_at=user["created_at"],
        auth_provider=user.get("auth_provider", "local")
    )
    
    # Generate token
    access_token = create_access_token({"sub": str(user["_id"])})
    
    return Token(access_token=access_token, user=user_response)
