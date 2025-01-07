import pandas as pd
import numpy as np

class FactorStrategy:
    def __init__(self, data, factor_column, factor=None):
        """
        初始化因子选股策略。
        :param data: 包含股票数据的 DataFrame。
        :param factor_column: 用于排序的因子列名。
        :param factor: 计算因子值的函数（可选）。如果未提供，则直接使用 factor_column 列的值。
        """
        self.data = data
        self.factor_column = factor_column
        self.factor = factor

    def calculate_factor(self):
        """
        计算因子值：
        - 如果提供了 factor 函数，则使用该函数计算因子值。
        - 否则，直接使用 factor_column 列的值。
        """
        if self.factor is not None:
            # 使用 factor 函数计算因子值
            self.data[self.factor_column] = self.factor(self.data)
            print("因子值计算完成（使用自定义函数）。")
        else:
            # 直接使用 factor_column 列的值
            print("因子值计算完成（使用现有列）。")

    def rank_stocks(self):
        """
        根据因子值对股票进行排序。
        """
        # 按因子值从高到低排序
        self.data['rank'] = self.data[self.factor_column].rank(ascending=False)
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
        'pe_ratio': [25, 30, 20, 50, 100, 40],  # 假设市盈率
        'roe': [0.15, 0.20, 0.18, 0.10, 0.05, 0.12]  # 假设净资产收益率
    }
    df = pd.DataFrame(data)

    # 自定义因子计算函数
    def custom_factor(data):
        """
        自定义因子计算逻辑：因子值 = ROE / PE Ratio
        """
        return data['roe'] / data['pe_ratio']

    # 初始化因子选股策略
    strategy = FactorStrategy(df, factor_column='factor_value', factor=custom_factor)

    # 计算因子值
    strategy.calculate_factor()

    # 对股票进行排序
    strategy.rank_stocks()

    # 生成交易信号
    strategy.generate_signals()

    # 回测策略
    strategy.backtest(initial_capital=100000)
