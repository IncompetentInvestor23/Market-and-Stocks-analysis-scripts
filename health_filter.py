# src/health_filter.py
"""
Filter to identify companies with a solid financial health.
Focus on low debt and revenue > costs.
"""

import numpy as np

class HealthFilter:
    """
    Rates the financial health of a company based in quality criteria.
    """

    def __init__(self):
        # Thresholds based in quality analysis

        # Maximum recommended debt to equity:
        self.max_debt_to_equity = 50.0

        # Maximum recommended debt:
        self.min_current_ratio = 1.5

        # Minimum operating margin (10%):
        self.min_operating_margin = 0.10

        # Interest coverage capability:
        self.min_interest_coverage = 3.0

    def analyze(self, stock_data):
        """
        Analyze the financial health of a company.
        """

        metrics = {}
        health_score = 0
        max_score = 5
        reasons = []

        info = stock_data.get('info', {})

        # 1.DEBT: should be low
        debt_to_equity = info.get('debtToEquity', np.nan)
        if not np.isnan(debt_to_equity):
            metrics['debt_to_equity'] = debt_to_equity

            if debt_to_equity < 30:
                health_score += 2
                reasons.append("Very low debt.")
            elif debt_to_equity < self.max_debt_to_equity:
                health_score += 1
                reasons.append("Controlled debt.")
            else:
                reasons.append(f"High debt: {debt_to_equity:.2f}")
        else:
            reasons.append("Not available.")

        # 2.LIQUIDITY: capacity of pay debt in a short time
        current_ratio = info.get('currentRatio', np.nan)
        if not np.isnan(current_ratio):
            metrics['current_ratio'] = current_ratio

            if current_ratio > 2.0:
                health_score += 1
                reasons.append("Excellent liquidity.")
            elif current_ratio > self.min_current_ratio:
                health_score += 0.5
                reasons.append("Acceptable liquidity.")
            else:
                reasons.append(f"Low liquidity: {current_ratio:.2f}")
        else:
            reasons.append("Not available.")

        # 3.PROFITABILITY: revenue > cost
        net_income = info.get('netIncomeToCommon', 0)
        total_revenue = info.get('totalRevenue', 1)
        operating_income = info.get('operatingIncome', 0)

        # Net Margin
        net_margin = (net_income / total_revenue * 100) if total_revenue > 0 else np.nan
        metrics['net_margin'] = net_margin

        if net_income > 0:
            health_score += 1
            reasons.append(f"Profit: {net_income/1e6:.1f}M")
        else:
            reasons.append("Loses.")

        # Operating margin
        op_margin = (operating_income / total_revenue) if total_revenue > 0 else np.nan
        if not np.isnan(op_margin) and op_margin > self.min_operating_margin:
            health_score += 0.5
            reasons.append(f"Operating margin: {op_margin*100:.1f}%")

        #4.FREE CASH FLOW: Generated cash
        fcf = info.get('freeCashFlow', 0)
        metrics['fcf'] = fcf

        if fcf > 0:
            health_score += 0.5
            reasons.append(f"FCF positive: {fcf/1e6:.1f}M")
        else:
            reasons.append("FCF negative.")

        #5.INTEREST COVERAGE: capability to pay interest
        ebit = info.get('ebitda', 0)
        #Aproximation
        interest = info.get('interestExpense', 1)
        interest_coverage = ebit / interest if interest > 0 else np.inf
        metrics['interest_coverage'] = interest_coverage

        if interest_coverage > self.min_interest_coverage:
            health_score += 0.5
            reasons.append("Good interest coverage.")
        elif interest_coverage > 1:
            reasons.append("Do not cover interest.")

        #FINAL RESULT
        is_healthy = health_score >= 3 # Minimum 3/5 points

        return {
            'is_healthy': is_healthy,
            'health_score': health_score,
            'max_score': max_score,
            'reasons': reasons[:3], #Top 3 reasons
            'metrics': metrics
        }

def filter_healthy_stocks(tickers_data):
    """
    Filter stocks with good financial health.
    """
    health_filter = HealthFilter()
    healthy_stocks = []

    print("\n Filtering by financial health...")

    for stock in tickers_data:
        ticker = stock.get('Ticker', '')
        analysis = health_filter.analyze(stock)

        if analysis['is_healthy']:
            stock['health_analysis'] = analysis
            healthy_stocks.append(stock)

            print(f"{ticker}: Score {analysis['health_score']}/5 - {analysis['reasons'][0]}")
        else:
            print(f"{ticker}: Score {analysis['health_score']}/5 - Do not pass financial health filter.")

    print(f"\n Stocks with solid financial health: {len(healthy_stocks)}")
    return healthy_stocks