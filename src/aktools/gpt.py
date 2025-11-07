"""
akshare-based simulated trading script
实现用户描述的“相对保守、左侧为主、低止盈（3%）、不设止损、分散持仓（20-30只）、高频换手”策略的回测与模拟。
特点：
 - 标的来源：A 股（akshare 提供）或用户自定义证券列表
 - 买入规则（左侧为主 + 简单右侧可选）：
     * 左侧（回调/低位买）：当前收盘价 <= 最近 N 天高点 * (1 - pullback_threshold)
     * 右侧（动量买，作补充）：当前收盘价 > SMA(M) 并且当日涨幅为正（短期趋势）
 - 卖出规则：
     * 固定止盈：达到 buy_price * (1 + take_profit) 即卖出（立刻落袋）
     * 不使用止损
 - 仿真：逐日遍历交易日，模拟资金、持仓、成交（按当日收盘价成交）
 - 支持交易成本（可配置），并输出回测结果与常见指标
注意：
 - 本脚本为回测/策略研究工具，不包含实盘下单逻辑
 - 需安装 akshare、pandas、numpy
   pip install akshare pandas numpy
"""

import akshare as ak
import pandas as pd
import numpy as np
import datetime
import time
import math
from typing import List, Dict, Tuple

# ----------------------------
# 配置参数（可修改）
# ----------------------------
START_DATE = "20251103"
END_DATE = "20251106"  # 设置你希望回测的区间
INITIAL_CAPITAL = 1_000_000.0  # 起始资金（人民币）
PORTFOLIO_SIZE = 25  # 目标持仓数量（20-30）
TAKE_PROFIT = 0.03  # 止盈收益率 3%
PULLBACK_DAYS = 20  # 计算最近高点的窗口，用于左侧入场
PULLBACK_THRESHOLD = 0.25  # 当价格回落到最近高点的 (1 - threshold) 或更低时视为左侧买点（例如 25% 回撤）
SMA_SHORT = 10  # 右侧动量信号使用的短期均线
USE_RIGHT_SIDE_AS_SUPPLEMENT = True  # 如果左侧买不到，是否用右侧动量买入补充
MAX_BUY_PER_DAY = 3  # 每日最多买入几只新标的（控制换手频率）
TRANSACTION_FEE_RATE = 0.0003  # 成交费及印花税等（示例）
MIN_PRICE = 1.0  # 排除过低价位（例如退市/风险股）
MAX_PRICE = 1000.0  # 排除异常高价（可调整）
VERBOSE = True


# ----------------------------
# 工具函数
# ----------------------------

def log(*args, **kwargs):
    if VERBOSE:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), *args, **kwargs)


def safe_sleep():
    # akshare 请求频繁时稍作等待，防止封禁（可根据需要调整或移除）
    time.sleep(0.15)


# ----------------------------
# 获取标的池（示例：取全部 A 股 或 用户自定义）
# ----------------------------
def get_universe_from_akshare(limit: int = 1000) -> pd.DataFrame:
    """
    获取 A 股代码与名称。返回 dataframe 包含 'code' 和 'name'
    limit: 限制数量，太多会很慢
    """
    log("正在从 akshare 获取 A 股列表...")
    df = ak.stock_zt_pool_em(date='20251106')
    df = df.rename(columns={"代码": "code", "名称": "name"})[["code", "name"]]
    # 过滤常见带通配符或 ST（可选），示例保留全部
    df = df.reset_index(drop=True)
    if limit:
        df = df.head(limit)
    return df


