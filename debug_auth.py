from dotenv import load_dotenv
import os

load_dotenv()

print("SECRET_KEY:", os.getenv("SECRET_KEY"))
print("ALGORITHM:", os.getenv("ALGORITHM"))
print("ACCESS_TOKEN_EXPIRE_MINUTES:", os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Test token creation and verification
from auth import create_token, verify_token
from fastapi import HTTPException

token = create_token({"user": "admin"})
print("\nGenerated Token:", token)

# Try to decode it manually
from jose import jwt
try:
    payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
    print("Decoded payload:", payload)
except Exception as e:
    print("Error decoding:", e)
