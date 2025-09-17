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


if __name__ == '__main__':
    stock_individual_basic_info_xq()
