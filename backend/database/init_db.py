from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL
import asyncio

async def init_database():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.user_management
    
    # 创建集合和索引
    
    # 用户集合
    await db.create_collection("users")
    await db.users.create_index("phone", unique=True, sparse=True)
    await db.users.create_index("email", unique=True, sparse=True)
    
    # 验证码集合
    await db.create_collection("verify_codes")
    await db.verify_codes.create_index("phone")
    await db.verify_codes.create_index("expire_time", expireAfterSeconds=300)  # 5分钟后自动删除
    
    # 用户角色集合
    await db.create_collection("roles")
    await db.roles.create_index("role_name", unique=True)
    
    # 权限集合
    await db.create_collection("permissions")
    await db.permissions.create_index("permission_name", unique=True)
    
    # 用户-角色关联集合
    await db.create_collection("user_roles")
    await db.user_roles.create_index([("user_id", 1), ("role_id", 1)], unique=True)
    
    # 角色-权限关联集合
    await db.create_collection("role_permissions")
    await db.role_permissions.create_index([("role_id", 1), ("permission_id", 1)], unique=True)
    
    # 用户登录历史记录
    await db.create_collection("login_history")
    await db.login_history.create_index("user_id")
    await db.login_history.create_index("login_time")
    
    # 调研集合
    await db.create_collection("research")
    await db.research.create_index("user_id")
    await db.research.create_index("research_type")
    
    # 决策集合
    await db.create_collection("decisions")
    await db.decisions.create_index("user_id")
    await db.decisions.create_index("research_id")
    
    # 目标集合
    await db.create_collection("goals")
    await db.goals.create_index("user_id")
    await db.goals.create_index([("status", 1), ("category", 1)])
    await db.goals.create_index("end_date")  # 用于查询即将到期的目标

    print("数据库初始化完成")

# 初始化基础数据
async def init_base_data():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.user_management
    
    # 创建基础角色
    base_roles = [
        {
            "role_name": "admin",
            "description": "系统管理员",
            "create_time": datetime.now()
        },
        {
            "role_name": "user",
            "description": "普通用户",
            "create_time": datetime.now()
        }
    ]
    
    for role in base_roles:
        await db.roles.update_one(
            {"role_name": role["role_name"]},
            {"$setOnInsert": role},
            upsert=True
        )
    
    # 创建基础权限
    base_permissions = [
        {
            "permission_name": "user:view",
            "description": "查看用户信息",
            "create_time": datetime.now()
        },
        {
            "permission_name": "user:edit",
            "description": "编辑用户信息",
            "create_time": datetime.now()
        },
        {
            "permission_name": "user:delete",
            "description": "删除用户",
            "create_time": datetime.now()
        },
        {
            "permission_name": "role:manage",
            "description": "角色管理",
            "create_time": datetime.now()
        }
    ]
    
    for permission in base_permissions:
        await db.permissions.update_one(
            {"permission_name": permission["permission_name"]},
            {"$setOnInsert": permission},
            upsert=True
        )

    print("基础数据初始化完成")

if __name__ == "__main__":
    asyncio.run(init_database())
    asyncio.run(init_base_data()) 