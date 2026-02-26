import akshare as ak
import requests

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


def stock_board_concept_name_em():
    """
    东方财富网-数据中心-板块概念-概念名称
    https://akshare.akfamily.xyz/data/stock/stock.html#id15
    :return: 概念名称
    :rtype: pandas.DataFrame
    """
    stock_board_concept_name_em_df = ak.stock_board_concept_name_em()
    print(stock_board_concept_name_em_df)


def stock_board_industry_name_em():
    """
    东方财富网-数据中心-板块概念-行业名称
    https://akshare.akfamily.xyz/data/stock/stock.html#id14
    :return: 行业名称
    :rtype: pandas.DataFrame
    """
    stock_board_industry_name_em_df = ak.stock_board_industry_name_em()
    print(stock_board_industry_name_em_df)


def stock_hot_follow_xq():
    """
    雪球-热门关注
    https://akshare.akfamily.xyz/data/stock/stock.html#id26
    :return: 热门关注
    :rtype: pandas.DataFrame
    """
    stock_hot_follow_xq_df = ak.stock_hot_follow_xq()
    print(stock_hot_follow_xq_df)


def stock_hot_rank_em():
    """
    东方财富网-数据中心-热门排行-热门排行
    https://akshare.akfamily.xyz/data/stock/stock.html#id16
    :return: 热门排行
    :rtype: pandas.DataFrame
    """
    stock_hot_rank_em_df = ak.stock_hot_rank_em()
    print(stock_hot_rank_em_df)


def stock_zt_pool_em():
    """
    东方财富网-数据中心-涨停板行情-涨停股池
    https://akshare.akfamily.xyz/data/stock/stock.html#id22
    :return: 涨停股池
    :rtype: pandas.DataFrame
    """
    stock_zt_pool_em_df = ak.stock_zt_pool_em(date='20251105')
    print(stock_zt_pool_em_df)


# 获取 品种列表
def stock_gold_sge_symbols():
    """
    东方财富网-数据中心-贵金属-品种列表
    https://akshare.akfamily.xyz/data/spot/spot.html
    :return: 品种列表
    :rtype: pandas.DataFrame
    """
    symbols = ak.spot_symbol_table_sge()
    print(symbols)


# 获取 上海黄金交易所 实时金价
def stock_gold_spot():
    """
    东方财富网-数据中心-贵金属-实时金价
    https://akshare.akfamily.xyz/data/spot/spot.html
    :return: 实时金价
    :rtype: pandas.DataFrame
    """
    spot_quotations_sge_df = ak.spot_quotations_sge(symbol="Au99.99")
    print(spot_quotations_sge_df)


# 获取 上海黄金交易所 历史行情金价
def stock_gold_hist():
    """
    东方财富网-数据中心-贵金属-历史行情金价
    https://akshare.akfamily.xyz/data/spot/spot.html
    :return: 历史行情金价
    :rtype: pandas.DataFrame
    """
    spot_hist_sge_df = ak.spot_hist_sge(symbol='Au99.99')
    print(spot_hist_sge_df)


# 伦敦金现价
def stock_gold_london_spot():
    """
    东方财富网-数据中心-贵金属-伦敦金现价
    https://akshare.akfamily.xyz/data/spot/spot.html
    :return: 伦敦金现价
    :rtype: pandas.DataFrame
    | 字段名 | 数据类型 | 说明 |
    | :--- | :--- | :--- |
    | **buy** | 字符串 | **买入价**。指平台或做市商愿意买入该商品的价格，对于投资者来说是卖出（做空）的价格。 |
    | **code** | 字符串 | **商品代码**。代表交易品种的缩写，`LLG` 是伦敦金（Local London Gold）的常见代码。 |
    | **excode** | 字符串 | **交易所代码**。代表服务器或平台内部的交易所/品种标识，`MT4` 通常指该数据来自 MT4 平台。 |
    | **exname** | 字符串 | **交易所/平台名称**。这里指提供报价的具体平台名称，例如 `鑫汇宝`。 |
    | **from** | 字符串 | **数据来源标识**。可能代表数据推送的来源或协议类型，`MT` 可能指来自 MT4/MT5 平台的数据流。 |
    | **high** | 字符串 | **最高价**。指当日或当前周期内，该品种达到的最高交易价格。 |
    | **last** | 字符串 | **最新价**。指最近一笔交易的成交价格。 |
    | **lastclose** | 字符串 | **昨收盘价**。指上一个交易日的最终收盘价格。 |
    | **low** | 字符串 | **最低价**。指当日或当前周期内，该品种达到的最低交易价格。 |
    | **name** | 字符串 | **商品名称**。该交易品种的中文名称，例如 `伦敦金`。 |
    | **open** | 字符串 | **开盘价**。指当日或当前周期开始时的第一笔交易价格。 |
    | **quoteTime** | 字符串 | **报价时间**。通常为 Unix 时间戳（秒级），表示该报价生成的时间。`1772013449` 是一个示例数值。 |
    | **sell** | 字符串 | **卖出价**。指平台或做市商愿意卖出该商品的价格，对于投资者来说是买入（做多）的价格。 |
    | **volume** | 字符串 | **成交量/持仓量**。代表当前的交易量或持仓量，数值为 `0` 可能表示数据未获取或无交易。 |
    | **status** | 字符串 | **交易状态**。代表当前市场状态，`open` 表示正在交易中（开盘状态）。 |

    **关键点提示：**

    1.  **买卖价差**：对比 `buy` (5190.39) 和 `sell` (5190.89)，可以看到有 0.5 的点差，这是做市商交易（如现货黄金）的典型特征。
    2.  **数据类型**：所有数值字段（如价格、成交量、时间戳）在 JSON 中都被定义为了 **字符串（String）**，在使用这些数据进行计算时，通常需要先将其转换为浮点数（Float）或整数（Integer）。
    """
    url = "https://hq.91pme.com/getmarketinfo/getQuotationByCode2.do?code=llg"
    payload = {}
    headers = {
        'Pragma': 'no-cache'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)


# 伦敦银价
def stock_silver_london_spot():
    """
    东方财富网-数据中心-贵金属-伦敦银价
    https://akshare.akfamily.xyz/data/spot/spot.html
    :return: 伦敦银价
    :rtype: pandas.DataFrame
    """
    url = "https://hq.91pme.com/getmarketinfo/getQuotationByCode2.do?code=lls"
    payload = {}
    headers = {
        'Pragma': 'no-cache'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)


if __name__ == '__main__':
    stock_gold_london_spot()
    stock_silver_london_spot()
