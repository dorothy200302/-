import pandas as pd
import numpy as np
from typing import List, Dict, Any
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from textblob import TextBlob

class DataAnalyzer:
    def __init__(self):
        self.scaler = MinMaxScaler()
        
    def analyze_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析数据趋势"""
        try:
            df = pd.DataFrame(data)
            
            # 时间序列分析
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values('timestamp')
                
            # 计算基本统计量
            stats = {
                'count': len(df),
                'mean': df.get('value', 0).mean(),
                'std': df.get('value', 0).std(),
                'min': df.get('value', 0).min(),
                'max': df.get('value', 0).max()
            }
            
            # 识别趋势
            if len(df) > 1:
                trend = 'increasing' if df['value'].iloc[-1] > df['value'].iloc[0] else 'decreasing'
            else:
                trend = 'unknown'
                
            return {
                'statistics': stats,
                'trend': trend
            }
        except Exception as e:
            print(f"趋势分析错误: {str(e)}")
            return {}
            
    def cluster_analysis(self, data: List[Dict[str, Any]], n_clusters: int = 3) -> Dict[str, Any]:
        """聚类分析"""
        try:
            # 准备数据
            features = self.prepare_features(data)
            
            # 标准化
            scaled_features = self.scaler.fit_transform(features)
            
            # KMeans聚类
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(scaled_features)
            
            # 分析结果
            cluster_stats = []
            for i in range(n_clusters):
                cluster_data = features[clusters == i]
                stats = {
                    'size': len(cluster_data),
                    'center': kmeans.cluster_centers_[i].tolist(),
                    'variance': cluster_data.var(axis=0).mean()
                }
                cluster_stats.append(stats)
                
            return {
                'n_clusters': n_clusters,
                'cluster_stats': cluster_stats,
                'labels': clusters.tolist()
            }
        except Exception as e:
            print(f"聚类分析错误: {str(e)}")
            return {}
            
    def sentiment_analysis(self, texts: List[str]) -> Dict[str, Any]:
        """情感分析"""
        try:
            sentiments = []
            for text in texts:
                blob = TextBlob(text)
                sentiment = {
                    'text': text,
                    'polarity': blob.sentiment.polarity,
                    'subjectivity': blob.sentiment.subjectivity
                }
                sentiments.append(sentiment)
                
            # 计算整体情感
            avg_polarity = sum(s['polarity'] for s in sentiments) / len(sentiments)
            avg_subjectivity = sum(s['subjectivity'] for s in sentiments) / len(sentiments)
            
            return {
                'overall_sentiment': {
                    'polarity': avg_polarity,
                    'subjectivity': avg_subjectivity
                },
                'detailed_sentiments': sentiments
            }
        except Exception as e:
            print(f"情感分析错误: {str(e)}")
            return {}
            
    def prepare_features(self, data: List[Dict[str, Any]]) -> np.ndarray:
        """准备特征数据"""
        # 示例特征提取，需要根据实际数据调整
        features = []
        for item in data:
            feature = [
                float(item.get('value', 0)),
                len(str(item.get('text', ''))),
                item.get('importance', 0)
            ]
            features.append(feature)
        return np.array(features) 