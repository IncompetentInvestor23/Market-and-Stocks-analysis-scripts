# src/dividend_screener.py
"""
Screener for High Dividend Investing.
Emphasis in sustainability and certainty of the dividend.
"""

import numpy as np

class DividendScreener:
    """
    Evaluates stocks based on quality and dividend certainty of the dividend.
    Based on the criteria of UK Dividend Aristocrats.
    """

    def __init__(self):
        # Dividend thresholds
        # Min Yield 3%
        self.min_yield = 3.0
        # Max Yield 10% (to avoid traps)
        self.max_yield = 10.0
        # Max payout rate %
        self.max_payout = 70
        # Min dividend years
        self.min_years_dividend = 7

    def analyze(self, stock_data):
        """
        Calculates dividend rating for a stock.
        """

        info = stock_data.get('info', {})
        health = stock_data.get('health_analysis', {})

        score = 0
        max_score = 10
        factors = []
        metrics = {}

        # 1. Dividend Yield (attractive but not excessive)
        # FIX: Yahoo Finance can return dividendYield as decimal (0.035) or
        # as percentage (3.5) depending on the ticker/region. Normalise to %.
        div_yield_raw = info.get('dividendYield', 0) or 0
        div_yield_pct = div_yield_raw * 100 if div_yield_raw < 1 else div_yield_raw
        metrics['dividend_yield'] = div_yield_pct

        if div_yield_pct > self.max_yield:
            score += 0
            factors.append(f"Yield too high: {div_yield_pct:.1f}% (possible trap)")
        elif div_yield_pct > 5:
            score += 3
            factors.append(f"Yield Excellent: {div_yield_pct:.1f}%")
        elif div_yield_pct > self.min_yield:
            score += 2
            factors.append(f"Yield Good: {div_yield_pct:.1f}%")
        elif div_yield_pct > 0:
            score += 1
            factors.append(f"Yield Low: {div_yield_pct:.1f}%")
        else:
            factors.append("Doesn't pay dividend")

        # 2. Payout Ratio (sustainability)
        payout = info.get('payoutRatio', np.nan)
        if not np.isnan(payout):
            payout_pct = payout * 100
            metrics['payout_ratio'] = payout_pct

            if payout_pct < 50:
                score += 2.5
                factors.append(f"Payout Conservative: {payout_pct:.0f}%")
            elif payout_pct < self.max_payout:
                score += 1.5
                factors.append(f"Payout Moderate: {payout_pct:.0f}%")
            else:
                score -= 1
                factors.append(f"Payout Unsustainable: {payout_pct:.0f}%")

        # 3. Dividend Growth (increases records)
        div_growth = info.get('dividendGrowth', np.nan)
        metrics['dividend_growth'] = div_growth * 100 if not np.isnan(div_growth) else 0

        if not np.isnan(div_growth) and div_growth > 0.05:
            score += 2
            factors.append(f"Dividend Growth: {div_growth*100:.0f}%")
        elif not np.isnan(div_growth) and div_growth > 0:
            score += 1
            factors.append(f"Dividend Growth Modest: {div_growth*100:.0f}%")

        # 4. Free Cash Flow Coverage
        # FIX: freeCashflow is the total company FCF in £.
        # dividendRate is the per-share annual dividend in £.
        # Multiplying by sharesOutstanding gives total dividends paid,
        # so the coverage ratio uses consistent units (£ total vs £ total).
        fcf = info.get('freeCashflow', 0) or 0
        div_rate = info.get('dividendRate', 0) or 0
        shares = info.get('sharesOutstanding', 0) or 0
        total_dividends_paid = div_rate * shares  # Total £ paid in dividends

        if total_dividends_paid > 0:
            if fcf > 0:
                fcf_coverage = fcf / total_dividends_paid
                metrics['fcf_coverage'] = fcf_coverage

                if fcf_coverage > 2:
                    score += 2.5
                    factors.append(f"FCF covers: {fcf_coverage:.1f}x dividend")
                elif fcf_coverage > 1:
                    score += 1.5
                    factors.append(f"FCF Tight: {fcf_coverage:.1f}x")
                else:
                    factors.append(f"FCF Insufficient: {fcf_coverage:.1f}x")
            else:
                metrics['fcf_coverage'] = 0
                factors.append("FCF Negative")
        else:
            metrics['fcf_coverage'] = 0

        # 5. Bonus: Financial health (critical for dividends)
        health_score = health.get('health_score', 0)

        if health_score >= 4:
            score += 1
            factors.append("Balance Solid")
        elif health_score < 3:
            score -= 1
            factors.append("Balance Weak - dividend at risk")

        # Normalize score to 0-10
        final_score = max(0, min(score, 10))

        return {
            'dividend_score': final_score,
            'factors': factors[:4],
            'metrics': metrics
        }

def get_top5_dividend(healthy_stocks):
    """
    Select top 5 stocks for dividend investing.
    """
    screener = DividendScreener()
    results = []

    print("\n Analysing for DIVIDEND INVESTING...")

    for stock in healthy_stocks:
        ticker = stock.get('Ticker', '')
        analysis = screener.analyze(stock)

        # Only consider stocks that pay a dividend
        if analysis['metrics'].get('dividend_yield', 0) > 0:
            results.append({
                'Ticker': ticker,
                'Name': stock['info'].get('longName', 'N/A')[:30],
                'Price': stock['info'].get('currentPrice', 0),
                'Dividend Score': analysis['dividend_score'],
                'Yield %': analysis['metrics'].get('dividend_yield', 0),
                'Payout %': analysis['metrics'].get('payout_ratio', 0),
                'FCF Coverage': analysis['metrics'].get('fcf_coverage', 0),
                'Factors': ', '.join(analysis['factors'])
            })

    # Order by score and take top 5
    top5 = sorted(results, key=lambda x: x['Dividend Score'], reverse=True)[:5]

    print(f"\n TOP 5 DIVIDEND STOCKS:")
    for i, stock in enumerate(top5, 1):
        print(f" {i}. {stock['Ticker']}: Score {stock['Dividend Score']:.1f} - Yield {stock['Yield %']:.1f}%")

    return top5
