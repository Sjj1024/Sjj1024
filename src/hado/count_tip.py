import pandas as pd

# 读取 CSV 文件
df = pd.read_csv('files/微信支付账单-转账(20250615-20250618.csv')

# 筛选交易对象包含 'hado' 且 '收/支' 类型是 '支出' 的数据
filtered_df = df[(df['交易对方'].str.contains('hado', na=False)) & (df['收/支'] == '支出')].copy()

# 使用 .loc 设置交易日期列
filtered_df.loc[:, '交易日期'] = pd.to_datetime(filtered_df['交易时间']).dt.date

# 去掉 "金额(元)" 列中的 "¥" 符号，并将其转换为浮点数
filtered_df['金额(元)'] = filtered_df['金额(元)'].replace('[¥,]', '', regex=True).astype(float)

# 计算交易日期的唯一天数
unique_days_count = filtered_df['交易日期'].nunique()

# 计算交易人一共多少个
unique_people_count = filtered_df['交易对方'].nunique()

# 计算金额总和
total_amount = filtered_df['金额(元)'].sum()

# 打印结果
print("一共有多少天：", unique_days_count)
print("一共有多少人：", unique_people_count)
print("预期金额总和", unique_days_count * 270)
print("实际金额总和：", total_amount)
# 加上我的一共多少钱
add_song = 27 * unique_days_count + total_amount
print(f"加上我的总和: {add_song}")