def fetch_daily(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    使用 akshare 获取单只股票日线数据
    返回 columns: date, open, high, low, close, volume, change_pct (float decimal)
    """
    # akshare 的函数：ak.stock_zh_a_daily(symbol) 或 ak.stock_zh_a_hist? 使用 stock_zh_a_daily
    # symbol 需要带市场后缀，如 'sh600000' 或 'sz000001'。ak.stock_zh_a_daily 接受 'sh600000' 或 'sz000001'。
    try:
        df = ak.stock_zh_a_daily(symbol="603122", start_date=start, end_date=end)
    except Exception as e:
        # 重试两次
        safe_sleep()
        try:
            df = ak.stock_zh_a_daily(symbol=symbol)
        except Exception as e2:
            log(f"无法获取 {symbol} 日线: {e2}")
            return pd.DataFrame()
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.reset_index()
    # akshare 返回：date, open, high, low, close, volume, amount, amktcap? 根据版本不同字段可能差异
    df = df.rename(columns={df.columns[0]: "date"}).loc[:, ["date", "open", "high", "low", "close", "volume"]]
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= pd.to_datetime(start)) & (df["date"] <= pd.to_datetime(end))]
    df = df.sort_values("date").reset_index(drop=True)
    df["pct_chg"] = df["close"].pct_change().fillna(0.0)
    return df


# ----------------------------
# 策略核心逻辑：信号生成
# ----------------------------
def is_left_side_buy(df_hist: pd.DataFrame, idx: int, pullback_days: int, pullback_threshold: float) -> bool:
    """
    判断在 idx 所在日期是否满足左侧（回调）买入条件：
    - 当前收盘价 <= 最近 pullback_days 天的最高价 * (1 - pullback_threshold)
    - 排除价格异常和无成交
    """
    if idx < 1:
        return False
    window_start = max(0, idx - pullback_days)
    recent_high = df_hist.loc[window_start:idx - 1, "high"].max()  # 不包括今天
    if pd.isna(recent_high) or recent_high <= 0:
        return False
    cur_close = df_hist.loc[idx, "close"]
    if cur_close <= 0 or cur_close < MIN_PRICE or cur_close > MAX_PRICE:
        return False
    threshold_price = recent_high * (1 - pullback_threshold)
    return cur_close <= threshold_price


def is_right_side_buy(df_hist: pd.DataFrame, idx: int, sma_period: int) -> bool:
    """
    简单右侧动量买入：
    - 当前价格在 sma_short 之上，且当日涨幅为正
    """
    if idx < sma_period:
        return False
    sma = df_hist.loc[idx - sma_period + 1:idx, "close"].mean()
    cur_close = df_hist.loc[idx, "close"]
    pct = df_hist.loc[idx, "pct_chg"]
    if cur_close <= 0 or cur_close < MIN_PRICE or cur_close > MAX_PRICE:
        return False
    return (cur_close > sma) and (pct > 0)


# ----------------------------
# 回测引擎（逐日仿真）
# ----------------------------
class Position:
    def __init__(self, code: str, buy_date: pd.Timestamp, buy_price: float, shares: int):
        self.code = code
        self.buy_date = buy_date
        self.buy_price = buy_price
        self.shares = shares
        self.sold = False
        self.sell_date = None
        self.sell_price = None

    def market_value(self, last_price: float) -> float:
        return self.shares * last_price

    def pnl_unrealized(self, last_price: float) -> float:
        return (last_price - self.buy_price) * self.shares

    def pnl_realized(self) -> float:
        if self.sold:
            return (self.sell_price - self.buy_price) * self.shares
        return 0.0


def backtest(universe: pd.DataFrame,
             start_date: str,
             end_date: str,
             initial_capital: float,
             portfolio_size: int,
             take_profit: float,
             pullback_days: int,
             pullback_threshold: float,
             sma_short: int,
             use_right_side: bool,
             max_buy_per_day: int,
             fee_rate: float) -> Dict:
    """
    基于每日收盘价的简单回测
    """
    # 1. 预取所有标的历史并缓存（可能耗时）
    log("开始下载标的历史数据（这一步可能较慢）...")
    symbol_hist = {}
    for i, row in universe.iterrows():
        code = row["code"]
        df = fetch_daily(code, start_date, end_date)
        if df is None or df.empty:
            continue
        # 只保留必要列
        df = df[["date", "open", "high", "low", "close", "volume", "pct_chg"]]
        df = df.reset_index(drop=True)
        symbol_hist[code] = df
        # 控制速率
        safe_sleep()

    # 2. 构建日期索引（以所有标的交易日期的并集为主）
    all_dates = pd.to_datetime(sorted(list(set(
        d for df in symbol_hist.values() for d in df['date'].dt.strftime('%Y-%m-%d').tolist()
    ))))
    # 过滤回测区间
    all_dates = all_dates[(all_dates >= pd.to_datetime(start_date)) & (all_dates <= pd.to_datetime(end_date))]
    all_dates = pd.Series(all_dates).sort_values().reset_index(drop=True)

    cash = initial_capital
    positions: Dict[str, Position] = {}
    trade_log = []  # 记录成交
    daily_nav = []  # 每日净值记录：date, nav, cash, market_value

    log("开始逐日回测...")
    for cur_date in all_dates:
        date_str = pd.to_datetime(cur_date).strftime("%Y-%m-%d")
        # 1) 卖出达到止盈的持仓（使用当日收盘价判断并以收盘价成交）
        to_sell = []
        for code, pos in list(positions.items()):
            if pos.sold:
                continue
            df = symbol_hist.get(code)
            if df is None:
                continue
            # find row for cur_date
            row = df[df["date"] == pd.to_datetime(date_str)]
            if row.empty:
                continue
            close = float(row["close"].iloc[0])
            target_price = pos.buy_price * (1 + take_profit)
            if close >= target_price:
                # 卖出
                sell_price = close
                proceeds = pos.shares * sell_price
                fee = proceeds * fee_rate
                cash += proceeds - fee
                pos.sold = True
                pos.sell_date = pd.to_datetime(date_str)
                pos.sell_price = sell_price
                trade_log.append({
                    "date": date_str,
                    "code": code,
                    "action": "SELL_TP",
                    "price": sell_price,
                    "shares": pos.shares,
                    "proceeds": proceeds,
                    "fee": fee
                })
                to_sell.append(code)
        for code in to_sell:
            positions.pop(code, None)

        # 2) 买入逻辑：优先左侧选股；若不足且启用右侧则补充
        # 每日找出可交易标的（有当日价格且未持仓）
        candidates_left = []
        candidates_right = []
        for code, df in symbol_hist.items():
            # skip already held
            if code in positions:
                continue
            row_idx = df.index[df["date"] == pd.to_datetime(date_str)].tolist()
            if not row_idx:
                continue
            idx = row_idx[0]
            # skip if too few days
            if idx < 1:
                continue
            # left-side
            if is_left_side_buy(df, idx, pullback_days, pullback_threshold):
                candidates_left.append((code, df.loc[idx, "close"]))
            elif use_right_side and is_right_side_buy(df, idx, sma_short):
                candidates_right.append((code, df.loc[idx, "close"]))

        # 排序：左侧优先，可按跌幅/回撤程度进一步排序（这里按价格低到高简单排序以便分散）
        candidates_left = sorted(candidates_left, key=lambda x: x[1])
        candidates_right = sorted(candidates_right, key=lambda x: x[1])

        # 每日最多买入 MAX_BUY_PER_DAY 只新标的，总持仓不能超过 portfolio_size
        buys_today = 0
        slots_available = portfolio_size - len(positions)
        buy_candidates = candidates_left + candidates_right
        for (code, price) in buy_candidates:
            if buys_today >= max_buy_per_day or slots_available <= 0:
                break
            # 以当日收盘价全部以尽量均等资金分配买入（每只目标持仓资金 = cash / slots_available）
            target_cash_per_position = cash / max(1, slots_available)
            # 购买尽可能整数股（A 股一般按手数100股，这里按股数整数）
            shares = int(target_cash_per_position / price)
            if shares <= 0:
                # 资金太少买不下
                continue
            cost = shares * price
            fee = cost * fee_rate
            total_cost = cost + fee
            if total_cost > cash:
                # 资金不足，尝试减少份额
                shares = int((cash / (1 + fee_rate)) / price)
                if shares <= 0:
                    continue
                cost = shares * price
                fee = cost * fee_rate
                total_cost = cost + fee
            # 执行买入
            cash -= total_cost
            pos = Position(code=code, buy_date=pd.to_datetime(date_str), buy_price=price, shares=shares)
            positions[code] = pos
            trade_log.append({
                "date": date_str,
                "code": code,
                "action": "BUY",
                "price": price,
                "shares": shares,
                "cost": cost,
                "fee": fee
            })
            buys_today += 1
            slots_available -= 1

        # 3) 记录当日净值
        market_value = 0.0
        for code, pos in positions.items():
            df = symbol_hist.get(code)
            if df is None:
                continue
            row = df[df["date"] == pd.to_datetime(date_str)]
            if row.empty:
                # 使用最后可用价格估算
                last_price = df["close"].iloc[idx] if not df.empty else pos.buy_price
            else:
                last_price = float(row["close"].iloc[0])
            market_value += pos.shares * last_price
        nav = cash + market_value
        daily_nav.append({
            "date": date_str,
            "nav": nav,
            "cash": cash,
            "market_value": market_value,
            "positions_count": len(positions)
        })

    # 回测结束：计算指标
    nav_df = pd.DataFrame(daily_nav)
    nav_df["date"] = pd.to_datetime(nav_df["date"])
    nav_df = nav_df.set_index("date").sort_index()
    # 若起止日期跨越多日，计算年化收益： (final/initial)^(252/num_days) - 1
    if not nav_df.empty:
        num_days = (nav_df.index[-1] - nav_df.index[0]).days or 1
    else:
        num_days = 1
    final_nav = nav_df["nav"].iloc[-1] if not nav_df.empty else initial_capital
    total_return = final_nav / initial_capital - 1.0
    annualized_return = (final_nav / initial_capital) ** (252.0 / max(1.0, num_days)) - 1.0
    # 最大回撤（基于净值序列）
    nav_series = nav_df["nav"]
    roll_max = nav_series.cummax()
    drawdown = (nav_series - roll_max) / roll_max
    max_drawdown = drawdown.min() if not drawdown.empty else 0.0

    # 统计交易记录
    trades_df = pd.DataFrame(trade_log)
    # 交易次数、胜率（基于卖出记录）
    sells = trades_df[trades_df["action"].str.startswith("SELL")]
    num_trades = len(sells)
    wins = 0
    total_realized_pnl = 0.0
    for _, row in sells.iterrows():
        buy_rows = trades_df[
            (trades_df["code"] == row["code"]) & (trades_df["date"] <= row["date"]) & (trades_df["action"] == "BUY")]
        if not buy_rows.empty:
            # 最近的 BUY
            buy_row = buy_rows.iloc[-1]
            pnl = row["price"] * row["shares"] - buy_row["price"] * buy_row["shares"] - (row["fee"] + buy_row["fee"])
            total_realized_pnl += pnl
            if pnl > 0:
                wins += 1
    win_rate = (wins / num_trades) if num_trades > 0 else None

    result = {
        "initial_capital": initial_capital,
        "final_nav": final_nav,
        "total_return": total_return,
        "annualized_return": annualized_return,
        "max_drawdown": max_drawdown,
        "num_trades": num_trades,
        "win_rate": win_rate,
        "total_realized_pnl": total_realized_pnl,
        "daily_nav": nav_df.reset_index(),
        "trades": trades_df,
    }
    return result


# ----------------------------
# 运行回测（主流程）
# ----------------------------
def main():
    # 1) 获取标的池（默认取前 500 支 A 股，用户可改）
    universe_df = get_universe_from_akshare(limit=100)
    log(f"标的池大小：{len(universe_df)}")

    # 2) 运行回测
    res = backtest(
        universe=universe_df,
        start_date=START_DATE,
        end_date=END_DATE,
        initial_capital=INITIAL_CAPITAL,
        portfolio_size=PORTFOLIO_SIZE,
        take_profit=TAKE_PROFIT,
        pullback_days=PULLBACK_DAYS,
        pullback_threshold=PULLBACK_THRESHOLD,
        sma_short=SMA_SHORT,
        use_right_side=USE_RIGHT_SIDE_AS_SUPPLEMENT,
        max_buy_per_day=MAX_BUY_PER_DAY,
        fee_rate=TRANSACTION_FEE_RATE
    )

    # 3) 输出结果摘要
    print("\n\n回测结果摘要")
    print("----------------------------")
    print(f"起始资金: {res['initial_capital']:.2f}")
    print(f"结束净值: {res['final_nav']:.2f}")
    print(f"总收益率: {res['total_return'] * 100:.2f}%")
    print(f"年化收益率(估算): {res['annualized_return'] * 100:.2f}%")
    print(f"最大回撤: {res['max_drawdown'] * 100:.2f}%")
    print(f"成交（止盈）次数: {res['num_trades']}")
    print(f"胜率（基于已实现交易）: {res['win_rate'] * 100:.2f}% " if res['win_rate'] is not None else "胜率：无交易")
    print(f"已实现盈亏: {res['total_realized_pnl']:.2f}")
    # 保存明细为 csv 方便后续分析
    res["daily_nav"].to_csv("daily_nav.csv", index=False)
    res["trades"].to_csv("trades.csv", index=False)
    print("已保存 daily_nav.csv 和 trades.csv 到当前目录。")


if __name__ == "__main__":
    main()
