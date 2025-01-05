from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from models import *
from database import db

class UserCRUD:
    @staticmethod
    async def create_user(user_data: dict) -> str:
        result = await db.users.insert_one(user_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[dict]:
        return await db.users.find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    async def get_user_roles(user_id: str) -> List[dict]:
        pipeline = [
            {"$match": {"user_id": ObjectId(user_id)}},
            {
                "$lookup": {
                    "from": "roles",
                    "localField": "role_id",
                    "foreignField": "_id",
                    "as": "role"
                }
            },
            {"$unwind": "$role"}
        ]
        return await db.user_roles.aggregate(pipeline).to_list(None)

class RoleCRUD:
    @staticmethod
    async def create_role(role_data: dict) -> str:
        result = await db.roles.insert_one(role_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_role_permissions(role_id: str) -> List[dict]:
        pipeline = [
            {"$match": {"role_id": ObjectId(role_id)}},
            {
                "$lookup": {
                    "from": "permissions",
                    "localField": "permission_id",
                    "foreignField": "_id",
                    "as": "permission"
                }
            },
            {"$unwind": "$permission"}
        ]
        return await db.role_permissions.aggregate(pipeline).to_list(None)

class LoginHistoryCRUD:
    @staticmethod
    async def add_login_record(login_data: dict) -> str:
        result = await db.login_history.insert_one(login_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_user_login_history(user_id: str, limit: int = 10) -> List[dict]:
        return await db.login_history.find(
            {"user_id": ObjectId(user_id)}
        ).sort("login_time", -1).limit(limit).to_list(None) 

class ResearchCRUD:
    @staticmethod
    async def create_research(research_data: dict) -> str:
        result = await db.research.insert_one(research_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_user_research(user_id: str, limit: int = 10) -> List[dict]:
        return await db.research.find(
            {"user_id": ObjectId(user_id)}
        ).sort("create_time", -1).limit(limit).to_list(None)

class DecisionCRUD:
    @staticmethod
    async def create_decision(decision_data: dict) -> str:
        result = await db.decisions.insert_one(decision_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_user_decisions(user_id: str, limit: int = 10) -> List[dict]:
        return await db.decisions.find(
            {"user_id": ObjectId(user_id)}
        ).sort("create_time", -1).limit(limit).to_list(None)

class GoalCRUD:
    @staticmethod
    async def create_goal(goal_data: dict) -> str:
        result = await db.goals.insert_one(goal_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_user_goals(
        user_id: str,
        status: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 10
    ) -> List[dict]:
        query = {"user_id": ObjectId(user_id)}
        if status:
            query["status"] = status
        if category:
            query["category"] = category
            
        return await db.goals.find(query).sort("create_time", -1).limit(limit).to_list(None)
    
    @staticmethod
    async def update_goal_progress(goal_id: str, progress: float) -> bool:
        result = await db.goals.update_one(
            {"_id": ObjectId(goal_id)},
            {"$set": {"progress": progress, "update_time": datetime.now()}}
        )
        return result.modified_count > 0 