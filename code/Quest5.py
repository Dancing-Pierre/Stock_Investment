"""
绘制任务3、4的结果，保存为图片。
"""
import pandas as pd
import matplotlib.pyplot as plt

# 读取组合每日价值
portfolio_values = pd.read_csv('../result/portfolio_values.csv', index_col=0, parse_dates=True)

# 绘制图表
plt.figure(figsize=(12, 6))
# 第一条线，策略1
plt.plot(portfolio_values['Strategy1'], label='Strategy 1')
# 第二条线，基准策略
plt.plot(portfolio_values['Benchmark'], label='Benchmark')
# 画标题
plt.title('Daily Portfolio Value')
# x轴标签
plt.xlabel('Date')
# y轴标签
plt.ylabel('Portfolio Value')
# 显示图例
plt.legend()
plt.grid(True)

# 保存图表
plt.savefig('../result/portfolio_values.png')
# 图表显示
plt.show()
