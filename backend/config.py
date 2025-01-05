import os

# MongoDB配置
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

# JWT配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 短信服务配置
SMS_ACCESS_KEY = os.getenv("SMS_ACCESS_KEY", "")
SMS_SECRET_KEY = os.getenv("SMS_SECRET_KEY", "")
SMS_SIGN_NAME = os.getenv("SMS_SIGN_NAME", "")
SMS_TEMPLATE_CODE = os.getenv("SMS_TEMPLATE_CODE", "")

# OpenAI配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# 数据分析配置
ANALYSIS_CONFIG = {
    'min_data_points': 10,
    'max_clusters': 5,
    'sentiment_threshold': 0.5
}

# 风险评估配置
RISK_CONFIG = {
    'probability_threshold': 0.7,
    'impact_threshold': 0.6,
    'risk_matrix': {
        'high': {'color': 'red', 'score_range': (0.6, 1.0)},
        'medium': {'color': 'yellow', 'score_range': (0.3, 0.6)},
        'low': {'color': 'green', 'score_range': (0, 0.3)}
    }
} 