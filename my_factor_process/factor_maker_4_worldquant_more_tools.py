import pandas as pd
import numpy as np
from scipy.stats import zscore

class FactorStrategy:
    def __init__(self, data, factor_expression):
        """
        初始化因子选股策略。
        :param data: 包含股票数据的 DataFrame。
        :param factor_expression: 计算因子值的表达式（如 'close + open' 或 'ts_rank(open, 20)'）。
        """
        self.data = data
        self.factor_expression = factor_expression

    def calculate_factor(self):
        """
        计算因子值：
        - 使用用户输入的表达式动态计算因子值。
        - 支持多种因子计算函数。
        """
        # 定义常用函数
        def rank(series):
            """截面排名函数"""
            return series.rank(ascending=False)
        
        def zscore_func(series):
            """截面标准化函数"""
            return (series - series.mean()) / series.std()
        
        def scale(series):
            """截面缩放函数（缩放到 [0, 1] 范围）"""
            return (series - series.min()) / (series.max() - series.min())
        
        def decile(series):
            """截面分位数函数（分为 10 个 decile）"""
            return pd.qcut(series, q=10, labels=False, duplicates='drop')
        
        def quantile(series, q):
            """截面分位数函数（指定分位数）"""
            return series.rank(pct=True) > q
        
        def ts_rank(series, window):
            """时间序列排名函数"""
            return series.rolling(window=window).apply(lambda x: x.rank(ascending=False).iloc[-1])
        
        def ts_zscore(series, window):
            """时间序列标准化函数"""
            return series.rolling(window=window).apply(lambda x: (x.iloc[-1] - x.mean()) / x.std())
        
        def ts_mean(series, window):
            """时间序列均值函数"""
            return series.rolling(window=window).mean()
        
        def ts_std_dev(series, window):
            """时间序列标准差函数"""
            return series.rolling(window=window).std()
        
        def ts_max(series, window):
            """时间序列最大值函数"""
            return series.rolling(window=window).max()
        
        def ts_min(series, window):
            """时间序列最小值函数"""
            return series.rolling(window=window).min()
        
        def ts_sum(series, window):
            """时间序列求和函数"""
            return series.rolling(window=window).sum()
        
        def ts_delta(series, window):
            """时间序列变化量函数"""
            return series.diff(window)
        
        def ts_returns(series, window):
            """时间序列收益率函数"""
            return series.pct_change(window)
        
        def correlation(x, y, window):
            """时间序列相关系数函数"""
            return x.rolling(window=window).corr(y)
        
        def covariance(x, y, window):
            """时间序列协方差函数"""
            return x.rolling(window=window).cov(y)
        
        def residual(x, y):
            """回归残差函数"""
            return x - np.polyval(np.polyfit(y, x, 1), y)
        
        # 将函数和 DataFrame 的列添加到局部变量中
        local_vars = {
            'rank': rank,
            'zscore': zscore_func,
            'scale': scale,
            'decile': decile,
            'quantile': quantile,
            'ts_rank': ts_rank,
            'ts_zscore': ts_zscore,
            'ts_mean': ts_mean,
            'ts_std_dev': ts_std_dev,
            'ts_max': ts_max,
            'ts_min': ts_min,
            'ts_sum': ts_sum,
            'ts_delta': ts_delta,
            'ts_returns': ts_returns,
            'correlation': correlation,
            'covariance': covariance,
            'residual': residual,
            **self.data.to_dict('list')
        }
        
        # 使用 eval 计算因子值
        self.data['factor_value'] = eval(self.factor_expression, {}, local_vars)
        print("因子值计算完成。")

    def rank_stocks(self):
        """
        根据因子值对股票进行排序。
        """
        # 按因子值从高到低排序
        self.data['rank'] = self.data['factor_value'].rank(ascending=False)
        print("股票排序完成。")

    def generate_signals(self):
        """
        生成交易信号：
        - 买入信号：因子值最高的前三名。
        - 卖出信号：因子
