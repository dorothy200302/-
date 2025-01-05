from fastapi import FastAPI, HTTPException, Depends, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import jwt
from models import *
from database import *
from schemas import *
import random
from utils.sms import send_sms
from utils.encrypt import encrypt_password
from typing import List, Dict, Any
from utils.research_assistant import ResearchAssistant
from utils.decision_support import DecisionSupport, DecisionOption, DecisionCriterion

app = FastAPI()

# 配置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT配置
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 用户登录
@app.post("/api/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    # 验证手机号登录
    if login_data.phone:
        # 验证验证码
        verify_code = await VerifyCode.find_one({
            "phone": login_data.phone,
            "code": login_data.verify_code,
            "expire_time": {"$gt": datetime.now()}
        })
        if not verify_code:
            raise HTTPException(status_code=400, detail="验证码无效或已过期")
        
        user = await User.find_one({"phone": login_data.phone})
    
    # 验证邮箱登录
    elif login_data.email:
        user = await User.find_one({"email": login_data.email})
        if not user or user.password != encrypt_password(login_data.password):
            raise HTTPException(status_code=400, detail="邮箱或密码错误")
    
    else:
        raise HTTPException(status_code=400, detail="请提供手机号或邮箱")

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 生成token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # 更新用户登录时间
    await User.update_one(
        {"_id": user.id},
        {"$set": {"last_login_time": datetime.now()}}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": user.dict(exclude={"password"})
    }

# 用户注册
@app.post("/api/register", response_model=RegisterResponse)
async def register(register_data: RegisterRequest):
    # 检查用户是否已存在
    existing_user = await User.find_one({
        "$or": [
            {"phone": register_data.phone},
            {"email": register_data.email}
        ]
    })
    if existing_user:
        raise HTTPException(status_code=400, detail="该手机号或邮箱已被注册")

    # 创建新用户
    user = User(
        phone=register_data.phone,
        email=register_data.email,
        nickname=register_data.nickname,
        avatar_url=register_data.avatar_url,
        password=encrypt_password(register_data.password),
        create_time=datetime.now(),
        update_time=datetime.now()
    )
    
    result = await user.insert()

    return {
        "success": True,
        "user_id": str(result.inserted_id)
    }

# 发送验证码
@app.post("/api/send-sms-code", response_model=BaseResponse)
async def send_sms_code(sms_request: SmsRequest):
    # 生成6位随机验证码
    code = ''.join(random.choices('0123456789', k=6))
    
    # 保存验证码
    verify_code = VerifyCode(
        phone=sms_request.phone,
        code=code,
        create_time=datetime.now(),
        expire_time=datetime.now() + timedelta(minutes=5)
    )
    await verify_code.insert()

    # 发送短信
    try:
        await send_sms(sms_request.phone, code)
    except Exception as e:
        raise HTTPException(status_code=500, detail="短信发送失败")

    return {"success": True}

# 生成JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 验证token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="无效的认证信息")
    except JWTError:
        raise HTTPException(status_code=401, detail="无效的认证信息")
        
    user = await User.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
        
    return user 

# 调研相关API
@app.post("/api/research", response_model=Research)
async def create_research(research: Research, current_user: User = Depends(get_current_user)):
    research.user_id = current_user.id
    research.create_time = datetime.now()
    research.update_time = datetime.now()
    result = await db.research.insert_one(research.dict(by_alias=True))
    return await db.research.find_one({"_id": result.inserted_id})

@app.get("/api/research/{research_id}", response_model=Research)
async def get_research(research_id: str, current_user: User = Depends(get_current_user)):
    research = await db.research.find_one({
        "_id": ObjectId(research_id),
        "user_id": current_user.id
    })
    if not research:
        raise HTTPException(status_code=404, detail="Research not found")
    return research

# 决策相关API
@app.post("/api/decisions", response_model=Decision)
async def create_decision(decision: Decision, current_user: User = Depends(get_current_user)):
    decision.user_id = current_user.id
    decision.create_time = datetime.now()
    decision.update_time = datetime.now()
    
    # 使用GPT-4分析决策选项
    analysis = await analyze_decision_options(decision.options, decision.criteria)
    decision.analysis = analysis
    
    result = await db.decisions.insert_one(decision.dict(by_alias=True))
    return await db.decisions.find_one({"_id": result.inserted_id})

@app.get("/api/decisions/{decision_id}", response_model=Decision)
async def get_decision(decision_id: str, current_user: User = Depends(get_current_user)):
    decision = await db.decisions.find_one({
        "_id": ObjectId(decision_id),
        "user_id": current_user.id
    })
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision

# 目标相关API
@app.post("/api/goals", response_model=Goal)
async def create_goal(goal: Goal, current_user: User = Depends(get_current_user)):
    # 验证SMART目标
    if not validate_smart_goal(goal.smart_criteria):
        raise HTTPException(status_code=400, detail="Goal does not meet SMART criteria")
    
    goal.user_id = current_user.id
    goal.create_time = datetime.now()
    goal.update_time = datetime.now()
    
    # 自动生成里程碑
    goal.milestones = await generate_milestones(goal)
    
    result = await db.goals.insert_one(goal.dict(by_alias=True))
    return await db.goals.find_one({"_id": result.inserted_id})

@app.get("/api/goals/{goal_id}", response_model=Goal)
async def get_goal(goal_id: str, current_user: User = Depends(get_current_user)):
    goal = await db.goals.find_one({
        "_id": ObjectId(goal_id),
        "user_id": current_user.id
    })
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

@app.put("/api/goals/{goal_id}/progress", response_model=Goal)
async def update_goal_progress(
    goal_id: str,
    progress: float = Body(...),
    current_user: User = Depends(get_current_user)
):
    if not 0 <= progress <= 100:
        raise HTTPException(status_code=400, detail="Progress must be between 0 and 100")
    
    result = await db.goals.update_one(
        {"_id": ObjectId(goal_id), "user_id": current_user.id},
        {"$set": {"progress": progress, "update_time": datetime.now()}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    return await db.goals.find_one({"_id": ObjectId(goal_id)})

# 辅助函数
async def analyze_decision_options(options: List[dict], criteria: List[dict]) -> dict:
    """使用GPT-4分析决策选项"""
    # TODO: 实现GPT-4分析逻辑
    return {
        "recommendations": [],
        "analysis": {},
        "scores": {}
    }

def validate_smart_goal(smart_criteria: dict) -> bool:
    """验证目标是否符合SMART原则"""
    required_fields = ["specific", "measurable", "achievable", "relevant", "time_bound"]
    return all(field in smart_criteria for field in required_fields)

async def generate_milestones(goal: Goal) -> List[dict]:
    """自动生成目标里程碑"""
    total_days = (goal.end_date - goal.start_date).days
    num_milestones = max(3, total_days // 30)  # 至少3个里程碑，或每30天一个
    
    milestones = []
    for i in range(num_milestones):
        milestone_date = goal.start_date + timedelta(days=(total_days * (i + 1) // num_milestones))
        milestones.append({
            "title": f"Milestone {i + 1}",
            "description": f"Auto-generated milestone {i + 1}",
            "due_date": milestone_date,
            "progress": 0,
            "status": "pending"
        })
    
    return milestones 

# 创建调研
@app.post("/api/research/auto", response_model=Dict[str, Any])
async def create_auto_research(
    research_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """自动执行调研"""
    assistant = ResearchAssistant()
    results = await assistant.start_research(
        topic=research_data["title"],
        focus_areas=research_data.get("focus_areas")
    )
    
    # 保存调研结果
    research = Research(
        user_id=current_user.id,
        title=research_data["title"],
        description=research_data.get("description", ""),
        research_type=research_data["research_type"],
        status="completed",
        data_sources=results["data_sources"],
        findings=results["findings"],
        summary=results["summary"],
        create_time=datetime.now(),
        update_time=datetime.now()
    )
    
    result = await db.research.insert_one(research.dict())
    return {
        "success": True,
        "research_id": str(result.inserted_id),
        "results": results
    }

# 分析决策
@app.post("/api/decisions/analyze", response_model=Dict[str, Any])
async def analyze_decision(
    decision_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """分析决策并提供建议"""
    support = DecisionSupport()
    
    # 添加决策标准
    for criterion in decision_data["criteria"]:
        support.add_criterion(DecisionCriterion(
            name=criterion["name"],
            weight=criterion["weight"],
            description=criterion.get("description", "")
        ))
    
    # 添加决策选项
    for option in decision_data["options"]:
        support.add_option(DecisionOption(
            title=option["title"],
            description=option["description"],
            pros=option.get("pros", []),
            cons=option.get("cons", []),
            criteria_scores=option["criteria_scores"]
        ))
    
    # 执行决策分析
    analysis = support.analyze_decision()
    
    # 保存决策记录
    decision = Decision(
        user_id=current_user.id,
        title=decision_data["title"],
        description=decision_data["description"],
        options=decision_data["options"],
        criteria=decision_data["criteria"],
        analysis=analysis,
        status="completed",
        create_time=datetime.now(),
        update_time=datetime.now()
    )
    
    result = await db.decisions.insert_one(decision.dict())
    return {
        "success": True,
        "decision_id": str(result.inserted_id),
        "analysis": analysis
    } 