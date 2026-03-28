# src/isa_filter.py
"""
Filter to verify ISA UK elegibility.
Based on HMRC regulation and brokers guidance.
"""

class ISAFilter:
    """
    Verify if a stock can be holded on an UK ISA account.
    """
    def __init__(self):
        #Exchanges recognized by HMRC
        self.recognized_exchanges = ['LSE', 'LON', 'London Stock Exchange']

        #Non allowed value types
        self.banned_types = ['ETF', 'ETC', 'Fund', 'Trust', 'REIT', 'CFD']

    def is_isa_eligible(self, ticker, stock_info):
        """
        Verify if a stock is qualified for an UK ISA account.
        Criteria:
        1. Should be listed on the LSE.
        2. Should not be an ETF/ETC (excluded).
        3.Individual companies, not funds.
        """

        reasons = []
        eligible = True

        #Criteria 1:
        exchange = stock_info.get('exchange', '')
        if not any(exch in exchange for exch in self.recognized_exchanges):
            eligible = False
            reasons.append(f"Exchange not recognized: {exchange}")

        #Criteria 2:
        quote_type = stock_info.get('quoteType', '')
        long_name = stock_info.get('longName', '').lower()

        if quote_type in self.banned_types:
            eligible = False
            reasons.append(f"Quote type not allowed: {quote_type}")

        #Criteria 3:
        if 'ETF' in long_name or 'ETC' in long_name or 'Fund' in long_name or 'Trust' in long_name or 'REIT' in long_name or 'CFD' in long_name:
            eligible = False
            reasons.append(f"Not allowed asset type")

        return eligible, reasons if not eligible else ["Eligible for ISA"]

def filter_isa_stocks(tickers_data):
    """
    Filter a list of stocks to keep only the eligible for ISA.
    Args:
        tickers_data (list): list of stock tickers.
    Returns:
        Filtered list of eligible stocks.
    """

    isa_filter = ISAFilter()
    eligible_stocks = []

    for stock in tickers_data:
        ticker = stock.get('Ticker', '')
        info = stock.get('info', {})
        eligible, reasons = isa_filter.is_isa_eligible(ticker, info)

        if eligible:
            stock['isa_eligible'] = True
            eligible_stocks.append(stock)
        else:
            print(f"{ticker} is not eligible for ISA: {reasons[0]}")

    print(f"ISA eligible stocks: {len(eligible_stocks)}")
    return eligible_stocks