"""
Difference between current price and ATH
Indices: S&P 500, NASDAQ 100, FTSE 100, FTSE 250
"""

import yfinance as yf
from datetime import datetime

INDICES = {
    "S&P 500":    "^GSPC",
    "NASDAQ 100": "^NDX",
    "FTSE 100":   "^FTSE",
    "FTSE 250":   "^FTMC",
}

def get_data(ticker_symbol: str) -> dict:
    ticker = yf.Ticker(ticker_symbol)

    # Current Price (last available close)
    hist_recent = ticker.history(period="5d")
    if hist_recent.empty:
        raise ValueError(f"Not available data for {ticker_symbol}")
    current_price = hist_recent["Close"].iloc[-1]

    # ATH
    hist_all = ticker.history(period="max")
    all_time_high = hist_all["High"].max()
    ath_date = hist_all["High"].idxmax().date()

    diff_abs = current_price - all_time_high
    diff_pct = (diff_abs / all_time_high) * 100

    return {
        "current":   current_price,
        "ath":       all_time_high,
        "ath_date":  ath_date,
        "diff_abs":  diff_abs,
        "diff_pct":  diff_pct,
    }

def main():
    width = 70
    print("=" * width)
    print(f"{'CURRENT PRICE vs ATH':^{width}}")
    print(f"{'Date of request: ' + datetime.now().strftime('%d/%m/%Y %H:%M'):^{width}}")
    print("=" * width)

    for name, symbol in INDICES.items():
        print(f"\n📊  {name}  ({symbol})")
        print("-" * width)
        try:
            d = get_data(symbol)

            status = "🔴 Lower than ATH" if d["diff_pct"] < -0.1 else "🟢 On ATH"

            print(f"  Current Price :  {d['current']:>12,.2f}")
            print(f"  ATH  :  {d['ath']:>12,.2f}  (reached on {d['ath_date']})")
            print(f"  Difference    :  {d['diff_abs']:>+12,.2f}  ({d['diff_pct']:>+.2f}%)")
            print(f"  Status        :  {status}")

        except Exception as e:
            print(f"  ⚠️  Error obtaining data: {e}")

    print("\n" + "=" * width)
    print("Data Source: Yahoo Finance (yfinance)")
    print("=" * width)

if __name__ == "__main__":
    main()"""
