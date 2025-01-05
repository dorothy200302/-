from typing import List, Dict, Any
import numpy as np
from dataclasses import dataclass

@dataclass
class DecisionOption:
    title: str
    description: str
    pros: List[str]
    cons: List[str]
    criteria_scores: Dict[str, float]

@dataclass
class DecisionCriterion:
    name: str
    weight: float
    description: str

class DecisionSupport:
    def __init__(self):
        self.options: List[DecisionOption] = []
        self.criteria: List[DecisionCriterion] = []
    
    def add_option(self, option: DecisionOption):
        """添加决策选项"""
        self.options.append(option)
    
    def add_criterion(self, criterion: DecisionCriterion):
        """添加决策标准"""
        self.criteria.append(criterion)
    
    def analyze_decision(self) -> Dict[str, Any]:
        """分析决策并提供建议"""
        if not self.options or not self.criteria:
            raise ValueError("需要至少一个选项和标准")
        
        # 计算加权得分
        scores = self._calculate_weighted_scores()
        
        # 排序选项
        ranked_options = self._rank_options(scores)
        
        # 生成分析报告
        return self._generate_analysis_report(ranked_options)
    
    def _calculate_weighted_scores(self) -> Dict[str, float]:
        """计算每个选项的加权得分"""
        scores = {}
        
        for option in self.options:
            total_score = 0
            for criterion in self.criteria:
                if criterion.name in option.criteria_scores:
                    score = option.criteria_scores[criterion.name]
                    weighted_score = score * criterion.weight
                    total_score += weighted_score
            scores[option.title] = total_score
            
        return scores
    
    def _rank_options(self, scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """对选项进行排序"""
        ranked = [
            {
                "title": title,
                "score": score,
                "option": next(opt for opt in self.options if opt.title == title)
            }
            for title, score in scores.items()
        ]
        
        return sorted(ranked, key=lambda x: x["score"], reverse=True)
    
    def _generate_analysis_report(self, ranked_options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成决策分析报告"""
        best_option = ranked_options[0]
        score_range = max(opt["score"] for opt in ranked_options) - min(opt["score"] for opt in ranked_options)
        
        report = {
            "recommendation": {
                "best_option": best_option["title"],
                "confidence": self._calculate_confidence(best_option["score"], score_range),
                "reasoning": self._generate_reasoning(best_option["option"])
            },
            "rankings": [
                {
                    "rank": i + 1,
                    "title": opt["title"],
                    "score": opt["score"],
                    "pros": opt["option"].pros,
                    "cons": opt["option"].cons
                }
                for i, opt in enumerate(ranked_options)
            ],
            "sensitivity_analysis": self._perform_sensitivity_analysis(),
            "risk_analysis": self._analyze_risks()
        }
        
        return report
    
    def _calculate_confidence(self, best_score: float, score_range: float) -> str:
        """计算推荐的置信度"""
        if score_range == 0:
            return "低"
        
        confidence_ratio = best_score / score_range
        if confidence_ratio > 2:
            return "高"
        elif confidence_ratio > 1.5:
            return "中"
        else:
            return "低"
    
    def _generate_reasoning(self, option: DecisionOption) -> str:
        """生成推荐理由"""
        pros_text = "、".join(option.pros[:3])
        return f"该选项的主要优势在于：{pros_text}"
    
    def _perform_sensitivity_analysis(self) -> Dict[str, Any]:
        """执行敏感性分析"""
        # TODO: 实现更复杂的敏感性分析
        return {
            "most_sensitive_criterion": self.criteria[0].name if self.criteria else None,
            "sensitivity_level": "中"
        }
    
    def _analyze_risks(self) -> List[Dict[str, Any]]:
        """分析潜在风险"""
        risks = []
        for option in self.options:
            for con in option.cons:
                risks.append({
                    "option": option.title,
                    "risk": con,
                    "severity": "中"  # TODO: 实现风险等级评估
                })
        return risks 