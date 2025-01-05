from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL

client = AsyncIOMotorClient(MONGODB_URL)
db = client.user_management

# 获取集合
users = db.users
verify_codes = db.verify_codes
roles = db.roles
permissions = db.permissions
user_roles = db.user_roles
role_permissions = db.role_permissions
login_history = db.login_history 