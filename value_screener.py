# src/value_screener.py
"""
Screener for value investing Based in the principles of Benjamin Graham.
"""

import numpy as np

class ValueScreener:
    """
    Evaluates stocks based in the value investing criteria.
    """

    def __init__(self):
        # Value Thresholds
        # Max P/E for value
        self.max_pe = 15
        # Max P/B
        self.max_pb = 1.5
        # Max P/S
        self.max_ps = 2.0
        # Min ROE %
        self.min_roe = 10

    def analyze(self, stock_data):
        """
        Calculates the value rating for a stock.
        """

        info = stock_data.get('info', {})
        health = stock_data.get('health_analysis', {})

        score = 0
        max_score = 10
        factors = []
        metrics = {}

        # 1. P/E Ratio (low is better)
        pe = info.get('trailingPE', np.nan)
        metrics['pe'] = pe
        if not np.isnan(pe):
            if pe < 10:
                score += 3
                factors.append(f"P/E excellent: {pe:.1f}")
            elif pe < self.max_pe:
                score += 2
                factors.append(f"P/E good: {pe:.1f}")
            elif pe < 20:
                score += 1
                factors.append(f"P/E acceptable: {pe:.1f}")
            else:
                factors.append(f"P/E high: {pe:.1f}")

        # 2. P/B Ratio (low is better)
        pb = info.get('priceToBook', np.nan)
        metrics['pb'] = pb
        if not np.isnan(pb):
            if pb < 1.0:
                score += 2
                factors.append(f"P/B < 1: {pb:.2f}")
            elif pb < self.max_pb:
                score += 1
                factors.append(f"P/B reasonable: {pb:.2f}")
            elif pb < 2.0:
                score += 0.5
                factors.append(f"P/B slightly high: {pb:.2f}")
            else:
                factors.append(f"P/B very high: {pb:.2f}")

        # 3. Dividend Yield (preferable one that pays dividends)
        # FIX: Yahoo Finance can return dividendYield as decimal (0.035) or
        # as percentage (3.5) depending on the ticker/region. Normalise to %.
        div_yield_raw = info.get('dividendYield', 0) or 0
        div_yield_pct = div_yield_raw * 100 if div_yield_raw < 1 else div_yield_raw
        metrics['dividend_yield'] = div_yield_pct

        # FIX: compare in percentage space (not against 0.03 decimal)
        if div_yield_pct > 3:
            score += 1.5
            factors.append(f"Good dividend: {div_yield_pct:.1f}%")
        elif div_yield_pct > 0:
            score += 0.5
            factors.append(f"Pays dividend: {div_yield_pct:.1f}%")

        # 4. ROE (profitability)
        roe = info.get('returnOnEquity', np.nan)
        metrics['roe'] = roe * 100 if not np.isnan(roe) else np.nan
        if not np.isnan(roe):
            roe_pct = roe * 100
            if roe_pct > 20:
                score += 2
                factors.append(f"ROE excellent: {roe_pct:.1f}%")
            elif roe_pct > self.min_roe:
                score += 1
                factors.append(f"ROE good: {roe_pct:.1f}%")
            else:
                factors.append(f"ROE low: {roe_pct:.1f}%")

        # 5. Earnings growth
        earnings_growth = info.get('earningsGrowth', np.nan)
        metrics['earnings_growth'] = earnings_growth
        if not np.isnan(earnings_growth) and earnings_growth > 0.05:
            score += 1.5
            factors.append(f"Earnings growth: {earnings_growth*100:.0f}%")

        # Bonus: financial health (already filtered but extra score)
        if health.get('health_score', 0) >= 4:
            score += 1
            factors.append("Excellent financial health")

        # Normalize score to 0-10
        final_score = min(score, 10)

        return {
            'value_score': final_score,
            'factors': factors[:4],  # Top 4 factors
            'metrics': metrics
        }

def get_top15_value(healthy_stocks):
    """
    Select the top 15 value stocks.
    """
    screener = ValueScreener()
    results = []

    print("\n Analysing for VALUE INVESTING...")

    for stock in healthy_stocks:
        ticker = stock.get('Ticker', '')
        analysis = screener.analyze(stock)

        results.append({
            'Ticker': ticker,
            'Name': stock['info'].get('longName', 'N/A')[:30],
            'Price': stock['info'].get('currentPrice', 0),
            'Value Score': analysis['value_score'],
            'P/E': analysis['metrics'].get('pe', 0),
            'P/B': analysis['metrics'].get('pb', 0),
            'ROE %': analysis['metrics'].get('roe', 0),
            'Div Yield %': analysis['metrics'].get('dividend_yield', 0),
            'Factors': ', '.join(analysis['factors'])
        })

    # Order by score and take top 15
    top15 = sorted(results, key=lambda x: x['Value Score'], reverse=True)[:15]

    print(f"\n TOP 15 VALUE STOCKS:")
    for i, stock in enumerate(top15, 1):
        print(f" {i}. {stock['Ticker']}: {stock['Value Score']:.1f} - {stock['Factors'][:50]}")

    return top15
