import akshare as ak


# 上海证券交易所
def stock_sse_summary():
    """
    上海证券交易所-数据中心-统计数据-沪市行情每日统计
    https://akshare.akfamily.xyz/data/stock/stock.html#id1
    :return: 沪市行情每日统计
    :rtype: pandas.DataFrame
    """
    stock_sse_summary_df = ak.stock_sse_summary()
    print(stock_sse_summary_df)


def stock_individual_info_em():
    """
    东方财富网-数据中心-沪深个股-个股资料
    https://akshare.akfamily.xyz/data/stock/stock.html#id8
    :return: 个股资料
    :rtype: pandas.DataFrame
    """
    stock_individual_info_em_df = ak.stock_individual_info_em(symbol="603316")
    print(stock_individual_info_em_df)


def stock_individual_basic_info_xq():
    """
    雪球-个股基本信息
    https://akshare.akfamily.xyz/data/stock/stock.html#id27
    :return: 个股基本信息
    :rtype: pandas.DataFrame
    """
    stock_individual_basic_info_xq_df = ak.stock_individual_basic_info_xq(symbol="sh603316")
    print(stock_individual_basic_info_xq_df)


def stock_zh_a_spot_em():
    """
    东方财富网-数据中心-沪深A股-实时行情
    https://akshare.akfamily.xyz/data/stock/stock.html#id3
    :return: 沪深A股-实时行情
    :rtype: pandas.DataFrame
    """
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    print(stock_zh_a_spot_em_df)


def stock_zt_pool_strong_em():
    """
    东方财富网-数据中心-涨停板行情-强势股池
    https://akshare.akfamily.xyz/data/stock/stock.html#id23
    :return: 强势股池
    :rtype: pandas.DataFrame
    """
    stock_zt_pool_strong_em_df = ak.stock_zt_pool_strong_em(date='20250917')
    print(stock_zt_pool_strong_em_df)


def stock_rank_lxsz_ths():
    """
    同花顺-数据中心-技术选股-连续上涨
    https://akshare.akfamily.xyz/data/stock/stock.html#id19
    :return: 龙虎榜机构席位
    :rtype: pandas.DataFrame
    """
    stock_rank_lxsz_ths_df = ak.stock_rank_lxsz_ths()
    print(stock_rank_lxsz_ths_df)


def stock_rank_cxfl_ths():
    """
    同花顺-数据中心-技术选股-持续放量
    https://akshare.akfamily.xyz/data/stock/stock.html#id20
    :return: 龙虎榜机构席位
    :rtype: pandas.DataFrame
    """
    stock_rank_cxfl_ths_df = ak.stock_rank_cxfl_ths()
    print(stock_rank_cxfl_ths_df)


def stock_rank_xstp_ths():
    """
    同花顺-数据中心-技术选股-向上突破
    目标地址: https://data.10jqka.com.cn/rank/xstp/
    :return: 龙虎榜机构席位
    :rtype: pandas.DataFrame
    """
    stock_rank_xstp_ths_df = ak.stock_rank_xstp_ths(symbol="500日均线")
    print(stock_rank_xstp_ths_df)


def stock_rank_ljqs_ths():
    """
    同花顺-数据中心-技术选股-量价齐升
    https://akshare.akfamily.xyz/data/stock/stock.html#id21
    :return: 龙虎榜机构席位
    :rtype: pandas.DataFrame
    """
    stock_rank_ljqs_ths_df = ak.stock_rank_ljqs_ths()
    print(stock_rank_ljqs_ths_df)


def stock_zh_a_hist():
    """
    东方财富网-数据中心-沪深A股-历史行情
    https://akshare.akfamily.xyz/data/stock/stock.html#id4
    :return: 沪深A股-历史行情
    :rtype: pandas.DataFrame
    """
    # 设置股票代码、开始日期、结束日期和调整方式
    stock_code = "603659"
    start_date = "20250801"
    end_date = "20250917"
    adjust = ""  # 不复权: ""; 前复权: "qfq"; 后复权: "hfq"
    # 获取数据，并指定需要计算的技术指标
    df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",  # 日线数据
        start_date=start_date,
        end_date=end_date,
        adjust=adjust,
    )
    # 查看数据列，会发现多了 MACD 和 KDJ 相关的列
    print(df.columns)
    # 查看最后几行数据
    print(df.tail())


if __name__ == '__main__':
    stock_zh_a_hist()
