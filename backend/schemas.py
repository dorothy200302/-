from pydantic import BaseModel
from typing import Optional, Dict, Any

class LoginRequest(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    verify_code: Optional[str] = None
    password: Optional[str] = None

class RegisterRequest(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    nickname: str
    avatar_url: str
    password: str

class SmsRequest(BaseModel):
    phone: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_info: Dict[str, Any]

class RegisterResponse(BaseModel):
    success: bool
    user_id: str

class BaseResponse(BaseModel):
    success: bool 