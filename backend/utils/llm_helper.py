from typing import List, Dict, Any
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class LLMHelper:
    @staticmethod
    async def analyze_text(text: str, prompt: str) -> str:
        """使用LLM分析文本"""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM分析错误: {str(e)}")
            return ""

    @staticmethod
    async def generate_research_focus(topic: str) -> List[str]:
        """生成研究重点"""
        prompt = f"""
        针对主题"{topic}"，请生成5-7个关键的研究重点。
        要求：
        1. 覆盖市场、用户、竞争、技术等维度
        2. 具体且可操作
        3. 每个重点用简短的短语表达
        请直接列出重点，每行一个。
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是一个专业的研究分析师"},
                    {"role": "user", "content": prompt}
                ]
            )
            focus_areas = response.choices[0].message.content.strip().split('\n')
            return [area.strip('- ') for area in focus_areas]
        except Exception as e:
            print(f"生成研究重点错误: {str(e)}")
            return []

    @staticmethod
    async def analyze_decision_criteria(options: List[Dict], criteria: List[Dict]) -> Dict[str, Any]:
        """分析决策选项和标准"""
        prompt = f"""
        请分析以下决策选项和标准，提供专业的决策建议。

        决策选项：
        {options}

        决策标准：
        {criteria}

        请提供：
        1. 每个选项的优缺点分析
        2. 各标准的重要性评估
        3. 最终建议和理由
        4. 潜在风险提示
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是一个专业的决策分析顾问"},
                    {"role": "user", "content": prompt}
                ]
            )
            return {
                "analysis": response.choices[0].message.content,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"决策分析错误: {str(e)}")
            return {} 