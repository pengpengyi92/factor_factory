import pandas as pd
import numpy as np

class FactorStrategy:
    def __init__(self, data, factor_expression):
        """
        初始化因子选股策略。
        :param data: 包含股票数据的 DataFrame。
        :param factor_expression: 计算因子值的表达式（如 'close + open' 或 'rank(open)'）。
        """
        self.data = data
        self.factor_expression = factor_expression

    def calculate_factor(self):
        """
        计算因子值：
        - 使用用户输入的表达式动态计算因子值。
        """
        # 定义 rank 函数
        def rank(series):
            return series.rank(ascending=False)
        
        # 将 rank 函数和 DataFrame 的列添加到局部变量中
        local_vars = {'rank': rank, **self.data.to_dict('list')}
        
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
        - 卖出信号：因子值最低的后三名。
        """
        # 买入信号
        buy_signals = self.data[self.data['rank'] <= 3]
        buy_signals['signal'] = 'buy'
        
        # 卖出信号
        sell_signals = self.data[self.data['rank'] >= (len(self.data) - 2)]
        sell_signals['signal'] = 'sell'
        
        # 合并信号
        self.signals = pd.concat([buy_signals, sell_signals])
        print("交易信号生成完成。")

    def backtest(self, initial_capital=100000):
        """
        回测策略：
        - 买入信号：买入等权重的股票。
        - 卖出信号：卖出对应股票。
        :param initial_capital: 初始资金。
        """
        portfolio_value = initial_capital
        positions = {}  # 持仓信息
        
        print("\n===== 回测开始 =====")
        
        for index, row in self.signals.iterrows():
            stock = row['stock']  # 假设数据中有 'stock' 列表示股票代码
            price = row['price']  # 假设数据中有 'price' 列表示股票价格
            signal = row['signal']
            
            if signal == 'buy':
                # 买入等权重的股票
                position_size = portfolio_value / 3  # 买入前三名，每只股票等权重
                shares = position_size // price
                positions[stock] = shares
                portfolio_value -= shares * price
                print(f"买入 {stock}，价格 {price}，数量 {shares}，剩余资金 {portfolio_value:.2f}")
            elif signal == 'sell':
                # 卖出对应股票
                if stock in positions:
                    shares = positions.pop(stock)
                    portfolio_value += shares * price
                    print(f"卖出 {stock}，价格 {price}，数量 {shares}，剩余资金 {portfolio_value:.2f}")
        
        print("===== 回测结束 =====")
        print(f"最终投资组合价值：{portfolio_value:.2f}")


# 示例用法
if __name__ == "__main__":
    # 示例数据
    data = {
        'stock': ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA'],
        'price': [150, 2800, 300, 3400, 700, 600],  # 假设当前价格
        'open': [145, 2750, 290, 3350, 680, 590],  # 假设开盘价
        'close': [155, 2850, 310, 3450, 720, 610]  # 假设收盘价
    }
    df = pd.DataFrame(data)

    # 初始化因子选股策略
    factor_expression = "close + open"  # 用户输入的表达式
    strategy = FactorStrategy(df, factor_expression)

    # 计算因子值
    strategy.calculate_factor()

    # 对股票进行排序
    strategy.rank_stocks()

    # 生成交易信号
    strategy.generate_signals()

    # 回测策略
    strategy.backtest(initial_capital=100000)
