from typing import List, Dict, Any
from dataclasses import dataclass
import numpy as np

@dataclass
class RiskFactor:
    name: str
    probability: float  # 0-1
    impact: float      # 0-1
    description: str
    mitigation: str

class RiskAssessor:
    def __init__(self):
        self.risk_levels = {
            'low': (0, 0.3),
            'medium': (0.3, 0.6),
            'high': (0.6, 1.0)
        }
        
    def assess_risks(self, risk_factors: List[RiskFactor]) -> Dict[str, Any]:
        """评估风险"""
        assessments = []
        
        for factor in risk_factors:
            # 计算风险分数
            risk_score = factor.probability * factor.impact
            
            # 确定风险等级
            risk_level = self.determine_risk_level(risk_score)
            
            assessment = {
                'factor': factor.name,
                'score': risk_score,
                'level': risk_level,
                'probability': factor.probability,
                'impact': factor.impact,
                'description': factor.description,
                'mitigation': factor.mitigation
            }
            assessments.append(assessment)
            
        # 整体风险评估
        overall_assessment = self.calculate_overall_risk(assessments)
        
        return {
            'risk_factors': assessments,
            'overall_assessment': overall_assessment
        }
        
    def determine_risk_level(self, score: float) -> str:
        """确定风险等级"""
        for level, (min_score, max_score) in self.risk_levels.items():
            if min_score <= score < max_score:
                return level
        return 'high'
        
    def calculate_overall_risk(self, assessments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """计算整体风险"""
        scores = [a['score'] for a in assessments]
        
        overall = {
            'average_score': np.mean(scores),
            'max_score': max(scores),
            'risk_level': self.determine_risk_level(np.mean(scores)),
            'high_risk_count': sum(1 for a in assessments if a['level'] == 'high'),
            'medium_risk_count': sum(1 for a in assessments if a['level'] == 'medium'),
            'low_risk_count': sum(1 for a in assessments if a['level'] == 'low')
        }
        
        return overall 