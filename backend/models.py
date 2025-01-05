from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    phone: Optional[str] = None
    email: Optional[str] = None
    nickname: str
    avatar_url: str
    password: str
    create_time: datetime
    update_time: datetime
    last_login_time: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class VerifyCode(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    phone: str
    code: str
    create_time: datetime
    expire_time: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Role(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    role_name: str
    description: str
    create_time: datetime
    update_time: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Permission(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    permission_name: str
    description: str
    create_time: datetime
    update_time: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserRole(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    role_id: PyObjectId
    create_time: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class RolePermission(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    role_id: PyObjectId
    permission_id: PyObjectId
    create_time: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class LoginHistory(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    login_time: datetime
    login_ip: str
    device_info: str
    login_type: str  # "phone", "email"
    status: str  # "success", "failed"
    fail_reason: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Research(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    title: str
    description: str
    research_type: str  # market, user, competitor, etc.
    status: str  # draft, in_progress, completed
    data_sources: List[str]
    findings: Dict[str, Any]
    create_time: datetime
    update_time: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Decision(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    research_id: Optional[PyObjectId]
    title: str
    description: str
    options: List[Dict[str, Any]]
    criteria: List[Dict[str, Any]]
    analysis: Dict[str, Any]
    final_decision: Optional[str]
    status: str  # draft, analyzing, completed
    create_time: datetime
    update_time: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Goal(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    title: str
    description: str
    category: str  # personal, career, health, etc.
    priority: int  # 1-5
    status: str  # draft, active, completed, cancelled
    start_date: datetime
    end_date: datetime
    progress: float  # 0-100
    smart_criteria: Dict[str, Any]  # specific, measurable, achievable, relevant, time-bound
    milestones: List[Dict[str, Any]]
    create_time: datetime
    update_time: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str} 